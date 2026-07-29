# ae_analysis_ct07.jl
#
# Acoustic Emission (AE) Analysis – CT-07 Commercial Tensile Test
# ────────────────────────────────────────────────────────────────
# Julia translation of the original MATLAB AE analysis framework.
#
# Dependencies — install once in the Julia REPL before running:
#
#   using Pkg
#   Pkg.add(["XLSX", "DataFrames", "Plots"])
#
# Usage:
#   julia ae_analysis_ct07.jl
#
# Julia-specific notes
# ───────────────────
#   • Column indexing is 1-based in both Julia and MATLAB, so df[:, N]
#     maps directly to MATLAB's data(:, N).
#   • XLSX.readtable treats row 1 as column headers and returns the rest as
#     data, matching MATLAB's xlsread behaviour for numeric-only extraction.
#   • Broadcasting dot syntax (e.g. `isfinite.(v)`) is used for
#     element-wise operations; the comprehension in `to_float` is an explicit
#     form of the same pattern, chosen for clarity when mixing type checks.
#   • `twinx(p)` from Plots.jl overlays a second y-axis sharing p's x-axis,
#     mirroring MATLAB's `yyaxis right`. Plotting to the returned subplot
#     reference controls the right axis; displaying `p` renders both axes.

using XLSX
using DataFrames
using Plots
gr()  # GR backend: fast rendering, no external window dependencies

# ═══════════════════════════════════════════════════════════════════════════════
# § 1  Data Loading
# ═══════════════════════════════════════════════════════════════════════════════

"""
    load_ae_data(filepath, sheet_name) -> NamedTuple

Load AE tensile-test data from *filepath* (Excel workbook), reading
*sheet_name*, and return a NamedTuple of plain `Float64` vectors.

Column mapping — 1-based indices match the original MATLAB `xlsread` call:

| Index | Signal    | Units |
|-------|-----------|-------|
|  1    | t1        | s     |  ← time axis for stress signal
|  3    | strain    | %     |
|  4    | stress    | MPa   |
|  5    | time      | s     |  ← time axis for AE signals
|  9    | rms       | a.u.  |  normalised RMS amplitude
| 10    | cumrms    | a.u.  |  normalised cumulative RMS
| 12    | energy    | a.u.  |  normalised AE energy
| 14    | cumenergy | a.u.  |  normalised cumulative AE energy

Empty / missing cells are replaced with `NaN` so Plots.jl skips them
silently rather than throwing a conversion error.
"""
function load_ae_data(filepath::String, sheet_name::String)

    # XLSX.readtable returns a Tables.jl-compatible object.
    # Wrapping in DataFrame gives us clean positional column access (df[:, N]).
    df = DataFrame(XLSX.readtable(filepath, sheet_name))

    # Element-wise type coercion with safe handling of both `missing`
    # (XLSX.jl ≥ 0.10 default) and `nothing` (older API, empty cells).
    # This is the broadcasting-equivalent manual form.
    function to_float(col)::Vector{Float64}
        return [ismissing(v) || isnothing(v) ? NaN : Float64(v) for v in col]
    end

    return (;
        t1        = to_float(df[:, 1]),   # stress signal time axis
        strain    = to_float(df[:, 3]),   # engineering strain (%)
        stress    = to_float(df[:, 4]),   # engineering stress (MPa)
        time      = to_float(df[:, 5]),   # AE signal time axis
        rms       = to_float(df[:, 9]),   # normalised RMS
        cumrms    = to_float(df[:, 10]),  # normalised cumulative RMS
        energy    = to_float(df[:, 12]),  # normalised AE energy
        cumenergy = to_float(df[:, 14]),  # normalised cumulative AE energy
    )
end

# ═══════════════════════════════════════════════════════════════════════════════
# § 2  Shared Helper – Stress vs. Time (left y-axis base)
# ═══════════════════════════════════════════════════════════════════════════════

