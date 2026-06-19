# Headless GR mode must be selected before Plots initializes the backend.
ENV["GKSwstype"] = get(ENV, "GKSwstype", "100")

using XLSX
using DataFrames
using Plots

gr()

const OUTPUT_FILENAMES = (
    "figure_1_strain_stress.png",
    "figure_2_rms.png",
    "figure_3_cumulative_rms.png",
    "figure_4_ae_energy.png",
    "figure_5_cumulative_ae_energy.png",
)

"""Return aligned finite Float64 vectors for rows that are numeric in every requested column."""
function numeric_columns(df::DataFrame, columns::Tuple)
    selected = df[:, collect(columns)]
    mask = [all(value -> value isa Real && isfinite(Float64(value)), row) for row in eachrow(selected)]
    any(mask) || error("No complete numeric rows found in columns $(collect(columns))")
    return tuple((Float64.(df[mask, column]) for column in columns)...)
end

"""Load CT07, clean mixed header/blank rows, create five plots, and save five PNG files."""
function process_acoustic_emission_data(
    filepath::String,
    output_dir::String;
    sheetname::String = "CT07",
)
    isfile(filepath) || error("Workbook not found: $filepath")
    mkpath(output_dir)

    df = XLSX.openxlsx(filepath) do xf
        sheetname in XLSX.sheetnames(xf) || error(
            "Sheet '$sheetname' not found. Available sheets: $(join(XLSX.sheetnames(xf), ", "))",
        )
        DataFrame(xf[sheetname][:], :auto)
    end

    # Mechanical channels begin on row 4; AE channels begin on row 2. Selecting
    # complete numeric rows independently preserves the alignment within each system.
    t1, strain, stress = numeric_columns(df, (1, 3, 4))
    time, rms, cumrms, energy, cumenergy = numeric_columns(df, (5, 9, 10, 12, 14))
    max_stress = maximum(stress)

    function plot_stress_base(x_limit)
        plot(
            t1,
            stress;
            color = :blue,
            linewidth = 2,
            ylabel = "Stress (MPa)",
            xlabel = "Time (s)",
            ylim = (0, max_stress),
            xlim = x_limit,
            grid = true,
            minorgrid = true,
            legend = false,
            size = (1200, 800),
            left_margin = 10Plots.mm,
            right_margin = 18Plots.mm,
        )
    end

    fig1 = plot(
        strain,
        stress;
        color = :blue,
        linewidth = 2,
        ylabel = "Stress (MPa)",
        xlabel = "Strain (%)",
        ylim = (0, 520),
        title = "T07 Strain vs. Stress",
        grid = true,
        minorgrid = true,
        legend = false,
        size = (1200, 800),
        left_margin = 10Plots.mm,
        right_margin = 6Plots.mm,
    )

    fig2 = plot_stress_base((0, 250))
    plot!(
        twinx(fig2),
        time,
        rms;
        color = :red,
        linewidth = 2,
        ylim = (0, 1.05),
        ylabel = "Normalised RMS (a.u.)",
        title = "T09 Commercial Normalised RMS Profile",
        legend = false,
    )

    fig3 = plot_stress_base((0, 300))
    plot!(
        twinx(fig3),
        time,
        cumrms;
        color = :red,
        linewidth = 2,
        ylim = (0, 1.05),
        ylabel = "Normalised Cumulative RMS (a.u.)",
        title = "T07 Commercial Normalised Cumulative RMS",
        legend = false,
    )

    fig4 = plot_stress_base((0, 300))
    scatter!(
        twinx(fig4),
        time,
        energy;
        markersize = 3,
        markerstrokewidth = 0,
        color = :red,
        ylabel = "Normalised AE Energy (a.u.)",
        ylim = (0, 1.05),
        title = "T07 Commercial Normalised AE Energy",
        legend = false,
    )

    fig5 = plot_stress_base((0, 300))
    plot!(
        twinx(fig5),
        time,
        cumenergy;
        color = :red,
        linewidth = 2,
        ylabel = "Normalised Cumulative AE Energy (a.u.)",
        ylim = (0, 1.05),
        title = "T07 Commercial Normalised Cumulative AE Energy",
        legend = false,
    )

    figures = (fig1, fig2, fig3, fig4, fig5)
    for (figure, filename) in zip(figures, OUTPUT_FILENAMES)
        path = joinpath(output_dir, filename)
        savefig(figure, path)
        println("SAVED $path")
    end

    println("MECHANICAL_ROWS $(length(t1))")
    println("AE_ROWS $(length(time))")
    println("MAX_STRESS $max_stress")
    return figures
end

if abspath(PROGRAM_FILE) == @__FILE__
    length(ARGS) in (1, 2) || error("Usage: julia Test3_fixed.jl <workbook.xlsx> [output_dir]")
    workbook_path = abspath(ARGS[1])
    output_dir = length(ARGS) == 2 ? abspath(ARGS[2]) : @__DIR__
    process_acoustic_emission_data(workbook_path, output_dir)
end
