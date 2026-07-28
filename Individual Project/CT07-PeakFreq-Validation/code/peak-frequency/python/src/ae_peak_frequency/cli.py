"""Command-line entry point for the Python AE prototype."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config import AnalysisConfig
from .matlab_legacy import run_matlab_legacy
from .pipeline import run_analysis


def _default_config() -> AnalysisConfig:
    return AnalysisConfig(
        sampling_rate_hz=1_000_000,
        event_window_samples=200,
        window_overlap_samples=1,
        legacy_rms_threshold=0.1,
        adaptive_sigma_multiplier=8.0,
    )


def main(argv: list[str] | None = None) -> int:
    """Run the adaptive Top-1 and Top-3 analysis for one or more MAT files."""
    parser = argparse.ArgumentParser(description="AE peak-frequency analysis prototype")
    parser.add_argument("mat_files", nargs="+", type=Path, help="MATLAB waveform files")
    parser.add_argument("--summary", type=Path, help="optional CSV or XLSX experiment summary")
    parser.add_argument("--summary-sheet", help="optional XLSX worksheet name")
    parser.add_argument(
        "--legacy-matlab-multifile",
        action="store_true",
        help="reproduce the legacy Peak_Freq.m multi-file export contract",
    )
    parser.add_argument("--output-dir", required=True, type=Path, help="directory for CSV, PNG, and JSON outputs")
    parser.add_argument("--no-plots", action="store_true", help="skip PNG output for batch validation")
    args = parser.parse_args(argv)

    if args.legacy_matlab_multifile:
        if args.summary is not None or args.summary_sheet is not None:
            parser.error("summary inputs are not used in legacy MATLAB multi-file mode")
        run_matlab_legacy(args.mat_files, output_dir=args.output_dir, config=_default_config())
    else:
        run_analysis(
            args.mat_files,
            output_dir=args.output_dir,
            config=_default_config(),
            summary_path=args.summary,
            summary_sheet=args.summary_sheet,
            write_plots=not args.no_plots,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
