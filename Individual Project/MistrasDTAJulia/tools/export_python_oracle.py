#!/usr/bin/env python3
"""Export the pinned MistrasDTA NPZ oracle to dependency-free test files."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import platform
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "test/data/python/210527-CH1-15.DTA"
NPZ_REFERENCE = ROOT / "test/reference/210527-CH1-15.npz"
UPSTREAM_SOURCE = ROOT / "upstream/python/MistrasDTA.py"
REFERENCE_DIR = ROOT / "test/reference"


def load_upstream():
    spec = importlib.util.spec_from_file_location("pinned_mistras_dta", UPSTREAM_SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {UPSTREAM_SOURCE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_tsv(path: Path, header: list[str], rows) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    upstream = load_upstream()
    parsed_hits, parsed_waveforms = upstream.read_bin(str(FIXTURE))
    reference = np.load(NPZ_REFERENCE, allow_pickle=False)
    reference_hits = reference["rec"]
    reference_waveforms = reference["wfm"]

    # Match the upstream regression contract: absolute TIMESTAMP is excluded.
    hit_fields = [name for name in reference_hits.dtype.names or () if name != "TIMESTAMP"]
    parsed_without_timestamp = parsed_hits[hit_fields]
    reference_without_timestamp = reference_hits[hit_fields]
    np.testing.assert_array_equal(parsed_without_timestamp, reference_without_timestamp)
    np.testing.assert_array_equal(parsed_waveforms, reference_waveforms)

    write_tsv(
        REFERENCE_DIR / "hits.tsv",
        hit_fields,
        ([row[name] for name in hit_fields] for row in reference_hits),
    )

    waveform_rows = []
    waveform_bytes = bytearray()
    value_offset = 0
    for index, row in enumerate(reference_waveforms, start=1):
        values = np.frombuffer(row["WAVEFORM"], dtype="<f8")
        waveform_rows.append(
            [
                index,
                row["SSSSSSSS.mmmuuun"],
                row["CH"],
                row["SRATE"],
                row["TDLY"],
                value_offset,
                len(values),
            ]
        )
        waveform_bytes.extend(values.astype("<f8", copy=False).tobytes())
        value_offset += len(values)

    write_tsv(
        REFERENCE_DIR / "waveforms.tsv",
        [
            "index",
            "time_s",
            "channel",
            "sample_rate_hz",
            "trigger_delay_samples",
            "value_offset",
            "sample_count",
        ],
        waveform_rows,
    )
    (REFERENCE_DIR / "waveforms.f64le").write_bytes(waveform_bytes)

    tracked = [
        FIXTURE,
        NPZ_REFERENCE,
        UPSTREAM_SOURCE,
        REFERENCE_DIR / "hits.tsv",
        REFERENCE_DIR / "waveforms.tsv",
        REFERENCE_DIR / "waveforms.f64le",
    ]
    with (REFERENCE_DIR / "reference.sha256").open("w", encoding="utf-8") as handle:
        for path in tracked:
            handle.write(f"{sha256(path)}  {path.relative_to(ROOT)}\n")

    with (REFERENCE_DIR / "oracle_environment.txt").open("w", encoding="utf-8") as handle:
        handle.write(f"python={platform.python_version()}\n")
        handle.write(f"numpy={np.__version__}\n")
        handle.write("python_upstream_commit=6c7dfb6f43f812dccff0c9219bd2c5c82bd98e85\n")
        handle.write("matlab_upstream_commit=43dd5300844f9f6d9be289a25ead319b47800041\n")
        handle.write("absolute_timestamp_excluded=true\n")

    print(f"Exported {len(reference_hits)} hits and {len(reference_waveforms)} waveforms")


if __name__ == "__main__":
    main()
