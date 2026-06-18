# User

Act as a Senior Scientific Computing Engineer and Julia Specialist. I am working on an MSc project migrating an Acoustic Emission (AE) analysis framework from MATLAB to Julia.

Your task is to translate the following MATLAB script into idiomatic Julia.

Requirements & Constraints:

1. Data Loading: Use `XLSX.jl` and `DataFrames.jl` to load the "Tensile-processed.xlsx" file. Ensure you read the specific sheet 'CT-07'.
2. Array Indexing: Note that Julia, like MATLAB, uses 1-based indexing. Ensure the column slicing matches the original MATLAB logic correctly (e.g., MATLAB's `data(:, 1)` should be handled appropriately in the context of a DataFrame or Matrix).
3. Broadcasting: Use Julia's broadcasting dot syntax (e.g., `sin.(x)`) for element-wise operations to ensure high performance.
4. Visualization: Use the `Plots.jl` library (with the GR backend). Replicate the dual-axis plots (`yyaxis left` and `yyaxis right`) using `twinx()`. Ensure titles, labels, and limits match the original script.
5. Readability: Keep the code modular. Wrap the logic in a main function or descriptive sub-functions. Add brief comments explaining the Julia-specific implementation choices.

Here is the original MATLAB code:

```matlab
data = xlsread("Tensile-processed.xlsx", 'CT-07'); 
% Selection of specific data from the sheet to be used for plotting 
t1 = data(:, 1);
stress = data(:, 4);
strain = data(:, 3); 
time = data(:,5);
rms = data(:, 9);
cumrms = data(:, 10);
energy = data(:, 12);
cumenergy = data(:, 14);

fig1 = figure; % Strain vs Stress plot
plot(strain, stress, 'b')
ylabel('Stress (MPa)');
xlabel('Strain (%)');
ylim([0 520]);
title('T07 Strain vs. Stress');
grid('minor');

fig2 = figure; 
yyaxis left % Stress vs time plot
plot(t1, stress, 'b')
ylabel('Stress (MPa)');
xlabel('Time (s)');
ylim([0 max(stress)]);
xlim([0 250]);

yyaxis right % Normalised RMS scatter plot
plot(time, rms, 'r')
ylim([0 1.05]);
ylabel('Normalised RMS (a.u.)');
title('T09 Commercial Normalised RMS Profile');
grid('minor');

fig3 = figure;
yyaxis left % Stress vs time plot
plot(t1, stress, 'b')
ylabel('Stress (MPa)');
xlabel('Time (s)');
ylim([0 max(stress)]);
xlim([0 300]);

yyaxis right % Normalised cumulative RMS plot
plot(time, cumrms, 'r')
ylim([0 1.05]);
ylabel('Normalised Cumulative RMS (a.u.)');
title('T07 Commercial Normalised Cumulative RMS');
grid('minor');

fig4 = figure;
yyaxis left % Stress vs time plot
plot(t1, stress, 'b')
ylabel('Stress (MPa)');
xlabel('Time (s)');
ylim([0 max(stress)]);
xlim([0 300]);

yyaxis right % Normalised AE energy plot
scatter(time, energy, markersize=5, markerstrokewidth=0, color=:red)
ylabel('Normalised AE Energy (a.u.)');
ylim([0 1.05]);
title('T07 Commercial Normalised AE Energy');
grid('minor');

fig5 = figure;
yyaxis left % Stress vs time plot
plot(t1, stress, 'b')
ylabel('Stress (MPa)');
xlabel('Time (s)');
ylim([0 max(stress)]);
xlim([0 300]);

yyaxis right % Normalised cumulative AE energy plot
plot(time, cumenergy, 'r')
ylabel('Normalised Cumulative AE Energy (a.u.)');
ylim([0 1.05]);
title('T07 Commercial Normalised Cumulative AE Energy');
grid('minor');
```

# Assistant

I’ll use the Superpowers guidance briefly here because this is a code-translation/design task, then I’ll give you a clean Julia version that maps the MATLAB plotting semantics directly.

# Assistant

Here is an idiomatic Julia translation. I kept the MATLAB column positions exactly, including the `T09` title in `fig2` since you asked for titles to match the original.

```julia
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
```

If the Excel sheet has no header row, `XLSX.readtable` may treat the first data row as headers. In that case, use a raw matrix read instead; but for a processed Excel table with column headers, this version is the closest Julia analogue. XLSX.jl’s `readtable` to `DataFrame` pattern is documented in the XLSX.jl tutorial: 【0†source】([felipenoris.github.io](https://felipenoris.github.io/XLSX.jl/stable/tutorial/)).

---
# Find mistake

Because in the original MATLAB code, the title of Figure 2 was hard-coded as:

```
title_text = "T09 Commercial Normalised RMS Profile"
```
But it reads CT-07/CT07 data, so this should be a typo in the original script. The Julia version retains it for faithful translation. The correct title should be changed to:

```
title_text = "T07 Commercial Normalised RMS Profile"
```
*So this isn't an LLM problem, it's the original script's problem.*

---
# Run and results:
Figure 1:
![[T3gptjlfig1.png]]
Figure 2:
![[T3gptjlfig2.png]]
Figure 3:
![[T3gptjlfig3.png]]
Figure 4:
![[T3gptjlfig4.png]]
Figure 5 :
![[T3gptjlfig5.png]]