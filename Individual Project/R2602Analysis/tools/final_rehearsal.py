#!/usr/bin/env python3
"""Run the bounded R260_2 analysis into a new, audited staging directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import locale
import os
import platform
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IGNORED_PARTS = {"__pycache__", ".pytest_cache"}
IGNORED_NAMES = {".DS_Store", "MANIFEST.sha256"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def files_under(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.name not in IGNORED_NAMES
        and not any(part in IGNORED_PARTS for part in path.relative_to(root).parts)
    )


def snapshot(root: Path, relative_to: Path) -> dict[str, str]:
    return {
        path.relative_to(relative_to).as_posix(): sha256(path)
        for path in files_under(root)
    }


def write_sha_manifest(path: Path, entries: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(f"{digest}  {relative}\n" for relative, digest in sorted(entries.items())),
        encoding="utf-8",
    )


def command_output(argv: list[str], cwd: Path = ROOT) -> str:
    completed = subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    return completed.stdout.strip() if completed.returncode == 0 else "not_available"


def run_stage(
    stage: str,
    argv: list[str],
    cwd: Path,
    logs: Path,
    command_log: Path,
) -> dict:
    index = len(command_log.read_text(encoding="utf-8").splitlines()) + 1
    stdout_path = logs / f"{index:02d}_{stage}.stdout.log"
    stderr_path = logs / f"{index:02d}_{stage}.stderr.log"
    started_at = utc_now()
    started = time.monotonic()
    with stdout_path.open("w", encoding="utf-8") as stdout, stderr_path.open(
        "w", encoding="utf-8"
    ) as stderr:
        completed = subprocess.run(argv, cwd=cwd, text=True, stdout=stdout, stderr=stderr)
    record = {
        "stage": stage,
        "argv": argv,
        "cwd": str(cwd),
        "start_time_utc": started_at,
        "end_time_utc": utc_now(),
        "elapsed_seconds": time.monotonic() - started,
        "stdout_path": str(stdout_path),
        "stderr_path": str(stderr_path),
        "exit_code": completed.returncode,
    }
    with command_log.open("a", encoding="utf-8") as output:
        output.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    if completed.returncode != 0:
        raise RuntimeError(f"{stage} failed with exit code {completed.returncode}")
    return record


def write_package_manifest() -> None:
    entries = {
        path.relative_to(ROOT).as_posix(): sha256(path)
        for path in files_under(ROOT)
    }
    write_sha_manifest(ROOT / "MANIFEST.sha256", entries)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workbook", type=Path, required=True)
    parser.add_argument("--staging", type=Path, required=True)
    parser.add_argument("--uv", default="uv")
    args = parser.parse_args()

    staging = args.staging.resolve()
    protected_results = (ROOT / "results").resolve()
    if staging.exists():
        parser.error(f"staging path already exists: {staging}")
    if staging == ROOT or staging == protected_results or protected_results in staging.parents:
        parser.error("staging must not be the package root or historical results directory")
    uv = shutil.which(args.uv)
    if uv is None:
        parser.error(f"uv executable not found: {args.uv}")
    if not args.workbook.is_file():
        parser.error(f"workbook not found: {args.workbook}")

    staging.mkdir(parents=True)
    logs = staging / "logs"
    outputs = staging / "outputs"
    manifests = staging / "manifests"
    logs.mkdir()
    outputs.mkdir()
    manifests.mkdir()
    command_log = staging / "commands.jsonl"
    command_log.touch()

    started_at = utc_now()
    before = snapshot(protected_results, ROOT)
    write_sha_manifest(manifests / "protected_results_before.sha256", before)

    plot_versions_raw = command_output(
        [uv, "run", str(ROOT / "tools" / "plot_s3.py"), "--versions"]
    )
    try:
        plot_versions = json.loads(plot_versions_raw)
    except json.JSONDecodeError:
        plot_versions = {"status": "not_available", "raw": plot_versions_raw}
    environment = {
        "captured_at_utc": utc_now(),
        "python": {
            "executable": sys.executable,
            "version": sys.version,
        },
        "uv": {
            "executable": uv,
            "version": command_output([uv, "--version"]),
        },
        "plot_dependencies": plot_versions,
        "os": {
            "platform": platform.platform(),
            "machine": platform.machine(),
            "locale": locale.getlocale(),
            "timezone": time.tzname,
        },
        "git": {
            "commit": command_output(["git", "rev-parse", "HEAD"], ROOT),
            "r260_status": command_output(
                ["git", "status", "--short", "--", str(ROOT.relative_to(ROOT.parents[1]))],
                ROOT.parents[1],
            ),
        },
        "external_input": {
            "path": str(args.workbook.resolve()),
            "bytes": args.workbook.stat().st_size,
            "sha256": sha256(args.workbook),
        },
    }
    (staging / "environment.json").write_text(
        json.dumps(environment, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    stages: list[dict] = []
    status = "passed"
    failure = None
    preliminary_summary = None
    try:
        stages.append(
            run_stage(
                "analyse",
                [
                    sys.executable,
                    str(ROOT / "tools" / "analyse_r260.py"),
                    str(args.workbook.resolve()),
                    "--output",
                    str(outputs),
                ],
                ROOT,
                logs,
                command_log,
            )
        )
        stages.append(
            run_stage(
                "plot",
                [
                    uv,
                    "run",
                    str(ROOT / "tools" / "plot_s3.py"),
                    "--results",
                    str(outputs),
                ],
                ROOT,
                logs,
                command_log,
            )
        )
        stages.append(
            run_stage(
                "verify_before_manifest",
                [
                    sys.executable,
                    str(ROOT / "tools" / "verify_r260.py"),
                    "--workbook",
                    str(args.workbook.resolve()),
                    "--results",
                    str(outputs),
                    "--package-root",
                    str(ROOT),
                    "--skip-package-manifest",
                ],
                ROOT,
                logs,
                command_log,
            )
        )
        preliminary_log = Path(stages[-1]["stdout_path"])
        preliminary_summary = json.loads(preliminary_log.read_text(encoding="utf-8"))
        (staging / "pre_manifest_verification_summary.json").write_text(
            json.dumps(preliminary_summary, ensure_ascii=False, indent=2, sort_keys=True)
            + "\n",
            encoding="utf-8",
        )
    except Exception as error:
        status = "failed"
        failure = f"{type(error).__name__}: {error}"

    after = snapshot(protected_results, ROOT)
    write_sha_manifest(manifests / "protected_results_after.sha256", after)
    protected_unchanged = before == after
    if not protected_unchanged:
        status = "failed"
        failure = failure or "historical results changed during the rehearsal"

    write_sha_manifest(
        manifests / "outputs.sha256",
        snapshot(outputs, staging),
    )
    summary = {
        "status": status,
        "scope": "bounded_r260_s3_processed_hit_level_rehearsal",
        "started_at_utc": started_at,
        "finished_at_utc": utc_now(),
        "staging": str(staging),
        "historical_results_unchanged": protected_unchanged,
        "stages": stages,
        "pre_manifest_verification": preliminary_summary,
        "failure": failure,
        "final_manifest_verification": (
            "run tools/verify_r260.py after this process writes MANIFEST.sha256"
        ),
    }
    (staging / "rehearsal_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    write_package_manifest()
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    raise SystemExit(0 if status == "passed" else 1)


if __name__ == "__main__":
    main()
