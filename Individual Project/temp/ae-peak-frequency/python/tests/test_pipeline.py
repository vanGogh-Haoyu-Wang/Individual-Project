from pathlib import Path
import json

import numpy as np
import pandas as pd
from scipy.io import savemat

from ae_peak_frequency.config import AnalysisConfig
from ae_peak_frequency.pipeline import run_analysis


def test_run_analysis_writes_top1_and_top3_outputs(tmp_path: Path) -> None:
    sampling_rate_hz = 1_000_000
    samples = np.arange(200) / sampling_rate_hz
    signal = np.zeros(600)
    signal[250:300] = (
        0.1 * np.sin(2 * np.pi * 100_000 * np.arange(50) / sampling_rate_hz)
        + 0.05 * np.sin(2 * np.pi * 200_000 * np.arange(50) / sampling_rate_hz)
    )
    mat_path = tmp_path / "synthetic.mat"
    savemat(mat_path, {"data": signal.reshape(-1, 1)})
    config = AnalysisConfig(
        sampling_rate_hz=sampling_rate_hz,
        event_window_samples=200,
        window_overlap_samples=1,
        legacy_rms_threshold=0.1,
        adaptive_sigma_multiplier=8.0,
    )

    run_analysis([mat_path], output_dir=tmp_path / "outputs", config=config)

    output_dir = tmp_path / "outputs"
    assert {path.name for path in output_dir.iterdir()} == {
        "baseline_events.csv",
        "top3_events.csv",
        "baseline_peak_frequency.png",
        "top3_peak_frequency.png",
        "run_metadata.json",
    }
    baseline = pd.read_csv(output_dir / "baseline_events.csv")
    top3 = pd.read_csv(output_dir / "top3_events.csv")
    assert baseline.columns.tolist() == [
        "event_id",
        "file_name",
        "event_time_s",
        "peak_rank",
        "frequency_khz",
        "magnitude",
    ]
    assert set(baseline["peak_rank"]) == {1}
    assert top3["peak_rank"].max() <= 3
    assert len(top3) >= len(baseline)
    metadata = json.loads((output_dir / "run_metadata.json").read_text())
    assert metadata["legacy"]["event_counts"] == {"synthetic.mat": 0}
