from __future__ import annotations

import hashlib
import importlib.util
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
VAULT = ROOT.parents[4]
RAW = ROOT / "raw" / "CT07_smop_raw.py"
NORMALIZED = ROOT / "raw" / "CT07_smop_syntax_normalized.py"
WORKBOOK = Path(
    "/Users/vangogh/Documents/毕设/初始数据&Matlab脚本/Commercial Tensile Tests.xlsx"
)
REFERENCE = VAULT / "Individual Project/temp/ct07-validation/reference"
EXPECTED_RAW_SHA256 = "f76ea90e77ec31612019d27ef5f12a6c683f12fc73bb316f0d224dee0d6d0993"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_raw_translation_failure_is_frozen() -> None:
    assert sha256(RAW) == EXPECTED_RAW_SHA256
    compiled = subprocess.run(
        [sys.executable, "-m", "py_compile", str(RAW)],
        text=True,
        capture_output=True,
    )
    assert compiled.returncode != 0
    assert "IndentationError" in compiled.stderr

    normalized = subprocess.run(
        [sys.executable, "-m", "py_compile", str(NORMALIZED)],
        text=True,
        capture_output=True,
    )
    assert normalized.returncode == 0
    imported = subprocess.run(
        [sys.executable, str(NORMALIZED)],
        text=True,
        capture_output=True,
    )
    assert imported.returncode != 0
    assert "No module named 'libsmop'" in imported.stderr
    assert sha256(RAW) == EXPECTED_RAW_SHA256


def test_ct07_runtime_primitives() -> None:
    runtime = load_module(
        "smop_runtime_primitives", ROOT / "runtime-compatible" / "libsmop.py"
    )
    runtime.configure(WORKBOOK, "CT07")
    matrix = runtime.xlsread("ignored.xlsx", "ignored")
    time = matrix(runtime.arange(), 5)
    assert len(time) == 5851
    assert time[1] == 20.3734047
    assert runtime.concat([0, 520]) == (0.0, 520.0)

    runtime.copy(runtime.figure)
    left = runtime.yyaxis("left")
    runtime.xlim((0, 250))
    right = runtime.yyaxis("right")
    assert left.get_shared_x_axes().joined(left, right)
    assert tuple(right.get_xlim()) == (0.0, 250.0)
    runtime.reset_figures()


def test_two_repair_paths_match_matlab(tmp_path: Path) -> None:
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "runtime-compatible"))
    fixed = load_module(
        "smop_script_fixed_test",
        ROOT / "script-fixed" / "CT07_smop_fixed.py",
    )
    runtime = load_module(
        "smop_runtime_runner_test",
        ROOT / "runtime-compatible" / "run_smop_ct07.py",
    )
    fixed_dir = tmp_path / "script_fixed"
    runtime_dir = tmp_path / "runtime_compatible"
    fixed_mechanical, fixed_ae = fixed.run_ct07(
        WORKBOOK, "CT07", fixed_dir
    )
    runtime_mechanical, runtime_ae = runtime.run_smop_ct07(
        NORMALIZED, WORKBOOK, "CT07", runtime_dir
    )

    assert len(fixed_mechanical) == len(runtime_mechanical) == 1807
    assert len(fixed_ae) == len(runtime_ae) == 5850
    pd.testing.assert_frame_equal(
        fixed_mechanical, runtime_mechanical, check_exact=False, rtol=1e-12, atol=1e-12
    )
    pd.testing.assert_frame_equal(
        fixed_ae, runtime_ae, check_exact=False, rtol=1e-12, atol=1e-12
    )

    comparator = load_module(
        "ct07_comparator_for_smop",
        VAULT / "Individual Project/temp/ct07-validation/compare_ct07_candidates.py",
    )
    for directory in (fixed_dir, runtime_dir):
        result = comparator.compare_candidate(REFERENCE, directory)
        assert result["fixed_run_passed"]
        assert result["mechanical"]["missing_in_candidate"] == 0
        assert result["ae"]["extra_in_candidate"] == 0
    assert sha256(RAW) == EXPECTED_RAW_SHA256


def test_comparator_rejects_deleted_added_reordered_and_shifted_rows() -> None:
    comparator = load_module(
        "ct07_comparator_mutations",
        VAULT / "Individual Project/temp/ct07-validation/compare_ct07_candidates.py",
    )
    reference = pd.DataFrame(
        {"record_index": [1, 2], "matrix_row": [4, 5], "value": [1.0, 2.0]}
    )
    deleted_added = pd.DataFrame(
        {"record_index": [2, 3], "matrix_row": [5, 6], "value": [2.0, 3.0]}
    )
    result = comparator.compare_domain(reference, deleted_added, ["value"])
    assert result["missing_in_candidate"] == 1
    assert result["extra_in_candidate"] == 1
    assert not result["passed"]

    reordered = reference.iloc[::-1].reset_index(drop=True)
    assert not comparator.compare_domain(reference, reordered, ["value"])["passed"]

    shifted = reference.copy()
    shifted["matrix_row"] += 1
    result = comparator.compare_domain(reference, shifted, ["value"])
    assert result["matrix_row_mismatches"] == 2
    assert not result["passed"]
