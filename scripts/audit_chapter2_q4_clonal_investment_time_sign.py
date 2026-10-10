"""Exact finite-state investment counterfactual and Q4 sensitivity decomposition.

This is a no-evolution, genetically clonal and static-pollinator RESTRICTED
Model 3. The original native fixed-B reproductive operator is unchanged.
The specified [0.34, 0.35, 0.36] investment values are an exploratory
post-outcome source-phenotype grid, NOT prospectively registered selection.

No stochastic histories are launched, no genotypes evolve, no empirical
survival is estimated, and no genetic mediator is identified.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path

import numpy as np
from scipy.stats import poisson

from scripts.audit_chapter2_exact_clonal_demographic_null import (
    B, BUDGETS, CAPACITIES, INITIAL_N, TRAITS,
    clone_state, fixed_config, static_visitors,
)
from scripts.chapter2_kb_reproduction import reproduce_kb

ROOT = Path(__file__).resolve().parents[1]
INVESTMENT_LEVELS = (0.34, 0.35, 0.36)
DERIVATIVE_STEP = 1e-5
HORIZONS = (1, 5, 10, 20, 40, 80)
STATUS = "EXPLORATORY_EXACT_CLONAL_INVESTMENT_TIME_SIGN_NOT_EVOLUTION"


def mean_seed_at_census(n: int, capacity: int, budget: float, investment: float) -> float:
    if type(investment) not in (int, float) or not 0 < investment < 1:
        raise ValueError("investment outside the clonal trait interior")
    if type(n) is not int or not 1 <= n <= capacity:
        raise ValueError("invalid census")
    cfg = fixed_config(capacity, budget)
    source = clone_state(n)
    alleles = source.alleles.copy()
    alleles[:, 1, :] = investment
    perturbed = replace(source, alleles=alleles)
    ledger = reproduce_kb(
        perturbed, static_visitors(), cfg, background_denominator_capacity=B,
    )
    return float(ledger.outcross.sum() + ledger.self_viable.sum())


def investment_kernel(capacity: int, budget: float, investment: float):
    fixed_config(capacity, budget)
    mat = np.zeros((capacity + 1, capacity + 1))
    mat[0, 0] = 1.
    mu = np.zeros(capacity + 1)
    for n in range(1, capacity + 1):
        mu[n] = mean_seed_at_census(n, capacity, budget, investment)
        mat[n, :capacity] = poisson.pmf(np.arange(capacity), mu[n])
        mat[n, capacity] = poisson.sf(capacity - 1, mu[n])
    if not np.allclose(mat.sum(axis=1), 1., atol=1e-12, rtol=0):
        raise AssertionError("transition mass is not conserved")
    if (mat < 0).any() or not np.isfinite(mat).all():
        raise AssertionError("invalid transition probabilities")
    return mat, mu


def propagations(matrix: np.ndarray, horizon: int = 80):
    k = matrix.shape[0] - 1
    probabilities = [np.eye(k+1)[INITIAL_N]]
    for _ in range(horizon):
        probabilities.append(probabilities[-1] @ matrix)
    return probabilities


def state_gradient_contributions(matrix, finite_difference_matrix, horizon=80):
    """First-order tangent dP_H/dI, partitioned by resident census n.

    Baseline forward p_t and backward survival probability V_{H-t-1}
    decompose each row's contribution exactly, GIVEN the central-difference
    approximation to dT/dI. This is a sensitivity decomposition, not a
    natural-history mediation estimator or an independent biological trial.
    """
    k = matrix.shape[0]-1
    fwd = propagations(matrix, horizon)
    survival = np.r_[0., np.ones(k)]
    backward = [survival]
    for _ in range(horizon):
        backward.append(matrix @ backward[-1])
    parts = np.zeros(k+1)
    for t in range(horizon):
        parts += fwd[t] * (finite_difference_matrix @ backward[horizon - 1 - t])
    return {
        "total": float(parts.sum()),
        "low_N1_5": float(parts[1:min(k, 5)+1].sum()),
        "high_N6_K": float(parts[6:].sum()),
        "zero_N0": float(parts[0]),
    }


def run_all():
    output = []
    for k in CAPACITIES:
        for budget in BUDGETS:
            kernels = {}
            distributions = {}
            mu = {}
            for investment in INVESTMENT_LEVELS:
                kernel, expected_seeds = investment_kernel(k, budget, investment)
                kernels[investment] = kernel
                mu[investment] = expected_seeds
                distributions[investment] = propagations(kernel)
            baseline = distributions[0.35]
            horizons = {}
            for h in HORIZONS:
                values = {
                    str(v): float(distributions[v][h][1:].sum())
                    for v in INVESTMENT_LEVELS
                }
                horizons[str(h)] = {
                    "P_occupied": values,
                    "group_shift_0p34_to_0p36": values["0.36"] - values["0.34"],
                }

            full_horizon_contrasts = [
                float(distributions[0.36][h][1:].sum() -
                      distributions[0.34][h][1:].sum())
                for h in range(81)
            ]
            first_negative_horizon = next(
                (h for h in range(1, 81) if full_horizon_contrasts[h] < -1e-12),
                None,
            )
            minimum_horizon = int(np.argmin(full_horizon_contrasts[1:])) + 1

            # Original source ledger tangent and exact Markov response, not
            # an evolved investment allele-selection effect.
            step = DERIVATIVE_STEP
            upper, mu_upper = investment_kernel(k, budget, 0.35+step)
            lower, mu_lower = investment_kernel(k, budget, 0.35-step)
            dkernel = (upper-lower)/(2*step)
            tangent = state_gradient_contributions(kernels[0.35], dkernel)
            true_forward_tangent = (
                propagations(upper)[80][1:].sum()
                - propagations(lower)[80][1:].sum()
            )/(2*step)
            if not np.isclose(tangent["total"], true_forward_tangent, atol=5e-9, rtol=0):
                raise AssertionError("state-by-state sensitivity partition failed")
            if not np.isclose(
                tangent["low_N1_5"] + tangent["high_N6_K"],
                tangent["total"], atol=1e-9, rtol=0
            ):
                raise AssertionError("sensitivity census partition incomplete")

            row = {
                "K": k, "B": B, "resource_budget": budget,
                "clonal_investment_levels": list(INVESTMENT_LEVELS),
                "baseline_P80": horizons["80"]["P_occupied"]["0.35"],
                "baseline_mu_N8": float(mu[0.35][8]),
                "baseline_mu_N1": float(mu[0.35][1]),
                "source_seed_response_N8_delta_per_unit": float(
                    (mu[0.36][8]-mu[0.34][8])/0.02
                ),
                "source_seed_response_N1_delta_per_unit": float(
                    (mu[0.36][1]-mu[0.34][1])/0.02
                ),
                "tangent_seed_response_by_N_at_baseline": {
                    str(n): float((mu_upper[n]-mu_lower[n])/(2*step))
                    for n in range(1,k+1)
                },
                "horizons": horizons,
                "first_negative_occupied_probability_contrast_update": first_negative_horizon,
                "most_negative_occupied_probability_contrast_update": minimum_horizon,
                "minimum_occupied_probability_contrast": float(
                    full_horizon_contrasts[minimum_horizon]
                ),
                "H80_tangent_sensitivity": tangent,
                "H80_tangent_forward_check": float(true_forward_tangent),
            }
            output.append(row)

    return {
        "schema": "chapter2_q4_exact_clonal_investment_time_response_v1",
        "status": STATUS,
        "base_operator": "original reproduce_kb fixed pollen background B48",
        "source_fixture": "previously exposed 2026-10-10 #452 static visitor/clone context",
        "observation_unit": "six deterministic source model settings, NOT independent biological replicates",
        "new_visitor_histories": 0,
        "new_evolutionary_trajectories": 0,
        "independent_confirmatory_tests": 0,
        "no_allele_change": True,
        "no_pollinator_turnover": True,
        "finite_investment_delta": 0.02,
        "derivative_step_numerical": DERIVATIVE_STEP,
        "horizons": list(HORIZONS),
        "results": output,
        "limitations": [
            "Uniform community-wide investment shift is not an individual rare-mutant gradient.",
            "All genotypes are fixed and clonal; observed persistence is NOT caused by inherited evolution.",
            "State-gradient decomposition is a first-order derivative attribution, not historical mediation.",
            "The K/resource/trait grid is exposed exploratory Model 3 source context; it is not externally calibrated or an independent new island dataset.",
            "A stronger new Q3→Q4 genetic mechanism requires the same-genome independently registered intervention and natural or externally validated evidence.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = run_all()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps([
        {
            "K": r["K"], "budget": r["resource_budget"],
            "initial_seed_slope": r["source_seed_response_N8_delta_per_unit"],
            "P1_shift": r["horizons"]["1"]["group_shift_0p34_to_0p36"],
            "P80_shift": r["horizons"]["80"]["group_shift_0p34_to_0p36"],
            "H80_low_N_sensitivity": r["H80_tangent_sensitivity"]["low_N1_5"],
            "H80_high_N_sensitivity": r["H80_tangent_sensitivity"]["high_N6_K"],
        }
        for r in result["results"]
    ], sort_keys=True))


if __name__ == "__main__":
    main()
