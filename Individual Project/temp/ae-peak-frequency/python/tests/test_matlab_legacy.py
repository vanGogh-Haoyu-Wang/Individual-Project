from pathlib import Path

import numpy as np
from scipy.io import savemat

from ae_peak_frequency.config import AnalysisConfig
from ae_peak_frequency.matlab_legacy import matlab_buffer_frames, run_matlab_legacy


def test_matlab_buffer_frames_have_the_initial_overlap_zero() -> None:
    frames = matlab_buffer_frames(np.arange(1.0, 401.0), window_samples=200, overlap_samples=1)

    assert frames.shape == (2, 200)
    np.testing.assert_allclose(np.sqrt(np.mean(frames[0] ** 2)), 115.0369505854532)
    assert frames[0, :3].tolist() == [0.0, 1.0, 2.0]
    assert frames[1, :3].tolist() == [199.0, 200.0, 201.0]


def test_matlab_legacy_mode_uses_global_frame_indices_and_exports_top1(tmp_path: Path) -> None:
    first = np.zeros(400)
    second = np.zeros(400)
    second[199:399] = 0.5 * np.sin(2 * np.pi * 100_000 * np.arange(200) / 1_000_000)
    first_path, second_path = tmp_path / "01.mat", tmp_path / "02.mat"
    savemat(first_path, {"data": first.reshape(-1, 1)})
    savemat(second_path, {"data": second.reshape(-1, 1)})
    config = AnalysisConfig(1_000_000, 200, 1, 0.1, 8.0)

    events, metadata = run_matlab_legacy(
        [first_path, second_path], config=config, padding_samples=0
    )

    assert events.columns.tolist() == [
        "event_index", "time_s", "peak_frequency_khz", "peak_magnitude"
    ]
    assert events["event_index"].tolist() == [4]
    assert events["time_s"].tolist() == [0.0008]
    assert events["peak_frequency_khz"].tolist() == [100.0]
    assert metadata["file_count"] == 2
    assert metadata["event_count"] == 1
