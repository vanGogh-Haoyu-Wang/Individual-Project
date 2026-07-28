using DataFrames
using XLSX

include("JuliaOutput.jl")
using .CT07Output

asnumber(value) = value isa Number ? Float64(value) : tryparse(Float64, strip(string(value)))

function run_ct07(input_path, sheet_name, output_dir)
    matrix = XLSX.readxlsx(input_path)[sheet_name][:]
    numeric = Matrix{Union{Nothing,Float64}}(undef, size(matrix))
    for index in eachindex(matrix)
        numeric[index] = asnumber(matrix[index])
    end
    mechanical_rows = [row for row in axes(numeric, 1) if all(index -> !isnothing(numeric[row, index]) && isfinite(numeric[row, index]), (1, 3, 4))]
    ae_rows = [row for row in axes(numeric, 1) if all(index -> !isnothing(numeric[row, index]) && isfinite(numeric[row, index]), (5, 9, 10, 12, 14))]
    mechanical = DataFrame(
        record_index=1:length(mechanical_rows), matrix_row=mechanical_rows,
        t1_s=Float64[numeric[row, 1] for row in mechanical_rows],
        strain_pct=Float64[numeric[row, 3] for row in mechanical_rows],
        stress_mpa=Float64[numeric[row, 4] for row in mechanical_rows],
    )
    ae = DataFrame(
        record_index=1:length(ae_rows), matrix_row=ae_rows,
        time_s=Float64[numeric[row, 5] for row in ae_rows],
        rms_norm=Float64[numeric[row, 9] for row in ae_rows],
        cumrms_norm=Float64[numeric[row, 10] for row in ae_rows],
        energy_norm=Float64[numeric[row, 12] for row in ae_rows],
        cumenergy_norm=Float64[numeric[row, 14] for row in ae_rows],
    )
    write_outputs(mechanical, ae, output_dir, "deepseek_julia", ["replace readtable with physical worksheet matrix", "mixed-cell conversion", "independent complete-case masks", "CLI/headless export"])
end

length(ARGS) == 3 && run_ct07(ARGS...)

