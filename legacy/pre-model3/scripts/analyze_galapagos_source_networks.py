#!/usr/bin/env python3
"""Analyse Galápagos multi-island networks only after source-schema admission."""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from statistics import mean
from typing import Iterable, Mapping, Sequence

from channel_id.external_archipelago_network import (
    WeightedNetwork,
    network_metrics as shared_network_metrics,
    shared_plant_contrasts,
)


def network_metrics(network: WeightedNetwork) -> dict[str, float | int | None]:
    """Expose the shared metrics plus the historical Galápagos weight alias."""
    result = dict(shared_network_metrics(network))
    result.setdefault("total_interaction_weight", result["total_visitation_rate"])
    return result


def norm(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value or "").strip().casefold()).strip("_")


def unique_role(record: Mapping[str, object], role: str, *, required: bool = True) -> str | None:
    values = list((record.get("role_matches") or {}).get(role) or [])
    if not values:
        if required:
            raise ValueError(f"required role {role!r} not resolved")
        return None
    if len(values) != 1:
        raise ValueError(f"role {role!r} ambiguous: {values}")
    return str(values[0])


def read_delimited(path: Path, delimiter: str | None) -> tuple[list[str], list[list[object]]]:
    with path.open(encoding="utf-8-sig", errors="replace", newline="") as handle:
        reader = csv.reader(handle, delimiter=delimiter or ",")
        rows = [list(row) for row in reader]
    while rows and not any(str(value or "").strip() for value in rows[0]):
        rows.pop(0)
    return ([str(value or "") for value in rows[0]], rows[1:]) if rows else ([], [])


def read_xlsx(path: Path, sheet: str) -> tuple[list[str], list[list[object]]]:
    import openpyxl

    workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
    worksheet = workbook[sheet]
    rows = [list(row) for row in worksheet.iter_rows(values_only=True)]
    workbook.close()
    while rows and not any(str(value or "").strip() for value in rows[0]):
        rows.pop(0)
    return ([str(value or "") for value in rows[0]], rows[1:]) if rows else ([], [])


def read_table(record: Mapping[str, object]) -> tuple[list[str], list[list[object]]]:
    path = Path(str(record["file"]))
    if path.suffix.casefold() in {".csv", ".tsv", ".txt"}:
        return read_delimited(path, str(record.get("delimiter") or ","))
    if path.suffix.casefold() in {".xlsx", ".xlsm"}:
        sheet = str(record.get("sheet") or "")
        if not sheet:
            raise ValueError("xlsx table lacks a sheet label")
        return read_xlsx(path, sheet)
    raise ValueError(f"unsupported table {path}")


