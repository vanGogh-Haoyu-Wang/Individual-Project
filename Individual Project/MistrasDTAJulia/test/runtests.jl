using Test
using MistrasDTAJulia

const ROOT = normpath(joinpath(@__DIR__, ".."))
const PYTHON_FIXTURE = joinpath(@__DIR__, "data", "python", "210527-CH1-15.DTA")
const MATLAB_FIXTURE = joinpath(@__DIR__, "data", "matlab", "ExampleDTAfile.DTA")
const REFERENCE = joinpath(@__DIR__, "reference")

le16(value::Integer) = UInt8[value & 0xff, (value >> 8) & 0xff]

function frame(id::Integer, body::Vector{UInt8}; secondary::Union{Nothing,UInt8}=nothing)
    payload = secondary === nothing ?
        vcat(UInt8(id), body) :
        vcat(UInt8(id), secondary, body)
    vcat(le16(length(payload)), payload)
end

function subrecord(id::Integer, payload::Vector{UInt8})
    vcat(le16(1 + length(payload)), UInt8(id), payload)
end

function setup_body(; chids=UInt8[1, 3, 4, 5, 6, 21, 23, 24], gain=true, hardware=true)
    body = UInt8[0x67, 0x00]
    append!(body, subrecord(5, UInt8[length(chids); chids]))
    gain && append!(body, subrecord(23, UInt8[1, 0, 20]))
    if hardware
        hardware_payload = UInt8[
            42, 100, 0, 2, 1, 0, 17, 0, 1, 3, 0, 0, 0,
            0x10, 0x27, 0, 0, 1, 0, 0, 0xfb, 0x0a, 0, 0x19, 0,
        ]
        append!(body, subrecord(173, hardware_payload))
    end
    body
end

function write_temp(f::Function, bytes::Vector{UInt8})
    mktemp() do path, io
        write(io, bytes)
        close(io)
        f(path)
    end
end

function read_tsv(path)
    rows = split.(readlines(path), '\t')
    rows[1], rows[2:end]
end

function read_reference_waveforms()
    raw = read(joinpath(REFERENCE, "waveforms.f64le"))
    @assert length(raw) % 8 == 0
    [
        reinterpret(Float64, ltoh(reinterpret(UInt64, raw[i:i+7])[1]))
        for i in 1:8:length(raw)
    ]
end

@testset "low-level decoding" begin
    @test MistrasDTAJulia._u48(UInt8[0, 0, 0, 0, 0, 0], 0) == 0
    @test MistrasDTAJulia._u48(UInt8[1, 2, 3, 4, 5, 6], 0) ==
          0x060504030201
    @test MistrasDTAJulia._u48(UInt8[0xff, 0xff, 0xff, 0xff, 0xff, 0xff], 0) ==
          0xffffffffffff
    @test MistrasDTAJulia._u16(UInt8[0x34, 0x12], 1, 0) == 0x1234
    @test MistrasDTAJulia._i16(UInt8[0x00, 0xfb], 1, 0) == -1280

    write_temp(UInt8[]) do path
        error = try
            read_dta(path)
            nothing
        catch caught
            caught
        end
        @test error isa DTAFormatError
        @test occursin("byte offset", sprint(showerror, error))
    end

    write_temp(UInt8[5, 0, 1]) do path
        error = try
            read_dta(path)
            nothing
        catch caught
            caught
        end
        @test error isa DTAFormatError
        @test occursin("byte offset", sprint(showerror, error))
    end

    bytes = UInt8[]
    append!(bytes, frame(250, UInt8[1, 2, 3]))
    append!(bytes, frame(42, setup_body(); secondary=0x00))
    write_temp(bytes) do path
        data = read_dta(path)
        @test data.unknown_message_counts == Dict(UInt8(250) => 1)
    end
end

@testset "invalid setup and unsupported dialects" begin
    malformed_setup = frame(
        42,
        UInt8[0x67, 0x00, 0x05, 0x00, 0x05, 0x01];
        secondary=0x00,
    )
    write_temp(malformed_setup) do path
        @test_throws DTAFormatError read_dta(path)
    end

    hit = UInt8[zeros(UInt8, 6); 1; 1; 0]
    write_temp(frame(1, hit)) do path
        @test_throws DTAFormatError read_dta(path)
    end

    unknown_chid_setup = frame(42, setup_body(chids=UInt8[255]); secondary=0x00)
    write_temp(UInt8[unknown_chid_setup; frame(1, UInt8[zeros(UInt8, 6); 1; 0])]) do path
        error = try
            read_dta(path)
            nothing
        catch caught
            caught
        end
        @test error isa DTAFormatError
        @test occursin("unknown CHID", sprint(showerror, error))
    end

    no_hardware = frame(42, setup_body(hardware=false); secondary=0x00)
    waveform = frame(173, UInt8[1; zeros(UInt8, 6); 1; 0; 0; 0])
    write_temp(UInt8[no_hardware; waveform]) do path
        error = try
            read_dta(path)
            nothing
        catch caught
            caught
        end
        @test error isa DTAFormatError
        @test occursin("hardware setup", sprint(showerror, error))
    end

    error = try
        read_dta(MATLAB_FIXTURE)
        nothing
    catch caught
        caught
    end
    @test error isa DTAFormatError
    @test occursin("unsupported DTA", sprint(showerror, error))
