#!/usr/bin/env python3
"""Freeze, verify, rerun or rehearse the CT07–Peak_Freq validation package."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time
import tomllib
from datetime import datetime, timezone
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
GROUPS = [f"T{index:02d}" for index in range(1, 10)]
CT07_CANDIDATES = {
    f"{model}_{language}"
    for model in ("deepseek", "gemini", "gpt55", "sonnet")
    for language in ("julia", "python")
}
CT07_RECONSTRUCTED = {"gpt55_python", "sonnet_julia", "sonnet_python"}
CT07_NORMALIZED = {
    "deepseek_julia",
    "gemini_julia",
    "gpt55_julia",
    "gpt55_python",
    "sonnet_julia",
}
CT07_PNGS = {
    "01_strain_stress.png",
    "02_rms.png",
    "03_cumulative_rms.png",
    "04_energy.png",
    "05_cumulative_energy.png",
}
FROZEN_TOTALS = {
    "ct07_candidates": 8,
    "legacy_t01_rows": 3098,
    "legacy_t01_t09_logical_frames": 11_366_550,
    "adaptive_files": 377,
    "adaptive_candidate_windows": 9_472_125,
    "adaptive_selected_events": 522_216,
    "adaptive_top3_rows": 1_566_634,
}
EXECUTABLE_ENV = {
    "python": "VALIDATION_PYTHON",
    "julia": "VALIDATION_JULIA",
    "matlab": "VALIDATION_MATLAB",
}
REHEARSAL_STAGE_ORDER = (
    "ct07",
    "legacy_top1_t01",
    "adaptive_top3_t01_t09",
    "scientific",
)


def resolve_executable(
    name: str,
    configured: str,
    config_dir: Path,
    environ: dict[str, str] | None = None,
) -> Path:
    environ = os.environ if environ is None else environ
    value = environ.get(EXECUTABLE_ENV[name], configured)
    candidate = Path(value).expanduser()
    if candidate.is_absolute() or candidate.parent != Path("."):
        return candidate if candidate.is_absolute() else (config_dir / candidate).resolve()
    located = shutil.which(value, path=environ.get("PATH"))
    return Path(located) if located else candidate


def load_config(path: Path, environ: dict[str, str] | None = None) -> dict:
    config = tomllib.loads(path.read_text())
    configured_executables = config["executables"]
    config_dir = path.resolve().parent

    def resolve(value: str) -> Path:
        candidate = Path(value).expanduser()
        return candidate if candidate.is_absolute() else (PACKAGE / candidate).resolve()

    config["config_path"] = path.resolve()
    config["paths"]["waveform_root"] = Path(config["paths"]["waveform_root"])
    for name in (
        "commercial_ct07_workbook",
        "ct07_script",
        "peak_freq_script",
    ):
        config["paths"][name] = Path(config["paths"][name])
    for name in (
        "adaptive_results",
        "legacy_group_results",
        "ct07_results",
        "smop_results",
        "scientific_results",
        "mat_metadata",
    ):
        config["paths"][name] = resolve(config["paths"][name])
    config["executables"] = {
        name: resolve_executable(name, value, config_dir, environ)
        for name, value in configured_executables.items()
    }
    return config


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_manifest(path: Path, files: list[Path], relative_to: Path | None) -> None:
    rows = []
    for file in sorted(set(item.resolve() for item in files), key=str):
        label = str(file.relative_to(relative_to)) if relative_to else str(file)
        rows.append(f"{sha256(file)}  {label}\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(rows))


def read_manifest(path: Path, base: Path | None) -> list[tuple[str, Path]]:
    rows = []
    for line in path.read_text().splitlines():
        expected, label = line.split("  ", 1)
        candidate = Path(label) if base is None else base / label
        rows.append((expected, candidate))
    return rows


def verify_manifest(path: Path, base: Path | None) -> list[str]:
    failures = []
    for expected, candidate in read_manifest(path, base):
        if not candidate.is_file():
            failures.append(f"missing: {candidate}")
        elif sha256(candidate) != expected:
            failures.append(f"hash mismatch: {candidate}")
    return failures


def input_files(config: dict) -> list[Path]:
    root = config["paths"]["waveform_root"]
    files = sorted(root.glob("T0[1-9]/*.mat"))
    files += [root / group / "Tensile-processed.xlsx" for group in GROUPS]
    files += [
        config["paths"]["commercial_ct07_workbook"],
        config["paths"]["ct07_script"],
        config["paths"]["peak_freq_script"],
    ]
    if len(list(root.glob("T0[1-9]/*.mat"))) != 377:
        raise ValueError("input manifest requires exactly 377 MAT files")
    if not all(path.is_file() for path in files):
        raise ValueError("one or more frozen inputs do not exist")
    return files


def package_code_files() -> list[Path]:
    files = [
        PACKAGE / ".gitignore",
        PACKAGE / "README.md",
        PACKAGE / "validation.toml",
        PACKAGE / "run_validation.py",
    ]
    for root_name in ("code", "scientific", "environment"):
        files.extend(
            path
            for path in (PACKAGE / root_name).rglob("*")
            if path.is_file()
            and "__pycache__" not in path.parts
            and path.name not in {".DS_Store"}
            and ".pytest_cache" not in path.parts
        )
    return files


def write_input_inventory(config: dict, path: Path) -> None:
    waveform_root = config["paths"]["waveform_root"]
    accessed_at = datetime.now(timezone.utc).date().isoformat()
    rows = []
    for file in input_files(config):
        if file.suffix.lower() == ".mat":
            role = f"{file.parent.name} raw waveform"
        elif file.name == "Tensile-processed.xlsx":
            role = f"{file.parent.name} processed mechanical and AE summary"
        elif file == config["paths"]["commercial_ct07_workbook"]:
            role = "CT07 MATLAB-reference workbook"
        elif file == config["paths"]["ct07_script"]:
            role = "CT07 MATLAB source"
        else:
            role = "Peak_Freq MATLAB source"
        rows.append([str(file), role, file.stat().st_size, sha256(file), accessed_at])
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["path", "logical_role", "size_bytes", "sha256", "accessed_at"])
        writer.writerows(rows)


def canonical_results_root() -> Path:
    return PACKAGE / "results"


def manifests_root(results_root: Path) -> Path:
    results_root = results_root.resolve()
    return (
        PACKAGE / "manifests"
        if results_root == canonical_results_root().resolve()
        else results_root.parent / "manifests"
    )


def package_result_files(results_root: Path | None = None) -> list[Path]:
    results_root = (results_root or canonical_results_root()).resolve()
    return [
        path
        for path in results_root.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.name != ".DS_Store"
    ]


def build_validation_summary(
    config: dict, results_root: Path | None = None
) -> dict:
    results_root = (results_root or canonical_results_root()).resolve()
    ct07 = json.loads(
        (config["paths"]["ct07_results"] / "comparison_summary.json").read_text()
    )
    smop = json.loads(
        (config["paths"]["smop_results"] / "smop_comparison_summary.json").read_text()
    )
    legacy_path = (
        results_root
        / "peak-frequency/legacy-t01-three-language/"
        "legacy-regression-current/comparison_summary.json"
    )
    legacy = json.loads(legacy_path.read_text())
    adaptive_root = config["paths"]["adaptive_results"]
    adaptive_by_group = {}
    totals = {
        "missing_in_python": 0,
        "extra_in_python": 0,
        "missing_in_julia": 0,
        "extra_in_julia": 0,
        "python_field_mismatches": 0,
        "julia_field_mismatches": 0,
    }
    for group in GROUPS:
        summary = json.loads(
            (adaptive_root / group.lower() / "comparison_summary.json").read_text()
        )
        metrics = summary["reported_metrics"]
        adaptive_by_group[group] = {
            **metrics,
            "passed": summary["passed"],
        }
        for name in (
            "missing_in_python",
            "extra_in_python",
            "missing_in_julia",
            "extra_in_julia",
        ):
            totals[name] += int(metrics[name])
        totals["python_field_mismatches"] += sum(
            int(metrics[name])
            for name in (
                "python_threshold_mismatches",
                "python_event_field_mismatches",
                "python_peak_field_mismatches",
                "python_no_peak_status_mismatches",
            )
        )
        totals["julia_field_mismatches"] += sum(
            int(metrics[name])
            for name in (
                "julia_threshold_mismatches",
                "julia_event_field_mismatches",
                "julia_peak_field_mismatches",
                "julia_no_peak_status_mismatches",
            )
        )
    scientific_root = config["paths"]["scientific_results"]
    alignment = json.loads((scientific_root / "alignment_summary.json").read_text())
    top3 = json.loads((scientific_root / "top3_value_summary.json").read_text())
    event_catalog = json.loads(
        (scientific_root / "event_catalog_summary.json").read_text()
    )
    framing_path = (
        results_root
        / "peak-frequency/legacy-adaptive-framing/"
        "t01_t09_comparison_summary.csv"
    )
    with framing_path.open(newline="") as handle:
        framing_rows = list(csv.DictReader(handle))
    framing = next(row for row in framing_rows if row["group"] == "TOTAL")
    summary = {
        "tolerances": {
            "rtol": float(config["analysis"]["rtol"]),
            "atol": float(config["analysis"]["atol"]),
        },
        "ct07": {
            "candidate_count": ct07["candidate_count"],
            "passed_candidates": ct07["passed_candidates"],
            "candidates": {
                candidate["candidate_id"]: {
                    "missing_in_candidate": (
                        candidate["mechanical"]["missing_in_candidate"]
                        + candidate["ae"]["missing_in_candidate"]
                    ),
                    "extra_in_candidate": (
                        candidate["mechanical"]["extra_in_candidate"]
                        + candidate["ae"]["extra_in_candidate"]
                    ),
                    "field_mismatches": (
                        sum(candidate["mechanical"]["field_mismatches"].values())
                        + sum(candidate["ae"]["field_mismatches"].values())
                    ),
                    "passed": candidate["fixed_run_passed"],
                }
                for candidate in ct07["candidates"]
            },
            "smop": {
                "candidate_count": smop["candidate_count"],
                "passed_candidates": smop["passed_candidates"],
                "counted_as_llm_candidate": False,
            },
        },
        "legacy_top1_t01": {
            "dataset_scope": "complete T01",
            "matlab_rows": legacy["matlab_rows"],
            "missing_in_python": legacy["python"]["missing_in_candidate"],
            "extra_in_python": legacy["python"]["extra_in_candidate"],
            "missing_in_julia": legacy["julia"]["missing_in_candidate"],
            "extra_in_julia": legacy["julia"]["extra_in_candidate"],
            "python_field_mismatches": sum(
                legacy["python"]["field_mismatches"].values()
            ),
            "julia_field_mismatches": sum(
                legacy["julia"]["field_mismatches"].values()
            ),
            "passed": legacy["passed"],
        },
        "legacy_matlab_t01_t09_context": {
            "research_role": "MATLAB-only descriptive context",
            "dataset_scope": "T01-T09",
            "file_count": int(framing["files"]),
            "logical_frames": int(framing["legacy_logical_frames"]),
            "selected_windows": int(framing["legacy_selected_windows"]),
            "valid_top1_rows": int(framing["legacy_top1_rows"]),
            "three_language_validation": False,
        },
        "adaptive_top3_t01_t09": {
            "dataset_scope": "T01-T09",
            "file_count": int(framing["files"]),
            "candidate_windows": int(framing["adaptive_complete_windows"]),
            "selected_events": int(framing["adaptive_selected_events"]),
            "top1_rows": int(framing["adaptive_top1_rows"]),
            "top3_rows": int(framing["adaptive_top3_rows"]),
            "totals": totals,
            "groups": adaptive_by_group,
            "passed": all(row["passed"] for row in adaptive_by_group.values()),
        },
        "scientific": {
            "event_catalog": event_catalog,
            "alignment": {
                "supported_group_count": alignment["supported_group_count"],
                "unresolved_group_count": alignment["unresolved_group_count"],
                "identity_assignment_is_optimal": alignment[
                    "identity_assignment_is_optimal"
                ],
                "claim_level": alignment["claim_level"],
            },
            "top3": top3,
        },
    }
    (results_root / "validation_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    return summary


def write_validation_matrix(
    summary: dict, results_root: Path | None = None
) -> None:
    results_root = (results_root or canonical_results_root()).resolve()
    rows = [
        [
            "Legacy T01-T09 context",
            "descriptive baseline context",
            "T01-T09",
            "11,366,550 logical frames",
            "MATLAB only; not a three-language validation",
            "selection context only",
        ],
        [
            "Legacy Top-1 T01",
            "primary numerical baseline",
            "complete T01",
            "1,266,300 logical frames",
            "MATLAB/Python/Julia; 3,098 matching rows",
            "deterministic class-hidden morphology screen; mechanical mapping unresolved",
        ],
        [
            "Adaptive threshold",
            "secondary numerical extension",
            "T01-T09",
            "9,472,125 complete windows",
            "MATLAB/Python/Julia full dataset",
            "deterministic class-hidden morphology screen; 9/9 mappings unresolved",
        ],
        [
            "Top-3",
            "secondary descriptive spectral extension",
            "T01-T09",
            "522,216 selected events",
            "MATLAB/Python/Julia; 1,566,634 rows",
            (
                f"{summary['scientific']['top3']['decision']}; descriptive spectral "
                "information only; no damage classification"
            ),
        ],
        [
            "CT07",
            "LLM-assisted migration case",
            "CT07 workbook",
            "1,807 mechanical; 5,850 AE rows",
            (
                "MATLAB oracle plus 8 candidate-derived validation runners; "
                "SMOP reported separately"
            ),
            "mechanical/AE summary validated; raw-waveform mapping unresolved",
        ],
    ]
    path = results_root / "validation_matrix.csv"
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            [
                "workflow",
                "research_role",
                "dataset_scope",
                "framing_count",
                "numerical_validation",
                "scientific_interpretation",
            ]
        )
        writer.writerows(rows)


def freeze(config: dict, results_root: Path | None = None) -> None:
    results_root = (results_root or canonical_results_root()).resolve()
    summary = build_validation_summary(config, results_root)
    write_validation_matrix(summary, results_root)
    manifests = manifests_root(results_root)
    manifests.mkdir(exist_ok=True)
    write_input_inventory(config, manifests / "input_inventory.csv")
    write_manifest(manifests / "inputs.sha256", input_files(config), None)
    write_manifest(manifests / "code.sha256", package_code_files(), PACKAGE)
    write_manifest(
        manifests / "results.sha256",
        package_result_files(results_root),
        results_root.parent,
    )
    metadata = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "python": sys.version,
        "input_file_count": len(input_files(config)),
        "code_file_count": len(package_code_files()),
        "result_file_count": len(package_result_files(results_root)),
        "frozen_totals": FROZEN_TOTALS,
    }
    (manifests / "manifest_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n"
    )


def count_csv_rows(path: Path) -> int:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", newline="") as handle:
        return sum(1 for _ in handle) - 1


def validate_alignment_outputs(scientific: Path, alignment: dict) -> list[str]:
    failures = []
    groups = alignment.get("groups", {})
    if set(groups) != set(GROUPS):
        failures.append("not every T group has an alignment status")
    if (
        alignment.get("supported_group_count") != 0
        or alignment.get("unresolved_group_count") != 9
        or any(row.get("status") != "unresolved" for row in groups.values())
    ):
        failures.append("alignment must remain 0 supported and 9 unresolved")
    if alignment.get("claim_level") != "unresolved":
        failures.append("alignment claim level must be unresolved")
    if alignment.get("stage_boundaries") != {}:
        failures.append("unresolved alignment cannot contain stage boundaries")
    for name in (
        "aligned_events.csv.gz",
        "stage_event_summary.csv",
        "stage_frequency_summary.csv",
    ):
        path = scientific / name
        if not path.is_file() or count_csv_rows(path) != 0:
            failures.append(f"unresolved alignment requires an empty {name}")
    return failures


def _verified_artifact(
    package: Path, artifact: dict, label: str, failures: list[str]
) -> Path | None:
    path_value = artifact.get("path")
    expected = artifact.get("sha256")
    if not isinstance(path_value, str) or Path(path_value).is_absolute():
        failures.append(f"{label}: artifact path must be package-relative")
        return None
    path = (package / path_value).resolve()
    try:
        path.relative_to(package.resolve())
    except ValueError:
        failures.append(f"{label}: artifact path escapes the package")
        return None
    if not path.is_file():
        failures.append(f"{label}: missing artifact {path_value}")
        return None
    if (
        not isinstance(expected, str)
        or len(expected) != 64
        or any(character not in "0123456789abcdef" for character in expected)
    ):
        failures.append(f"{label}: invalid SHA-256 declaration")
    elif sha256(path) != expected:
        failures.append(f"{label}: SHA-256 mismatch")
    return path


def _verify_normalization(
    candidate_id: str,
    original: Path | None,
    normalized: Path | None,
    declaration: dict,
    failures: list[str],
) -> None:
    status = declaration.get("status")
    changes = declaration.get("changes")
    if status == "no_change_required":
        if candidate_id in CT07_NORMALIZED:
            failures.append(f"{candidate_id}: normalization unexpectedly omitted")
        if original != normalized or changes != []:
            failures.append(
                f"{candidate_id}: no-change probe must reuse the original artifact"
            )
        return
    if status != "fixture_normalized" or candidate_id not in CT07_NORMALIZED:
        failures.append(f"{candidate_id}: invalid normalization status")
        return
    if (
        declaration.get("terminal_newline_changed") is True
        and candidate_id != "gpt55_julia"
    ):
        failures.append(f"{candidate_id}: unexpected terminal-newline exception")
    expected_changes = {
        ("Tensile-processed.xlsx", "Commercial Tensile Tests.xlsx"): 1,
        ("CT-07", "CT07"): 1,
    }
    declared_changes = {}
    if isinstance(changes, list):
        for change in changes:
            if not isinstance(change, dict):
                continue
            key = (change.get("old"), change.get("new"))
            declared_changes[key] = change.get("count")
    if declared_changes != expected_changes:
        failures.append(f"{candidate_id}: normalization declaration is not fixture-only")
        return
    if not original or not normalized:
        return
    original_lines = original.read_text().splitlines(keepends=True)
    normalized_lines = normalized.read_text().splitlines(keepends=True)
    if len(original_lines) != len(normalized_lines):
        failures.append(f"{candidate_id}: normalization changed line structure")
        return
    observed = {key: 0 for key in expected_changes}
    for original_line, normalized_line in zip(original_lines, normalized_lines):
        if original_line == normalized_line:
            continue
        if (
            declaration.get("terminal_newline_changed") is True
            and original_line.rstrip("\r\n") == normalized_line.rstrip("\r\n")
        ):
            continue
        transformed = original_line
        for key in expected_changes:
            old, new = key
            count = transformed.count(old)
            if count:
                transformed = transformed.replace(old, new)
                observed[key] += count
        if transformed != normalized_line:
            failures.append(
                f"{candidate_id}: normalized probe contains a non-fixture change"
            )
            return
    if observed != expected_changes:
        failures.append(f"{candidate_id}: normalized probe did not apply both identifiers")


def verify_ct07_candidate_evidence(
    package: Path = PACKAGE, manifest_path: Path | None = None
) -> list[str]:
    failures = []
    manifest_path = manifest_path or (
        package
        / "results/ct07/llm-validation/evidence/candidate_manifest.json"
    )
    try:
        manifest = json.loads(manifest_path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        return [f"CT07 candidate manifest cannot be read: {error}"]
    candidates = manifest.get("candidates")
    if manifest.get("schema_version") != "1.0" or not isinstance(candidates, list):
        return ["CT07 candidate manifest schema is invalid"]
    identifiers = [
        candidate.get("candidate_id")
        for candidate in candidates
        if isinstance(candidate, dict)
    ]
    if (
        manifest.get("candidate_count") != 8
        or len(identifiers) != 8
        or len(set(identifiers)) != 8
        or set(identifiers) != CT07_CANDIDATES
    ):
        failures.append("CT07 candidate manifest must contain the fixed eight LLM IDs")
    if manifest.get("smop", {}).get("included_in_candidate_count") is not False:
        failures.append("SMOP must remain outside the eight LLM candidates")

    comparison_path = package / "results/ct07/llm-validation/comparison_summary.json"
    try:
        comparison = json.loads(comparison_path.read_text())
        comparison_rows = {
            row["candidate_id"]: row for row in comparison["candidates"]
        }
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        failures.append(f"CT07 comparison summary cannot be read: {error}")
        comparison = {}
        comparison_rows = {}
    if (
        comparison.get("candidate_count") != 8
        or comparison.get("passed_candidates") != 8
        or set(comparison_rows) != CT07_CANDIDATES
    ):
        failures.append("CT07 comparison summary is not the fixed 8/8 result")

    for candidate in candidates:
        if not isinstance(candidate, dict):
            failures.append("CT07 candidate manifest contains a non-object entry")
            continue
        candidate_id = candidate.get("candidate_id")
        if candidate_id not in CT07_CANDIDATES:
            continue
        for field in (
            "language",
            "model",
            "interface",
            "reasoning_level",
            "generation_date",
            "session_id",
        ):
            if not candidate.get(field):
                failures.append(f"{candidate_id}: missing generation field {field}")
        if candidate_id.startswith("gpt55_") and candidate.get("reasoning_level") != "XHigh":
            failures.append(f"{candidate_id}: GPT-5.5 reasoning must be XHigh")

        artifacts = {}
        for field in ("historical_record", "prompt", "response", "original_generation"):
            declaration = candidate.get(field)
            if not isinstance(declaration, dict):
                failures.append(f"{candidate_id}: missing {field} declaration")
                artifacts[field] = None
            else:
                artifacts[field] = _verified_artifact(
                    package, declaration, f"{candidate_id}/{field}", failures
                )
        reconstructed = candidate_id in CT07_RECONSTRUCTED
        original_declaration = candidate.get("original_generation", {})
        if (
            original_declaration.get("reconstructed_from_record") is not reconstructed
            or original_declaration.get("artifact_origin")
            != (
                "reconstructed_from_record"
                if reconstructed
                else "direct_historical_file"
            )
        ):
            failures.append(f"{candidate_id}: original-generation provenance is wrong")

        normalized_declaration = candidate.get("fixture_normalized_probe")
        if not isinstance(normalized_declaration, dict):
            failures.append(f"{candidate_id}: missing normalized-probe declaration")
            normalized_path = None
        else:
            normalized_path = _verified_artifact(
                package,
                normalized_declaration,
                f"{candidate_id}/fixture_normalized_probe",
                failures,
            )
            if normalized_declaration.get("status") == "fixture_normalized":
                diff_declaration = {
                    "path": normalized_declaration.get("diff_path"),
                    "sha256": normalized_declaration.get("diff_sha256"),
                }
                _verified_artifact(
                    package,
                    diff_declaration,
                    f"{candidate_id}/normalization_diff",
                    failures,
                )
            _verify_normalization(
                candidate_id,
                artifacts.get("original_generation"),
                normalized_path,
                normalized_declaration,
                failures,
            )

        runner_declaration = candidate.get("candidate_derived_validation_runner")
        if not isinstance(runner_declaration, dict):
            failures.append(f"{candidate_id}: missing validation-runner declaration")
        else:
            runner_path = _verified_artifact(
                package,
                runner_declaration,
                f"{candidate_id}/candidate_derived_validation_runner",
                failures,
            )
            suffix = ".py" if candidate.get("language") == "Python" else ".jl"
            expected_runner = (
                package
                / "code/ct07"
                / candidate.get("language", "").lower()
                / f"{candidate_id}{suffix}"
            ).resolve()
            if runner_path != expected_runner:
                failures.append(f"{candidate_id}: runner is not the canonical code path")
            _verified_artifact(
                package,
                {
                    "path": runner_declaration.get("run_metadata_path"),
                    "sha256": runner_declaration.get("run_metadata_sha256"),
                },
                f"{candidate_id}/run_metadata",
                failures,
            )
            if runner_declaration.get("repair_effort_quantified") is not False:
                failures.append(f"{candidate_id}: repair effort must not be inferred")

        output = package / "results/ct07/llm-validation/candidates" / candidate_id
        for filename, expected_rows in (
            ("mechanical.csv", 1807),
            ("ae.csv", 5850),
        ):
            path = output / filename
            if not path.is_file() or count_csv_rows(path) != expected_rows:
                failures.append(
                    f"{candidate_id}: {filename} does not contain {expected_rows} records"
                )
        pngs = {path.name for path in output.glob("*.png") if path.stat().st_size}
        if pngs != CT07_PNGS:
            failures.append(f"{candidate_id}: retained PNG set is incomplete")
        elif any(
            (output / name).read_bytes()[:8] != b"\x89PNG\r\n\x1a\n"
            for name in CT07_PNGS
        ):
            failures.append(f"{candidate_id}: retained PNG signature is invalid")

        comparison_row = comparison_rows.get(candidate_id)
        if not comparison_row:
            continue
        for domain in ("mechanical", "ae"):
            result = comparison_row.get(domain, {})
            if (
                result.get("missing_in_candidate") != 0
                or result.get("extra_in_candidate") != 0
                or result.get("matrix_row_mismatches") != 0
                or result.get("record_order_matches") is not True
                or any(result.get("field_mismatches", {}).values())
                or result.get("passed") is not True
            ):
                failures.append(f"{candidate_id}: {domain} comparison is not exact")
        parseable = comparison_row.get("png_parseable", {})
        if (
            comparison_row.get("png_count") != 5
            or comparison_row.get("png_set_matches") is not True
            or set(parseable) != CT07_PNGS
            or not all(parseable.values())
            or comparison_row.get("fixed_run_passed") is not True
        ):
            failures.append(f"{candidate_id}: retained comparison did not pass")
        recorded = candidate.get("matlab_comparison", {})
        if (
            recorded.get("passed") is not True
            or recorded.get("mechanical_rows") != 1807
            or recorded.get("ae_rows") != 5850
            or recorded.get("png_count") != 5
            or recorded.get("missing_in_candidate") != 0
            or recorded.get("extra_in_candidate") != 0
            or recorded.get("field_mismatches") != 0
        ):
            failures.append(f"{candidate_id}: manifest comparison result is stale")
    return failures


def verify(config: dict, results_root: Path | None = None) -> None:
    results_root = (results_root or canonical_results_root()).resolve()
    failures = []
    manifests = manifests_root(results_root)
    failures.extend(verify_manifest(manifests / "inputs.sha256", None))
    failures.extend(verify_manifest(manifests / "code.sha256", PACKAGE))
    failures.extend(
        verify_manifest(manifests / "results.sha256", results_root.parent)
    )
    metadata = json.loads((manifests / "manifest_metadata.json").read_text())
    if metadata.get("frozen_totals") != FROZEN_TOTALS:
        failures.append("manifest frozen totals changed")
    failures.extend(verify_ct07_candidate_evidence())
    summary = json.loads((results_root / "validation_summary.json").read_text())
    if summary["ct07"]["candidate_count"] != 8 or summary["ct07"]["passed_candidates"] != 8:
        failures.append("CT07 8/8 validation is not retained")
    if (
        summary["ct07"]["smop"]["candidate_count"] != 2
        or summary["ct07"]["smop"]["passed_candidates"] != 2
        or summary["ct07"]["smop"]["counted_as_llm_candidate"] is not False
    ):
        failures.append("SMOP two-path summary is absent")
    if not summary["legacy_top1_t01"]["passed"]:
        failures.append("legacy T01 three-language comparison failed")
    if not summary["adaptive_top3_t01_t09"]["passed"]:
        failures.append("adaptive/Top-3 three-language comparison failed")
    legacy_context = summary.get("legacy_matlab_t01_t09_context", {})
    if (
        legacy_context.get("file_count") != 377
        or legacy_context.get("logical_frames") != 11_366_550
        or legacy_context.get("selected_windows") != 16_240
        or legacy_context.get("valid_top1_rows") != 16_239
        or legacy_context.get("three_language_validation") is not False
    ):
        failures.append("Legacy T01-T09 MATLAB context totals or scope changed")
    adaptive = summary["adaptive_top3_t01_t09"]
    if (
        adaptive.get("file_count") != 377
        or adaptive.get("candidate_windows") != 9_472_125
        or adaptive.get("selected_events") != 522_216
        or adaptive.get("top1_rows") != 522_216
        or adaptive.get("top3_rows") != 1_566_634
    ):
        failures.append("Adaptive/Top-3 framing totals changed")
    event_summary = summary["scientific"]["event_catalog"]
    if (
        event_summary["rows"] != 522_216
        or event_summary["legacy_matched"] != 16_240
        or event_summary["valid_peak_count"] != {"1": 2, "2": 10, "3": 522_204}
    ):
        failures.append("event catalog totals changed")
    scientific = config["paths"]["scientific_results"]
    sample_count = count_csv_rows(scientific / "waveform_sample_manifest.csv")
    pngs = list((scientific / "waveform_figures").glob("*.png"))
    if sample_count != 413 or len(pngs) != sample_count:
        failures.append("waveform sample/PNG set is incomplete")
    for png in pngs:
        if png.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
            failures.append(f"invalid PNG signature: {png}")
            break
    recalculation = json.loads(
        (scientific / "waveform_recalculation_summary.json").read_text()
    )
    if (
        recalculation.get("sample_count") != 413
        or recalculation.get("rms_mismatch_count") != 0
        or recalculation.get("peak_mismatch_count") != 0
        or recalculation.get("all_png_written") is not True
    ):
        failures.append("waveform recalculation evidence changed")
    hidden_path = scientific / "waveform_morphology_screen_class_hidden.csv"
    revealed_path = scientific / "waveform_morphology_screen_class_revealed.csv"
    method_path = scientific / "waveform_morphology_screen_method.json"
    if count_csv_rows(hidden_path) != 413 or count_csv_rows(revealed_path) != 413:
        failures.append("morphology screen row count changed")
    with hidden_path.open(newline="") as handle:
        hidden_header = next(csv.reader(handle))
    if hidden_header != [
        "sample_id",
        "morphology",
        "burst_pattern",
        "screen_metrics",
        "screen_status",
    ]:
        failures.append("class-hidden morphology screen schema changed")
    method = json.loads(method_path.read_text())
    if (
        method.get("method") != "deterministic_class_hidden_morphology_screen"
        or method.get("used_matched_or_adaptive_class") is not False
        or method.get("expert_review") is not False
        or method.get("damage_ground_truth") is not False
    ):
        failures.append("morphology screen method boundary changed")
    alignment = json.loads((scientific / "alignment_summary.json").read_text())
    failures.extend(validate_alignment_outputs(scientific, alignment))
    top3 = summary["scientific"]["top3"]
    if top3.get("decision") not in {"retained", "appendix_only"}:
        failures.append("Top-3 has no binary scope decision")
    if (
        top3.get("research_role") != "secondary_descriptive_extension"
        or top3.get("decision_rule_label")
        != "pre-specified follow-on decision rule"
        or top3.get("formal_preregistration") is not False
        or top3.get("morphology_screen_complete") is not True
        or top3.get("morphology_screen_pass") is not True
        or top3.get("numerical_criteria_pass") is not True
        or top3.get("follow_on_decision_rule_pass") is not True
    ):
        failures.append("Top-3 scientific scope metadata changed")
    matrix_path = results_root / "validation_matrix.csv"
    with matrix_path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        matrix_fields = reader.fieldnames
        matrix = list(reader)
    if matrix_fields != [
        "workflow",
        "research_role",
        "dataset_scope",
        "framing_count",
        "numerical_validation",
        "scientific_interpretation",
    ] or {row["workflow"] for row in matrix} != {
        "Legacy T01-T09 context",
        "Legacy Top-1 T01",
        "Adaptive threshold",
        "Top-3",
        "CT07",
    }:
        failures.append("validation matrix scope/schema changed")
    readme = (PACKAGE / "README.md").read_text()
    for stale in (
        "/Users/vangogh/Documents/temp/",
        "/Users/vangogh/Desktop/毕设/",
    ):
        if stale in readme:
            failures.append(f"README retains stale path: {stale}")
    forbidden = [
        path
        for path in PACKAGE.rglob("*")
        if path.name in {".venv", "julia_depot", "__pycache__", ".pytest_cache", ".DS_Store"}
    ]
    if forbidden:
        failures.append(f"forbidden cache/environment paths: {forbidden[:3]}")
    if failures:
        raise SystemExit("VERIFY FAILED\n" + "\n".join(failures))
    print(
        json.dumps(
            {
                "verified": True,
                "ct07_candidates": "8/8",
                "smop_paths": "2/2",
                "legacy_t01_rows": 3098,
                "legacy_t01_t09_logical_frames": 11366550,
                "adaptive_candidate_windows": 9472125,
                "adaptive_selected_events": 522216,
                "top3_rows": 1566634,
                "waveform_samples": sample_count,
                "alignment_supported": alignment["supported_group_count"],
                "alignment_unresolved": alignment["unresolved_group_count"],
                "top3_decision": summary["scientific"]["top3"]["decision"],
            },
            indent=2,
        )
    )


def run(
    command: list[str],
    *,
    cwd: Path,
    log: Path,
    env: dict | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    log.parent.mkdir(parents=True, exist_ok=True)
    started_at = datetime.now(timezone.utc)
    started = time.monotonic()
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
    )
    ended_at = datetime.now(timezone.utc)
    prefix = log.with_suffix("")
    prefix.with_suffix(".stdout.txt").write_text(completed.stdout)
    prefix.with_suffix(".stderr.txt").write_text(completed.stderr)
    log.write_text(completed.stdout + completed.stderr)
    prefix.with_suffix(".json").write_text(
        json.dumps(
            {
                "command": command,
                "cwd": str(cwd),
                "started_at_utc": started_at.isoformat(),
                "ended_at_utc": ended_at.isoformat(),
                "duration_seconds": time.monotonic() - started,
                "exit_code": completed.returncode,
                "stdout": prefix.with_suffix(".stdout.txt").name,
                "stderr": prefix.with_suffix(".stderr.txt").name,
            },
            indent=2,
        )
        + "\n"
    )
    if check and completed.returncode:
        raise RuntimeError(f"command failed ({completed.returncode}); see {log}")
    return completed


def prepare_rehearsal_output(output: Path) -> Path:
    output = output.expanduser().resolve()
    package = PACKAGE.resolve()
    if output == package or (
        package in output.parents
        and output.relative_to(package).parts[0] != "rehearsals"
    ):
        raise ValueError(
            "rehearsal output inside the package must be under rehearsals/"
        )
    if output.exists():
        raise FileExistsError(f"rehearsal output already exists: {output}")
    output.mkdir(parents=True)
    return output


def protected_snapshot() -> dict[str, str]:
    manifests = PACKAGE / "manifests"
    snapshot = {
        f"manifest:{path.name}": sha256(path)
        for path in (
            manifests / "inputs.sha256",
            manifests / "code.sha256",
            manifests / "results.sha256",
            manifests / "manifest_metadata.json",
        )
    }
    for kind, manifest, base in (
        ("input", manifests / "inputs.sha256", None),
        ("code", manifests / "code.sha256", PACKAGE),
        ("result", manifests / "results.sha256", PACKAGE),
    ):
        for _, path in read_manifest(manifest, base):
            if not path.is_file():
                raise FileNotFoundError(f"protected artifact is missing: {path}")
            snapshot[f"{kind}:{path}"] = sha256(path)
    return dict(sorted(snapshot.items()))


def write_effective_config(
    config: dict, destination: Path, results_root: Path
) -> None:
    paths = {
        **config["paths"],
        "adaptive_results": results_root / "peak-frequency/adaptive-three-language",
        "ct07_results": results_root / "ct07/llm-validation",
        "scientific_results": results_root / "scientific",
    }

    def literal(value: object) -> str:
        if isinstance(value, Path):
            return json.dumps(str(value))
        if isinstance(value, str):
            return json.dumps(value)
        if isinstance(value, bool):
            return str(value).lower()
        if isinstance(value, list):
            return "[" + ", ".join(literal(item) for item in value) + "]"
        return str(value)

    lines = []
    for section, values in (
        ("paths", paths),
        ("executables", config["executables"]),
        ("analysis", config["analysis"]),
    ):
        lines.append(f"[{section}]")
        lines.extend(f"{name} = {literal(value)}" for name, value in values.items())
        lines.append("")
    destination.write_text("\n".join(lines))


def preflight(config: dict, rehearsal_root: Path) -> dict:
    logs = rehearsal_root / "logs/preflight"
    failures = []
    executable_checks = {}
    for name, executable in config["executables"].items():
        available = executable.is_file() and os.access(executable, os.X_OK)
        executable_checks[name] = {
            "path": str(executable),
            "available": available,
            "override": EXECUTABLE_ENV[name],
        }
        if not available:
            failures.append(f"{name} executable is unavailable: {executable}")

    try:
        inputs = input_files(config)
        input_check = {"available": True, "file_count": len(inputs)}
    except ValueError as error:
        input_check = {"available": False, "error": str(error)}
        failures.append(str(error))

    probe_env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    probes = {}
    if executable_checks["python"]["available"]:
        expected = {
            line.split("==", 1)[0]: line.split("==", 1)[1]
            for line in (PACKAGE / "environment/requirements.txt").read_text().splitlines()
            if "==" in line
        }
        python_probe = (
            "import importlib.metadata,json,sys;"
            f"expected={expected!r};"
            "actual={k:importlib.metadata.version(k) for k in expected};"
            "print(json.dumps({'python':sys.version,'packages':actual}));"
            "assert actual==expected,(actual,expected)"
        )
        completed = run(
            [str(config["executables"]["python"]), "-c", python_probe],
            cwd=PACKAGE,
            log=logs / "python-environment.log",
            env=probe_env,
            check=False,
        )
        probes["python"] = {"exit_code": completed.returncode}
        if completed.returncode:
            failures.append("Python environment probe failed")
    if executable_checks["julia"]["available"]:
        completed = run(
            [str(config["executables"]["julia"]), "--version"],
            cwd=PACKAGE,
            log=logs / "julia-version.log",
            env=probe_env,
            check=False,
        )
        probes["julia"] = {"exit_code": completed.returncode}
        if completed.returncode or "1.12.6" not in completed.stdout:
            failures.append("Julia 1.12.6 probe failed")
        for probe_name, project, expression in (
            (
                "julia_ct07",
                PACKAGE / "code/ct07/julia",
                "using CSV, DataFrames, JSON3, Plots, XLSX",
            ),
            (
                "julia_peak_frequency",
                PACKAGE / "code/peak-frequency/julia",
                "using AEPeakFrequency",
            ),
        ):
            completed = run(
                [
                    str(config["executables"]["julia"]),
                    f"--project={project}",
                    "--startup-file=no",
                    "-e",
                    expression,
                ],
                cwd=PACKAGE,
                log=logs / f"{probe_name}.log",
                env=probe_env,
                check=False,
            )
            probes[probe_name] = {"exit_code": completed.returncode}
            if completed.returncode:
                failures.append(f"{probe_name} project probe failed")
    if executable_checks["matlab"]["available"]:
        expression = (
            "fprintf('VERSION=%s\\nARCH=%s\\n',version,computer);"
            "assert(~isempty(which('findpeaks')),'findpeaks unavailable');"
            "assert(~isempty(which('buffer')),'buffer unavailable');"
        )
        completed = run(
            [str(config["executables"]["matlab"]), "-batch", expression],
            cwd=PACKAGE,
            log=logs / "matlab-environment.log",
            env=probe_env,
            check=False,
        )
        probes["matlab"] = {"exit_code": completed.returncode}
        if completed.returncode:
            failures.append("MATLAB/toolbox probe failed")

    if executable_checks["python"]["available"]:
        completed = run(
            [
                str(config["executables"]["python"]),
                str(PACKAGE / "run_validation.py"),
                "verify",
                "--config",
                str(config["config_path"]),
            ],
            cwd=PACKAGE,
            log=logs / "canonical-verify.log",
            env=probe_env,
            check=False,
        )
        probes["canonical_verify"] = {"exit_code": completed.returncode}
        if completed.returncode:
            failures.append("canonical package verification failed")

    result = {
        "passed": not failures,
        "executables": executable_checks,
        "inputs": input_check,
        "disk_free_bytes": shutil.disk_usage(rehearsal_root).free,
        "probes": probes,
        "failures": failures,
    }
    (rehearsal_root / "preflight.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    if failures:
        raise RuntimeError("preflight failed: " + "; ".join(failures))
    return result


def write_environment_record(
    config: dict, rehearsal_root: Path, preflight_result: dict
) -> None:
    record = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "orchestrator_python": sys.version,
        "executables": {
            name: {
                "path": str(path),
                "environment_override": EXECUTABLE_ENV[name],
                "override_was_set": EXECUTABLE_ENV[name] in os.environ,
            }
            for name, path in config["executables"].items()
        },
        "runtime_environment": {
            name: os.environ.get(name, "not_set")
            for name in ("JULIA_DEPOT_PATH", "MPLCONFIGDIR")
        },
        "preflight": preflight_result,
    }
    (rehearsal_root / "environment.json").write_text(
        json.dumps(record, indent=2) + "\n"
    )


def matlab_quote(path: Path) -> str:
    return str(path).replace("'", "''")


def rerun_scientific(config: dict) -> None:
    python = config["executables"]["python"]
    run(
        [
            str(python),
            str(PACKAGE / "scientific/scientific_analysis.py"),
            "all",
            "--config",
            str(config["config_path"]),
        ],
        cwd=PACKAGE,
        log=PACKAGE / "results/rerun_scientific.log",
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def rerun_all_numerical(
    config: dict,
    results_root: Path | None = None,
    logs: Path | None = None,
) -> Path:
    """Rerun independent numerical workflows into non-overwriting staging."""
    if results_root is None:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        rehearsal_root = PACKAGE / "staging" / f"rerun-{timestamp}"
        results_root = rehearsal_root / "results"
        results_root.mkdir(parents=True)
        logs = rehearsal_root / "logs"
    else:
        results_root = results_root.resolve()
        rehearsal_root = results_root.parent
        results_root.mkdir(parents=True, exist_ok=True)
        logs = logs or rehearsal_root / "logs"
    python = config["executables"]["python"]
    julia = config["executables"]["julia"]
    matlab = config["executables"]["matlab"]
    waveform_root = config["paths"]["waveform_root"]
    peak_code = PACKAGE / "code/peak-frequency"
    ct07_code = PACKAGE / "code/ct07"
    python_env = {
        **os.environ,
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONPATH": str(peak_code / "python/src"),
        "MPLCONFIGDIR": str(rehearsal_root / "matplotlib-cache"),
    }

    ct07 = results_root / "ct07/llm-validation"
    ct07_reference = ct07 / "reference"
    ct07_expression = (
        f"addpath('{matlab_quote(ct07_code / 'matlab')}');"
        f"run_ct07_reference('{matlab_quote(config['paths']['ct07_script'])}',"
        f"'{matlab_quote(config['paths']['commercial_ct07_workbook'])}',"
        f"'{matlab_quote(ct07_reference)}');"
    )
    run(
        [str(matlab), "-batch", ct07_expression],
        cwd=PACKAGE,
        log=logs / "ct07-matlab-reference.log",
    )
    candidate_root = ct07 / "candidates"
    python_candidates = [
        "deepseek_python.py",
        "gemini_python.py",
        "gpt55_python.py",
        "sonnet_python.py",
    ]
    julia_candidates = [
        "deepseek_julia.jl",
        "gemini_julia.jl",
        "gpt55_julia.jl",
        "sonnet_julia.jl",
    ]
    for script_name in python_candidates:
        candidate_id = Path(script_name).stem
        run(
            [
                str(python),
                script_name,
                str(config["paths"]["commercial_ct07_workbook"]),
                "CT07",
                str(candidate_root / candidate_id),
            ],
            cwd=ct07_code / "python",
            log=logs / f"ct07-{candidate_id}.log",
            env={
                **os.environ,
                "PYTHONDONTWRITEBYTECODE": "1",
                "MPLCONFIGDIR": str(rehearsal_root / "matplotlib-cache"),
            },
        )
    for script_name in julia_candidates:
        candidate_id = Path(script_name).stem
        run(
            [
                str(julia),
                f"--project={ct07_code / 'julia'}",
                script_name,
                str(config["paths"]["commercial_ct07_workbook"]),
                "CT07",
                str(candidate_root / candidate_id),
            ],
            cwd=ct07_code / "julia",
            log=logs / f"ct07-{candidate_id}.log",
        )
    run(
        [
            str(python),
            str(ct07_code / "compare_ct07_candidates.py"),
            str(ct07_reference),
            str(candidate_root),
            str(ct07 / "comparison_summary.json"),
        ],
        cwd=PACKAGE,
        log=logs / "ct07-compare.log",
        env=python_env,
    )

    t01_files = sorted((waveform_root / "T01").glob("*.mat"))
    legacy = (
        results_root
        / "peak-frequency/legacy-t01-three-language/legacy-regression-current"
    )
    expression = (
        f"addpath('{matlab_quote(peak_code / 'matlab')}');"
        f"run_legacy_peak_freq_export('{matlab_quote(waveform_root / 'T01')}',"
        f"'{matlab_quote(legacy / 'matlab')}',"
        f"'{matlab_quote(config['paths']['peak_freq_script'])}');"
    )
    run(
        [str(matlab), "-batch", expression],
        cwd=PACKAGE,
        log=logs / "legacy-matlab.log",
    )
    run(
        [
            str(python),
            "-m",
            "ae_peak_frequency.cli",
            *map(str, t01_files),
            "--legacy-matlab-multifile",
            "--output-dir",
            str(legacy / "python"),
            "--no-plots",
        ],
        cwd=peak_code / "python",
        log=logs / "legacy-python.log",
        env=python_env,
    )
    julia_expression = (
        "using AEPeakFrequency;"
        "c=AnalysisConfig(1000000,200,1,0.1,8.0);"
        f"run_matlab_legacy({json.dumps([str(path) for path in t01_files])},"
        f"{json.dumps(str(legacy / 'julia'))},c)"
    )
    run(
        [str(julia), f"--project={peak_code / 'julia'}", "-e", julia_expression],
        cwd=peak_code / "julia",
        log=logs / "legacy-julia.log",
    )
    run(
        [
            str(python),
            str(peak_code / "analysis/compare_legacy_top1.py"),
            str(legacy / "matlab/legacy_top1_events.csv"),
            str(legacy / "python/legacy_top1_events.csv"),
            str(legacy / "julia/legacy_top1_events.csv"),
            str(legacy / "comparison_summary.json"),
        ],
        cwd=PACKAGE,
        log=logs / "legacy-compare.log",
        env=python_env,
    )

    for group in GROUPS:
        input_dir = waveform_root / group
        mat_files = sorted(input_dir.glob("*.mat"))
        group_out = (
            results_root
            / "peak-frequency/adaptive-three-language"
            / group.lower()
        )
        expression = (
            f"addpath('{matlab_quote(peak_code / 'matlab')}');"
            f"run_adaptive_peak_freq_export('{matlab_quote(input_dir)}',"
            f"'{matlab_quote(group_out / 'matlab')}');"
        )
        run(
            [str(matlab), "-batch", expression],
            cwd=PACKAGE,
            log=logs / f"{group}-matlab-adaptive.log",
        )
        run(
            [
                str(python),
                "-m",
                "ae_peak_frequency.cli",
                *map(str, mat_files),
                "--output-dir",
                str(group_out / "python"),
                "--no-plots",
            ],
            cwd=peak_code / "python",
            log=logs / f"{group}-python-adaptive.log",
            env=python_env,
        )
        run(
            [
                str(julia),
                f"--project={peak_code / 'julia'}",
                str(peak_code / "julia/run_analysis.jl"),
                str(group_out / "julia"),
                *map(str, mat_files),
                "--no-plots",
            ],
            cwd=peak_code / "julia",
            log=logs / f"{group}-julia-adaptive.log",
        )
        run(
            [
                str(python),
                str(peak_code / "analysis/compare_adaptive_three_language.py"),
                str(group_out / "matlab"),
                str(group_out / "python"),
                str(group_out / "julia"),
                str(group_out / "comparison_summary.json"),
            ],
            cwd=PACKAGE,
            log=logs / f"{group}-adaptive-compare.log",
            env=python_env,
        )
    (rehearsal_root / "README.txt").write_text(
        "Numerical rerun completed in staging. Compare and freeze before replacing retained evidence.\n"
    )
    return rehearsal_root


def rehearse(config: dict, output: Path) -> Path:
    rehearsal_root = prepare_rehearsal_output(output)
    results_root = rehearsal_root / "results"
    logs = rehearsal_root / "logs"
    effective_config = rehearsal_root / "effective_validation.toml"
    before = protected_snapshot()
    (rehearsal_root / "protected_hashes_before.json").write_text(
        json.dumps(before, indent=2) + "\n"
    )
    status = {
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "running",
        "stage_order": list(REHEARSAL_STAGE_ORDER),
        "results_root": str(results_root),
        "effective_config": str(effective_config),
        "frozen_dependencies_reused": [
            "results/peak-frequency/legacy-matlab-t01-t09",
            "results/input/mat_metadata.csv",
            "results/ct07/smop",
            "CT07 prompt/original-generation provenance",
        ],
    }
    active_error = False
    try:
        preflight_result = preflight(config, rehearsal_root)
        write_environment_record(config, rehearsal_root, preflight_result)
        write_effective_config(config, effective_config, results_root)
        rerun_all_numerical(config, results_root, logs)
        peak_analysis = PACKAGE / "code/peak-frequency/analysis"
        command_env = {
            **os.environ,
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONPATH": str(PACKAGE / "code/peak-frequency/python/src"),
        }
        run(
            [
                str(config["executables"]["python"]),
                str(peak_analysis / "summarize_adaptive_three_language.py"),
                str(results_root / "peak-frequency/adaptive-three-language"),
            ],
            cwd=PACKAGE,
            log=logs / "adaptive-aggregate.log",
            env=command_env,
        )
        run(
            [
                str(config["executables"]["python"]),
                str(peak_analysis / "build_t01_t09_comparison.py"),
                "--config",
                str(effective_config),
            ],
            cwd=PACKAGE,
            log=logs / "legacy-adaptive-framing.log",
            env=command_env,
        )
        run(
            [
                str(config["executables"]["python"]),
                str(PACKAGE / "scientific/scientific_analysis.py"),
                "all",
                "--config",
                str(effective_config),
            ],
            cwd=PACKAGE,
            log=logs / "scientific-all.log",
            env={
                **command_env,
                "MPLCONFIGDIR": str(rehearsal_root / "matplotlib-cache"),
            },
        )
        for command in ("freeze", "verify"):
            run(
                [
                    str(config["executables"]["python"]),
                    str(PACKAGE / "run_validation.py"),
                    command,
                    "--config",
                    str(effective_config),
                    "--results-root",
                    str(results_root),
                ],
                cwd=PACKAGE,
                log=logs / f"{command}.log",
                env=command_env,
            )
        status["status"] = "passed"
    except BaseException as error:
        active_error = True
        status["status"] = "failed"
        status["error"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        after = protected_snapshot()
        changed = {
            name: {"before": before.get(name), "after": after.get(name)}
            for name in sorted(set(before) | set(after))
            if before.get(name) != after.get(name)
        }
        (rehearsal_root / "protected_hashes_after.json").write_text(
            json.dumps(after, indent=2) + "\n"
        )
        (rehearsal_root / "protected_hash_comparison.json").write_text(
            json.dumps({"passed": not changed, "changed": changed}, indent=2) + "\n"
        )
        status["protected_hashes_unchanged"] = not changed
        status["ended_at_utc"] = datetime.now(timezone.utc).isoformat()
        (rehearsal_root / "rehearsal_summary.json").write_text(
            json.dumps(status, indent=2) + "\n"
        )
        if changed and not active_error:
            raise RuntimeError("canonical protected artifacts changed during rehearsal")
    return rehearsal_root


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("freeze", "verify"):
        command = subparsers.add_parser(name)
        command.add_argument("--config", type=Path, required=True)
        command.add_argument("--results-root", type=Path)
    rerun = subparsers.add_parser("rerun")
    rerun.add_argument("--config", type=Path, required=True)
    rerun.add_argument("--stage", choices=["scientific", "all"], default="scientific")
    rehearsal = subparsers.add_parser("rehearse")
    rehearsal.add_argument("--config", type=Path, required=True)
    rehearsal.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = load_config(args.config)
    if args.command == "freeze":
        freeze(config, args.results_root)
    elif args.command == "verify":
        verify(config, args.results_root)
    elif args.command == "rerun":
        if args.stage == "scientific":
            rerun_scientific(config)
            freeze(config)
        else:
            staging = rerun_all_numerical(config)
            print(f"Complete numerical rerun retained at {staging}")
    elif args.command == "rehearse":
        output = rehearse(config, args.output)
        print(f"Complete rehearsal retained at {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
