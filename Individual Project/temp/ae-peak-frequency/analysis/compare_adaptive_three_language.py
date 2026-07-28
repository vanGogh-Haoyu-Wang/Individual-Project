from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


TABLES = {
    "thresholds": (
        ["file_name"],
        ["candidate_window_count", "selected_event_count", "threshold"],
    ),
    "selected_events": (
        ["file_name", "start_sample"],
        ["event_time_s", "rms", "threshold", "valid_peak_count"],
    ),
    "baseline_events": (
        ["file_name", "start_sample", "peak_rank"],
        ["event_time_s", "frequency_khz", "magnitude"],
    ),
    "top3_events": (
        ["file_name", "start_sample", "peak_rank"],
        ["event_time_s", "frequency_khz", "magnitude"],
    ),
}


def compare_table(reference: pd.DataFrame, candidate: pd.DataFrame, keys: list[str], fields: list[str]) -> dict:
    key_order_matches = (
        list(reference[keys].itertuples(index=False, name=None))
        == list(candidate[keys].itertuples(index=False, name=None))
    )
    reference = reference.set_index(keys).sort_index()
    candidate = candidate.set_index(keys).sort_index()
    reference_keys = set(reference.index)
    candidate_keys = set(candidate.index)
    shared = sorted(reference_keys & candidate_keys)
    mismatches: dict[str, int] = {}
    max_abs_error: dict[str, float] = {}
    for field in fields:
        left = reference.loc[shared, field].to_numpy()
        right = candidate.loc[shared, field].to_numpy()
        if np.issubdtype(np.asarray(left).dtype, np.number):
            left_float = left.astype(float)
            right_float = right.astype(float)
            error = np.abs(left_float - right_float)
            mismatches[field] = int(
                np.count_nonzero(
                    ~np.isclose(left_float, right_float, rtol=1e-12, atol=1e-12, equal_nan=True)
                )
            )
            max_abs_error[field] = float(np.nanmax(error)) if error.size else 0.0
        else:
            mismatches[field] = int(np.count_nonzero(left != right))
    return {
        "missing_in_candidate": len(reference_keys - candidate_keys),
        "extra_in_candidate": len(candidate_keys - reference_keys),
        "field_mismatches": mismatches,
        "max_abs_error": max_abs_error,
        "key_order_matches": key_order_matches,
        "passed": (
            reference_keys == candidate_keys
            and key_order_matches
            and all(value == 0 for value in mismatches.values())
        ),
    }


def compare_language(reference_dir: Path, candidate_dir: Path) -> dict:
    result = {}
    reference_thresholds = pd.read_csv(reference_dir / "thresholds.csv")
    candidate_thresholds = pd.read_csv(candidate_dir / "thresholds.csv")
    result["input_order_matches"] = (
        reference_thresholds["file_name"].tolist()
        == candidate_thresholds["file_name"].tolist()
    )
    for name, (keys, fields) in TABLES.items():
        result[name] = compare_table(
            pd.read_csv(reference_dir / f"{name}.csv"),
            pd.read_csv(candidate_dir / f"{name}.csv"),
            keys,
            fields,
        )
    top1 = pd.read_csv(candidate_dir / "baseline_events.csv")
    top3_rank1 = pd.read_csv(candidate_dir / "top3_events.csv")
    top3_rank1 = top3_rank1[top3_rank1["peak_rank"] == 1].reset_index(drop=True)
    result["top1_equals_top3_rank1"] = top1.equals(top3_rank1[top1.columns])
    reference_selected = pd.read_csv(reference_dir / "selected_events.csv")
    candidate_selected = pd.read_csv(candidate_dir / "selected_events.csv")
    reference_no_peak = set(
        map(
            tuple,
            reference_selected.loc[
                reference_selected["valid_peak_count"] == 0,
                ["file_name", "start_sample"],
            ].to_numpy(),
        )
    )
    candidate_no_peak = set(
        map(
            tuple,
            candidate_selected.loc[
                candidate_selected["valid_peak_count"] == 0,
                ["file_name", "start_sample"],
            ].to_numpy(),
        )
    )
    result["no_peak_status_mismatches"] = len(reference_no_peak ^ candidate_no_peak)
    result["missing_total"] = sum(result[name]["missing_in_candidate"] for name in TABLES)
    result["extra_total"] = sum(result[name]["extra_in_candidate"] for name in TABLES)
    result["threshold_mismatches"] = sum(result["thresholds"]["field_mismatches"].values())
    result["event_field_mismatches"] = sum(result["selected_events"]["field_mismatches"].values())
    result["peak_field_mismatches"] = sum(
        result[name]["field_mismatches"][field]
        for name in ("baseline_events", "top3_events")
        for field in ("event_time_s", "frequency_khz", "magnitude")
    )
    result["passed"] = (
        all(result[name]["passed"] for name in TABLES)
        and result["input_order_matches"]
        and result["top1_equals_top3_rank1"]
        and result["no_peak_status_mismatches"] == 0
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("matlab_dir", type=Path)
    parser.add_argument("python_dir", type=Path)
    parser.add_argument("julia_dir", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    summary = {
        "rtol": 1e-12,
        "atol": 1e-12,
        "python": compare_language(args.matlab_dir, args.python_dir),
        "julia": compare_language(args.matlab_dir, args.julia_dir),
    }
    summary["reported_metrics"] = {
        "missing_in_python": summary["python"]["missing_total"],
        "extra_in_python": summary["python"]["extra_total"],
        "missing_in_julia": summary["julia"]["missing_total"],
        "extra_in_julia": summary["julia"]["extra_total"],
        "python_threshold_mismatches": summary["python"]["threshold_mismatches"],
        "julia_threshold_mismatches": summary["julia"]["threshold_mismatches"],
        "python_event_field_mismatches": summary["python"]["event_field_mismatches"],
        "julia_event_field_mismatches": summary["julia"]["event_field_mismatches"],
        "python_peak_field_mismatches": summary["python"]["peak_field_mismatches"],
        "julia_peak_field_mismatches": summary["julia"]["peak_field_mismatches"],
        "python_no_peak_status_mismatches": summary["python"]["no_peak_status_mismatches"],
        "julia_no_peak_status_mismatches": summary["julia"]["no_peak_status_mismatches"],
    }
    summary["passed"] = summary["python"]["passed"] and summary["julia"]["passed"]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