def finite_nonnegative(value: object, label: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{label} is not numeric: {value!r}") from error
    if not math.isfinite(number) or number < 0:
        raise ValueError(f"{label} must be finite and non-negative")
    return number


def network_from_edges(rows: Iterable[Mapping[str, object]]) -> WeightedNetwork:
    rows = list(rows)
    plants = sorted({str(row["plant"]) for row in rows}, key=str.casefold)
    pollinators = sorted({str(row["pollinator"]) for row in rows}, key=str.casefold)
    plant_index = {value: index for index, value in enumerate(plants)}
    pollinator_index = {value: index for index, value in enumerate(pollinators)}
    matrix = [[0.0 for _ in pollinators] for _ in plants]
    for row in rows:
        matrix[plant_index[str(row["plant"])]][pollinator_index[str(row["pollinator"])]] += float(row["weight"])
    return WeightedNetwork.from_rows(plants, pollinators, matrix)


def parse_long_edge_table(record: Mapping[str, object]) -> dict[str, WeightedNetwork]:
    headers, rows = read_table(record)
    index = {header: position for position, header in enumerate(headers)}
    island_column = unique_role(record, "island")
    plant_column = unique_role(record, "plant")
    pollinator_column = unique_role(record, "pollinator")
    weight_column = unique_role(record, "interaction_weight")
    required = [island_column, plant_column, pollinator_column, weight_column]
    if any(column not in index for column in required):
        raise ValueError("resolved long-edge columns are absent from the source header")

    by_island: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row_number, values in enumerate(rows, start=2):
        island = str(values[index[island_column]] if index[island_column] < len(values) else "").strip()
        plant = str(values[index[plant_column]] if index[plant_column] < len(values) else "").strip()
        pollinator = str(values[index[pollinator_column]] if index[pollinator_column] < len(values) else "").strip()
        if not island or not plant or not pollinator:
            continue
        weight = finite_nonnegative(
            values[index[weight_column]] if index[weight_column] < len(values) else None,
            f"row {row_number} interaction weight",
        )
        if weight > 0:
            by_island[island].append({"plant": plant, "pollinator": pollinator, "weight": weight})
    if len(by_island) < 2:
        raise ValueError("long-edge table must resolve at least two islands")
    return {island: network_from_edges(group) for island, group in by_island.items()}


def clean_matrix_label(record: Mapping[str, object]) -> str:
    sheet = str(record.get("sheet") or "").strip()
    path = Path(str(record["file"]))
    candidates = [sheet, path.stem]
    generic = {"data", "matrix", "network", "interactions", "sheet1", "table"}
    for candidate in candidates:
        value = candidate.strip()
        if value and norm(value) not in generic:
            return value
    raise ValueError(f"matrix island label unresolved for {path} sheet={sheet!r}")


def parse_oriented_matrix(record: Mapping[str, object]) -> tuple[str, WeightedNetwork]:
    if not record.get("analysis_admissible_matrix"):
        raise ValueError("matrix is not schema-admissible")
    headers, rows = read_table(record)
    if len(headers) < 2:
        raise ValueError("matrix has fewer than two columns")
    orientation = str(record.get("matrix_orientation"))
    row_labels = []
    matrix = []
    for row_number, values in enumerate(rows, start=2):
        if not values:
            continue
        label = str(values[0] or "").strip()
        if not label:
            continue
        weights = []
        for column, header in enumerate(headers[1:], start=1):
            raw = values[column] if column < len(values) else 0
            if raw is None or str(raw).strip() == "":
                raw = 0
            weights.append(finite_nonnegative(raw, f"row {row_number} column {header!r}"))
        row_labels.append(label)
        matrix.append(weights)
    column_labels = [str(value or "").strip() for value in headers[1:]]
    if not row_labels or not all(column_labels):
        raise ValueError("matrix lacks identified row or column taxa")
    if orientation == "plants_by_pollinators":
        network = WeightedNetwork.from_rows(row_labels, column_labels, matrix)
    elif orientation == "pollinators_by_plants":
        transposed = [list(column) for column in zip(*matrix)]
        network = WeightedNetwork.from_rows(column_labels, row_labels, transposed)
    else:
        raise ValueError("matrix orientation unresolved")
    return clean_matrix_label(record), network


def jaccard(left: set[str], right: set[str]) -> float:
    union = left | right
    return 1.0 if not union else len(left & right) / len(union)


def pairwise_metrics(networks: Mapping[str, WeightedNetwork]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    summary = []
    plant_contrasts = []
    for left, right in combinations(sorted(networks, key=str.casefold), 2):
        first = networks[left]
        second = networks[right]
        contrasts = shared_plant_contrasts(first, second)
        first_links = {
            f"{plant}\t{pollinator}"
            for plant, row in zip(first.plant_names, first.matrix)
            for pollinator, weight in zip(first.pollinator_names, row)
            if weight > 0
        }
        second_links = {
            f"{plant}\t{pollinator}"
            for plant, row in zip(second.plant_names, second.matrix)
            for pollinator, weight in zip(second.pollinator_names, row)
            if weight > 0
        }
        summary.append(
            {
                "left_island": left,
                "right_island": right,
                "plant_jaccard": jaccard(set(first.plant_names), set(second.plant_names)),
                "pollinator_jaccard": jaccard(set(first.pollinator_names), set(second.pollinator_names)),
                "interaction_pair_jaccard": jaccard(first_links, second_links),
                "n_shared_plants": len(set(first.plant_names) & set(second.plant_names)),
                "mean_shared_plant_pollinator_turnover": (
                    mean(float(row["pollinator_morisita_horn_turnover"]) for row in contrasts)
                    if contrasts
                    else None
                ),
            }
        )
        plant_contrasts.extend({"left_island": left, "right_island": right, **row} for row in contrasts)
    return summary, plant_contrasts


def parse_covariates(record: Mapping[str, object]) -> list[dict[str, object]]:
    headers, rows = read_table(record)
    index = {header: position for position, header in enumerate(headers)}
    island_column = unique_role(record, "island")
    covariate_roles = [role for role in ("area", "isolation", "age", "elevation") if (record.get("role_matches") or {}).get(role)]
    columns = {role: unique_role(record, role) for role in covariate_roles}
    if island_column not in index or any(column not in index for column in columns.values()):
        raise ValueError("covariate headers do not match resolved schema")
    output = []
    for row_number, values in enumerate(rows, start=2):
        island = str(values[index[island_column]] if index[island_column] < len(values) else "").strip()
        if not island:
            continue
        row: dict[str, object] = {"island": island, "island_key": norm(island)}
        for role, column in columns.items():
            raw = values[index[column]] if index[column] < len(values) else None
            if raw is None or str(raw).strip() == "":
                row[role] = None
            else:
                row[role] = finite_nonnegative(raw, f"row {row_number} {role}")
        output.append(row)
    return output


def pearson(pairs: Sequence[tuple[float, float]]) -> float | None:
    if len(pairs) < 4:
        return None
    xs = [pair[0] for pair in pairs]
    ys = [pair[1] for pair in pairs]
    x_mean = mean(xs)
    y_mean = mean(ys)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in pairs)
    x_ss = sum((x - x_mean) ** 2 for x in xs)
    y_ss = sum((y - y_mean) ** 2 for y in ys)
    if x_ss <= 0 or y_ss <= 0:
        return None
    return numerator / math.sqrt(x_ss * y_ss)


def descriptive_covariate_links(
    island_metrics: Sequence[Mapping[str, object]],
    covariates: Sequence[Mapping[str, object]],
) -> list[dict[str, object]]:
    covariate_index = {str(row["island_key"]): row for row in covariates}
    metrics = ("plant_richness", "pollinator_richness", "link_richness", "weighted_shannon", "connectance")
    predictors = ("area", "isolation", "age", "elevation")
    output = []
    for predictor in predictors:
        for metric in metrics:
            pairs = []
            islands = []
            for row in island_metrics:
                covariate = covariate_index.get(norm(row["island"]))
                if not covariate or covariate.get(predictor) is None or row.get(metric) is None:
                    continue
                pairs.append((float(covariate[predictor]), float(row[metric])))
                islands.append(str(row["island"]))
            output.append(
                {
                    "predictor": predictor,
                    "network_metric": metric,
                    "n_islands": len(pairs),
                    "pearson_r": pearson(pairs),
                    "matched_islands": islands,
                    "status": "descriptive_only" if len(pairs) >= 4 else "insufficient_islands",
                }
            )
    return output


def write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    if not rows:
        return
    columns = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", type=Path, default=Path("artifacts/galapagos_dryad/schema_audit.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/galapagos_analysis"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    long_candidates = [row for row in schema.get("tables", []) if row.get("long_edge_list_candidate")]
    matrix_candidates = [row for row in schema.get("tables", []) if row.get("analysis_admissible_matrix")]
    networks: dict[str, WeightedNetwork] = {}
    source_mode = None
    try:
        if len(long_candidates) == 1:
            networks = parse_long_edge_table(long_candidates[0])
            source_mode = "single_long_edge_table"
        elif not long_candidates and len(matrix_candidates) >= 2:
            for record in matrix_candidates:
                label, network = parse_oriented_matrix(record)
                if norm(label) in {norm(existing) for existing in networks}:
                    raise ValueError(f"duplicate normalized island label {label!r}")
                networks[label] = network
            source_mode = "multiple_oriented_matrices"
        else:
            raise ValueError(
                f"network source not uniquely admitted: long={len(long_candidates)}, oriented_matrices={len(matrix_candidates)}"
            )
    except Exception as error:
        blocked = {
            "status": "blocked_network_source_not_resolved",
            "error": repr(error),
            "n_long_candidates": len(long_candidates),
            "n_oriented_matrix_candidates": len(matrix_candidates),
            "next_gate": "Inspect the source package and add an explicit source mapping rather than choosing a table or matrix orientation post hoc.",
            "claim_boundary": schema.get("claim_boundary"),
        }
        (args.output_dir / "analysis_blocked.json").write_text(
            json.dumps(blocked, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(blocked["status"])
        return

    island_metrics = [{"island": island, **network_metrics(network)} for island, network in sorted(networks.items())]
    pair_metrics, plant_contrasts = pairwise_metrics(networks)
    covariate_candidates = [row for row in schema.get("tables", []) if row.get("island_covariate_candidate")]
    covariates = []
    covariate_links = []
    covariate_status = "not_uniquely_resolved"
    if len(covariate_candidates) == 1:
        try:
            covariates = parse_covariates(covariate_candidates[0])
            covariate_links = descriptive_covariate_links(island_metrics, covariates)
            covariate_status = "descriptive_links_computed"
        except Exception as error:
            covariate_status = f"blocked:{error!r}"

    result = {
        "status": "source_resolved_multi_island_network_analysis",
        "source_mode": source_mode,
        "n_islands": len(networks),
        "island_metrics": island_metrics,
        "pair_metrics": pair_metrics,
        "n_shared_plant_pair_contrasts": len(plant_contrasts),
        "covariate_status": covariate_status,
        "covariates": covariates,
        "descriptive_covariate_links": covariate_links,
        "sampling_effort_candidate_count": schema.get("n_sampling_effort_candidates"),
        "claim_boundary": (
            "Source-native descriptive multi-island analysis. Pairwise turnover and metric-covariate correlations do not identify pollinator effectiveness, effective dependency, reproductive success, adaptive rewiring, or causal effects of island area, age or isolation. Sampling effort is not silently standardized when its source semantics are unresolved."
        ),
    }
    (args.output_dir / "analysis.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8"
    )
    write_csv(args.output_dir / "island_metrics.csv", island_metrics)
    write_csv(args.output_dir / "island_pair_metrics.csv", pair_metrics)
    write_csv(args.output_dir / "shared_plant_pair_contrasts.csv", plant_contrasts)
    write_csv(args.output_dir / "island_covariates.csv", covariates)
    write_csv(args.output_dir / "descriptive_covariate_links.csv", covariate_links)
    print(f"islands analysed: {len(networks)}")
    print(f"shared-plant pair contrasts: {len(plant_contrasts)}")
    print(f"covariate status: {covariate_status}")


if __name__ == "__main__":
    main()
