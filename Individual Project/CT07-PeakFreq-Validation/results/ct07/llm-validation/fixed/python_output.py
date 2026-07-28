from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


PNG_NAMES = (
    "01_strain_stress.png",
    "02_rms.png",
    "03_cumulative_rms.png",
    "04_energy.png",
    "05_cumulative_energy.png",
)


def write_outputs(mechanical, ae, output_dir, candidate_id, repairs):
    """Write the common validation contract after candidate-specific loading."""
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    mechanical.to_csv(output / "mechanical.csv", index=False)
    ae.to_csv(output / "ae.csv", index=False)

    figures = []
    fig, axis = plt.subplots()
    axis.plot(mechanical.strain_pct, mechanical.stress_mpa, color="blue")
    axis.set(xlabel="Strain (%)", ylabel="Stress (MPa)", ylim=(0, 520), title="T07 Strain vs. Stress")
    figures.append(fig)

    def dual(values, ylabel, title, xmax, scatter=False):
        fig, left = plt.subplots()
        right = left.twinx()
        left.plot(mechanical.t1_s, mechanical.stress_mpa, color="blue")
        (right.scatter if scatter else right.plot)(ae.time_s, values, color="red", **({"s": 5} if scatter else {}))
        left.set(xlabel="Time (s)", ylabel="Stress (MPa)", xlim=(0, xmax), ylim=(0, mechanical.stress_mpa.max()), title=title)
        right.set(ylabel=ylabel, xlim=(0, xmax), ylim=(0, 1.05))
        return fig

    figures.extend(
        (
            dual(ae.rms_norm, "Normalised RMS (a.u.)", "T09 Commercial Normalised RMS Profile", 250),
            dual(ae.cumrms_norm, "Normalised Cumulative RMS (a.u.)", "T07 Commercial Normalised Cumulative RMS", 300),
            dual(ae.energy_norm, "Normalised AE Energy (a.u.)", "T07 Commercial Normalised AE Energy", 300, True),
            dual(ae.cumenergy_norm, "Normalised Cumulative AE Energy (a.u.)", "T07 Commercial Normalised Cumulative AE Energy", 300),
        )
    )
    for figure, name in zip(figures, PNG_NAMES):
        figure.tight_layout()
        figure.savefig(output / name, dpi=150)
        plt.close(figure)

    (output / "run_metadata.json").write_text(
        json.dumps(
            {
                "candidate_id": candidate_id,
                "mechanical_rows": len(mechanical),
                "ae_rows": len(ae),
                "png_count": len(PNG_NAMES),
                "repairs": repairs,
                "source_inherited_issue": "Figure 2 title says T09",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

