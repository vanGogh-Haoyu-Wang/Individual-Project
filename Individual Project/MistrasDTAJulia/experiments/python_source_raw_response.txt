module MistrasDTAJulia

export read_dta, waveform_axes, DTAData, HitRecord, WaveformRecord

struct HitRecord
    relative_time::Float64
    channel::UInt8
    features::Dict{String,Any}
end

struct WaveformRecord
    relative_time::Float64
    channel::UInt8
    sample_rate::Float64
    trigger_delay::Int
    samples::Vector{Int16}
    voltage::Vector{Float64}
    subid::UInt8
    alb::UInt8
end

WaveformRecord(relative_time, channel, sample_rate, trigger_delay, samples::Vector{Int16}, voltage::Vector{Float64}) =
    WaveformRecord(Float64(relative_time), UInt8(channel), Float64(sample_rate), Int(trigger_delay), samples, voltage, UInt8(0), UInt8(0))

struct DTAData
    hits::Vector{HitRecord}
    waveforms::Vector{WaveformRecord}
    unknown_counts::Dict{UInt8,Int}
end

struct ChannelSetup
    sample_rate::Float64
    trigger_delay::Int
end

function Base.getproperty(x::HitRecord, s::Symbol)
    if s === :time || s === :relative_time_seconds || s === :rtot
        return getfield(x, :relative_time)
    end
    return getfield(x, s)
end

function Base.getproperty(x::WaveformRecord, s::Symbol)
    if s === :time || s === :relative_time_seconds || s === :rtot
        return getfield(x, :relative_time)
    elseif s === :sample_rate_hz || s === :srate
        return getfield(x, :sample_rate)
    elseif s === :tdly || s === :trigger_delay_samples
        return getfield(x, :trigger_delay)
    elseif s === :raw_samples
        return getfield(x, :samples)
    elseif s === :scaled_voltage
        return getfield(x, :voltage)
    end
    return getfield(x, s)
end

function Base.getproperty(x::DTAData, s::Symbol)
    if s === :unknown_message_counts || s === :unknown_messages
        return getfield(x, :unknown_counts)
    end
    return getfield(x, s)
end

Base.:(==)(a::HitRecord, b::HitRecord) =
    getfield(a, :relative_time) == getfield(b, :relative_time) &&
    getfield(a, :channel) == getfield(b, :channel) &&
    getfield(a, :features) == getfield(b, :features)

Base.:(==)(a::WaveformRecord, b::WaveformRecord) =
    getfield(a, :relative_time) == getfield(b, :relative_time) &&
    getfield(a, :channel) == getfield(b, :channel) &&
    getfield(a, :sample_rate) == getfield(b, :sample_rate) &&
    getfield(a, :trigger_delay) == getfield(b, :trigger_delay) &&
    getfield(a, :samples) == getfield(b, :samples) &&
    getfield(a, :voltage) == getfield(b, :voltage) &&
    getfield(a, :subid) == getfield(b, :subid) &&
    getfield(a, :alb) == getfield(b, :alb)

Base.:(==)(a::DTAData, b::DTAData) =
    getfield(a, :hits) == getfield(b, :hits) &&
    getfield(a, :waveforms) == getfield(b, :waveforms) &&
    getfield(a, :unknown_counts) == getfield(b, :unknown_counts)

const CHID_NAMES = Dict{UInt8,String}(
    UInt8(1) => "RISE",
    UInt8(2) => "PCNTS",
    UInt8(3) => "COUN",
    UInt8(4) => "ENER",
    UInt8(5) => "DURATION",
    UInt8(6) => "AMP",
    UInt8(8) => "ASL",
    UInt8(10) => "THR",
    UInt8(13) => "A-FRQ",
    UInt8(17) => "RMS",
    UInt8(18) => "R-FRQ",
    UInt8(19) => "I-FRQ",
    UInt8(20) => "SIG STRENGTH",
    UInt8(21) => "ABS-ENERGY",
    UInt8(23) => "FRQ-C",
    UInt8(24) => "P-FRQ",
)

const CHID_BYTE_LENGTHS = Dict{UInt8,Int}(
    UInt8(1) => 2,
    UInt8(2) => 2,
    UInt8(3) => 2,
    UInt8(4) => 2,
    UInt8(5) => 4,
    UInt8(6) => 1,
    UInt8(8) => 1,
    UInt8(10) => 1,
    UInt8(13) => 2,
    UInt8(17) => 2,
    UInt8(18) => 2,
    UInt8(19) => 2,
    UInt8(20) => 4,
    UInt8(21) => 4,
    UInt8(23) => 2,
    UInt8(24) => 2,
)

