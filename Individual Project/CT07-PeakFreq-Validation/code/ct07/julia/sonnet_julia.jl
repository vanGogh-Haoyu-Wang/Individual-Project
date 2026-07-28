using DataFrames
using XLSX

include("JuliaOutput.jl")
using .CT07Output

function numeric(value)
    value isa Number && return Float64(value)
    return tryparse(Float64, strip(string(value)))
end

function run_ct07(input_path, sheet_name, output_dir)
    raw = XLSX.getdata(XLSX.readxlsx(input_path)[sheet_name])
    signals = Dict(
        name => [numeric(raw[row, column]) for row in axes(raw, 1)]
        for (name, column) in (
            :t1_s => 1, :strain_pct => 3, :stress_mpa => 4, :time_s => 5,
            :rms_norm => 9, :cumrms_norm => 10, :energy_norm => 12, :cumenergy_norm => 14,
        )
    )
    valid(names, row) = all(!isnothing(signals[name][row]) && isfinite(signals[name][row]) for name in names)
    mechanical_rows = [row for row in axes(raw, 1) if valid((:t1_s, :strain_pct, :stress_mpa), row)]
    ae_rows = [row for row in axes(raw, 1) if valid((:time_s, :rms_norm, :cumrms_norm, :energy_norm, :cumenergy_norm), row)]
    mechanical = DataFrame(record_index=1:length(mechanical_rows), matrix_row=mechanical_rows)
    ae = DataFrame(record_index=1:length(ae_rows), matrix_row=ae_rows)
    for name in (:t1_s, :strain_pct, :stress_mpa)
        mechanical[!, name] = Float64[signals[name][row] for row in mechanical_rows]
    end
    for name in (:time_s, :rms_norm, :cumrms_norm, :energy_norm, :cumenergy_norm)
        ae[!, name] = Float64[signals[name][row] for row in ae_rows]
    end
    write_outputs(mechanical, ae, output_dir, "sonnet_julia", ["read complete worksheet instead of first_row=4", "restore first two AE rows", "independent complete-case masks", "synchronise twin x axes"])
end

length(ARGS) == 3 && run_ct07(ARGS...)

