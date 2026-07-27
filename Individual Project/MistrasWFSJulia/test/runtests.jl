using Test
using MistrasWFSJulia

const ROOT = normpath(joinpath(@__DIR__, ".."))
const FIXTURE = joinpath(@__DIR__, "data", "ExampleWFSdata.wfs")
const REFERENCE = joinpath(@__DIR__, "reference")

function reference_header()
    rows = split.(readlines(joinpath(REFERENCE, "header.tsv"))[2:end], '\t')
    Dict(row[1] => row[2] for row in rows)
end

function reference_voltage()
    bytes = read(joinpath(REFERENCE, "waveforms.f64le"))
    @assert length(bytes) % 8 == 0
    values = [
        reinterpret(Float64, ltoh(reinterpret(UInt64, bytes[index:index+7])[1]))
        for index in 1:8:length(bytes)
    ]
    reshape(values, 2, :)
end

@testset "low-level bounds and errors" begin
    cursor = MistrasWFSJulia.Cursor(UInt8[0x34, 0x12])
    @test MistrasWFSJulia.read_u16(cursor) == 0x1234
    @test MistrasWFSJulia.remaining(cursor) == 0

    mktemp() do path, io
        close(io)
        error = try
            read_wfs(path)
            nothing
        catch caught
            caught
        end
        @test error isa WFSFormatError
        @test occursin("byte offset 0", sprint(showerror, error))
    end

    bytes = read(FIXTURE)
    mktemp() do path, io
        write(io, bytes[1:end-4])
        close(io)
        error = try
            read_wfs(path)
            nothing
        catch caught
            caught
        end
        @test error isa WFSFormatError
        @test occursin("byte offset", sprint(showerror, error))
    end
end

@testset "MATLAB fixture regression" begin
    expected = reference_header()
    reference = reference_voltage()
    data = read_wfs(FIXTURE)
    header = data.header

    @test header.num_channels == parse(Int, expected["num_channels"]) == 2
    @test header.sample_rate_hz == parse.(Int, split(expected["sample_rate_hz"], ','))
    @test header.pretrigger_samples ==
          parse.(Int, split(expected["pretrigger_samples"], ','))
    @test header.max_voltage_v ==
          parse.(Float64, split(expected["max_voltage_v"], ','))
    @test header.header_length == parse(Int, expected["header_length"]) == 244
    @test header.channel_numbers ==
          parse.(UInt8, split(expected["channel_numbers"], ','))
    @test size(data.raw_counts) == size(data.voltage_mv) == size(reference)
    @test size(data.voltage_mv) == (2, parse(Int, expected["sample_count"]))
    @test data.voltage_mv == reference
    @test data.ignored_frame_lengths == Dict(UInt16(7) => 1)

    for row in axes(data.raw_counts, 1)
        scale = 1000 * header.max_voltage_v[row] / 32767
        @test data.voltage_mv[row, :] == Float64.(data.raw_counts[row, :]) .* scale
    end

    axes_seconds = waveform_axes(data, 1)
    @test axes_seconds.time[1] == parse(Float64, expected["time_start_s"])
    @test axes_seconds.time[2] - axes_seconds.time[1] ==
          parse(Float64, expected["time_step_s"])
    @test axes_seconds.time[end] == parse(Float64, expected["time_end_s"])
    @test axes_seconds.voltage_mv == vec(reference[1, :])

    axes_microseconds = waveform_axes(data, 2; time_unit=:us)
    @test axes_microseconds.time[2] == 1.0
    @test axes_microseconds.voltage_mv == vec(reference[2, :])
    @test_throws ArgumentError waveform_axes(data, 99)
    @test_throws ArgumentError waveform_axes(data, 1; time_unit=:ms)
end
