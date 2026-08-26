from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean

from scripts.run_response_geometry_parameter_robustness import (
    BASE,
    SWEEPS,
    TRAIT_GRID,
    apply_sweep,
    endpoint_on_trajectory,
    pollinator_trajectory,
    sign,
)

OUT = Path("data/results/response_geometry_realization_stability.json")


def realization_stability(cfg, replicates: int, seed: int) -> dict:
    mixed = 0
    all_positive = 0
    all_negative = 0
    other = 0
    switch_counts = []
    trait_positive = {trait: 0 for trait in TRAIT_GRID}
    trait_negative = {trait: 0 for trait in TRAIT_GRID}
    trait_deltas = {trait: [] for trait in TRAIT_GRID}

    for rep in range(replicates):
        run_seed = seed + rep * 10_000
        mainland = pollinator_trajectory(cfg.mainland, run_seed + 100_000, cfg)
        island = pollinator_trajectory(cfg.island, run_seed + 200_000, cfg)
        signs = []
        for trait in TRAIT_GRID:
            _, mainland_service = endpoint_on_trajectory(trait, mainland, cfg)
            _, island_service = endpoint_on_trajectory(trait, island, cfg)
            delta = island_service - mainland_service
            trait_deltas[trait].append(delta)
            value_sign = sign(delta)
            signs.append(value_sign)
            trait_positive[trait] += int(value_sign > 0)
            trait_negative[trait] += int(value_sign < 0)

        nonzero = [value for value in signs if value != 0]
        switches = sum(a != b for a, b in zip(nonzero, nonzero[1:]))
        switch_counts.append(switches)
        has_positive = 1 in signs
        has_negative = -1 in signs
        if has_positive and has_negative:
            mixed += 1
        elif has_positive and not has_negative:
            all_positive += 1
        elif has_negative and not has_positive:
            all_negative += 1
        else:
            other += 1

    trait_rows = []
    for trait in TRAIT_GRID:
        deltas = trait_deltas[trait]
        trait_rows.append({
            "initial_trait": trait,
            "mean_delta_service": mean(deltas),
            "mean_sign": sign(mean(deltas)),
            "positive_realization_fraction": trait_positive[trait] / replicates,
            "negative_realization_fraction": trait_negative[trait] / replicates,
        })

    mean_signs = [row["mean_sign"] for row in trait_rows]
    return {
        "replicates": replicates,
        "mixed_sign_realizations": mixed,
        "mixed_sign_realization_fraction": mixed / replicates,
        "all_positive_realizations": all_positive,
        "all_negative_realizations": all_negative,
        "other_realizations": other,
        "mean_switch_count_within_realization": mean(switch_counts),
        "mean_geometry_mixed_sign": 1 in mean_signs and -1 in mean_signs,
        "mean_geometry_all_positive": all(value >= 0 for value in mean_signs) and 1 in mean_signs,
        "mean_geometry_all_negative": all(value <= 0 for value in mean_signs) and -1 in mean_signs,
        "trait_rows": trait_rows,
    }


def build(replicates: int = 24, seed: int = 20260826) -> dict:
    baseline = realization_stability(BASE, replicates, seed)
    sweeps = {}
    settings_with_mixed = 0
    setting_count = 0
    for name, values in SWEEPS.items():
        rows = []
        for value in values:
            cfg = apply_sweep(BASE, name, value)
            result = realization_stability(cfg, replicates, seed + 10_000_000 + setting_count * 1_000_000)
            rows.append({"value": value, **result})
            settings_with_mixed += int(result["mixed_sign_realizations"] > 0)
            setting_count += 1
        sweeps[name] = rows

    classification = "stable_mean_geometry"
    if not baseline["mean_geometry_mixed_sign"] and baseline["mixed_sign_realization_fraction"] > 0:
        classification = "realization_contingent_branching_without_mean_sign_boundary"
    elif baseline["mean_geometry_mixed_sign"]:
        classification = "mean_sign_boundary_present"

    return {
        "analysis": "response_geometry_realization_stability",
        "status": "scientific_reassessment_gate_phase1b",
        "question": "Is mixed-sign branching a stable response boundary across plant starting positions, or does it arise conditionally within particular stochastic pollinator-community realizations?",
        "baseline": baseline,
        "baseline_classification": classification,
        "parameter_sweeps": sweeps,
        "robustness_summary": {
            "parameter_settings": setting_count,
            "settings_with_at_least_one_mixed_realization": settings_with_mixed,
            "fraction_settings_with_at_least_one_mixed_realization": settings_with_mixed / setting_count if setting_count else None,
        },
        "design": {
            "matched_pollinator_realization_across_all_trait_positions": True,
            "trait_grid": list(TRAIT_GRID),
            "replicates_per_setting": replicates,
            "empirical_inputs_loaded": [],
        },
        "interpretation_rule": "A mixed mean geometry supports a stable starting-position sign boundary. A one-sided mean geometry together with frequent mixed individual realizations instead implies that partner-community realization and starting position interact, so branching should not be attributed to starting position alone.",
        "claim_boundary": "This remains a synthetic model diagnostic. Realization-level branching frequency is a design robustness quantity, not a natural ecological prevalence estimate.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=24)
    parser.add_argument("--seed", type=int, default=20260826)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build(args.replicates, args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({
        "baseline_classification": payload["baseline_classification"],
        "baseline_mixed_realization_fraction": payload["baseline"]["mixed_sign_realization_fraction"],
        "mean_geometry_mixed_sign": payload["baseline"]["mean_geometry_mixed_sign"],
    }, indent=2))


if __name__ == "__main__":
    main()
