module MistrasDTAJulia

export DTAData, DTAFormatError, HitRecord, WaveformRecord, read_dta, waveform_axes

struct DTAFormatError <: Exception
    offset::Int
    message::String
end

Base.showerror(io::IO, error::DTAFormatError) =
    print(io, error.message, " at byte offset ", error.offset)

struct HitRecord
    time_s::Float64
    channel::UInt8
    features::Dict{Symbol,Float64}
end

Base.:(==)(left::HitRecord, right::HitRecord) =
    left.time_s == right.time_s &&
    left.channel == right.channel &&
    left.features == right.features

struct WaveformRecord
    time_s::Float64
    channel::UInt8
    sample_rate_hz::Int
    trigger_delay_samples::Int
    raw_counts::Vector{Int16}
    voltage_v::Vector{Float64}
end

Base.:(==)(left::WaveformRecord, right::WaveformRecord) =
    left.time_s == right.time_s &&
    left.channel == right.channel &&
    left.sample_rate_hz == right.sample_rate_hz &&
    left.trigger_delay_samples == right.trigger_delay_samples &&
    left.raw_counts == right.raw_counts &&
    left.voltage_v == right.voltage_v

struct DTAData
    hits::Vector{HitRecord}
    waveforms::Vector{WaveformRecord}
    unknown_message_counts::Dict{UInt8,Int}
end

mutable struct ParserState
    chids::Vector{UInt8}
    gains_db::Dict{UInt8,UInt8}
    hardware::Dict{UInt8,Tuple{Int,Int}}
    setup_seen::Bool
end

ParserState() = ParserState(UInt8[], Dict{UInt8,UInt8}(), Dict{UInt8,Tuple{Int,Int}}(), false)

const CHID_NAMES = Dict{UInt8,Symbol}(
    1 => :RISE,
    2 => :PCNTS,
    3 => :COUN,
    4 => :ENER,
    5 => :DURATION,
    6 => :AMP,
    8 => :ASL,
    10 => :THR,
    13 => Symbol("A-FRQ"),
    17 => :RMS,
    18 => Symbol("R-FRQ"),
    19 => Symbol("I-FRQ"),
    20 => Symbol("SIG STRENGTH"),
    21 => Symbol("ABS-ENERGY"),
    23 => Symbol("FRQ-C"),
    24 => Symbol("P-FRQ"),
)

const CHID_WIDTHS = Dict{UInt8,Int}(
    1 => 2,
    2 => 2,
    3 => 2,
    4 => 2,
    5 => 4,
    6 => 1,
    8 => 1,
    10 => 1,
    13 => 2,
    17 => 2,
    18 => 2,
    19 => 2,
    20 => 4,
    21 => 4,
    23 => 2,
    24 => 2,
)

const SUPPORTED_CHIDS = UInt8[1, 3, 4, 5, 6, 21, 23, 24]

const KNOWN_IGNORED_MESSAGES = Set{UInt8}([
    2, 7, 8, 11, 38, 41, 44, 49, 99, 107, 116, 128, 129, 130,
])

function _require(data, position::Int, count::Int, offset::Int, what::AbstractString)
    count >= 0 || throw(DTAFormatError(offset + position - 1, "invalid $what length"))
    position >= 1 || throw(DTAFormatError(offset, "invalid $what position"))
    position + count - 1 <= length(data) ||
        throw(DTAFormatError(offset + position - 1, "truncated $what"))
end

function _u16(data, position::Int, offset::Int)
    _require(data, position, 2, offset, "UInt16")
    UInt16(data[position]) | (UInt16(data[position + 1]) << 8)
end

function _u32(data, position::Int, offset::Int)
    _require(data, position, 4, offset, "UInt32")
    UInt32(data[position]) |
    (UInt32(data[position + 1]) << 8) |
    (UInt32(data[position + 2]) << 16) |
    (UInt32(data[position + 3]) << 24)
end

_i16(data, position::Int, offset::Int) = reinterpret(Int16, _u16(data, position, offset))
_i32(data, position::Int, offset::Int) = reinterpret(Int32, _u32(data, position, offset))
_f32(data, position::Int, offset::Int) = reinterpret(Float32, _u32(data, position, offset))

