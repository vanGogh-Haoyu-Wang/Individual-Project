from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


COLUMN_INDEXES = {
    "t1": 0,
    "strain": 2,
    "stress": 3,
    "time": 4,
    "rms": 8,
    "cumrms": 9,
    "energy": 11,
    "cumenergy": 13,
}

OUTPUT_FILENAMES = [
    "01_strain_vs_stress.png",
    "02_normalised_rms_profile.png",
    "03_normalised_cumulative_rms.png",
    "04_normalised_ae_energy.png",
    "05_normalised_cumulative_ae_energy.png",
]


def load_numeric_columns(file_path: Path, sheet_name: str) -> dict[str, pd.Series]:
    """Load target columns and reproduce MATLAB's numeric/NaN behavior."""
    data = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    if data.shape[1] <= max(COLUMN_INDEXES.values()):
        raise ValueError(
            f"Sheet {sheet_name!r} has {data.shape[1]} columns; "
            f"at least {max(COLUMN_INDEXES.values()) + 1} are required."
        )
    return {
        name: pd.to_numeric(data.iloc[:, index], errors="coerce")
        for name, index in COLUMN_INDEXES.items()
    }


def paired_values(x: pd.Series, y: pd.Series) -> tuple[pd.Series, pd.Series]:
    valid = x.notna() & y.notna()
    return x.loc[valid], y.loc[valid]


def style_grid(axis: plt.Axes) -> None:
    axis.minorticks_on()
    axis.grid(True, which="minor", linestyle=":", alpha=0.6)
    axis.grid(True, which="major", linestyle="-", alpha=0.8)


def make_stress_axis(t1: pd.Series, stress: pd.Series, x_max: float):
    x_values, y_values = paired_values(t1, stress)
    figure, axis = plt.subplots(figsize=(10, 6))
    axis.plot(x_values, y_values, "b")
    axis.set_ylabel("Stress (MPa)", color="b")
    axis.tick_params(axis="y", labelcolor="b")
    axis.set_xlabel("Time (s)")
    axis.set_ylim([0, float(y_values.max())])
    axis.set_xlim([0, x_max])
    style_grid(axis)
    return figure, axis


def build_figures(columns: dict[str, pd.Series]):
    strain, stress_for_strain = paired_values(columns["strain"], columns["stress"])
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(strain, stress_for_strain, "b")
    ax1.set_ylabel("Stress (MPa)")
    ax1.set_xlabel("Strain (%)")
    ax1.set_ylim([0, 520])
    ax1.set_title("T07 Strain vs. Stress")
    style_grid(ax1)

    fig2, ax2_left = make_stress_axis(columns["t1"], columns["stress"], 250)
    time_rms, rms = paired_values(columns["time"], columns["rms"])
    ax2_right = ax2_left.twinx()
    ax2_right.plot(time_rms, rms, "r")
    ax2_right.set_ylabel("Normalised RMS (a.u.)", color="r")
    ax2_right.tick_params(axis="y", labelcolor="r")
    ax2_right.set_ylim([0, 1.05])
    ax2_left.set_title("T09 Commercial Normalised RMS Profile")

    fig3, ax3_left = make_stress_axis(columns["t1"], columns["stress"], 300)
    time_cumrms, cumrms = paired_values(columns["time"], columns["cumrms"])
    ax3_right = ax3_left.twinx()
    ax3_right.plot(time_cumrms, cumrms, "r")
    ax3_right.set_ylabel("Normalised Cumulative RMS (a.u.)", color="r")
    ax3_right.tick_params(axis="y", labelcolor="r")
    ax3_right.set_ylim([0, 1.05])
    ax3_left.set_title("T07 Commercial Normalised Cumulative RMS")

    fig4, ax4_left = make_stress_axis(columns["t1"], columns["stress"], 300)
    time_energy, energy = paired_values(columns["time"], columns["energy"])
    ax4_right = ax4_left.twinx()
    ax4_right.scatter(time_energy, energy, s=5, c="r")
    ax4_right.set_ylabel("Normalised AE Energy (a.u.)", color="r")
    ax4_right.tick_params(axis="y", labelcolor="r")
    ax4_right.set_ylim([0, 1.05])
    ax4_left.set_title("T07 Commercial Normalised AE Energy")

    fig5, ax5_left = make_stress_axis(columns["t1"], columns["stress"], 300)
    time_cumenergy, cumenergy = paired_values(
        columns["time"], columns["cumenergy"]
    )
    ax5_right = ax5_left.twinx()
    ax5_right.plot(time_cumenergy, cumenergy, "r")
    ax5_right.set_ylabel("Normalised Cumulative AE Energy (a.u.)", color="r")
    ax5_right.tick_params(axis="y", labelcolor="r")
    ax5_right.set_ylim([0, 1.05])
    ax5_left.set_title("T07 Commercial Normalised Cumulative AE Energy")

    figures = [fig1, fig2, fig3, fig4, fig5]
    for figure in figures:
        figure.tight_layout()
    return figures


def save_figures(figures, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_paths = []
    for figure, filename in zip(figures, OUTPUT_FILENAMES, strict=True):
        output_path = output_dir / filename
        figure.savefig(output_path, dpi=160, bbox_inches="tight")
        output_paths.append(output_path)
    return output_paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate five tensile-test and acoustic-emission plots."
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--sheet", default="CT07")
    parser.add_argument(
        "--output-dir", type=Path, default=Path(__file__).resolve().parent
    )
    parser.add_argument("--no-show", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    file_path = args.input.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()
    if not file_path.is_file():
        raise FileNotFoundError(f"Workbook not found: {file_path}")

    columns = load_numeric_columns(file_path, args.sheet)
    figures = build_figures(columns)
    output_paths = save_figures(figures, output_dir)

    print(f"Loaded workbook: {file_path}")
    print(f"Mechanical paired points: {paired_values(columns['t1'], columns['stress'])[0].size}")
    print(f"AE paired points: {paired_values(columns['time'], columns['rms'])[0].size}")
    for output_path in output_paths:
        print(f"Saved: {output_path}")

    if not args.no_show:
        plt.show()
    plt.close("all")


if __name__ == "__main__":
    main()
