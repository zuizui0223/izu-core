from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

import numpy as np
from scipy.special import ndtr

from scripts.run_response_geometry_parameter_robustness import BASE, TRAIT_GRID, make_pollinator

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_el_nonlinear_reduction_audit_20260913.json"
INDEPENDENT = ROOT / "data/results/chapter2_trait_adjustment_system_size_rank_crossover_summary_20260910.json"
OUT = ROOT / "data/results/chapter2_el_nonlinear_reduction_audit_20260913.json"


def two_way_fractions(matrix: np.ndarray) -> np.ndarray:
    matrix = np.asarray(matrix, dtype=float)
    grand = matrix.mean()
    row = matrix.mean(axis=1)
    col = matrix.mean(axis=0)
    residual = matrix - (row[:, None] + col[None, :] - grand)
    ss_total = float(np.sum((matrix - grand) ** 2))
    ss = np.array([
        matrix.shape[1] * np.sum((row - grand) ** 2),
        matrix.shape[0] * np.sum((col - grand) ** 2),
        np.sum(residual ** 2),
    ])
    return ss / ss_total


def order_label(fractions) -> str:
    labels = np.array(list("SCI"))
    values = np.asarray(fractions, dtype=float)
    return "".join(labels[np.argsort(values)[::-1]])


def exact_bilinear(*, a: float, b: float, c: float, var_x: float, sigma2: float, k: int, rho: float) -> dict:
    tau = sigma2 * (rho + (1.0 - rho) / k)
    s = a * a * var_x
    cc = b * b * tau
    ii = c * c * var_x * tau
    return {
        "k": k, "rho": rho, "tau": tau,
        "S": s, "C": cc, "I": ii,
        "I_over_C": ii / cc if cc else None,
        "order": order_label((s, cc, ii)),
    }


def adaptive_consumer_resource(*, k: int, seed: int, realizations: int, n_resource: int,
                               width: float, handling: float, alpha: float, steps: int,
                               state_points: int = 17) -> np.ndarray:
    """Structurally distinct nonlinear ecology: adaptive consumer with Holling-II intake."""
    rng = np.random.default_rng(seed)
    initial_states = np.linspace(0.0, 1.0, state_points)
    resources = rng.beta(2.0, 2.0, size=(realizations, k * n_resource))
    matrix = np.empty((state_points, realizations), dtype=float)
    for row_index, initial in enumerate(initial_states):
        state = np.full(realizations, initial, dtype=float)
        for _ in range(steps):
            weights = np.exp(-((state[:, None] - resources) / width) ** 2)
            target = (weights * resources).sum(axis=1) / np.maximum(weights.sum(axis=1), 1e-12)
            state = state + alpha * (target - state)
        weights = np.exp(-((state[:, None] - resources) / width) ** 2)
        attack = weights.mean(axis=1)
        matrix[row_index] = attack / (1.0 + handling * attack)
    return two_way_fractions(matrix)


