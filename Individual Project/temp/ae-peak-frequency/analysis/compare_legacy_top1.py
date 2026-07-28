#!/usr/bin/env python3
"""Compare current Python/Julia legacy exports with the MATLAB Top-1 oracle."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd


def compare(reference: pd.DataFrame, path: Path) -> dict[str, object]:
    candidate = pd.read_csv(path)
    missing = sorted(set(reference.event_index) - set(candidate.event_index))
    extra = sorted(set(candidate.event_index) - set(reference.event_index))
    joined = reference.merge(candidate, on="event_index", suffixes=("_matlab", "_candidate"))
    fields = ("time_s", "peak_frequency_khz", "peak_magnitude")
    maxima = {
        field: float(
            np.max(
                np.abs(
                    joined[f"{field}_candidate"].to_numpy()
                    - joined[f"{field}_matlab"].to_numpy()
                )
            )
        )
        for field in fields
    }
    mismatches = {
        field: int(
            np.count_nonzero(
                ~np.isclose(
                    joined[f"{field}_candidate"],
                    joined[f"{field}_matlab"],
                    rtol=1e-12,
                    atol=1e-12,
                )
            )
        )
        for field in fields
    }
    return {
        "rows": len(candidate),
        "missing_in_candidate": len(missing),
        "extra_in_candidate": len(extra),
        "field_mismatches": mismatches,
        "max_abs_error": maxima,
        "passed": not missing and not extra and not any(mismatches.values()),
    }


def main(reference_path: Path, python_path: Path, julia_path: Path, output: Path) -> None:
    reference = pd.read_csv(reference_path)
    summary = {
        "matlab_rows": len(reference),
        "python": compare(reference, python_path),
        "julia": compare(reference, julia_path),
        "rtol": 1e-12,
        "atol": 1e-12,
    }
    summary["passed"] = summary["python"]["passed"] and summary["julia"]["passed"]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    if not summary["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main(*(Path(value) for value in sys.argv[1:5]))
