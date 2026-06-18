from pathlib import Path
import os
import subprocess


ROOT = Path(
    "/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/Tools history/"
    "Claude code Desktop Sonnet 4.6"
)
OUTPUT_DIR = ROOT / "outputs" / "02Test Outputs"
SCRIPT = ROOT / "Test2 by sonnet4.6high ae_analysis.py"
PYTHON = Path(
    "/Users/vangogh/.cache/codex-runtimes/codex-primary-runtime/"
    "dependencies/python/bin/python3"
)
EXPECTED = [
    "01_strain_vs_stress.png",
    "02_stress_normalised_rms.png",
    "03_stress_normalised_cumulative_rms.png",
    "04_stress_normalised_ae_energy.png",
    "05_stress_normalised_cumulative_ae_energy.png",
]


def test_script_generates_five_pngs() -> None:
    env = os.environ.copy()
    env["MPLBACKEND"] = "Agg"
    env["MPLCONFIGDIR"] = str(OUTPUT_DIR / ".matplotlib")
    env["PYTHONPATH"] = str(OUTPUT_DIR / ".python_packages")

    result = subprocess.run(
        [str(PYTHON), str(SCRIPT)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "UserWarning" not in result.stderr, result.stderr
    actual = sorted(path.name for path in OUTPUT_DIR.glob("*.png"))
    assert actual == EXPECTED
    for name in EXPECTED:
        path = OUTPUT_DIR / name
        assert path.stat().st_size > 10_000, f"Image is unexpectedly small: {path}"


if __name__ == "__main__":
    test_script_generates_five_pngs()
    print("PASS: script generated exactly five non-empty PNG files")
