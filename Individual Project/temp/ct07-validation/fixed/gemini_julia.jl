using DataFrames
using XLSX

include("JuliaOutput.jl")
using .CT07Output

tofloat(value) = value isa Number ? Float64(value) : tryparse(Float64, strip(string(value)))
finite(value) = !isnothing(value) && isfinite(value)

function run_ct07(input_path, sheet_name, output_dir)
    data = XLSX.readxlsx(input_path)[sheet_name][:]
    columns = Dict(index => [tofloat(data[row, index]) for row in axes(data, 1)] for index in (1, 3, 4, 5, 9, 10, 12, 14))
    mechanical_rows = [row for row in axes(data, 1) if all(finite(columns[index][row]) for index in (1, 3, 4))]
    ae_rows = [row for row in axes(data, 1) if all(finite(columns[index][row]) for index in (5, 9, 10, 12, 14))]
    mechanical = DataFrame(
        record_index=1:length(mechanical_rows), matrix_row=mechanical_rows,
        t1_s=Float64[columns[1][row] for row in mechanical_rows],
        strain_pct=Float64[columns[3][row] for row in mechanical_rows],
        stress_mpa=Float64[columns[4][row] for row in mechanical_rows],
    )
    ae = DataFrame(
        record_index=1:length(ae_rows), matrix_row=ae_rows,
        time_s=Float64[columns[5][row] for row in ae_rows],
        rms_norm=Float64[columns[9][row] for row in ae_rows],
        cumrms_norm=Float64[columns[10][row] for row in ae_rows],
        energy_norm=Float64[columns[12][row] for row in ae_rows],
        cumenergy_norm=Float64[columns[14][row] for row in ae_rows],
    )
    write_outputs(mechanical, ae, output_dir, "gemini_julia", ["enable callable entry point", "safe mixed-cell conversion", "independent complete-case masks", "headless output contract"])
end

length(ARGS) == 3 && run_ct07(ARGS...)

