from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path
from statistics import mean, pstdev

from scripts.run_chapter2_conditional_why_diagnostics import realization_class_counts, two_way_decomposition
from scripts.run_response_geometry_parameter_robustness import BASE, TRAIT_GRID, make_pollinator, service

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_finite_community_system_size_freeze_20260908.json"
OUT = ROOT / "data/results/chapter2_finite_community_system_size_20260908.json"
COPY_SEED_STRIDE = 1_000_003


def terminal_pollinators(scenario, seed: int, cfg):
    rng = random.Random(seed)
    pollinators = [make_pollinator(rng, scenario, cfg) for _ in range(scenario.n_pollinator_types)]
    for _ in range(cfg.steps):
        pollinators = [p for p in pollinators if rng.random() >= scenario.partner_loss]
        if rng.random() < scenario.partner_arrival:
            pollinators.append(make_pollinator(rng, scenario, cfg))
    return tuple(pollinators)


def pooled_terminal_pollinators(scenario, seed: int, cfg, copies: int):
    pooled = []
    for copy_index in range(copies):
        pooled.extend(terminal_pollinators(scenario, seed + copy_index * COPY_SEED_STRIDE, cfg))
    return tuple(pooled)


def summarize_counts(values: list[int]) -> dict:
    mu = mean(values)
    sd = pstdev(values)
    return {
        "mean": mu,
        "sd": sd,
        "cv": sd / mu if mu else None,
        "empty_fraction": sum(value == 0 for value in values) / len(values),
        "min": min(values),
        "max": max(values),
    }


def response_matrix_for_scale(*, copies: int, seed: int, replicates: int):
    cfg = BASE.__class__(
        mainland=BASE.mainland,
        island=BASE.island,
        generalist_breadth=BASE.generalist_breadth,
        specialist_breadth=BASE.specialist_breadth,
        replacement_penalty=BASE.replacement_penalty,
        saturation=BASE.saturation,
        trait_adjustment=0.0,
        steps=BASE.steps,
    )
    matrix = [[] for _ in TRAIT_GRID]
    mainland_sizes = []
    island_sizes = []
    for rep in range(replicates):
        run_seed = seed + rep * 10_000
        mainland = pooled_terminal_pollinators(cfg.mainland, run_seed + 100_000, cfg, copies)
        island = pooled_terminal_pollinators(cfg.island, run_seed + 200_000, cfg, copies)
        mainland_sizes.append(len(mainland))
        island_sizes.append(len(island))
        for index, trait in enumerate(TRAIT_GRID):
            matrix[index].append(service(trait, island, cfg) - service(trait, mainland, cfg))
    return matrix, mainland_sizes, island_sizes


def summarize_scale(*, copies: int, seed: int, replicates: int) -> dict:
    matrix, mainland_sizes, island_sizes = response_matrix_for_scale(copies=copies, seed=seed, replicates=replicates)
    decomposition = two_way_decomposition(matrix)
    return {
        "copies": copies,
        "seed": seed,
        "realization_class_counts": realization_class_counts(matrix),
        "sum_of_squares_fraction": decomposition["sum_of_squares_fraction"],
        "additive_sign_mismatch_fraction": decomposition["additive_sign_mismatch_fraction"],
        "final_pollinator_count": {
            "mainland_like": summarize_counts(mainland_sizes),
            "island_like": summarize_counts(island_sizes),
        },
    }


def _range(rows: list[dict], path: tuple[str, ...]):
    values = []
    for row in rows:
        value = row
        for key in path:
            value = value[key]
        values.append(float(value))
    return [min(values), max(values)]


def build() -> dict:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    if design.get("status") != "fixed_before_execution":
        raise ValueError("finite-community system-size design is not frozen")
    replicates = int(design["baseline"]["matched_community_realizations"])
    rows = []
    for copies in design["system_size_scaling"]["copy_counts"]:
        for seed in design["seed_ensemble"]["values"]:
            rows.append(summarize_scale(copies=int(copies), seed=int(seed), replicates=replicates))

    by_scale = []
    for copies in design["system_size_scaling"]["copy_counts"]:
        selected = [row for row in rows if row["copies"] == copies]
        by_scale.append({
            "copies": copies,
            "seed_count": len(selected),
            "mixed_sign_count_range": _range(selected, ("realization_class_counts", "mixed_sign")),
            "community_realization_fraction_range": _range(selected, ("sum_of_squares_fraction", "community_realization")),
            "nonadditivity_fraction_range": _range(selected, ("sum_of_squares_fraction", "starting_position_by_community_nonadditivity")),
            "mainland_final_count_cv_range": _range(selected, ("final_pollinator_count", "mainland_like", "cv")),
            "island_final_count_cv_range": _range(selected, ("final_pollinator_count", "island_like", "cv")),
            "island_empty_fraction_range": _range(selected, ("final_pollinator_count", "island_like", "empty_fraction")),
        })

    return {
        "schema_version": "1.0",
        "analysis": "chapter2_finite_community_system_size",
        "status": "complete_from_prespecified_20260908_freeze",
        "design": DESIGN.relative_to(ROOT).as_posix(),
        "rows": rows,
        "scale_summary": by_scale,
        "interpretation_boundary": design["claim_boundary"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["scale_summary"], indent=2))


if __name__ == "__main__":
    main()
