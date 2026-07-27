#!/usr/bin/env python3
"""Stream the large R260_2 workbook without loading it into Excel memory."""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import re
import statistics
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = f"{{{MAIN_NS}}}"

CONFIG_LABELS = {
    "Max Load",
    "Min Load",
    "R",
    "Frequency",
    "Current",
    "Chart Velocity",
    "V in",
    "Initial Crack length",
    "Width",
    "Thickness",
    "Half of sensors distance",
    "Cycles to failure",
}

DETAIL_FIELDS = [
    "COUN",
    "ENER",
    "DURATION",
    "AMP",
    "RMS",
    "SIG STRNGTH",
    "ABS-ENERGY",
    "P-FRQ",
]
EXPECTED_SHA256 = "2bf80527130a7eab326297a2dc1c17974dbae45cf3840217378169d227f8ea64"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def column_number(reference: str) -> int:
    letters = re.match(r"[A-Z]+", reference).group()
    result = 0
    for letter in letters:
        result = result * 26 + ord(letter) - 64
    return result


def shared_strings(archive: zipfile.ZipFile) -> list[str]:
    with archive.open("xl/sharedStrings.xml") as source:
        root = ET.parse(source).getroot()
    return ["".join(node.itertext()) for node in root.findall(f"{NS}si")]


def sheet_map(archive: zipfile.ZipFile) -> dict[str, str]:
    with archive.open("xl/_rels/workbook.xml.rels") as source:
        rels = ET.parse(source).getroot()
    targets = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in rels.findall(f"{{{PKG_REL_NS}}}Relationship")
    }
    with archive.open("xl/workbook.xml") as source:
        workbook = ET.parse(source).getroot()
    return {
        sheet.attrib["name"]: "xl/" + targets[sheet.attrib[f"{{{REL_NS}}}id"]]
        for sheet in workbook.find(f"{NS}sheets")
    }


def parse_scalar(text: str | None) -> str | int | float | None:
    if text is None or text == "":
        return None
    try:
        value = float(text)
    except ValueError:
        return text
    if value.is_integer() and abs(value) <= 2**53:
        return int(value)
    return value


def cell_value(cell: ET.Element, strings: list[str]) -> str | int | float | None:
    value_node = cell.find(f"{NS}v")
    raw = None if value_node is None else value_node.text
    if cell.attrib.get("t") == "s" and raw is not None:
        return strings[int(raw)]
    if cell.attrib.get("t") == "inlineStr":
        inline = cell.find(f"{NS}is")
        return "" if inline is None else "".join(inline.itertext())
    return parse_scalar(raw)


