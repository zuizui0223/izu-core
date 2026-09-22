from __future__ import annotations

import argparse
import json
import math
import multiprocessing as mp
import random
from collections import Counter
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_el_nonlinear_reduction import endpoint_vectorized, order_label, two_way_fractions
from scripts.chapter2_rng import scenario_copy_seeds
from scripts.run_response_geometry_parameter_robustness import BASE, pollinator_trajectory

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_el_dense_phase_map_freeze_20260913.json"
OUT = ROOT / "data/results/chapter2_el_dense_phase_map_20260913.json"


def clone_probability_for_pairwise_rho(rho: float) -> float:
    if not 0.0 <= rho <= 1.0:
        raise ValueError("rho must lie in [0,1]")
    return math.sqrt(rho)


def k_eff(k: int, rho: float) -> float:
    if k < 1:
        raise ValueError("k must be positive")
    return k / (1.0 + (k - 1.0) * rho)


def expected_distinct_trajectory_support(k: int, rho: float) -> float:
    if k < 1:
        raise ValueError("k must be positive")
    if rho == 0.0:
        return float(k)
    q = clone_probability_for_pairwise_rho(rho)
    return k * (1.0 - q) + 1.0 - (1.0 - q) ** k


def _pollinator_row(pollinator) -> tuple[float, float, float]:
    return (
        float(pollinator.trait),
        float(pollinator.breadth),
        float(BASE.replacement_penalty if pollinator.introduced else 1.0),
    )


def _as_arrays(trajectory) -> list[np.ndarray]:
    rows = []
    for snapshot in trajectory:
        if snapshot:
            rows.append(np.asarray([_pollinator_row(p) for p in snapshot], dtype=float).reshape((-1, 3)))
        else:
            rows.append(np.empty((0, 3), dtype=float))
    return rows


def _merge_trajectories(trajectories: list[list[np.ndarray]]) -> list[np.ndarray]:
    merged = []
    for step in range(BASE.steps):
        present = [trajectory[step] for trajectory in trajectories if len(trajectory[step])]
        merged.append(np.concatenate(present, axis=0) if present else np.empty((0, 3), dtype=float))
    return merged


def _point_set(design: dict) -> list[tuple[int, float]]:
    points = {
        (int(k), float(rho))
        for k in design["grid"]["k_values"]
        for rho in design["grid"]["rho_values"]
    }
    for contour in design["exact_contour_challenges"]:
        for k, rho in contour["points"]:
            points.add((int(k), float(rho)))
    return sorted(points)


def _seed_grid(args) -> tuple[int, dict[str, list[float]]]:
    seed, design = args
    points = _point_set(design)
    max_k = max(k for k, _ in points)
    realizations = int(design["grid"]["realizations_per_seed"])
    matrices = {point: np.empty((21, realizations), dtype=float) for point in points}

    for rep in range(realizations):
        cache = {}
        for scenario_index, (name, scenario) in enumerate((
            ("mainland", BASE.mainland),
            ("island", BASE.island),
        )):
            child_seeds = scenario_copy_seeds(
                int(seed), rep, scenario_index, max_k + 2
            )
            independent = [
                _as_arrays(pollinator_trajectory(scenario, child_seed, BASE))
                for child_seed in child_seeds[:max_k]
            ]
            common = _as_arrays(
                pollinator_trajectory(scenario, child_seeds[max_k], BASE)
            )
            selector = random.Random(child_seeds[max_k + 1])
            uniforms = np.asarray([selector.random() for _ in range(max_k)], dtype=float)
            cache[name] = (common, independent, uniforms)

        for k, rho in points:
            q = clone_probability_for_pairwise_rho(rho)
            endpoints = {}
            for name in ("mainland", "island"):
                common, independent, uniforms = cache[name]
                if k == 1 or rho == 0.0:
                    chosen = independent[:k]
                else:
                    chosen = [
                        common if uniforms[copy_index] < q else independent[copy_index]
                        for copy_index in range(k)
                    ]
                endpoints[name] = endpoint_vectorized(_merge_trajectories(chosen))
            matrices[(k, rho)][:, rep] = endpoints["island"] - endpoints["mainland"]

    return int(seed), {
        f"{k}|{rho:.16g}": two_way_fractions(matrix).tolist()
        for (k, rho), matrix in matrices.items()
    }


