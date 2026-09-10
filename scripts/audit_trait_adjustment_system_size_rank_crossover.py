from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import median

from scripts.audit_chapter2_finite_community_system_size import COPY_SEED_STRIDE
from scripts.run_chapter2_conditional_why_diagnostics import realization_class_counts, two_way_decomposition
from scripts.run_response_geometry_parameter_robustness import (
    BASE,
    TRAIT_GRID,
    endpoint_on_trajectory,
    pollinator_trajectory,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_trait_adjustment_system_size_rank_crossover_freeze_20260910.json"
OUT = ROOT / "data/results/chapter2_trait_adjustment_system_size_rank_crossover_20260910.json"


def pooled_trajectory(scenario, seed: int, cfg, copies: int):
    trajectories = [
        pollinator_trajectory(scenario, seed + copy_index * COPY_SEED_STRIDE, cfg)
        for copy_index in range(copies)
    ]
    return tuple(
        tuple(pollinator for trajectory in trajectories for pollinator in trajectory[step])
        for step in range(cfg.steps)
    )


def response_matrix_for_scale(*, copies: int, seed: int, replicates: int):
    if abs(BASE.trait_adjustment - 0.03) > 1e-12:
        raise ValueError("headline BASE.trait_adjustment is no longer 0.03")
    matrix = [[] for _ in TRAIT_GRID]
    for rep in range(replicates):
        run_seed = seed + rep * 10_000
        mainland = pooled_trajectory(BASE.mainland, run_seed + 100_000, BASE, copies)
        island = pooled_trajectory(BASE.island, run_seed + 200_000, BASE, copies)
        for index, trait in enumerate(TRAIT_GRID):
            _, mainland_service = endpoint_on_trajectory(trait, mainland, BASE)
            _, island_service = endpoint_on_trajectory(trait, island, BASE)
            matrix[index].append(island_service - mainland_service)
    return matrix


def summarize_scale(*, copies: int, seed: int, replicates: int) -> dict:
    matrix = response_matrix_for_scale(copies=copies, seed=seed, replicates=replicates)
    decomposition = two_way_decomposition(matrix)
    fractions = decomposition["sum_of_squares_fraction"]
    return {
        "copies": copies,
        "seed": seed,
        "realization_class_counts": realization_class_counts(matrix),
        "sum_of_squares_fraction": fractions,
        "starting_exceeds_community": (
            fractions["starting_position"] > fractions["community_realization"]
        ),
        "additive_sign_mismatch_fraction": decomposition["additive_sign_mismatch_fraction"],
    }


def build() -> dict:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    if design.get("status") != "frozen_before_execution":
        raise ValueError("rank-crossover design is not frozen")
    if float(design["trait_adjustment"]) != BASE.trait_adjustment:
        raise ValueError("frozen trait_adjustment differs from headline BASE")

    copies_values = [int(value) for value in design["system_size_multipliers"]]
    seeds = [int(value) for value in design["matching_seeds"]]
    replicates = int(design["realizations_per_seed"])
    rows = [
        summarize_scale(copies=copies, seed=seed, replicates=replicates)
        for copies in copies_values
        for seed in seeds
    ]

    scale_summary = []
    median_start = []
    median_community = []
    for copies in copies_values:
        selected = [row for row in rows if row["copies"] == copies]
        starts = [row["sum_of_squares_fraction"]["starting_position"] for row in selected]
        communities = [row["sum_of_squares_fraction"]["community_realization"] for row in selected]
        nonadds = [
            row["sum_of_squares_fraction"]["starting_position_by_community_nonadditivity"]
            for row in selected
        ]
        mixed = [row["realization_class_counts"]["mixed_sign"] for row in selected]
        median_start.append(median(starts))
        median_community.append(median(communities))
        scale_summary.append({
            "copies": copies,
            "mixed_sign_count_range": [min(mixed), max(mixed)],
            "starting_position_fraction_range": [min(starts), max(starts)],
            "community_realization_fraction_range": [min(communities), max(communities)],
            "nonadditivity_fraction_range": [min(nonadds), max(nonadds)],
            "median_starting_position_fraction": median(starts),
            "median_community_realization_fraction": median(communities),
            "median_nonadditivity_fraction": median(nonadds),
            "seeds_starting_exceeds_community": sum(row["starting_exceeds_community"] for row in selected),
        })

    monotone_start = all(b > a for a, b in zip(median_start, median_start[1:]))
    monotone_community = all(b < a for a, b in zip(median_community, median_community[1:]))
    kmax_selected = [row for row in rows if row["copies"] == copies_values[-1]]
    kmax_crossovers = sum(row["starting_exceeds_community"] for row in kmax_selected)
    decision = kmax_crossovers >= 5 and monotone_start and monotone_community

    return {
        "schema_version": "1.0",
        "analysis": "chapter2_trait_adjustment_system_size_rank_crossover",
        "status": "complete_from_prespecified_20260910_freeze",
        "design": DESIGN.relative_to(ROOT).as_posix(),
        "rows": rows,
        "scale_summary": scale_summary,
        "decision": {
            "seed_stable_rank_crossover": decision,
            "kmax": copies_values[-1],
            "kmax_seeds_starting_exceeds_community": kmax_crossovers,
            "required_kmax_seed_count": 5,
            "median_starting_share_strictly_increases": monotone_start,
            "median_community_share_strictly_decreases": monotone_community,
        },
        "interpretation_boundary": design["claim_boundary"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"scale_summary": payload["scale_summary"], "decision": payload["decision"]}, indent=2))


if __name__ == "__main__":
    main()
