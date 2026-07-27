#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "matplotlib>=3.10,<4",
#   "numpy>=2,<3",
# ]
# ///
"""Generate the two waveform figures used to inspect the validated fixture."""

from __future__ import annotations

import csv
import subprocess
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "test/data/python/210527-CH1-15.DTA"
REFERENCE = ROOT / "test/reference"
RESULTS = ROOT / "results"

JULIA_EXPORT = r"""
using MistrasDTAJulia

data = read_dta(ARGS[1])
open(ARGS[2], "w") do io
    for waveform in data.waveforms
        axes = waveform_axes(waveform; time_unit=:us)
        write(io, axes.time)
        write(io, axes.voltage)
    end
end
"""


def load_metadata() -> list[dict[str, int | float]]:
    with (REFERENCE / "waveforms.tsv").open(newline="") as handle:
        return [
            {
                "index": int(row["index"]),
                "time_s": float(row["time_s"]),
                "channel": int(row["channel"]),
                "sample_rate_hz": int(row["sample_rate_hz"]),
                "trigger_delay_samples": int(row["trigger_delay_samples"]),
                "value_offset": int(row["value_offset"]),
                "sample_count": int(row["sample_count"]),
            }
            for row in csv.DictReader(handle, delimiter="\t")
        ]


def load_waveforms() -> tuple[list[dict[str, int | float]], list[np.ndarray], list[np.ndarray], list[np.ndarray]]:
    metadata = load_metadata()
    reference_values = np.fromfile(REFERENCE / "waveforms.f64le", dtype="<f8")

    with tempfile.TemporaryDirectory() as directory:
        julia_output = Path(directory) / "waveforms.f64le"
        subprocess.run(
            [
                "julia",
                f"--project={ROOT}",
                "-e",
                JULIA_EXPORT,
                str(FIXTURE),
                str(julia_output),
            ],
            check=True,
        )
        julia_values = np.fromfile(julia_output, dtype="<f8")

    sample_total = sum(int(row["sample_count"]) for row in metadata)
    if julia_values.size != 2 * sample_total:
        raise RuntimeError(
            f"Julia exported {julia_values.size} values; expected {2 * sample_total}"
        )

    reference_voltage: list[np.ndarray] = []
    julia_time: list[np.ndarray] = []
    julia_voltage: list[np.ndarray] = []
    cursor = 0
    for row in metadata:
        count = int(row["sample_count"])
        offset = int(row["value_offset"])
        time = julia_values[cursor : cursor + count]
        voltage = julia_values[cursor + count : cursor + 2 * count]
        reference = reference_values[offset : offset + count]
        expected_time = (
            np.arange(count) + int(row["trigger_delay_samples"])
        ) / int(row["sample_rate_hz"]) * 1e6

        np.testing.assert_allclose(time, expected_time, rtol=0, atol=1e-12)
        np.testing.assert_allclose(voltage, reference, rtol=1e-12, atol=1e-12)
        julia_time.append(time)
        julia_voltage.append(voltage)
        reference_voltage.append(reference)
        cursor += 2 * count

    return metadata, julia_time, julia_voltage, reference_voltage


def save_comparison(
    metadata: list[dict[str, int | float]],
    time: list[np.ndarray],
    julia_voltage: list[np.ndarray],
    reference_voltage: list[np.ndarray],
) -> Path:
    row = metadata[0]
    difference = float(np.max(np.abs(julia_voltage[0] - reference_voltage[0])))
    figure, axis = plt.subplots(figsize=(11, 5.8))
    figure.subplots_adjust(left=0.09, right=0.98, top=0.84, bottom=0.18)
    axis.plot(
        time[0],
        reference_voltage[0] * 1e3,
        color="#E69F00",
        linewidth=2.4,
        label="Python reference",
    )
    axis.plot(
        time[0],
        julia_voltage[0] * 1e3,
        color="#0072B2",
        linewidth=1.35,
        linestyle=(0, (5, 3)),
        label="Julia reader",
    )
    axis.axhline(0, color="#666666", linewidth=0.7)
    axis.grid(alpha=0.22)
    axis.set(
        title=(
            "Waveform 1: Julia reader vs Python reference\n"
            f"Channel {row['channel']} · sample rate {int(row['sample_rate_hz']) / 1e6:g} MHz "
            f"· trigger delay {row['trigger_delay_samples']} samples"
        ),
        xlabel="Trigger-relative time (µs)",
        ylabel="Voltage (mV)",
    )
    axis.legend(frameon=False)
    axis.text(
        0.015,
        0.96,
        f"max |ΔV| = {difference:.3e} V",
        transform=axis.transAxes,
        va="top",
        fontsize=10,
    )
    figure.text(
        0.5,
        0.025,
        "Fixture: 210527-CH1-15.DTA. Public fixture provenance is not identified as rail steel.",
        ha="center",
        fontsize=8.5,
        color="#555555",
    )
    output = RESULTS / "waveform_01_julia_vs_python.png"
    figure.savefig(output, dpi=300)
    plt.close(figure)
    return output


def save_overview(
    metadata: list[dict[str, int | float]],
    time: list[np.ndarray],
    julia_voltage: list[np.ndarray],
) -> Path:
    figure, axes = plt.subplots(4, 2, figsize=(12, 10), sharex=True)
    figure.subplots_adjust(
        left=0.075,
        right=0.98,
        top=0.91,
        bottom=0.12,
        hspace=0.42,
        wspace=0.16,
    )
    for axis, row, waveform_time, voltage in zip(
        axes.flat, metadata, time, julia_voltage, strict=True
    ):
        millivolts = voltage * 1e3
        axis.plot(waveform_time, millivolts, color="#0072B2", linewidth=0.9)
        axis.axhline(0, color="#666666", linewidth=0.55)
        axis.grid(alpha=0.18)
        axis.set_title(
            f"#{row['index']} · channel {row['channel']} · "
            f"record time {row['time_s']:.6f} s · peak {np.max(np.abs(millivolts)):.3g} mV",
            fontsize=9.5,
        )
    for axis in axes[-1, :]:
        axis.set_xlabel("Trigger-relative time (µs)")
    figure.supylabel("Voltage (mV)")
    figure.suptitle(
        "All 8 waveforms decoded by MistrasDTAJulia\n"
        "210527-CH1-15.DTA · 10 MHz · 3,072 samples per waveform",
        fontsize=14,
    )
    figure.text(
        0.5,
        0.018,
        "Format-level validation fixture; not evidence of steel crack detection.",
        ha="center",
        fontsize=8.5,
        color="#555555",
    )
    output = RESULTS / "all_8_waveforms.png"
    figure.savefig(output, dpi=300)
    plt.close(figure)
    return output


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    metadata, time, julia_voltage, reference_voltage = load_waveforms()
    outputs = [
        save_comparison(metadata, time, julia_voltage, reference_voltage),
        save_overview(metadata, time, julia_voltage),
    ]
    for output in outputs:
        if not output.is_file() or output.stat().st_size == 0:
            raise RuntimeError(f"figure was not written: {output}")
        print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
