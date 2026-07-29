#!/usr/bin/env python3
"""Build the formal T01--T09 Legacy/Adaptive framing comparison."""

from __future__ import annotations

import argparse
import json
import tomllib
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.io import loadmat


PACKAGE = Path(__file__).resolve().parents[3]
GROUPS = [f"T{index:02d}" for index in range(1, 10)]
OUTPUT_COLUMNS = [
    "group",
    "files",
    "legacy_logical_frames",
    "adaptive_complete_windows",
    "legacy_selected_windows",
    "legacy_top1_rows",
    "adaptive_selected_events",
    "adaptive_top1_rows",
    "adaptive_top3_rows",
    "legacy_selection_rate",
    "adaptive_selection_rate",
    "selected_count_ratio",
    "legacy_matched_by_adaptive",
    "legacy_missing_from_adaptive",
]


def selection_metrics(
    legacy_selected: int,
    legacy_frames: int,
    adaptive_selected: int,
    adaptive_windows: int,
) -> dict[str, float]:
    if min(legacy_selected, legacy_frames, adaptive_selected, adaptive_windows) < 0:
        raise ValueError("framing counts cannot be negative")
    if not legacy_frames or not adaptive_windows or not legacy_selected:
        raise ValueError("framing denominators and Legacy selected count must be non-zero")
    return {
        "legacy_selection_rate": legacy_selected / legacy_frames,
        "adaptive_selection_rate": adaptive_selected / adaptive_windows,
        "selected_count_ratio": adaptive_selected / legacy_selected,
    }


def load_config(path: Path) -> dict:
    config = tomllib.loads(path.read_text())
    package = path.resolve().parent

    def resolve(value: str) -> Path:
        candidate = Path(value).expanduser()
        return candidate if candidate.is_absolute() else (package / candidate).resolve()

    return {
        "legacy_root": resolve(config["paths"]["legacy_group_results"]),
        "adaptive_root": resolve(config["paths"]["adaptive_results"]),
        "output": package
        / "results/peak-frequency/legacy-adaptive-framing",
        "windows_per_legacy_file": int(config["analysis"]["legacy_windows_per_file"]),
        "hop_samples": int(config["analysis"]["hop_samples"]),
    }


def build_rows(config: dict) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for group in GROUPS:
        legacy_dir = config["legacy_root"] / group
        adaptive_dir = config["adaptive_root"] / group.lower() / "matlab"
        legacy_meta = json.loads((legacy_dir / "legacy_run_metadata.json").read_text())
        legacy_files = [Path(path).name for path in legacy_meta["input_files"]]
        legacy_top1 = pd.read_csv(legacy_dir / "legacy_top1_events.csv")
        selected = np.atleast_1d(
            loadmat(
                legacy_dir / "legacy_peak_freq_export.mat",
                variable_names=["event_index"],
                squeeze_me=True,
            )["event_index"]
        ).astype(np.int64)

        thresholds = pd.read_csv(adaptive_dir / "thresholds.csv")
        adaptive_selected = pd.read_csv(adaptive_dir / "selected_events.csv")
        adaptive_top1 = pd.read_csv(adaptive_dir / "baseline_events.csv")
        adaptive_top3 = pd.read_csv(adaptive_dir / "top3_events.csv")
        adaptive_files = thresholds["file_name"].tolist()
        if legacy_files != adaptive_files:
            raise ValueError(f"{group}: Legacy and Adaptive file order differs")

        windows_per_file = config["windows_per_legacy_file"]
        legacy_frames = len(legacy_files) * windows_per_file
        adaptive_windows = int(thresholds["candidate_window_count"].sum())
        if int(thresholds["selected_event_count"].sum()) != len(adaptive_selected):
            raise ValueError(f"{group}: Adaptive threshold and event counts differ")

        legacy_keys = {
            (
                legacy_files[(index - 1) // windows_per_file],
                ((index - 1) % windows_per_file) * config["hop_samples"],
            )
            for index in selected
        }
        adaptive_keys = set(
            zip(
                adaptive_selected["file_name"],
                adaptive_selected["start_sample"].astype(int),
            )
        )
        metrics = selection_metrics(
            len(selected), legacy_frames, len(adaptive_selected), adaptive_windows
        )
        rows.append(
            {
                "group": group,
                "files": len(legacy_files),
                "legacy_logical_frames": legacy_frames,
                "adaptive_complete_windows": adaptive_windows,
                "legacy_selected_windows": len(selected),
                "legacy_top1_rows": len(legacy_top1),
                "adaptive_selected_events": len(adaptive_selected),
                "adaptive_top1_rows": len(adaptive_top1),
                "adaptive_top3_rows": len(adaptive_top3),
                **metrics,
                "legacy_matched_by_adaptive": len(legacy_keys & adaptive_keys),
                "legacy_missing_from_adaptive": len(legacy_keys - adaptive_keys),
            }
        )

    table = pd.DataFrame(rows, columns=OUTPUT_COLUMNS)
    totals = {
        column: int(table[column].sum())
        for column in OUTPUT_COLUMNS
        if column
        not in {
            "group",
            "legacy_selection_rate",
            "adaptive_selection_rate",
            "selected_count_ratio",
        }
    }
    totals["group"] = "TOTAL"
    totals.update(
        selection_metrics(
            totals["legacy_selected_windows"],
            totals["legacy_logical_frames"],
            totals["adaptive_selected_events"],
            totals["adaptive_complete_windows"],
        )
    )
    return pd.concat([table, pd.DataFrame([totals])], ignore_index=True)[OUTPUT_COLUMNS]


def write_outputs(table: pd.DataFrame, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    table.to_csv(output / "t01_t09_comparison_summary.csv", index=False)
    total = table.loc[table["group"] == "TOTAL"].iloc[0]
    shortfall = int(total["adaptive_selected_events"] * 3 - total["adaptive_top3_rows"])
    lines = [
        "# T01–T09 Legacy and Adaptive Framing Comparison",
        "",
        "This table separates the framing domains. Legacy T01–T09 is MATLAB-only",
        "descriptive context; Adaptive/Top-3 T01–T09 is the three-language result.",
        "",
        "| Workflow | Files | Framing count | Selected | Rate | Output rows |",
        "|---|---:|---:|---:|---:|---:|",
        (
            f"| Legacy MATLAB context | {int(total['files']):,} | "
            f"{int(total['legacy_logical_frames']):,} logical frames | "
            f"{int(total['legacy_selected_windows']):,} | "
            f"{100 * total['legacy_selection_rate']:.3f}% | "
            f"{int(total['legacy_top1_rows']):,} valid Top-1 |"
        ),
        (
            f"| Adaptive/Top-3 | {int(total['files']):,} | "
            f"{int(total['adaptive_complete_windows']):,} complete windows | "
            f"{int(total['adaptive_selected_events']):,} | "
            f"{100 * total['adaptive_selection_rate']:.3f}% | "
            f"{int(total['adaptive_top3_rows']):,} Top-3 |"
        ),
        "",
        (
            f"Adaptive selected {total['selected_count_ratio']:.2f}× as many windows "
            "as Legacy. This is a selected-count ratio, not a same-denominator rate ratio."
        ),
        (
            f"The Top-3 table is {shortfall} rows below three rows per selected event: "
            "two events have one valid peak and ten have two."
        ),
        "",
        "The additional Adaptive selections are not confirmed physical AE damage events.",
    ]
    (output / "T01-T09 Legacy vs Adaptive Comparison.md").write_text(
        "\n".join(lines) + "\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    config = load_config(args.config)
    table = build_rows(config)
    write_outputs(table, config["output"])
    print(table.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
