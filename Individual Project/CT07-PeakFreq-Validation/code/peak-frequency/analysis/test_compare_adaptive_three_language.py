import pandas as pd

from compare_adaptive_three_language import compare_table


def test_comparator_reports_missing_extra_and_value_mismatch() -> None:
    reference = pd.DataFrame(
        {"file_name": ["a", "b"], "start_sample": [0, 199], "rms": [1.0, 2.0]}
    )
    candidate = pd.DataFrame(
        {"file_name": ["b", "c"], "start_sample": [199, 398], "rms": [20.0, 3.0]}
    )
    result = compare_table(reference, candidate, ["file_name", "start_sample"], ["rms"])
    assert result["missing_in_candidate"] == 1
    assert result["extra_in_candidate"] == 1
    assert result["field_mismatches"]["rms"] == 1
    assert not result["passed"]


def test_reordered_keys_and_wrong_peak_rank_fail() -> None:
    reference = pd.DataFrame(
        {
            "file_name": ["a", "a"],
            "start_sample": [0, 0],
            "peak_rank": [1, 2],
            "magnitude": [2.0, 1.0],
        }
    )
    reordered = reference.iloc[::-1].reset_index(drop=True)
    result = compare_table(
        reference,
        reordered,
        ["file_name", "start_sample", "peak_rank"],
        ["magnitude"],
    )
    assert not result["key_order_matches"]
    assert not result["passed"]

    wrong_rank = reference.copy()
    wrong_rank.loc[1, "peak_rank"] = 3
    result = compare_table(
        reference,
        wrong_rank,
        ["file_name", "start_sample", "peak_rank"],
        ["magnitude"],
    )
    assert result["missing_in_candidate"] == 1
    assert result["extra_in_candidate"] == 1
    assert not result["passed"]
