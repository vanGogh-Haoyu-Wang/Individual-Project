"""Analysis configuration shared by event-selection modes."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AnalysisConfig:
    sampling_rate_hz: int
    event_window_samples: int
    window_overlap_samples: int
    legacy_rms_threshold: float
    adaptive_sigma_multiplier: float
