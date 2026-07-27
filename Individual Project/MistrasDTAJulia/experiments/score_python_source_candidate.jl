include(joinpath(@__DIR__, "python_source_candidate.jl"))
using .MistrasDTAJulia

const ROOT = normpath(joinpath(@__DIR__, ".."))
const FIXTURE = joinpath(ROOT, "test", "data", "python", "210527-CH1-15.DTA")
const REFERENCE = joinpath(ROOT, "test", "reference")

read_tsv(path) = (rows = split.(readlines(path), '\t'); (rows[1], rows[2:end]))

function reference_voltage()
    raw = read(joinpath(REFERENCE, "waveforms.f64le"))
    [
        reinterpret(Float64, ltoh(reinterpret(UInt64, raw[i:i+7])[1]))
        for i in 1:8:length(raw)
    ]
end

function main()
    data = read_dta(FIXTURE)
    hit_header, hit_rows = read_tsv(joinpath(REFERENCE, "hits.tsv"))
    _, waveform_rows = read_tsv(joinpath(REFERENCE, "waveforms.tsv"))
    voltage = reference_voltage()

    field_mismatches = 0
    max_hit_time_error_s = 0.0
    max_feature_error = 0.0
    max_waveform_time_error_s = 0.0
    max_waveform_voltage_error_v = 0.0

    for (hit, row) in zip(data.hits, hit_rows)
    max_hit_time_error_s = max(
        max_hit_time_error_s,
        abs(hit.relative_time - parse(Float64, row[1])),
    )
    field_mismatches += hit.channel == parse(UInt8, row[2]) ? 0 : 1
    for (name, text) in zip(hit_header[3:end], row[3:end])
        actual = Float64(get(hit.features, name, NaN))
        expected = parse(Float64, text)
        max_feature_error = max(max_feature_error, abs(actual - expected))
        field_mismatches += actual == expected ? 0 : 1
    end
    end

    for (waveform, row) in zip(data.waveforms, waveform_rows)
    expected_time = parse(Float64, row[2])
    expected_channel = parse(UInt8, row[3])
    expected_rate = parse(Float64, row[4])
    expected_delay = parse(Int, row[5])
    offset = parse(Int, row[6])
    count = parse(Int, row[7])
    expected_voltage = voltage[offset+1:offset+count]

    field_mismatches += waveform.channel == expected_channel ? 0 : 1
    field_mismatches += waveform.sample_rate == expected_rate ? 0 : 1
    field_mismatches += waveform.trigger_delay == expected_delay ? 0 : 1
    field_mismatches += length(waveform.voltage) == count ? 0 : 1
    max_waveform_time_error_s = max(
        max_waveform_time_error_s,
        abs(waveform.relative_time - expected_time),
    )
    max_waveform_voltage_error_v = max(
        max_waveform_voltage_error_v,
        maximum(abs.(waveform.voltage .- expected_voltage)),
    )
    end

    println("hits=", length(data.hits))
    println("waveforms=", length(data.waveforms))
    println("field_mismatches=", field_mismatches)
    println("max_hit_time_error_s=", max_hit_time_error_s)
    println("max_feature_error=", max_feature_error)
    println("max_waveform_time_error_s=", max_waveform_time_error_s)
    println("max_waveform_voltage_error_v=", max_waveform_voltage_error_v)
    println("unknown_message_entries=", length(data.unknown_message_counts))
    println("unknown_message_total=", sum(values(data.unknown_message_counts)))
end

main()
