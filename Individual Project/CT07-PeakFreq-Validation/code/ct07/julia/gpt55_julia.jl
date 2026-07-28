using DataFrames
using XLSX

include("JuliaOutput.jl")
using .CT07Output

function numeric_column(matrix, column)
    return [cell isa Number ? Float64(cell) : tryparse(Float64, strip(string(cell))) for cell in matrix[:, column]]
end

function run_ct07(input_path, sheet_name, output_dir)
    matrix = XLSX.readxlsx(input_path)[sheet_name][:]
    signals = Dict(column => numeric_column(matrix, column) for column in (1, 3, 4, 5, 9, 10, 12, 14))
    valid(row, columns) = all(column -> !isnothing(signals[column][row]) && isfinite(signals[column][row]), columns)
    mechanical_rows = filter(row -> valid(row, (1, 3, 4)), axes(matrix, 1))
    ae_rows = filter(row -> valid(row, (5, 9, 10, 12, 14)), axes(matrix, 1))
    mechanical = DataFrame(
        record_index=eachindex(mechanical_rows), matrix_row=mechanical_rows,
        t1_s=Float64[signals[1][row] for row in mechanical_rows],
        strain_pct=Float64[signals[3][row] for row in mechanical_rows],
        stress_mpa=Float64[signals[4][row] for row in mechanical_rows],
    )
    ae = DataFrame(
        record_index=eachindex(ae_rows), matrix_row=ae_rows,
        time_s=Float64[signals[5][row] for row in ae_rows],
        rms_norm=Float64[signals[9][row] for row in ae_rows],
        cumrms_norm=Float64[signals[10][row] for row in ae_rows],
        energy_norm=Float64[signals[12][row] for row in ae_rows],
        cumenergy_norm=Float64[signals[14][row] for row in ae_rows],
    )
    write_outputs(mechanical, ae, output_dir, "gpt55_julia", ["replace automatic readtable detection with physical columns", "independent complete-case masks", "callable CLI", "synchronise twin x axes"])
end

length(ARGS) == 3 && run_ct07(ARGS...)
