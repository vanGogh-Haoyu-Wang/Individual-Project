#!/usr/bin/env julia
#=
Acoustic Emission (AE) Analysis — MATLAB → Julia Translation
=============================================================
Original MATLAB script: Tensile test data visualisation
Julia version:        Idiomatic, modular, Plots.jl + GR backend

Column layout of "Tensile-processed.xlsx" / sheet "CT-07":
   1: t1 (time axis variant 1)
   3: Strain (%)
   4: Stress (MPa)
   5: Time (s)
   9: Normalised RMS
  10: Normalised Cumulative RMS
  12: Normalised AE Energy
  14: Normalised Cumulative AE Energy
=#

using XLSX, DataFrames, Plots
gr()  # GR backend — fast, publication-quality vector output

# --------------------------------------------------------------------------- #
#  Data Loading                                                               #
# --------------------------------------------------------------------------- #

"""
    load_tensile_data(filepath, sheet)

Read tensile-test data from an Excel workbook and return extracted columns as a
NamedTuple.

**Julia notes:**
- `XLSX.readtable` returns a Tables.jl-compatible object; `DataFrame()` wraps it.
- `df[:, col]` with an integer uses **1-based positional indexing** — identical to
  MATLAB's `data(:, col)` so no index adjustments are needed.
- Missing/empty cells are skipped with `dropmissing` so Plots.jl doesn't error.
"""
function load_tensile_data(filepath::String, sheet::String)
    df = DataFrame(XLSX.readtable(filepath, sheet))

    # Drop rows with missing values in the columns we care about.
    # This guards against trailing empty rows common in instrument exports.
    key_cols = [1, 3, 4, 5, 9, 10, 12, 14]
    df_clean = dropmissing(df[:, key_cols])

    return (;
        t1         = df_clean[:, 1],   # time axis 1
        strain     = df_clean[:, 3],   # Strain (%)
        stress     = df_clean[:, 4],   # Stress (MPa)
        time       = df_clean[:, 5],   # time axis 2 (s)
        rms        = df_clean[:, 9],   # Normalised RMS
        cumrms     = df_clean[:, 10],  # Normalised cumulative RMS
        energy     = df_clean[:, 12],  # Normalised AE energy
        cumenergy  = df_clean[:, 14],  # Normalised cumulative AE energy
    )
end

# --------------------------------------------------------------------------- #
#  Plotting Helpers                                                           #
# --------------------------------------------------------------------------- #

"""
    twin_plot!(p, x, y; color, ylabel, ylims, plot_type, markersize)

Add a right-y-axis trace onto an existing left-axis plot `p`.

**Julia notes:**
- `twinx()` creates an overlaid subplot that shares the x-axis — the idiomatic
  Plots.jl equivalent of MATLABʼs `yyaxis right`.
- `plot!` / `scatter!` mutate the twin axis in-place (note the `!` convention),
  avoiding unnecessary copies of potentially large AE time series.
- All element-wise operations use Juliaʼs **dot-broadcasting** syntax (e.g.,
  `sin.(x)`) for fused-vector performance without allocations.
"""
function twin_plot!(p, x, y;
                    color   = :red,
                    ylabel  = "",
                    ylims   = (0, 1.05),
                    plot_type = :line,
                    markersize = 5)
    p_twin = twinx(p)                        # create right-side y-axis

    if plot_type == :scatter
        scatter!(p_twin, x, y;
                 color           = color,
                 label           = nothing,
                 markersize      = markersize,
                 markerstrokewidth = 0)       # match MATLAB: no stroke
    else
        plot!(p_twin, x, y;
              color = color,
              label = nothing)
    end

    ylabel!(p_twin, ylabel)
    ylims!(p_twin, ylims)
    return p
end

# --------------------------------------------------------------------------- #
#  Figure Generators                                                          #
# --------------------------------------------------------------------------- #

function fig1_strain_vs_stress(strain, stress)
    """T07 Strain vs. Stress — single-axis line plot."""
    plot(strain, stress;
         color     = :blue,
         label     = nothing,
         ylabel    = "Stress (MPa)",
         xlabel    = "Strain (%)",
         ylims     = (0, 520),
         title     = "T07 Strain vs. Stress",
         minorgrid = true)                    # replaces grid('minor')
end

