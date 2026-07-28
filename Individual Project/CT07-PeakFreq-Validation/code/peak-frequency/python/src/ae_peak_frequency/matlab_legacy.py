"""Exact-data-contract reproduction of the multi-file legacy MATLAB workflow."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from .config import AnalysisConfig
from .io import load_waveform
from .spectrum import ranked_peaks


LEGACY_COLUMNS = ["event_index", "time_s", "peak_frequency_khz", "peak_magnitude"]


def matlab_buffer_frames(
    signal: np.ndarray, *, window_samples: int, overlap_samples: int
) -> np.ndarray:
    """Return the non-final columns from MATLAB ``buffer(signal,n,p)``.

    MATLAB prepends ``p`` zeros to the first column and its final padded column
    is discarded by the original script via ``adj(1:end-1)``.
    """
    signal = np.asarray(signal, dtype=float)
    hop = window_samples - overlap_samples
    padded = np.concatenate((np.zeros(overlap_samples), signal))
    starts = np.arange(0, len(padded) - window_samples + 1, hop)
    return np.stack([padded[start : start + window_samples] for start in starts])


def run_matlab_legacy(
    mat_paths: list[Path],
    *,
    config: AnalysisConfig,
    output_dir: Path | None = None,
    padding_samples: int = 1_000_000,
) -> tuple[pd.DataFrame, dict[str, object]]:
    """Reproduce ``Peak_Freq.m`` multi-file event and Top-1 peak rows.

    The first file defines the mean and extrema for every following file.
    ``event_index`` and ``time_s`` intentionally use the script's concatenated
    MovingRMS-frame convention, including its 200-sample time multiplier.
    """
    paths = sorted((Path(path) for path in mat_paths), key=lambda path: path.name)
    if not paths:
        raise ValueError("at least one MAT file is required")

    first_signal = load_waveform(paths[0])
    first_mean = float(np.mean(first_signal))
    first_working = np.concatenate((first_signal - first_mean, np.zeros(padding_samples)))
    upper_extreme = float(np.max(first_working))
    lower_extreme = float(np.min(first_working))

    rows: list[dict[str, float | int]] = []
    global_frame_offset = 0
    for path in paths:
        signal = load_waveform(path)
        working = np.concatenate((signal - first_mean, np.zeros(padding_samples)))
        working[(working < upper_extreme) & (working > lower_extreme)] = 0.0
        frames = matlab_buffer_frames(
            working,
            window_samples=config.event_window_samples,
            overlap_samples=config.window_overlap_samples,
        )
        rms = np.sqrt(np.mean(np.square(frames), axis=1))
        selected_frames = np.flatnonzero(rms > config.legacy_rms_threshold)
        for frame in selected_frames:
            samples = frames[frame]
            peaks = ranked_peaks(
                samples,
                sampling_rate_hz=config.sampling_rate_hz,
                min_peak_distance_khz=20.0,
                count=1,
            )
            if not peaks:
                continue
            peak = peaks[0]
            event_index = global_frame_offset + int(frame) + 1
            rows.append(
                {
                    "event_index": event_index,
                    "time_s": event_index * config.event_window_samples / config.sampling_rate_hz,
                    "peak_frequency_khz": peak.frequency_khz,
                    "peak_magnitude": peak.magnitude,
                }
            )
        global_frame_offset += len(frames)

    events = pd.DataFrame(rows, columns=LEGACY_COLUMNS)
    metadata: dict[str, object] = {
        "mode": "matlab_legacy_multifile",
        "input_files": [str(path) for path in paths],
        "file_count": len(paths),
        "first_file_mean": first_mean,
        "upper_extreme": upper_extreme,
        "lower_extreme": lower_extreme,
        "padding_samples": padding_samples,
        "window_samples": config.event_window_samples,
        "sample_rate_hz": config.sampling_rate_hz,
        "event_rms_threshold": config.legacy_rms_threshold,
        "event_count": len(events),
    }
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        events.to_csv(output_dir / "legacy_top1_events.csv", index=False)
        (output_dir / "legacy_run_metadata.json").write_text(json.dumps(metadata, indent=2))
    return events, metadata