"""
    _stress_time_base(t1, stress; xlim_max, fig_title) -> Plots.Plot

Internal helper: build the blue Stress–Time left-axis plot.

Factored out because Figures 2–5 all share an identical left axis before
overlaying different AE signals on the right axis via `twinx()`.

`filter(isfinite, stress)` excludes both `NaN` and `Inf` values introduced
by `to_float` when computing the dynamic y-axis upper limit.
"""
function _stress_time_base(
        t1::Vector{Float64},
        stress::Vector{Float64};
        xlim_max::Real,
        fig_title::String)

    max_stress = maximum(filter(isfinite, stress))

    return plot(t1, stress;
        color     = :blue,
        linewidth = 1.5,
        xlabel    = "Time (s)",
        ylabel    = "Stress (MPa)",
        ylims     = (0.0, max_stress),
        xlims     = (0.0, Float64(xlim_max)),
        title     = fig_title,
        minorgrid = true,   # Julia/Plots equivalent of MATLAB's grid('minor')
        legend    = false)
end

# ═══════════════════════════════════════════════════════════════════════════════
# § 3  Figure 1 – Strain vs. Stress
# ═══════════════════════════════════════════════════════════════════════════════

"""
    fig1_strain_stress(strain, stress) -> Plots.Plot

Single-axis line plot: Engineering Strain (%) on x, Stress (MPa) on y.
Mirrors MATLAB Figure 1.
"""
function fig1_strain_stress(strain::Vector{Float64}, stress::Vector{Float64})
    return plot(strain, stress;
        color     = :blue,
        linewidth = 1.5,
        xlabel    = "Strain (%)",
        ylabel    = "Stress (MPa)",
        ylims     = (0, 520),
        title     = "T07 Strain vs. Stress",
        minorgrid = true,
        legend    = false)
end

# ═══════════════════════════════════════════════════════════════════════════════
# § 4  Figure 2 – Normalised RMS Profile
# ═══════════════════════════════════════════════════════════════════════════════

"""
    fig2_rms_profile(t1, stress, time, rms) -> Plots.Plot

Dual-axis plot:
  Left  (blue)  — Stress vs. Time
  Right (red)   — Normalised RMS vs. Time

⚠ The title "T09" is preserved verbatim from the original MATLAB script;
it is almost certainly a copy-paste error (should be "T07").
"""
function fig2_rms_profile(
        t1::Vector{Float64}, stress::Vector{Float64},
        time::Vector{Float64}, rms::Vector{Float64})

    # Left axis (mirrors MATLAB's `yyaxis left`)
    p = _stress_time_base(t1, stress;
            xlim_max  = 250,
            fig_title = "T09 Commercial Normalised RMS Profile")  # 'T09': as per original MATLAB

    # Right axis (mirrors MATLAB's `yyaxis right`).
    # twinx(p) adds an overlapping subplot sharing p's x-axis and returns a
    # reference to it.  Attributes set here govern the right y-axis only.
    p_right = twinx(p)
    plot!(p_right, time, rms;
        color     = :red,
        linewidth = 1.5,
        ylabel    = "Normalised RMS (a.u.)",
        ylims     = (0, 1.05),
        legend    = false)

    return p  # `p` now contains both axes; display(p) renders the full figure
end

# ═══════════════════════════════════════════════════════════════════════════════
# § 5  Figure 3 – Normalised Cumulative RMS
# ═══════════════════════════════════════════════════════════════════════════════

"""
    fig3_cumrms_profile(t1, stress, time, cumrms) -> Plots.Plot

Dual-axis plot:
  Left  (blue) — Stress vs. Time
  Right (red)  — Normalised Cumulative RMS vs. Time
"""
function fig3_cumrms_profile(
        t1::Vector{Float64}, stress::Vector{Float64},
        time::Vector{Float64}, cumrms::Vector{Float64})

    p = _stress_time_base(t1, stress;
            xlim_max  = 300,
            fig_title = "T07 Commercial Normalised Cumulative RMS")

    p_right = twinx(p)
    plot!(p_right, time, cumrms;
        color     = :red,
        linewidth = 1.5,
        ylabel    = "Normalised Cumulative RMS (a.u.)",
        ylims     = (0, 1.05),
        legend    = false)

    return p
