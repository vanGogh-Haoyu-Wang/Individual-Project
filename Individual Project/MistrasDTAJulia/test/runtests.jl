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

_record_key(time_s, channel) = (
    isfinite(time_s) ? string(round(Int64, time_s * 4_000_000)) : string(time_s),
    channel,
)

_comparison_error(actual, expected) = begin
    error = abs(actual - expected)
    isfinite(error) ? Float64(error) : Inf
end

_toml_float(value) = isinf(value) ? (signbit(value) ? "-inf" : "inf") :
                     isnan(value) ? "nan" : repr(value)

function _difference_counts(expected_keys, actual_keys)
    balance = Dict{eltype(expected_keys),Int}()
    for key in expected_keys
        balance[key] = get(balance, key, 0) + 1
    end
    for key in actual_keys
        balance[key] = get(balance, key, 0) - 1
    end
    sum(max(value, 0) for value in values(balance)),
    sum(max(-value, 0) for value in values(balance))
end

function compare_fixture(data, hits_header, hits_rows, wave_rows, reference_voltage)
    expected_features = Symbol.(hits_header[3:end])
    hit_mismatches = Dict(
        "time_s" => 0,
        "channel" => 0,
        "feature_set" => 0,
        (String(name) => 0 for name in expected_features)...,
    )
    hit_errors = Dict(
        "time_s" => 0.0,
        "channel" => 0.0,
        (String(name) => 0.0 for name in expected_features)...,
    )

    expected_hit_keys = [
        _record_key(parse(Float64, row[1]), parse(UInt8, row[2]))
        for row in hits_rows
    ]
    actual_hit_keys = [_record_key(hit.time_s, hit.channel) for hit in data.hits]
    missing_hits, extra_hits = _difference_counts(expected_hit_keys, actual_hit_keys)
    hit_order_matches = expected_hit_keys == actual_hit_keys

    for index in 1:min(length(data.hits), length(hits_rows))
        hit = data.hits[index]
        row = hits_rows[index]
        expected_time = parse(Float64, row[1])
        expected_channel = parse(UInt8, row[2])
        time_error = _comparison_error(hit.time_s, expected_time)
        channel_error = _comparison_error(Int(hit.channel), Int(expected_channel))

        hit_errors["time_s"] = max(hit_errors["time_s"], time_error)
        hit_errors["channel"] = max(hit_errors["channel"], channel_error)
        hit_mismatches["time_s"] +=
            isapprox(hit.time_s, expected_time; rtol=0, atol=1e-12) ? 0 : 1
        hit_mismatches["channel"] += hit.channel == expected_channel ? 0 : 1
        hit_mismatches["feature_set"] +=
            Set(keys(hit.features)) == Set(expected_features) ? 0 : 1

        for (name, text) in zip(expected_features, row[3:end])
            key = String(name)
            expected = parse(Float64, text)
            if !haskey(hit.features, name)
                hit_mismatches[key] += 1
                continue
            end
            actual = hit.features[name]
            error = _comparison_error(actual, expected)
            hit_errors[key] = max(hit_errors[key], error)
            matches = name == Symbol("ABS-ENERGY") ?
                isapprox(actual, expected; rtol=1e-12, atol=1e-12) :
                actual == expected
            hit_mismatches[key] += matches ? 0 : 1
        end
    end

    waveform_mismatches = Dict(
        "time_s" => 0,
        "channel" => 0,
        "sample_rate_hz" => 0,
        "trigger_delay_samples" => 0,
        "sample_count" => 0,
    )
    waveform_errors = Dict(
        "time_s" => 0.0,
        "channel" => 0.0,
        "sample_rate_hz" => 0.0,
        "trigger_delay_samples" => 0.0,
        "sample_count" => 0.0,
        "raw_counts" => 0.0,
        "voltage_v" => 0.0,
    )

    expected_waveform_keys = [
        _record_key(parse(Float64, row[2]), parse(UInt8, row[3]))
        for row in wave_rows
    ]
    actual_waveform_keys = [
        _record_key(waveform.time_s, waveform.channel)
        for waveform in data.waveforms
    ]
    missing_waveforms, extra_waveforms =
        _difference_counts(expected_waveform_keys, actual_waveform_keys)
    waveform_order_matches = expected_waveform_keys == actual_waveform_keys

    waveform_length_mismatches = 0
    raw_count_mismatches = 0
    voltage_mismatches = 0
    for index in 1:min(length(data.waveforms), length(wave_rows))
        waveform = data.waveforms[index]
        row = wave_rows[index]
        expected_time = parse(Float64, row[2])
        expected_channel = parse(UInt8, row[3])
        expected_rate = parse(Int, row[4])
        expected_delay = parse(Int, row[5])
        offset = parse(Int, row[6])
        count = parse(Int, row[7])
        expected_voltage = reference_voltage[offset+1:offset+count]
        expected_counts = round.(Int16, expected_voltage ./ (10.0 / 32768.0))

        metadata = (
            time_s=(waveform.time_s, expected_time, 0.0, 1e-12),
            channel=(Int(waveform.channel), Int(expected_channel), 0.0, 0.0),
            sample_rate_hz=(waveform.sample_rate_hz, expected_rate, 0.0, 0.0),
            trigger_delay_samples=(
                waveform.trigger_delay_samples,
                expected_delay,
                0.0,
                0.0,
            ),
        )
        for (name, (actual, expected, rtol, atol)) in pairs(metadata)
            key = String(name)
            error = _comparison_error(actual, expected)
            waveform_errors[key] = max(waveform_errors[key], error)
            waveform_mismatches[key] +=
                isapprox(actual, expected; rtol=rtol, atol=atol) ? 0 : 1
        end

        raw_length_error = abs(length(waveform.raw_counts) - count)
        voltage_length_error = abs(length(waveform.voltage_v) - count)
        length_mismatch = raw_length_error != 0 || voltage_length_error != 0
        waveform_length_mismatches += length_mismatch ? 1 : 0
        waveform_mismatches["sample_count"] += length_mismatch ? 1 : 0
        waveform_errors["sample_count"] = max(
            waveform_errors["sample_count"],
            raw_length_error,
            voltage_length_error,
        )

        for sample_index in 1:min(length(waveform.raw_counts), count)
            error = abs(Int(waveform.raw_counts[sample_index]) -
                        Int(expected_counts[sample_index]))
            waveform_errors["raw_counts"] =
                max(waveform_errors["raw_counts"], error)
            raw_count_mismatches += iszero(error) ? 0 : 1
        end
        for sample_index in 1:min(length(waveform.voltage_v), count)
            error = _comparison_error(
                waveform.voltage_v[sample_index],
                expected_voltage[sample_index],
            )
            waveform_errors["voltage_v"] =
                max(waveform_errors["voltage_v"], error)
            voltage_mismatches +=
                isapprox(
                    waveform.voltage_v[sample_index],
                    expected_voltage[sample_index];
                    rtol=1e-12,
                    atol=1e-12,
                ) ? 0 : 1
        end
    end

    missing_in_julia = missing_hits + missing_waveforms
    extra_in_julia = extra_hits + extra_waveforms
    field_mismatches =
        sum(values(hit_mismatches)) +
        sum(values(waveform_mismatches)) +
        raw_count_mismatches +
        voltage_mismatches
    passed =
        missing_in_julia == 0 &&
        extra_in_julia == 0 &&
        hit_order_matches &&
        waveform_order_matches &&
        field_mismatches == 0 &&
        waveform_length_mismatches == 0 &&
        isempty(data.unknown_message_counts)

    (
        expected_hits=length(hits_rows),
        actual_hits=length(data.hits),
        missing_hits,
        extra_hits,
        expected_waveforms=length(wave_rows),
        actual_waveforms=length(data.waveforms),
        missing_waveforms,
        extra_waveforms,
        missing_in_julia,
        extra_in_julia,
        hit_order_matches,
        waveform_order_matches,
        hit_mismatches,
        waveform_mismatches,
        waveform_length_mismatches,
        raw_count_mismatches,
        voltage_mismatches,
        field_mismatches,
        hit_errors,
        waveform_errors,
        passed,
    )
