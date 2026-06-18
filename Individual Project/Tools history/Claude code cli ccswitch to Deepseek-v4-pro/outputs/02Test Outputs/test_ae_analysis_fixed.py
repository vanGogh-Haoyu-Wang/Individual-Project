import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = Path(__file__).with_name("ae_analysis_fixed.py")
WORKBOOK = ROOT / "Commercial Tensile Tests.xlsx"


class AEAnalysisIntegrationTest(unittest.TestCase):
    def test_generates_exactly_five_nonempty_pngs(self):
        with tempfile.TemporaryDirectory() as output_dir:
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--input",
                    str(WORKBOOK),
                    "--output-dir",
                    output_dir,
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            images = sorted(Path(output_dir).glob("*.png"))
            self.assertEqual(len(images), 5)
            self.assertTrue(all(image.stat().st_size > 10_000 for image in images))


if __name__ == "__main__":
    unittest.main()
