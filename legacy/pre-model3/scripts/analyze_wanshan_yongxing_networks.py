#!/usr/bin/env python3
"""Reanalyse Wanshan–Yongxing whole and shared-plant visitation networks."""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Sequence

from channel_id.external_archipelago_network import (
    WeightedNetwork,
    network_metrics,
    shared_plant_contrasts,
    summarize_shared_plant_contrasts,
)


def _is_number(value: object) -> bool:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return math.isfinite(float(value))
    if isinstance(value, str):
        try:
            return math.isfinite(float(value.strip()))
        except ValueError:
            return False
    return False


def _detect_header(rows: Sequence[Sequence[object]]) -> int:
    candidates: list[tuple[int, int, int]] = []
    for row_index, row in enumerate(rows[:25]):
        string_headers = sum(
            isinstance(value, str) and bool(value.strip()) and not _is_number(value)
            for value in row[1:]
        )
        nonempty = sum(value not in (None, "") for value in row)
        if string_headers > 0 and nonempty >= 2:
            candidates.append((string_headers, nonempty, -row_index))
    if not candidates:
        raise ValueError("unable to detect matrix header row")
    best = max(candidates)
    return -best[2]


def _as_weight(value: object, *, cell: str) -> float:
    if value is None or (isinstance(value, str) and not value.strip()):
        return 0.0
    if isinstance(value, str) and value.strip().casefold() in {"na", "n/a", "-"}:
        return 0.0
    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"nonnumeric interaction value at {cell}: {value!r}") from error
    if not math.isfinite(number) or number < 0:
        raise ValueError(f"invalid interaction value at {cell}: {value!r}")
    return number


def read_matrix_sheet(worksheet: object) -> WeightedNetwork:
    raw_rows = [list(row) for row in worksheet.iter_rows(values_only=True)]
    header_index = _detect_header(raw_rows)
    header = raw_rows[header_index]
    pollinator_columns = [
        index
        for index, value in enumerate(header[1:], start=1)
        if value is not None and str(value).strip()
    ]
    if not pollinator_columns:
        raise ValueError(f"sheet {worksheet.title!r} has no pollinator headers")
    pollinator_names = [str(header[index]).strip() for index in pollinator_columns]
    plants: list[str] = []
    matrix: list[list[float]] = []
    for row_index, row in enumerate(raw_rows[header_index + 1 :], start=header_index + 2):
        plant = row[0] if row else None
        if plant is None or not str(plant).strip():
            continue
        plant_name = " ".join(str(plant).split())
        values = [
            _as_weight(row[column] if column < len(row) else None, cell=f"{worksheet.title}!R{row_index}C{column + 1}")
            for column in pollinator_columns
        ]
        plants.append(plant_name)
        matrix.append(values)
    if not plants:
        raise ValueError(f"sheet {worksheet.title!r} has no plant rows")
    return WeightedNetwork.from_rows(plants, pollinator_names, matrix)


