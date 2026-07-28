import numpy as np
import pytest

from ae_peak_frequency.spectrum import ranked_peaks


def test_ranked_peaks_returns_strongest_known_frequency() -> None:
    sampling_rate_hz = 1_000_000
    samples = np.arange(200) / sampling_rate_hz
    waveform = 0.8 * np.sin(2 * np.pi * 100_000 * samples)

    peaks = ranked_peaks(
        waveform,
        sampling_rate_hz=sampling_rate_hz,
        min_peak_distance_khz=20.0,
        count=1,
    )

    assert len(peaks) == 1
    assert peaks[0].frequency_khz == pytest.approx(100.0, abs=5.0)


def test_ranked_peaks_returns_top_three_by_magnitude() -> None:
    sampling_rate_hz = 1_000_000
    samples = np.arange(200) / sampling_rate_hz
    waveform = (
        0.8 * np.sin(2 * np.pi * 100_000 * samples)
        + 0.5 * np.sin(2 * np.pi * 200_000 * samples)
        + 0.2 * np.sin(2 * np.pi * 300_000 * samples)
    )

    peaks = ranked_peaks(
        waveform,
        sampling_rate_hz=sampling_rate_hz,
        min_peak_distance_khz=20.0,
        count=3,
    )

    assert [peak.frequency_khz for peak in peaks] == pytest.approx([100.0, 200.0, 300.0])
    assert peaks[0].magnitude > peaks[1].magnitude > peaks[2].magnitude


def test_ranked_peaks_returns_no_peak_for_zero_waveform() -> None:
    peaks = ranked_peaks(
        np.zeros(200),
        sampling_rate_hz=1_000_000,
        min_peak_distance_khz=20.0,
        count=3,
    )

    assert peaks == []


def test_minimum_peak_distance_matches_matlab_strict_boundary() -> None:
    samples = np.arange(200) / 1_000_000
    waveform = (
        np.sin(2 * np.pi * 100_000 * samples)
        + 0.8 * np.sin(2 * np.pi * 120_000 * samples)
        + 0.6 * np.sin(2 * np.pi * 160_000 * samples)
    )
    peaks = ranked_peaks(
        waveform,
        sampling_rate_hz=1_000_000,
        min_peak_distance_khz=20.0,
        count=3,
    )
    frequencies = [peak.frequency_khz for peak in peaks]
    assert frequencies[:2] == pytest.approx([100.0, 160.0])
    assert 120.0 not in frequencies
