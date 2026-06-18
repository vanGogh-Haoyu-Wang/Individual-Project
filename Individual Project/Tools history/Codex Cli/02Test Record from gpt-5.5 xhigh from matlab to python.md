# Prompt:

Act as a Senior Scientific Computing Engineer. I am working on an MSc project migrating an Acoustic Emission (AE) analysis framework from MATLAB to an open-source Python environment. 

Your task is to translate the following MATLAB script into Python. 

Requirements & Constraints:

1. Data Loading: Replace MATLAB's `xlsread` with an appropriate Python library (e.g., `pandas`).
2. Array Indexing: Pay strict attention to the 1-based to 0-based indexing conversion between MATLAB and Python. Ensure data slicing is correct.
3. Visualization: Use `matplotlib` (and/or `seaborn`) to replicate the exact plots. Handle MATLAB's `yyaxis left` and `yyaxis right` elegantly using Python's object-oriented plotting approach (e.g., `twinx()`).
4. Readability: Keep the code clean, modular, and PEP-8 compliant. Add brief comments explaining the Python-specific implementation choices.

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
scatter(time, energy, 5, 'filled', 'r')
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
---
# Answer：

```python
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


DATA_FILE = Path("Tensile-processed.xlsx")
SHEET_NAME = "CT-07"


def load_ae_data(file_path: Path, sheet_name: str) -> dict[str, np.ndarray]:
    """Load and extract the required AE columns from an Excel worksheet."""
    # header=None prevents pandas from assuming that the first row is a header.
    raw_data = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        header=None,
        engine="openpyxl",
    )

    # MATLAB xlsread returns numeric content. Text-only rows, such as column
    # headings, become NaN here and are then removed.
    data = raw_data.apply(pd.to_numeric, errors="coerce").dropna(how="all")

    if data.shape[1] < 14:
        raise ValueError(
            f"Expected at least 14 columns in {sheet_name!r}, "
            f"but found {data.shape[1]}."
        )

    # MATLAB column n becomes Python positional column n - 1.
    return {
        "t1": data.iloc[:, 0].to_numpy(),
        "stress": data.iloc[:, 3].to_numpy(),
        "strain": data.iloc[:, 2].to_numpy(),
        "time": data.iloc[:, 4].to_numpy(),
        "rms": data.iloc[:, 8].to_numpy(),
        "cum_rms": data.iloc[:, 9].to_numpy(),
        "energy": data.iloc[:, 11].to_numpy(),
        "cum_energy": data.iloc[:, 13].to_numpy(),
    }


def enable_minor_grid(axis: plt.Axes) -> None:
    """Approximate MATLAB's grid('minor') behaviour."""
    axis.minorticks_on()
    axis.grid(True, which="both", linestyle=":", linewidth=0.6, alpha=0.7)


def plot_strain_stress(
    strain: np.ndarray,
    stress: np.ndarray,
) -> None:
    """Create the strain-versus-stress plot."""
    figure, axis = plt.subplots()

    axis.plot(strain, stress, color="blue")
    axis.set_xlabel("Strain (%)")
    axis.set_ylabel("Stress (MPa)")
    axis.set_ylim(0, 520)
    axis.set_title("T07 Strain vs. Stress")
    enable_minor_grid(axis)

    figure.tight_layout()


def plot_dual_axis_profile(
    t1: np.ndarray,
    stress: np.ndarray,
    time: np.ndarray,
    ae_values: np.ndarray,
    *,
    title: str,
    right_label: str,
    x_max: float,
    scatter: bool = False,
) -> None:
    """Plot stress and an AE quantity on shared-x twin y-axes."""
    figure, left_axis = plt.subplots()
    right_axis = left_axis.twinx()

    left_axis.plot(t1, stress, color="blue")
    left_axis.set_xlabel("Time (s)")
    left_axis.set_ylabel("Stress (MPa)")
    left_axis.set_xlim(0, x_max)
    left_axis.set_ylim(0, np.nanmax(stress))

    if scatter:
        # Matplotlib's s argument controls marker area, equivalent to
        # MATLAB's scatter marker-size argument.
        right_axis.scatter(
            time,
            ae_values,
            s=5,
            color="red",
            edgecolors="none",
        )
    else:
        right_axis.plot(time, ae_values, color="red")

    right_axis.set_ylabel(right_label)
    right_axis.set_ylim(0, 1.05)

    left_axis.set_title(title)
    enable_minor_grid(left_axis)
    right_axis.minorticks_on()

    figure.tight_layout()


def main() -> None:
    ae_data = load_ae_data(DATA_FILE, SHEET_NAME)

    plot_strain_stress(
        ae_data["strain"],
        ae_data["stress"],
    )

    plot_dual_axis_profile(
        ae_data["t1"],
        ae_data["stress"],
        ae_data["time"],
        ae_data["rms"],
        title="T09 Commercial Normalised RMS Profile",
        right_label="Normalised RMS (a.u.)",
        x_max=250,
    )

    plot_dual_axis_profile(
        ae_data["t1"],
        ae_data["stress"],
        ae_data["time"],
        ae_data["cum_rms"],
        title="T07 Commercial Normalised Cumulative RMS",
        right_label="Normalised Cumulative RMS (a.u.)",
        x_max=300,
    )

    plot_dual_axis_profile(
        ae_data["t1"],
        ae_data["stress"],
        ae_data["time"],
        ae_data["energy"],
        title="T07 Commercial Normalised AE Energy",
        right_label="Normalised AE Energy (a.u.)",
        x_max=300,
        scatter=True,
    )

    plot_dual_axis_profile(
        ae_data["t1"],
        ae_data["stress"],
        ae_data["time"],
        ae_data["cum_energy"],
        title="T07 Commercial Normalised Cumulative AE Energy",
        right_label="Normalised Cumulative AE Energy (a.u.)",
        x_max=300,
    )

    plt.show()


if __name__ == "__main__":
    main()
```

