module MistrasWFSJulia

export WFSData, WFSFormatError, WFSHeader, read_wfs, waveform_axes

struct WFSFormatError <: Exception
    offset::Int
    message::String
end

Base.showerror(io::IO, error::WFSFormatError) =
    print(io, error.message, " at byte offset ", error.offset)

struct WFSHeader
    num_channels::Int
    sample_rate_hz::Vector{Int}
    pretrigger_samples::Vector{Int}
    max_voltage_v::Vector{Float64}
    header_length::Int
    timestamp::String
    version::String
    channel_numbers::Vector{UInt8}
end

struct WFSData
    header::WFSHeader
    raw_counts::Matrix{Int16}
    voltage_mv::Matrix{Float64}
    ignored_frame_lengths::Dict{UInt16,Int}
end

mutable struct Cursor
    bytes::Vector{UInt8}
    position::Int
    limit::Int
end

Cursor(bytes::Vector{UInt8}) = Cursor(bytes, 1, length(bytes))
offset(cursor::Cursor) = cursor.position - 1
remaining(cursor::Cursor) = cursor.limit - cursor.position + 1

function require_bytes(cursor::Cursor, count::Int, what::AbstractString)
    count >= 0 || throw(WFSFormatError(offset(cursor), "invalid $what length"))
    count <= remaining(cursor) ||
        throw(WFSFormatError(offset(cursor), "truncated $what"))
end

function read_u8(cursor::Cursor)
    require_bytes(cursor, 1, "UInt8")
    value = cursor.bytes[cursor.position]
    cursor.position += 1
    value
end

read_i8(cursor::Cursor) = reinterpret(Int8, read_u8(cursor))

function read_u16(cursor::Cursor)
    require_bytes(cursor, 2, "UInt16")
    value = UInt16(cursor.bytes[cursor.position]) |
            (UInt16(cursor.bytes[cursor.position + 1]) << 8)
    cursor.position += 2
    value
end

read_i16(cursor::Cursor) = reinterpret(Int16, read_u16(cursor))

function read_u32(cursor::Cursor)
    require_bytes(cursor, 4, "UInt32")
    value = UInt32(0)
    for shift in 0:3
        value |= UInt32(cursor.bytes[cursor.position + shift]) << (8 * shift)
    end
    cursor.position += 4
    value
end

function read_u64(cursor::Cursor)
    require_bytes(cursor, 8, "UInt64")
    value = UInt64(0)
    for shift in 0:7
        value |= UInt64(cursor.bytes[cursor.position + shift]) << (8 * shift)
    end
    cursor.position += 8
    value
end

read_i64(cursor::Cursor) = reinterpret(Int64, read_u64(cursor))

function read_bytes(cursor::Cursor, count::Int, what::AbstractString)
    require_bytes(cursor, count, what)
    first = cursor.position
    cursor.position += count
    cursor.bytes[first:first+count-1]
end

function skip_bytes(cursor::Cursor, count::Int, what::AbstractString)
    require_bytes(cursor, count, what)
    cursor.position += count
end

function parse_version(model::AbstractString)
    match_result = match(r"V(\d+\.\d+)", model)
    match_result === nothing &&
        throw(WFSFormatError(6, "unsupported product version string"))
    parse(Float64, match_result.captures[1])
end