mutable struct Cursor
    data::Vector{UInt8}
    pos::Int
    limit::Int
end

_remaining(r::Cursor) = r.limit - r.pos

function _need!(r::Cursor, n::Int, what::AbstractString)
    if _remaining(r) < n
        error("truncated $what at byte offset $(r.pos): need $n bytes, have $(_remaining(r))")
    end
    return nothing
end

function _read_u8!(r::Cursor, what::AbstractString)
    _need!(r, 1, what)
    value = r.data[r.pos + 1]
    r.pos += 1
    return value
end

function _read_u16le!(r::Cursor, what::AbstractString)
    _need!(r, 2, what)
    i = r.pos + 1
    value = UInt16(r.data[i]) | (UInt16(r.data[i + 1]) << 8)
    r.pos += 2
    return value
end

function _read_u32le!(r::Cursor, what::AbstractString)
    _need!(r, 4, what)
    i = r.pos + 1
    value = UInt32(r.data[i]) |
            (UInt32(r.data[i + 1]) << 8) |
            (UInt32(r.data[i + 2]) << 16) |
            (UInt32(r.data[i + 3]) << 24)
    r.pos += 4
    return value
end

_read_i16le!(r::Cursor, what::AbstractString) = reinterpret(Int16, _read_u16le!(r, what))
_read_i32le!(r::Cursor, what::AbstractString) = reinterpret(Int32, _read_u32le!(r, what))
_read_float32le!(r::Cursor, what::AbstractString) = reinterpret(Float32, _read_u32le!(r, what))

function _read_rtot!(r::Cursor, what::AbstractString)
    _need!(r, 6, what)
    i = r.pos + 1
    low = UInt32(r.data[i]) |
          (UInt32(r.data[i + 1]) << 8) |
          (UInt32(r.data[i + 2]) << 16) |
          (UInt32(r.data[i + 3]) << 24)
    high = UInt16(r.data[i + 4]) | (UInt16(r.data[i + 5]) << 8)
    r.pos += 6
    return (Float64(low) + 4294967296.0 * Float64(high)) * 0.25e-6
end

function _skip!(r::Cursor, n::Int, what::AbstractString)
    _need!(r, n, what)
    r.pos += n
    return nothing
end

_invalid_setup(offset::Int, detail::AbstractString) =
    error("invalid setup record at byte offset $offset: $detail")

function _parse_chid_list!(r::Cursor, chid_list::Vector{UInt8})
    if _remaining(r) < 1
        _invalid_setup(r.pos, "missing CHID count")
    end

    count = Int(_read_u8!(r, "CHID count"))
    if _remaining(r) < count
        _invalid_setup(r.pos, "CHID list declares $count entries but only $(_remaining(r)) bytes remain")
    end

    empty!(chid_list)
    for _ in 1:count
        offset = r.pos
        chid = _read_u8!(r, "CHID")
        if !(haskey(CHID_NAMES, chid) && haskey(CHID_BYTE_LENGTHS, chid))
            error("unknown CHID $(Int(chid)) at byte offset $offset")
        end
        push!(chid_list, chid)
    end

    return nothing
end

function _parse_gain!(r::Cursor, gains::Dict{UInt8,UInt8})
    if _remaining(r) < 2
        _invalid_setup(r.pos, "gain record is shorter than 2 bytes")
    end
    channel = _read_u8!(r, "gain channel")
    gain = _read_u8!(r, "gain value")
    gains[channel] = gain
    return nothing
end

function _parse_hardware_setup!(r::Cursor, setups::Dict{UInt8,ChannelSetup})
    _ = _read_u8!(r, "hardware setup MVERN")
    _ = _read_u8!(r, "hardware setup secondary ID")
    _ = _read_u8!(r, "hardware setup ADT")
    _ = _read_u8!(r, "hardware setup SETS")
    _skip!(r, 1, "hardware setup padding")
    _ = _read_u16le!(r, "hardware setup SLEN")
    channel = _read_u8!(r, "hardware setup channel")
    _ = _read_u16le!(r, "hardware setup HLK")
    _skip!(r, 2, "hardware setup padding")
    sample_rate = 1000.0 * Float64(_read_u16le!(r, "hardware setup sample rate"))
    _ = _read_u16le!(r, "hardware setup TMODE")
    _ = _read_u16le!(r, "hardware setup TSRC")
    trigger_delay = Int(_read_i16le!(r, "hardware setup trigger delay"))
    _ = _read_u16le!(r, "hardware setup MXIN")
    _ = _read_u16le!(r, "hardware setup THRD")
    setups[channel] = ChannelSetup(sample_rate, trigger_delay)
    return nothing
