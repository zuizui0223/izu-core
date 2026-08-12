#!/usr/bin/env python3
"""Restrict the Southwest Pacific source-method sensitivity to mixed-source islands."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from analyze_southwest_pacific_source_method_sensitivity import (
    island_cluster_interval,
    load_animal_pairs,
    ols_slope,
)


def analyze(rows, *, repetitions: int, seed: int) -> dict[str, object]:
    methods_by_island: dict[str, set[str]] = {}
    for row in rows:
        methods_by_island.setdefault(str(row["island"]), set()).add(str(row["source_method"]))
    mixed_islands = sorted(
        island
        for island, methods in methods_by_island.items()
        if {"Online databases", "Herbaria"}.issubset(methods)
    )
    overlap_rows = [row for row in rows if str(row["island"]) in mixed_islands]
    online_rows = [row for row in overlap_rows if row["source_method"] == "Online databases"]
    herbaria_rows = [row for row in overlap_rows if row["source_method"] == "Herbaria"]

    def record(subset, offset):
        interval = island_cluster_interval(
            subset, repetitions=repetitions, seed=seed + offset
        )
        estimate = ols_slope(subset)
        return {
            "n_pairs": len(subset),
            "n_islands": len({str(row["island"]) for row in subset}),
            "slope": estimate,
            "island_cluster_95": list(interval) if interval else None,
            "cluster_interval_wholly_below_isometry": bool(interval and interval[1] < 1.0),
        }

    online = record(online_rows, 0)
    return {
        "schema_version": "1.0",
        "analysis_role": "source_method_geographic_overlap_adversary",
        "mixed_source_islands": mixed_islands,
        "all_pairs_within_mixed_source_islands": record(overlap_rows, 1009),
        "online_only_within_mixed_source_islands": online,
        "herbaria_only_within_mixed_source_islands": record(herbaria_rows, 2018),
        "adversarial_reading": (
            "online_only_below_isometry_with_geographic_overlap_preserved"
            if online["cluster_interval_wholly_below_isometry"]
            else "overlap_restriction_removes_online_only_below_isometry"
        ),
        "formal_consequence": {
            "online_only_result_explained_by_nonoverlapping_island_composition": False
            if online["cluster_interval_wholly_below_isometry"]
            else None,
            "source_method_causal_effect_identified": False,
            "empirical_reliability_identified": False,
            "formal_admission_opened": False
        },
        "claim_boundary": "Restricting to islands represented by both source methods reduces geographic-composition confounding but does not randomize measurement source, estimate measurement reliability, or identify a source-method effect."
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--s1", type=Path, required=True)
    parser.add_argument("--s2", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bootstrap-repetitions", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=20260813)
    args = parser.parse_args()
    report = analyze(
        load_animal_pairs(args.s1, args.s2),
        repetitions=args.bootstrap_repetitions,
        seed=args.seed,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
