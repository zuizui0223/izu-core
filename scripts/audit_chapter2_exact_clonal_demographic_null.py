"""Exact 80-update census Markov null for fixed clonal Model 3 plants and visitors.

The restricted model is a closed, fixed-phenotype, zero-mutation,
zero-adult-survival, zero-immigration case of the ORIGINAL reproduction operator,
with pollen-background B held at 48 separately from carrying capacity K.
Only finite recruitment Poisson randomness is integrated analytically.

NO stochastic visitor history, genetic evolution, parameter search, model fitting,
empirical field inference, or new confirmatory population history is generated.
"""
from __future__ import annotations

from dataclasses import replace
import argparse
import json
from pathlib import Path

import numpy as np
from scipy.stats import poisson

from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.model3_island.types import PlantState, VisitorState
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as model_config, load_design,
)

ROOT = Path(__file__).resolve().parents[1]
HORIZONS = (0, 1, 20, 80)
BUDGETS = (4.5, 6.0, 8.0)
CAPACITIES = (8, 48)
VISITOR_OPTIMA = (0.15, 0.35, 0.55, 0.75)
TRAITS = (0.2, 0.35, 0.35)  # matching, investment, assurance
B = 48
INITIAL_N = 8
STATUS = "EXACT_CLONAL_STATIC_VISITOR_DEMOGRAPHIC_NULL_NOT_GENETIC_MEDIATION"


def clone_state(n: int) -> PlantState:
    if not isinstance(n, int) or n < 1 or n > 48:
        raise ValueError("only the original source census domain 1..48 is allowed")
    alleles = np.broadcast_to(np.asarray(TRAITS)[None, :, None], (n, 3, 2)).copy()
    return PlantState(
        alleles=alleles,
        allele_origin=np.arange(n * 6, dtype=np.int64).reshape(n, 3, 2),
        mutation_flags=np.zeros((n, 3, 2), dtype=bool),
        ids=np.arange(n, dtype=np.int64),
        birth_years=np.zeros(n, dtype=np.int64),
    )


def static_visitors() -> VisitorState:
    return VisitorState(
        ids=np.arange(4, dtype=np.int64),
        optima=np.asarray(VISITOR_OPTIMA),
        breadths=np.full(4, 0.18),
        effectiveness=np.ones(4),
    )


def fixed_config(capacity: int, budget: float):
    if capacity not in CAPACITIES or budget not in BUDGETS:
        raise ValueError("outside disclosed exploratory source K/resource grid")
    cfg = model_config(load_design(DEFAULT_DESIGN), "delayed_control", 0.0, "evolving")
    return replace(
        cfg, capacity=capacity, ovule_budget=budget,
        mutation_rate=0.0, mutation_sd=0.0, survival=0.0,
        seed_arrival=replace(cfg.seed_arrival, supply=0.0),
    )


def source_viable_mu(n: int, capacity: int, budget: float) -> float:
    """Exact original Model3 KB-ledger expected viable seeds at census n."""
    if n < 1 or n > capacity:
        raise ValueError("source N exceeds K")
    cfg = fixed_config(capacity, budget)
    result = reproduce_kb(
        clone_state(n), static_visitors(), cfg,
        background_denominator_capacity=B,
    )
    return float(result.outcross.sum() + result.self_viable.sum())


def transition(capacity: int, budget: float):
    """T[n,k]=Pr(N_next=k | current census n), with zero absorbing.

    Identical diploid parental alleles ensure every recruited individual has
    the identical phenotype and genotype when mutation=0. Therefore the
    fixed-visitor population's future reproduction depends only on N.
    This closed Markov chain is an EXACT *restricted clonal* Model 3 process,
    NOT a closure of the segregating-genotype evolutionary model.
    """
    fixed_config(capacity, budget)
    matrix = np.zeros((capacity + 1, capacity + 1), dtype=float)
    matrix[0, 0] = 1.0
    local_mu = {}
    for n in range(1, capacity + 1):
        mu = source_viable_mu(n, capacity, budget)
        local_mu[n] = mu
        matrix[n, :capacity] = poisson.pmf(np.arange(capacity), mu)
        matrix[n, capacity] = poisson.sf(capacity - 1, mu)
    if not np.allclose(matrix.sum(axis=1), 1.0, atol=1e-12, rtol=0):
        raise ArithmeticError("Markov transition rows do not conserve probability")
    if (matrix < 0).any() or not np.isfinite(matrix).all():
        raise ArithmeticError("invalid Markov entries")
    return matrix, local_mu


