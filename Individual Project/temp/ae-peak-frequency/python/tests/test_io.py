from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy.io import savemat

from ae_peak_frequency.io import load_summary, load_waveform


def test_load_waveform_uses_first_data_column(tmp_path: Path) -> None:
    mat_path = tmp_path / "signal.mat"
    savemat(mat_path, {"data": np.array([[0.0, 10.0], [1.0, 11.0], [-1.0, 12.0]])})

    signal = load_waveform(mat_path)

    assert signal.ndim == 1
    assert signal.dtype == np.float64
    assert signal.tolist() == [0.0, 1.0, -1.0]


def test_load_waveform_rejects_missing_data_variable(tmp_path: Path) -> None:
    mat_path = tmp_path / "missing_data.mat"
    savemat(mat_path, {"other": np.array([1.0])})

    with pytest.raises(ValueError, match="data"):
        load_waveform(mat_path)


def test_load_summary_reads_csv(tmp_path: Path) -> None:
    csv_path = tmp_path / "summary.csv"
    pd.DataFrame([["time", "stress"], [0.0, 10.0], [1.0, 20.0]]).to_csv(
        csv_path, index=False, header=False
    )

    summary = load_summary(csv_path)

    assert summary.shape == (3, 2)
    assert summary.iloc[0].tolist() == ["time", "stress"]


def test_load_summary_reads_xlsx_without_reinterpreting_rows(tmp_path: Path) -> None:
    xlsx_path = tmp_path / "summary.xlsx"
    pd.DataFrame([["label", "units"], [1.0, 2.0]]).to_excel(xlsx_path, index=False, header=False)

    summary = load_summary(xlsx_path)

    assert summary.shape == (2, 2)
    assert summary.iloc[0, 0] == "label"


def test_load_summary_reads_requested_xlsx_sheet(tmp_path: Path) -> None:
    xlsx_path = tmp_path / "summary.xlsx"
    with pd.ExcelWriter(xlsx_path) as writer:
        pd.DataFrame([["first"]]).to_excel(writer, sheet_name="Summary", index=False, header=False)
        pd.DataFrame([["ct07"], [1.0]]).to_excel(writer, sheet_name="CT-07", index=False, header=False)

    summary = load_summary(xlsx_path, sheet_name="CT-07")

    assert summary.shape == (2, 1)
    assert summary.iloc[0, 0] == "ct07"
