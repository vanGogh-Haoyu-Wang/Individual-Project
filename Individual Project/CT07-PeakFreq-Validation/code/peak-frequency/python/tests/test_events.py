import numpy as np
import pytest

from ae_peak_frequency.config import AnalysisConfig
from ae_peak_frequency.events import (
    adaptive_threshold,
    detect_events,
    legacy_extrema_filter,
)


@pytest.fixture
def config() -> AnalysisConfig:
    return AnalysisConfig(
        sampling_rate_hz=1_000_000,
        event_window_samples=200,
        window_overlap_samples=1,
        legacy_rms_threshold=0.1,
        adaptive_sigma_multiplier=8.0,
    )


def test_legacy_extrema_filter_keeps_only_global_extrema() -> None:
    filtered = legacy_extrema_filter(np.array([-2.0, -1.0, 0.0, 1.0, 3.0]))

    assert filtered.tolist() == [-2.0, 0.0, 0.0, 0.0, 3.0]


def test_adaptive_threshold_uses_median_and_robust_noise_scale() -> None:
    rms = np.array([0.9, 1.0, 1.0, 1.1, 4.0])

    threshold = adaptive_threshold(rms, sigma_multiplier=8.0)

    assert threshold == pytest.approx(2.18608, abs=1e-5)


def test_adaptive_detection_returns_one_event_window(config: AnalysisConfig) -> None:
    signal = np.zeros(600)
    signal[250:300] = 0.1 * np.sin(2 * np.pi * np.arange(50) / 20)

    events, threshold = detect_events(signal, config, mode="adaptive")

    assert 0.0 < threshold < 0.01
    assert len(events) == 1
    assert events[0].start_sample == 199
    assert events[0].samples.shape == (200,)
