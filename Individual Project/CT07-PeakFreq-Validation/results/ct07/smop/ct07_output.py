"""Shared CT07 CSV, metadata, and figure writer (no loading or masking)."""

from __future__ import annotations

import json
from pathlib import Path


MECHANICAL_COLUMNS = [
    "record_index",
    "matrix_row",
    "t1_s",
    "strain_pct",
    "stress_mpa",
]
AE_COLUMNS = [
    "record_index",
    "matrix_row",
    "time_s",
    "rms_norm",
    "cumrms_norm",
    "energy_norm",
    "cumenergy_norm",
]
PNG_NAMES = [
    "01_strain_stress.png",
    "02_rms.png",
    "03_cumulative_rms.png",
    "04_energy.png",
    "05_cumulative_energy.png",
]


def write_contract(mechanical, ae, figures, output_dir, metadata):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    if list(mechanical.columns) != MECHANICAL_COLUMNS:
        raise ValueError("Unexpected mechanical.csv schema.")
    if list(ae.columns) != AE_COLUMNS:
        raise ValueError("Unexpected ae.csv schema.")
    if len(figures) != len(PNG_NAMES):
        raise ValueError("Exactly five figures are required.")

    mechanical.to_csv(output / "mechanical.csv", index=False)
    ae.to_csv(output / "ae.csv", index=False)
    for figure, name in zip(figures, PNG_NAMES):
        figure.tight_layout()
        figure.savefig(output / name, dpi=150)

    payload = {
        **metadata,
        "mechanical_rows": len(mechanical),
        "ae_rows": len(ae),
        "png_count": len(PNG_NAMES),
        "source_inherited_issue": "Figure 2 title says T09",
    }
    (output / "run_metadata.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )

