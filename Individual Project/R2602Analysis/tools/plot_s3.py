#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "matplotlib>=3.10,<4",
#   "numpy>=2,<3",
# ]
# ///
"""Plot the reproducible S3 supplementary analysis."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def timing_and_frequency(s3: dict) -> Path:
    figure, axes = plt.subplots(1, 2, figsize=(12, 5))
    figure.subplots_adjust(left=0.07, right=0.98, top=0.82, bottom=0.27, wspace=0.25)

    time_counts = s3["ten_equal_time_bin_hit_counts"]
    labels = [f"{index * 10}–{(index + 1) * 10}%" for index in range(10)]
    axes[0].bar(labels, time_counts, color="#0072B2")
    axes[0].set(
        title="Hit count by equal-duration time bin",
        xlabel="Position within recorded S3 interval",
        ylabel="Recognised hit count",
    )
    axes[0].tick_params(axis="x", rotation=45)
    axes[0].grid(axis="y", alpha=0.2)

    frequencies = s3["pfrq_top_values"]
    axes[1].bar(
        [str(int(item["value"])) for item in frequencies],
        [item["count"] for item in frequencies],
        color="#E69F00",
    )
    axes[1].set(
        title="Most frequent P-FRQ values",
        xlabel="Workbook P-FRQ value (unit not confirmed)",
        ylabel="Hit count",
    )
    axes[1].grid(axis="y", alpha=0.2)

    figure.suptitle(
        "S3 paired AE hits: timing concentration and recorded peak-frequency values",
        fontsize=14,
    )
    figure.text(
        0.5,
        0.025,
        "3,553 matched Msg-173/Msg-1 pairs. Equal-duration bins are not mechanical load stages.",
        ha="center",
        fontsize=9,
        color="#555555",
    )
    output = RESULTS / "s3_hit_timing_and_pfrq.png"
    figure.savefig(output, dpi=300)
    plt.close(figure)
    return output


def crack_growth(s3: dict) -> Path:
    with (RESULTS / "s3_crack_growth.tsv").open(newline="") as source:
        rows = [
            row
            for row in csv.DictReader(source, delimiter="\t")
            if row["da_dn"] and row["label"] != "failure" and float(row["da_dn"]) > 0
        ]
    log_delta_k = np.log10([float(row["delta_k"]) for row in rows])
    log_da_dn = np.log10([float(row["da_dn"]) for row in rows])
    correlations = s3["exploratory_correlations"]
    fitted = (
        correlations["paris_log10_slope"] * log_delta_k
        + correlations["paris_log10_intercept"]
    )

    figure, axes = plt.subplots(1, 2, figsize=(12, 5))
    figure.subplots_adjust(left=0.08, right=0.98, top=0.82, bottom=0.22, wspace=0.27)
    axes[0].scatter(log_delta_k, log_da_dn, color="#0072B2", s=45)
    order = np.argsort(log_delta_k)
    axes[0].plot(log_delta_k[order], fitted[order], color="#D55E00", linewidth=1.6)
    axes[0].set(
        title=f"Cached crack-growth relation (n={len(rows)}, r={correlations['paris_log10_pearson_r']:.3f})",
        xlabel="log₁₀(ΔK)",
        ylabel="log₁₀(da/dN)",
    )
    axes[0].grid(alpha=0.2)

    names = ["AE count/cycle", "AE energy/cycle", "AE duration/cycle"]
    values = [
        correlations["da_dn_vs_ae_count_per_cycle_r"],
        correlations["da_dn_vs_ae_energy_per_cycle_r"],
        correlations["da_dn_vs_ae_duration_per_cycle_r"],
    ]
    axes[1].barh(names, values, color=["#009E73", "#E69F00", "#56B4E9"])
    axes[1].set(
        title="Exploratory Pearson correlation with da/dN",
        xlabel="Pearson r",
        xlim=(0, 1),
    )
    axes[1].grid(axis="x", alpha=0.2)
    for index, value in enumerate(values):
        axes[1].text(value + 0.015, index, f"{value:.3f}", va="center")

    figure.suptitle("S3 crack-growth and interval AE metrics", fontsize=14)
    figure.text(
        0.5,
        0.035,
        "Exploratory only: nine cached intervals; failure row excluded because its SUMIFS lacks a lower bound.",
        ha="center",
        fontsize=9,
        color="#555555",
    )
    output = RESULTS / "s3_crack_growth_exploratory.png"
    figure.savefig(output, dpi=300)
    plt.close(figure)
    return output


def main() -> None:
    with (RESULTS / "analysis.json").open() as source:
        s3 = json.load(source)["sheets"]["S3"]
    outputs = [timing_and_frequency(s3), crack_growth(s3)]
    for output in outputs:
        if not output.is_file() or output.stat().st_size == 0:
            raise RuntimeError(f"figure was not written: {output}")
        print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
