from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest


MODULE_PATH = Path(__file__).with_name("scientific_analysis.py")
SPEC = importlib.util.spec_from_file_location("scientific_analysis", MODULE_PATH)
analysis = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(analysis)


def test_legacy_index_mapping_uses_30150_window_file_domain() -> None:
    files = ["a.mat", "b.mat"]
    assert analysis.legacy_index_to_key(1, files, 30_150, 199) == ("a.mat", 0)
    assert analysis.legacy_index_to_key(30_150, files, 30_150, 199) == (
        "a.mat",
        30_149 * 199,
    )
    assert analysis.legacy_index_to_key(30_151, files, 30_150, 199) == (
        "b.mat",
        0,
    )
    with pytest.raises(ValueError):
        analysis.legacy_index_to_key(60_301, files, 30_150, 199)


def test_burst_clustering_respects_hop_factor_and_keeps_max_rms() -> None:
    catalog = pd.DataFrame(
        {
            "group": ["T01"] * 4,
            "file_name": ["a.mat"] * 4,
            "start_sample": [0, 199, 597, 1_194],
            "rms": [1.0, 3.0, 2.0, 4.0],
        }
    )
    bursts = analysis.cluster_bursts(catalog, hop_factor=2, hop=199)
    assert len(bursts) == 2
    assert bursts["start_sample"].tolist() == [199, 1_194]
    assert bursts["burst_event_count"].tolist() == [3, 1]


def test_alignment_recovers_known_shift() -> None:
    index = np.arange(20)
    pulse = np.zeros(20)
    pulse[[2, 7, 12, 17]] = [1, 4, 2, 3]
    waveform = pd.DataFrame(index=index)
    ct = pd.DataFrame(index=np.arange(30))
    for waveform_name, ct_name in analysis.ACTIVITY_PAIRS:
        waveform[waveform_name] = pulse
        shifted = np.zeros(30)
        shifted[5:25] = pulse
        ct[ct_name] = shifted
    result = analysis.best_alignment(waveform, ct, 1.0, -10, 10)
    assert result["offset_s"] == 5.0
    assert result["composite_score"] == pytest.approx(1.0)


def test_stage_boundaries_and_no_extrapolation() -> None:
    mechanical = pd.DataFrame(
        {
            "test_time_s": [0, 1, 2, 3, 4],
            "stress_mpa": [0, 10, 50, 100, 20],
        }
    )
    stages, boundaries = analysis.assign_stage(
        np.array([-1, 0, 1, 2, 3, 4, 5], dtype=float), mechanical
    )
    assert stages.tolist() == [
        "out_of_range",
        "preload",
        "rising_load",
        "rising_load",
        "near_peak",
        "post_peak",
        "out_of_range",
    ]
    assert boundaries == {"t5_s": 1.0, "t90_s": 3.0, "tmax_s": 3.0}


def test_bh_adjust_and_frequency_bands() -> None:
    adjusted = analysis.bh_adjust(
        [(("a", "a", "m"), 0.001), (("b", "b", "m"), 0.04)]
    )
    assert adjusted[("a", "a", "m")] == pytest.approx(0.002)
    assert adjusted[("b", "b", "m")] == pytest.approx(0.04)
    bands = analysis.frequency_band(pd.Series([0, 199.999, 200, 500]))
    assert bands.astype(str).tolist() == ["0-200", "0-200", "200-250", "400-500"]