Install the dependencies with:

```bash
pip install pandas matplotlib numpy openpyxl
```

The original figure-2 title says `T09` despite loading sheet `CT-07`; this translation preserves it exactly. Change it to `T07` if that was a MATLAB typo.

---
# Find problem: 
```
DATA_FILE = Path("Tensile-processed.xlsx")
SHEET_NAME = "CT-07"
```
should be changed to
```
DATA_FILE = Path("Commercial Tensile Tests.xlsx")
SHEET_NAME = "CT07"
```

---
# Run and results:
Figure 1:
![[Figure_1.png]]
Figure 2:
![[Figure_2.png]]
Figure 3:
![[Figure_3.png]]
Figure 4:
![[Figure_4.png]]
Figure 5:![[Figure_5.png]]


---
# Find mistake

Because in the original MATLAB code, the title of Figure 2 was hard-coded as:

```
title('T09 Commercial Normalised RMS Profile');
```

But it reads CT-07/CT07 data, so this should be a typo in the original script. The Python version retains it for faithful translation. The correct title should be changed to:

```
title="T07 Commercial Normalised RMS Profile"
```
*So this isn't an LLM problem, it's the original script's problem.*

---
## 1. An objective evaluation of `01Test Record from gpt-5.5 max`
### A. Indexing - **Excellent**
**Evaluation**: GPT-5.5 Max perfectly handled the conversion from 1-based to 0-based indexing. 
**Evidence**: 
* MATLAB `data(:, 1)` (t1) -> Python `data.iloc[:, 0]`
* MATLAB `data(:, 3)` (strain) -> Python `data.iloc[:, 2]`
* MATLAB `data(:, 4)` (stress) -> Python `data.iloc[:, 3]`
* MATLAB `data(:, 9)` (rms) -> Python `data.iloc[:, 8]`
* ... and so on, all column indices are correctly decreased by 1.
**Conclusion**: Meets the strict standard of "checking if the index changes," with no points deducted.
#### B. Pandas Usage (Data Loading) - **Good / Effective for This Workbook**
* **Evaluation**: Using `header=None` is an appropriate choice for this worksheet because it preserves the physical Excel column positions required by the MATLAB script. Applying `pd.to_numeric(..., errors="coerce")` then converts text in the selected signal columns to `NaN` without shifting those columns.
* **Evidence**:
```python  
raw_data = pd.read_excel(..., header=None, ...)  
data = raw_data.apply(pd.to_numeric, errors="coerce").dropna(how="all")  
```
* **Observed behaviour with `Commercial Tensile Tests.xlsx`**:
  * The raw worksheet and the post-`dropna` DataFrame are both `5851 x 15`; `dropna(how="all")` removes zero rows.
  * The first row contains one numeric value (`0.4242`), while the second and third rows contain AE values in the right-hand columns. These rows are therefore not entirely `NaN` after coercion and are retained.
  * The mechanical columns contain 1,807 finite records, whereas the AE time column contains 5,850. The leading text or unavailable cells in each selected plotting pair become `NaN`, and Matplotlib ignores those non-finite points while preserving the physical row and column alignment.