function parse_header!(cursor::Cursor)
    table1_size = Int(read_u16(cursor))
    table1_size >= 4 || throw(WFSFormatError(0, "invalid table 1 length"))
    read_u8(cursor)  # product ID
    read_i8(cursor)  # reserved byte
    read_i16(cursor)
    model_bytes = read_bytes(cursor, table1_size - 4, "table 1 model")
    model = rstrip(String(model_bytes), '\0')
    board_model = first(model, min(3, length(model)))
    software_version = parse_version(model)

    table2_size = Int(read_u16(cursor))
    table2_start = offset(cursor)
    read_u8(cursor) == 174 ||
        throw(WFSFormatError(table2_start, "invalid table 2 message ID"))
    read_u8(cursor) == 106 ||
        throw(WFSFormatError(table2_start + 1, "invalid table 2 sub-ID"))
    read_i8(cursor)
    num_channels = Int(read_i8(cursor))
    num_channels > 0 ||
        throw(WFSFormatError(table2_start + 3, "invalid channel count"))
    channel_numbers = read_bytes(cursor, num_channels, "channel list")
    table2_size == 4 + num_channels ||
        throw(WFSFormatError(table2_start - 2, "unsupported table 2 length"))

    sample_rate_hz = Vector{Int}(undef, num_channels)
    pretrigger = Vector{Int}(undef, num_channels)
    max_voltage = Vector{Float64}(undef, num_channels)
    hardware_channels = Vector{UInt8}(undef, num_channels)
    for index in 1:num_channels
        table3_start = offset(cursor)
        table3_size = Int(read_u16(cursor))
        table3_size == 26 ||
            throw(WFSFormatError(table3_start, "unsupported table 3 length"))
        read_u8(cursor) == 174 ||
            throw(WFSFormatError(table3_start + 2, "invalid table 3 message ID"))
        read_u8(cursor)
        read_i16(cursor)
        read_i8(cursor)
        hardware_channels[index] = read_u8(cursor)
        read_u32(cursor)
        read_i16(cursor)
        sample_rate_hz[index] = 1000 * Int(read_i16(cursor))
        read_i16(cursor)
        read_i16(cursor)
        pretrigger[index] = reinterpret(Int32, read_u32(cursor))
        max_voltage[index] = Float64(read_i16(cursor))
        read_i16(cursor)
    end
    hardware_channels == channel_numbers ||
        throw(WFSFormatError(0, "hardware channel list does not match group definition"))

    if (board_model == "Exp" || board_model == "PCI") && software_version < 5.0
        throw(WFSFormatError(offset(cursor), "unsupported legacy Express/PCI WFS header"))
    end

    table4_size = Int(read_u16(cursor))
    table4_start = offset(cursor) - 2
    table4_size == 6 + 2 * num_channels ||
        throw(WFSFormatError(table4_start, "unsupported table 4 length"))
    read_u8(cursor) == 174 ||
        throw(WFSFormatError(table4_start + 2, "invalid table 4 message ID"))
    read_u8(cursor) == 20 ||
        throw(WFSFormatError(table4_start + 3, "invalid table 4 sub-ID"))
    read_i16(cursor)
    read_i16(cursor)
    for _ in 1:num_channels
        read_i8(cursor)
        read_i8(cursor)
    end

    table5_size = Int(read_u16(cursor))
    table5_start = offset(cursor) - 2
    table5_size == 6 + 2 * num_channels ||
        throw(WFSFormatError(table5_start, "unsupported table 5 length"))
    read_u8(cursor) == 174 ||
        throw(WFSFormatError(table5_start + 2, "invalid table 5 message ID"))
    read_u8(cursor) == 23 ||
        throw(WFSFormatError(table5_start + 3, "invalid table 5 sub-ID"))
    read_i16(cursor)
    read_i16(cursor)
    gain_codes = Int8[]
    for _ in 1:num_channels
        read_i8(cursor)
        push!(gain_codes, read_i8(cursor))
    end

    preamp_size = Int(read_u16(cursor))
    preamp_start = offset(cursor) - 2
    read_u8(cursor) == 174 ||
        throw(WFSFormatError(preamp_start + 2, "invalid preamp message ID"))
    preamp = read_bytes(cursor, preamp_size - 1, "preamp message")
    length(preamp) >= 9 ||
        throw(WFSFormatError(preamp_start, "unsupported preamp message"))

    gain_factor = preamp[9] == 5 ? 0.2 : 1.0
    if gain_codes[1] == 6
        gain_factor /= 2
    elseif gain_codes[1] == 12
        gain_factor /= 4
    end
    max_voltage .*= gain_factor

    for _ in 1:num_channels
        size = Int(read_u16(cursor))
        start = offset(cursor) - 2
        size == 5 || throw(WFSFormatError(start, "unsupported analog filter record"))
        read_u8(cursor) == 137 ||
            throw(WFSFormatError(start + 2, "invalid analog filter message ID"))
        skip_bytes(cursor, 4, "analog filter")
    end
    for _ in 1:num_channels
        size = Int(read_u16(cursor))
        start = offset(cursor) - 2
        size == 10 || throw(WFSFormatError(start, "unsupported digital filter record"))
        read_u8(cursor) == 146 ||
            throw(WFSFormatError(start + 2, "invalid digital filter message ID"))
        skip_bytes(cursor, 9, "digital filter")
    end

    table6_size = Int(read_u16(cursor))
    table6_start = offset(cursor) - 2
    read_u8(cursor) == 99 ||
        throw(WFSFormatError(table6_start + 2, "invalid timestamp message ID"))
    timestamp = rstrip(String(read_bytes(cursor, table6_size - 1, "timestamp")), '\0')

    table7_size = Int(read_u16(cursor))
    table7_size == 1 || throw(WFSFormatError(offset(cursor) - 2, "invalid table 7 length"))
    read_u8(cursor) == 11 ||
        throw(WFSFormatError(offset(cursor) - 1, "invalid table 7 message ID"))

    table8_size = Int(read_u16(cursor))
    table8_size == 7 || throw(WFSFormatError(offset(cursor) - 2, "invalid table 8 length"))
    read_u8(cursor) == 128 ||
        throw(WFSFormatError(offset(cursor) - 1, "invalid table 8 message ID"))
    skip_bytes(cursor, 6, "table 8")

    WFSHeader(
        num_channels,
        sample_rate_hz,
        pretrigger,
        max_voltage,
        offset(cursor),
        timestamp,
        model,
        channel_numbers,
    )