end

@testset "Python fixture numerical regression" begin
    data = read_dta(PYTHON_FIXTURE)
    hits_header, hits_rows = read_tsv(joinpath(REFERENCE, "hits.tsv"))
    _, wave_rows = read_tsv(joinpath(REFERENCE, "waveforms.tsv"))
    reference_voltage = read_reference_waveforms()

    @test length(data.hits) == length(hits_rows) == 8
    @test length(data.waveforms) == length(wave_rows) == 8
    @test isempty(data.unknown_message_counts)

    missing_in_julia = 0
    extra_in_julia = 0
    field_mismatches = 0
    waveform_length_mismatches = 0
    max_hit_time_error = 0.0
    max_feature_error = 0.0
    max_waveform_time_error = 0.0
    max_waveform_voltage_error = 0.0

    expected_features = Symbol.(hits_header[3:end])
    for (hit, row) in zip(data.hits, hits_rows)
        expected_time = parse(Float64, row[1])
        expected_channel = parse(UInt8, row[2])
        max_hit_time_error = max(max_hit_time_error, abs(hit.time_s - expected_time))
        field_mismatches += hit.channel == expected_channel ? 0 : 1
        field_mismatches += Set(keys(hit.features)) == Set(expected_features) ? 0 : 1
        for (name, text) in zip(expected_features, row[3:end])
            actual = get(hit.features, name, NaN)
            expected = parse(Float64, text)
            error = abs(actual - expected)
            max_feature_error = max(max_feature_error, error)
            field_mismatches += iszero(error) ? 0 : 1
        end
    end

    for (waveform, row) in zip(data.waveforms, wave_rows)
        expected_time = parse(Float64, row[2])
        expected_channel = parse(UInt8, row[3])
        expected_rate = parse(Int, row[4])
        expected_delay = parse(Int, row[5])
        offset = parse(Int, row[6])
        count = parse(Int, row[7])
        expected_voltage = reference_voltage[offset+1:offset+count]

        field_mismatches += waveform.channel == expected_channel ? 0 : 1
        field_mismatches += waveform.sample_rate_hz == expected_rate ? 0 : 1
        field_mismatches += waveform.trigger_delay_samples == expected_delay ? 0 : 1
        waveform_length_mismatches += length(waveform.voltage_v) == count ? 0 : 1
        max_waveform_time_error = max(
            max_waveform_time_error,
            abs(waveform.time_s - expected_time),
        )
        if length(waveform.voltage_v) == count
            max_waveform_voltage_error = max(
                max_waveform_voltage_error,
                maximum(abs.(waveform.voltage_v .- expected_voltage)),
            )
            expected_counts = round.(Int16, expected_voltage ./ (10.0 / 32768.0))
            field_mismatches += waveform.raw_counts == expected_counts ? 0 : 1
        end

        axes = waveform_axes(waveform)
        @test axes.voltage === waveform.voltage_v
        @test axes.time[1] ≈ expected_delay * 1e6 / expected_rate atol=1e-12 rtol=0
        @test waveform_axes(waveform; time_unit=:s).time[1] ≈
              expected_delay / expected_rate atol=1e-12 rtol=0
    end
    @test_throws ArgumentError waveform_axes(data.waveforms[1]; time_unit=:minutes)

    hits_only = read_dta(PYTHON_FIXTURE; read_waveforms=false)
    @test hits_only.hits == data.hits
    @test isempty(hits_only.waveforms)

    @test missing_in_julia == 0
    @test extra_in_julia == 0
    @test field_mismatches == 0
    @test waveform_length_mismatches == 0
    @test max_hit_time_error <= 1e-12
    @test max_feature_error == 0
    @test max_waveform_time_error <= 1e-12
    @test max_waveform_voltage_error <= 1e-12

    results_dir = joinpath(ROOT, "results")
    mkpath(results_dir)
    open(joinpath(results_dir, "comparison_summary.toml"), "w") do io
        println(io, "fixture = \"210527-CH1-15.DTA\"")
        println(io, "python_upstream_commit = \"6c7dfb6f43f812dccff0c9219bd2c5c82bd98e85\"")
        println(io, "hits = ", length(data.hits))
        println(io, "waveforms = ", length(data.waveforms))
        println(io, "missing_in_julia = ", missing_in_julia)
        println(io, "extra_in_julia = ", extra_in_julia)
        println(io, "field_mismatches = ", field_mismatches)
        println(io, "waveform_length_mismatches = ", waveform_length_mismatches)
        println(io, "max_hit_time_error_s = ", repr(max_hit_time_error))
        println(io, "max_feature_error = ", repr(max_feature_error))
        println(io, "max_waveform_time_error_s = ", repr(max_waveform_time_error))
        println(io, "max_waveform_voltage_error_v = ", repr(max_waveform_voltage_error))
        println(io, "status = \"numerically validated against the Python reference\"")
    end
end
