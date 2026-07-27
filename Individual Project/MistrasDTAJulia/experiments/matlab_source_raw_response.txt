module MistrasDTAJulia

export DTAData, HitRecord, WaveformRecord, read_dta, waveform_axes

const COUNTER_HZ = 4_000_000.0
const VOLTS_PER_COUNT = 0.000305
const ABSOLUTE_ENERGY_IMPEDANCE_OHMS = 10_000_000.0

struct HitRecord
    relative_time::Float64
    channel::UInt8
    features::Dict{Symbol,Any}
end

struct WaveformRecord
    relative_time::Float64
    channel::UInt8
    sample_rate::Float64
    trigger_delay::Float64
    raw_samples::Vector{Int16}
    voltage::Vector{Float64}
    subid::UInt8
    alb::UInt8
    rms::Float64
    signal_strength::Float64
    absolute_energy::Float64
end

struct DTAData
    hits::Vector{HitRecord}
    waveforms::Vector{WaveformRecord}
    unknown_message_counts::Dict{Int,Int}
end

struct ChannelSetup
    gain::Float64
    sample_rate::Float64
    trigger_delay::Float64
end

struct SetupState
    feature_chids::Vector{UInt8}
    channels::Dict{UInt8,ChannelSetup}
end

const FEATURE_NAMES = Dict{UInt8,Symbol}(
    0x01 => :risetime_us,
    0x03 => :counts,
    0x04 => :energy_u,
    0x05 => :duration_us,
    0x06 => :amplitude_db,
    0x15 => :absolute_energy,
    0x17 => :signal_strength,
    0x18 => :rms,
)

const FEATURE_SIZES = Dict{UInt8,Int}(
    0x01 => 2,
    0x03 => 2,
    0x04 => 2,
    0x05 => 4,
    0x06 => 1,
    0x15 => 4,
    0x17 => 2,
    0x18 => 2,
)

const CORE_CHIDS = UInt8[0x01, 0x03, 0x04, 0x05, 0x06]

function read_dta(path; read_waveforms=true)
    bytes = read(path)
    hits = HitRecord[]
    waveforms = WaveformRecord[]
    unknowns = Dict{Int,Int}()
    setup = nothing

    pos = 1
    n = length(bytes)

    while pos <= n
        if n - pos + 1 < 3
            fail("truncated frame header", pos - 1)
        end

        frame_offset = pos - 1
        frame_len = Int(le_u16(bytes, pos))
        frame_len < 1 && fail("invalid frame length", frame_offset)

        frame_end = pos + 1 + frame_len
        frame_end > n && fail("truncated frame", frame_offset)

        msgid = bytes[pos + 2]
        body_start = pos + 3
        body_offset = body_start - 1
        body = bytes[body_start:frame_end]

        if 0x28 <= msgid <= 0x31 && isempty(body)
            fail("truncated extended message id", body_offset)
        end

        if msgid == 0x2a
            setup = parse_setup(body[2:end], body_offset + 1)
        elseif msgid == 0x01
            setup === nothing && fail("missing channel setup", body_offset)
            push!(hits, parse_hit(body, body_offset, setup))
        elseif msgid == 0xad
            if read_waveforms
                setup === nothing && fail("missing channel setup", body_offset)
                push!(waveforms, parse_waveform(body, body_offset, setup))
            end
        else
            id = Int(msgid)
            unknowns[id] = get(unknowns, id, 0) + 1
        end

        pos = frame_end + 1
    end

    return DTAData(hits, waveforms, unknowns)
end

function waveform_axes(waveform::WaveformRecord; time_unit=:us)
    scale =
        time_unit === :s ? 1.0 :
        time_unit === :ms ? 1.0e3 :
        time_unit === :us ? 1.0e6 :
        time_unit === :ns ? 1.0e9 :
        throw(ArgumentError("unsupported time_unit: $(repr(time_unit))"))

    time = Vector{Float64}(undef, length(waveform.raw_samples))
    start_time = -waveform.trigger_delay
    for i in eachindex(time)
        time[i] = (start_time + (i - 1) / waveform.sample_rate) * scale
    end

    return time, copy(waveform.voltage)
end

function parse_setup(body::Vector{UInt8}, body_offset::Int)
    isempty(body) && fail("invalid setup record", body_offset)

    chids = find_feature_chids(body, body_offset)
    channels = find_channel_setups(body, body_offset)
    isempty(channels) && fail("invalid setup record: missing channel setup records", body_offset)

    return SetupState(chids, channels)
end

function find_feature_chids(body::Vector{UInt8}, body_offset::Int)
    best = nothing
    best_score = -1

    for p in 1:max(0, length(body) - 2)
        body[p] == 0x05 || continue

        count = Int(body[p + 1])
        1 <= count <= 32 || continue
        p + 1 + count <= length(body) || fail("invalid setup record", body_offset + p - 1)

        ids = Vector{UInt8}(body[p + 2:p + 1 + count])
        core_count = count(id -> id in ids, CORE_CHIDS)
        core_count >= 3 || continue

        for (i, id) in pairs(ids)
            haskey(FEATURE_SIZES, id) || fail("unknown CHID $(Int(id))", body_offset + p + i)
        end

        score = core_count * 100 + count
        if score > best_score
            best = ids
            best_score = score
        end
    end

    best === nothing && fail("invalid setup record: missing dynamic CHID list", body_offset)
    return best
end

function find_channel_setups(body::Vector{UInt8}, body_offset::Int)
    gains = Dict{UInt8,Float64}()
    sample_rates = Dict{UInt8,Float64}()
    trigger_delays = Dict{UInt8,Float64}()

    p = 1
    while p <= length(body) - 1
        record_len = Int(le_u16(body, p))
        payload_start = p + 2
        payload_end = p + 1 + record_len

        if record_len == 8 && payload_start + 3 <= length(body)
            if body[payload_start] == 0x13 &&
               body[payload_start + 1] == 0x64 &&
               body[payload_start + 2] == 0x00
                payload_end <= length(body) || fail("invalid setup record", body_offset + p - 1)
                channel = body[payload_start + 3]
                trigger_delays[channel] = Float64(le_u32(body, payload_start + 4)) / 1.0e9
            end
        elseif record_len == 17 && payload_start + 4 <= length(body)
            if body[payload_start] == 0xb0 &&
               body[payload_start + 1] == 0x2a &&
               body[payload_start + 2] == 0x65 &&
               body[payload_start + 3] == 0x00
                payload_end <= length(body) || fail("invalid setup record", body_offset + p - 1)

                channel = body[payload_start + 4]
                gain = Float64(le_f64(body, payload_start + 5))
                sample_rate = Float64(le_u32(body, payload_start + 13))

                (isfinite(gain) && sample_rate > 0) ||
                    fail("invalid setup record", body_offset + p - 1)

                gains[channel] = gain
                sample_rates[channel] = sample_rate
            end
        end

        p += 1
    end

    channels = Dict{UInt8,ChannelSetup}()
    for (channel, sample_rate) in sample_rates
        channels[channel] = ChannelSetup(
            get(gains, channel, 1.0),
            sample_rate,
            get(trigger_delays, channel, 0.0),
        )
    end

    return channels
end

function parse_hit(body::Vector{UInt8}, body_offset::Int, setup::SetupState)
    length(body) >= 7 || fail("truncated hit record", body_offset)

    counter = le_u48(body, 1)
    channel = body[7]
    haskey(setup.channels, channel) || fail("missing channel setup", body_offset + 6)

    features = Dict{Symbol,Any}()
    features[:time_counter] = counter

    p = 8
    for chid in setup.feature_chids
        size = FEATURE_SIZES[chid]
        p + size - 1 <= length(body) || fail("truncated hit features", body_offset + p - 1)
        features[FEATURE_NAMES[chid]] = decode_feature(chid, body, p)
        p += size
    end

    if p <= length(body)
        features[:trailing_bytes] = length(body) - p + 1
    end

    return HitRecord(Float64(counter) / COUNTER_HZ, channel, features)