end

function parse_sync!(cursor::Cursor, header::WFSHeader)
    frame_start = offset(cursor)
    frame_length = Int(read_u16(cursor))
    frame_length == 6 + 15 * header.num_channels ||
        throw(WFSFormatError(frame_start, "unsupported sync message length"))
    frame_end = offset(cursor) + frame_length
    read_u8(cursor) == 174 ||
        throw(WFSFormatError(frame_start + 2, "invalid sync message ID"))
    read_u8(cursor) == 174 ||
        throw(WFSFormatError(frame_start + 3, "invalid sync sub-ID"))
    read_i16(cursor)
    Int(read_i16(cursor)) == header.num_channels ||
        throw(WFSFormatError(frame_start + 6, "sync channel count mismatch"))

    sample_start = Dict{UInt8,Int64}()
    for channel in header.channel_numbers
        actual_channel = read_u8(cursor)
        actual_channel == channel ||
            throw(WFSFormatError(offset(cursor) - 1, "sync channel order mismatch"))
        read_u32(cursor)
        read_u16(cursor)
        sample_start[channel] = read_i64(cursor)
    end
    offset(cursor) == frame_end ||
        throw(WFSFormatError(offset(cursor), "invalid sync message boundary"))
    sample_start
end

function parse_chunks!(cursor::Cursor, header::WFSHeader, sample_start)
    samples = Dict(channel => Int16[] for channel in header.channel_numbers)
    offsets = Dict{UInt8,Int}()
    ignored = Dict{UInt16,Int}()

    while remaining(cursor) > 0
        remaining(cursor) >= 2 ||
            throw(WFSFormatError(offset(cursor), "truncated frame length"))
        frame_start = offset(cursor)
        frame_length_u16 = read_u16(cursor)
        frame_length = Int(frame_length_u16)
        frame_length <= remaining(cursor) ||
            throw(WFSFormatError(frame_start, "truncated data frame"))
        frame_end = offset(cursor) + frame_length

        if frame_length == 2076 || frame_length == 8220
            read_u8(cursor) == 174 ||
                throw(WFSFormatError(frame_start + 2, "invalid data message ID"))
            read_u8(cursor) == 1 ||
                throw(WFSFormatError(frame_start + 3, "invalid data sub-ID"))
            read_i16(cursor)
            read_u32(cursor)
            channel_value = read_u32(cursor)
            channel_value <= typemax(UInt8) ||
                throw(WFSFormatError(frame_start + 10, "invalid data channel"))
            channel = UInt8(channel_value)
            haskey(samples, channel) ||
                throw(WFSFormatError(frame_start + 10, "unconfigured data channel"))
            read_i64(cursor)
            fifo_high = read_u32(cursor)
            fifo_low = read_u32(cursor)
            fifo_read = UInt64(fifo_high) * UInt64(4294967296) + UInt64(fifo_low)
            if !haskey(offsets, channel)
                difference = Int128(sample_start[channel]) - 2 * Int128(fifo_read)
                0 <= difference <= typemax(Int) ||
                    throw(WFSFormatError(frame_start, "invalid FIFO offset"))
                offsets[channel] = Int(difference)
            end

            sample_count = (frame_length - 28) ÷ 2
            for _ in 1:sample_count
                push!(samples[channel], read_i16(cursor))
            end
        else
            ignored[frame_length_u16] = get(ignored, frame_length_u16, 0) + 1
            skip_bytes(cursor, frame_length, "ignored data frame")
        end

        offset(cursor) == frame_end ||
            throw(WFSFormatError(offset(cursor), "invalid data frame boundary"))
    end

    length(offsets) == header.num_channels ||
        throw(WFSFormatError(header.header_length, "missing channel data"))
    sample_lengths = length.(values(samples))
    allequal(sample_lengths) ||
        throw(WFSFormatError(header.header_length, "channel sample counts differ"))
    max_offset = maximum(values(offsets))
    data_length = first(sample_lengths) - max_offset
    data_length > 0 ||
        throw(WFSFormatError(header.header_length, "invalid aligned data length"))

    raw_counts = Matrix{Int16}(undef, header.num_channels, data_length)
    for (row, channel) in enumerate(header.channel_numbers)
        first_sample = offsets[channel] + 1
        raw_counts[row, :] = samples[channel][first_sample:first_sample+data_length-1]
    end
    raw_counts, ignored