def run_consumer_resource_grid(design: dict) -> dict:
    cfg = design["nonlinear_generalization"]
    settings = []
    total_trajectories = trajectories_i_mid = trajectories_ci_flip = trajectories_full = 0
    representative = None
    for n_resource in cfg["resource_types_per_copy"]:
        for width in cfg["match_width"]:
            for handling in cfg["handling"]:
                for alpha in cfg["adaptation_rate"]:
                    setting_id = f"m{n_resource}_w{width:.2f}_h{handling:.1f}_a{alpha:.2f}"
                    seed_patterns = []
                    all_seed_rows = {}
                    for seed in cfg["seed_ensemble"]:
                        rows = []
                        for k in cfg["k_values"]:
                            fr = adaptive_consumer_resource(
                                k=int(k), seed=int(seed), realizations=int(cfg["realizations_per_seed"]),
                                n_resource=int(n_resource), width=float(width), handling=float(handling),
                                alpha=float(alpha), steps=int(cfg["adaptation_steps"]),
                            )
                            rows.append({"k": int(k), "S": float(fr[0]), "C": float(fr[1]),
                                         "I": float(fr[2]), "I_over_C": float(fr[2] / fr[1]),
                                         "order": order_label(fr)})
                        all_seed_rows[int(seed)] = rows
                        winners = [row["order"][0] for row in rows]
                        full = winners[0] == "C" and "I" in winners[1:4] and winners[-1] == "S"
                        i_mid = "I" in winners[1:4]
                        ci_flip = rows[0]["C"] > rows[0]["I"] and any(row["I"] > row["C"] for row in rows[1:])
                        seed_patterns.append((full, i_mid, ci_flip))
                        total_trajectories += 1
                        trajectories_full += int(full)
                        trajectories_i_mid += int(i_mid)
                        trajectories_ci_flip += int(ci_flip)
                    settings.append({
                        "setting_id": setting_id, "n_resource": n_resource, "width": width,
                        "handling": handling, "alpha": alpha,
                        "seeds_full_C_to_I_to_S": sum(p[0] for p in seed_patterns),
                        "seeds_intermediate_I_winner": sum(p[1] for p in seed_patterns),
                        "seeds_CI_order_flip": sum(p[2] for p in seed_patterns),
                    })
                    if setting_id == "m2_w0.18_h2.0_a0.15":
                        med_rows = []
                        for idx, k in enumerate(cfg["k_values"]):
                            vals = np.asarray([[all_seed_rows[int(seed)][idx][x] for x in ("S","C","I")]
                                               for seed in cfg["seed_ensemble"]])
                            med_rows.append({
                                "k": int(k),
                                "median_S": float(np.median(vals[:, 0])),
                                "median_C": float(np.median(vals[:, 1])),
                                "median_I": float(np.median(vals[:, 2])),
                                "median_I_over_C": float(np.median(vals[:, 2] / vals[:, 1])),
                                "orders_across_six_seeds": [all_seed_rows[int(seed)][idx]["order"] for seed in cfg["seed_ensemble"]],
                            })
                        representative = {
                            "setting_id": setting_id,
                            "parameters": {"resources_per_copy": 2, "match_width": 0.18, "handling": 2.0,
                                           "adaptation_rate": 0.15, "adaptation_steps": cfg["adaptation_steps"]},
                            "rows": med_rows,
                            "role": "illustration only; inference uses the full grid summary",
                        }
    return {
        "model": "adaptive_consumer_resource",
        "parameter_grid": {**{key: cfg[key] for key in ("resource_types_per_copy","match_width","handling",
                                                           "adaptation_rate","adaptation_steps","k_values",
                                                           "seed_ensemble","realizations_per_seed")},
                           "settings": len(settings)},
        "grid_summary": {
            "seed_setting_trajectories": total_trajectories,
            "trajectories_with_intermediate_I_winner": trajectories_i_mid,
            "trajectories_with_CI_order_flip": trajectories_ci_flip,
            "trajectories_with_full_C_to_I_to_S_pattern": trajectories_full,
            "settings_with_intermediate_I_winner_in_at_least_4_of_6_seeds": sum(r["seeds_intermediate_I_winner"] >= 4 for r in settings),
            "settings_with_CI_order_flip_in_at_least_4_of_6_seeds": sum(r["seeds_CI_order_flip"] >= 4 for r in settings),
            "settings_with_full_C_to_I_to_S_in_at_least_4_of_6_seeds": sum(r["seeds_full_C_to_I_to_S"] >= 4 for r in settings),
            "settings_with_full_C_to_I_to_S_in_all_6_seeds": sum(r["seeds_full_C_to_I_to_S"] == 6 for r in settings),
        },
        "setting_summaries": settings,
        "illustrative_central_setting": representative,
    }


def _pollinator_row(pollinator):
    penalty = BASE.replacement_penalty if pollinator.introduced else 1.0
    return pollinator.trait, pollinator.breadth, penalty


def endpoint_vectorized(trajectory: list[np.ndarray]) -> np.ndarray:
    state = np.asarray(TRAIT_GRID, dtype=float).copy()
    for array in trajectory:
        if len(array) == 0:
            continue
        p_trait, breadth, penalty = array[:, 0], array[:, 1], array[:, 2]
        match = np.exp(-((np.abs(state[:, None] - p_trait[None, :]) / breadth[None, :]) ** 2))
        match *= penalty[None, :]
        service = 1.0 - np.exp(-BASE.saturation * match.mean(axis=1))
        mask = service < 0.45
        if BASE.trait_adjustment > 0 and np.any(mask):
            best = p_trait[np.argmax(match, axis=1)]
            state[mask] = np.clip(state[mask] + BASE.trait_adjustment * (best[mask] - state[mask]), 0.0, 1.0)
    final = trajectory[-1] if trajectory else np.empty((0, 3))
    if len(final) == 0:
        return np.zeros(len(state))
    match = np.exp(-((np.abs(state[:, None] - final[:, 0][None, :]) / final[:, 1][None, :]) ** 2))
    match *= final[:, 2][None, :]
    return np.clip(1.0 - np.exp(-BASE.saturation * match.mean(axis=1)), 0.0, 1.0)


