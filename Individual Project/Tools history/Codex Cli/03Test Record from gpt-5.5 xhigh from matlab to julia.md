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

---
# Evaluation: Objective Assessment of the MATLAB-to-Julia Translation

## 1. Indexing Logic - **Good in Isolation / Blocked by the Data Model**

* **Assessment**: The translation correctly recognised that MATLAB and Julia are both 1-based. The requested physical-column mappings were transcribed accurately:
  * MATLAB `data(:, 1)` -> Julia column 1 (`t1`)
  * MATLAB `data(:, 3)` -> Julia column 3 (`strain`)
  * MATLAB `data(:, 4)` -> Julia column 4 (`stress`)
  * MATLAB `data(:, 5)` -> Julia column 5 (`time`)
  * MATLAB columns 9, 10, 12, and 14 -> Julia columns 9, 10, 12, and 14
* **Important distinction**: The index numbers are not the source of the failure. The failure occurs because `DataFrame(XLSX.readtable(path, sheet))` does not preserve the worksheet as the same physical A:N matrix returned by MATLAB's `xlsread`.
* **Observed behaviour**: For the supplied `Commercial Tensile Tests.xlsx` workbook and its actual `CT07` sheet, `XLSX.readtable` identifies only a nine-column table corresponding to Excel columns E:M. Consequently, `df[!, 1]` represents Excel column E rather than A, and `extract_signals` terminates when it requests DataFrame column 10:

  ```text
  AssertionError: Column 10 not found; sheet has 9 columns.
  ```

* **Conclusion**: The 1-based indexing conversion is correct as written, but it is applied to an incorrectly constructed table. The unmodified loading and extraction pipeline is therefore not functionally equivalent to the MATLAB code.

## 2. XLSX and DataFrame Usage - **Poor / Blocking Defect**

* **Assessment**: The chosen packages are appropriate, but `XLSX.readtable` is the wrong abstraction for this particular worksheet layout.
* **Worksheet structure**:
  * Mechanical-test data occupy columns A:D and begin on row 4, providing 1,807 numeric records.
  * AE data occupy columns E:N and begin on row 2, providing 5,850 numeric records.
  * The top rows contain blanks, text labels, units, and a numeric normalisation value; column N also has a blank header.
* Because the worksheet contains two adjacent regions with different header rows and different valid lengths, it is not a conventional rectangular table. `readtable` selects the E:M region and omits the other physical columns required by the MATLAB script.
* The default constants also refer to `Tensile-processed.xlsx` and `CT-07`, whereas the supplied workbook is `Commercial Tensile Tests.xlsx` and the actual sheet name is `CT07`. Runtime overrides can work around the names, but not the table-shape problem.
* **Conclusion**: This is the primary blocking defect. With the supplied workbook, the original Julia `main()` cannot reach the plotting stage.
* **Required approach**: Read an explicit physical range with the available XLSX.jl API, for example `XLSX.readdata(path, sheet, "A1:N5851")`, then parse the mechanical and AE regions independently while preserving their separate valid-row domains. Recommendations should be limited to APIs that exist in the tested XLSX.jl version.

## 3. Broadcasting and Type Handling - **Good / Limited Robustness**

* **Assessment**: The code uses Julia broadcasting correctly:

  ```julia
  Float64.(coalesce.(df[!, j], NaN))
  ```

  This is concise and correctly maps `missing` values to `NaN` when the remaining entries are already numeric.
* **Limitation**: `coalesce` does not convert strings. A mixed-type column containing labels or units would still cause `Float64.(...)` to fail. This matters for the supplied worksheet, whose upper rows contain text.
* **Conclusion**: The broadcasting syntax is idiomatic, but the conversion function is not a general equivalent of MATLAB `xlsread` or Python's `pd.to_numeric(..., errors="coerce")`.

## 4. Plot Object Management - **Good Structure / Partial Visual Equivalence**

* **Strengths**:
  * `plot_stress_with_signal` removes repeated dual-axis plotting code.
  * Colours, labels, Y limits, titles, grid settings, and the Figure 4 scatter/line distinction follow the MATLAB script.
  * Preserving the `T09` title in Figure 2 is faithful to the supplied MATLAB source; the title inconsistency originates in that source.
* **Critical plotting defect**: `xlims = (0, xmax)` is applied only to the left subplot. In Plots.jl, the subplot created by `twinx()` retains its own X range unless it is set explicitly. The measured limits were:
  * Figure 2: left `(0, 250)`, right approximately `(-7.66, 263.00)`
  * Figures 3-5: left `(0, 300)`, right approximately `(-7.66, 263.00)`
