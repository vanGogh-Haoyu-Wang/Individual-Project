#!/usr/bin/env python3
"""Regression checks for the CT07 candidate evidence chain."""

from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PACKAGE))

import run_validation  # noqa: E402


class CandidateEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest_path = (
            PACKAGE
            / "results/ct07/llm-validation/evidence/candidate_manifest.json"
        )
        cls.manifest = json.loads(cls.manifest_path.read_text())

    def verify_mutation(self, mutate) -> list[str]:
        manifest = copy.deepcopy(self.manifest)
        mutate(manifest)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidate_manifest.json"
            path.write_text(json.dumps(manifest))
            return run_validation.verify_ct07_candidate_evidence(PACKAGE, path)

    def test_current_package_and_tamper_detection(self) -> None:
        self.assertEqual(run_validation.verify_ct07_candidate_evidence(PACKAGE), [])

        cases = [
            (
                "wrong prompt hash",
                lambda data: data["candidates"][0]["prompt"].update({"sha256": "0" * 64}),
                "SHA-256 mismatch",
            ),
            (
                "duplicate candidate",
                lambda data: data["candidates"][0].update(
                    {"candidate_id": data["candidates"][1]["candidate_id"]}
                ),
                "fixed eight LLM IDs",
            ),
            (
                "path traversal",
                lambda data: data["candidates"][0]["prompt"].update(
                    {"path": "../README.md"}
                ),
                "escapes the package",
            ),
            (
                "missing reconstructed flag",
                lambda data: next(
                    row
                    for row in data["candidates"]
                    if row["candidate_id"] == "sonnet_python"
                )["original_generation"].update({"reconstructed_from_record": False}),
                "original-generation provenance is wrong",
            ),
            (
                "GPT filename treated as reasoning",
                lambda data: next(
                    row
                    for row in data["candidates"]
                    if row["candidate_id"] == "gpt55_python"
                ).update({"reasoning_level": "Max"}),
                "reasoning must be XHigh",
            ),
            (
                "extra normalization",
                lambda data: next(
                    row
                    for row in data["candidates"]
                    if row["candidate_id"] == "gpt55_julia"
                )["fixture_normalized_probe"]["changes"].append(
                    {"old": "plot", "new": "scatter", "count": 1}
                ),
                "normalization declaration is not fixture-only",
            ),
        ]
        for name, mutate, expected in cases:
            with self.subTest(name=name):
                self.assertTrue(
                    any(expected in failure for failure in self.verify_mutation(mutate))
                )


if __name__ == "__main__":
    unittest.main()
