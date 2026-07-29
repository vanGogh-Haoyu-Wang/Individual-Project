#!/usr/bin/env python3
"""Independently verify the bounded R260_2 S3 evidence package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import struct
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_S3_RECORDS = 3553
IGNORED_PARTS = {"__pycache__", ".pytest_cache"}
IGNORED_NAMES = {".DS_Store", "MANIFEST.sha256"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def external_input_entry(path: Path) -> tuple[str, str]:
    entries = [
        line.split(maxsplit=1)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(entries) != 1 or len(entries[0]) != 2:
        raise ValueError("EXTERNAL_INPUTS.sha256 must contain exactly one entry")
    digest, logical_name = entries[0]
    if len(digest) != 64 or Path(logical_name).is_absolute():
        raise ValueError("invalid external-input manifest entry")
    return digest, logical_name.strip()


def package_files(root: Path) -> dict[str, Path]:
    return {
        path.relative_to(root).as_posix(): path
        for path in root.rglob("*")
        if path.is_file()
        and path.name not in IGNORED_NAMES
        and not any(part in IGNORED_PARTS for part in path.relative_to(root).parts)
    }


def verify_manifest(root: Path, manifest: Path) -> dict:
    entries: dict[str, str] = {}
    failures: list[str] = []
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, relative = line.split(maxsplit=1)
        relative = relative.strip()
        if Path(relative).is_absolute() or relative in entries:
            failures.append(f"invalid or duplicate manifest path: {relative}")
            continue
        entries[relative] = digest

    actual = package_files(root)
    missing = sorted(set(actual) - set(entries))
    extra = sorted(set(entries) - set(actual))
    mismatches = sorted(
        relative
        for relative in set(actual) & set(entries)
        if sha256(actual[relative]) != entries[relative]
    )
    failures.extend(f"missing from manifest: {path}" for path in missing)
    failures.extend(f"extra in manifest: {path}" for path in extra)
    failures.extend(f"hash mismatch: {path}" for path in mismatches)
    return {
        "status": "passed" if not failures else "failed",
        "checked_files": len(actual),
        "missing_paths": missing,
        "extra_paths": extra,
        "hash_mismatches": mismatches,
        "failures": failures,
    }


def png_metadata(path: Path) -> dict:
    header = path.read_bytes()[:24]
    valid = (
        path.stat().st_size > 24
        and header[:8] == b"\x89PNG\r\n\x1a\n"
        and header[12:16] == b"IHDR"
    )
    width, height = struct.unpack(">II", header[16:24]) if valid else (0, 0)
    return {
        "path": path.name,
        "bytes": path.stat().st_size,
        "width": width,
        "height": height,
        "valid": valid and width > 0 and height > 0,
    }


def verify(args: argparse.Namespace) -> tuple[dict, list[str]]:
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    expected_digest, logical_name = external_input_entry(args.external_inputs)
    actual_digest = sha256(args.workbook)
    check(args.workbook.name == logical_name, "workbook name differs from input manifest")
    check(actual_digest == expected_digest, "workbook SHA-256 differs from input manifest")

    analysis = json.loads((args.results / "analysis.json").read_text(encoding="utf-8"))
    s3 = analysis["sheets"]["S3"]
    hits = int(s3["message_1_count"])
    waveforms = int(s3["message_173_count"])
    pairs = int(s3["matched_173_1_pairs"])
    order_mismatches = int(s3["pair_mismatches"])
    time_bin_total = sum(int(value) for value in s3["ten_equal_time_bin_hit_counts"])

    counts = {
        "expected_hits": EXPECTED_S3_RECORDS,
        "actual_hits": hits,
        "missing_hits": max(0, EXPECTED_S3_RECORDS - hits),
        "extra_hits": max(0, hits - EXPECTED_S3_RECORDS),
        "expected_waveform_markers": EXPECTED_S3_RECORDS,
        "actual_waveform_markers": waveforms,
        "missing_waveform_markers": max(0, EXPECTED_S3_RECORDS - waveforms),
        "extra_waveform_markers": max(0, waveforms - EXPECTED_S3_RECORDS),
        "expected_pairs": EXPECTED_S3_RECORDS,
        "actual_pairs": pairs,
        "missing_pairs": max(0, EXPECTED_S3_RECORDS - pairs),
        "extra_pairs": max(0, pairs - EXPECTED_S3_RECORDS),
        "order_mismatches": order_mismatches,
    }
    check(all(counts[key] == 0 for key in (
        "missing_hits",
        "extra_hits",
        "missing_waveform_markers",
        "extra_waveform_markers",
        "missing_pairs",
        "extra_pairs",
        "order_mismatches",
    )), "S3 contains missing, extra, or out-of-order records")
    check(time_bin_total == EXPECTED_S3_RECORDS, "S3 time-bin total is not 3,553")

    with (args.results / "s3_crack_growth.tsv").open(
        encoding="utf-8", newline=""
    ) as source:
        crack_rows = list(csv.DictReader(source, delimiter="\t"))
    failure_rows = [row for row in crack_rows if row["label"] == "failure"]
    valid_rows = [
        row
        for row in crack_rows
        if row["label"] != "failure"
        and row["da_dn"]
        and float(row["da_dn"]) > 0
        and row["cycle_interval"]
        and float(row["cycle_interval"]) > 0
    ]
    failure_audit = s3["failure_row_audit"]
    correlation_rows = int(s3["exploratory_correlations"]["n_intervals"])
    invalid_failure_excluded = (
        len(failure_rows) == 1
        and failure_audit["formula_lacks_lower_bound"] is True
        and failure_audit["exclude_from_interval_analysis"] is True
        and len(valid_rows) == correlation_rows == 9
    )
    check(invalid_failure_excluded, "invalid S3 failure row was not demonstrably excluded")

    pngs = [
        png_metadata(args.results / name)
        for name in (
            "s3_hit_timing_and_pfrq.png",
            "s3_crack_growth_exploratory.png",
        )
    ]
    check(all(item["valid"] for item in pngs), "one or more S3 PNG files are invalid")

    if args.skip_package_manifest:
        package_manifest = {"status": "not_checked", "reason": "explicitly skipped"}
    else:
        package_manifest = verify_manifest(args.package_root, args.manifest)
        failures.extend(package_manifest["failures"])

    summary = {
        "status": "passed" if not failures else "failed",
        "scope": "processed_hit_level_s3_exploratory_audit",
        "input": {
            "logical_name": logical_name,
            "expected_sha256": expected_digest,
            "actual_sha256": actual_digest,
            "matched": expected_digest == actual_digest,
        },
        "s3_records": counts,
        "time_bin_total": time_bin_total,
        "invalid_failure_row_excluded": invalid_failure_excluded,
        "correlation_interval_count": correlation_rows,
        "pngs": pngs,
        "package_manifest": package_manifest,
        "failures": failures,
    }
    return summary, failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workbook", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--package-root", type=Path, default=ROOT)
    parser.add_argument(
        "--external-inputs", type=Path, default=ROOT / "EXTERNAL_INPUTS.sha256"
    )
    parser.add_argument("--manifest", type=Path, default=ROOT / "MANIFEST.sha256")
    parser.add_argument("--skip-package-manifest", action="store_true")
    args = parser.parse_args()
    try:
        summary, failures = verify(args)
    except Exception as error:
        summary = {"status": "failed", "fatal_error": f"{type(error).__name__}: {error}"}
        failures = [summary["fatal_error"]]
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
