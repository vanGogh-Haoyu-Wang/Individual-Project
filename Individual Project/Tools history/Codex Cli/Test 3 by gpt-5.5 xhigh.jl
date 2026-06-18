using XLSX
using DataFrames
using Plots

gr()  # Use the GR backend, matching the requested Plots.jl setup.

const DATA_FILE = "Tensile-processed.xlsx"
const SHEET_NAME = "CT-07"

function load_ct07(path::AbstractString=DATA_FILE; sheet::AbstractString=SHEET_NAME)
    # XLSX.readtable reads the named worksheet as tabular data; DataFrame gives
    # convenient column-position indexing while preserving Julia's 1-based logic.
    return DataFrame(XLSX.readtable(path, sheet))
end

function numeric_column(df::DataFrame, j::Integer)
    @assert 1 <= j <= ncol(df) "Column $j not found; sheet has $(ncol(df)) columns."

    # Julia and MATLAB are both 1-based, so df[!, 1] corresponds to data(:, 1).
    # Broadcasting converts the full column element-wise and maps missing cells to NaN.
    return Float64.(coalesce.(df[!, j], NaN))
end

function extract_signals(df::DataFrame)
    return (
        t1        = numeric_column(df, 1),
        stress    = numeric_column(df, 4),
        strain    = numeric_column(df, 3),
        time      = numeric_column(df, 5),
        rms       = numeric_column(df, 9),
        cumrms    = numeric_column(df, 10),
        energy    = numeric_column(df, 12),
        cumenergy = numeric_column(df, 14),
    )
end

finite_max(x) = maximum(v for v in x if isfinite(v))

const COMMON_PLOT_KW = (
    legend = false,
    linewidth = 1.5,
    grid = true,
    minorgrid = true,
    minorticks = 5,
)

function plot_strain_stress(s)
    return plot(
        s.strain,
        s.stress;
        color = :blue,
        xlabel = "Strain (%)",
        ylabel = "Stress (MPa)",
        ylims = (0, 520),
        title = "T07 Strain vs. Stress",
        COMMON_PLOT_KW...,
    )
end

function plot_stress_with_signal(
    s,
    signal;
    right_ylabel::AbstractString,
    title_text::AbstractString,
    xmax::Real,
    scatter_right::Bool=false,
)
    p = plot(
        s.t1,
        s.stress;
        color = :blue,
        xlabel = "Time (s)",
        ylabel = "Stress (MPa)",
        ylims = (0, finite_max(s.stress)),
        xlims = (0, xmax),
        title = title_text,
        COMMON_PLOT_KW...,
    )

    right_axis = twinx()

    if scatter_right
        scatter!(
            right_axis,
            s.time,
            signal;
            markersize = 5,
            markerstrokewidth = 0,
            color = :red,
            ylabel = right_ylabel,
            ylims = (0, 1.05),
            legend = false,
        )
    else
        plot!(
            right_axis,
            s.time,
            signal;
            color = :red,
            linewidth = 1.5,
            ylabel = right_ylabel,
            ylims = (0, 1.05),
            legend = false,
        )
    end

    return p
end

function make_plots(s)
    fig1 = plot_strain_stress(s)

    fig2 = plot_stress_with_signal(
        s,
        s.rms;
        right_ylabel = "Normalised RMS (a.u.)",
        title_text = "T09 Commercial Normalised RMS Profile",
        xmax = 250,
    )

    fig3 = plot_stress_with_signal(
        s,
        s.cumrms;
        right_ylabel = "Normalised Cumulative RMS (a.u.)",
        title_text = "T07 Commercial Normalised Cumulative RMS",
        xmax = 300,
    )

    fig4 = plot_stress_with_signal(
        s,
        s.energy;
        right_ylabel = "Normalised AE Energy (a.u.)",
        title_text = "T07 Commercial Normalised AE Energy",
        xmax = 300,
        scatter_right = true,
    )

    fig5 = plot_stress_with_signal(
        s,
        s.cumenergy;
        right_ylabel = "Normalised Cumulative AE Energy (a.u.)",
        title_text = "T07 Commercial Normalised Cumulative AE Energy",
        xmax = 300,
    )

    return (; fig1, fig2, fig3, fig4, fig5)
end

function main(; filepath::AbstractString=DATA_FILE, sheet::AbstractString=SHEET_NAME)
    df = load_ct07(filepath; sheet)
    signals = extract_signals(df)
    figs = make_plots(signals)

    foreach(display, values(figs))
    return figs
end

if abspath(PROGRAM_FILE) == @__FILE__
    main()
end