def identity_preserving_correlated_trajectory(scenario, *, seed: int, copies: int, rho_event: float):
    identity_rng = [random.Random(seed + 10_000_019 * (i + 1)) for i in range(copies)]
    communities = [[make_pollinator(identity_rng[i], scenario, BASE) for _ in range(scenario.n_pollinator_types)]
                   for i in range(copies)]
    common_rng = np.random.default_rng(seed + 777_777)
    event_rng = [np.random.default_rng(seed + 20_000_033 * (i + 1)) for i in range(copies)]
    shared_weight, independent_weight = math.sqrt(rho_event), math.sqrt(1.0 - rho_event)
    snapshots = []
    for _ in range(BASE.steps):
        max_size = max((len(group) for group in communities), default=0)
        shared_loss = common_rng.standard_normal(max_size)
        shared_arrival = float(common_rng.standard_normal())
        for copy_index in range(copies):
            group = communities[copy_index]
            if group:
                latent = shared_weight * shared_loss[:len(group)] + independent_weight * event_rng[copy_index].standard_normal(len(group))
                uniforms = ndtr(latent)
                communities[copy_index] = [p for p, u in zip(group, uniforms) if u >= scenario.partner_loss]
            arrival_uniform = float(ndtr(shared_weight * shared_arrival + independent_weight * float(event_rng[copy_index].standard_normal())))
            if arrival_uniform < scenario.partner_arrival:
                communities[copy_index].append(make_pollinator(identity_rng[copy_index], scenario, BASE))
        merged = [_pollinator_row(p) for group in communities for p in group]
        snapshots.append(np.asarray(merged, dtype=float).reshape((-1, 3)) if merged else np.empty((0, 3)))
    return snapshots, communities


def correlated_response_fractions(*, copies: int, rho_event: float, seed: int, realizations: int) -> np.ndarray:
    matrix = np.empty((len(TRAIT_GRID), realizations), dtype=float)
    for rep in range(realizations):
        run_seed = seed + rep * 10_000
        mainland, _ = identity_preserving_correlated_trajectory(BASE.mainland, seed=run_seed + 100_000, copies=copies, rho_event=rho_event)
        island, _ = identity_preserving_correlated_trajectory(BASE.island, seed=run_seed + 200_000, copies=copies, rho_event=rho_event)
        matrix[:, rep] = endpoint_vectorized(island) - endpoint_vectorized(mainland)
    return two_way_fractions(matrix)


def final_count_vector(scenario, *, seed: int, copies: int, rho_event: float) -> np.ndarray:
    _, communities = identity_preserving_correlated_trajectory(scenario, seed=seed, copies=copies, rho_event=rho_event)
    return np.asarray([len(group) for group in communities], dtype=float)


def mean_off_diagonal_correlation(matrix: np.ndarray) -> float:
    correlation = np.corrcoef(matrix, rowvar=False)
    upper = np.triu_indices_from(correlation, 1)
    return float(np.nanmean(correlation[upper]))


def independent_summary() -> dict[int, tuple[float, float, float]]:
    source = json.loads(INDEPENDENT.read_text(encoding="utf-8"))
    return {int(row["k"]): (float(row["median_starting_position_fraction"]),
                              float(row["median_community_realization_fraction"]),
                              float(row["median_nonadditivity_fraction"]))
            for row in source["scale_summary"]}


