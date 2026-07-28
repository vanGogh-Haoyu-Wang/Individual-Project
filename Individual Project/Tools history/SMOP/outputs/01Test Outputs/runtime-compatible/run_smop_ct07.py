"""Execute the syntax-normalized SMOP output through the CT07 runtime adapter."""

from __future__ import annotations

import hashlib
import runpy
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import libsmop
from ct07_output import write_contract


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run_smop_ct07(raw_script, input_path, sheet_name, output_dir):
    raw_script = Path(raw_script).resolve()
    libsmop.configure(input_path, sheet_name)
    namespace = runpy.run_path(str(raw_script), run_name="__smop_ct07__")

    values = {
        name: np.asarray(namespace[name], dtype=float).reshape(-1)
        for name in (
            "t1",
            "stress",
            "strain",
            "time",
            "rms",
            "cumrms",
            "energy",
            "cumenergy",
        )
    }
    mechanical_mask = np.isfinite(
        np.column_stack((values["t1"], values["strain"], values["stress"]))
    ).all(axis=1)
    ae_mask = np.isfinite(
        np.column_stack(
            (
                values["time"],
                values["rms"],
                values["cumrms"],
                values["energy"],
                values["cumenergy"],
            )
        )
    ).all(axis=1)
    mechanical_rows = np.flatnonzero(mechanical_mask)
    ae_rows = np.flatnonzero(ae_mask)
    mechanical = pd.DataFrame(
        {
            "record_index": np.arange(1, len(mechanical_rows) + 1),
            "matrix_row": mechanical_rows + 1,
            "t1_s": values["t1"][mechanical_rows],
            "strain_pct": values["strain"][mechanical_rows],
            "stress_mpa": values["stress"][mechanical_rows],
        }
    )
    ae = pd.DataFrame(
        {
            "record_index": np.arange(1, len(ae_rows) + 1),
            "matrix_row": ae_rows + 1,
            "time_s": values["time"][ae_rows],
            "rms_norm": values["rms"][ae_rows],
            "cumrms_norm": values["cumrms"][ae_rows],
            "energy_norm": values["energy"][ae_rows],
            "cumenergy_norm": values["cumenergy"][ae_rows],
        }
    )
    write_contract(
        mechanical,
        ae,
        libsmop.figures(),
        output_dir,
        {
            "candidate_id": "smop_runtime_compatible",
            "path": "runtime-compatible",
            "executed_script": str(raw_script),
            "executed_script_sha256": sha256(raw_script),
            "runtime_scope": "CT07-only; not a general libsmop replacement",
            "repairs": [
                "syntax-only top-level indentation normalization",
                "CT07-scoped Excel and MATLAB indexing adapter",
                "CT07-scoped pyplot and yyaxis adapter",
                "runner-owned independent masks and output contract",
            ],
        },
    )
    return mechanical, ae


if __name__ == "__main__":
    run_smop_ct07(*sys.argv[1:5])
