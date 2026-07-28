from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image


DOMAINS = {
    "mechanical": (
        "ct07_mechanical_reference.csv",
        "mechanical.csv",
        ["t1_s", "strain_pct", "stress_mpa"],
    ),
    "ae": (
        "ct07_ae_reference.csv",
        "ae.csv",
        ["time_s", "rms_norm", "cumrms_norm", "energy_norm", "cumenergy_norm"],
    ),
}
PNG_NAMES = {
    "01_strain_stress.png",
    "02_rms.png",
    "03_cumulative_rms.png",
    "04_energy.png",
    "05_cumulative_energy.png",
}


def compare_domain(reference: pd.DataFrame, candidate: pd.DataFrame, fields: list[str]) -> dict:
    required = {"record_index", "matrix_row", *fields}
    missing_columns = sorted(required - set(candidate.columns))
    if missing_columns:
        return {"missing_columns": missing_columns, "passed": False}

    record_order_matches = (
        reference["record_index"].tolist() == candidate["record_index"].tolist()
    )
    reference = reference.set_index("record_index", drop=False)
    candidate = candidate.set_index("record_index", drop=False)
    reference_keys = set(reference.index)
    candidate_keys = set(candidate.index)
    shared = sorted(reference_keys & candidate_keys)
    field_mismatches: dict[str, int] = {}
    max_abs_error: dict[str, float] = {}
    for field in fields:
        left = reference.loc[shared, field].to_numpy(float)
        right = candidate.loc[shared, field].to_numpy(float)
        error = np.abs(left - right)
        field_mismatches[field] = int(
            np.count_nonzero(~np.isclose(left, right, rtol=1e-12, atol=1e-12, equal_nan=True))
        )
        max_abs_error[field] = float(np.nanmax(error)) if error.size else 0.0
    matrix_row_mismatches = int(
        np.count_nonzero(
            reference.loc[shared, "matrix_row"].to_numpy(int)
            != candidate.loc[shared, "matrix_row"].to_numpy(int)
        )
    )
    result = {
        "missing_in_candidate": len(reference_keys - candidate_keys),
        "extra_in_candidate": len(candidate_keys - reference_keys),
        "matrix_row_mismatches": matrix_row_mismatches,
        "record_order_matches": record_order_matches,
        "field_mismatches": field_mismatches,
        "max_abs_error": max_abs_error,
    }
    result["passed"] = (
        result["missing_in_candidate"] == 0
        and result["extra_in_candidate"] == 0
        and matrix_row_mismatches == 0
        and record_order_matches
        and all(value == 0 for value in field_mismatches.values())
    )
    return result


def compare_candidate(reference_dir: Path, candidate_dir: Path) -> dict:
    result: dict[str, object] = {"candidate_id": candidate_dir.name}
    for domain, (reference_name, candidate_name, fields) in DOMAINS.items():
        path = candidate_dir / candidate_name
        if not path.is_file():
            result[domain] = {"missing_file": candidate_name, "passed": False}
            continue
        result[domain] = compare_domain(
            pd.read_csv(reference_dir / reference_name), pd.read_csv(path), fields
        )
    pngs = {path.name for path in candidate_dir.glob("*.png") if path.stat().st_size > 0}
    parseable = {}
    for name in sorted(pngs):
        try:
            with Image.open(candidate_dir / name) as image:
                image.verify()
            parseable[name] = True
        except Exception:
            parseable[name] = False
    result["png_count"] = len(pngs)
    result["png_set_matches"] = pngs == PNG_NAMES
    result["png_parseable"] = parseable
    result["fixed_run_passed"] = (
        all(result[domain]["passed"] for domain in DOMAINS)
        and result["png_set_matches"]
        and all(parseable.values())
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("reference_dir", type=Path)
    parser.add_argument("candidates_dir", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    results = [
        compare_candidate(args.reference_dir, path)
        for path in sorted(args.candidates_dir.iterdir())
        if path.is_dir()
    ]
    summary = {
        "rtol": 1e-12,
        "atol": 1e-12,
        "candidate_count": len(results),
        "passed_candidates": sum(item["fixed_run_passed"] for item in results),
        "candidates": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 0 if results and all(item["fixed_run_passed"] for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