* **Strength**: For this workbook, the approach produces the intended arrays and closely approximates MATLAB `xlsread` behaviour without losing the offset between the mechanical and AE regions.
* **Limitation**: The code does not actually remove every header or metadata row, and its correctness depends on the relevant text cells coercing to `NaN` and the selected columns remaining in their expected physical positions. It should not be described as universally robust for arbitrary Excel header structures.
* **Conclusion**: The loading strategy is effective for the supplied workbook and avoids type errors in the selected columns, but it would benefit from explicit validation of column count, finite-value counts, and time ranges.
  
#### C. Plotting Object Management (Plotting API) - **Excellent** 
**Evaluation**: The code fully adheres to the Object-Oriented Programming (OOP) style and elegantly reuses the dual-axis plotting logic. 
**Evidence**: 
* Used the `fig, axis = plt.subplots()` and `ax1, ax2 = plt.subplots()` patterns. 
* Correctly used `ax2 = ax1.twinx()` to create a secondary Y-axis sharing the same X-axis. 
**Highlight**: Encapsulated the repetitive `yyaxis` logic into the `plot_dual_axis_profile` function, demonstrating a "Senior Engineer's" modular thinking, making it more maintainable than MATLAB scripts. 
**Conclusion**: Proficient in the plotting API, with correct dual-axis binding. 
#### D. Details & Robustness - **Good/Excellent**  
* **Evaluation**:  
  * **Grid lines**: MATLAB's `grid('minor')` in Matplotlib requires manually enabling `minorticks_on()` and setting `grid(which='both')`. The code implements the `enable_minor_grid` function to restore the visual effect.  
  * **Scatter plot**: The `5` in MATLAB's `scatter(..., 5, ...)` represents marker size. The code correctly maps it to `s=5`.  
  * **Hard-coded correction**: The code retains potential typos (e.g., Fig 2 title as T09) from the MATLAB script and reminds users in comments. This is an honest and professional approach.  
  * **File path**: The user later corrected the file name and sheet name, and the code structure supports such parameterized modifications.
  * **Data-loading robustness**: The conversion succeeds for the supplied workbook because `NaN` values preserve the worksheet's physical alignment and Matplotlib tolerates them. The implementation does not validate the expected finite record counts or detect an unexpected worksheet layout, so its robustness is dataset-specific rather than universal.
## 2. Evaluation of the Resulting Images Based on the Provided Image Links: 

**Figure 1 (Strain vs Stress)**: 
* The curve is smooth, the axis labels are correct, and the Y-axis limit [0, 520] is effective. 
* The grid lines are displayed normally. 
**Figure 2 (Stress vs RMS)**: 
* The dual Y-axes are correctly displayed. The left axis is the blue stress curve, and the right axis is the red RMS scatter plot/curve. 
* The X-axis limit [0, 250] is effective. 
* The title "T09 Commercial..." matches the original MATLAB code (although it might be a typo, but it remains faithful to the input). 
**Figure 3, 4, 5**: 
* All correctly show the dual Y-axis structure. 
* Figure 4 correctly uses a scatter plot (`scatter`) instead of a line plot, aligning with the MATLAB `scatter` command. 
* The X-axis range (250s or 300s) is correctly applied to all figures. 

## 3. Summary **GPT-5.5 Max's performance: Very Good**

* **Index conversion**: 100% correct. 
* **Data loading**: Effective for the supplied workbook and faithful to its physical column positions, but dependent on this worksheet's structure and not universally robust to arbitrary headers or metadata rows.
* **Visualization**: Correctly reproduces the MATLAB plotting logic for the tested data, with a clearer and more reusable modular structure.
* **Compliance with methodology**: Largely complies with the "Senior Scientific Computing Engineer" persona set in [[01Prompt_Methodology_Overview]], achieving functional equivalence for the supplied dataset while leaving room for stronger input validation.
