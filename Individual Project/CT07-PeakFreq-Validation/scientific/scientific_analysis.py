#!/usr/bin/env python3
"""Result-layer scientific analysis for CT01-CT09 and Peak_Freq outputs."""

from __future__ import annotations

import argparse
import json
import math
import tomllib
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.io import loadmat
from scipy.optimize import linear_sum_assignment
from scipy.stats import rankdata, spearmanr


CATALOG_COLUMNS = [
    "group",
    "file_name",
    "file_start_time",
    "start_sample",
    "event_time_in_file_s",
    "event_time_from_group_start_s",
    "rms",
    "threshold",
    "rms_threshold_ratio",
    "legacy_matched",
    "valid_peak_count",
    "rank1_frequency_khz",
    "rank1_magnitude",
    "rank2_frequency_khz",
    "rank2_magnitude",
    "rank3_frequency_khz",
    "rank3_magnitude",
]
MORPHOLOGY_LABELS = {
    "impulsive",
    "oscillatory",
    "noise_like",
    "clipped",
    "ambiguous",
}
BURST_LABELS = {"single_burst", "repeated_or_adjacent", "uncertain"}
ACTIVITY_PAIRS = [
    ("selected_event_count", "hit_count"),
    ("burst_count", "hit_count"),
    ("waveform_rms_sum", "ct_rms_sum"),
    ("waveform_rms_median", "ct_rms_median"),
    ("waveform_rms_max", "ct_rms_max"),
    ("rank1_magnitude_sum", "energy_sum"),
]
FREQUENCY_BANDS = [-np.inf, 200.0, 250.0, 325.0, 400.0, np.inf]
FREQUENCY_LABELS = ["0-200", "200-250", "250-325", "325-400", "400-500"]


def load_config(path: Path) -> dict:
    package = path.resolve().parent
    config = tomllib.loads(path.read_text())

    def resolve(value: str) -> Path:
        candidate = Path(value).expanduser()
        return candidate if candidate.is_absolute() else (package / candidate).resolve()

    paths = config["paths"]
    resolved = {
        "package": package,
        "waveform_root": Path(paths["waveform_root"]),
        "commercial_ct07_workbook": Path(paths["commercial_ct07_workbook"]),
        "ct07_script": Path(paths["ct07_script"]),
        "peak_freq_script": Path(paths["peak_freq_script"]),
    }
    for name in (
        "adaptive_results",
        "legacy_group_results",
        "ct07_results",
        "smop_results",
        "scientific_results",
        "mat_metadata",
    ):
        resolved[name] = resolve(paths[name])
    resolved["processed_workbook_pattern"] = paths["processed_workbook_pattern"]
    config["resolved"] = resolved
    return config


def require_columns(table: pd.DataFrame, columns: list[str], source: Path) -> None:
    missing = sorted(set(columns) - set(table.columns))
    if missing:
        raise ValueError(f"{source} is missing columns: {missing}")


def parse_file_time(file_name: str) -> datetime:
    return datetime.strptime(Path(file_name).stem, "%Y%m%d_%H%M%S")


def legacy_index_to_key(
    event_index: int, files: list[str], windows_per_file: int, hop: int
) -> tuple[str, int]:
    zero_based = int(event_index) - 1
    file_index, window_index = divmod(zero_based, windows_per_file)
    if event_index < 1 or file_index >= len(files):
        raise ValueError(f"legacy event_index is outside the frozen file domain: {event_index}")
    return files[file_index], window_index * hop


def legacy_keys(config: dict, group: str) -> tuple[set[tuple[str, int]], set[tuple[str, int]]]:
    root = config["resolved"]["legacy_group_results"] / group
    metadata = json.loads((root / "legacy_run_metadata.json").read_text())
    files = [Path(path).name for path in metadata["input_files"]]
    windows_per_file = int(config["analysis"]["legacy_windows_per_file"])
    hop = int(config["analysis"]["hop_samples"])
    top1 = pd.read_csv(root / "legacy_top1_events.csv")
    indices = top1["event_index"].astype(np.int64).to_numpy()
    top1_keys = {
        legacy_index_to_key(index, files, windows_per_file, hop)
        for index in indices
    }
    mat_path = root / "legacy_peak_freq_export.mat"
    selected = loadmat(mat_path, variable_names=["event_index"], squeeze_me=True)
    all_indices = np.atleast_1d(selected["event_index"]).astype(np.int64)
    all_keys = {
        legacy_index_to_key(index, files, windows_per_file, hop)
        for index in all_indices
    }
    return top1_keys, all_keys - top1_keys


def validate_mat_metadata(config: dict) -> pd.DataFrame:
    path = config["resolved"]["mat_metadata"]
    metadata = pd.read_csv(path)
    require_columns(
        metadata,
        [
            "group",
            "file_name",
            "filename_start_time",
            "record_start_time",
            "sampling_rate_hz",
            "data_rows",
            "data_columns",
        ],
        path,
    )
    expected_rate = int(config["analysis"]["sampling_rate_hz"])
    if len(metadata) != 377:
        raise ValueError(f"expected 377 MAT metadata rows, got {len(metadata)}")
    if not (metadata["sampling_rate_hz"] == expected_rate).all():
        raise ValueError("not every MAT file uses the configured sampling rate")
    if not (metadata["data_rows"] == 5_000_000).all():
        raise ValueError("not every MAT file contains 5,000,000 waveform samples")
    if not (metadata["data_columns"] >= 1).all():
        raise ValueError("a MAT data variable has no numeric column")
    filename_times = pd.to_datetime(metadata["filename_start_time"])
    record_times = pd.to_datetime(metadata["record_start_time"], errors="coerce")
    if record_times.isna().any():
        raise ValueError("MATLAB did not export every RecordStartTime")
    delta = (record_times - filename_times).dt.total_seconds()
    if (delta.abs() >= 1.0).any():
        bad = metadata.loc[delta.abs() >= 1.0, ["group", "file_name"]]
        raise ValueError(f"filename and RecordStartTime differ by >=1 s: {bad.to_dict('records')[:3]}")
    spread = delta.groupby(metadata["group"]).agg(lambda values: values.max() - values.min())
    if (spread > 0.001).any():
        raise ValueError("RecordStartTime sub-second offset is not stable within a group")
    return metadata


