from __future__ import annotations

import sys

import numpy as np
import pandas as pd

from python_output import write_outputs


def run_ct07(input_path, sheet_name, output_dir):
    data = pd.read_excel(input_path, sheet_name=sheet_name, header=None)
    columns = {index: pd.to_numeric(data.iloc[:, index], errors="coerce") for index in (0, 2, 3, 4, 8, 9, 11, 13)}
    mechanical_rows = np.flatnonzero(np.isfinite(np.column_stack([columns[0], columns[2], columns[3]])).all(axis=1))
    ae_rows = np.flatnonzero(np.isfinite(np.column_stack([columns[4], columns[8], columns[9], columns[11], columns[13]])).all(axis=1))
    mechanical = pd.DataFrame(
        {
            "record_index": np.arange(1, len(mechanical_rows) + 1),
            "matrix_row": mechanical_rows + 1,
            "t1_s": columns[0].iloc[mechanical_rows].to_numpy(),
            "strain_pct": columns[2].iloc[mechanical_rows].to_numpy(),
            "stress_mpa": columns[3].iloc[mechanical_rows].to_numpy(),
        }
    )
    ae = pd.DataFrame(
        {
            "record_index": np.arange(1, len(ae_rows) + 1),
            "matrix_row": ae_rows + 1,
            "time_s": columns[4].iloc[ae_rows].to_numpy(),
            "rms_norm": columns[8].iloc[ae_rows].to_numpy(),
            "cumrms_norm": columns[9].iloc[ae_rows].to_numpy(),
            "energy_norm": columns[11].iloc[ae_rows].to_numpy(),
            "cumenergy_norm": columns[13].iloc[ae_rows].to_numpy(),
        }
    )
    write_outputs(mechanical, ae, output_dir, "gemini_python", ["safe numeric coercion", "independent complete-case masks", "CLI/output contract", "headless PNG export"])


if __name__ == "__main__":
    run_ct07(*sys.argv[1:4])

