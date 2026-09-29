#!/usr/bin/env python3
"""Audit archipelago-level heterogeneity in the Southwest Pacific flower-size data.

This is a descriptive robustness layer for the already source-locked 129-pair
analysis. It asks whether the animal-pollinated starting-size relationship is
broadly represented across source-defined island groups or is compatible with a
mixture of substantially different island-specific responses.

The script never recodes flower morphology or breeding system as pollinator
dependency. Individual colonisation events are nested within island groups; an
island-specific slope is reported only when at least five valid animal-pollinated
pairs with non-degenerate mainland flower-size variation are available.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Mapping, Sequence

import analyze_southwest_pacific_flower_size as base


MIN_SLOPE_PAIRS = 5
COLUMNS = (
    "island",
    "n_animal_valid",
    "n_families",
    "n_negative_lr",
    "n_positive_lr",
    "n_zero_lr",
    "mean_lr",
    "median_lr",
    "starting_value_slope_status",
    "ols_slope",
    "ols_slope_se",
    "event_bootstrap_ci_low",
    "event_bootstrap_ci_high",
    "mainland_sources",
    "row_role",
    "cross_system_model_eligible",
    "causal_claim_allowed",
)


def animal_rows(rows: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    return [
        row
        for row in rows
        if base.pollination_syndrome(row) == "animal"
        and base.valid_flower_size(row)
    ]


def island_groups(
    rows: Sequence[Mapping[str, Any]],
) -> dict[str, list[Mapping[str, Any]]]:
    grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in animal_rows(rows):
        island = base.clean_text(row.get("Island"))
        if not island:
            raise ValueError(
                f"animal pair {row.get('Pair number')} has no source-defined Island"
            )
        grouped[island].append(row)
    if not grouped:
        raise ValueError("no valid source-coded animal-pollinated island rows")
    return dict(sorted(grouped.items(), key=lambda item: item[0].casefold()))


def lr_values(rows: Sequence[Mapping[str, Any]]) -> list[float]:
    values = [base.numeric(row.get("LR")) for row in rows]
    return [float(value) for value in values if value is not None]


def island_record(
    island: str,
    rows: Sequence[Mapping[str, Any]],
    *,
    bootstrap_repetitions: int,
) -> dict[str, object]:
    values = lr_values(rows)
    if len(values) != len(rows):
        raise ValueError(f"valid animal rows unexpectedly lack LR on {island}")
    negative = sum(value < -1e-12 for value in values)
    positive = sum(value > 1e-12 for value in values)
    zero = len(values) - negative - positive
    predictors, responses = base.model_vectors(rows)
    status = "blocked_n_below_predeclared_minimum"
    slope = None
    slope_se = None
    ci_low = None
    ci_high = None
    if len(predictors) >= MIN_SLOPE_PAIRS and len(set(predictors)) >= 2:
        try:
            model = base.ordinary_least_squares(predictors, responses)
            bootstrap = base.bootstrap_slope(
                rows,
                cluster=None,
                repetitions=bootstrap_repetitions,
                seed_label=f"southwest_pacific_archipelago::{island}",
            )
            status = "estimated_descriptive_within_archipelago"
            slope = float(model["slope"])
            slope_se = float(model["slope_se"])
            ci_low, ci_high = [float(value) for value in bootstrap["ci_95"]]
        except (ValueError, RuntimeError):
            status = "blocked_degenerate_or_bootstrap_unstable"

    sources = Counter(base.clean_text(row.get("Mainland")) for row in rows)
    return {
        "island": island,
        "n_animal_valid": len(rows),
        "n_families": len({base.clean_text(row.get("Family")) for row in rows}),
        "n_negative_lr": negative,
        "n_positive_lr": positive,
        "n_zero_lr": zero,
        "mean_lr": statistics.fmean(values),
        "median_lr": statistics.median(values),
        "starting_value_slope_status": status,
        "ols_slope": slope,
        "ols_slope_se": slope_se,
        "event_bootstrap_ci_low": ci_low,
        "event_bootstrap_ci_high": ci_high,
        "mainland_sources": json.dumps(dict(sorted(sources.items())), separators=(",", ":")),
        "row_role": "within_archipelago_descriptive_sensitivity",
        "cross_system_model_eligible": "no",
        "causal_claim_allowed": "no",
    }


def summarize(records: Sequence[Mapping[str, object]]) -> dict[str, object]:
    estimated = [
        row
        for row in records
        if row["starting_value_slope_status"]
        == "estimated_descriptive_within_archipelago"
    ]
    slopes = [float(row["ols_slope"]) for row in estimated]
    mean_lrs = [float(row["mean_lr"]) for row in records]
    return {
        "schema_version": "1.0",
        "status": "archipelago_heterogeneity_descriptive_audit_complete",
        "source_id": "southwest_pacific_mainland_island_floral_pairs",
        "article_doi": "10.1093/aob/mcaf005",
        "source_file": "mcaf005_suppl_supplementary_data_s2.xlsx",
        "source_sheet": "Flower dataframe",
        "pollination_subset": "source-coded animal only; unresolved syndrome excluded",
        "minimum_pairs_for_island_slope": MIN_SLOPE_PAIRS,
        "n_archipelagos_with_valid_animal_pairs": len(records),
        "n_archipelagos_with_estimable_slope": len(estimated),
        "n_estimated_negative_slopes": sum(value < 0 for value in slopes),
        "n_estimated_positive_slopes": sum(value > 0 for value in slopes),
        "estimated_slope_range": [min(slopes), max(slopes)] if slopes else None,
        "estimated_slope_median": statistics.median(slopes) if slopes else None,
        "n_archipelagos_with_negative_mean_lr": sum(value < 0 for value in mean_lrs),
        "n_archipelagos_with_positive_mean_lr": sum(value > 0 for value in mean_lrs),
        "mean_lr_range": [min(mean_lrs), max(mean_lrs)] if mean_lrs else None,
        "reading": (
            "Archipelago-specific slopes and mean log response ratios are a descriptive heterogeneity audit. "
            "They test whether one global island-rule coefficient hides different regional response shapes; "
            "they do not make island groups independent experimental treatments or identify pollinator dependency."
        ),
        "claim_boundary": (
            "Flower morphology and source-coded pollination syndrome are not effective-dependency measures. "
            "Small archipelago subsets are not used for causal geological-origin claims, and these rows are not entered "
            "as independent effects in the cross-system registry."
        ),
    }


def analyse(
    rows: Sequence[Mapping[str, Any]], *, bootstrap_repetitions: int
) -> tuple[list[dict[str, object]], dict[str, object]]:
    records = [
        island_record(
            island,
            group,
            bootstrap_repetitions=bootstrap_repetitions,
        )
        for island, group in island_groups(rows).items()
    ]
    return records, summarize(records)


def write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def locate_analysis_file(input_dir: Path) -> Path:
    candidates = sorted(input_dir.rglob("mcaf005_suppl_supplementary_data_s2.xlsx"))
    if len(candidates) != 1:
        raise ValueError(
            f"expected exactly one S2 workbook under {input_dir}, found {len(candidates)}"
        )
    return candidates[0]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("artifacts/southwest_pacific_aob"),
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("artifacts/southwest_pacific_analysis/archipelago_heterogeneity.csv"),
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=Path("artifacts/southwest_pacific_analysis/archipelago_heterogeneity_summary.json"),
    )
    parser.add_argument("--bootstrap-repetitions", type=int, default=5000)
    args = parser.parse_args()

    source = locate_analysis_file(args.input_dir)
    rows = base.read_source_rows(source)
    records, summary = analyse(
        rows, bootstrap_repetitions=args.bootstrap_repetitions
    )
    write_csv(args.output_csv, records)
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"archipelagos: {summary['n_archipelagos_with_valid_animal_pairs']}")
    print(f"estimable slopes: {summary['n_archipelagos_with_estimable_slope']}")
    print(args.summary_output)


if __name__ == "__main__":
    main()
