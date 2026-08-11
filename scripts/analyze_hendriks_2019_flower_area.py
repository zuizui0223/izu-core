#!/usr/bin/env python3
"""Audit the Hendriks (2019) flower-area island/mainland reconstruction.

The checked CSV is reconstructed from the author-uploaded thesis as indexed by
public search, not from a checksum-locked PDF.  This script therefore focuses on
reproducing reported numerical anchors and stress-testing the slope-to-isometry
claim; it deliberately does not emit a formally model-eligible cross-system
effect row.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
from pathlib import Path
from typing import Iterable, Sequence


EXPECTED_N = 35
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
    bootstrap = bootstrap_slopes(
        mainland_log,
        island_log,
        repetitions=bootstrap_repetitions,
        seed=seed,
    )

    ols_upper = float(bootstrap["ols_slope_percentiles"]["p97_5"])
    sma_upper = float(bootstrap["sma_slope_percentiles"]["p97_5"])

    return {
        "schema_version": "1.0",
        "status": "indexed_author_upload_numeric_reconstruction_audited",
        "n_pairs": len(rows),
        "transform": "natural log",
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
        "pair_bootstrap": bootstrap,
        "measurement_error_sensitivity": {
            "classical_x_error_model": "beta_observed = reliability_x * beta_true",
            "ols_point_below_isometry_if_reliability_exceeds": direct["slope"],
            "ols_bootstrap_upper_below_isometry_if_reliability_exceeds": ols_upper,
            "author_reported_ols_upper_below_isometry_if_reliability_exceeds": AUTHOR_MODEL2_CI[1],
            "sma_point_slope": sma,
            "sma_point_below_isometry": sma < 1.0,
            "sma_bootstrap_interval": [
                bootstrap["sma_slope_percentiles"]["p2_5"],
                sma_upper,
            ],
            "sma_bootstrap_interval_excludes_isometry": sma_upper < 1.0,
            "reading": "The direct OLS pattern is substantially less coupled than log(I/M) ~ log(M), but attenuation from error in mainland size can still move the corrected slope toward or above isometry. SMA is a structural sensitivity, not a uniquely identified measurement-error correction."
        },
        "formal_cross_system_fit_ready": False,
        "effect_registry_eligible": False,
        "blocking_gates": [
            "underlying PDF/data artifact not checksum locked",
            "island/family clustering for the 35 pairs not yet recovered into the checked table",
            "SMA pair-bootstrap interval includes the line-of-isometry slope of 1"
        ],
        "claim_boundary": "This reconstruction supports an independent descriptive replication of a starting-size-dependent island flower-area response under OLS. It does not identify pollinator mechanism, does not resolve measurement error, and is not admitted to the formal cross-system fit."
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
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
    if source.get("raw_pdf_checksum_locked") is not False:
        raise ValueError("unexpected source-lock state")

    result = analyze(
        read_pairs(args.input),
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
