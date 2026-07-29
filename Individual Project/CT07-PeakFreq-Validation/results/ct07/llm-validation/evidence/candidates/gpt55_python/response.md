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
