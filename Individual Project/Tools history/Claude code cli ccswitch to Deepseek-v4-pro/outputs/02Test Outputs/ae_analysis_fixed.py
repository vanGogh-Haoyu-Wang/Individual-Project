"""Generate the five CT07 acoustic-emission plots from the supplied workbook."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


SHEET = "CT07"
OUTPUT_NAMES = (
    "01_CT07_strain_vs_stress.png",
    "02_CT07_normalised_RMS_profile.png",
    "03_CT07_normalised_cumulative_RMS.png",
    "04_CT07_normalised_AE_energy.png",
    "05_CT07_normalised_cumulative_AE_energy.png",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def load_data(input_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    # The workbook has three non-data rows: AE headings, tensile headings, units.
    raw = pd.read_excel(input_path, sheet_name=SHEET, header=None, skiprows=3)
    if raw.shape[1] < 14:
        raise ValueError(f"Expected at least 14 columns, found {raw.shape[1]}")

    selected = raw.iloc[:, [0, 2, 3, 4, 8, 9, 11, 13]].copy()
    selected.columns = [
        "test_time",
        "strain",
        "stress",
        "ae_time",
        "rms",
        "cumulative_rms",
        "energy",
        "cumulative_energy",
    ]
    selected = selected.apply(pd.to_numeric, errors="coerce")

    mechanical = selected[["test_time", "strain", "stress"]].dropna()
    acoustic = selected[
        ["ae_time", "rms", "cumulative_rms", "energy", "cumulative_energy"]
    ].dropna()
    if mechanical.empty or acoustic.empty:
        raise ValueError("No valid mechanical or acoustic-emission observations found")
    return mechanical, acoustic


def finish_figure(fig: plt.Figure, output_path: Path) -> None:
    fig.tight_layout()
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def generate_plots(mechanical: pd.DataFrame, acoustic: pd.DataFrame, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "axes.grid": True,
            "axes.grid.which": "both",
            "grid.alpha": 0.4,
            "figure.figsize": (9, 5.5),
        }
    )

    paths = [output_dir / name for name in OUTPUT_NAMES]

    fig1, ax1 = plt.subplots()
    ax1.plot(mechanical["strain"], mechanical["stress"], "b")
    ax1.set(xlabel="Strain (%)", ylabel="Stress (MPa)", ylim=(0, 520))
    ax1.set_title(f"{SHEET} Strain vs. Stress")
    ax1.minorticks_on()
    finish_figure(fig1, paths[0])

    fig2, ax2_left = plt.subplots()
    ax2_left.plot(mechanical["test_time"], mechanical["stress"], "b")
    ax2_left.set(xlabel="Time (s)", ylabel="Stress (MPa)", xlim=(0, 250))
    ax2_left.set_ylim(0, mechanical["stress"].max())
    ax2_right = ax2_left.twinx()
    ax2_right.plot(acoustic["ae_time"], acoustic["rms"], "r")
    ax2_right.set(ylabel="Normalised RMS (a.u.)", ylim=(0, 1.05))
    ax2_left.set_title(f"{SHEET} Commercial Normalised RMS Profile")
    ax2_left.minorticks_on()
    finish_figure(fig2, paths[1])

    fig3, ax3_left = plt.subplots()
    ax3_left.plot(mechanical["test_time"], mechanical["stress"], "b")
    ax3_left.set(xlabel="Time (s)", ylabel="Stress (MPa)", xlim=(0, 300))
    ax3_left.set_ylim(0, mechanical["stress"].max())
    ax3_right = ax3_left.twinx()
    ax3_right.plot(acoustic["ae_time"], acoustic["cumulative_rms"], "r")
    ax3_right.set(ylabel="Normalised Cumulative RMS (a.u.)", ylim=(0, 1.05))
    ax3_left.set_title(f"{SHEET} Commercial Normalised Cumulative RMS")
    ax3_left.minorticks_on()
    finish_figure(fig3, paths[2])

    fig4, ax4_left = plt.subplots()
    ax4_left.plot(mechanical["test_time"], mechanical["stress"], "b")
    ax4_left.set(xlabel="Time (s)", ylabel="Stress (MPa)", xlim=(0, 300))
    ax4_left.set_ylim(0, mechanical["stress"].max())
    ax4_right = ax4_left.twinx()
    ax4_right.scatter(
        acoustic["ae_time"], acoustic["energy"], s=5, c="r", edgecolors="none"
    )
    ax4_right.set(ylabel="Normalised AE Energy (a.u.)", ylim=(0, 1.05))
    ax4_left.set_title(f"{SHEET} Commercial Normalised AE Energy")
    ax4_left.minorticks_on()
    finish_figure(fig4, paths[3])

    fig5, ax5_left = plt.subplots()
    ax5_left.plot(mechanical["test_time"], mechanical["stress"], "b")
    ax5_left.set(xlabel="Time (s)", ylabel="Stress (MPa)", xlim=(0, 300))
    ax5_left.set_ylim(0, mechanical["stress"].max())
    ax5_right = ax5_left.twinx()
    ax5_right.plot(acoustic["ae_time"], acoustic["cumulative_energy"], "r")
    ax5_right.set(
        ylabel="Normalised Cumulative AE Energy (a.u.)", ylim=(0, 1.05)
    )
    ax5_left.set_title(f"{SHEET} Commercial Normalised Cumulative AE Energy")
    ax5_left.minorticks_on()
    finish_figure(fig5, paths[4])

    return paths


def main() -> None:
    args = parse_args()
    mechanical, acoustic = load_data(args.input)
    paths = generate_plots(mechanical, acoustic, args.output_dir)
    print(f"Input: {args.input.resolve()}")
    print(f"Sheet: {SHEET}")
    print(f"Mechanical rows: {len(mechanical)}")
    print(f"AE rows: {len(acoustic)}")
    for path in paths:
        print(f"Saved: {path.resolve()} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
