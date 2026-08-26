from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import asdict, replace
from pathlib import Path
from statistics import mean

from scripts.run_response_geometry_parameter_robustness import BASE, TRAIT_GRID, apply_sweep
from scripts.run_response_geometry_realization_stability import realization_stability

OUT = Path("data/results/joint_response_transition_surface.json")

PARAMETER_RANGES = {
    "trait_dispersion_multiplier": (0.5, 1.5),
    "generalist_fraction_shift": (-0.20, 0.20),
    "replacement_fraction_shift": (-0.15, 0.15),
    "partner_loss_multiplier": (0.5, 1.5),
    "partner_arrival_multiplier": (0.5, 1.5),
    "saturation": (1.0, 3.0),
    "trait_adjustment": (0.0, 0.06),
    "generalist_breadth": (0.30, 0.54),
    "specialist_breadth": (0.10, 0.22),
    "replacement_penalty": (0.65, 1.0),
}


def latin_hypercube(n: int, seed: int) -> list[dict[str, float]]:
    if n < 2:
        raise ValueError("n must be at least 2")
    rng = random.Random(seed)
    names = tuple(PARAMETER_RANGES)
    columns = {}
    for name in names:
        lo, hi = PARAMETER_RANGES[name]
        bins = list(range(n))
        rng.shuffle(bins)
        values = []
        for bin_index in bins:
            u = (bin_index + rng.random()) / n
            values.append(lo + u * (hi - lo))
        columns[name] = values
    return [
        {name: columns[name][row] for name in names}
        for row in range(n)
    ]


def config_from_point(point: dict[str, float]):
    cfg = BASE
    for name, value in point.items():
        cfg = apply_sweep(cfg, name, value)
    return cfg


def classify(result: dict) -> str:
    if result["mean_geometry_mixed_sign"]:
        return "mixed_mean_geometry"
    if result["mean_geometry_all_positive"]:
        return "all_positive_mean_geometry"
    if result["mean_geometry_all_negative"]:
        return "all_negative_mean_geometry"
    return "near_zero_or_fragmented_mean_geometry"


def trait_negative_fraction(result: dict) -> float:
    return sum(row["mean_sign"] < 0 for row in result["trait_rows"]) / len(TRAIT_GRID)


def pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) != len(ys) or len(xs) < 2:
        return None
    mx = mean(xs)
    my = mean(ys)
    dx = [x - mx for x in xs]
    dy = [y - my for y in ys]
    denom = math.sqrt(sum(x * x for x in dx) * sum(y * y for y in dy))
    if denom == 0:
        return None
    return sum(x * y for x, y in zip(dx, dy)) / denom


def build(points: int = 48, replicates: int = 12, seed: int = 20260826) -> dict:
    design = latin_hypercube(points, seed + 70_000_000)
    rows = []
    for index, point in enumerate(design):
        cfg = config_from_point(point)
        result = realization_stability(cfg, replicates, seed + 80_000_000)
        rows.append({
            "point_index": index,
            "parameters": point,
            "classification": classify(result),
            "mixed_sign_realization_fraction": result["mixed_sign_realization_fraction"],
            "mean_switch_count_within_realization": result["mean_switch_count_within_realization"],
            "negative_trait_grid_fraction": trait_negative_fraction(result),
            "trait_rows": result["trait_rows"],
        })

    classes = sorted({row["classification"] for row in rows})
    class_counts = {name: sum(row["classification"] == name for row in rows) for name in classes}
    associations = {}
    for name in PARAMETER_RANGES:
        xs = [row["parameters"][name] for row in rows]
        associations[name] = {
            "r_with_negative_trait_grid_fraction": pearson(xs, [row["negative_trait_grid_fraction"] for row in rows]),
            "r_with_mixed_sign_realization_fraction": pearson(xs, [row["mixed_sign_realization_fraction"] for row in rows]),
        }

    return {
        "analysis": "joint_response_transition_surface",
        "status": "scientific_reassessment_gate_phase2",
        "question": "When key pollinator-reorganization and matching parameters vary jointly, which regions produce mixed, uniformly positive, or uniformly negative plant response geometry?",
        "design": {
            "sampling": "fixed_seed_latin_hypercube",
            "points": points,
            "replicates_per_point": replicates,
            "trait_grid": list(TRAIT_GRID),
            "parameter_ranges": {name: list(bounds) for name, bounds in PARAMETER_RANGES.items()},
            "common_seed_ensemble_across_parameter_points": True,
            "empirical_inputs_loaded": [],
        },
        "class_counts": class_counts,
        "class_fractions": {name: count / points for name, count in class_counts.items()},
        "parameter_associations": associations,
        "points": rows,
        "interpretation_rule": "A Research Article-level robustness claim requires mixed response geometry to occupy a nontrivial region of the joint parameter design rather than a narrow isolated setting. Associations are descriptive transition-surface diagnostics, not causal effect estimates.",
        "failure_rule": "If mixed geometry is rare or confined to a narrow parameter corner, do not retune toward it; demote the branching result and retain the three-layer conceptual decomposition as the stronger product.",
        "claim_boundary": "This is a synthetic joint robustness design with no empirical calibration. Latin-hypercube frequencies describe the declared design volume only and must not be interpreted as natural ecological prevalence.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--points", type=int, default=48)
    parser.add_argument("--replicates", type=int, default=12)
    parser.add_argument("--seed", type=int, default=20260826)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build(args.points, args.replicates, args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"class_counts": payload["class_counts"], "class_fractions": payload["class_fractions"]}, indent=2))


if __name__ == "__main__":
    main()
