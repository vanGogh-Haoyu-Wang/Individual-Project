#!/usr/bin/env python3
"""Aggregate the already-generated T01-T09 comparison summaries."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


def row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return sum(1 for _ in csv.reader(handle)) - 1


def main(root: Path) -> None:
    groups: dict[str, object] = {}
    maxima = {
        language: {
            "threshold": 0.0,
            "rms": 0.0,
            "event_time_s": 0.0,
            "frequency_khz": 0.0,
            "magnitude": 0.0,
        }
        for language in ("python", "julia")
    }
    totals = {
        "files": 0,
        "candidate_windows": 0,
        "selected_events": 0,
        "baseline_rows": 0,
        "top3_rows": 0,
    }

    for index in range(1, 10):
        name = f"t{index:02d}"
        directory = root / name
        summary = json.loads((directory / "comparison_summary.json").read_text())
        thresholds = directory / "matlab" / "thresholds.csv"
        selected = directory / "matlab" / "selected_events.csv"
        baseline = directory / "matlab" / "baseline_events.csv"
        top3 = directory / "matlab" / "top3_events.csv"

        files = row_count(thresholds)
        selected_rows = row_count(selected)
        baseline_rows = row_count(baseline)
        top3_rows = row_count(top3)
        with thresholds.open(newline="", encoding="utf-8") as handle:
            candidate_windows = sum(
                int(float(row["candidate_window_count"])) for row in csv.DictReader(handle)
            )

        group_counts = {
            "files": files,
            "candidate_windows": candidate_windows,
            "selected_events": selected_rows,
            "baseline_rows": baseline_rows,
            "top3_rows": top3_rows,
        }
        for key, value in group_counts.items():
            totals[key] += value

        groups[name.upper()] = {
            **group_counts,
            "python_passed": summary["python"]["passed"],
            "julia_passed": summary["julia"]["passed"],
            "passed": summary["passed"],
        }

        for language in ("python", "julia"):
            candidate = summary[language]
            maxima[language]["threshold"] = max(
                maxima[language]["threshold"],
                candidate["thresholds"]["max_abs_error"]["threshold"],
            )
            maxima[language]["rms"] = max(
                maxima[language]["rms"],
                candidate["selected_events"]["max_abs_error"]["rms"],
            )
            maxima[language]["event_time_s"] = max(
                maxima[language]["event_time_s"],
                candidate["selected_events"]["max_abs_error"]["event_time_s"],
                candidate["baseline_events"]["max_abs_error"]["event_time_s"],
                candidate["top3_events"]["max_abs_error"]["event_time_s"],
            )
            maxima[language]["frequency_khz"] = max(
                maxima[language]["frequency_khz"],
                candidate["baseline_events"]["max_abs_error"]["frequency_khz"],
                candidate["top3_events"]["max_abs_error"]["frequency_khz"],
            )
            maxima[language]["magnitude"] = max(
                maxima[language]["magnitude"],
                candidate["baseline_events"]["max_abs_error"]["magnitude"],
                candidate["top3_events"]["max_abs_error"]["magnitude"],
            )

    output = {
        "rtol": 1e-12,
        "atol": 1e-12,
        "totals": totals,
        "max_abs_error": maxima,
        "groups": groups,
        "all_groups_passed": all(group["passed"] for group in groups.values()),
    }
    (root / "comparison_summary.json").write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2))
    if not output["all_groups_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
