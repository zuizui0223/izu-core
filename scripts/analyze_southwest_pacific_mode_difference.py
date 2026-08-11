#!/usr/bin/env python3
"""Directly test animal-vs-wind flower-size slope differences."""
from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path
from statistics import fmean
from typing import Any, Mapping, Sequence

from scripts.analyze_southwest_pacific_flower_size import (
    model_vectors,
    ordinary_least_squares,
    percentile,
    pollination_syndrome,
    read_source_rows,
    stable_seed,
    valid_flower_size,
)


def slope(rows: Sequence[Mapping[str, Any]]) -> float:
    x, y = model_vectors(rows)
    return float(ordinary_least_squares(x, y)["slope"])


def mean_lr(rows: Sequence[Mapping[str, Any]]) -> float:
    return fmean(float(row["LR"]) for row in rows)


def split(rows: Sequence[Mapping[str, Any]]):
    valid = [row for row in rows if valid_flower_size(row)]
    animal = [row for row in valid if pollination_syndrome(row) == "animal"]
    wind = [row for row in valid if pollination_syndrome(row) == "wind"]
    if len(animal) < 3 or len(wind) < 3:
        raise ValueError("both pollination modes require at least three rows")
    return animal, wind


def summarize(values: Sequence[float]) -> dict[str, object]:
    ordered = sorted(values)
    return {
        "n_valid": len(ordered),
        "median": percentile(ordered, 0.5),
        "ci_95": [percentile(ordered, 0.025), percentile(ordered, 0.975)],
        "fraction_below_zero": sum(value < 0 for value in ordered) / len(ordered),
    }


def cluster_bootstrap(
    rows: Sequence[Mapping[str, Any]], cluster: str, repetitions: int
) -> dict[str, object]:
    grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        key = str(row.get(cluster) or "").strip()
        if key:
            grouped[key].append(row)
    keys = sorted(grouped)
    rng = random.Random(stable_seed(f"southwest-mode:{cluster}"))
    slope_diff: list[float] = []
    mean_diff: list[float] = []
    attempts = 0
    while len(slope_diff) < repetitions and attempts < repetitions * 10:
        attempts += 1
        sample: list[Mapping[str, Any]] = []
        for _ in keys:
            sample.extend(grouped[rng.choice(keys)])
        try:
            animal, wind = split(sample)
            slope_diff.append(slope(animal) - slope(wind))
            mean_diff.append(mean_lr(animal) - mean_lr(wind))
        except ValueError:
            continue
    if len(slope_diff) < max(100, repetitions // 2):
        raise RuntimeError(f"too few valid {cluster} bootstrap replicates")
    return {
        "cluster": cluster,
        "n_source_clusters": len(keys),
        "slope_difference": summarize(slope_diff),
        "mean_lr_difference": summarize(mean_diff),
    }


def event_bootstrap(animal, wind, repetitions: int) -> dict[str, object]:
    rng = random.Random(stable_seed("southwest-mode:event"))
    slope_diff = []
    mean_diff = []
    for _ in range(repetitions):
        aa = [animal[rng.randrange(len(animal))] for _ in animal]
        ww = [wind[rng.randrange(len(wind))] for _ in wind]
        slope_diff.append(slope(aa) - slope(ww))
        mean_diff.append(mean_lr(aa) - mean_lr(ww))
    return {
        "slope_difference": summarize(slope_diff),
        "mean_lr_difference": summarize(mean_diff),
    }


def analyse(rows: Sequence[Mapping[str, Any]], repetitions: int = 5000):
    animal, wind = split(rows)
    island = cluster_bootstrap(animal + wind, "Island", repetitions)
    family = cluster_bootstrap(animal + wind, "Family", repetitions)
    event = event_bootstrap(animal, wind, repetitions)
    island_ci = island["slope_difference"]["ci_95"]
    family_ci = family["slope_difference"]["ci_95"]
    robust = (island_ci[1] < 0 and family_ci[1] < 0) or (
        island_ci[0] > 0 and family_ci[0] > 0
    )
    return {
        "schema_version": "1.0",
        "status": "pollination_mode_slope_difference_audited",
        "n_animal": len(animal),
        "n_wind": len(wind),
        "animal_slope": slope(animal),
        "wind_slope": slope(wind),
        "animal_minus_wind_slope": slope(animal) - slope(wind),
        "animal_minus_wind_mean_lr": mean_lr(animal) - mean_lr(wind),
        "event_bootstrap": event,
        "island_cluster_bootstrap": island,
        "family_cluster_bootstrap": family,
        "robust_mode_difference": robust,
        "effect_registry_eligible": False,
        "causal_claim_allowed": False,
        "reading": "The animal-vs-wind slope difference is tested directly; significance in only one stratum is not itself evidence of a between-stratum difference.",
        "claim_boundary": "Pollination mode is not effective dependency or specialist/generalist status, and this contrast does not identify adaptive causation.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bootstrap-repetitions", type=int, default=5000)
    args = parser.parse_args()
    result = analyse(read_source_rows(args.source), args.bootstrap_repetitions)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result["animal_minus_wind_slope"])
    print(result["island_cluster_bootstrap"]["slope_difference"]["ci_95"])
    print(result["family_cluster_bootstrap"]["slope_difference"]["ci_95"])


if __name__ == "__main__":
    main()