function _u48_at(data, position::Int, offset::Int)
    _require(data, position, 6, offset, "48-bit timestamp")
    value = UInt64(0)
    for index in 0:5
        value |= UInt64(data[position + index]) << (8 * index)
    end
    value
end

_u48(data, offset::Int) = _u48_at(data, 1, offset)

function _parse_setup!(state::ParserState, body, body_offset::Int)
    _require(body, 1, 2, body_offset, "Msg-42 version")
    cursor = 3
    while cursor <= length(body)
        _require(body, cursor, 2, body_offset, "setup subrecord length")
        subrecord_length = Int(_u16(body, cursor, body_offset))
        subrecord_length >= 1 ||
            throw(DTAFormatError(body_offset + cursor - 1, "invalid setup subrecord length"))
        _require(body, cursor + 2, subrecord_length, body_offset, "setup subrecord")

        subid = body[cursor + 2]
        payload_start = cursor + 3

        if subid == 5
            _require(body, payload_start, 1, body_offset, "CHID count")
            count = Int(body[payload_start])
            _require(body, payload_start + 1, count, body_offset, "CHID list")
            chids = collect(body[payload_start+1:payload_start+count])
            for chid in chids
                haskey(CHID_WIDTHS, chid) ||
                    throw(DTAFormatError(
                        body_offset + payload_start,
                        "unknown CHID $(Int(chid))",
                    ))
            end
            state.chids = chids
        elseif subid == 23
            _require(body, payload_start, 2, body_offset, "channel gain")
            state.gains_db[body[payload_start]] = body[payload_start + 1]
        elseif subid == 173
            _require(body, payload_start, 1, body_offset, "hardware setup subtype")
            if body[payload_start] == 42
                _require(body, payload_start + 1, 24, body_offset, "hardware setup")
                hardware_start = payload_start + 1
                channel = body[hardware_start + 7]
                sample_rate_hz = 1000 * Int(_u16(body, hardware_start + 12, body_offset))
                trigger_delay = Int(_i16(body, hardware_start + 18, body_offset))
                state.hardware[channel] = (sample_rate_hz, trigger_delay)
            end
        end

        cursor += 2 + subrecord_length
    end
    cursor == length(body) + 1 ||
        throw(DTAFormatError(body_offset + cursor - 1, "invalid setup record boundary"))
    state.chids == SUPPORTED_CHIDS ||
        throw(DTAFormatError(body_offset, "unsupported DTA feature layout"))
    state.setup_seen = true
end

function _parse_feature(chid::UInt8, body, position::Int, body_offset::Int)
    width = get(CHID_WIDTHS, chid, 0)
    width > 0 ||
        throw(DTAFormatError(body_offset + position - 1, "unknown CHID $(Int(chid))"))
    _require(body, position, width, body_offset, "CHID $(Int(chid)) value")

    value = if chid == 17
        Float64(_u16(body, position, body_offset)) / 5000.0
    elseif chid == 5
        Float64(_i32(body, position, body_offset))
    elseif chid == 20
        Float64(_i32(body, position, body_offset)) * 3.05
    elseif chid == 21
        Float64(_f32(body, position, body_offset)) * 9.31e-4
    elseif width == 1
        Float64(body[position])
    elseif width == 2
        Float64(_u16(body, position, body_offset))
    else
        throw(DTAFormatError(body_offset + position - 1, "unsupported CHID $(Int(chid))"))
    end
    value, width
end

function _parse_hit(state::ParserState, body, body_offset::Int)
    state.setup_seen ||
        throw(DTAFormatError(body_offset, "Msg-1 encountered before hardware setup"))
    isempty(state.chids) &&
        throw(DTAFormatError(body_offset, "Msg-1 encountered without a CHID definition"))
    _require(body, 1, 7, body_offset, "Msg-1 header")

    time_s = Float64(_u48_at(body, 1, body_offset)) * 0.25e-6
    channel = body[7]
    cursor = 8
    features = Dict{Symbol,Float64}()
    for chid in state.chids
        value, width = _parse_feature(chid, body, cursor, body_offset)
        features[CHID_NAMES[chid]] = value
        cursor += width
    end
    HitRecord(time_s, channel, features)
