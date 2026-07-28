"""Audited direct repair of the SMOP 0.41 CT07 translation."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ct07_output import write_contract


def run_ct07(input_path, sheet_name, output_dir):
    data = pd.read_excel(input_path, sheet_name=sheet_name, header=None)
    numeric = data.apply(pd.to_numeric, errors="coerce")

    # Preserve SMOP's translated physical-column order.
    t1 = numeric.iloc[:, 0]
    stress = numeric.iloc[:, 3]
    strain = numeric.iloc[:, 2]
    time = numeric.iloc[:, 4]
    rms = numeric.iloc[:, 8]
    cumrms = numeric.iloc[:, 9]
    energy = numeric.iloc[:, 11]
    cumenergy = numeric.iloc[:, 13]

    mechanical_mask = np.isfinite(
        np.column_stack((t1, strain, stress))
    ).all(axis=1)
    ae_mask = np.isfinite(
        np.column_stack((time, rms, cumrms, energy, cumenergy))
    ).all(axis=1)
    mechanical_rows = np.flatnonzero(mechanical_mask)
    ae_rows = np.flatnonzero(ae_mask)
    mechanical = pd.DataFrame(
        {
            "record_index": np.arange(1, len(mechanical_rows) + 1),
            "matrix_row": mechanical_rows + 1,
            "t1_s": t1.iloc[mechanical_rows].to_numpy(),
            "strain_pct": strain.iloc[mechanical_rows].to_numpy(),
            "stress_mpa": stress.iloc[mechanical_rows].to_numpy(),
        }
    )
    ae = pd.DataFrame(
        {
            "record_index": np.arange(1, len(ae_rows) + 1),
            "matrix_row": ae_rows + 1,
            "time_s": time.iloc[ae_rows].to_numpy(),
            "rms_norm": rms.iloc[ae_rows].to_numpy(),
            "cumrms_norm": cumrms.iloc[ae_rows].to_numpy(),
            "energy_norm": energy.iloc[ae_rows].to_numpy(),
            "cumenergy_norm": cumenergy.iloc[ae_rows].to_numpy(),
        }
    )

    figures = []
    fig1, axis1 = plt.subplots()
    axis1.plot(mechanical.strain_pct, mechanical.stress_mpa, "b")
    axis1.set(
        xlabel="Strain (%)",
        ylabel="Stress (MPa)",
        ylim=(0, 520),
        title="T07 Strain vs. Stress",
    )
    axis1.minorticks_on()
    axis1.grid(True, which="minor")
    figures.append(fig1)

    def dual(values, ylabel, title, xmax, scatter=False):
        figure, left = plt.subplots()
        right = left.twinx()
        left.plot(mechanical.t1_s, mechanical.stress_mpa, "b")
        if scatter:
            right.scatter(ae.time_s, values, s=5, color="red")
        else:
            right.plot(ae.time_s, values, "r")
        left.set(
            xlabel="Time (s)",
            ylabel="Stress (MPa)",
            xlim=(0, xmax),
            ylim=(0, mechanical.stress_mpa.max()),
            title=title,
        )
        right.set(xlim=(0, xmax), ylim=(0, 1.05), ylabel=ylabel)
        left.minorticks_on()
        left.grid(True, which="minor")
        return figure

    figures.extend(
        [
            dual(
                ae.rms_norm,
                "Normalised RMS (a.u.)",
                "T09 Commercial Normalised RMS Profile",
                250,
            ),
            dual(
                ae.cumrms_norm,
                "Normalised Cumulative RMS (a.u.)",
                "T07 Commercial Normalised Cumulative RMS",
                300,
            ),
            dual(
                ae.energy_norm,
                "Normalised AE Energy (a.u.)",
                "T07 Commercial Normalised AE Energy",
                300,
                scatter=True,
            ),
            dual(
                ae.cumenergy_norm,
                "Normalised Cumulative AE Energy (a.u.)",
                "T07 Commercial Normalised Cumulative AE Energy",
                300,
            ),
        ]
    )
    write_contract(
        mechanical,
        ae,
        figures,
        output_dir,
        {
            "candidate_id": "smop_script_fixed",
            "path": "script-fixed",
            "repairs": [
                "replace unavailable libsmop IO and plotting",
                "safe mixed-cell numeric conversion",
                "independent mechanical and AE masks",
                "callable CLI and standard output contract",
            ],
        },
    )
    plt.close("all")
    return mechanical, ae


if __name__ == "__main__":
    run_ct07(*sys.argv[1:4])