end

function parse_waveform(body::Vector{UInt8}, body_offset::Int, setup::SetupState)
    length(body) >= 9 || fail("unsupported waveform layout", body_offset)

    subid = body[1]
    subid == 0x01 || fail("unsupported waveform layout", body_offset)

    counter = le_u48(body, 2)
    channel = body[8]
    alb = body[9]
    channel_setup = get(setup.channels, channel, nothing)
    channel_setup === nothing && fail("missing channel setup", body_offset + 7)

    sample_bytes = length(body) - 9
    sample_bytes > 0 && iseven(sample_bytes) || fail("unsupported waveform layout", body_offset)

    nsamples = sample_bytes ÷ 2
    raw_samples = Vector{Int16}(undef, nsamples)
    p = 10
    for i in 1:nsamples
        raw_samples[i] = le_i16(body, p)
        p += 2
    end

    voltage = Vector{Float64}(undef, nsamples)
    voltage_scale = VOLTS_PER_COUNT * channel_setup.gain
    for i in eachindex(raw_samples)
        voltage[i] = Float64(raw_samples[i]) * voltage_scale
    end

    rms_value = rms(voltage)
    signal_strength = sum(abs, voltage) / channel_setup.sample_rate
    absolute_energy = sum(v -> v * v, voltage) /
                      channel_setup.sample_rate /
                      ABSOLUTE_ENERGY_IMPEDANCE_OHMS *
                      1.0e18

    return WaveformRecord(
        Float64(counter) / COUNTER_HZ,
        channel,
        channel_setup.sample_rate,
        channel_setup.trigger_delay,
        raw_samples,
        voltage,
        subid,
        alb,
        rms_value,
        signal_strength,
        absolute_energy,
    )
end

function decode_feature(chid::UInt8, body::Vector{UInt8}, p::Int)
    if chid == 0x01 || chid == 0x03 || chid == 0x04 || chid == 0x17 || chid == 0x18
        return le_u16(body, p)
    elseif chid == 0x05
        return le_u32(body, p)
    elseif chid == 0x06
        return body[p]
    elseif chid == 0x15
        return Float64(le_f32(body, p))
    else
        error("internal error: unsupported CHID $(Int(chid))")
    end
end

function rms(values::Vector{Float64})
    isempty(values) && return 0.0
    return sqrt(sum(v -> v * v, values) / length(values))
end

@inline function le_u16(bytes::Vector{UInt8}, p::Int)
    return UInt16(bytes[p]) | (UInt16(bytes[p + 1]) << 8)
end

@inline function le_i16(bytes::Vector{UInt8}, p::Int)
    return reinterpret(Int16, le_u16(bytes, p))
end

@inline function le_u32(bytes::Vector{UInt8}, p::Int)
    return UInt32(bytes[p]) |
           (UInt32(bytes[p + 1]) << 8) |
           (UInt32(bytes[p + 2]) << 16) |
           (UInt32(bytes[p + 3]) << 24)
end

@inline function le_u64(bytes::Vector{UInt8}, p::Int)
    value = UInt64(0)
    for i in 0:7
        value |= UInt64(bytes[p + i]) << (8 * i)
    end
    return value
end

@inline function le_u48(bytes::Vector{UInt8}, p::Int)
    value = UInt64(0)
    for i in 0:5
        value |= UInt64(bytes[p + i]) << (8 * i)
    end
    return value
end

@inline le_f32(bytes::Vector{UInt8}, p::Int) = reinterpret(Float32, le_u32(bytes, p))
@inline le_f64(bytes::Vector{UInt8}, p::Int) = reinterpret(Float64, le_u64(bytes, p))

function fail(message::AbstractString, offset::Integer)
    throw(ArgumentError("$message at byte offset $(offset)"))
end

function Base.getproperty(data::DTAData, name::Symbol)
    if name === :unknown_counts || name === :unknown_messages
        return getfield(data, :unknown_message_counts)
    end
    return getfield(data, name)
end

end