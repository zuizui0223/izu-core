#!/usr/bin/env python3
"""Analyse Ogasawara interaction contexts only after a source-schema gate passes."""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from typing import Iterable, Mapping

from channel_id.external_archipelago_network import (
    WeightedNetwork,
    network_metrics,
    shared_plant_contrasts,
)


def norm(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value or "").strip().casefold()).strip("_")


def choose_role(record: Mapping[str, object], role: str, *, required: bool) -> str | None:
    values = list((record.get("role_matches") or {}).get(role) or [])
    if not values:
        if required:
            raise ValueError(f"required role {role!r} was not resolved")
        return None
    if len(values) != 1:
        raise ValueError(f"role {role!r} is ambiguous: {values}")
    return str(values[0])


def read_delimited(path: Path, delimiter: str | None) -> list[dict[str, object]]:
    with path.open(encoding="utf-8-sig", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter or ",")
        return [dict(row) for row in reader]


def read_xlsx(path: Path, sheet: str) -> list[dict[str, object]]:
    import openpyxl

    workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
    worksheet = workbook[sheet]
    rows = worksheet.iter_rows(values_only=True)
    headers = None
    output = []
    for values in rows:
        if headers is None:
            if not any(str(value or "").strip() for value in values):
                continue
            headers = [str(value or "") for value in values]
            continue
        if not any(str(value or "").strip() for value in values):
            continue
        output.append({header: value for header, value in zip(headers, values)})
    workbook.close()
    return output


def read_table(record: Mapping[str, object]) -> list[dict[str, object]]:
    path = Path(str(record["file"]))
    suffix = path.suffix.lower()
    if suffix in {".csv", ".tsv", ".txt"}:
        return read_delimited(path, record.get("delimiter") or None)
    if suffix in {".xlsx", ".xlsm"}:
        sheet = str(record.get("sheet") or "")
        if not sheet:
            raise ValueError("xlsx candidate lacks a sheet name")
        return read_xlsx(path, sheet)
    raise ValueError(f"unsupported candidate table: {path}")


