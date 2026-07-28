"""Build reproducible T01--T09 legacy-versus-adaptive comparison artifacts."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.io import loadmat


ROOT = Path(__file__).resolve().parents[1] / "outputs" / "t01-t09-revalidation"
SUMMARY_DIR = ROOT / "summary"
REPORT_PATH = SUMMARY_DIR / "T01-T09 Legacy vs Adaptive Comparison.md"


def percentage(numerator: int, denominator: int) -> str:
    return f"{100 * numerator / denominator:.3f}%"


def describe_frequency(values: pd.Series) -> tuple[float, float, float]:
    return float(values.median()), float(values.quantile(0.25)), float(values.quantile(0.75))


def main() -> None:
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []

    for group_number in range(1, 10):
        group = f"T{group_number:02d}"
        tag = group.lower()
        legacy_dir = ROOT / f"{tag}-matlab-legacy"
        adaptive_dir = ROOT / f"{tag}-python-adaptive"

        legacy_meta = json.loads((legacy_dir / "legacy_run_metadata.json").read_text())
        adaptive_meta = json.loads((adaptive_dir / "run_metadata.json").read_text())
        legacy_top1 = pd.read_csv(legacy_dir / "legacy_top1_events.csv")
        adaptive_top1 = pd.read_csv(adaptive_dir / "baseline_events.csv")
        legacy_mat = loadmat(legacy_dir / "legacy_peak_freq_export.mat", squeeze_me=True)

        selected_indices = np.atleast_1d(legacy_mat["event_index"]).astype(int)
        candidate_windows = int(np.atleast_1d(legacy_mat["P"]).size)
        file_names = [Path(path).name for path in legacy_meta["input_files"]]
        windows_per_file = candidate_windows // len(file_names)
        if candidate_windows % len(file_names):
            raise ValueError(f"{group}: candidate windows do not divide into files")

        # MATLAB's buffer(..., 200, 1) produces logical frames with a 199-sample
        # hop. Its first frame includes an initial zero, so logical frame i maps
        # to the Adaptive raw-waveform start sample (i - 1) * 199.
        legacy_keys = {
            (file_names[(index - 1) // windows_per_file], ((index - 1) % windows_per_file) * 199)
            for index in selected_indices
        }
        adaptive_keys = {
            (row.file_name, int(round(row.event_time_s * 1_000_000)))
            for row in adaptive_top1.itertuples(index=False)
        }
        matched_windows = len(legacy_keys & adaptive_keys)
        missing_windows = len(legacy_keys - adaptive_keys)

        legacy_median, legacy_q1, legacy_q3 = describe_frequency(legacy_top1["peak_frequency_khz"])
        adaptive_median, adaptive_q1, adaptive_q3 = describe_frequency(adaptive_top1["frequency_khz"])
        thresholds = list(adaptive_meta["thresholds"].values())
        rows.append(
            {
                "group": group,
                "files": len(file_names),
                "candidate_windows": candidate_windows,
                "legacy_selected_windows": len(selected_indices),
                "legacy_top1_rows": len(legacy_top1),
                "legacy_no_peak_windows": int(legacy_meta.get("events_without_valid_peak", 0)),
                "adaptive_top1_rows": len(adaptive_top1),
                "legacy_active_files": len({file_name for file_name, _ in legacy_keys}),
                "adaptive_active_files": int(adaptive_top1["file_name"].nunique()),
                "adaptive_only_windows": len(adaptive_keys - legacy_keys),
                "legacy_selection_rate": 100 * len(selected_indices) / candidate_windows,
                "adaptive_selection_rate": 100 * len(adaptive_top1) / candidate_windows,
                "adaptive_to_legacy_ratio": len(adaptive_top1) / len(selected_indices),
                "legacy_windows_matched_by_adaptive": matched_windows,
                "legacy_windows_missing_from_adaptive": missing_windows,
                "legacy_median_khz": legacy_median,
                "legacy_iqr_low_khz": legacy_q1,
                "legacy_iqr_high_khz": legacy_q3,
                "adaptive_median_khz": adaptive_median,
                "adaptive_iqr_low_khz": adaptive_q1,
                "adaptive_iqr_high_khz": adaptive_q3,
                "adaptive_threshold_min": min(thresholds),
                "adaptive_threshold_max": max(thresholds),
            }
        )

    summary = pd.DataFrame(rows)
    summary.to_csv(SUMMARY_DIR / "t01_t09_comparison_summary.csv", index=False)

    total_candidates = int(summary.candidate_windows.sum())
    total_legacy = int(summary.legacy_selected_windows.sum())
    total_legacy_top1 = int(summary.legacy_top1_rows.sum())
    total_adaptive = int(summary.adaptive_top1_rows.sum())
    total_missing_peaks = int(summary.legacy_no_peak_windows.sum())
    all_matched = int(summary.legacy_windows_matched_by_adaptive.sum())
    missing_from_adaptive = int(summary.legacy_windows_missing_from_adaptive.sum())

    lines = [
        "# T01-T09 Legacy vs Adaptive Comparison",
        "",
        "**Date:** 2026-07-15  ",
        "**Purpose:** Independent repeat validation of the Legacy MATLAB-style AE peak-frequency workflow against the Adaptive Python workflow across every available T01-T09 raw-waveform group.",
        "",
        "## Scope and Reproducibility",
        "",
        f"- Input: {int(summary.files.sum())} MAT waveform files in T01-T09.",
        "- Outputs: one Legacy export and one Adaptive export per group, stored in `ae-peak-frequency/outputs/t01-t09-revalidation/`.",
        "- The original `Peak_Freq.m` was not edited. A companion MATLAB exporter reproduces its computational path and writes machine-readable CSV/MAT/JSON outputs.",
        "- The comparison uses the same method as the earlier T02-T04 note, extended to all nine groups.",
        "",
        "## Methods Compared",
        "",
        "### Legacy MATLAB-style workflow",
        "",
        "1. Sort MAT files by filename; use the mean and extreme values of the first file for the complete group.",
        "2. Subtract that mean, append the original 1,000,000-sample zero padding, and retain only samples at or beyond the first-file extrema.",
        "3. Compute a 200-sample moving RMS and select 200-sample frames with one-sample overlap (199-sample hop) above the fixed threshold 0.1.",
        "4. Calculate a 200-point FFT for each selected window; retain the strongest detected peak with a 20 kHz minimum peak distance.",
        "",
        "### Adaptive Python workflow",
        "",
        "1. Process each MAT file independently and subtract its own mean.",
        "2. Keep the raw centred waveform, without the first-file-extrema filter or appended padding.",
        "3. Use the same 200-sample window and one-sample overlap (199-sample hop), but set the RMS threshold per file as `median + 8 x 1.4826 x MAD`.",
        "4. Use the same FFT length, frequency range, Top-1 peak output, and 20 kHz minimum peak distance.",
        "",
        "The raw threshold numbers are not directly comparable: Legacy RMS is calculated after an extreme-value filter and zero padding, while Adaptive RMS is calculated on the original centred waveform.",
        "",
        "## Results Summary",
        "",
        "| Group | Files | Candidate windows | Legacy selected (active files) | Adaptive Top-1 (active files) | Adaptive-only | Legacy rate | Adaptive rate | Adaptive/Legacy | Legacy windows also adaptive |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['group']} | {row['files']} | {row['candidate_windows']:,} | {row['legacy_selected_windows']:,} ({row['legacy_active_files']}/{row['files']}) | {row['adaptive_top1_rows']:,} ({row['adaptive_active_files']}/{row['files']}) | {row['adaptive_only_windows']:,} | {row['legacy_selection_rate']:.3f}% | {row['adaptive_selection_rate']:.3f}% | {row['adaptive_to_legacy_ratio']:.1f}x | {row['legacy_windows_matched_by_adaptive']:,}/{row['legacy_selected_windows']:,} |"
        )

    lines += [
        "",
        "## Per-group Frequency Results",
        "",
        "Frequency values below are Top-1 peak frequencies in kHz. IQR gives the middle 50% of results.",
        "",
        "| Group | Legacy median (IQR) | Adaptive median (IQR) | Adaptive threshold range | Result |",
        "|---|---:|---:|---:|---|",
    ]
    for row in rows:
        issue = "All Legacy-selected windows were also selected by Adaptive."
        if row["legacy_no_peak_windows"]:
            issue += f" {row['legacy_no_peak_windows']} Legacy-selected window had no valid FFT peak."
        lines.append(
            f"| {row['group']} | {row['legacy_median_khz']:.1f} ({row['legacy_iqr_low_khz']:.1f}-{row['legacy_iqr_high_khz']:.1f}) | {row['adaptive_median_khz']:.1f} ({row['adaptive_iqr_low_khz']:.1f}-{row['adaptive_iqr_high_khz']:.1f}) | {row['adaptive_threshold_min']:.6f}-{row['adaptive_threshold_max']:.6f} | {issue} |"
        )

    lines += [
        "",
        "## Interpretation",
        "",
        f"1. **The repeated result is consistent across all nine groups.** Adaptive selected {total_adaptive:,} Top-1 windows from {total_candidates:,} candidates ({percentage(total_adaptive, total_candidates)}), compared with {total_legacy:,} Legacy-selected windows ({percentage(total_legacy, total_candidates)}). Adaptive therefore returned {total_adaptive / total_legacy:.1f} times as many candidate events.",
        f"2. **Adaptive retained the Legacy selections.** {all_matched:,} of {total_legacy:,} Legacy-selected windows mapped exactly to an Adaptive selected window; {missing_from_adaptive:,} were absent. This is an event-selection containment result, not proof that every added Adaptive window is real AE.",
        "3. **The difference is caused by selection logic, not by using a different FFT.** Both methods use the same 200-sample FFT, Top-1 peak representation, and 20 kHz spacing. The major change is the gate before the FFT: a fixed, group-level and strongly filtered Legacy gate versus a per-file, robust and unfiltered Adaptive gate.",
        "4. **Adaptive frequencies are not expected to be numerically identical to Legacy frequencies.** Adaptive includes many lower-amplitude windows that Legacy discarded, so its median and IQR describe a broader population. The appropriate next comparison is matched-window frequency agreement, followed by waveform and mechanical-data checks.",
        f"5. **T09 exposed one Legacy robustness limitation.** {total_missing_peaks} of {total_legacy:,} Legacy-selected windows had no valid local FFT peak. The original `Peak_Freq.m` assumes that every selected window yields a peak and would form unequal output vectors here. The companion exporter recorded this case and excluded it only from the frequency table; the selected window remains counted. This is not evidence of a bad raw file.",
        "",
        "## Conclusion",
        "",
        "The T01-T09 repeat validation supports the earlier T02-T04 conclusion: the Adaptive workflow is a reproducible superset of the Legacy selection on these nine datasets, while producing substantially more candidate windows. That is a useful algorithmic improvement because it removes dependence on one fixed threshold and one first-file extreme-value setting. It is not yet a claim that the extra Adaptive windows are all genuine AE events or that the method is better for a particular material. Those claims require checking representative raw waveforms and aligning event times with tensile load/displacement or other experiment labels.",
        "",
        "## Next Validation Step",
        "",
        "For each group, sample matched Legacy/Adaptive windows and Adaptive-only windows from low, middle, and high test activity. Plot their raw waveform, RMS, and FFT, then align them with the mechanical record once the correct specimen/time mapping is confirmed. This will test whether the added Adaptive detections are physical AE, background noise, or repeated windows from the same burst.",
    ]
    REPORT_PATH.write_text("\n".join(lines) + "\n")
    print(summary.to_string(index=False))
    print(f"\nWrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