def build_event_catalog(config: dict) -> pd.DataFrame:
    metadata = validate_mat_metadata(config)
    adaptive_root = config["resolved"]["adaptive_results"]
    parts: list[pd.DataFrame] = []
    no_peak_rows: list[dict[str, object]] = []
    expected_rate = float(config["analysis"]["sampling_rate_hz"])

    for group in config["analysis"]["groups"]:
        reference = adaptive_root / group.lower() / "matlab"
        selected_path = reference / "selected_events.csv"
        top3_path = reference / "top3_events.csv"
        selected = pd.read_csv(selected_path)
        top3 = pd.read_csv(top3_path)
        require_columns(
            selected,
            [
                "file_name",
                "start_sample",
                "event_time_s",
                "rms",
                "threshold",
                "valid_peak_count",
            ],
            selected_path,
        )
        require_columns(
            top3,
            ["file_name", "start_sample", "peak_rank", "frequency_khz", "magnitude"],
            top3_path,
        )
        duplicate_peaks = top3.duplicated(["file_name", "start_sample", "peak_rank"])
        if duplicate_peaks.any():
            raise ValueError(f"{group} has duplicate Top-3 keys")
        frequencies = top3.pivot(
            index=["file_name", "start_sample"],
            columns="peak_rank",
            values="frequency_khz",
        ).rename(columns=lambda rank: f"rank{int(rank)}_frequency_khz")
        magnitudes = top3.pivot(
            index=["file_name", "start_sample"],
            columns="peak_rank",
            values="magnitude",
        ).rename(columns=lambda rank: f"rank{int(rank)}_magnitude")
        merged = selected.merge(
            frequencies.join(magnitudes).reset_index(),
            on=["file_name", "start_sample"],
            how="left",
            validate="one_to_one",
            sort=False,
        )
        top1 = pd.read_csv(reference / "baseline_events.csv")
        expected_top1 = merged[
            ["file_name", "start_sample", "rank1_frequency_khz", "rank1_magnitude"]
        ].rename(
            columns={
                "rank1_frequency_khz": "frequency_khz",
                "rank1_magnitude": "magnitude",
            }
        )
        observed_top1 = top1[
            ["file_name", "start_sample", "frequency_khz", "magnitude"]
        ]
        top1_matches = (
            expected_top1[["file_name", "start_sample"]]
            .equals(observed_top1[["file_name", "start_sample"]])
            and np.array_equal(
                expected_top1[["frequency_khz", "magnitude"]].to_numpy(float),
                observed_top1[["frequency_khz", "magnitude"]].to_numpy(float),
            )
        )
        if not top1_matches:
            raise ValueError(f"{group} Top-1 is not identical to Top-3 rank 1")

        group_meta = metadata[metadata["group"] == group].copy()
        expected_files = group_meta["file_name"].tolist()
        threshold_files = pd.read_csv(reference / "thresholds.csv")["file_name"].tolist()
        if expected_files != threshold_files:
            raise ValueError(f"{group} MAT file order differs from MATLAB reference")
        time_lookup = {
            row.file_name: pd.Timestamp(row.record_start_time)
            for row in group_meta.itertuples(index=False)
        }
        first_time = min(time_lookup.values())
        legacy_with_peak, legacy_without_peak = legacy_keys(config, group)
        matched = legacy_with_peak | legacy_without_peak
        keys = list(zip(merged["file_name"], merged["start_sample"].astype(int)))
        merged["group"] = group
        merged["file_start_time"] = [
            time_lookup[name].isoformat() for name in merged["file_name"]
        ]
        merged["event_time_in_file_s"] = (
            merged["start_sample"].astype(np.float64) / expected_rate
        )
        merged["event_time_from_group_start_s"] = [
            (time_lookup[name] - first_time).total_seconds() + sample / expected_rate
            for name, sample in zip(merged["file_name"], merged["start_sample"])
        ]
        merged["rms_threshold_ratio"] = merged["rms"] / merged["threshold"]
        merged["legacy_matched"] = [key in matched for key in keys]
        for name in (
            "rank1_frequency_khz",
            "rank1_magnitude",
            "rank2_frequency_khz",
            "rank2_magnitude",
            "rank3_frequency_khz",
            "rank3_magnitude",
        ):
            if name not in merged:
                merged[name] = np.nan
        parts.append(merged[CATALOG_COLUMNS])
        no_peak_rows.extend(
            {
                "group": group,
                "file_name": file_name,
                "start_sample": start_sample,
                "reason": "legacy_selected_without_valid_peak",
            }
            for file_name, start_sample in sorted(legacy_without_peak)
        )

    catalog = pd.concat(parts, ignore_index=True)
    output = config["resolved"]["scientific_results"]
    output.mkdir(parents=True, exist_ok=True)
    catalog.to_csv(
        output / "event_catalog.csv.gz",
        index=False,
        compression="gzip",
        float_format="%.17g",
    )
    pd.DataFrame(
        no_peak_rows,
        columns=["group", "file_name", "start_sample", "reason"],
    ).to_csv(output / "legacy_no_peak_events.csv", index=False)
    summary = {
        "rows": int(len(catalog)),
        "legacy_matched": int(catalog["legacy_matched"].sum()),
        "adaptive_only": int((~catalog["legacy_matched"]).sum()),
        "valid_peak_count": {
            str(int(key)): int(value)
            for key, value in catalog["valid_peak_count"].value_counts().sort_index().items()
        },
        "classification_is_complete_and_exclusive": True,
    }
    (output / "event_catalog_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    return catalog


def cluster_bursts(catalog: pd.DataFrame, hop_factor: int, hop: int) -> pd.DataFrame:
    ordered = catalog.sort_values(["group", "file_name", "start_sample"]).copy()
    gap = ordered.groupby(["group", "file_name"])["start_sample"].diff()
    new_burst = gap.isna() | (gap > hop_factor * hop)
    ordered["burst_number"] = new_burst.groupby(
        [ordered["group"], ordered["file_name"]]
    ).cumsum()
    keys = ["group", "file_name", "burst_number"]
    representative_indices = ordered.groupby(keys, sort=False)["rms"].idxmax()
    representatives = ordered.loc[representative_indices].copy()
    counts = ordered.groupby(keys, sort=False).size().rename("burst_event_count")
    starts = ordered.groupby(keys, sort=False)["start_sample"].agg(["min", "max"])
    representatives = representatives.join(counts, on=keys).join(starts, on=keys)
    representatives = representatives.rename(
        columns={"min": "burst_start_sample", "max": "burst_end_start_sample"}
    )
    representatives["burst_hop_factor"] = hop_factor
    return representatives.reset_index(drop=True)


def build_bursts(config: dict, catalog: pd.DataFrame | None = None) -> pd.DataFrame:
    output = config["resolved"]["scientific_results"]
    if catalog is None:
        catalog = pd.read_csv(output / "event_catalog.csv.gz")
    hop = int(config["analysis"]["hop_samples"])
    summary: dict[str, object] = {"hop_samples": hop, "factors": {}}
    main = pd.DataFrame()
    for factor in (1, 2, 5):
        bursts = cluster_bursts(catalog, factor, hop)
        summary["factors"][str(factor)] = {
            "total_bursts": int(len(bursts)),
            "by_group": {
                key: int(value)
                for key, value in bursts.groupby("group").size().items()
            },
        }
        if factor == 2:
            main = bursts
    main.to_csv(
        output / "burst_catalog.csv.gz",
        index=False,
        compression="gzip",
        float_format="%.17g",
    )
    (output / "burst_sensitivity_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    return main


def deterministic_samples(config: dict, catalog: pd.DataFrame | None = None) -> pd.DataFrame:
    output = config["resolved"]["scientific_results"]
    if catalog is None:
        catalog = pd.read_csv(output / "event_catalog.csv.gz")
    selections: list[pd.DataFrame] = []
    quantiles = [("Q10", 0.10), ("Q50", 0.50), ("Q90", 0.90)]
    for group in config["analysis"]["groups"]:
        group_rows = catalog[catalog["group"] == group]
        for matched, class_name in ((True, "matched"), (False, "adaptive_only")):
            class_rows = group_rows[group_rows["legacy_matched"] == matched].copy()
            if len(class_rows) < 6:
                raise ValueError(f"{group} {class_name} has fewer than six events")
            used: set[tuple[str, int]] = set()
            for quantile_name, quantile in quantiles:
                target = class_rows["rms_threshold_ratio"].quantile(quantile)
                ranked = class_rows.assign(
                    distance=(class_rows["rms_threshold_ratio"] - target).abs()
                ).sort_values(["distance", "file_name", "start_sample"])
                chosen_indices = []
                for row in ranked.itertuples():
                    key = (row.file_name, int(row.start_sample))
                    if key not in used:
                        chosen_indices.append(row.Index)
                        used.add(key)
                    if len(chosen_indices) == 2:
                        break
                chosen = class_rows.loc[chosen_indices].copy()
                chosen["sample_reason"] = f"base_{class_name}_{quantile_name}"
                selections.append(chosen)

    base = pd.concat(selections, ignore_index=True)
    extras: list[pd.DataFrame] = []
    low_peak = catalog[catalog["valid_peak_count"] < 3].copy()
    if not low_peak.empty:
        low_peak["sample_reason"] = "valid_peak_count_lt_3"
        extras.append(low_peak)
    no_peak_path = output / "legacy_no_peak_events.csv"
    no_peak = pd.read_csv(no_peak_path)
    if not no_peak.empty:
        edge = catalog.merge(
            no_peak[["group", "file_name", "start_sample"]],
            on=["group", "file_name", "start_sample"],
            how="inner",
        )
        edge["sample_reason"] = "legacy_selected_without_valid_peak"
        extras.append(edge)
    boundary = catalog[
        (catalog["start_sample"] < 1_000)
        | (catalog["start_sample"] > 5_000_000 - 1_200)
    ].copy()
    if not boundary.empty:
        boundary["sample_reason"] = "file_boundary"
        extras.append(boundary)
    samples = pd.concat([base, *extras], ignore_index=True)
    samples = samples.drop_duplicates(
        ["group", "file_name", "start_sample"], keep="first"
    ).sort_values(["group", "file_name", "start_sample"])
    samples.insert(0, "sample_id", [f"S{index:04d}" for index in range(1, len(samples) + 1)])
    samples.to_csv(output / "waveform_sample_manifest.csv", index=False)
    blinded = pd.DataFrame(
        {
            "sample_id": samples["sample_id"],
            "morphology": "",
            "burst_pattern": "",
            "reviewer_notes": "",
            "review_status": "pending",
        }
    )
    blinded.to_csv(output / "waveform_audit_blinded.csv", index=False)
    unblinded = samples.copy()
    for column in ("morphology", "burst_pattern", "reviewer_notes"):
        unblinded[column] = ""
    unblinded["review_status"] = "pending"
    unblinded.to_csv(output / "waveform_audit_unblinded.csv", index=False)
    return samples


def render_waveform_samples(config: dict, samples: pd.DataFrame | None = None) -> dict:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    output = config["resolved"]["scientific_results"]
    if samples is None:
        samples = pd.read_csv(output / "waveform_sample_manifest.csv")
    figure_dir = output / "waveform_figures"
    figure_dir.mkdir(parents=True, exist_ok=True)
    fs = float(config["analysis"]["sampling_rate_hz"])
    window = int(config["analysis"]["window_samples"])
    hop = int(config["analysis"]["hop_samples"])
    tolerances = config["analysis"]
    checks: list[dict[str, object]] = []
    grouped = samples.groupby(["group", "file_name"], sort=True)
    for (group, file_name), rows in grouped:
        path = config["resolved"]["waveform_root"] / group / file_name
        raw = np.asarray(
            loadmat(path, variable_names=["data"])["data"][:, 0], dtype=np.float64
        )
        centred = raw - raw.mean()
        for row in rows.itertuples(index=False):
            start = int(row.start_sample)
            event = centred[start : start + window]
            rms = float(np.sqrt(np.mean(event**2)))
            rms_matches = bool(
                np.isclose(
                    rms,
                    float(row.rms),
                    rtol=float(tolerances["rtol"]),
                    atol=float(tolerances["atol"]),
                )
            )
            left = max(0, start - 1_000)
            right = min(len(centred), start + window + 1_000)
            context = centred[left:right]
            context_starts = np.arange(0, max(1, len(context) - window + 1), hop)
            context_rms = np.array(
                [
                    np.sqrt(np.mean(context[offset : offset + window] ** 2))
                    for offset in context_starts
                ]
            )
            spectrum = np.abs(np.fft.fft(event))[:101]
            frequencies = np.arange(101) * fs / window / 1_000
            peak_checks = []
            for rank in (1, 2, 3):
                frequency = getattr(row, f"rank{rank}_frequency_khz")
                magnitude = getattr(row, f"rank{rank}_magnitude")
                if pd.isna(frequency):
                    continue
                index = int(round(float(frequency) / 5.0))
                peak_checks.append(
                    bool(
                        np.isclose(
                            spectrum[index],
                            float(magnitude),
                            rtol=float(tolerances["rtol"]),
                            atol=float(tolerances["atol"]),
                        )
                    )
                )

            path_out = figure_dir / f"{row.sample_id}.png"
            if not path_out.is_file():
                figure, axes = plt.subplots(3, 1, figsize=(9, 8))
                context_time_ms = (np.arange(left, right) - start) / fs * 1_000
                axes[0].plot(context_time_ms, context, linewidth=0.7)
                axes[0].axvspan(0, window / fs * 1_000, color="tab:red", alpha=0.18)
                axes[0].set_ylabel("Centred amplitude")
                axes[0].set_title(row.sample_id)
                rms_time_ms = (left + context_starts - start) / fs * 1_000
                axes[1].plot(rms_time_ms, context_rms, marker="o", markersize=2)
                axes[1].axhline(float(row.threshold), color="tab:red", linestyle="--")
                axes[1].scatter([0], [rms], color="black", zorder=3)
                axes[1].set_ylabel("200-sample RMS")
                axes[2].plot(frequencies, spectrum, linewidth=0.8)
                for rank in (1, 2, 3):
                    frequency = getattr(row, f"rank{rank}_frequency_khz")
                    magnitude = getattr(row, f"rank{rank}_magnitude")
                    if not pd.isna(frequency):
                        axes[2].scatter([frequency], [magnitude], label=f"Rank {rank}")
                axes[2].set_xlim(0, 500)
                axes[2].set_xlabel("Frequency (kHz)")
                axes[2].set_ylabel("|FFT|")
                if int(row.valid_peak_count):
                    axes[2].legend()
                for axis in axes:
                    axis.grid(alpha=0.25)
                figure.tight_layout()
                figure.savefig(path_out, dpi=150)
                plt.close(figure)
            checks.append(
                {
                    "sample_id": row.sample_id,
                    "rms_matches": rms_matches,
                    "all_stored_peak_magnitudes_match": all(peak_checks),
                    "png": str(path_out.relative_to(output)),
                }
            )
    summary = {
        "sample_count": len(checks),
        "rms_mismatch_count": sum(not row["rms_matches"] for row in checks),
        "peak_mismatch_count": sum(
            not row["all_stored_peak_magnitudes_match"] for row in checks
        ),
        "all_png_written": len(list(figure_dir.glob("*.png"))) == len(checks),
        "checks": checks,
    }
    (output / "waveform_recalculation_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    if summary["rms_mismatch_count"] or summary["peak_mismatch_count"]:
        raise ValueError("sample waveform recomputation does not match MATLAB rows")
    return summary


def blind_signal_audit(config: dict) -> pd.DataFrame:
    """Apply a fixed signal-shape rubric without using matched/adaptive class."""
    from scipy.stats import kurtosis

    output = config["resolved"]["scientific_results"]
    samples = pd.read_csv(output / "waveform_sample_manifest.csv")
    catalog = pd.read_csv(output / "event_catalog.csv.gz")
    clustered = cluster_bursts(
        catalog, 2, int(config["analysis"]["hop_samples"])
    )
    burst_sizes = {
        (row.group, row.file_name, int(row.start_sample)): int(row.burst_event_count)
        for row in clustered.itertuples(index=False)
    }
    rows: list[dict[str, object]] = []
    root = config["resolved"]["waveform_root"]
    for (group, file_name), selected in samples.groupby(
        ["group", "file_name"], sort=True
    ):
        raw = np.asarray(
            loadmat(root / group / file_name, variable_names=["data"])["data"][:, 0],
            dtype=np.float64,
        )
        centred = raw - raw.mean()
        for row in selected.itertuples(index=False):
            event = centred[int(row.start_sample) : int(row.start_sample) + 200]
            rms = float(np.sqrt(np.mean(event**2)))
            crest = float(np.max(np.abs(event)) / rms)
            excess_kurtosis = float(kurtosis(event, fisher=True, bias=False))
            spectrum = np.abs(np.fft.fft(event))[:101]
            concentration = float(np.max(spectrum[1:100]) / np.sum(spectrum[1:100]))
            flat_fraction = float(
                max(np.mean(event == event.max()), np.mean(event == event.min()))
            )
            ratio = float(row.rms_threshold_ratio)
            if flat_fraction >= 0.05:
                morphology = "clipped"
            elif crest >= 5.0 or excess_kurtosis >= 8.0:
                morphology = "impulsive"
            elif concentration >= 0.15 and excess_kurtosis < 8.0:
                morphology = "oscillatory"
            elif ratio < 1.25 and crest < 3.5 and concentration < 0.10:
                morphology = "noise_like"
            else:
                morphology = "ambiguous"
            burst_size = burst_sizes.get(
                (group, file_name, int(row.start_sample)), 1
            )
            rows.append(
                {
                    "sample_id": row.sample_id,
                    "morphology": morphology,
                    "burst_pattern": (
                        "repeated_or_adjacent" if burst_size > 1 else "single_burst"
                    ),
                    "reviewer_notes": (
                        "deterministic_blind_signal_rubric;"
                        f"crest={crest:.6g};kurtosis={excess_kurtosis:.6g};"
                        f"spectral_concentration={concentration:.6g};"
                        f"flat_fraction={flat_fraction:.6g};burst_size={burst_size}"
                    ),
                    "review_status": "complete",
                }
            )
    audit = pd.DataFrame(rows)
    audit.to_csv(output / "waveform_audit_blinded.csv", index=False)
    (output / "waveform_audit_method.json").write_text(
        json.dumps(
            {
                "method": "deterministic_blind_signal_rubric",
                "used_matched_or_adaptive_class": False,
                "damage_ground_truth": False,
                "thresholds": {
                    "clipped": "flat_fraction >= 0.05",
                    "impulsive": "crest >= 5 or excess_kurtosis >= 8",
                    "oscillatory": "spectral_concentration >= 0.15 and kurtosis < 8",
                    "noise_like": "rms/threshold < 1.25, crest < 3.5 and concentration < 0.10",
                    "otherwise": "ambiguous",
                },
            },
            indent=2,
        )
        + "\n"
    )
    return audit


def unblind(config: dict) -> pd.DataFrame:
    output = config["resolved"]["scientific_results"]
    manifest = pd.read_csv(output / "waveform_sample_manifest.csv")
    blinded = pd.read_csv(output / "waveform_audit_blinded.csv", keep_default_na=False)
    require_columns(
        blinded,
        ["sample_id", "morphology", "burst_pattern", "reviewer_notes", "review_status"],
        output / "waveform_audit_blinded.csv",
    )
    invalid_morphology = set(blinded["morphology"]) - MORPHOLOGY_LABELS - {""}
    invalid_burst = set(blinded["burst_pattern"]) - BURST_LABELS - {""}
    if invalid_morphology or invalid_burst:
        raise ValueError(
            f"invalid audit labels: morphology={invalid_morphology}, burst={invalid_burst}"
        )
    merged = manifest.merge(blinded, on="sample_id", how="left", validate="one_to_one")
    merged.to_csv(output / "waveform_audit_unblinded.csv", index=False)
    return merged


def extract_ct_context(config: dict) -> dict[str, tuple[pd.DataFrame, pd.DataFrame]]:
    output = config["resolved"]["scientific_results"] / "ct_context"
    output.mkdir(parents=True, exist_ok=True)
    contexts: dict[str, tuple[pd.DataFrame, pd.DataFrame]] = {}
    pattern = config["resolved"]["processed_workbook_pattern"]
    waveform_root = str(config["resolved"]["waveform_root"])
    for group in config["analysis"]["groups"]:
        workbook = Path(pattern.format(waveform_root=waveform_root, group=group))
        sheet = f"CT-{group[1:]}"
        raw = pd.read_excel(workbook, sheet_name=sheet, header=None)
        mechanical_values = raw.iloc[:, [0, 1, 2, 3, 4]].apply(
            pd.to_numeric, errors="coerce"
        )
        mechanical = mechanical_values[
            mechanical_values.notna().all(axis=1)
        ].copy()
        mechanical.columns = [
            "test_time_s",
            "nominal_displacement_mm",
            "strain_pct",
            "force_n",
            "stress_mpa",
        ]
        ae_values = raw.iloc[:, [6, 15, 12, 22]].apply(
            pd.to_numeric, errors="coerce"
        )
        ae = ae_values[ae_values.notna().all(axis=1)].copy()
        ae.columns = ["ae_time_s", "rms", "energy", "cumulative_energy"]
        ae["cumulative_rms"] = ae["rms"].cumsum()
        mechanical.to_csv(output / f"{group}_mechanical.csv", index=False)
        ae.to_csv(output / f"{group}_ae.csv", index=False)
        contexts[group] = (mechanical.reset_index(drop=True), ae.reset_index(drop=True))
    validate_ct07_bridge(config, *contexts["T07"])
    return contexts


def validate_ct07_bridge(
    config: dict, mechanical: pd.DataFrame, ae: pd.DataFrame
) -> dict:
    reference = config["resolved"]["ct07_results"] / "reference"
    mechanical_reference = pd.read_csv(reference / "ct07_mechanical_reference.csv")
    ae_reference = pd.read_csv(reference / "ct07_ae_reference.csv")
    rtol = float(config["analysis"]["rtol"])
    atol = float(config["analysis"]["atol"])
    mechanical_ok = (
        len(mechanical) == len(mechanical_reference)
        and np.allclose(
            mechanical[["test_time_s", "strain_pct", "stress_mpa"]].to_numpy(),
            mechanical_reference[["t1_s", "strain_pct", "stress_mpa"]].to_numpy(),
            rtol=rtol,
            atol=atol,
        )
    )
    rms = ae["rms"].to_numpy()
    energy = ae["energy"].to_numpy()
    cumulative_energy = ae["cumulative_energy"].to_numpy()
    derived = np.column_stack(
        [
            ae["ae_time_s"].to_numpy(),
            rms / np.nanmax(rms),
            np.cumsum(rms) / np.nansum(rms),
            energy / np.nanmax(energy),
            cumulative_energy / np.nanmax(cumulative_energy),
        ]
    )
    ae_ok = len(ae) == len(ae_reference) and np.allclose(
        derived,
        ae_reference[
            ["time_s", "rms_norm", "cumrms_norm", "energy_norm", "cumenergy_norm"]
        ].to_numpy(),
        rtol=rtol,
        atol=atol,
    )
    result = {
        "mechanical_rows": int(len(mechanical)),
        "ae_rows": int(len(ae)),
        "mechanical_matches_matlab_oracle": bool(mechanical_ok),
        "ae_matches_matlab_oracle": bool(ae_ok),
        "proves_waveform_specimen_mapping": False,
    }
    path = config["resolved"]["scientific_results"] / "ct07_bridge_summary.json"
    path.write_text(json.dumps(result, indent=2) + "\n")
    if not mechanical_ok or not ae_ok:
        raise ValueError("Tensile-processed CT-07 does not match the CT07 MATLAB oracle")
    return result


def _bin_values(
    times: pd.Series, values: dict[str, pd.Series], width: float, end: float
) -> pd.DataFrame:
    count = int(math.floor(end / width)) + 1
    bins = np.arange(count)
    source = pd.DataFrame({"bin": np.floor(times / width).astype(int), **values})
    aggregations: dict[str, object] = {}
    for name in values:
        if name.endswith("_count"):
            aggregations[name] = "sum"
        elif name.endswith("_median"):
            aggregations[name] = "median"
        elif name.endswith("_max"):
            aggregations[name] = "max"
        else:
            aggregations[name] = "sum"
    result = source.groupby("bin").agg(aggregations).reindex(bins).fillna(0.0)
    result.index.name = "bin"
    return result


def waveform_bins(
    catalog: pd.DataFrame, bursts: pd.DataFrame, group: str, width: float
) -> pd.DataFrame:
    rows = catalog[catalog["group"] == group].copy()
    burst_rows = bursts[bursts["group"] == group]
    end = max(rows["event_time_from_group_start_s"].max(), 0.0) + 5.0
    source = pd.DataFrame(
        {
            "bin": np.floor(rows["event_time_from_group_start_s"] / width).astype(int),
            "rms": rows["rms"],
            "magnitude": rows["rank1_magnitude"],
        }
    )
    result = pd.DataFrame(index=np.arange(int(math.floor(end / width)) + 1))
    grouped = source.groupby("bin")
    result["selected_event_count"] = grouped.size()
    result["waveform_rms_sum"] = grouped["rms"].sum()
    result["waveform_rms_median"] = grouped["rms"].median()
    result["waveform_rms_max"] = grouped["rms"].max()
    result["rank1_magnitude_sum"] = grouped["magnitude"].sum()
    burst_bin = np.floor(
        burst_rows["event_time_from_group_start_s"] / width
    ).astype(int)
    result["burst_count"] = burst_bin.value_counts()
    return result.fillna(0.0)


def ct_bins(ae: pd.DataFrame, width: float) -> pd.DataFrame:
    end = max(ae["ae_time_s"].max(), 0.0)
    bins = np.arange(int(math.floor(end / width)) + 1)
    source = ae.copy()
    source["bin"] = np.floor(source["ae_time_s"] / width).astype(int)
    grouped = source.groupby("bin")
    result = pd.DataFrame(index=bins)
    result["hit_count"] = grouped.size()
    result["ct_rms_sum"] = grouped["rms"].sum()
    result["ct_rms_median"] = grouped["rms"].median()
    result["ct_rms_max"] = grouped["rms"].max()
    result["energy_sum"] = grouped["energy"].sum()
    result["cumulative_rms_increment"] = grouped["rms"].sum()
    result["cumulative_energy_increment"] = grouped["energy"].sum()
    return result.fillna(0.0)


def _aligned(
    waveform: pd.DataFrame, ct: pd.DataFrame, offset_bins: int
) -> tuple[pd.DataFrame, pd.DataFrame, float]:
    shifted = waveform.copy()
    shifted.index = shifted.index + offset_bins
    shared = shifted.index.intersection(ct.index)
    overlap = len(shared) / max(1, len(waveform))
    return shifted.loc[shared], ct.loc[shared], overlap


def _rho(left: np.ndarray, right: np.ndarray) -> float:
    if len(left) < 4 or np.all(left == left[0]) or np.all(right == right[0]):
        return 0.0
    value = spearmanr(left, right).statistic
    return 0.0 if np.isnan(value) else float(value)


def best_alignment(
    waveform: pd.DataFrame,
    ct: pd.DataFrame,
    width: float,
    minimum: int,
    maximum: int,
) -> dict:
    best: dict[str, object] | None = None
    step_min = int(round(minimum / width))
    step_max = int(round(maximum / width))
    for offset_bins in range(step_min, step_max + 1):
        left, right, overlap = _aligned(waveform, ct, offset_bins)
        metrics = {
            f"{waveform_name}__{ct_name}": _rho(
                left[waveform_name].to_numpy(), right[ct_name].to_numpy()
            )
            for waveform_name, ct_name in ACTIVITY_PAIRS
        }
        score = float(np.mean(list(metrics.values())))
        candidate = {
            "offset_s": offset_bins * width,
            "composite_score": score,
            "overlap_ratio": overlap,
            "metrics": metrics,
        }
        if best is None or (score, overlap, -abs(candidate["offset_s"])) > (
            best["composite_score"],
            best["overlap_ratio"],
            -abs(best["offset_s"]),
        ):
            best = candidate
    assert best is not None
    return best


def circular_permutation_pvalues(
    waveform: pd.DataFrame,
    ct: pd.DataFrame,
    offset_s: float,
    width: float,
    permutations: int,
    rng: np.random.Generator,
) -> dict[str, float]:
    left, right, _ = _aligned(waveform, ct, int(round(offset_s / width)))
    n = len(left)
    if n < 5:
        return {f"{a}__{b}": 1.0 for a, b in ACTIVITY_PAIRS}
    shifts = rng.integers(1, n, size=permutations)
    result: dict[str, float] = {}
    for waveform_name, ct_name in ACTIVITY_PAIRS:
        left_rank = rankdata(left[waveform_name].to_numpy()).astype(float)
        right_rank = rankdata(right[ct_name].to_numpy()).astype(float)
        left_rank -= left_rank.mean()
        right_rank -= right_rank.mean()
        denominator = np.linalg.norm(left_rank) * np.linalg.norm(right_rank)
        if denominator == 0:
            result[f"{waveform_name}__{ct_name}"] = 1.0
            continue
        observed = float(np.dot(left_rank, right_rank) / denominator)
        null = np.array(
            [np.dot(np.roll(left_rank, int(shift)), right_rank) / denominator for shift in shifts]
        )
        result[f"{waveform_name}__{ct_name}"] = float(
            (1 + np.count_nonzero(null >= observed)) / (permutations + 1)
        )
    return result


def bh_adjust(rows: list[tuple[tuple[str, str, str], float]]) -> dict[tuple[str, str, str], float]:
    ordered = sorted(rows, key=lambda item: item[1])
    count = len(ordered)
    adjusted: dict[tuple[str, str, str], float] = {}
    running = 1.0
    for rank in range(count, 0, -1):
        key, value = ordered[rank - 1]
        running = min(running, value * count / rank)
        adjusted[key] = min(1.0, running)
    return adjusted


def file_jackknife_ci(
    config: dict,
    catalog: pd.DataFrame,
    bursts: pd.DataFrame,
    ct: pd.DataFrame,
    group: str,
    best_offset: float,
) -> tuple[float, float]:
    offsets = []
    group_rows = catalog[catalog["group"] == group]
    for file_name in sorted(group_rows["file_name"].unique()):
        reduced_catalog = group_rows[group_rows["file_name"] != file_name]
        reduced_bursts = bursts[
            (bursts["group"] == group) & (bursts["file_name"] != file_name)
        ]
        waveform = waveform_bins(reduced_catalog, reduced_bursts, group, 1.0)
        result = best_alignment(
            waveform,
            ct,
            1.0,
            max(int(config["analysis"]["offset_min_s"]), int(best_offset) - 10),
            min(int(config["analysis"]["offset_max_s"]), int(best_offset) + 10),
        )
        offsets.append(float(result["offset_s"]))
    rng = np.random.default_rng(int(config["analysis"]["random_seed"]))
    offsets_array = np.asarray(offsets)
    bootstrap_medians = np.median(
        rng.choice(
            offsets_array,
            size=(int(config["analysis"]["bootstraps"]), len(offsets_array)),
            replace=True,
        ),
        axis=1,
    )
    low, high = np.quantile(bootstrap_medians, [0.025, 0.975])
    return float(low), float(high)


def assign_stage(times: np.ndarray, mechanical: pd.DataFrame) -> tuple[np.ndarray, dict]:
    stress = mechanical["stress_mpa"].to_numpy(float)
    mechanical_time = mechanical["test_time_s"].to_numpy(float)
    max_index = int(np.nanargmax(stress))
    max_stress = stress[max_index]
    before_peak = np.arange(len(stress)) <= max_index
    five = np.flatnonzero(before_peak & (stress >= 0.05 * max_stress))
    ninety = np.flatnonzero(before_peak & (stress >= 0.90 * max_stress))
    t5 = mechanical_time[int(five[0])] if len(five) else mechanical_time[0]
    t90 = mechanical_time[int(ninety[0])] if len(ninety) else mechanical_time[max_index]
    tmax = mechanical_time[max_index]
    stages = np.full(len(times), "out_of_range", dtype=object)
    valid = (times >= mechanical_time.min()) & (times <= mechanical_time.max())
    stages[valid & (times < t5)] = "preload"
    stages[valid & (times >= t5) & (times < t90)] = "rising_load"
    stages[valid & (times >= t90) & (times <= tmax)] = "near_peak"
    stages[valid & (times > tmax)] = "post_peak"
    return stages, {"t5_s": float(t5), "t90_s": float(t90), "tmax_s": float(tmax)}


def align_all(config: dict) -> dict:
    output = config["resolved"]["scientific_results"]
    catalog = pd.read_csv(output / "event_catalog.csv.gz")
    bursts = pd.read_csv(output / "burst_catalog.csv.gz")
    contexts = extract_ct_context(config)
    groups = list(config["analysis"]["groups"])
    bin_widths = [float(value) for value in config["analysis"]["alignment_bin_widths_s"]]
    waveform_by_width = {
        width: {group: waveform_bins(catalog, bursts, group, width) for group in groups}
        for width in bin_widths
    }
    ct_by_width = {
        width: {group: ct_bins(contexts[group][1], width) for group in groups}
        for width in bin_widths
    }
    rng = np.random.default_rng(int(config["analysis"]["random_seed"]))
    pair_rows: list[dict[str, object]] = []
    pvalue_rows: list[tuple[tuple[str, str, str], float]] = []
    pair_lookup: dict[tuple[str, str, float], dict] = {}
    for waveform_group in groups:
        for ct_group in groups:
            for width in bin_widths:
                result = best_alignment(
                    waveform_by_width[width][waveform_group],
                    ct_by_width[width][ct_group],
                    width,
                    int(config["analysis"]["offset_min_s"]),
                    int(config["analysis"]["offset_max_s"]),
                )
                pair_lookup[(waveform_group, ct_group, width)] = result
                if width == 1.0:
                    pvalues = circular_permutation_pvalues(
                        waveform_by_width[width][waveform_group],
                        ct_by_width[width][ct_group],
                        float(result["offset_s"]),
                        width,
                        int(config["analysis"]["permutations"]),
                        rng,
                    )
                    row = {
                        "waveform_group": waveform_group,
                        "ct_group": ct_group,
                        "offset_s": result["offset_s"],
                        "composite_score": result["composite_score"],
                        "overlap_ratio": result["overlap_ratio"],
                    }
                    for metric, value in result["metrics"].items():
                        row[f"rho__{metric}"] = value
                        row[f"p__{metric}"] = pvalues[metric]
                        pvalue_rows.append(((waveform_group, ct_group, metric), pvalues[metric]))
                    pair_rows.append(row)
    adjusted = bh_adjust(pvalue_rows)
    for row in pair_rows:
        for waveform_name, ct_name in ACTIVITY_PAIRS:
            metric = f"{waveform_name}__{ct_name}"
            row[f"q__{metric}"] = adjusted[
                (row["waveform_group"], row["ct_group"], metric)
            ]
    score_table = pd.DataFrame(pair_rows)
    score_table.to_csv(output / "mapping_score_matrix.csv", index=False)

    matrix = score_table.pivot(
        index="waveform_group", columns="ct_group", values="composite_score"
    ).loc[groups, groups]
    row_indices, column_indices = linear_sum_assignment(-matrix.to_numpy())
    assignment = {
        groups[row]: groups[column] for row, column in zip(row_indices, column_indices)
    }
    identity_assignment = all(assignment[group] == group for group in groups)

    offsets_rows = []
    supported: dict[str, bool] = {}
    for group in groups:
        diagonal = score_table[
            (score_table["waveform_group"] == group)
            & (score_table["ct_group"] == group)
        ].iloc[0]
        best_ct = (
            score_table[score_table["waveform_group"] == group]
            .sort_values(["composite_score", "overlap_ratio"], ascending=False)
            .iloc[0]["ct_group"]
        )
        offsets = [
            float(pair_lookup[(group, group, width)]["offset_s"]) for width in bin_widths
        ]
        significant_metrics = sum(
            diagonal[f"q__{waveform_name}__{ct_name}"] < 0.05
            for waveform_name, ct_name in ACTIVITY_PAIRS
        )
        ci_low, ci_high = file_jackknife_ci(
            config,
            catalog,
            bursts,
            ct_by_width[1.0][group],
            group,
            float(diagonal["offset_s"]),
        )
        is_supported = (
            best_ct == group
            and identity_assignment
            and significant_metrics >= 2
            and max(offsets) - min(offsets) <= 2.0
            and ci_high - ci_low <= 5.0
            and float(diagonal["overlap_ratio"]) >= 0.80
        )
        supported[group] = bool(is_supported)
        offsets_rows.append(
            {
                "group": group,
                "candidate_ct_sheet": f"CT-{group[1:]}",
                "best_scoring_ct_group": best_ct,
                "offset_0_5s": offsets[0],
                "offset_1s": offsets[1],
                "offset_2s": offsets[2],
                "bootstrap_ci_low_s": ci_low,
                "bootstrap_ci_high_s": ci_high,
                "overlap_ratio": float(diagonal["overlap_ratio"]),
                "significant_metric_count": significant_metrics,
                "mapping_status": (
                    "provisional_data_supported" if is_supported else "unresolved"
                ),
                "supervisor_confirmed": False,
            }
        )
    offsets_table = pd.DataFrame(offsets_rows)
    offsets_table.to_csv(output / "alignment_offsets.csv", index=False)

    aligned_parts = []
    stage_boundaries = {}
    for group in groups:
        if not supported[group]:
            continue
        rows = catalog[catalog["group"] == group].copy()
        offset = float(
            offsets_table.loc[offsets_table["group"] == group, "offset_1s"].iloc[0]
        )
        rows["ct_time_s"] = rows["event_time_from_group_start_s"] + offset
        mechanical, ae = contexts[group]
        stages, boundaries = assign_stage(rows["ct_time_s"].to_numpy(), mechanical)
        stage_boundaries[group] = boundaries
        rows["mechanical_stage"] = stages
        valid = stages != "out_of_range"
        for column in (
            "nominal_displacement_mm",
            "strain_pct",
            "force_n",
            "stress_mpa",
        ):
            rows[column] = np.nan
            rows.loc[valid, column] = np.interp(
                rows.loc[valid, "ct_time_s"],
                mechanical["test_time_s"],
                mechanical[column],
            )
        ae_one_second = ct_bins(ae, 1.0)
        event_bins = np.floor(rows["ct_time_s"]).astype(int)
        for column in (
            "hit_count",
            "ct_rms_sum",
            "ct_rms_median",
            "ct_rms_max",
            "energy_sum",
        ):
            rows[f"ct_ae_{column}"] = [
                ae_one_second.at[index, column] if index in ae_one_second.index else 0.0
                for index in event_bins
            ]
        aligned_parts.append(rows)
    aligned = pd.concat(aligned_parts, ignore_index=True) if aligned_parts else pd.DataFrame(
        columns=CATALOG_COLUMNS
        + [
            "ct_time_s",
            "mechanical_stage",
            "nominal_displacement_mm",
            "strain_pct",
            "force_n",
            "stress_mpa",
        ]
    )
    aligned.to_csv(
        output / "aligned_events.csv.gz",
        index=False,
        compression="gzip",
        float_format="%.17g",
    )
    if aligned.empty:
        stage_summary = pd.DataFrame(
            columns=["group", "mechanical_stage", "legacy_matched", "event_count"]
        )
        frequency_summary = pd.DataFrame(
            columns=["group", "mechanical_stage", "legacy_matched", "median_frequency_khz"]
        )
    else:
        stage_summary = (
            aligned.groupby(["group", "mechanical_stage", "legacy_matched"])
            .size()
            .rename("event_count")
            .reset_index()
        )
        frequency_summary = (
            aligned.groupby(["group", "mechanical_stage", "legacy_matched"])[
                "rank1_frequency_khz"
            ]
            .median()
            .rename("median_frequency_khz")
            .reset_index()
        )
    stage_summary.to_csv(output / "stage_event_summary.csv", index=False)
    frequency_summary.to_csv(output / "stage_frequency_summary.csv", index=False)
    render_alignment_diagnostics(config, matrix, offsets_table, waveform_by_width[1.0], ct_by_width[1.0])
    summary = {
        "candidate_mapping": {group: f"CT-{group[1:]}" for group in groups},
        "global_assignment": assignment,
        "identity_assignment_is_optimal": identity_assignment,
        "groups": {
            row["group"]: {
                "status": row["mapping_status"],
                "offset_s": row["offset_1s"],
                "bootstrap_ci_s": [
                    row["bootstrap_ci_low_s"],
                    row["bootstrap_ci_high_s"],
                ],
                "supervisor_confirmed": False,
            }
            for row in offsets_rows
        },
        "supported_group_count": sum(supported.values()),
        "unresolved_group_count": len(groups) - sum(supported.values()),
        "stage_boundaries": stage_boundaries,
        "interpretation": (
            "Every data-supported mapping remains provisional until independently confirmed."
        ),
    }
    (output / "alignment_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    return summary


def render_alignment_diagnostics(
    config: dict,
    matrix: pd.DataFrame,
    offsets: pd.DataFrame,
    waveform: dict[str, pd.DataFrame],
    ct: dict[str, pd.DataFrame],
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    output = config["resolved"]["scientific_results"] / "alignment_diagnostics"
    output.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(7, 6))
    image = axis.imshow(matrix.to_numpy(), cmap="viridis")
    axis.set_xticks(range(len(matrix.columns)), matrix.columns)
    axis.set_yticks(range(len(matrix.index)), matrix.index)
    axis.set_xlabel("CT group")
    axis.set_ylabel("Waveform group")
    figure.colorbar(image, ax=axis, label="Composite Spearman score")
    figure.tight_layout()
    figure.savefig(output / "mapping_score_heatmap.png", dpi=150)
    plt.close(figure)
    for row in offsets.itertuples(index=False):
        group = row.group
        shifted, right, _ = _aligned(
            waveform[group], ct[group], int(round(row.offset_1s))
        )
        left_count = shifted["selected_event_count"].to_numpy(float)
        right_count = right["hit_count"].to_numpy(float)
        left_scale = left_count.max() or 1.0
        right_scale = right_count.max() or 1.0
        figure, axis = plt.subplots(figsize=(9, 3.5))
        axis.plot(shifted.index, left_count / left_scale, label="Adaptive event count")
        axis.plot(right.index, right_count / right_scale, label="CT hit count")
        axis.set_title(f"{group} ↔ CT-{group[1:]} ({row.mapping_status})")
        axis.set_xlabel("Candidate CT time (s)")
        axis.set_ylabel("Normalised activity")
        axis.grid(alpha=0.25)
        axis.legend()
        figure.tight_layout()
        figure.savefig(output / f"{group}_activity_overlay.png", dpi=150)
        plt.close(figure)


def frequency_band(values: pd.Series) -> pd.Series:
    return pd.cut(
        values,
        bins=FREQUENCY_BANDS,
        labels=FREQUENCY_LABELS,
        right=False,
    )


def bootstrap_file_mean(
    table: pd.DataFrame, value_column: str, bootstraps: int, seed: int
) -> tuple[float, float]:
    per_file = table.groupby("file_name")[value_column].mean().to_numpy(float)
    if not len(per_file):
        return 0.0, 0.0
    rng = np.random.default_rng(seed)
    values = rng.choice(
        per_file, size=(bootstraps, len(per_file)), replace=True
    ).mean(axis=1)
    low, high = np.quantile(values, [0.025, 0.975])
    return float(low), float(high)


def evaluate_top3(config: dict) -> dict:
    output = config["resolved"]["scientific_results"]
    seed = int(config["analysis"]["random_seed"])
    catalog = pd.read_csv(output / "event_catalog.csv.gz")

    def evaluate_factor(factor: int) -> pd.DataFrame:
        factor_rows = cluster_bursts(
            catalog, factor, int(config["analysis"]["hop_samples"])
        )
        factor_rows["m2_m1"] = (
            factor_rows["rank2_magnitude"] / factor_rows["rank1_magnitude"]
        )
        factor_rows["m3_m1"] = (
            factor_rows["rank3_magnitude"] / factor_rows["rank1_magnitude"]
        )
        rank1_band = frequency_band(factor_rows["rank1_frequency_khz"])
        rank2_band = frequency_band(factor_rows["rank2_frequency_khz"])
        rank3_band = frequency_band(factor_rows["rank3_frequency_khz"])
        factor_rows["secondary_cross_band"] = (
            ((rank2_band.notna()) & (rank2_band != rank1_band))
            | ((rank3_band.notna()) & (rank3_band != rank1_band))
        )
        result = []
        for group_index, group in enumerate(config["analysis"]["groups"]):
            rows = factor_rows[factor_rows["group"] == group]
            cross_low, cross_high = bootstrap_file_mean(
                rows,
                "secondary_cross_band",
                int(config["analysis"]["bootstraps"]),
                seed + factor * 100 + group_index,
            )
            row = {
                "group": group,
                "burst_count": int(len(rows)),
                "rank2_availability": float(rows["rank2_magnitude"].notna().mean()),
                "rank3_availability": float(rows["rank3_magnitude"].notna().mean()),
                "median_m2_m1": float(rows["m2_m1"].median()),
                "median_m3_m1": float(rows["m3_m1"].median()),
                "secondary_cross_band_fraction": float(
                    rows["secondary_cross_band"].mean()
                ),
                "secondary_cross_band_bootstrap_ci_low": cross_low,
                "secondary_cross_band_bootstrap_ci_high": cross_high,
            }
            row["availability_pass"] = row["rank3_availability"] >= 0.95
            row["magnitude_pass"] = (
                row["median_m2_m1"] >= 0.20 and row["median_m3_m1"] >= 0.10
            )
            row["cross_band_pass"] = (
                row["secondary_cross_band_fraction"] >= 0.10
                and row["secondary_cross_band_bootstrap_ci_low"] > 0.05
            )
            result.append(row)
        return pd.DataFrame(result)

    factor_tables = {factor: evaluate_factor(factor) for factor in (1, 2, 5)}
    groups = factor_tables[2]
    groups.to_csv(output / "top3_value_by_group.csv", index=False)
    criteria = {
        "availability_pass_groups": int(groups["availability_pass"].sum()),
        "magnitude_pass_groups": int(groups["magnitude_pass"].sum()),
        "cross_band_pass_groups": int(groups["cross_band_pass"].sum()),
    }
    factor_counts = {
        str(factor): int(len(cluster_bursts(
            catalog, factor, int(config["analysis"]["hop_samples"])
        )))
        for factor in (1, 2, 5)
    }
    clustering_stable = all(
        table["availability_pass"].sum() >= 6
        and table["magnitude_pass"].sum() >= 6
        and table["cross_band_pass"].sum() >= 6
        for table in factor_tables.values()
    )
    leave_one_out_stable = True
    for omitted in config["analysis"]["groups"]:
        subset = groups[groups["group"] != omitted]
        if not (
            subset["availability_pass"].sum() >= 6
            and subset["magnitude_pass"].sum() >= 6
            and subset["cross_band_pass"].sum() >= 6
        ):
            leave_one_out_stable = False
            break
    audit_path = output / "waveform_audit_unblinded.csv"
    audit = pd.read_csv(audit_path, keep_default_na=False)
    audit_complete = bool(
        len(audit)
        and (audit["review_status"] == "complete").all()
        and audit["morphology"].isin(MORPHOLOGY_LABELS).all()
        and audit["burst_pattern"].isin(BURST_LABELS).all()
    )
    noise_fraction = (
        float(audit["morphology"].isin({"noise_like", "clipped"}).mean())
        if audit_complete
        else None
    )
    blind_audit_pass = bool(audit_complete and noise_fraction < 0.50)
    numerical_gate = (
        criteria["availability_pass_groups"] >= 6
        and criteria["magnitude_pass_groups"] >= 6
        and criteria["cross_band_pass_groups"] >= 6
        and clustering_stable
        and leave_one_out_stable
    )
    decision = "retained" if numerical_gate and blind_audit_pass else "appendix_only"
    summary = {
        "decision": decision,
        "criteria": criteria,
        "burst_clustering_counts": factor_counts,
        "burst_clustering_conclusions_stable": clustering_stable,
        "leave_one_group_out_stable": leave_one_out_stable,
        "blind_audit_complete": audit_complete,
        "blind_audit_noise_like_fraction": noise_fraction,
        "blind_audit_pass": blind_audit_pass,
        "numerical_gate_pass": numerical_gate,
        "reason_if_appendix_only": (
            None
            if decision == "retained"
            else "At least one preregistered numerical, sensitivity, or blind-audit condition failed or remains incomplete."
        ),
        "claim_boundary": (
            "Secondary peaks are descriptive spectral information, not crack-type labels or detection-accuracy evidence."
        ),
    }
    (output / "top3_value_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    return summary


def run_all(config: dict) -> None:
    catalog = build_event_catalog(config)
    build_bursts(config, catalog)
    samples = deterministic_samples(config, catalog)
    render_waveform_samples(config, samples)
    blind_signal_audit(config)
    unblind(config)
    align_all(config)
    evaluate_top3(config)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=["all", "catalog", "bursts", "sample", "audit", "align", "unblind", "top3"],
    )
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    config = load_config(args.config)
    output = config["resolved"]["scientific_results"]
    output.mkdir(parents=True, exist_ok=True)
    if args.command == "all":
        run_all(config)
    elif args.command == "catalog":
        build_event_catalog(config)
    elif args.command == "bursts":
        build_bursts(config)
    elif args.command == "sample":
        samples = deterministic_samples(config)
        render_waveform_samples(config, samples)
    elif args.command == "audit":
        blind_signal_audit(config)
        unblind(config)
    elif args.command == "align":
        align_all(config)
    elif args.command == "unblind":
        unblind(config)
    elif args.command == "top3":
        evaluate_top3(config)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
