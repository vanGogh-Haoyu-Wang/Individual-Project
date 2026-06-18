# User

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
# Assistant

Great migration target. Here is a clean, modular Python equivalent that preserves MATLAB behavior and indexing.

```python
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_ae_data(file_path: str, sheet_name: str = "CT-07") -> dict[str, np.ndarray]:
    """
    Load numeric AE data from Excel.

    MATLAB -> Python column mapping (1-based -> 0-based):
    1->0 (t1), 4->3 (stress), 3->2 (strain), 5->4 (time),
    9->8 (rms), 10->9 (cumrms), 12->11 (energy), 14->13 (cumenergy)
    """
    # header=None mimics xlsread-style raw numeric matrix access
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

    # Force numeric (non-numeric cells become NaN, similar to MATLAB numeric matrix behavior)
    df = df.apply(pd.to_numeric, errors="coerce")

    data = {
        "t1": df.iloc[:, 0].to_numpy(),
        "stress": df.iloc[:, 3].to_numpy(),
        "strain": df.iloc[:, 2].to_numpy(),
        "time": df.iloc[:, 4].to_numpy(),
        "rms": df.iloc[:, 8].to_numpy(),
        "cumrms": df.iloc[:, 9].to_numpy(),
        "energy": df.iloc[:, 11].to_numpy(),
        "cumenergy": df.iloc[:, 13].to_numpy(),
    }
    return data


def add_minor_grid(ax: plt.Axes) -> None:
    """Replicate MATLAB `grid('minor')` behavior."""
    ax.minorticks_on()
    ax.grid(True, which="minor", linestyle=":", alpha=0.7)


def plot_dual_axis(
    x_left: np.ndarray,
    y_left: np.ndarray,
    x_right: np.ndarray,
    y_right: np.ndarray,
    right_label: str,
    title: str,
    xlim: tuple[float, float],
    right_as_scatter: bool = False,
) -> None:
    """Create MATLAB `yyaxis left/right` style plot using twinx()."""
    fig, ax_left = plt.subplots()

    # Left axis: stress vs time
    ax_left.plot(x_left, y_left, color="b")
    ax_left.set_xlabel("Time (s)")
    ax_left.set_ylabel("Stress (MPa)")
    ax_left.set_ylim(0, np.nanmax(y_left))
    ax_left.set_xlim(*xlim)

    # Right axis
    ax_right = ax_left.twinx()
    if right_as_scatter:
        ax_right.scatter(x_right, y_right, s=5, c="r")
    else:
        ax_right.plot(x_right, y_right, color="r")
    ax_right.set_ylabel(right_label)
    ax_right.set_ylim(0, 1.05)

    ax_left.set_title(title)
    add_minor_grid(ax_left)

    fig.tight_layout()


def main() -> None:
    file_path = Path("Tensile-processed.xlsx")
    d = load_ae_data(str(file_path), sheet_name="CT-07")

    # Fig 1: Strain vs Stress
    fig1, ax1 = plt.subplots()
    ax1.plot(d["strain"], d["stress"], color="b")
    ax1.set_xlabel("Strain (%)")
    ax1.set_ylabel("Stress (MPa)")
    ax1.set_ylim(0, 520)
    ax1.set_title("T07 Strain vs. Stress")
    add_minor_grid(ax1)
    fig1.tight_layout()

    # Fig 2
    plot_dual_axis(
        x_left=d["t1"],
        y_left=d["stress"],
        x_right=d["time"],
        y_right=d["rms"],
        right_label="Normalised RMS (a.u.)",
        title="T09 Commercial Normalised RMS Profile",
        xlim=(0, 250),
    )

    # Fig 3
    plot_dual_axis(
        x_left=d["t1"],
        y_left=d["stress"],
        x_right=d["time"],
        y_right=d["cumrms"],
        right_label="Normalised Cumulative RMS (a.u.)",
        title="T07 Commercial Normalised Cumulative RMS",
        xlim=(0, 300),
    )

    # Fig 4 (scatter on right axis)
    plot_dual_axis(
        x_left=d["t1"],
        y_left=d["stress"],
        x_right=d["time"],
        y_right=d["energy"],
        right_label="Normalised AE Energy (a.u.)",
        title="T07 Commercial Normalised AE Energy",
        xlim=(0, 300),
        right_as_scatter=True,
    )

    # Fig 5
    plot_dual_axis(
        x_left=d["t1"],
        y_left=d["stress"],
        x_right=d["time"],
        y_right=d["cumenergy"],
        right_label="Normalised Cumulative AE Energy (a.u.)",
        title="T07 Commercial Normalised Cumulative AE Energy",
        xlim=(0, 300),
    )

    plt.show()


if __name__ == "__main__":
    main()
```

Install deps if needed:

```bash
pip install pandas matplotlib openpyxl
```

If your Excel sheet has a header row, switch `header=None` to `header=0` and adjust column access accordingly.
