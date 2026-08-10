#!/usr/bin/env python3
"""Analyse source-published Galápagos network summaries without raw-row recovery.

The Dryad ZIP remains the required source for plant-by-pollinator matrices. The
article itself nevertheless publishes ten-island network descriptors (Table 1)
and observed/AIS/null nestedness summaries (Table 2). This script reproduces
only calculations supported by those table values:

* the reported approximately 69% observed-versus-AIS nestedness association;
* aggregate AIS and null prediction errors and interval coverage;
* an exact sign-flip test for the paired absolute-error difference;
* descriptive island-level correlations with leave-one-island ranges.

Published table rows are islands, not independent archipelagos. No result here
is admitted as a raw-network effect, partner-turnover effect, pollinator
effectiveness estimate, or geological-origin causal effect.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
from pathlib import Path
from statistics import mean, median
from typing import Iterable, Mapping, Sequence


REQUIRED_COLUMNS = (
    "island",
    "plant_richness",
    "pollinator_richness",
    "interaction_count",
    "weighted_connectance",
    "sampling_hours",
    "isolation_km",
    "area_km2",
    "age_ma",
    "observed_nestedness",
    "ais_prediction_mean",
    "ais_prediction_half_width_95",
    "null_prediction_mean",
    "null_prediction_half_width_95",
)
PREDICTORS = (
    "plant_richness",
    "pollinator_richness",
    "interaction_count",
    "weighted_connectance",
    "sampling_hours",
    "isolation_km",
    "area_km2",
    "age_ma",
    "log10_sampling_hours",
    "log10_area_km2",
)
DIAGNOSTIC_COLUMNS = (
    "island",
    "observed_nestedness",
    "ais_prediction_mean",
    "ais_prediction_low_95",
    "ais_prediction_high_95",
    "ais_residual",
    "ais_absolute_error",
    "ais_interval_covers_observed",
    "null_prediction_mean",
    "null_prediction_low_95",
    "null_prediction_high_95",
    "null_residual",
    "null_absolute_error",
    "null_interval_covers_observed",
    "absolute_error_improvement_null_minus_ais",
    "ais_lower_absolute_error",
)


def finite_float(value: object, label: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{label} is not numeric: {value!r}") from error
    if not math.isfinite(number):
        raise ValueError(f"{label} must be finite")
    return number


def load_table(path: Path) -> list[dict[str, object]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = sorted(set(REQUIRED_COLUMNS) - set(reader.fieldnames or ()))
        if missing:
            raise ValueError(f"published table missing columns: {missing}")
        rows: list[dict[str, object]] = []
        for line_number, source in enumerate(reader, start=2):
            island = str(source.get("island") or "").strip()
            if not island:
                raise ValueError(f"line {line_number} lacks island identity")
            row: dict[str, object] = {"island": island}
            for column in REQUIRED_COLUMNS[1:]:
                row[column] = finite_float(source.get(column), f"line {line_number} {column}")
            rows.append(row)
    validate_table(rows)
    for row in rows:
        row["log10_sampling_hours"] = math.log10(float(row["sampling_hours"]))
        row["log10_area_km2"] = math.log10(float(row["area_km2"]))
    return rows


def validate_table(rows: Sequence[Mapping[str, object]]) -> None:
    if len(rows) != 10:
        raise ValueError(f"expected the ten published islands, found {len(rows)}")
    islands = [str(row["island"]) for row in rows]
    if len(set(islands)) != len(islands):
        raise ValueError("published island identities must be unique")
    for row in rows:
        for column in REQUIRED_COLUMNS[1:]:
            value = float(row[column])
            if value < 0:
                raise ValueError(f"{row['island']} {column} must be non-negative")
        for column in (
            "weighted_connectance",
            "observed_nestedness",
            "ais_prediction_mean",
            "null_prediction_mean",
        ):
            if float(row[column]) > 1:
                raise ValueError(f"{row['island']} {column} exceeds one")
        if float(row["sampling_hours"]) <= 0 or float(row["area_km2"]) <= 0:
            raise ValueError("sampling effort and area must be positive")


def pearson(left: Sequence[float], right: Sequence[float]) -> float | None:
    if len(left) != len(right):
        raise ValueError("Pearson vectors must have equal length")
    if len(left) < 3:
        return None
    left_mean = mean(left)
    right_mean = mean(right)
    numerator = sum((x - left_mean) * (y - right_mean) for x, y in zip(left, right))
    left_ss = sum((x - left_mean) ** 2 for x in left)
    right_ss = sum((y - right_mean) ** 2 for y in right)
    if left_ss <= 0 or right_ss <= 0:
        return None
    return numerator / math.sqrt(left_ss * right_ss)


def rmse(values: Iterable[float]) -> float:
    values = list(values)
    if not values:
        raise ValueError("RMSE requires values")
    return math.sqrt(mean(value**2 for value in values))


def exact_sign_flip_pvalue(values: Sequence[float]) -> float | None:
    """Two-sided exact randomisation p-value for a paired mean difference."""
    values = [float(value) for value in values if abs(float(value)) > 1e-15]
    if not values:
        return None
    observed = mean(values)
    extreme = 0
    total = 0
    for signs in itertools.product((-1.0, 1.0), repeat=len(values)):
        permuted = mean(value * sign for value, sign in zip(values, signs))
        total += 1
        extreme += abs(permuted) >= abs(observed) - 1e-15
    return extreme / total


def interval_coverage(observed: float, centre: float, half_width: float) -> bool:
    return centre - half_width <= observed <= centre + half_width


def model_diagnostics(rows: Sequence[Mapping[str, object]]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    for row in rows:
        observed = float(row["observed_nestedness"])
        ais = float(row["ais_prediction_mean"])
        ais_half = float(row["ais_prediction_half_width_95"])
        null = float(row["null_prediction_mean"])
        null_half = float(row["null_prediction_half_width_95"])
        ais_residual = observed - ais
        null_residual = observed - null
        ais_error = abs(ais_residual)
        null_error = abs(null_residual)
        output.append(
            {
                "island": row["island"],
                "observed_nestedness": observed,
                "ais_prediction_mean": ais,
                "ais_prediction_low_95": ais - ais_half,
                "ais_prediction_high_95": ais + ais_half,
                "ais_residual": ais_residual,
                "ais_absolute_error": ais_error,
                "ais_interval_covers_observed": interval_coverage(observed, ais, ais_half),
                "null_prediction_mean": null,
                "null_prediction_low_95": null - null_half,
                "null_prediction_high_95": null + null_half,
                "null_residual": null_residual,
                "null_absolute_error": null_error,
                "null_interval_covers_observed": interval_coverage(observed, null, null_half),
                "absolute_error_improvement_null_minus_ais": null_error - ais_error,
                "ais_lower_absolute_error": ais_error < null_error,
            }
        )
    return output


def leave_one_out_correlations(
    rows: Sequence[Mapping[str, object]], predictor: str, response: str
) -> list[float]:
    values: list[float] = []
    for excluded in range(len(rows)):
        subset = [row for index, row in enumerate(rows) if index != excluded]
        correlation = pearson(
            [float(row[predictor]) for row in subset],
            [float(row[response]) for row in subset],
        )
        if correlation is not None:
            values.append(correlation)
    return values


def correlation_record(
    rows: Sequence[Mapping[str, object]], predictor: str, response: str
) -> dict[str, object]:
    correlation = pearson(
        [float(row[predictor]) for row in rows],
        [float(row[response]) for row in rows],
    )
    loo = leave_one_out_correlations(rows, predictor, response)
    return {
        "predictor": predictor,
        "response": response,
        "n_islands": len(rows),
        "pearson_r": correlation,
        "pearson_r_squared": correlation**2 if correlation is not None else None,
        "leave_one_island_r_min": min(loo) if loo else None,
        "leave_one_island_r_max": max(loo) if loo else None,
        "status": "descriptive_fixed_published_table_values",
    }


def analyse(rows: Sequence[Mapping[str, object]]) -> tuple[dict[str, object], list[dict[str, object]]]:
    diagnostics = model_diagnostics(rows)
    observed = [float(row["observed_nestedness"]) for row in rows]
    ais = [float(row["ais_prediction_mean"]) for row in rows]
    null = [float(row["null_prediction_mean"]) for row in rows]
    ais_r = pearson(observed, ais)
    null_r = pearson(observed, null)
    ais_residuals = [float(row["ais_residual"]) for row in diagnostics]
    null_residuals = [float(row["null_residual"]) for row in diagnostics]
    paired_improvement = [
        float(row["absolute_error_improvement_null_minus_ais"]) for row in diagnostics
    ]

    model_comparison = {
        "n_islands": len(rows),
        "observed_vs_ais_pearson_r": ais_r,
        "observed_vs_ais_r_squared": ais_r**2 if ais_r is not None else None,
        "observed_vs_null_pearson_r": null_r,
        "observed_vs_null_r_squared": null_r**2 if null_r is not None else None,
        "ais_mean_absolute_error": mean(abs(value) for value in ais_residuals),
        "null_mean_absolute_error": mean(abs(value) for value in null_residuals),
        "ais_root_mean_squared_error": rmse(ais_residuals),
        "null_root_mean_squared_error": rmse(null_residuals),
        "mean_absolute_error_improvement_null_minus_ais": mean(paired_improvement),
        "median_absolute_error_improvement_null_minus_ais": median(paired_improvement),
        "exact_paired_sign_flip_pvalue_for_mean_absolute_error_improvement": exact_sign_flip_pvalue(
            paired_improvement
        ),
        "n_islands_where_ais_has_lower_absolute_error": sum(
            bool(row["ais_lower_absolute_error"]) for row in diagnostics
        ),
        "n_ais_intervals_covering_observed": sum(
            bool(row["ais_interval_covers_observed"]) for row in diagnostics
        ),
        "n_null_intervals_covering_observed": sum(
            bool(row["null_interval_covers_observed"]) for row in diagnostics
        ),
        "published_69_percent_reproduced": (
            ais_r is not None and abs(ais_r**2 - 0.69) <= 0.01
        ),
        "reading": (
            "The source-published means reproduce the article's approximately 69% observed-versus-AIS association. AIS has lower aggregate MAE and RMSE than the null prediction, but lower absolute error on only four of ten islands and no paired sign-flip support for a consistent island-level improvement."
        ),
    }

    covariate_correlations = [
        correlation_record(rows, predictor, "observed_nestedness")
        for predictor in PREDICTORS
    ]
    summary: dict[str, object] = {
        "schema_version": "1.0",
        "status": "source_published_summary_analysis_complete",
        "source_id": "nnakenyi_et_al_2019_galapagos_published_tables",
        "article_doi": "10.1111/oik.06053",
        "dataset_doi": "10.5061/dryad.0c3cn5f",
        "source_scope": "article Tables 1 and 2; ten island-level published summary rows",
        "raw_dryad_network_source_recovered": False,
        "n_islands": len(rows),
        "model_comparison": model_comparison,
        "observed_nestedness_covariate_correlations": covariate_correlations,
        "effect_registry_eligible": False,
        "cross_system_model_eligible": False,
        "independent_unit": (
            "island within one Galápagos archipelago; ten islands do not constitute ten independent archipelagos"
        ),
        "uncertainty_boundary": (
            "Published AIS/null intervals describe simulation predictions. They are not sampling uncertainty for island-level network metrics, and leave-one-island ranges are sensitivity summaries rather than standard errors."
        ),
        "reading": (
            "While raw interaction matrices remain blocked, the article's published table values support a reproducible ten-island model-performance and covariate description. They reproduce the approximately 69% AIS association but do not establish universal adaptive rewiring, geological causation, partner turnover, or reproductive consequences."
        ),
        "next_gate": (
            "Recover data_galapagos_islands.zip or an author/institutional copy with matching provenance before calculating plant-level partner turnover, shared-species effects, or raw-network uncertainty."
        ),
        "claim_boundary": (
            "These are fixed source-published summaries. No raw plant-pollinator edges are reconstructed; no visit is relabelled as effectiveness; no island-level correlation is interpreted causally."
        ),
    }
    return summary, diagnostics


def write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=DIAGNOSTIC_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/source_tables/galapagos_nnakenyi_2019_tables_1_2.csv"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/results/galapagos/published_summary"),
    )
    args = parser.parse_args()
    rows = load_table(args.input)
    summary, diagnostics = analyse(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "analysis.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    write_csv(args.output_dir / "island_model_diagnostics.csv", diagnostics)
    print(f"islands: {summary['n_islands']}")
    print(
        "observed vs AIS R2: "
        f"{summary['model_comparison']['observed_vs_ais_r_squared']:.6f}"
    )
    print(
        "AIS lower absolute error: "
        f"{summary['model_comparison']['n_islands_where_ais_has_lower_absolute_error']}/10"
    )


if __name__ == "__main__":
    main()
