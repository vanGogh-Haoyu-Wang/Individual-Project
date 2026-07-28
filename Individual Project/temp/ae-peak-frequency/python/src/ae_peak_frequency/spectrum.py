"""Frequency-domain analysis for selected AE waveform events."""

from dataclasses import dataclass

import numpy as np
from scipy.signal import find_peaks


@dataclass(frozen=True)
class Peak:
    frequency_khz: float
    magnitude: float


def ranked_peaks(
    samples: np.ndarray,
    *,
    sampling_rate_hz: int,
    min_peak_distance_khz: float,
    count: int,
) -> list[Peak]:
    """Return up to ``count`` separated FFT peaks in descending magnitude order."""
    waveform = np.asarray(samples, dtype=float)
    magnitudes = np.abs(np.fft.rfft(waveform))
    frequencies_khz = np.fft.rfftfreq(len(waveform), d=1 / sampling_rate_hz) / 1000.0
    bin_spacing_khz = sampling_rate_hz / len(waveform) / 1000.0
    # MATLAB findpeaks treats MinPeakDistance as a strict separation boundary.
    minimum_distance_bins = max(
        1, int(np.floor(min_peak_distance_khz / bin_spacing_khz)) + 1
    )

    indices, _ = find_peaks(magnitudes, distance=minimum_distance_bins)
    ordered_indices = indices[np.argsort(magnitudes[indices])[::-1]]

    return [
        Peak(float(frequencies_khz[index]), float(magnitudes[index]))
        for index in ordered_indices[:count]
    ]
