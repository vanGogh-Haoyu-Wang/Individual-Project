using MistrasWFSJulia

const ROOT = normpath(joinpath(@__DIR__, ".."))
const FIXTURE = joinpath(ROOT, "test", "data", "ExampleWFSdata.wfs")
const REFERENCE = joinpath(ROOT, "test", "reference")
const OUTPUT = joinpath(ROOT, "results", "comparison_summary.toml")

function reference_header()
    rows = split.(readlines(joinpath(REFERENCE, "header.tsv"))[2:end], '\t')
    Dict(row[1] => row[2] for row in rows)
end

function reference_voltage()
    bytes = read(joinpath(REFERENCE, "waveforms.f64le"))
    length(bytes) % 8 == 0 || error("invalid reference waveform byte length")
    values = [
        reinterpret(Float64, ltoh(reinterpret(UInt64, bytes[index:index+7])[1]))
        for index in 1:8:length(bytes)
    ]
    reshape(values, 2, :)
end

toml_array(values) = "[" * join(repr.(values), ", ") * "]"

function main()
expected = reference_header()
reference = reference_voltage()
data = read_wfs(FIXTURE)
header = data.header

expected_channels = parse.(UInt8, split(expected["channel_numbers"], ','))
actual_channels = header.channel_numbers
missing_channels = setdiff(expected_channels, actual_channels)
extra_channels = setdiff(actual_channels, expected_channels)
channel_order_matches = expected_channels == actual_channels

expected_sample_count = parse(Int, expected["sample_count"])
actual_sample_counts = fill(size(data.voltage_mv, 2), length(actual_channels))
missing_samples = Int[]
voltage_value_mismatches = 0
max_abs_voltage_error_mv = 0.0

for channel in expected_channels
    expected_row = findfirst(==(channel), expected_channels)
    actual_row = findfirst(==(channel), actual_channels)
    actual_count = actual_row === nothing ? 0 : actual_sample_counts[actual_row]
    push!(missing_samples, max(expected_sample_count - actual_count, 0))
    actual_row === nothing && continue

    common_count = min(expected_sample_count, actual_count)
    for column in 1:common_count
        error_mv = abs(data.voltage_mv[actual_row, column] - reference[expected_row, column])
        voltage_value_mismatches += error_mv == 0.0 ? 0 : 1
        max_abs_voltage_error_mv = max(max_abs_voltage_error_mv, error_mv)
    end
end

extra_samples = [
    max(
        actual_sample_counts[row] -
        (channel in expected_channels ? expected_sample_count : 0),
        0,
    )
    for (row, channel) in enumerate(actual_channels)
]

header_mismatch_fields = String[]
header.num_channels == parse(Int, expected["num_channels"]) ||
    push!(header_mismatch_fields, "num_channels")
header.sample_rate_hz == parse.(Int, split(expected["sample_rate_hz"], ',')) ||
    push!(header_mismatch_fields, "sample_rate_hz")
header.pretrigger_samples == parse.(Int, split(expected["pretrigger_samples"], ',')) ||
    push!(header_mismatch_fields, "pretrigger_samples")
header.max_voltage_v == parse.(Float64, split(expected["max_voltage_v"], ',')) ||
    push!(header_mismatch_fields, "max_voltage_v")
header.header_length == parse(Int, expected["header_length"]) ||
    push!(header_mismatch_fields, "header_length")
header.channel_numbers == expected_channels ||
    push!(header_mismatch_fields, "channel_numbers")

axes_seconds = waveform_axes(data, expected_channels[1])
time_errors_s = [
    abs(axes_seconds.time[1] - parse(Float64, expected["time_start_s"])),
    abs(
        (axes_seconds.time[2] - axes_seconds.time[1]) -
        parse(Float64, expected["time_step_s"]),
    ),
    abs(axes_seconds.time[end] - parse(Float64, expected["time_end_s"])),
]
time_axis_mismatches = count(!=(0.0), time_errors_s)
max_abs_time_error_s = maximum(time_errors_s)

passed = isempty(missing_channels) &&
         isempty(extra_channels) &&
         channel_order_matches &&
         all(==(0), missing_samples) &&
         all(==(0), extra_samples) &&
         isempty(header_mismatch_fields) &&
         time_axis_mismatches == 0 &&
         voltage_value_mismatches == 0

open(OUTPUT, "w") do io
    println(io, "schema_version = 1")
    println(io, "status = ", repr(passed ? "passed" : "failed"))
    println(io, "passed = ", passed)
    println(io)
    println(io, "[scope]")
    println(io, "fixture = ", repr("test/data/ExampleWFSdata.wfs"))
    println(io, "numerical_reference = ", repr("MATLAB R2026a fixture export"))
    println(io, "fixture_variant_only = true")
    println(io, "material_provenance = ", repr("not_available"))
    println(io, "raw_count_reference_available = false")
    println(io)
    println(io, "[channels]")
    println(io, "expected = ", length(expected_channels))
    println(io, "actual = ", length(actual_channels))
    println(io, "expected_order = ", toml_array(Int.(expected_channels)))
    println(io, "actual_order = ", toml_array(Int.(actual_channels)))
    println(io, "missing_in_julia = ", toml_array(Int.(missing_channels)))
    println(io, "extra_in_julia = ", toml_array(Int.(extra_channels)))
    println(io, "order_matches = ", channel_order_matches)
    println(io)
    println(io, "[samples]")
    println(io, "expected_per_channel = ", expected_sample_count)
    println(io, "actual_per_channel = ", toml_array(actual_sample_counts))
    println(io, "missing_in_julia_per_expected_channel = ", toml_array(missing_samples))
    println(io, "extra_in_julia_per_actual_channel = ", toml_array(extra_samples))
    println(io, "missing_in_julia_total = ", sum(missing_samples))
    println(io, "extra_in_julia_total = ", sum(extra_samples))
    println(io)
    println(io, "[header]")
    println(io, "field_mismatches = ", length(header_mismatch_fields))
    println(io, "mismatch_fields = ", toml_array(header_mismatch_fields))
    println(io)
    println(io, "[time_axis]")
    println(io, "field_mismatches = ", time_axis_mismatches)
    println(io, "max_abs_error_s = ", repr(max_abs_time_error_s))
    println(io)
    println(io, "[voltage]")
    println(io, "compared_values = ", length(reference))
    println(io, "value_mismatches = ", voltage_value_mismatches)
    println(io, "max_abs_error_mv = ", repr(max_abs_voltage_error_mv))
    println(io, "exact_full_matrix_match = ", voltage_value_mismatches == 0)
end

println("comparison_summary=", relpath(OUTPUT, ROOT))
println("missing_channels=", length(missing_channels))
println("extra_channels=", length(extra_channels))
println("missing_samples=", sum(missing_samples))
println("extra_samples=", sum(extra_samples))
println("voltage_value_mismatches=", voltage_value_mismatches)
println("max_abs_voltage_error_mv=", max_abs_voltage_error_mv)
println("passed=", passed)

passed || exit(1)
end

main()