end

function write_comparison_summary(path, comparison, unknown_message_counts)
    open(path, "w") do io
        println(io, "schema_version = 2")
        println(io, "fixture = \"210527-CH1-15.DTA\"")
        println(io, "python_upstream_commit = \"6c7dfb6f43f812dccff0c9219bd2c5c82bd98e85\"")
        println(io, "hit_time_rtol = 0.0")
        println(io, "hit_time_atol_s = 1.0e-12")
        println(io, "integer_features_exact = true")
        println(io, "toleranced_feature = \"ABS-ENERGY\"")
        println(io, "floating_feature_rtol = 1.0e-12")
        println(io, "floating_feature_atol = 1.0e-12")
        println(io, "waveform_time_rtol = 0.0")
        println(io, "waveform_time_atol_s = 1.0e-12")
        println(io, "waveform_metadata_exact = true")
        println(io, "raw_counts_exact = true")
        println(io, "waveform_voltage_rtol = 1.0e-12")
        println(io, "waveform_voltage_atol_v = 1.0e-12")
        println(io, "hits = ", comparison.actual_hits)
        println(io, "waveforms = ", comparison.actual_waveforms)
        println(io, "missing_in_julia = ", comparison.missing_in_julia)
        println(io, "extra_in_julia = ", comparison.extra_in_julia)
        println(io, "field_mismatches = ", comparison.field_mismatches)
        println(
            io,
            "waveform_length_mismatches = ",
            comparison.waveform_length_mismatches,
        )
        println(
            io,
            "max_hit_time_error_s = ",
            _toml_float(comparison.hit_errors["time_s"]),
        )
        feature_names = filter(
            name -> !(name in ("time_s", "channel")),
            keys(comparison.hit_errors),
        )
        max_feature_error = maximum(
            (comparison.hit_errors[name] for name in feature_names);
            init=0.0,
        )
        println(io, "max_feature_error = ", _toml_float(max_feature_error))
        println(
            io,
            "max_waveform_time_error_s = ",
            _toml_float(comparison.waveform_errors["time_s"]),
        )
        println(
            io,
            "max_waveform_voltage_error_v = ",
            _toml_float(comparison.waveform_errors["voltage_v"]),
        )
        println(io, "passed = ", comparison.passed)
        status = comparison.passed ?
            "numerically validated against the Python reference" :
            "failed"
        println(io, "status = ", repr(status))

        println(io, "\n[hit_counts]")
        println(io, "expected = ", comparison.expected_hits)
        println(io, "actual = ", comparison.actual_hits)
        println(io, "missing = ", comparison.missing_hits)
        println(io, "extra = ", comparison.extra_hits)
        println(io, "order_matches = ", comparison.hit_order_matches)

        println(io, "\n[waveform_counts]")
        println(io, "expected = ", comparison.expected_waveforms)
        println(io, "actual = ", comparison.actual_waveforms)
        println(io, "missing = ", comparison.missing_waveforms)
        println(io, "extra = ", comparison.extra_waveforms)
        println(io, "order_matches = ", comparison.waveform_order_matches)

        println(io, "\n[hit_field_mismatches]")
        for name in sort!(collect(keys(comparison.hit_mismatches)))
            println(io, repr(name), " = ", comparison.hit_mismatches[name])
        end

        println(io, "\n[hit_max_abs_error]")
        for name in sort!(collect(keys(comparison.hit_errors)))
            println(io, repr(name), " = ", _toml_float(comparison.hit_errors[name]))
        end

        println(io, "\n[waveform_field_mismatches]")
        for name in sort!(collect(keys(comparison.waveform_mismatches)))
            println(io, repr(name), " = ", comparison.waveform_mismatches[name])
        end
        println(io, "raw_counts = ", comparison.raw_count_mismatches)
        println(io, "voltage_v = ", comparison.voltage_mismatches)

        println(io, "\n[waveform_max_abs_error]")
        for name in sort!(collect(keys(comparison.waveform_errors)))
            println(
                io,
                repr(name),
                " = ",
                _toml_float(comparison.waveform_errors[name]),
            )
        end

        println(io, "\n[unknown_message_counts]")
        for message_id in sort!(collect(keys(unknown_message_counts)))
            println(
                io,
                repr(string(Int(message_id))),
                " = ",
                unknown_message_counts[message_id],
            )
        end
    end
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

    for (waveform, row) in zip(data.waveforms, wave_rows)
        expected_rate = parse(Int, row[4])
        expected_delay = parse(Int, row[5])

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

    comparison =
        compare_fixture(data, hits_header, hits_rows, wave_rows, reference_voltage)
    @test comparison.missing_hits == 0
    @test comparison.extra_hits == 0
    @test comparison.missing_waveforms == 0
    @test comparison.extra_waveforms == 0
    @test comparison.passed

    missing_data = DTAData(
        data.hits[1:end-1],
        data.waveforms[1:end-1],
        data.unknown_message_counts,
    )
    missing_comparison = compare_fixture(
        missing_data,
        hits_header,
        hits_rows,
        wave_rows,
        reference_voltage,
    )
    @test missing_comparison.missing_hits == 1 &&
          missing_comparison.missing_waveforms == 1 &&
          missing_comparison.extra_in_julia == 0 &&
          !missing_comparison.passed

    extra_data = DTAData(
        [data.hits; data.hits[end]],
        [data.waveforms; data.waveforms[end]],
        data.unknown_message_counts,
    )
    extra_comparison = compare_fixture(
        extra_data,
        hits_header,
        hits_rows,
        wave_rows,
        reference_voltage,
    )
    @test extra_comparison.extra_hits == 1 &&
          extra_comparison.extra_waveforms == 1 &&
          extra_comparison.missing_in_julia == 0 &&
          !extra_comparison.passed

    reordered_hits = copy(data.hits)
    reordered_waveforms = copy(data.waveforms)
    reordered_hits[1:2] = reordered_hits[2:-1:1]
    reordered_waveforms[1:2] = reordered_waveforms[2:-1:1]
    reordered_data =
        DTAData(reordered_hits, reordered_waveforms, data.unknown_message_counts)
    reordered_comparison = compare_fixture(
        reordered_data,
        hits_header,
        hits_rows,
        wave_rows,
        reference_voltage,
    )
    @test reordered_comparison.missing_in_julia == 0 &&
          reordered_comparison.extra_in_julia == 0 &&
          !reordered_comparison.hit_order_matches &&
          !reordered_comparison.waveform_order_matches &&
          !reordered_comparison.passed

    results_dir = joinpath(ROOT, "results")
    mkpath(results_dir)
    write_comparison_summary(
        joinpath(results_dir, "comparison_summary.toml"),
        comparison,
        data.unknown_message_counts,
    )
end
