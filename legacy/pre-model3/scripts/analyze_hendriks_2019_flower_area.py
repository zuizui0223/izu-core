#!/usr/bin/env python3
"""Audit the Hendriks (2019) flower-area island/mainland reconstruction.

The checked numeric table is now tied to a checksum-locked institutional PDF.
The separate island mapping is reconstructed from Appendix-A island checklists
and checked against Table A14's flower-area frequency vector. This script
reproduces the reported OLS anchors and stress-tests the slope-to-isometry claim
at both pair and island-cluster levels; provenance completion does not by itself
emit a formally model-eligible effect because measurement-error and symmetric-
axis uncertainty remain separate gates.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Sequence


EXPECTED_N = 35
EXPECTED_ISLAND_COUNTS = {
    "Antipodes": 1,
    "Auckland": 1,
    "Campbell": 1,
    "Chatham": 10,
    "Kermadec": 4,
    "Lord Howe": 11,
    "Norfolk": 3,
    "Stewart": 1,
    "Three Kings": 3,
}
AUTHOR_MODEL1_SLOPE = -0.39
AUTHOR_MODEL1_CI = [-0.63, -0.16]
AUTHOR_MODEL2_SLOPE = 0.58
AUTHOR_MODEL2_CI = [0.36, 0.82]
DEFAULT_BOOTSTRAP_REPETITIONS = 20000
DEFAULT_SEED = 20260811


def mean(values: Sequence[float]) -> float:
    return sum(values) / len(values)


def percentile(sorted_values: Sequence[float], probability: float) -> float:
    if not sorted_values:
        raise ValueError("cannot take percentile of empty data")
    position = (len(sorted_values) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return sorted_values[lower]
    fraction = position - lower
    return sorted_values[lower] + fraction * (
        sorted_values[upper] - sorted_values[lower]
    )


def ordinary_least_squares(
    x: Sequence[float], y: Sequence[float]
) -> dict[str, float]:
    if len(x) != len(y) or len(x) < 3:
        raise ValueError("OLS requires equal vectors with at least three values")
    x_mean = mean(x)
    y_mean = mean(y)
    sxx = sum((value - x_mean) ** 2 for value in x)
    syy = sum((value - y_mean) ** 2 for value in y)
    sxy = sum((a - x_mean) * (b - y_mean) for a, b in zip(x, y))
    if sxx <= 0 or syy <= 0:
        raise ValueError("OLS requires nonzero variation")
    slope = sxy / sxx
    intercept = y_mean - slope * x_mean
    correlation = sxy / math.sqrt(sxx * syy)
    return {
        "intercept": intercept,
        "slope": slope,
        "correlation": correlation,
        "r_squared": correlation * correlation,
    }


def standard_major_axis(x: Sequence[float], y: Sequence[float]) -> float:
    if len(x) != len(y) or len(x) < 3:
        raise ValueError("SMA requires equal vectors with at least three values")
    x_mean = mean(x)
    y_mean = mean(y)
    sxx = sum((value - x_mean) ** 2 for value in x)
    syy = sum((value - y_mean) ** 2 for value in y)
    sxy = sum((a - x_mean) * (b - y_mean) for a, b in zip(x, y))
    if sxx <= 0 or syy <= 0:
        raise ValueError("SMA requires nonzero variation")
    sign = 1.0 if sxy >= 0 else -1.0
    return sign * math.sqrt(syy / sxx)


def summarize_bootstrap(
    ols_values: list[float],
    sma_values: list[float],
    *,
    repetitions: int,
    seed: int,
) -> dict[str, object]:
    if not ols_values or not sma_values:
        raise ValueError("no valid bootstrap replicates")
    ols_values.sort()
    sma_values.sort()
    return {
        "repetitions_requested": repetitions,
        "repetitions_valid": len(ols_values),
        "seed": seed,
        "ols_slope_percentiles": {
            "p2_5": percentile(ols_values, 0.025),
            "p50": percentile(ols_values, 0.5),
            "p97_5": percentile(ols_values, 0.975),
        },
        "sma_slope_percentiles": {
            "p2_5": percentile(sma_values, 0.025),
            "p50": percentile(sma_values, 0.5),
            "p97_5": percentile(sma_values, 0.975),
        },
    }


def bootstrap_slopes(
    x: Sequence[float],
    y: Sequence[float],
    repetitions: int = DEFAULT_BOOTSTRAP_REPETITIONS,
    seed: int = DEFAULT_SEED,
) -> dict[str, object]:
    rng = random.Random(seed)
    n = len(x)
    ols_values: list[float] = []
    sma_values: list[float] = []
    for _ in range(repetitions):
        indices = [rng.randrange(n) for _ in range(n)]
        xb = [x[index] for index in indices]
        yb = [y[index] for index in indices]
        try:
            ols_values.append(ordinary_least_squares(xb, yb)["slope"])
            sma_values.append(standard_major_axis(xb, yb))
        except ValueError:
            continue
    return summarize_bootstrap(
        ols_values,
        sma_values,
        repetitions=repetitions,
        seed=seed,
    )


def cluster_bootstrap_slopes(
    rows: Sequence[dict[str, object]],
    repetitions: int = DEFAULT_BOOTSTRAP_REPETITIONS,
    seed: int = DEFAULT_SEED,
) -> dict[str, object]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        group = str(row.get("island_group", ""))
        if not group:
            raise ValueError("cluster bootstrap requires island_group on every row")
        grouped[group].append(row)
    groups = sorted(grouped)
    if len(groups) < 2:
        raise ValueError("cluster bootstrap requires at least two island groups")

    rng = random.Random(seed)
    ols_values: list[float] = []
    sma_values: list[float] = []
    for _ in range(repetitions):
        sampled_groups = [rng.choice(groups) for _ in groups]
        sampled_rows: list[dict[str, object]] = []
        for group in sampled_groups:
            sampled_rows.extend(grouped[group])
        x = [math.log(float(row["mainland_flower_area_cm2"])) for row in sampled_rows]
        y = [math.log(float(row["island_flower_area_cm2"])) for row in sampled_rows]
        try:
            ols_values.append(ordinary_least_squares(x, y)["slope"])
            sma_values.append(standard_major_axis(x, y))
        except ValueError:
            continue

    summary = summarize_bootstrap(
        ols_values,
        sma_values,
        repetitions=repetitions,
        seed=seed,
    )
    summary["cluster_unit"] = "Appendix-A island group"
    summary["n_clusters"] = len(groups)
    summary["clusters"] = groups
    return summary


def read_pairs(path: Path) -> list[dict[str, object]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != EXPECTED_N:
        raise ValueError(f"expected {EXPECTED_N} flower-area pairs, found {len(rows)}")
    parsed: list[dict[str, object]] = []
    pair_ids: set[int] = set()
    for row in rows:
        pair_id = int(row["pair_id"])
        island = float(row["island_flower_area_cm2"])
        mainland = float(row["mainland_flower_area_cm2"])
        if island <= 0 or mainland <= 0:
            raise ValueError(f"pair {pair_id} has nonpositive flower area")
        if pair_id in pair_ids:
            raise ValueError(f"duplicate pair_id {pair_id}")
        pair_ids.add(pair_id)
        parsed.append(
            {
                "pair_id": pair_id,
                "island_species": row["island_species"],
                "island_flower_area_cm2": island,
                "mainland_relative": row["mainland_relative"],
                "mainland_flower_area_cm2": mainland,
            }
        )
    if pair_ids != set(range(1, EXPECTED_N + 1)):
        raise ValueError("pair IDs must be consecutive 1..35")
    return parsed


def read_island_mapping(path: Path) -> dict[int, dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != EXPECTED_N:
        raise ValueError(f"expected {EXPECTED_N} island mappings, found {len(rows)}")
    mapping: dict[int, dict[str, str]] = {}
    for row in rows:
        pair_id = int(row["pair_id"])
        if pair_id in mapping:
            raise ValueError(f"duplicate mapped pair_id {pair_id}")
        mapping[pair_id] = {
            "island_species": row["island_species"],
            "island_group": row["island_group"],
            "appendix_source_table": row["appendix_source_table"],
        }
    if set(mapping) != set(range(1, EXPECTED_N + 1)):
        raise ValueError("mapped pair IDs must be consecutive 1..35")
    counts = Counter(row["island_group"] for row in mapping.values())
    if dict(sorted(counts.items())) != dict(sorted(EXPECTED_ISLAND_COUNTS.items())):
        raise ValueError(
            f"island mapping does not match Table A14 flower-area counts: {dict(counts)}"
        )
    return mapping


def attach_island_mapping(
    rows: Sequence[dict[str, object]], mapping: dict[int, dict[str, str]]
) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for row in rows:
        pair_id = int(row["pair_id"])
        mapped = mapping[pair_id]
        if str(row["island_species"]).casefold() != mapped["island_species"].casefold():
            raise ValueError(f"island species mismatch for pair {pair_id}")
        enriched = dict(row)
        enriched["island_group"] = mapped["island_group"]
        enriched["appendix_source_table"] = mapped["appendix_source_table"]
        result.append(enriched)
    return result


def leave_one_island_slopes(rows: Sequence[dict[str, object]]) -> dict[str, object]:
    groups = sorted({str(row["island_group"]) for row in rows})
    estimates: dict[str, dict[str, float | int]] = {}
    for omitted in groups:
        kept = [row for row in rows if row["island_group"] != omitted]
        x = [math.log(float(row["mainland_flower_area_cm2"])) for row in kept]
        y = [math.log(float(row["island_flower_area_cm2"])) for row in kept]
        estimates[omitted] = {
            "n_pairs": len(kept),
            "ols_slope": ordinary_least_squares(x, y)["slope"],
            "sma_slope": standard_major_axis(x, y),
        }
    ols_slopes = [float(value["ols_slope"]) for value in estimates.values()]
    sma_slopes = [float(value["sma_slope"]) for value in estimates.values()]
    return {
        "estimates": estimates,
        "ols_slope_range": [min(ols_slopes), max(ols_slopes)],
        "sma_slope_range": [min(sma_slopes), max(sma_slopes)],
        "all_leave_one_island_ols_below_isometry": max(ols_slopes) < 1.0,
        "all_leave_one_island_sma_below_isometry": max(sma_slopes) < 1.0,
    }


def analyze(
    rows: Sequence[dict[str, object]],
    *,
    bootstrap_repetitions: int = DEFAULT_BOOTSTRAP_REPETITIONS,
    seed: int = DEFAULT_SEED,
) -> dict[str, object]:
    mainland_log = [
        math.log(float(row["mainland_flower_area_cm2"])) for row in rows
    ]
    island_log = [math.log(float(row["island_flower_area_cm2"])) for row in rows]
    log_ratio = [island - mainland for island, mainland in zip(island_log, mainland_log)]

    direct = ordinary_least_squares(mainland_log, island_log)
    ratio_model = ordinary_least_squares(mainland_log, log_ratio)
    sma = standard_major_axis(mainland_log, island_log)
    pair_bootstrap = bootstrap_slopes(
        mainland_log,
        island_log,
        repetitions=bootstrap_repetitions,
        seed=seed,
    )

    has_island_groups = all(row.get("island_group") for row in rows)
    island_bootstrap = (
        cluster_bootstrap_slopes(
            rows,
            repetitions=bootstrap_repetitions,
            seed=seed,
        )
        if has_island_groups
        else None
    )
    leave_one = leave_one_island_slopes(rows) if has_island_groups else None

    pair_ols_upper = float(pair_bootstrap["ols_slope_percentiles"]["p97_5"])
    pair_sma_upper = float(pair_bootstrap["sma_slope_percentiles"]["p97_5"])
    island_ols_upper = (
        float(island_bootstrap["ols_slope_percentiles"]["p97_5"])
        if island_bootstrap
        else None
    )
    island_sma_upper = (
        float(island_bootstrap["sma_slope_percentiles"]["p97_5"])
        if island_bootstrap
        else None
    )

    return {
        "schema_version": "1.1",
        "status": "indexed_author_upload_numeric_and_island_cluster_reconstruction_audited",
        "n_pairs": len(rows),
        "transform": "natural log",
        "island_group_structure": {
            "available": has_island_groups,
            "n_groups": len({str(row["island_group"]) for row in rows})
            if has_island_groups
            else 0,
            "pair_counts": dict(
                sorted(Counter(str(row["island_group"]) for row in rows).items())
            )
            if has_island_groups
            else {},
            "matches_appendix_a14": has_island_groups
            and dict(
                sorted(Counter(str(row["island_group"]) for row in rows).items())
            )
            == dict(sorted(EXPECTED_ISLAND_COUNTS.items())),
        },
        "reconstructed_models": {
            "direct_log_island_on_log_mainland_ols": direct,
            "log_island_mainland_ratio_on_log_mainland_ols": ratio_model,
            "direct_log_island_on_log_mainland_sma_slope": sma,
        },
        "author_reported_anchors": {
            "model_1_slope": AUTHOR_MODEL1_SLOPE,
            "model_1_slope_95_ci": AUTHOR_MODEL1_CI,
            "model_2_slope": AUTHOR_MODEL2_SLOPE,
            "model_2_slope_95_ci": AUTHOR_MODEL2_CI,
        },
        "anchor_reproduction": {
            "direct_ols_absolute_slope_difference": abs(
                direct["slope"] - AUTHOR_MODEL2_SLOPE
            ),
            "direct_ols_reproduces_reported_slope_within_0_01": abs(
                direct["slope"] - AUTHOR_MODEL2_SLOPE
            )
            <= 0.01,
            "log_ratio_ols_absolute_slope_difference": abs(
                ratio_model["slope"] - AUTHOR_MODEL1_SLOPE
            ),
            "log_ratio_ols_reproduces_reported_slope_within_0_03": abs(
                ratio_model["slope"] - AUTHOR_MODEL1_SLOPE
            )
            <= 0.03,
            "reading": "The rounded Table B9 values closely reproduce both reported flower-area slope anchors; small differences are retained rather than silently corrected."
        },
        "pair_bootstrap": pair_bootstrap,
        "island_cluster_bootstrap": island_bootstrap,
        "leave_one_island": leave_one,
        "measurement_error_sensitivity": {
            "classical_x_error_model": "beta_observed = reliability_x * beta_true",
            "ols_point_below_isometry_if_reliability_exceeds": direct["slope"],
            "pair_bootstrap_upper_below_isometry_if_reliability_exceeds": pair_ols_upper,
            "island_cluster_bootstrap_upper_below_isometry_if_reliability_exceeds": island_ols_upper,
            "author_reported_ols_upper_below_isometry_if_reliability_exceeds": AUTHOR_MODEL2_CI[1],
            "sma_point_slope": sma,
            "sma_point_below_isometry": sma < 1.0,
            "pair_sma_bootstrap_interval": [
                pair_bootstrap["sma_slope_percentiles"]["p2_5"],
                pair_sma_upper,
            ],
            "pair_sma_bootstrap_interval_excludes_isometry": pair_sma_upper < 1.0,
            "island_cluster_sma_bootstrap_interval": [
                island_bootstrap["sma_slope_percentiles"]["p2_5"],
                island_sma_upper,
            ]
            if island_bootstrap
            else None,
            "island_cluster_sma_bootstrap_interval_excludes_isometry": (
                island_sma_upper < 1.0 if island_sma_upper is not None else None
            ),
            "reading": "The direct OLS pattern is not an artefact of treating the 35 pairs as independent: the Appendix-A island-cluster OLS interval remains below isometry. However, attenuation from error in mainland size can still move the corrected slope toward or above isometry, and both pair- and island-cluster SMA intervals include slope 1. SMA is a structural sensitivity, not a uniquely identified measurement-error correction."
        },
        "formal_cross_system_fit_ready": False,
        "effect_registry_eligible": False,
        "blocking_gates": [
            "mainland flower-area measurement reliability is not empirically identified",
            "SMA island-cluster bootstrap interval includes the line-of-isometry slope of 1"
        ],
        "claim_boundary": "The checksum-locked reconstruction supports an independent descriptive replication of a starting-size-dependent island flower-area response under OLS, including island-cluster resampling. Provenance is complete, but this does not identify pollinator mechanism, does not resolve errors in variables, and is not admitted to the formal cross-system fit."
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--island-mapping", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--bootstrap-repetitions",
        type=int,
        default=DEFAULT_BOOTSTRAP_REPETITIONS,
    )
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = parser.parse_args()

    source = json.loads(args.source.read_text(encoding="utf-8"))
    if source.get("reconstructed_numeric_pair_count") != EXPECTED_N:
        raise ValueError("source provenance does not declare 35 reconstructed pairs")
    if source.get("raw_pdf_checksum_locked") is not True:
        raise ValueError("Hendriks provenance requires checksum-locked institutional PDF bytes")
    strict = source.get("strict_locked_pdf_reverification") or {}
    if strict.get("provenance_gate_opened") is not True:
        raise ValueError("Hendriks strict locked-PDF reverification is incomplete")
    if strict.get("table_b9_pairs_verified") != EXPECTED_N:
        raise ValueError("Hendriks Table B9 locked-PDF reverification is incomplete")
    if strict.get("appendix_a_island_assignments_verified") != EXPECTED_N:
        raise ValueError("Hendriks Appendix-A locked-PDF reverification is incomplete")
    mapping_state = source.get("island_group_mapping") or {}
    if mapping_state.get("frequency_vector_matches_table_a14") is not True:
        raise ValueError("source provenance has not validated the Appendix-A mapping")

    rows = attach_island_mapping(
        read_pairs(args.input),
        read_island_mapping(args.island_mapping),
    )
    result = analyze(
        rows,
        bootstrap_repetitions=args.bootstrap_repetitions,
        seed=args.seed,
    )
    result["source_id"] = source["source_id"]
    result["source_retrieval_state"] = source["retrieval_state"]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(args.output)


if __name__ == "__main__":
    main()
