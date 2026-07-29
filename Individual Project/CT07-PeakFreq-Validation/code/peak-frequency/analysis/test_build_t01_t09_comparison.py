from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).with_name("build_t01_t09_comparison.py")
SPEC = importlib.util.spec_from_file_location("build_t01_t09_comparison", MODULE_PATH)
comparison = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(comparison)


def test_selection_metrics_keep_legacy_and_adaptive_denominators_separate() -> None:
    metrics = comparison.selection_metrics(
        legacy_selected=16_240,
        legacy_frames=11_366_550,
        adaptive_selected=522_216,
        adaptive_windows=9_472_125,
    )
    assert metrics["legacy_selection_rate"] == pytest.approx(16_240 / 11_366_550)
    assert metrics["adaptive_selection_rate"] == pytest.approx(522_216 / 9_472_125)
    assert metrics["adaptive_selection_rate"] != pytest.approx(522_216 / 11_366_550)
    assert metrics["selected_count_ratio"] == pytest.approx(522_216 / 16_240)