def _write_csv(path: Path, rows: Sequence[dict[str, object]]) -> None:
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def _format(value: object, digits: int = 3) -> str:
    if value is None:
        return "NA"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def build_markdown(result: dict[str, object]) -> str:
    metrics = result["network_metrics"]
    shared = result["shared_plant_summary"]
    lines = [
        "# Wanshan–Yongxing external network reanalysis",
        "",
        "## Source-native design",
        "",
        "One continental island (Wanshan) and one oceanic coral island (Yongxing) are compared. The workbook contains whole-community matrices and a matched seven-plant subnetwork.",
        "",
        "## Transparent network summaries",
        "",
        "| network | plants | pollinators | positive links | total visitation rate | binary connectance | mean plant partner richness |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for role in (
        "wanshan_full",
        "yongxing_full",
        "wanshan_shared_plants",
        "yongxing_shared_plants",
    ):
        row = metrics[role]
        lines.append(
            "| {role} | {n_plants} | {n_pollinators} | {links} | {total} | {connectance} | {mean_richness} |".format(
                role=role,
                n_plants=row["n_plants"],
                n_pollinators=row["n_pollinators"],
                links=row["n_positive_links"],
                total=_format(row["total_visitation_rate"]),
                connectance=_format(row["binary_connectance"]),
                mean_richness=_format(row["mean_pollinator_richness_per_plant"]),
            )
        )
    lines.extend(
        [
            "",
            "## Matched shared-plant contrast",
            "",
            f"Shared plants: **{shared['n_shared_plants']}**.",
            "",
            "- Oceanic-lower visitation: "
            f"{shared['visitation_direction_counts']['oceanic_lower']} / {shared['n_shared_plants']} "
            f"(two-sided sign test = {_format(shared['visitation_exact_sign_test_two_sided'])}).",
            "- Median log response ratio for visitation, ln(oceanic/continental): "
            f"{_format(shared['median_visitation_log_response_ratio'])}.",
            "- Oceanic-lower pollinator richness: "
            f"{shared['pollinator_richness_direction_counts']['oceanic_lower']} / {shared['n_shared_plants']} "
            f"(two-sided sign test = {_format(shared['pollinator_richness_exact_sign_test_two_sided'])}).",
            "- Median log response ratio for pollinator richness: "
            f"{_format(shared['median_pollinator_richness_log_response_ratio'])}.",
            "- Median Morisita–Horn pollinator-assemblage turnover: "
            f"{_format(shared['median_pollinator_morisita_horn_turnover'])}.",
            "",
            "## Claim boundary",
            "",
            str(result["claim_boundary"]),
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/wanshan_yongxing_dryad_source.json"),
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=Path("artifacts/wanshan_yongxing_dryad"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/wanshan_yongxing_analysis"),
    )
    args = parser.parse_args()

    try:
        import openpyxl
    except ImportError as error:
        raise RuntimeError("openpyxl is required for workbook analysis") from error

    config = json.loads(args.config.read_text(encoding="utf-8"))
    workbook_path = args.source_dir / str(config["known_file"]["filename"])
    inventory_path = args.source_dir / "source_inventory.json"
    if not workbook_path.exists():
        raise FileNotFoundError(workbook_path)
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    workbook = openpyxl.load_workbook(workbook_path, read_only=True, data_only=True)
    roles: dict[str, WeightedNetwork] = {}
    source_sheets: dict[str, str] = {}
    for mapping in config["sheet_roles"]:
        index = int(mapping["sheet_index"])
        if index >= len(workbook.worksheets):
            raise ValueError(f"workbook lacks sheet index {index}")
        worksheet = workbook.worksheets[index]
        role = str(mapping["role"])
        roles[role] = read_matrix_sheet(worksheet)
        source_sheets[role] = worksheet.title
    workbook.close()

    required = {
        "wanshan_full",
        "yongxing_full",
        "wanshan_shared_plants",
        "yongxing_shared_plants",
    }
    if set(roles) != required:
        raise ValueError(f"unexpected role set: {sorted(roles)}")

    metric_rows: list[dict[str, object]] = []
    metric_index: dict[str, dict[str, object]] = {}
    for role, network in roles.items():
        row = {"role": role, "source_sheet": source_sheets[role], **network_metrics(network)}
        metric_rows.append(row)
        metric_index[role] = row

    contrasts = list(
        shared_plant_contrasts(
            roles["wanshan_shared_plants"],
            roles["yongxing_shared_plants"],
        )
    )
    summary = summarize_shared_plant_contrasts(contrasts)
    expected = int(config["expected_shared_plant_count"])
    if int(summary["n_shared_plants"]) != expected:
        raise ValueError(
            f"expected {expected} shared plants, recovered {summary['n_shared_plants']}"
        )

    result = {
        "schema_version": "1.0",
        "analysis_status": "source_native_external_contrast",
        "source_id": config["source_id"],
        "article_doi": config["article_doi"],
        "dataset_doi": config["dataset_doi"],
        "source_sha256": inventory["sha256"],
        "source_sheets": source_sheets,
        "network_metrics": metric_index,
        "shared_plant_summary": summary,
        "methods": {
            "whole_network": [
                "plant richness",
                "pollinator richness",
                "positive-link count",
                "total visitation rate",
                "binary connectance",
                "Shannon interaction diversity",
                "Morisita-Horn mean niche overlap"
            ],
            "matched_shared_plants": [
                "plant-specific visitation log response ratio",
                "plant-specific pollinator-richness log response ratio",
                "binary Jaccard similarity",
                "Morisita-Horn abundance similarity and turnover",
                "exact two-sided sign tests",
                "leave-one-plant median sensitivity"
            ],
            "not_reconstructed": [
                "package-specific H2 prime",
                "package-specific weighted NODF",
                "FDQ",
                "trait matching",
                "pollinator effectiveness",
                "effective dependency"
            ]
        },
        "claim_boundary": config["claim_boundary"]
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "analysis.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    _write_csv(args.output_dir / "network_metrics.csv", metric_rows)
    _write_csv(args.output_dir / "shared_plant_contrasts.csv", contrasts)
    (args.output_dir / "report.md").write_text(build_markdown(result), encoding="utf-8")

    print(f"source sha256: {result['source_sha256']}")
    print(f"shared plants: {summary['n_shared_plants']}")
    print(
        "oceanic-lower visitation: "
        f"{summary['visitation_direction_counts']['oceanic_lower']}"
    )
    print(args.output_dir / "analysis.json")


if __name__ == "__main__":
    main()
