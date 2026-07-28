from __future__ import annotations

import sys

import numpy as np
import pandas as pd

from python_output import write_outputs


def load_candidate_data(input_path, sheet_name):
    raw = pd.read_excel(input_path, sheet_name=sheet_name, header=None, engine="openpyxl")
    return raw.apply(pd.to_numeric, errors="coerce")


def run_ct07(input_path, sheet_name, output_dir):
    data = load_candidate_data(input_path, sheet_name)
    mechanical_mask = np.isfinite(data.iloc[:, [0, 2, 3]].to_numpy(float)).all(axis=1)
    ae_mask = np.isfinite(data.iloc[:, [4, 8, 9, 11, 13]].to_numpy(float)).all(axis=1)
    mechanical_rows = np.flatnonzero(mechanical_mask)
    ae_rows = np.flatnonzero(ae_mask)
    mechanical = pd.DataFrame(
        {
            "record_index": np.arange(1, len(mechanical_rows) + 1),
            "matrix_row": mechanical_rows + 1,
            "t1_s": data.iloc[mechanical_rows, 0].to_numpy(),
            "strain_pct": data.iloc[mechanical_rows, 2].to_numpy(),
            "stress_mpa": data.iloc[mechanical_rows, 3].to_numpy(),
        }
    )
    ae = pd.DataFrame(
        {
            "record_index": np.arange(1, len(ae_rows) + 1),
            "matrix_row": ae_rows + 1,
            "time_s": data.iloc[ae_rows, 4].to_numpy(),
            "rms_norm": data.iloc[ae_rows, 8].to_numpy(),
            "cumrms_norm": data.iloc[ae_rows, 9].to_numpy(),
            "energy_norm": data.iloc[ae_rows, 11].to_numpy(),
            "cumenergy_norm": data.iloc[ae_rows, 13].to_numpy(),
        }
    )
    write_outputs(mechanical, ae, output_dir, "gpt55_python", ["replace global dropna with two masks", "preserve physical column positions", "CLI/output contract", "headless PNG export"])


if __name__ == "__main__":
    run_ct07(*sys.argv[1:4])