end

function _parse_nested_173_setup!(r::Cursor, setups::Dict{UInt8,ChannelSetup})
    if _remaining(r) < 1
        _invalid_setup(r.pos, "missing nested setup SUBID")
    end

    nested_subid = _read_u8!(r, "nested setup SUBID")
    if nested_subid == UInt8(42)
        if _remaining(r) < 24
            _invalid_setup(r.pos, "hardware setup is shorter than 24 bytes")
        end
        body = Cursor(r.data, r.pos, r.pos + 24)
        _parse_hardware_setup!(body, setups)
        r.pos = body.limit
    end

    return nothing
end

function _parse_setup!(r::Cursor, chid_list::Vector{UInt8}, gains::Dict{UInt8,UInt8}, setups::Dict{UInt8,ChannelSetup})
    if _remaining(r) < 2
        _invalid_setup(r.pos, "missing message version")
    end
    _skip!(r, 2, "setup message version")

    while r.pos < r.limit
        sub_start = r.pos
        if _remaining(r) < 2
            _invalid_setup(sub_start, "missing subrecord length")
        end

        sub_len = Int(_read_u16le!(r, "setup subrecord length"))
        if sub_len < 1
            _invalid_setup(sub_start, "subrecord length $sub_len is too short")
        end

        after_length = r.pos
        sub_end = after_length + sub_len
        if sub_end > r.limit
            _invalid_setup(sub_start, "subrecord length $sub_len exceeds setup frame")
        end

        sub = Cursor(r.data, after_length, sub_end)
        subid = _read_u8!(sub, "setup SUBID")

        if subid == UInt8(5)
            _parse_chid_list!(sub, chid_list)
        elseif subid == UInt8(23)
            _parse_gain!(sub, gains)
        elseif subid == UInt8(173)
            _parse_nested_173_setup!(sub, setups)
        end

        r.pos = sub_end
    end

    return nothing
end

function _parse_feature!(r::Cursor, chid::UInt8)
    if !haskey(CHID_BYTE_LENGTHS, chid)
        error("unknown CHID $(Int(chid)) at byte offset $(r.pos)")
    end

    if chid == UInt8(17)
        return Float64(_read_u16le!(r, "RMS feature")) / 5000.0
    elseif chid == UInt8(5)
        return Int(_read_i32le!(r, "DURATION feature"))
    elseif chid == UInt8(20)
        return Float64(_read_i32le!(r, "SIG STRENGTH feature")) * 3.05
    elseif chid == UInt8(21)
        return Float64(_read_float32le!(r, "ABS-ENERGY feature")) * 9.31e-4
    end

    byte_length = CHID_BYTE_LENGTHS[chid]
    if byte_length == 1
        return Int(_read_u8!(r, "hit feature"))
    elseif byte_length == 2
        return Int(_read_u16le!(r, "hit feature"))
    elseif byte_length == 4
        return Int(_read_u32le!(r, "hit feature"))
    end

    error("unknown CHID $(Int(chid)) at byte offset $(r.pos)")
end

function _parse_hit!(r::Cursor, chid_list::Vector{UInt8})
    relative_time = _read_rtot!(r, "hit relative time")
    channel = _read_u8!(r, "hit channel")
    features = Dict{String,Any}()

    for chid in chid_list
        offset = r.pos
        name = get(CHID_NAMES, chid, nothing)
        if name === nothing
            error("unknown CHID $(Int(chid)) at byte offset $offset")
        end

        byte_length = CHID_BYTE_LENGTHS[chid]
        if _remaining(r) < byte_length
            error("truncated hit feature at byte offset $offset: CHID $(Int(chid)) needs $byte_length bytes, have $(_remaining(r))")
        end

        features[name] = _parse_feature!(r, chid)
    end

    return HitRecord(relative_time, channel, features)
end

