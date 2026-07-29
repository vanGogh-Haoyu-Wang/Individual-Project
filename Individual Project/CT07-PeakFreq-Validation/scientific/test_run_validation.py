from __future__ import annotations

import gzip
import importlib.util
import json
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "run_validation.py"
SPEC = importlib.util.spec_from_file_location("run_validation", MODULE_PATH)
validation = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validation)


def write_empty_alignment_outputs(root: Path) -> None:
    with gzip.open(root / "aligned_events.csv.gz", "wt") as handle:
        handle.write("group,start_sample\n")
    (root / "stage_event_summary.csv").write_text("group,mechanical_stage\n")
    (root / "stage_frequency_summary.csv").write_text(
        "group,mechanical_stage,median_frequency_khz\n"
    )


def unresolved_alignment() -> dict:
    return {
        "groups": {group: {"status": "unresolved"} for group in validation.GROUPS},
        "supported_group_count": 0,
        "unresolved_group_count": 9,
        "claim_level": "unresolved",
        "stage_boundaries": {},
    }


def test_alignment_verifier_requires_zero_supported_and_empty_stage_outputs(
    tmp_path: Path,
) -> None:
    write_empty_alignment_outputs(tmp_path)
    alignment = unresolved_alignment()
    assert validation.validate_alignment_outputs(tmp_path, alignment) == []

    alignment["groups"]["T01"]["status"] = "provisional_data_supported"
    alignment["supported_group_count"] = 1
    alignment["unresolved_group_count"] = 8
    assert validation.validate_alignment_outputs(tmp_path, alignment)

    alignment = unresolved_alignment()
    (tmp_path / "stage_event_summary.csv").write_text(
        "group,mechanical_stage\nT01,near_peak\n"
    )
    assert validation.validate_alignment_outputs(tmp_path, alignment)


def test_executable_resolution_supports_path_lookup_and_environment_override(
    tmp_path: Path,
) -> None:
    assert validation.EXECUTABLE_ENV == {
        "python": "VALIDATION_PYTHON",
        "julia": "VALIDATION_JULIA",
        "matlab": "VALIDATION_MATLAB",
    }
    configured = tmp_path / "python3"
    override = tmp_path / "custom-python"
    for path in (configured, override):
        path.write_text("#!/bin/sh\n")
        path.chmod(0o755)
    environ = {"PATH": str(tmp_path)}
    assert validation.resolve_executable(
        "python", "python3", tmp_path, environ
    ) == configured
    environ["VALIDATION_PYTHON"] = str(override)
    assert validation.resolve_executable(
        "python", "python3", tmp_path, environ
    ) == override


def test_rehearsal_output_is_new_and_command_logs_are_auditable(
    tmp_path: Path,
) -> None:
    output = validation.prepare_rehearsal_output(tmp_path / "rehearsal")
    log = output / "logs/probe.log"
    completed = validation.run(
        [
            sys.executable,
            "-c",
            "import sys; print('out'); print('err', file=sys.stderr)",
        ],
        cwd=tmp_path,
        log=log,
    )
    assert completed.returncode == 0
    assert log.with_suffix(".stdout.txt").read_text() == "out\n"
    assert log.with_suffix(".stderr.txt").read_text() == "err\n"
    metadata = json.loads(log.with_suffix(".json").read_text())
    assert metadata["exit_code"] == 0
    assert metadata["duration_seconds"] >= 0
    with pytest.raises(FileExistsError):
        validation.prepare_rehearsal_output(output)
    with pytest.raises(ValueError):
        validation.prepare_rehearsal_output(
            validation.PACKAGE / "scientific/rehearsal-probe"
        )


def test_effective_config_points_only_fresh_outputs_to_results_root(
    tmp_path: Path,
) -> None:
    canonical_dependency = tmp_path / "canonical-legacy"
    config = {
        "paths": {
            "waveform_root": tmp_path / "waveforms",
            "commercial_ct07_workbook": tmp_path / "ct07.xlsx",
            "ct07_script": tmp_path / "CT07.m",
            "peak_freq_script": tmp_path / "Peak_Freq.m",
            "processed_workbook_pattern": "{waveform_root}/{group}/Tensile-processed.xlsx",
            "adaptive_results": tmp_path / "canonical-adaptive",
            "legacy_group_results": canonical_dependency,
            "ct07_results": tmp_path / "canonical-ct07",
            "smop_results": tmp_path / "canonical-smop",
            "scientific_results": tmp_path / "canonical-scientific",
            "mat_metadata": tmp_path / "canonical-metadata.csv",
        },
        "executables": {
            "python": Path(sys.executable),
            "julia": Path("/bin/true"),
            "matlab": Path("/bin/true"),
        },
        "analysis": {"groups": ["T01"], "rtol": 1e-12},
    }
    results = tmp_path / "fresh/results"
    destination = tmp_path / "effective.toml"
    validation.write_effective_config(config, destination, results)
    parsed = tomllib.loads(destination.read_text())
    assert parsed["paths"]["adaptive_results"] == str(
        results / "peak-frequency/adaptive-three-language"
    )
    assert parsed["paths"]["ct07_results"] == str(results / "ct07/llm-validation")
    assert parsed["paths"]["scientific_results"] == str(results / "scientific")
    assert parsed["paths"]["legacy_group_results"] == str(canonical_dependency)
    assert validation.manifests_root(results) == results.parent / "manifests"


def test_numerical_rehearsal_runs_ct07_then_legacy_then_adaptive(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    log_names = []

    def fake_run(command: list[str], *, log: Path, **kwargs: object):
        log_names.append(log.name)
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(validation, "run", fake_run)
    config = {
        "paths": {
            "waveform_root": tmp_path / "waveforms",
            "commercial_ct07_workbook": tmp_path / "ct07.xlsx",
            "ct07_script": tmp_path / "CT07.m",
            "peak_freq_script": tmp_path / "Peak_Freq.m",
        },
        "executables": {
            "python": Path("/bin/true"),
            "julia": Path("/bin/true"),
            "matlab": Path("/bin/true"),
        },
    }
    validation.rerun_all_numerical(
        config,
        tmp_path / "rehearsal/results",
        tmp_path / "rehearsal/logs",
    )
    assert log_names.index("ct07-compare.log") < log_names.index("legacy-matlab.log")
    assert log_names.index("legacy-compare.log") < log_names.index(
        "T01-matlab-adaptive.log"
    )
    assert validation.REHEARSAL_STAGE_ORDER == (
        "ct07",
        "legacy_top1_t01",
        "adaptive_top3_t01_t09",
        "scientific",
    )


def test_ct07_julia_project_declares_output_helper_dependencies() -> None:
    project = tomllib.loads(
        (MODULE_PATH.parent / "code/ct07/julia/Project.toml").read_text()
    )
    assert {"CSV", "DataFrames", "JSON3", "Plots", "XLSX"} <= set(project["deps"])
