from pathlib import Path
import json

import numpy as np
import pandas as pd
import pytest
from scipy.io import savemat

from ae_peak_frequency.cli import main


def test_cli_runs_a_mat_file_and_writes_outputs(tmp_path: Path) -> None:
    signal = np.zeros(600)
    signal[250:300] = 0.1 * np.sin(2 * np.pi * np.arange(50) / 20)
    mat_path = tmp_path / "command_input.mat"
    savemat(mat_path, {"data": signal.reshape(-1, 1)})
    output_dir = tmp_path / "outputs"

    exit_code = main([str(mat_path), "--output-dir", str(output_dir)])

    assert exit_code == 0
    assert (output_dir / "baseline_events.csv").exists()
    assert (output_dir / "top3_events.csv").exists()


def test_cli_runs_matlab_legacy_multifile_mode(tmp_path: Path) -> None:
    first_path, second_path = tmp_path / "01.mat", tmp_path / "02.mat"
    savemat(first_path, {"data": np.zeros((400, 1))})
    signal = np.zeros(400)
    signal[199:399] = 0.5 * np.sin(2 * np.pi * 100_000 * np.arange(200) / 1_000_000)
    savemat(second_path, {"data": signal.reshape(-1, 1)})
    output_dir = tmp_path / "legacy-outputs"

    exit_code = main(
        [
            str(first_path),
            str(second_path),
            "--legacy-matlab-multifile",
            "--output-dir",
            str(output_dir),
        ]
    )

    assert exit_code == 0
    assert (output_dir / "legacy_top1_events.csv").exists()
    assert (output_dir / "legacy_run_metadata.json").exists()


@pytest.mark.parametrize("suffix", [".csv", ".xlsx"])
def test_cli_records_optional_summary_dimensions(tmp_path: Path, suffix: str) -> None:
    signal = np.zeros(600)
    signal[250:300] = 0.1 * np.sin(2 * np.pi * np.arange(50) / 20)
    mat_path = tmp_path / "summary_input.mat"
    savemat(mat_path, {"data": signal.reshape(-1, 1)})
    summary_path = tmp_path / f"summary{suffix}"
    summary = pd.DataFrame([["time", "stress"], [0.0, 10.0]])
    if suffix == ".csv":
        summary.to_csv(summary_path, index=False, header=False)
    else:
        summary.to_excel(summary_path, index=False, header=False)
    output_dir = tmp_path / "outputs"

    exit_code = main(
        [
            str(mat_path),
            "--summary",
            str(summary_path),
            "--output-dir",
            str(output_dir),
        ]
    )

    metadata = json.loads((output_dir / "run_metadata.json").read_text())
    assert exit_code == 0
    assert metadata["summary"] == {
        "path": str(summary_path),
        "rows": 2,
        "columns": 2,
        "sheet_name": None,
    }
