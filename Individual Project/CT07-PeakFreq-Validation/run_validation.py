#!/usr/bin/env python3
"""Freeze, verify or rerun the CT07–Peak_Freq validation package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
GROUPS = [f"T{index:02d}" for index in range(1, 10)]


def load_config(path: Path) -> dict:
    config = tomllib.loads(path.read_text())

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
    config["executables"] = {}
    for name, value in tomllib.loads(path.read_text())["executables"].items():
        candidate = Path(value).expanduser()
        config["executables"][name] = (
            candidate if candidate.is_absolute() else (PACKAGE / candidate).absolute()
        )
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
        writer = csv.writer(handle)
        writer.writerow(["path", "logical_role", "size_bytes", "sha256", "accessed_at"])
        writer.writerows(rows)


def package_result_files() -> list[Path]:
    return [
        path
        for path in (PACKAGE / "results").rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.name != ".DS_Store"
    ]


def build_validation_summary(config: dict) -> dict:
    ct07 = json.loads(
        (config["paths"]["ct07_results"] / "comparison_summary.json").read_text()
    )
    smop = json.loads(
        (config["paths"]["smop_results"] / "smop_comparison_summary.json").read_text()
    )
    legacy_path = (
        PACKAGE
        / "results/peak-frequency/legacy-t01-three-language/"
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
        "adaptive_top3_t01_t09": {
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
                "claim_level": "provisional_or_unresolved",
            },
            "top3": top3,
        },
    }
    (PACKAGE / "results/validation_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    return summary


def write_validation_matrix(summary: dict) -> None:
    rows = [
        [
            "Legacy Top-1",
            "MATLAB/Python/Julia full T01; 3,098 rows",
            "waveform-audited; mechanical stage unresolved unless mapping passes",
        ],
        [
            "Adaptive threshold",
            "MATLAB/Python/Julia full T01-T09",
            "waveform-audited; time alignment provisional or unresolved",
        ],
        [
            "Top-3",
            "MATLAB/Python/Julia full T01-T09",
            (
                f"{summary['scientific']['top3']['decision']}; descriptive spectral "
                "information only"
            ),
        ],
        [
            "CT07",
            "MATLAB oracle plus 8 LLM candidates; SMOP reported separately",
            "mechanical/AE summary validated; raw-waveform mapping unresolved",
        ],
    ]
    path = PACKAGE / "results/validation_matrix.csv"
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            ["workflow", "numerical_validation", "scientific_interpretation"]
        )
        writer.writerows(rows)


def freeze(config: dict) -> None:
    summary = build_validation_summary(config)
    write_validation_matrix(summary)
    manifests = PACKAGE / "manifests"
    manifests.mkdir(exist_ok=True)
    write_input_inventory(config, manifests / "input_inventory.csv")
    write_manifest(manifests / "inputs.sha256", input_files(config), None)
    write_manifest(manifests / "code.sha256", package_code_files(), PACKAGE)
    write_manifest(manifests / "results.sha256", package_result_files(), PACKAGE)
    metadata = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "python": sys.version,
        "input_file_count": len(input_files(config)),
        "code_file_count": len(package_code_files()),
        "result_file_count": len(package_result_files()),
        "frozen_totals": {
            "ct07_candidates": 8,
            "legacy_t01_rows": 3098,
            "adaptive_files": 377,
            "adaptive_events": 522216,
            "adaptive_top3_rows": 1566634,
        },
    }
    (manifests / "manifest_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n"
    )


def count_csv_rows(path: Path) -> int:
    with path.open(newline="") as handle:
        return sum(1 for _ in handle) - 1


def verify(config: dict) -> None:
    failures = []
    manifests = PACKAGE / "manifests"
    failures.extend(verify_manifest(manifests / "inputs.sha256", None))
    failures.extend(verify_manifest(manifests / "code.sha256", PACKAGE))
    failures.extend(verify_manifest(manifests / "results.sha256", PACKAGE))
    summary = json.loads((PACKAGE / "results/validation_summary.json").read_text())
    if summary["ct07"]["candidate_count"] != 8 or summary["ct07"]["passed_candidates"] != 8:
        failures.append("CT07 8/8 validation is not retained")
    if summary["ct07"]["smop"]["candidate_count"] != 2:
        failures.append("SMOP two-path summary is absent")
    if not summary["legacy_top1_t01"]["passed"]:
        failures.append("legacy T01 three-language comparison failed")
    if not summary["adaptive_top3_t01_t09"]["passed"]:
        failures.append("adaptive/Top-3 three-language comparison failed")
    event_summary = summary["scientific"]["event_catalog"]
    if event_summary["rows"] != 522_216 or event_summary["legacy_matched"] != 16_240:
        failures.append("event catalog totals changed")
    scientific = config["paths"]["scientific_results"]
    sample_count = count_csv_rows(scientific / "waveform_sample_manifest.csv")
    pngs = list((scientific / "waveform_figures").glob("*.png"))
    if sample_count < 108 or len(pngs) != sample_count:
        failures.append("waveform sample/PNG set is incomplete")
    for png in pngs:
        if png.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
            failures.append(f"invalid PNG signature: {png}")
            break
    alignment = json.loads((scientific / "alignment_summary.json").read_text())
    if len(alignment["groups"]) != 9:
        failures.append("not every T group has an alignment status")
    if any(
        row["status"] not in {"provisional_data_supported", "unresolved"}
        for row in alignment["groups"].values()
    ):
        failures.append("invalid physical mapping status")
    if summary["scientific"]["top3"]["decision"] not in {"retained", "appendix_only"}:
        failures.append("Top-3 has no binary scope decision")
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
                "adaptive_events": 522216,
                "top3_rows": 1566634,
                "waveform_samples": sample_count,
                "alignment_supported": alignment["supported_group_count"],
                "alignment_unresolved": alignment["unresolved_group_count"],
                "top3_decision": summary["scientific"]["top3"]["decision"],
            },
            indent=2,
        )
    )


def run(command: list[str], *, cwd: Path, log: Path, env: dict | None = None) -> None:
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("w") as handle:
        completed = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            text=True,
            stdout=handle,
            stderr=subprocess.STDOUT,
        )
    if completed.returncode:
        raise RuntimeError(f"command failed ({completed.returncode}); see {log}")


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


def rerun_all_numerical(config: dict) -> Path:
    """Rerun independent numerical workflows into non-overwriting staging."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    staging = PACKAGE / "staging" / f"rerun-{timestamp}"
    staging.mkdir(parents=True)
    logs = staging / "logs"
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
        "MPLCONFIGDIR": str(staging / "matplotlib-cache"),
    }

    ct07 = staging / "ct07"
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
                "MPLCONFIGDIR": str(staging / "matplotlib-cache"),
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

    for group in GROUPS:
        input_dir = waveform_root / group
        mat_files = sorted(input_dir.glob("*.mat"))
        group_out = staging / "adaptive" / group.lower()
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

    t01_files = sorted((waveform_root / "T01").glob("*.mat"))
    legacy = staging / "legacy-t01"
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
    (staging / "README.txt").write_text(
        "Numerical rerun completed in staging. Compare and freeze before replacing retained evidence.\n"
    )
    return staging


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("freeze", "verify"):
        command = subparsers.add_parser(name)
        command.add_argument("--config", type=Path, required=True)
    rerun = subparsers.add_parser("rerun")
    rerun.add_argument("--config", type=Path, required=True)
    rerun.add_argument("--stage", choices=["scientific", "all"], default="scientific")
    args = parser.parse_args()
    config = load_config(args.config)
    if args.command == "freeze":
        freeze(config)
    elif args.command == "verify":
        verify(config)
    elif args.command == "rerun":
        if args.stage == "scientific":
            rerun_scientific(config)
            freeze(config)
        else:
            staging = rerun_all_numerical(config)
            print(f"Complete numerical rerun retained at {staging}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
