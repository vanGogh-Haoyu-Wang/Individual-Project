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
# Debug

## 1. Execution issues and resolutions

### A. Python environment and dependencies

**Evidence**: The first environment check identified Homebrew Python 3.14.6 at `/opt/homebrew/opt/python@3.14/bin/python3.14`. Importing the translated script's dependencies failed at `numpy` with `ModuleNotFoundError`. The available system Python 3.9.6 also did not contain NumPy.

**Resolution**: A project-local `.venv` was created to avoid modifying the system Python installation. The first package installation attempt could not reach PyPI because network access was unavailable in the restricted execution environment. After network access was approved, the following requested versions were installed in `.venv`:

* `numpy==2.4.6`
* `pandas==3.0.3`
* `matplotlib==3.11.0`
* `openpyxl==3.1.5`

The installation also added required transitive dependencies, including `contourpy`, `cycler`, `fonttools`, `kiwisolver`, `packaging`, `Pillow`, `pyparsing`, `python-dateutil`, `six`, and `et-xmlfile`.

**Finding**: The initial import failure was caused by the selected Python environment, not by the translation's import statements. Subsequent runs used `.venv/bin/python` rather than the unconfigured Homebrew or system interpreter.

### B. Workbook and worksheet identifiers

**Evidence**: The translated script initially expected:

```python
DATA_FILE = Path("Tensile-processed.xlsx")
SHEET_NAME = "CT-07"
```

The supplied workbook was actually named `Commercial Tensile Tests.xlsx`. Workbook inspection reported the worksheet names `CT07` and `CT09`; there was no worksheet named `CT-07`.

**Resolution**: Only the two input constants were changed:

```python
DATA_FILE = Path("Commercial Tensile Tests.xlsx")
SHEET_NAME = "CT07"
```

**Finding**: These corrections adapt the translated script to the supplied data source. They do not alter the column mapping or plotting logic.

### C. Non-interactive and interactive plotting runs

**Evidence**: The first complete execution used `MPLBACKEND=Agg` so that Excel loading and all plotting calls could be tested without opening graphical windows. The process exited with code 0. Because `Agg` is non-interactive, `plt.show()` emitted the expected warning that the figures could not be shown.

Matplotlib also reported that the restricted environment could not create `/Users/vangogh/.matplotlib`, so it temporarily placed its cache under the system temporary directory.

**Resolution**: A writable project-local `.mplconfig` directory was used for Matplotlib's configuration and font cache. The script was then run with the macOS graphical backend, and `plt.show()` opened five interactive figure windows.

**Finding**: The non-interactive run verified execution; the interactive run provided the displayed figures. The backend and cache messages were environment-specific and did not require changes to the plotting functions.

### D. Execution verification and image-output boundary

**Evidence**: A separate verification run confirmed:

* All eight extracted arrays contained 5,851 entries.
* Five Matplotlib `Figure` objects were created.
* The axes counts were `[1, 2, 2, 2, 2]`, corresponding to one single-axis figure followed by four dual-axis figures.

**Finding**: The script successfully loaded the supplied CT07 worksheet and constructed the five intended plots. However, the script contains `plt.show()` and no `savefig()` call. It displays the figures but does not automatically write PNG files.

**Output boundary**: The five PNG files shown in the record were saved manually from the Matplotlib figure windows after the plotting run. Manual saving is not part of the script execution assessed here.

### E. Figure 2 title inconsistency

**Evidence**: The original MATLAB code hard-codes:

```matlab
title('T09 Commercial Normalised RMS Profile');
```

The data source used for the run was CT07. The Python translation retained the source title as:

```python
title="T09 Commercial Normalised RMS Profile"
```

**Finding**: The `T09` label is inconsistent with the CT07 dataset, but it was inherited directly from the supplied MATLAB code. It is therefore a source-script inconsistency rather than an indexing or plotting translation error. If the title is intended to identify the dataset, it should be changed to `T07 Commercial Normalised RMS Profile`.

---
# Results:
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
# Evidence-based evaluation of the Python translation

### A. Array indexing

**Evidence**: The required MATLAB-to-Python column mappings are:

* MATLAB `data(:, 1)` (`t1`) -> Python `data.iloc[:, 0]`
* MATLAB `data(:, 4)` (`stress`) -> Python `data.iloc[:, 3]`
* MATLAB `data(:, 3)` (`strain`) -> Python `data.iloc[:, 2]`
* MATLAB `data(:, 5)` (`time`) -> Python `data.iloc[:, 4]`
* MATLAB `data(:, 9)` (`rms`) -> Python `data.iloc[:, 8]`
* MATLAB `data(:, 10)` (`cumrms`) -> Python `data.iloc[:, 9]`
* MATLAB `data(:, 12)` (`energy`) -> Python `data.iloc[:, 11]`
* MATLAB `data(:, 14)` (`cumenergy`) -> Python `data.iloc[:, 13]`

**Finding**: Each specified MATLAB column index was reduced by one, which is the required conversion from MATLAB's 1-based indexing to pandas' zero-based positional indexing.

**Limitation**: The correctness of these mappings assumes that the worksheet retains the same physical column layout as the supplied workbook.

**Conclusion**: The column mappings are correct for the stated MATLAB inputs and the tested CT07 worksheet.

### B. pandas data loading

**Evidence**:

```python
raw_data = pd.read_excel(..., header=None, ...)
data = raw_data.apply(pd.to_numeric, errors="coerce").dropna(how="all")
```

For `Commercial Tensile Tests.xlsx`, both the raw DataFrame and the DataFrame after `dropna(how="all")` measured `5851 x 15`; zero rows were removed. The selected mechanical fields (`t1`, `stress`, and `strain`) each contained 1,807 finite values. The selected AE fields (`time`, `rms`, `cum_rms`, `energy`, and `cum_energy`) each contained 5,850 finite values.

