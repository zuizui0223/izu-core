#!/usr/bin/env python3
"""Estimate a non-transferable flower-measurement repeatability benchmark.

Tribulus contains repeated petal-length rows nested within source-defined `ID`.
This script uses those repetitions to estimate a one-way random-effects
repeatability benchmark.  The result is *not* an estimate of measurement
reliability for the Southwest Pacific or Hendriks sources.  Its role is only to
show the order of magnitude attainable in an independently measured floral trait
with repeated observations.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
from pathlib import Path
from statistics import median
from typing import Sequence


DEFAULT_BOOTSTRAP_REPETITIONS = 5000
DEFAULT_SEED = 20260811
# Current upper island-cluster coupling bound from the source-native Southwest
# Pacific animal analysis.  This is a comparison threshold only: Tribulus is
# never used to impute reliability into another system.
CROSS_SYSTEM_CLUSTER_THRESHOLD = 0.9258005353502381


def find_source_csv(source_dir: Path) -> Path:
    matches = sorted(source_dir.rglob("Tribulus_flower_data_clean.csv"))
    if len(matches) != 1:
        raise ValueError(
            f"expected exactly one Tribulus_flower_data_clean.csv under {source_dir}, found {len(matches)}"
        )
    return matches[0]


def read_repeated_groups(path: Path) -> tuple[list[list[float]], dict[str, int]]:
    grouped: dict[str, list[float]] = {}
    rows_total = 0
    rows_numeric = 0
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or "ID" not in reader.fieldnames or "petal_length" not in reader.fieldnames:
            raise ValueError("source CSV must contain ID and petal_length")
        for row in reader:
            rows_total += 1
            identifier = str(row.get("ID") or "").strip()
            raw = str(row.get("petal_length") or "").strip()
            if not identifier or not raw or raw.casefold() in {"na", "nan", "null"}:
                continue
            try:
                value = float(raw)
            except ValueError:
                continue
            if not math.isfinite(value):
                continue
            rows_numeric += 1
            grouped.setdefault(identifier, []).append(value)

    repeated = [values for values in grouped.values() if len(values) >= 2]
    return repeated, {
        "rows_total": rows_total,
        "rows_numeric_petal_length": rows_numeric,
        "ids_with_numeric_petal_length": len(grouped),
        "ids_with_repeated_petal_length": len(repeated),
        "numeric_rows_in_repeated_ids": sum(len(values) for values in repeated),
    }


def one_way_repeatability(groups: Sequence[Sequence[float]]) -> dict[str, float | int]:
    clean = [list(map(float, values)) for values in groups if len(values) >= 2]
    if len(clean) < 3:
        raise ValueError("repeatability requires at least three groups with repeated measurements")
    n_groups = len(clean)
    sizes = [len(values) for values in clean]
    n_obs = sum(sizes)
    if n_obs <= n_groups:
        raise ValueError("no within-group degrees of freedom")

    grand = sum(sum(values) for values in clean) / n_obs
    group_means = [sum(values) / len(values) for values in clean]
    ss_between = sum(
        len(values) * (group_mean - grand) ** 2
        for values, group_mean in zip(clean, group_means)
    )
    ss_within = sum(
        sum((value - group_mean) ** 2 for value in values)
        for values, group_mean in zip(clean, group_means)
    )
    df_between = n_groups - 1
    df_within = n_obs - n_groups
    ms_between = ss_between / df_between
    ms_within = ss_within / df_within

    # Effective group size for an unbalanced one-way random-effects design.
    n0 = (n_obs - sum(size * size for size in sizes) / n_obs) / df_between
    if n0 <= 0:
        raise ValueError("invalid effective group size")
    variance_between = max(0.0, (ms_between - ms_within) / n0)
    variance_within = max(0.0, ms_within)
    total = variance_between + variance_within
    single_icc = variance_between / total if total > 0 else 0.0
    mean_reliability_n0 = (
        variance_between / (variance_between + variance_within / n0)
        if variance_between + variance_within / n0 > 0
        else 0.0
    )
    return {
        "n_groups": n_groups,
        "n_observations": n_obs,
        "min_repeats_per_group": min(sizes),
        "median_repeats_per_group": float(median(sizes)),
        "max_repeats_per_group": max(sizes),
        "effective_group_size_n0": n0,
        "ms_between": ms_between,
        "ms_within": ms_within,
        "variance_between": variance_between,
        "variance_within": variance_within,
        "single_measurement_icc": single_icc,
        "mean_measurement_reliability_at_n0": mean_reliability_n0,
    }


def percentile(values: Sequence[float], probability: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] + fraction * (ordered[upper] - ordered[lower])


def cluster_bootstrap(
    groups: Sequence[Sequence[float]], *, repetitions: int, seed: int
) -> dict[str, object]:
    clean = [list(map(float, values)) for values in groups if len(values) >= 2]
    rng = random.Random(seed)
    single: list[float] = []
    means: list[float] = []
    for _ in range(repetitions):
        sampled = [rng.choice(clean) for _ in clean]
        try:
            result = one_way_repeatability(sampled)
        except ValueError:
            continue
        single.append(float(result["single_measurement_icc"]))
        means.append(float(result["mean_measurement_reliability_at_n0"]))
    if not single:
        raise ValueError("no valid repeatability bootstrap replicates")
    return {
        "repetitions_requested": repetitions,
        "repetitions_valid": len(single),
        "seed": seed,
        "single_measurement_icc_percentiles": {
            "p2_5": percentile(single, 0.025),
            "p50": percentile(single, 0.5),
            "p97_5": percentile(single, 0.975),
        },
        "mean_measurement_reliability_at_n0_percentiles": {
            "p2_5": percentile(means, 0.025),
            "p50": percentile(means, 0.5),
            "p97_5": percentile(means, 0.975),
        },
    }


def analyze(
    groups: Sequence[Sequence[float]],
    counts: dict[str, int],
    *,
    repetitions: int = DEFAULT_BOOTSTRAP_REPETITIONS,
    seed: int = DEFAULT_SEED,
) -> dict[str, object]:
    point = one_way_repeatability(groups)
    bootstrap = cluster_bootstrap(groups, repetitions=repetitions, seed=seed)
    return {
        "schema_version": "1.0",
        "status": "independent_flower_measurement_repeatability_benchmark_complete",
        "source_system": "Tribulus cistoides island-continent floral trait dataset",
        "source_unit": "repeated petal_length measurements nested within source-defined ID",
        "source_counts": counts,
        "one_way_random_effects_repeatability": point,
        "id_cluster_bootstrap": bootstrap,
        "cross_system_eiv_context": {
            "morphology_joint_cluster_reliability_threshold": CROSS_SYSTEM_CLUSTER_THRESHOLD,
            "single_measurement_icc_exceeds_threshold": float(point["single_measurement_icc"]) > CROSS_SYSTEM_CLUSTER_THRESHOLD,
            "id_mean_reliability_exceeds_threshold": float(point["mean_measurement_reliability_at_n0"]) > CROSS_SYSTEM_CLUSTER_THRESHOLD,
            "transfer_to_southwest_pacific_or_hendriks_allowed": False,
            "reading": "This independent repeated-flower dataset can contextualize whether very high floral measurement repeatability is plausible, but it cannot supply the unobserved reliability of either paired morphology source."
        },
        "effect_registry_eligible": False,
        "formal_morphology_eiv_gate_resolved": False,
        "claim_boundary": "Tribulus repeatability is a calibration benchmark only. Different species, observers, trait definitions, source summaries and measurement protocols prevent borrowing this ICC as the Southwest Pacific or Hendriks reliability."
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bootstrap-repetitions", type=int, default=DEFAULT_BOOTSTRAP_REPETITIONS)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = parser.parse_args()

    source_csv = find_source_csv(args.source_dir)
    groups, counts = read_repeated_groups(source_csv)
    result = analyze(
        groups,
        counts,
        repetitions=args.bootstrap_repetitions,
        seed=args.seed,
    )
    result["source_file"] = str(source_csv.relative_to(args.source_dir))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