def nonnegative_number(value: object, label: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{label} is not numeric: {value!r}") from error
    if not math.isfinite(number) or number < 0:
        raise ValueError(f"{label} must be finite and non-negative")
    return number


def standardize_rows(record: Mapping[str, object]) -> tuple[list[dict[str, object]], dict[str, str | None]]:
    columns = {
        "island": choose_role(record, "island", required=True),
        "site": choose_role(record, "site", required=False),
        "season": choose_role(record, "season", required=False),
        "habitat": choose_role(record, "habitat", required=False),
        "anole_context": choose_role(record, "anole_context", required=False),
        "plant": choose_role(record, "plant", required=True),
        "pollinator": choose_role(record, "pollinator", required=True),
        "interaction_count": choose_role(record, "interaction_count", required=True),
    }
    count_header = norm(columns["interaction_count"])
    if not any(token in count_header for token in ("legitimate", "interaction", "visit")):
        raise ValueError(
            "interaction-count header is too generic for source-specific analysis; "
            f"resolved header={columns['interaction_count']!r}"
        )

    rows = []
    for index, source in enumerate(read_table(record), start=2):
        island = str(source.get(columns["island"], "") or "").strip()
        plant = str(source.get(columns["plant"], "") or "").strip()
        pollinator = str(source.get(columns["pollinator"], "") or "").strip()
        if not island or not plant or not pollinator:
            continue
        count = nonnegative_number(source.get(columns["interaction_count"]), f"row {index} count")
        if count <= 0:
            continue
        row: dict[str, object] = {
            "island": island,
            "plant": plant,
            "pollinator": pollinator,
            "interaction_count": count,
        }
        for role in ("site", "season", "habitat", "anole_context"):
            header = columns[role]
            row[role] = str(source.get(header, "") or "").strip() if header else ""
        rows.append(row)
    if not rows:
        raise ValueError("candidate table yielded no positive, identified interaction rows")
    return rows, columns


def build_network(rows: Iterable[Mapping[str, object]]) -> WeightedNetwork:
    rows = list(rows)
    plants = sorted({str(row["plant"]) for row in rows}, key=str.casefold)
    pollinators = sorted({str(row["pollinator"]) for row in rows}, key=str.casefold)
    plant_index = {name: index for index, name in enumerate(plants)}
    pollinator_index = {name: index for index, name in enumerate(pollinators)}
    matrix = [[0.0 for _ in pollinators] for _ in plants]
    for row in rows:
        matrix[plant_index[str(row["plant"])]][pollinator_index[str(row["pollinator"])]] += float(
            row["interaction_count"]
        )
    return WeightedNetwork.from_rows(plants, pollinators, matrix)


def context_key(row: Mapping[str, object], fields: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(str(row.get(field, "") or "").strip() or "__unreported__" for field in fields)


def grouped_metrics(rows: list[dict[str, object]], fields: tuple[str, ...]) -> list[dict[str, object]]:
    groups: dict[tuple[str, ...], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[context_key(row, fields)].append(row)
    output = []
    for key, group in sorted(groups.items()):
        metrics = network_metrics(build_network(group))
        output.append(
            {
                **{field: value for field, value in zip(fields, key)},
                "n_long_rows": len(group),
                **metrics,
            }
        )
    return output


def jaccard(left: set[str], right: set[str]) -> float:
    union = left | right
    return 1.0 if not union else len(left & right) / len(union)


def island_pair_summaries(rows: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    by_island: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_island[str(row["island"])].append(row)
    networks = {island: build_network(group) for island, group in by_island.items()}
    pair_rows = []
    plant_rows = []
    for left, right in combinations(sorted(networks, key=str.casefold), 2):
        left_rows = by_island[left]
        right_rows = by_island[right]
        left_plants = {str(row["plant"]) for row in left_rows}
        right_plants = {str(row["plant"]) for row in right_rows}
        left_pollinators = {str(row["pollinator"]) for row in left_rows}
        right_pollinators = {str(row["pollinator"]) for row in right_rows}
        left_links = {(str(row["plant"]), str(row["pollinator"])) for row in left_rows}
        right_links = {(str(row["plant"]), str(row["pollinator"])) for row in right_rows}
        contrasts = shared_plant_contrasts(networks[left], networks[right])
        pair_rows.append(
            {
                "left_island": left,
                "right_island": right,
                "plant_jaccard": jaccard(left_plants, right_plants),
                "pollinator_jaccard": jaccard(left_pollinators, right_pollinators),
                "interaction_pair_jaccard": jaccard(
                    {f"{plant}\t{pollinator}" for plant, pollinator in left_links},
                    {f"{plant}\t{pollinator}" for plant, pollinator in right_links},
                ),
                "n_shared_plants": len(left_plants & right_plants),
                "mean_shared_plant_pollinator_turnover": (
                    sum(float(row["pollinator_morisita_horn_turnover"]) for row in contrasts) / len(contrasts)
                    if contrasts
                    else None
                ),
            }
        )
        for row in contrasts:
            plant_rows.append({"left_island": left, "right_island": right, **row})
    return pair_rows, plant_rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    columns = list(rows[0])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", type=Path, default=Path("artifacts/ogasawara_zenodo/schema_audit.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/ogasawara_context_analysis"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    candidates = [row for row in schema.get("tables", []) if row.get("contextual_long_network_candidate")]
    if len(candidates) != 1:
        blocked = {
            "status": "blocked_schema_not_uniquely_resolved",
            "n_contextual_long_candidates": len(candidates),
            "candidate_tables": candidates,
            "next_gate": "Manually verify source-defined table roles or implement a wide-matrix parser after inspecting the source workbook.",
            "claim_boundary": schema.get("claim_boundary"),
        }
        (args.output_dir / "analysis_blocked.json").write_text(
            json.dumps(blocked, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(blocked["status"])
        return

    try:
        rows, columns = standardize_rows(candidates[0])
    except Exception as error:
        blocked = {
            "status": "blocked_source_semantics_or_parser",
            "error": repr(error),
            "candidate_table": candidates[0],
            "claim_boundary": schema.get("claim_boundary"),
        }
        (args.output_dir / "analysis_blocked.json").write_text(
            json.dumps(blocked, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(blocked["status"])
        return

    island_metrics = grouped_metrics(rows, ("island",))
    context_metrics = []
    for fields in (
        ("island", "season"),
        ("island", "habitat"),
        ("island", "anole_context"),
        ("island", "season", "habitat", "anole_context"),
    ):
        if any(str(row.get(field, "") or "").strip() for row in rows for field in fields[1:]):
            context_metrics.extend(grouped_metrics(rows, fields))
    pair_metrics, shared_plant_rows = island_pair_summaries(rows)

    summary = {
        "status": "source_resolved_descriptive_analysis",
        "source_table": candidates[0],
        "resolved_columns": columns,
        "n_positive_long_rows": len(rows),
        "n_islands": len({str(row["island"]) for row in rows}),
        "n_sites": len({str(row["site"]) for row in rows if str(row["site"])}),
        "n_seasons": len({str(row["season"]) for row in rows if str(row["season"])}),
        "n_plants": len({str(row["plant"]) for row in rows}),
        "n_pollinators": len({str(row["pollinator"]) for row in rows}),
        "total_legitimate_interaction_count": sum(float(row["interaction_count"]) for row in rows),
        "island_metrics": island_metrics,
        "context_metrics": context_metrics,
        "island_pair_metrics": pair_metrics,
        "claim_boundary": (
            "Descriptive contemporary interaction-count analysis only. The records do not identify per-visit effectiveness, effective dependency, reproductive success, historical adaptation, invasion causation, or a mainland-distance effect."
        ),
    }
    (args.output_dir / "analysis.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8"
    )
    write_csv(args.output_dir / "island_metrics.csv", island_metrics)
    write_csv(args.output_dir / "context_metrics.csv", context_metrics)
    write_csv(args.output_dir / "island_pair_metrics.csv", pair_metrics)
    write_csv(args.output_dir / "shared_plant_pair_contrasts.csv", shared_plant_rows)
    print(f"positive interaction rows: {len(rows)}")
    print(f"islands: {summary['n_islands']}")
    print(f"shared-plant pair contrasts: {len(shared_plant_rows)}")


if __name__ == "__main__":
    main()