def run_correlation_robustness(design: dict) -> dict:
    cfg = design["correlation_robustness"]
    independent = independent_summary()
    rows = []
    for rho_event in cfg["latent_event_rho"]:
        mainland_counts = np.asarray([final_count_vector(BASE.mainland, seed=910_000 + rep * 1_000,
                                                         copies=cfg["k"], rho_event=rho_event)
                                      for rep in range(cfg["rho_calibration_replicates"])])
        island_counts = np.asarray([final_count_vector(BASE.island, seed=730_000 + rep * 1_000,
                                                       copies=cfg["k"], rho_event=rho_event)
                                    for rep in range(cfg["rho_calibration_replicates"])])
        rho_mainland = mean_off_diagonal_correlation(mainland_counts)
        rho_island = mean_off_diagonal_correlation(island_counts)
        rho_realized = (rho_mainland + rho_island) / 2.0
        k_eff = cfg["k"] / (1.0 + (cfg["k"] - 1.0) * max(rho_realized, 0.0))
        seed_values, seed_orders = [], []
        for seed in cfg["seed_ensemble"]:
            fr = correlated_response_fractions(copies=cfg["k"], rho_event=rho_event, seed=int(seed),
                                               realizations=cfg["response_realizations_per_seed"])
            seed_values.append(fr); seed_orders.append(order_label(fr))
        array = np.asarray(seed_values); med = np.median(array, axis=0)
        nearest_k = min(independent, key=lambda value: abs(value - k_eff)); nearest = np.asarray(independent[nearest_k])
        rows.append({
            "rho_event_latent": rho_event,
            "realized_final_count_pairwise_rho_mainland": rho_mainland,
            "realized_final_count_pairwise_rho_island": rho_island,
            "realized_final_count_pairwise_rho_mean": rho_realized,
            "count_variance_equivalent_k_eff": k_eff,
            "median_S": float(med[0]), "median_C": float(med[1]), "median_I": float(med[2]),
            "median_I_over_C": float(np.median(array[:, 2] / array[:, 1])),
            "orders_across_six_seeds": {label: seed_orders.count(label) for label in sorted(set(seed_orders))},
            "nearest_independent_k": nearest_k,
            "nearest_independent_median_S": float(nearest[0]),
            "nearest_independent_median_C": float(nearest[1]),
            "nearest_independent_median_I": float(nearest[2]),
            "nearest_independent_order": order_label(nearest),
            "L1_fraction_distance_to_nearest_independent": float(np.abs(med - nearest).sum()),
        })
    return {
        "description": "Each pooled copy retains independent pollinator identities and trait draws. Arrival/loss event uniforms share Gaussian common shocks; no whole-community trajectory is cloned.",
        "k": cfg["k"], "response_realizations_per_seed": cfg["response_realizations_per_seed"],
        "seed_ensemble": cfg["seed_ensemble"], "rho_calibration_replicates": cfg["rho_calibration_replicates"],
        "rows": rows,
        "decision": {
            "k_eff_as_variance_equivalent_count_coordinate_is_sufficient_for_response_decomposition": False,
            "I_over_C_strictly_rho_invariant_in_nonlinear_ABM": False,
            "I_over_C_role": "diagnostic of nonlinear reduction failure, not a preregisterable rho-invariance law",
        },
    }


def build() -> dict:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    independent = independent_summary()
    chapter2_rows = [{"k": k, "S": v[0], "C": v[1], "I": v[2], "I_over_C": v[2]/v[1], "order": order_label(v)}
                     for k, v in sorted(independent.items())]
    return {
        "schema_version": "1.0", "analysis": "chapter2_el_nonlinear_reduction_failure",
        "status": "exploratory_generalization_complete", "updated_on": "2026-09-13",
        "design": DESIGN.relative_to(ROOT).as_posix(), "claim_boundary": design["claim_boundaries"],
        "exact_bilinear": {
            "tau_k": "sigma2 * (rho + (1-rho)/k)", "S_k": "a^2 Var(X)", "C_k": "b^2 tau_k",
            "I_k": "c^2 Var(X) tau_k", "I_over_C": "c^2 Var(X) / b^2",
            "exact_invariances": {"I_over_C_independent_of_k": True, "I_over_C_independent_of_rho": True,
                                  "C_vs_I_relative_order_can_flip": False,
                                  "maximum_S_crossing_events_as_tau_decreases": 2,
                                  "maximum_order_regions_along_monotone_tau": 3},
            "smooth_first_order_extension": "C_k=A_C tau_k+O(tau_k^2), I_k=A_I tau_k+O(tau_k^2); I/C approaches A_I/A_C as tau_k->0 but is not generally exactly finite-k invariant.",
        },
        "chapter2_abm_existing": {"source": INDEPENDENT.relative_to(ROOT).as_posix(), "rows": chapter2_rows,
                                  "C_over_I_order_reverses": True, "intermediate_I_winner_present": True,
                                  "order_path": [row["order"] for row in chapter2_rows]},
        "adaptive_consumer_resource": run_consumer_resource_grid(design),
        "identity_preserving_event_correlation": run_correlation_robustness(design),
        "revised_lane_B_claim": "Effective independence is a variance-equivalent coordinate in the linearized theory, not a sufficient statistic for nonlinear ecological response. Aggregation and synchrony can alter different components of response variance; this can create an interaction-dominated intermediate phase absent from both small-system and asymptotic limits.",
        "lane_C_implication": "Do not collapse breadth/aggregation and synchrony/stability into one effective-independence covariate. If Lane C is ever reactivated, preserve them as separate pre-outcome context axes. Do not require rho-invariance of I/C from the current nonlinear evidence.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--out", type=Path, default=OUT); args = parser.parse_args()
    payload = build(); args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"consumer_resource_grid": payload["adaptive_consumer_resource"]["grid_summary"],
                      "correlation_rows": payload["identity_preserving_event_correlation"]["rows"]}, indent=2))


if __name__ == "__main__":
    main()