function _parse_waveform!(r::Cursor, gains::Dict{UInt8,UInt8}, setups::Dict{UInt8,ChannelSetup}, frame_start::Int)
    subid = _read_u8!(r, "waveform SUBID")
    relative_time = _read_rtot!(r, "waveform relative time")
    channel = _read_u8!(r, "waveform channel")
    alb = _read_u8!(r, "waveform ALB")

    sample_bytes = _remaining(r)
    if isodd(sample_bytes)
        error("unsupported waveform layout at byte offset $(r.pos): Int16 payload has odd byte length $sample_bytes")
    end

    if !haskey(setups, channel)
        error("missing channel setup for channel $(Int(channel)) at byte offset $frame_start")
    end

    if !haskey(gains, channel)
        error("missing channel setup for channel $(Int(channel)): gain is unavailable at byte offset $frame_start")
    end

    count = sample_bytes ÷ 2
    samples = Vector{Int16}(undef, count)
    for i in 1:count
        samples[i] = _read_i16le!(r, "waveform samples")
    end

    gain = 10.0 ^ (Float64(gains[channel]) / 20.0)
    scale = 10.0 / (gain * 32768.0)
    voltage = Vector{Float64}(undef, count)
    for i in 1:count
        voltage[i] = scale * Float64(samples[i])
    end

    setup = setups[channel]
    return WaveformRecord(relative_time, channel, setup.sample_rate, setup.trigger_delay, samples, voltage, subid, alb)
end

_is_known_skipped_message(id::UInt8) =
    id == UInt8(7) ||
    id == UInt8(8) ||
    id == UInt8(41) ||
    id == UInt8(99) ||
    id == UInt8(128) ||
    id == UInt8(129) ||
    id == UInt8(130)

function read_dta(path; read_waveforms=true)
    bytes = read(path)
    stream = Cursor(bytes, 0, length(bytes))

    hits = HitRecord[]
    waveforms = WaveformRecord[]
    unknown_counts = Dict{UInt8,Int}()

    chid_list = UInt8[]
    gains = Dict{UInt8,UInt8}()
    setups = Dict{UInt8,ChannelSetup}()

    while stream.pos < stream.limit
        frame_start = stream.pos
        frame_length = Int(_read_u16le!(stream, "frame length"))

        if frame_length < 1
            error("invalid frame length at byte offset $frame_start: declared length $frame_length")
        end

        if _remaining(stream) < frame_length
            error("truncated frame at byte offset $frame_start: declared length $frame_length exceeds remaining $(_remaining(stream)) bytes")
        end

        frame_end = stream.pos + frame_length
        message_id = _read_u8!(stream, "message ID")

        if 40 <= Int(message_id) <= 49
            if stream.pos >= frame_end
                error("truncated frame at byte offset $frame_start: missing additional ID byte at byte offset $(stream.pos)")
            end
            _ = _read_u8!(stream, "additional message ID")
        end

        payload = Cursor(bytes, stream.pos, frame_end)

        if message_id == UInt8(1)
            push!(hits, _parse_hit!(payload, chid_list))
        elseif message_id == UInt8(42)
            _parse_setup!(payload, chid_list, gains, setups)
        elseif message_id == UInt8(173)
            if read_waveforms
                push!(waveforms, _parse_waveform!(payload, gains, setups, frame_start))
            end
        elseif !_is_known_skipped_message(message_id)
            unknown_counts[message_id] = get(unknown_counts, message_id, 0) + 1
        end

        stream.pos = frame_end
    end

    return DTAData(hits, waveforms, unknown_counts)
end

function _time_multiplier(time_unit)
    if time_unit === :s || time_unit === :sec || time_unit === :second || time_unit === :seconds
        return 1.0
    elseif time_unit === :ms || time_unit === :millisecond || time_unit === :milliseconds
        return 1.0e3
    elseif time_unit === :us || time_unit === :microsecond || time_unit === :microseconds
        return 1.0e6
    elseif time_unit === :ns || time_unit === :nanosecond || time_unit === :nanoseconds
        return 1.0e9
    end
    throw(ArgumentError("unsupported time_unit: $(repr(time_unit))"))
end

function waveform_axes(waveform::WaveformRecord; time_unit=:us)
    multiplier = _time_multiplier(time_unit)
    samples = getfield(waveform, :samples)
    sample_rate = getfield(waveform, :sample_rate)
    trigger_delay = Float64(getfield(waveform, :trigger_delay))

    time = Vector{Float64}(undef, length(samples))
    for i in eachindex(time)
        time[i] = multiplier * ((Float64(i - 1) + trigger_delay) / sample_rate)
    end

    return time, getfield(waveform, :voltage)
end

end