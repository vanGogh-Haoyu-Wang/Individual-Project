from __future__ import annotations

import hashlib
import os
from pathlib import Path
import subprocess
import sys
import time

from PIL import Image


OUTPUT_DIR = Path(__file__).resolve().parent
WORKSPACE = OUTPUT_DIR.parents[1]
FIXED_SCRIPT = OUTPUT_DIR / "Test2_fixed.py"
ORIGINAL_SCRIPT = WORKSPACE / "Test2 by Gemini 3.1pro high.py"
WORKBOOK = WORKSPACE / "Commercial Tensile Tests.xlsx"
ORIGINAL_SHA256 = "76c5fc095e4829f00970f6958a0d6c4d335f33714f7bdb676126948bc3d66f88"
EXPECTED = [
    "01_strain_vs_stress.png",
    "02_normalised_rms_profile.png",
    "03_normalised_cumulative_rms.png",
    "04_normalised_ae_energy.png",
    "05_normalised_cumulative_ae_energy.png",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    assert sha256(ORIGINAL_SCRIPT) == ORIGINAL_SHA256, "Original script was changed"

    started_ns = time.time_ns()
    env = os.environ.copy()
    env["MPLBACKEND"] = "Agg"
    env["MPLCONFIGDIR"] = str(OUTPUT_DIR / ".matplotlib")
    result = subprocess.run(
        [
            sys.executable,
            str(FIXED_SCRIPT),
            "--input",
            str(WORKBOOK),
            "--sheet",
            "CT07",
            "--output-dir",
            str(OUTPUT_DIR),
            "--no-show",
        ],
        cwd=OUTPUT_DIR,
        env=env,
        text=True,
        capture_output=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    actual = sorted(path.name for path in OUTPUT_DIR.glob("*.png"))
    assert actual == EXPECTED, f"Expected {EXPECTED}, got {actual}"

    for name in EXPECTED:
        path = OUTPUT_DIR / name
        assert path.stat().st_mtime_ns >= started_ns, f"Image was not regenerated: {path}"
        assert path.stat().st_size > 20_000, f"Suspiciously small image: {path}"
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            assert image.width >= 640 and image.height >= 480, (
                f"Image resolution too small: {path} -> {image.size}"
            )
            populated_bins = sum(count > 0 for count in image.convert("L").histogram())
            assert populated_bins > 16, f"Image appears blank: {path}"

    assert sha256(ORIGINAL_SCRIPT) == ORIGINAL_SHA256, "Original script changed during run"
    print("PASS: regenerated and validated exactly five PNG images; original unchanged")


if __name__ == "__main__":
    main()
