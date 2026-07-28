using AEPeakFrequency

const CONFIG = AnalysisConfig(1_000_000, 200, 1, 0.1, 8.0)

positional = filter(!=("--no-plots"), ARGS)
length(positional) >= 2 || error("Usage: julia run_analysis.jl <output_dir> <mat_file>... [--no-plots]")
output_dir = abspath(first(positional))
mat_paths = sort(abspath.(positional[2:end]); by=basename)
all(isfile, mat_paths) || error("One or more MAT files do not exist.")
run_analysis(mat_paths, output_dir, CONFIG; write_plots=!("--no-plots" in ARGS))