def run_all():
    summaries = []
    for capacity in CAPACITIES:
        for budget in BUDGETS:
            matrix, local_mu = transition(capacity, budget)
            current = np.zeros(capacity + 1)
            current[INITIAL_N] = 1.0
            moments = {}
            for t in range(max(HORIZONS) + 1):
                if t in HORIZONS:
                    # Absolute population mass, including extinction as N=0.
                    occupied = float(np.sum(current[1:]))
                    moments[str(t)] = {
                        "p_occupied": occupied,
                        "expected_census_unconditional": float(
                            np.dot(np.arange(capacity + 1), current)
                        ),
                        "p_at_N6_to_N9_unconditional": float(
                            np.sum(current[6:min(capacity, 9) + 1])
                        ),
                        "distribution_sum": float(current.sum()),
                    }
                if t < max(HORIZONS):
                    current = current @ matrix
            if not all(np.isclose(z["distribution_sum"], 1.0, atol=1e-10)
                       for z in moments.values()):
                raise ArithmeticError("probability mass not conserved")
            if not (moments["0"]["p_occupied"] >= moments["1"]["p_occupied"]
                    >= moments["20"]["p_occupied"] >= moments["80"]["p_occupied"]):
                raise ArithmeticError("closed extinct population resurrected")
            summaries.append({
                "static_visitors": 4, "K": capacity, "B": B, "budget": budget,
                "start_N": INITIAL_N,
                "source_mu_at_N8": local_mu[8],
                "moments": moments,
            })
    return {
        "schema": "chapter2_exact_clonal_census_null_v1",
        "status": STATUS,
        "model": "Original reproduce_kb with B=48; source 2026-10-10 K8/K48 investment pilot fixture",
        "n_evaluated_conditions": len(summaries),
        "visitor_regime": "fixed source 4 visitor optima",
        "genetic_regime": "all plants identical in matching/investment/assurance, no mutation, no immigration",
        "adult_survival": 0,
        "initial_census": INITIAL_N,
        "horizons": list(HORIZONS),
        "source_budget_grid": list(BUDGETS),
        "new_stochastic_histories": 0,
        "new_genetic_trajectories": 0,
        "is_confirmatory_evolution_test": False,
        "results": summaries,
        "interpretation": (
            "Finite recruitment/carrying capacity alone generates strongly different "
            "80-step occupancy regimes when plant genotypes and four visitor types "
            "are fixed. This is a demographic-only baseline, NOT a genetic "
            "evolution or evolution-to-extinction mediation estimate."
        ),
        "limitations": [
            "The original investment-only pilot in draft #452 has segregating investment genotypes, and its stochastic-visitor arm is excluded.",
            "The finite genotype/visitor/density process cannot generally be closed into a census-only Markov chain.",
            "Source settings and 4-visitor composition are selected from already exposed pilot, not external biological calibration.",
            "No claim of a natural-island demographic survival probability or confidence interval.",
        ],
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, required=True)
    arg = p.parse_args()
    results = run_all()
    arg.out.parent.mkdir(parents=True, exist_ok=True)
    arg.out.write_text(json.dumps(results, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": results["status"],
        "n_conditions": results["n_evaluated_conditions"],
        "p_occupied80": [
            {"K": row["K"], "budget": row["budget"],
             "P80": row["moments"]["80"]["p_occupied"]}
            for row in results["results"]
        ],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