function fig2_stress_rms(t1, stress, time, rms)
    """T09: Stress vs Time (left) + Normalised RMS scatter (right)."""
    p = plot(t1, stress;
             color     = :blue,
             label     = nothing,
             ylabel    = "Stress (MPa)",
             xlabel    = "Time (s)",
             ylims     = (0, maximum(stress)),  # dot-broadcast friendly alternative
             xlims     = (0, 250),
             title     = "T09 Commercial Normalised RMS Profile",
             minorgrid = true)

    twin_plot!(p, time, rms;
               color  = :red,
               ylabel = "Normalised RMS (a.u.)",
               ylims  = (0, 1.05))
    return p
end

function fig3_stress_cumrms(t1, stress, time, cumrms)
    """T07: Stress vs Time (left) + Normalised Cumulative RMS (right)."""
    p = plot(t1, stress;
             color     = :blue,
             label     = nothing,
             ylabel    = "Stress (MPa)",
             xlabel    = "Time (s)",
             ylims     = (0, maximum(stress)),
             xlims     = (0, 300),
             title     = "T07 Commercial Normalised Cumulative RMS",
             minorgrid = true)

    twin_plot!(p, time, cumrms;
               color  = :red,
               ylabel = "Normalised Cumulative RMS (a.u.)",
               ylims  = (0, 1.05))
    return p
end

function fig4_stress_energy(t1, stress, time, energy)
    """T07: Stress vs Time (left) + Normalised AE Energy scatter (right)."""
    p = plot(t1, stress;
             color     = :blue,
             label     = nothing,
             ylabel    = "Stress (MPa)",
             xlabel    = "Time (s)",
             ylims     = (0, maximum(stress)),
             xlims     = (0, 300),
             title     = "T07 Commercial Normalised AE Energy",
             minorgrid = true)

    twin_plot!(p, time, energy;
               color     = :red,
               ylabel    = "Normalised AE Energy (a.u.)",
               ylims     = (0, 1.05),
               plot_type = :scatter,
               markersize = 5)
    return p
end

function fig5_stress_cumenergy(t1, stress, time, cumenergy)
    """T07: Stress vs Time (left) + Normalised Cumulative AE Energy (right)."""
    p = plot(t1, stress;
             color     = :blue,
             label     = nothing,
             ylabel    = "Stress (MPa)",
             xlabel    = "Time (s)",
             ylims     = (0, maximum(stress)),
             xlims     = (0, 300),
             title     = "T07 Commercial Normalised Cumulative AE Energy",
             minorgrid = true)

    twin_plot!(p, time, cumenergy;
               color  = :red,
               ylabel = "Normalised Cumulative AE Energy (a.u.)",
               ylims  = (0, 1.05))
    return p
end

# --------------------------------------------------------------------------- #
#  Main Entry Point                                                           #
# --------------------------------------------------------------------------- #

function main(; filepath = "Tensile-processed.xlsx", sheet = "CT-07")
    # ── Load ──────────────────────────────────────────────────────────────
    println("Loading $filepath → sheet '$sheet' …")
    d = load_tensile_data(filepath, sheet)
    println("Loaded $(length(d.stress)) data points.")

    # ── Plot ──────────────────────────────────────────────────────────────
    p1 = fig1_strain_vs_stress(d.strain, d.stress)
    p2 = fig2_stress_rms(d.t1, d.stress, d.time, d.rms)
    p3 = fig3_stress_cumrms(d.t1, d.stress, d.time, d.cumrms)
    p4 = fig4_stress_energy(d.t1, d.stress, d.time, d.energy)
    p5 = fig5_stress_cumenergy(d.t1, d.stress, d.time, d.cumenergy)

    # Display interactively (REPL / Jupyter / VS Code plot pane)
    display(p1)
    display(p2)
    display(p3)
    display(p4)
    display(p5)

    # ── Optional: batch-save to disk ──────────────────────────────────────
    # Uncomment the block below to export PNG/PDF figures:
    #
    # outdir = "figures"
    # mkpath(outdir)
    # savefig(p1, joinpath(outdir, "fig1_strain_vs_stress.png"))
    # savefig(p2, joinpath(outdir, "fig2_stress_rms.png"))
    # savefig(p3, joinpath(outdir, "fig3_stress_cumrms.png"))
    # savefig(p4, joinpath(outdir, "fig4_stress_energy.png"))
    # savefig(p5, joinpath(outdir, "fig5_stress_cumenergy.png"))
    # println("Figures saved to $outdir/")

    return (; p1, p2, p3, p4, p5)
end

# --------------------------------------------------------------------------- #
#  Execution                                                                  #
# --------------------------------------------------------------------------- #
if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