end

function _parse_waveform(state::ParserState, body, body_offset::Int)
    state.setup_seen ||
        throw(DTAFormatError(body_offset, "Msg-173 encountered before hardware setup"))
    _require(body, 1, 9, body_offset, "Msg-173 header")
    body[1] == 1 ||
        throw(DTAFormatError(body_offset, "unsupported Msg-173 waveform layout"))

    time_s = Float64(_u48_at(body, 2, body_offset)) * 0.25e-6
    channel = body[8]
    haskey(state.gains_db, channel) ||
        throw(DTAFormatError(body_offset + 7, "missing gain setup for channel $(Int(channel))"))
    haskey(state.hardware, channel) ||
        throw(DTAFormatError(body_offset + 7, "missing hardware setup for channel $(Int(channel))"))

    sample_bytes = length(body) - 9
    iseven(sample_bytes) ||
        throw(DTAFormatError(body_offset + 9, "unsupported Msg-173 waveform layout"))
    raw_counts = Vector{Int16}(undef, sample_bytes ÷ 2)
    cursor = 10
    for index in eachindex(raw_counts)
        raw_counts[index] = _i16(body, cursor, body_offset)
        cursor += 2
    end

    gain = 10.0^(Float64(state.gains_db[channel]) / 20.0)
    scale = 10.0 / (gain * 32768.0)
    voltage = Float64.(raw_counts) .* scale
    sample_rate_hz, trigger_delay = state.hardware[channel]
    WaveformRecord(
        time_s,
        channel,
        sample_rate_hz,
        trigger_delay,
        raw_counts,
        voltage,
    )
end

"""
    read_dta(path; read_waveforms=true) -> DTAData

Read the tested AEWin/Mistras DTA dialect. Unsupported layouts fail explicitly
instead of returning guessed data.
"""
function read_dta(path::AbstractString; read_waveforms::Bool=true)
    raw = read(path)
    isempty(raw) && throw(DTAFormatError(0, "empty DTA file"))

    hits = HitRecord[]
    waveforms = WaveformRecord[]
    unknown = Dict{UInt8,Int}()
    state = ParserState()
    position = 1

    while position <= length(raw)
        frame_offset = position - 1
        _require(raw, position, 2, 0, "frame length")
        frame_length = Int(_u16(raw, position, 0))
        frame_length >= 1 ||
            throw(DTAFormatError(frame_offset, "invalid frame length"))
        _require(raw, position + 2, frame_length, 0, "frame")

        message_id = raw[position + 2]
        body_start = position + 3
        body_end = position + 1 + frame_length
        if 40 <= message_id <= 49
            frame_length >= 2 ||
                throw(DTAFormatError(frame_offset, "missing secondary message ID"))
            body_start += 1
        end
        body = @view raw[body_start:body_end]
        body_offset = body_start - 1

        if message_id == 42
            _parse_setup!(state, body, body_offset)
        elseif message_id == 1
            push!(hits, _parse_hit(state, body, body_offset))
        elseif message_id == 173
            read_waveforms && push!(waveforms, _parse_waveform(state, body, body_offset))
        elseif !(message_id in KNOWN_IGNORED_MESSAGES)
            unknown[message_id] = get(unknown, message_id, 0) + 1
        end

        position = body_end + 1
    end

    DTAData(hits, waveforms, unknown)
end

"""
    waveform_axes(waveform; time_unit=:us)

Return the trigger-delay-adjusted time axis and the already scaled voltage.
"""
function waveform_axes(waveform::WaveformRecord; time_unit::Symbol=:us)
    multiplier = time_unit === :us ? 1e6 : time_unit === :s ? 1.0 :
        throw(ArgumentError("time_unit must be :us or :s"))
    time = (
        (collect(0:length(waveform.voltage_v)-1) .+ waveform.trigger_delay_samples) ./
        waveform.sample_rate_hz
    ) .* multiplier
    (time=time, voltage=waveform.voltage_v)
end

end
