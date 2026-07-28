from pathlib import Path

import pandas as pd

from compare_ct07_candidates import compare_domain


def test_symmetric_missing_extra_and_mismatch() -> None:
    reference = pd.DataFrame(
        {
            "record_index": [1, 2],
            "matrix_row": [4, 5],
            "value": [1.0, 2.0],
        }
    )
    candidate = pd.DataFrame(
        {
            "record_index": [2, 3],
            "matrix_row": [6, 7],
            "value": [20.0, 3.0],
        }
    )
    result = compare_domain(reference, candidate, ["value"])
    assert result["missing_in_candidate"] == 1
    assert result["extra_in_candidate"] == 1
    assert result["matrix_row_mismatches"] == 1
    assert result["field_mismatches"]["value"] == 1
    assert not result["passed"]


def test_reordered_records_fail() -> None:
    reference = pd.DataFrame(
        {"record_index": [1, 2], "matrix_row": [4, 5], "value": [1.0, 2.0]}
    )
    candidate = reference.iloc[::-1].reset_index(drop=True)
    result = compare_domain(reference, candidate, ["value"])
    assert not result["record_order_matches"]
    assert not result["passed"]
