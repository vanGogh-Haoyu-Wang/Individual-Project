"""Input helpers for raw AE waveforms and experiment summaries."""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.io import loadmat


def load_waveform(path: Path) -> np.ndarray:
    """Load the first numeric column of the MATLAB ``data`` variable."""
    raw = loadmat(path)
    if "data" not in raw:
        raise ValueError(f"{path} does not contain a data variable")

    data = np.asarray(raw["data"], dtype=float)
    if data.ndim != 2 or data.shape[1] < 1:
        raise ValueError(f"{path} data must have at least one column")

    return data[:, 0]


def load_summary(path: Path, sheet_name: str | None = None) -> pd.DataFrame:
    """Read a CSV or Excel summary without changing its physical rows."""
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path, header=None)
    if suffix == ".xlsx":
        selected_sheet = 0 if sheet_name is None else sheet_name
        return pd.read_excel(path, sheet_name=selected_sheet, header=None)
    raise ValueError("summary input must be .csv or .xlsx")
