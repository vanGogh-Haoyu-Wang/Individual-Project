"""RMS-based AE event selection."""

from dataclasses import dataclass

import numpy as np

from .config import AnalysisConfig


@dataclass(frozen=True)
class Event:
    start_sample: int
    samples: np.ndarray


def legacy_extrema_filter(signal: np.ndarray) -> np.ndarray:
    """Preserve only global extrema, matching the MATLAB mask operation."""
    filtered = np.asarray(signal, dtype=float).copy()
    minimum = filtered.min()
    maximum = filtered.max()
    filtered[(filtered > minimum) & (filtered < maximum)] = 0.0
    return filtered


def adaptive_threshold(rms: np.ndarray, sigma_multiplier: float) -> float:
    """Return median RMS plus a robust multiple of background variation."""
    median = float(np.median(rms))
    mad = float(np.median(np.abs(rms - median)))
    return median + sigma_multiplier * 1.4826 * mad


def _window_starts(signal_length: int, config: AnalysisConfig) -> np.ndarray:
    hop = config.event_window_samples - config.window_overlap_samples
    return np.arange(0, signal_length - config.event_window_samples + 1, hop)


def _window_rms(signal: np.ndarray, starts: np.ndarray, window_length: int) -> np.ndarray:
    return np.array(
        [np.sqrt(np.mean(signal[start : start + window_length] ** 2)) for start in starts],
        dtype=float,
    )


def detect_events(
    signal: np.ndarray, config: AnalysisConfig, mode: str
) -> tuple[list[Event], float]:
    """Select fixed-length waveform segments with legacy or adaptive RMS thresholds."""
    centered = np.asarray(signal, dtype=float) - float(np.mean(signal))
    working = legacy_extrema_filter(centered) if mode == "legacy" else centered
    starts = _window_starts(len(working), config)
    rms = _window_rms(working, starts, config.event_window_samples)

    if mode == "legacy":
        threshold = config.legacy_rms_threshold
    elif mode == "adaptive":
        threshold = adaptive_threshold(rms, config.adaptive_sigma_multiplier)
    else:
        raise ValueError("mode must be 'legacy' or 'adaptive'")

    selected_starts = starts[rms > threshold]
    events = [
        Event(
            start_sample=int(start),
            samples=working[start : start + config.event_window_samples],
        )
        for start in selected_starts
    ]
    return events, threshold
