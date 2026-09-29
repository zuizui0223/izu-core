from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import median

import numpy as np

from scripts.audit_trait_adjustment_system_size_rank_crossover import pooled_trajectory_from_seeds
from scripts.chapter2_rng import scenario_copy_seeds
from scripts.run_chapter2_conditional_why_diagnostics import (
    realization_class_counts,
    two_way_decomposition,
)
from scripts.run_response_geometry_parameter_robustness import (
    BASE,
    EPS,
    clamp,
    encounter,
    endpoint_on_trajectory,
    pollinator_trajectory,
    service,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_postfreeze_grid_update_rule_challenge_20260925.json"
OUT = ROOT / "data/results/chapter2_postfreeze_grid_update_rule_challenge_20260925.json"

COMPONENTS = (
    "starting_position",
    "community_realization",
    "starting_position_by_community_nonadditivity",
)


def trait_grid(points: int) -> tuple[float, ...]:
    if points < 2:
        raise ValueError("trait grid requires at least two points")
    return tuple(i / (points - 1) for i in range(points))


def endpoint_with_rule(initial_trait, trajectory, cfg, rule: str):
    if rule == "threshold_best":
        return endpoint_on_trajectory(initial_trait, trajectory, cfg)
    if rule == "fixed":
        final_pollinators = trajectory[-1] if trajectory else ()
        return initial_trait, service(initial_trait, final_pollinators, cfg)
    if rule != "smooth_weighted":
        raise ValueError(f"unknown update rule: {rule}")

    trait = float(initial_trait)
    for pollinators in trajectory:
        if not pollinators or cfg.trait_adjustment <= 0.0:
            continue
        current_service = service(trait, pollinators, cfg)
        weights = [encounter(trait, pollinator, cfg) for pollinator in pollinators]
        total_weight = sum(weights)
        if total_weight <= EPS:
            continue
        centroid = sum(
            weight * pollinator.trait
            for weight, pollinator in zip(weights, pollinators)
        ) / total_weight
        trait = clamp(
            trait
            + cfg.trait_adjustment
            * (1.0 - current_service)
            * (centroid - trait)
        )
    final_pollinators = trajectory[-1] if trajectory else ()
    return trait, service(trait, final_pollinators, cfg)


def _encounter_matrix(traits: np.ndarray, pollinators, cfg) -> np.ndarray:
    if not pollinators:
        return np.empty((traits.size, 0), dtype=float)
    partner_traits = np.asarray([p.trait for p in pollinators], dtype=float)
    breadths = np.asarray([max(p.breadth, 1e-6) for p in pollinators], dtype=float)
    penalties = np.asarray(
        [cfg.replacement_penalty if p.introduced else 1.0 for p in pollinators],
        dtype=float,
    )
    mismatch = np.abs(traits[:, None] - partner_traits[None, :])
    matches = np.exp(-np.square(mismatch / breadths[None, :]))
    return np.clip(matches * penalties[None, :], 0.0, 1.0)


def _service_from_encounters(encounters: np.ndarray, cfg) -> np.ndarray:
    if encounters.shape[1] == 0:
        return np.zeros(encounters.shape[0], dtype=float)
    mean_match = encounters.mean(axis=1)
    return np.clip(1.0 - np.exp(-cfg.saturation * mean_match), 0.0, 1.0)


def services_for_grid(grid: tuple[float, ...], trajectory, cfg, rule: str) -> np.ndarray:
    traits = np.asarray(grid, dtype=float).copy()

    if rule == "fixed":
        final_pollinators = trajectory[-1] if trajectory else ()
        return _service_from_encounters(
            _encounter_matrix(traits, final_pollinators, cfg), cfg
        )

    if rule not in {"threshold_best", "smooth_weighted"}:
        raise ValueError(f"unknown update rule: {rule}")

    for pollinators in trajectory:
        if not pollinators or cfg.trait_adjustment <= 0.0:
            continue
        encounters = _encounter_matrix(traits, pollinators, cfg)
        current_service = _service_from_encounters(encounters, cfg)
        partner_traits = np.asarray([p.trait for p in pollinators], dtype=float)

        if rule == "threshold_best":
            mask = current_service < 0.45
            if np.any(mask):
                best_index = np.argmax(encounters, axis=1)
                targets = partner_traits[best_index]
                traits[mask] = (
                    traits[mask]
                    + cfg.trait_adjustment * (targets[mask] - traits[mask])
                )
        else:
            total_weight = encounters.sum(axis=1)
            mask = total_weight > EPS
            if np.any(mask):
                centroids = np.zeros_like(traits)
                centroids[mask] = (
                    encounters[mask] @ partner_traits
                ) / total_weight[mask]
                traits[mask] = (
                    traits[mask]
                    + cfg.trait_adjustment
                    * (1.0 - current_service[mask])
                    * (centroids[mask] - traits[mask])
                )
        traits = np.clip(traits, 0.0, 1.0)

    final_pollinators = trajectory[-1] if trajectory else ()
    return _service_from_encounters(
        _encounter_matrix(traits, final_pollinators, cfg), cfg
    )


def variants_from_design(design: dict) -> list[tuple[str, int]]:
    variants = [
        ("threshold_best", int(points))
        for points in design["grid_resolution_challenge"]["grid_points"]
    ]
    rule_grid = int(design["update_rule_challenge"]["grid_points"])
    variants.extend(
        (rule, rule_grid)
        for rule in design["update_rule_challenge"]["rules"]
        if (rule, rule_grid) not in variants
    )
    return variants


def summarize_matrix(matrix: list[list[float]], *, rule: str, grid_points: int, copies: int, seed: int) -> dict:
    decomposition = two_way_decomposition(matrix)
    fractions = decomposition["sum_of_squares_fraction"]
    raw = decomposition["sum_of_squares"]
    cells = len(matrix) * len(matrix[0])
    per_cell = {
        component: raw[component] / cells
        for component in COMPONENTS
    }
    winner = max(COMPONENTS, key=lambda component: fractions[component])
    return {
        "rule": rule,
        "grid_points": grid_points,
        "copies": copies,
        "seed": seed,
        "realization_class_counts": realization_class_counts(matrix),
        "sum_of_squares": raw,
        "sum_of_squares_per_cell": per_cell,
        "sum_of_squares_fraction": fractions,
        "dominant_component": winner,
        "community_exceeds_interaction": (
            fractions["community_realization"]
            > fractions["starting_position_by_community_nonadditivity"]
        ),
        "interaction_exceeds_community": (
            fractions["starting_position_by_community_nonadditivity"]
            > fractions["community_realization"]
        ),
        "additive_sign_mismatch_fraction": decomposition["additive_sign_mismatch_fraction"],
    }


def rows_for_seed_and_scale(*, design: dict, seed: int, copies: int) -> list[dict]:
    replicates = int(design["preserved"]["realizations_per_seed"])
    variants = variants_from_design(design)
    matrices = {
        variant: [[] for _ in trait_grid(variant[1])]
        for variant in variants
    }

    for rep in range(replicates):
        mainland_seeds = scenario_copy_seeds(seed, rep, 0, copies)
        island_seeds = scenario_copy_seeds(seed, rep, 1, copies)
        mainland = pooled_trajectory_from_seeds(BASE.mainland, mainland_seeds, BASE)
        island = pooled_trajectory_from_seeds(BASE.island, island_seeds, BASE)

        for rule, grid_points in variants:
            grid = trait_grid(grid_points)
            matrix = matrices[(rule, grid_points)]
            mainland_service = services_for_grid(grid, mainland, BASE, rule)
            island_service = services_for_grid(grid, island, BASE, rule)
            delta = island_service - mainland_service
            for index, value in enumerate(delta):
                matrix[index].append(float(value))

    return [
        summarize_matrix(
            matrices[(rule, grid_points)],
            rule=rule,
            grid_points=grid_points,
            copies=copies,
            seed=seed,
        )
        for rule, grid_points in variants
    ]


def _component_medians(rows: list[dict], key: str) -> dict[str, float]:
    return {
        component: median(row[key][component] for row in rows)
        for component in COMPONENTS
    }


def _winner(component_values: dict[str, float]) -> str:
    return max(COMPONENTS, key=lambda component: component_values[component])


def _log2_slope(k_values: list[int], values: list[float]) -> float | None:
    if any(value <= 0 for value in values):
        return None
    x = np.log2(np.asarray(k_values, dtype=float))
    y = np.log2(np.asarray(values, dtype=float))
    return float(np.polyfit(x, y, 1)[0])


def aggregate(rows: list[dict], design: dict) -> tuple[list[dict], dict]:
    k_values = [int(value) for value in design["preserved"]["system_size_multipliers"]]
    variants = variants_from_design(design)
    summary = []

    for rule, grid_points in variants:
        for copies in k_values:
            selected = [
                row for row in rows
                if row["rule"] == rule
                and row["grid_points"] == grid_points
                and row["copies"] == copies
            ]
            fraction_medians = _component_medians(selected, "sum_of_squares_fraction")
            ss_medians = _component_medians(selected, "sum_of_squares")
            per_cell_medians = _component_medians(selected, "sum_of_squares_per_cell")
            summary.append({
                "rule": rule,
                "grid_points": grid_points,
                "copies": copies,
                "median_sum_of_squares_fraction": fraction_medians,
                "median_sum_of_squares": ss_medians,
                "median_sum_of_squares_per_cell": per_cell_medians,
                "winner_by_median_fraction": _winner(fraction_medians),
                "seed_winner_counts": {
                    component: sum(row["dominant_component"] == component for row in selected)
                    for component in COMPONENTS
                },
                "median_mixed_sign_count": median(
                    row["realization_class_counts"]["mixed_sign"] for row in selected
                ),
            })

    scaling = {}
    for rule, grid_points in variants:
        key = f"{rule}|grid={grid_points}"
        selected = [
            row for row in summary
            if row["rule"] == rule and row["grid_points"] == grid_points
        ]
        selected.sort(key=lambda row: row["copies"])
        scaling[key] = {
            component: {
                "median_per_cell_ss_by_k": [
                    row["median_sum_of_squares_per_cell"][component]
                    for row in selected
                ],
                "log2_slope_vs_k": _log2_slope(
                    [row["copies"] for row in selected],
                    [
                        row["median_sum_of_squares_per_cell"][component]
                        for row in selected
                    ],
                ),
            }
            for component in COMPONENTS
        }

    return summary, scaling


def decisions(rows: list[dict], summary: list[dict], design: dict) -> dict:
    def median_winner(rule: str, grid_points: int, copies: int) -> str:
        for row in summary:
            if (
                row["rule"] == rule
                and row["grid_points"] == grid_points
                and row["copies"] == copies
            ):
                return row["winner_by_median_fraction"]
        raise KeyError((rule, grid_points, copies))

    grid_rows = []
    for grid_points in design["grid_resolution_challenge"]["grid_points"]:
        observed = {
            "k1": median_winner("threshold_best", int(grid_points), 1),
            "k4": median_winner("threshold_best", int(grid_points), 4),
            "k16": median_winner("threshold_best", int(grid_points), 16),
        }
        expected = {
            "k1": "community_realization",
            "k4": "starting_position_by_community_nonadditivity",
            "k16": "starting_position",
        }
        grid_rows.append({
            "grid_points": int(grid_points),
            "observed": observed,
            "expected": expected,
            "passes": observed == expected,
        })

    seeds = [int(value) for value in design["preserved"]["master_seeds"]]
    smooth_seed_rows = []
    for seed in seeds:
        selected = sorted(
            [
                row for row in rows
                if row["rule"] == "smooth_weighted"
                and row["grid_points"] == int(design["update_rule_challenge"]["grid_points"])
                and row["seed"] == seed
            ],
            key=lambda row: row["copies"],
        )
        baseline = selected[0]
        later = selected[1:]
        passes = (
            baseline["community_exceeds_interaction"]
            and any(row["interaction_exceeds_community"] for row in later)
        )
        first_crossover = next(
            (row["copies"] for row in later if row["interaction_exceeds_community"]),
            None,
        )
        smooth_seed_rows.append({
            "seed": seed,
            "community_exceeds_interaction_at_k1": baseline["community_exceeds_interaction"],
            "first_later_k_with_interaction_exceeds_community": first_crossover,
            "passes": passes,
        })

    required = 4
    smooth_pass_count = sum(row["passes"] for row in smooth_seed_rows)
    return {
        "grid_resolution_topology": {
            "rows": grid_rows,
            "passes": all(row["passes"] for row in grid_rows),
        },
        "smooth_weighted_ci_crossover": {
            "seed_rows": smooth_seed_rows,
            "passing_seeds": smooth_pass_count,
            "required_passing_seeds": required,
            "passes": smooth_pass_count >= required,
        },
        "fixed_rule": {
            "role": "negative_control_descriptive_only",
            "winner_sequence": {
                str(k): median_winner(
                    "fixed",
                    int(design["update_rule_challenge"]["grid_points"]),
                    k,
                )
                for k in design["preserved"]["system_size_multipliers"]
            },
        },
    }


def build() -> dict:
    from scripts.chapter2_simulation_integrity import verify_model
    provenance = verify_model(BASE)
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    if design.get("status") != "frozen_before_execution":
        raise ValueError("post-freeze challenge design is not frozen before execution")
    if abs(float(design["preserved"]["trait_adjustment"]) - BASE.trait_adjustment) > 1e-12:
        raise ValueError("challenge must preserve BASE.trait_adjustment")

    seeds = [int(value) for value in design["preserved"]["master_seeds"]]
    k_values = [int(value) for value in design["preserved"]["system_size_multipliers"]]

    rows = []
    for copies in k_values:
        for seed in seeds:
            rows.extend(rows_for_seed_and_scale(design=design, seed=seed, copies=copies))

    summary, scaling = aggregate(rows, design)
    decision = decisions(rows, summary, design)
    return {
        "schema_version": "1.0",
        "replay_integrity": provenance,
        "analysis": design["analysis"],
        "status": "complete_postfreeze_structural_challenge",
        "design": DESIGN.relative_to(ROOT).as_posix(),
        "rows": rows,
        "scale_summary": summary,
        "absolute_ss_scaling": scaling,
        "decision": decision,
        "claim_boundary": design["claim_boundary"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "decision": payload["decision"],
        "absolute_ss_scaling": payload["absolute_ss_scaling"],
    }, indent=2))


if __name__ == "__main__":
    main()