end

"""
    read_wfs(path) -> WFSData

Read the WFS layout exercised by the pinned public MATLAB fixture. Unsupported
header branches and malformed records fail with a byte offset.
"""
function read_wfs(path::AbstractString)
    bytes = read(path)
    isempty(bytes) && throw(WFSFormatError(0, "empty WFS file"))
    cursor = Cursor(bytes)
    header = parse_header!(cursor)
    sample_start = parse_sync!(cursor, header)
    raw_counts, ignored = parse_chunks!(cursor, header, sample_start)

    voltage_mv = Matrix{Float64}(undef, size(raw_counts))
    for row in axes(raw_counts, 1)
        scale = 1000 * header.max_voltage_v[row] / 32767
        voltage_mv[row, :] = Float64.(raw_counts[row, :]) .* scale
    end
    WFSData(header, raw_counts, voltage_mv, ignored)
end

"""
    waveform_axes(data, channel; time_unit=:s)

Return the MATLAB-reference time axis and voltage in millivolts for one
hardware channel.
"""
function waveform_axes(data::WFSData, channel::Integer; time_unit::Symbol=:s)
    row = findfirst(==(channel), data.header.channel_numbers)
    row === nothing && throw(ArgumentError("channel $channel is not present"))
    multiplier = time_unit === :s ? 1.0 : time_unit === :us ? 1e6 :
        throw(ArgumentError("time_unit must be :s or :us"))
    count = size(data.voltage_mv, 2)
    time = collect(0:count-1) ./ data.header.sample_rate_hz[row] .* multiplier
    (time=time, voltage_mv=vec(data.voltage_mv[row, :]))
end

end