def _fractions(seed_payload: dict[str, list[float]], k: int, rho: float) -> np.ndarray:
    return np.asarray(seed_payload[f"{k}|{rho:.16g}"], dtype=float)


def _summarize_point(by_seed: dict[int, dict[str, list[float]]], seeds: list[int], k: int, rho: float) -> dict:
    values = np.asarray([_fractions(by_seed[seed], k, rho) for seed in seeds], dtype=float)
    median = np.median(values, axis=0)
    seed_orders = [order_label(row) for row in values]
    return {
        "k": int(k),
        "rho": float(rho),
        "k_eff": float(k_eff(k, rho)),
        "support": float(expected_distinct_trajectory_support(k, rho)),
        "S": float(median[0]),
        "C": float(median[1]),
        "I": float(median[2]),
        "I_over_C": float(np.median(values[:, 2] / values[:, 1])),
        "order": order_label(median),
        "seed_order_counts": dict(Counter(seed_orders)),
    }


def build(workers: int | None = None) -> dict:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    seeds = [int(seed) for seed in design["grid"]["seed_ensemble"]]
    process_count = workers or min(len(seeds), max(mp.cpu_count() - 1, 1))
    with mp.get_context("spawn").Pool(processes=process_count) as pool:
        outputs = pool.map(_seed_grid, [(seed, design) for seed in seeds])
    by_seed = dict(outputs)

    grid_rows = [
        _summarize_point(by_seed, seeds, int(k), float(rho))
        for k in design["grid"]["k_values"]
        for rho in design["grid"]["rho_values"]
    ]

    contours = []
    for contour in design["exact_contour_challenges"]:
        target = float(contour["target_k_eff"])
        for k, rho in contour["points"]:
            row = _summarize_point(by_seed, seeds, int(k), float(rho))
            row["target_k_eff"] = target
            contours.append(row)

    contour_two = [row for row in contours if row["target_k_eff"] == 2.0]
    contour_four = [row for row in contours if row["target_k_eff"] == 4.0]
    orders_two = [row["order"] for row in contour_two]
    orders_four = [row["order"] for row in contour_four]
    support_two = [row["support"] for row in contour_two]
    same_k_eff_can_change_order = len(set(orders_two)) > 1 or len(set(orders_four)) > 1

    if not same_k_eff_can_change_order:
        raise RuntimeError("dense phase-map audit did not demonstrate k_eff insufficiency")

    return {
        "schema_version": "1.0",
        "analysis": "chapter2_el_dense_phase_map",
        "status": "complete",
        "documented_on": "2026-09-13",
        "design": DESIGN.relative_to(ROOT).as_posix(),
        "grid_rows": grid_rows,
        "exact_k_eff_contours": contours,
        "decision": {
            "k_eff_is_sufficient_statistic_for_nonlinear_order": False,
            "same_k_eff_can_change_order": same_k_eff_can_change_order,
            "exact_k_eff_2_order_sequence": orders_two,
            "exact_k_eff_2_support_sequence": support_two,
            "exact_k_eff_4_order_sequence": orders_four,
            "mechanistic_explanation": (
                "variance-equivalent effective independence does not fix distinct trajectory support; "
                "nonlinear response operators are support-sensitive"
            ),
        },
        "claim_boundary": design["claim_boundary"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--workers", type=int)
    args = parser.parse_args()
    payload = build(args.workers)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["decision"], indent=2))


if __name__ == "__main__":
    main()