end

# ═══════════════════════════════════════════════════════════════════════════════
# § 6  Figure 4 – Normalised AE Energy (scatter)
# ═══════════════════════════════════════════════════════════════════════════════

"""
    fig4_energy_profile(t1, stress, time, energy) -> Plots.Plot

Dual-axis plot:
  Left  (blue) — Stress vs. Time (line)
  Right (red)  — Normalised AE Energy vs. Time (scatter)

Uses `scatter!` to replicate MATLAB's `scatter()` call.
`markerstrokewidth = 0` removes the border ring on each marker
(equivalent to MATLAB's `markerstrokewidth = 0`).
`markersize = 5` matches MATLAB's `markersize = 5`.
"""
function fig4_energy_profile(
        t1::Vector{Float64}, stress::Vector{Float64},
        time::Vector{Float64}, energy::Vector{Float64})

    p = _stress_time_base(t1, stress;
            xlim_max  = 300,
            fig_title = "T07 Commercial Normalised AE Energy")

    p_right = twinx(p)
    scatter!(p_right, time, energy;
        markersize        = 5,
        markerstrokewidth = 0,      # no border ring — matches MATLAB original
        color             = :red,
        ylabel            = "Normalised AE Energy (a.u.)",
        ylims             = (0, 1.05),
        legend            = false)

    return p
end

# ═══════════════════════════════════════════════════════════════════════════════
# § 7  Figure 5 – Normalised Cumulative AE Energy
# ═══════════════════════════════════════════════════════════════════════════════

"""
    fig5_cumenergy_profile(t1, stress, time, cumenergy) -> Plots.Plot

Dual-axis plot:
  Left  (blue) — Stress vs. Time
  Right (red)  — Normalised Cumulative AE Energy vs. Time
"""
function fig5_cumenergy_profile(
        t1::Vector{Float64}, stress::Vector{Float64},
        time::Vector{Float64}, cumenergy::Vector{Float64})

    p = _stress_time_base(t1, stress;
            xlim_max  = 300,
            fig_title = "T07 Commercial Normalised Cumulative AE Energy")

    p_right = twinx(p)
    plot!(p_right, time, cumenergy;
        color     = :red,
        linewidth = 1.5,
        ylabel    = "Normalised Cumulative AE Energy (a.u.)",
        ylims     = (0, 1.05),
        legend    = false)

    return p
end

# ═══════════════════════════════════════════════════════════════════════════════
# § 8  Entry Point
# ═══════════════════════════════════════════════════════════════════════════════

"""
    main() -> NTuple{5, Plots.Plot}

Orchestrates data loading and figure generation for the CT-07 AE analysis.
Returns all five plot objects so the caller can optionally save them:

    figs = main()
    savefig(figs[1], "ct07_strain_stress.png")
"""
function main()
    filepath   = "Tensile-processed.xlsx"
    sheet_name = "CT-07"

    println("─── CT-07 AE Analysis ─────────────────────────────────────")
    println("  File  : $filepath")
    println("  Sheet : $sheet_name")

    d = load_ae_data(filepath, sheet_name)
    println("  Loaded $(length(d.t1)) data points.\n")

    # Build figures
    fig1 = fig1_strain_stress(d.strain, d.stress)
    fig2 = fig2_rms_profile(d.t1, d.stress, d.time, d.rms)
    fig3 = fig3_cumrms_profile(d.t1, d.stress, d.time, d.cumrms)
    fig4 = fig4_energy_profile(d.t1, d.stress, d.time, d.energy)
    fig5 = fig5_cumenergy_profile(d.t1, d.stress, d.time, d.cumenergy)

    # Render — each `display` call opens a GR window (or inlines in Jupyter)
    display(fig1)
    display(fig2)
    display(fig3)
    display(fig4)
    display(fig5)

    println("All five figures rendered successfully.")
    return (fig1, fig2, fig3, fig4, fig5)
end

# Run when executed as a script: `julia ae_analysis_ct07.jl`
main()
