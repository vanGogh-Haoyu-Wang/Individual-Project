from __future__ import annotations

import sys

import numpy as np
import pandas as pd

from python_output import write_outputs


def run_ct07(input_path, sheet_name, output_dir):
    frame = pd.read_excel(input_path, sheet_name=sheet_name, header=None)
    signals = {
        name: pd.to_numeric(frame.iloc[:, column], errors="coerce")
        for name, column in {
            "t1_s": 0, "strain_pct": 2, "stress_mpa": 3, "time_s": 4,
            "rms_norm": 8, "cumrms_norm": 9, "energy_norm": 11, "cumenergy_norm": 13,
        }.items()
    }
    mechanical_rows = frame.index[np.isfinite(pd.DataFrame({name: signals[name] for name in ("t1_s", "strain_pct", "stress_mpa")}).to_numpy()).all(axis=1)]
    ae_rows = frame.index[np.isfinite(pd.DataFrame({name: signals[name] for name in ("time_s", "rms_norm", "cumrms_norm", "energy_norm", "cumenergy_norm")}).to_numpy()).all(axis=1)]
    mechanical = pd.DataFrame({"record_index": range(1, len(mechanical_rows) + 1), "matrix_row": mechanical_rows + 1, **{name: signals[name].loc[mechanical_rows].to_numpy() for name in ("t1_s", "strain_pct", "stress_mpa")}})
    ae = pd.DataFrame({"record_index": range(1, len(ae_rows) + 1), "matrix_row": ae_rows + 1, **{name: signals[name].loc[ae_rows].to_numpy() for name in ("time_s", "rms_norm", "cumrms_norm", "energy_norm", "cumenergy_norm")}})
    write_outputs(mechanical, ae, output_dir, "sonnet_python", ["header row handling", "numeric coercion for AE columns", "independent complete-case masks", "function/CLI/output contract"])


if __name__ == "__main__":
    run_ct07(*sys.argv[1:4])

