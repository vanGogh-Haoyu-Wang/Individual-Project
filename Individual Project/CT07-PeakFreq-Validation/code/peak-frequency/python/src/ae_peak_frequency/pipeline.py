"""Run adaptive Top-1 and Top-3 AE peak-frequency analysis."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pandas as pd

from .config import AnalysisConfig
from .events import detect_events
from .io import load_summary, load_waveform
from .spectrum import ranked_peaks


EVENT_COLUMNS = [
    "event_id",
    "file_name",
    "start_sample",
    "event_time_s",
    "peak_rank",
    "frequency_khz",
    "magnitude",
]
SELECTED_EVENT_COLUMNS = [
    "event_id",
    "file_name",
    "start_sample",
    "event_time_s",
    "rms",
    "threshold",
    "valid_peak_count",
]


def _event_rows(
    events, source_path: Path, config: AnalysisConfig, peak_count: int, event_id_start: int
) -> list[dict[str, float | int | str]]:
    rows: list[dict[str, float | int | str]] = []
    for offset, event in enumerate(events):
        event_id = event_id_start + offset
        peaks = ranked_peaks(
            event.samples,
            sampling_rate_hz=config.sampling_rate_hz,
            min_peak_distance_khz=20.0,
            count=peak_count,
        )
        for rank, peak in enumerate(peaks, start=1):
            rows.append(
                {
                    "event_id": event_id,
                    "file_name": source_path.name,
                    "start_sample": event.start_sample,
                    "event_time_s": event.start_sample / config.sampling_rate_hz,
                    "peak_rank": rank,
                    "frequency_khz": peak.frequency_khz,
                    "magnitude": peak.magnitude,
                }
            )
    return rows


def _write_plot(events: pd.DataFrame, title: str, path: Path) -> None:
    os.environ.setdefault("MPLCONFIGDIR", str(path.parent.parent / ".matplotlib-cache"))
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    figure, axis = plt.subplots(figsize=(8, 4.5))
    axis.scatter(events["event_time_s"], events["frequency_khz"], s=8, color="tab:red")
    axis.set_xlabel("Time (s)")
    axis.set_ylabel("Peak Frequency (kHz)")
    axis.set_ylim(0, 500)
    axis.grid(which="both", alpha=0.3)
    axis.set_title(title)
    figure.tight_layout()
    figure.savefig(path, dpi=150)
    plt.close(figure)


def run_analysis(
    mat_paths: list[Path], *, output_dir: Path, config: AnalysisConfig,
    summary_path: Path | None = None, summary_sheet: str | None = None,
    write_plots: bool = True,
) -> None:
    """Analyse selected waveform files and export Top-1 and Top-3 results."""
    output_dir.mkdir(parents=True, exist_ok=True)
    baseline_rows: list[dict[str, float | int | str]] = []
    top3_rows: list[dict[str, float | int | str]] = []
    selected_rows: list[dict[str, float | int | str]] = []
    threshold_rows: list[dict[str, float | int | str]] = []
    thresholds: dict[str, float] = {}
    legacy_thresholds: dict[str, float] = {}
    legacy_event_counts: dict[str, int] = {}
    next_event_id = 1
    summary_metadata = None
    if summary_path is not None:
        summary = load_summary(summary_path, sheet_name=summary_sheet)
        summary_metadata = {
            "path": str(summary_path),
            "rows": int(summary.shape[0]),
            "columns": int(summary.shape[1]),
            "sheet_name": summary_sheet,
        }

    for path in mat_paths:
        waveform = load_waveform(path)
        legacy_events, legacy_threshold = detect_events(waveform, config, mode="legacy")
        events, threshold = detect_events(waveform, config, mode="adaptive")
        thresholds[path.name] = threshold
        legacy_thresholds[path.name] = legacy_threshold
        legacy_event_counts[path.name] = len(legacy_events)
        for offset, event in enumerate(events):
            peak_count = len(
                ranked_peaks(
                    event.samples,
                    sampling_rate_hz=config.sampling_rate_hz,
                    min_peak_distance_khz=20.0,
                    count=3,
                )
            )
            selected_rows.append(
                {
                    "event_id": next_event_id + offset,
                    "file_name": path.name,
                    "start_sample": event.start_sample,
                    "event_time_s": event.start_sample / config.sampling_rate_hz,
                    "rms": event.rms,
                    "threshold": threshold,
                    "valid_peak_count": peak_count,
                }
            )
        candidate_count = max(
            0,
            (len(waveform) - config.event_window_samples)
            // (config.event_window_samples - config.window_overlap_samples)
            + 1,
        )
        threshold_rows.append(
            {
                "file_name": path.name,
                "candidate_window_count": candidate_count,
                "selected_event_count": len(events),
                "threshold": threshold,
            }
        )
        baseline_rows.extend(_event_rows(events, path, config, peak_count=1, event_id_start=next_event_id))
        top3_rows.extend(_event_rows(events, path, config, peak_count=3, event_id_start=next_event_id))
        next_event_id += len(events)

    baseline = pd.DataFrame(baseline_rows, columns=EVENT_COLUMNS)
    top3 = pd.DataFrame(top3_rows, columns=EVENT_COLUMNS)
    selected = pd.DataFrame(selected_rows, columns=SELECTED_EVENT_COLUMNS)
    threshold_table = pd.DataFrame(
        threshold_rows,
        columns=[
            "file_name",
            "candidate_window_count",
            "selected_event_count",
            "threshold",
        ],
    )
    baseline.to_csv(output_dir / "baseline_events.csv", index=False)
    top3.to_csv(output_dir / "top3_events.csv", index=False)
    selected.to_csv(output_dir / "selected_events.csv", index=False)
    threshold_table.to_csv(output_dir / "thresholds.csv", index=False)
    if write_plots:
        _write_plot(baseline, "AE Peak Frequency: Top-1", output_dir / "baseline_peak_frequency.png")
        _write_plot(top3, "AE Peak Frequency: Top-3", output_dir / "top3_peak_frequency.png")
    (output_dir / "run_metadata.json").write_text(
        json.dumps(
            {
                "mode": "adaptive",
                "sampling_rate_hz": config.sampling_rate_hz,
                "event_window_samples": config.event_window_samples,
                "window_overlap_samples": config.window_overlap_samples,
                "adaptive_sigma_multiplier": config.adaptive_sigma_multiplier,
                "thresholds": thresholds,
                "legacy": {
                    "rms_threshold": config.legacy_rms_threshold,
                    "thresholds": legacy_thresholds,
                    "event_counts": legacy_event_counts,
                },
                "summary": summary_metadata,
            },
            indent=2,
        )
    )