def quantile(sorted_values: list[float], probability: float) -> float:
    if not sorted_values:
        return math.nan
    position = (len(sorted_values) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return sorted_values[lower]
    return sorted_values[lower] + (position - lower) * (
        sorted_values[upper] - sorted_values[lower]
    )


def describe(values: list[float]) -> dict[str, float | int]:
    ordered = sorted(values)
    return {
        "count": len(ordered),
        "min": ordered[0],
        "mean": statistics.fmean(ordered),
        "median": quantile(ordered, 0.5),
        "p90": quantile(ordered, 0.9),
        "p95": quantile(ordered, 0.95),
        "max": ordered[-1],
    }


def pearson(left: list[float], right: list[float]) -> float:
    left_mean = statistics.fmean(left)
    right_mean = statistics.fmean(right)
    numerator = sum(
        (x - left_mean) * (y - right_mean) for x, y in zip(left, right)
    )
    denominator = math.sqrt(
        sum((x - left_mean) ** 2 for x in left)
        * sum((y - right_mean) ** 2 for y in right)
    )
    return numerator / denominator


def parse_sheet(
    archive: zipfile.ZipFile,
    xml_path: str,
    strings: list[str],
    detailed: bool,
) -> dict:
    result = {
        "dimension": None,
        "config": {},
        "formula_count": 0,
        "error_counts": {},
        "error_examples": [],
        "hit_header_row": None,
        "message_1_count": 0,
        "message_173_count": 0,
        "matched_173_1_pairs": 0,
        "pair_mismatches": 0,
        "pair_mismatch_examples": [],
        "channel_counts": {},
    }
    header_by_column: dict[int, str] | None = None
    pending_waveform: tuple[float | int | None, float | int | None] | None = None
    detail_values = {field: [] for field in DETAIL_FIELDS}
    hit_times_s: list[float] = []
    crack_rows = []

    with archive.open(xml_path) as source:
        for event, element in ET.iterparse(source, events=("end",)):
            if element.tag == f"{NS}dimension":
                result["dimension"] = element.attrib.get("ref")
                element.clear()
                continue
            if element.tag != f"{NS}row":
                continue

            row_number = int(element.attrib["r"])
            row: dict[int, tuple[str, str | int | float | None, str | None]] = {}
            for cell in element.findall(f"{NS}c"):
                reference = cell.attrib["r"]
                column = column_number(reference)
                value = cell_value(cell, strings)
                formula_node = cell.find(f"{NS}f")
                formula = None if formula_node is None else formula_node.text
                if formula_node is not None:
                    result["formula_count"] += 1
                if cell.attrib.get("t") == "e" and value is not None:
                    key = str(value)
                    result["error_counts"][key] = result["error_counts"].get(key, 0) + 1
                    if len(result["error_examples"]) < 12:
                        result["error_examples"].append(
                            {"cell": reference, "error": key, "formula": formula}
                        )
                row[column] = (reference, value, formula)

            if row_number <= 14:
                for column, (_, value, _) in row.items():
                    label = value.strip() if isinstance(value, str) else value
                    if label in CONFIG_LABELS:
                        right = row.get(column + 1, ("", None, None))[1]
                        if isinstance(right, (int, float)):
                            result["config"][str(label)] = right

            labels = {
                str(value): column
                for column, (_, value, _) in row.items()
                if isinstance(value, str)
            }
            if (
                header_by_column is None
                and "ID" in labels
                and "CH" in labels
                and "P-FRQ" in labels
            ):
                header_by_column = {
                    column: str(value)
                    for column, (_, value, _) in row.items()
                    if isinstance(value, str)
                }
                result["hit_header_row"] = row_number
                element.clear()
                continue

            if header_by_column is not None and row_number > result["hit_header_row"]:
                values_by_name = {
                    name: row.get(column, ("", None, None))[1]
                    for column, name in header_by_column.items()
                }
                message_id = values_by_name.get("ID")
                event_time = values_by_name.get("HH:MM:SS.mmmuuun")
                channel = values_by_name.get("CH")
                if message_id == 173:
                    result["message_173_count"] += 1
                    if pending_waveform is not None:
                        result["pair_mismatches"] += 1
                        if len(result["pair_mismatch_examples"]) < 5:
                            result["pair_mismatch_examples"].append(
                                {"row": row_number, "reason": "consecutive waveform markers"}
                            )
                    pending_waveform = (event_time, channel)
                elif message_id == 1:
                    result["message_1_count"] += 1
                    channel_key = str(channel)
                    result["channel_counts"][channel_key] = (
                        result["channel_counts"].get(channel_key, 0) + 1
                    )
                    if pending_waveform == (event_time, channel):
                        result["matched_173_1_pairs"] += 1
                    elif pending_waveform is not None:
                        result["pair_mismatches"] += 1
                        if len(result["pair_mismatch_examples"]) < 5:
                            result["pair_mismatch_examples"].append(
                                {
                                    "row": row_number,
                                    "reason": "time or channel mismatch",
                                    "waveform": pending_waveform,
                                    "hit": (event_time, channel),
                                }
                            )
                    pending_waveform = None
                    if detailed:
                        if isinstance(event_time, (int, float)):
                            hit_times_s.append(float(event_time) * 86400)
                        for field in DETAIL_FIELDS:
                            value = values_by_name.get(field)
                            if isinstance(value, (int, float)):
                                detail_values[field].append(float(value))

            if detailed and 15 <= row_number <= 40:
                value = lambda column: row.get(column, ("", None, None))[1]
                label = value(1)
                cycles = value(6)
                crack_size = value(8)
                delta_k = value(12)
                da_dn = value(14)
                if (
                    isinstance(cycles, (int, float))
                    and isinstance(crack_size, (int, float))
                    and isinstance(delta_k, (int, float))
                ):
                    crack_rows.append(
                        {
                            "row": row_number,
                            "label": label,
                            "cycles": cycles,
                            "crack_size_m": crack_size,
                            "delta_k": delta_k,
                            "da_dn": da_dn,
                            "ae_count": value(18),
                            "ae_energy": value(19),
                            "ae_duration": value(20),
                            "cycle_interval": value(11),
                            "ae_count_formula": row.get(18, ("", None, None))[2],
                        }
                    )

            element.clear()

    if pending_waveform is not None:
        result["pair_mismatches"] += 1
        if len(result["pair_mismatch_examples"]) < 5:
            result["pair_mismatch_examples"].append(
                {"row": None, "reason": "unmatched final waveform marker"}
            )
    result["recognised_schema"] = header_by_column is not None

    if detailed:
        result["features"] = {
            field: describe(values) for field, values in detail_values.items() if values
        }
        result["crack_growth_rows"] = crack_rows
        if hit_times_s:
            start = min(hit_times_s)
            end = max(hit_times_s)
            result["time_start_s"] = start
            result["time_end_s"] = end
            result["duration_s"] = end - start
            bins = [0] * 10
            width = (end - start) / 10
            for value in hit_times_s:
                index = 0 if width == 0 else min(9, int((value - start) / width))
                bins[index] += 1
            result["ten_equal_time_bin_hit_counts"] = bins
        amplitudes = detail_values["AMP"]
        if amplitudes:
            result["amplitude_bin_counts"] = {
                "<50": sum(value < 50 for value in amplitudes),
                "50-59": sum(50 <= value < 60 for value in amplitudes),
                "60-69": sum(60 <= value < 70 for value in amplitudes),
                "70-79": sum(70 <= value < 80 for value in amplitudes),
                "80-89": sum(80 <= value < 90 for value in amplitudes),
                ">=90": sum(value >= 90 for value in amplitudes),
            }
        frequencies = detail_values["P-FRQ"]
        if frequencies:
            result["pfrq_top_values"] = [
                {"value": value, "count": count}
                for value, count in collections.Counter(frequencies).most_common(10)
            ]
        valid_crack_rows = [
            row
            for row in crack_rows
            if isinstance(row["da_dn"], (int, float))
            and row["da_dn"] > 0
            and isinstance(row["cycle_interval"], (int, float))
            and row["cycle_interval"] > 0
            and row["label"] != "failure"
        ]
        if len(valid_crack_rows) >= 3:
            log_delta_k = [math.log10(row["delta_k"]) for row in valid_crack_rows]
            log_da_dn = [math.log10(row["da_dn"]) for row in valid_crack_rows]
            x_mean = statistics.fmean(log_delta_k)
            y_mean = statistics.fmean(log_da_dn)
            slope = sum(
                (x - x_mean) * (y - y_mean)
                for x, y in zip(log_delta_k, log_da_dn)
            ) / sum((x - x_mean) ** 2 for x in log_delta_k)
            rates = {
                field: [
                    row[field] / row["cycle_interval"] for row in valid_crack_rows
                ]
                for field in ("ae_count", "ae_energy", "ae_duration")
            }
            result["exploratory_correlations"] = {
                "n_intervals": len(valid_crack_rows),
                "paris_log10_slope": slope,
                "paris_log10_intercept": y_mean - slope * x_mean,
                "paris_log10_pearson_r": pearson(log_delta_k, log_da_dn),
                "da_dn_vs_ae_count_per_cycle_r": pearson(
                    [row["da_dn"] for row in valid_crack_rows],
                    rates["ae_count"],
                ),
                "da_dn_vs_ae_energy_per_cycle_r": pearson(
                    [row["da_dn"] for row in valid_crack_rows],
                    rates["ae_energy"],
                ),
                "da_dn_vs_ae_duration_per_cycle_r": pearson(
                    [row["da_dn"] for row in valid_crack_rows],
                    rates["ae_duration"],
                ),
            }
        failure_rows = [row for row in crack_rows if row["label"] == "failure"]
        if failure_rows:
            failure = failure_rows[-1]
            formula = failure["ae_count_formula"] or ""
            result["failure_row_audit"] = {
                "row": failure["row"],
                "cycles_in_failure_row": failure["cycles"],
                "cycles_to_failure_config": result["config"].get("Cycles to failure"),
                "cycle_difference": (
                    result["config"].get("Cycles to failure") - failure["cycles"]
                    if isinstance(result["config"].get("Cycles to failure"), (int, float))
                    else None
                ),
                "ae_count_formula": formula,
                "formula_lacks_lower_bound": formula.count("Y:Y") == 1,
                "exclude_from_interval_analysis": True,
            }

    return result


def write_tsv(path: Path, headers: list[str], rows: list[list[object]]) -> None:
    with path.open("w", encoding="utf-8") as output:
        output.write("\t".join(headers) + "\n")
        for row in rows:
            output.write("\t".join("" if value is None else str(value) for value in row) + "\n")


def validate_analysis(analysis: dict) -> None:
    if analysis["sha256"] != EXPECTED_SHA256:
        raise RuntimeError("source workbook checksum differs from the analysed fixture")
    s3 = analysis["sheets"]["S3"]
    if not (
        s3["message_1_count"]
        == s3["message_173_count"]
        == s3["matched_173_1_pairs"]
        == 3553
    ):
        raise RuntimeError("S3 hit/waveform pairing regression")
    if s3["pair_mismatches"] != 0:
        raise RuntimeError("S3 contains an unexpected pairing mismatch")
    if sum(s3["ten_equal_time_bin_hit_counts"]) != s3["message_1_count"]:
        raise RuntimeError("S3 time-bin counts do not reconcile")
    if not s3["failure_row_audit"]["formula_lacks_lower_bound"]:
        raise RuntimeError("S3 failure-row formula audit changed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("workbook", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    analysis = {
        "source": str(args.workbook),
        "sha256": sha256(args.workbook),
        "sheets": {},
    }
    with zipfile.ZipFile(args.workbook) as archive:
        strings = shared_strings(archive)
        for name, xml_path in sheet_map(archive).items():
            if name == "summar_R260_2":
                continue
            print(f"analysing {name}", flush=True)
            analysis["sheets"][name] = parse_sheet(
                archive,
                xml_path,
                strings,
                detailed=name == "S3",
            )
    validate_analysis(analysis)

    with (args.output / "analysis.json").open("w", encoding="utf-8") as output:
        json.dump(analysis, output, ensure_ascii=False, indent=2)

    specimen_rows = []
    for name, sheet in analysis["sheets"].items():
        config = sheet["config"]
        specimen_rows.append(
            [
                name,
                sheet["dimension"],
                config.get("Initial Crack length"),
                config.get("Cycles to failure"),
                config.get("Max Load"),
                config.get("Min Load"),
                config.get("Frequency"),
                sheet["message_1_count"],
                sheet["message_173_count"],
                sheet["matched_173_1_pairs"],
                sheet["pair_mismatches"],
                json.dumps(sheet["channel_counts"], sort_keys=True),
                sum(sheet["error_counts"].values()),
            ]
        )
    write_tsv(
        args.output / "specimen_summary.tsv",
        [
            "sheet",
            "dimension",
            "initial_crack_length_source_value",
            "cycles_to_failure",
            "max_load",
            "min_load",
            "frequency",
            "recognised_common_schema_hit_count",
            "recognised_common_schema_waveform_marker_count",
            "recognised_common_schema_matched_pairs",
            "pair_mismatches",
            "channel_counts",
            "cached_formula_errors",
        ],
        specimen_rows,
    )

    s3 = analysis["sheets"]["S3"]
    write_tsv(
        args.output / "s3_feature_summary.tsv",
        ["feature", "count", "min", "mean", "median", "p90", "p95", "max"],
        [
            [
                feature,
                summary["count"],
                summary["min"],
                summary["mean"],
                summary["median"],
                summary["p90"],
                summary["p95"],
                summary["max"],
            ]
            for feature, summary in s3["features"].items()
        ],
    )
    write_tsv(
        args.output / "s3_crack_growth.tsv",
        [
            "row",
            "label",
            "cycles",
            "crack_size_m",
            "delta_k",
            "da_dn",
            "cycle_interval",
            "ae_count",
            "ae_energy",
            "ae_duration",
            "ae_count_formula",
        ],
        [
            [row.get(header) for header in [
                "row",
                "label",
                "cycles",
                "crack_size_m",
                "delta_k",
                "da_dn",
                "cycle_interval",
                "ae_count",
                "ae_energy",
                "ae_duration",
                "ae_count_formula",
            ]]
            for row in s3["crack_growth_rows"]
        ],
    )
    print(args.output / "analysis.json")


if __name__ == "__main__":
    main()