* The AE time series actually ends at approximately 254.588 s. Because the right subplot autoscales independently, its final point is drawn at the right edge of the overlay. On Figures 3-5 this makes the red signal appear to end near 300 s and horizontally stretches all AE events relative to the blue stress curve.
* Figure 2 is affected by the same independent-axis issue, although the distortion is less visually obvious because its left limit ends at 250 s.
* Figure 4 also uses visibly larger points than the Python/MATLAB-style output because Plots.jl `markersize` and MATLAB/Matplotlib scatter-area arguments do not have identical semantics.
* **Conclusion**: The plotting architecture is clean, but the output is not an exact dual-axis reproduction. The right subplot must receive the same X limits as the left subplot, and the marker size should be calibrated separately.

## 5. Modularity and Performance - **Good**

* **Assessment**: The separation into `load_ct07`, `numeric_column`, `extract_signals`, `make_plots`, and `main` is clear and maintainable. The named tuple returned by `extract_signals`, constants, keyword arguments, and standard Julia entry-point guard are all appropriate.
* **Performance**: Vectorised column conversion and direct array plotting are suitable for this data volume. No performance benchmark was provided, so an "excellent performance" claim would be stronger than the available evidence.
* **Limitations**: The design assumes a single rectangular DataFrame and therefore does not model the two independent row domains present in the actual workbook. `finite_max` also assumes that at least one finite stress value exists.
* **Conclusion**: The code is well organised, but modularity does not compensate for the incorrect ingestion model.

---

## 6. Evaluation of the Generated Figures

**Important provenance note**: With the supplied workbook and the original `load_ct07` implementation, the Julia program fails before producing figures. The saved Julia images can only be evaluated as outputs generated after bypassing or replacing the documented loader with explicit physical-range extraction; they do not prove that the original `main()` works.

### Figure 1 - Strain vs Stress: **Correct after explicit extraction**

* The Julia and Python curves contain the same mechanical data and agree in shape, peak stress, fracture drop, labels, and Y range.
* Differences are limited to plotting-library styling.

### Figure 2 - Stress vs Normalised RMS: **Correct Y Data / Misaligned X Scale**

* The RMS amplitudes and event pattern agree with the Python result after correct extraction.
* The independently autoscaled right X axis shifts the red events horizontally relative to stress.
* The `T09` title is inherited faithfully from the original MATLAB script and should not be counted as a translation error.

### Figure 3 - Stress vs Normalised Cumulative RMS: **Correct Y Data / Misaligned X Scale**

* The red cumulative-RMS staircase is the correct signal, not an unrelated or incorrectly indexed column.
* Its step positions are stretched towards the right edge because the right subplot uses a different X range.

### Figure 4 - Stress vs Normalised AE Energy: **Correct Y Data / Misaligned X Scale and Marker Size**

* The energy events and their relative amplitudes agree with the Python result.
* Horizontal positions are distorted by the independent right-axis limits, and the Julia markers are substantially larger.

### Figure 5 - Stress vs Normalised Cumulative AE Energy: **Correct Y Data / Misaligned X Scale**

* The cumulative-energy staircase agrees with the Python data after explicit extraction.
* As in Figure 3, the curve is horizontally stretched; this is an axis-coordination problem rather than a wrong-column problem.

---

## 7. Overall Assessment

**GPT-5.5 (xhigh) MATLAB-to-Julia migration result: Partial Failure**

* **Index mapping**: Good. The MATLAB-to-Julia column numbers were transcribed correctly.
* **Data loading**: Poor and blocking. The selected table loader does not represent the supplied worksheet's physical layout, so the original program terminates before plotting.
* **Broadcasting and Julia style**: Good, but mixed text values are not safely coerced.
* **Visualisation structure**: Good, with reusable plotting functions and correct signal assignments.
* **Visual equivalence**: Partial. After the loading defect is bypassed, the Y data agree with Python, but Figures 2-5 have inconsistent left/right X scales and Figure 4 has a marker-size mismatch.
* **Methodological compliance**: Partial. The response demonstrates competent Julia syntax and organisation, but it does not validate the actual workbook structure or verify that the two axes share the same physical time scale. Both checks are essential in a scientific-computing migration.

The result should therefore not be described as a successful end-to-end translation. It is a strong structural draft with one blocking ingestion defect and one material plotting-equivalence defect.

## 8. Recommendations

1. Read the required physical worksheet range explicitly with `XLSX.readdata`, rather than asking `readtable` to infer a table from a non-rectangular layout.
2. Parse A:D from their mechanical-data start row and E:N from their AE-data start row; keep the two valid row counts independent.
3. Validate the workbook path, sheet name, physical column count, finite-value counts, and time ranges before plotting.
4. Apply `xlims = (0, xmax)` to the right subplot as well as the left subplot, then verify both subplot limits programmatically.
5. Calibrate the Figure 4 marker size against the MATLAB output instead of assuming identical size semantics across plotting libraries.
6. Add regression checks comparing the extracted arrays and key plot limits with a trusted MATLAB or Python baseline.
