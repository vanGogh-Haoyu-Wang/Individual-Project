from __future__ import annotations

import sys

import numpy as np
import pandas as pd

from python_output import write_outputs


def run_ct07(input_path, sheet_name, output_dir):
    data = pd.read_excel(input_path, sheet_name=sheet_name, header=None).to_numpy()
    numeric = pd.DataFrame(data).apply(pd.to_numeric, errors="coerce").to_numpy(float)
    mechanical_rows = np.flatnonzero(np.isfinite(numeric[:, [0, 2, 3]]).all(axis=1))
    ae_rows = np.flatnonzero(np.isfinite(numeric[:, [4, 8, 9, 11, 13]]).all(axis=1))
    mechanical = pd.DataFrame(
        np.column_stack((np.arange(1, len(mechanical_rows) + 1), mechanical_rows + 1, numeric[mechanical_rows][:, [0, 2, 3]])),
        columns=("record_index", "matrix_row", "t1_s", "strain_pct", "stress_mpa"),
    )
    ae = pd.DataFrame(
        np.column_stack((np.arange(1, len(ae_rows) + 1), ae_rows + 1, numeric[ae_rows][:, [4, 8, 9, 11, 13]])),
        columns=("record_index", "matrix_row", "time_s", "rms_norm", "cumrms_norm", "energy_norm", "cumenergy_norm"),
    )
    mechanical[["record_index", "matrix_row"]] = mechanical[["record_index", "matrix_row"]].astype(int)
    ae[["record_index", "matrix_row"]] = ae[["record_index", "matrix_row"]].astype(int)
    write_outputs(mechanical, ae, output_dir, "deepseek_python", ["mixed-cell conversion", "independent complete-case masks", "CLI/output contract", "headless rendering"])


if __name__ == "__main__":
    run_ct07(*sys.argv[1:4])