The first worksheet row contains the numeric value `0.4242` in physical column 8. It is therefore not entirely `NaN` after numeric coercion and is not removed by `dropna(how="all")`.

**Finding**: `header=None` preserves the worksheet's physical column positions, while numeric coercion converts text and unavailable entries to `NaN` without shifting the data. This behaviour preserves the offset between the mechanical and AE regions in the supplied worksheet. Matplotlib omits non-finite plotting points.

**Limitation**: The code comment stating that text-only rows are subsequently removed is not demonstrated by this workbook because no complete row is removed. The approach also depends on the expected physical column layout and should not be treated as a general parser for arbitrary header or metadata structures. The code checks for at least 14 columns but does not validate expected finite-value counts or time ranges.

**Conclusion**: The loading method is suitable for the supplied workbook, but its robustness is dataset-specific.

### C. Matplotlib plotting interface and code structure

**Evidence**: The implementation creates axes with:

```python
figure, left_axis = plt.subplots()
right_axis = left_axis.twinx()
```

The repeated dual-axis logic is contained in `plot_dual_axis_profile`, and minor-grid configuration is contained in `enable_minor_grid`.

**Finding**: The code uses Matplotlib's object-oriented plotting interface because plotting operations are performed through explicit `Axes` objects. The overall program remains a procedural, function-based design rather than a class-based object-oriented architecture.

**Limitation**: The helper functions create figures but do not return their `Figure` or `Axes` objects, which limits direct programmatic saving or further composition by a caller.

**Conclusion**: The structure reduces repetition and implements the four dual-axis figures through a shared plotting function.

### D. Plotting fidelity and robustness

**Evidence**:

* Blue is used for stress and red for the AE quantities, matching the MATLAB colour specifications.
* The requested labels and axis limits are represented in the Python calls.
* Figure 2 uses `plot(time, rms, ...)`, matching the MATLAB command. Although the MATLAB comment calls it a scatter plot, the executable MATLAB statement is a line plot.
* Figure 4 maps MATLAB `scatter(time, energy, 5, 'filled', 'r')` to Matplotlib `scatter(..., s=5, color="red", edgecolors="none")`.
* `minorticks_on()` and `grid(which="both")` provide an approximation of MATLAB's minor-grid presentation.

**Finding**: The Python implementation reproduces the requested plot types, axis roles, colours, labels, and numerical limits for the tested data.

**Limitation**: Matplotlib and MATLAB use different rendering engines and default styles, so the grid appearance and other visual details are not guaranteed to be pixel-identical. The workbook path is relative to the current working directory. The script has no automatic image export, and the inherited Figure 2 title remains inconsistent with CT07.

**Conclusion**: Functional plotting equivalence is supported for this run; exact visual equivalence cannot be established without corresponding MATLAB reference images.

---
# Evaluation of the resulting images

All five manually saved PNG files are `640 x 480` pixels.

### Figure 1: Strain versus stress

**Evidence**: The image contains a blue strain-stress line, the labels `Strain (%)` and `Stress (MPa)`, the title `T07 Strain vs. Stress`, and a stress-axis range from 0 to 520 MPa. Major and minor grid lines are visible.

**Finding**: The observable labels, colour, plot type, title, and Y-axis limit correspond to the translated plotting instructions.

### Figure 2: Stress and normalised RMS versus time

**Evidence**: The image contains two Y-axes, a blue stress line on the left axis, and a red RMS line on the right axis. The displayed time range is 0 to 250 seconds, and the right-axis range extends to approximately 1.05. The title is `T09 Commercial Normalised RMS Profile`.

**Finding**: The dual-axis structure and line types correspond to the executable MATLAB and Python plotting commands. The title exposes the inherited T09/CT07 inconsistency described above.

### Figure 3: Stress and normalised cumulative RMS versus time

**Evidence**: The image contains a blue stress line and a red cumulative RMS line on separate Y-axes over a displayed time range of 0 to 300 seconds. The cumulative series rises in steps toward its normalised upper range.

**Finding**: The dual-axis structure, cumulative line representation, labels, colours, and limits correspond to the translated plotting instructions.

### Figure 4: Stress and normalised AE energy versus time

**Evidence**: The image contains a blue stress line and red AE-energy scatter markers on separate Y-axes. The displayed time range is 0 to 300 seconds, and the energy markers use the scatter representation requested by the MATLAB command.

**Finding**: This is the only AE panel that uses scatter markers; Figure 2 uses a line.

### Figure 5: Stress and normalised cumulative AE energy versus time

**Evidence**: The image contains a blue stress line and a red cumulative AE-energy line on separate Y-axes over a displayed time range of 0 to 300 seconds. The cumulative series increases in steps toward its normalised upper range.

**Finding**: The dual-axis structure, cumulative line representation, labels, colours, and limits correspond to the translated plotting instructions.

**Comparison limitation**: These observations establish consistency between the Python code and the saved Python figures. They do not establish pixel-level equivalence with MATLAB because no corresponding MATLAB-rendered reference images were supplied for direct comparison.

---
# Overall conclusion

The translation satisfies the requested MATLAB-to-Python index conversion, pandas-based Excel loading, modular Matplotlib plotting, and `twinx()` dual-axis construction for the supplied CT07 workbook after correcting the external file and worksheet identifiers. The execution produced five interactive figures, which were subsequently saved manually.

The result is verified for the tested workbook rather than for arbitrary AE spreadsheets. Its main remaining limitations are dependence on fixed physical column positions, limited input validation, a relative workbook path, no automatic image export, and the inherited T09 title in Figure 2.
