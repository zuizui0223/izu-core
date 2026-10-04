"""Selection-only trait-density reduction of the Model 3 reproductive operator.

This is deliberately a reduced PDE layer, not the exact sexual-genetic Model 3.
It keeps the same visitor affinity, pollen export/receipt, ovule cost, delayed
assurance, and expected parental-genome contribution, but treats investment as
a continuous breeding-value density p(i,t):

    dp/dt = (w(i; p, V) - mean_w) p + D d2p/di2.

The frozen unified-reduction audit has mutation_rate=0, hence D=0 for the
operator-level sign test below.  The goal is only to test whether the local
selection branching survives the continuous trait-density reduction.
"""
from __future__ import annotations

import json
from math import copysign

import numpy as np


COMMUNITIES = {
    "left4": np.array([0.15, 0.25, 0.35, 0.45]),
    "right4": np.array([0.55, 0.65, 0.75, 0.85]),
    "center4": np.array([0.35, 0.45, 0.55, 0.65]),
}

KNOWN_FIXED_GRADIENTS = {
    (0.2, "left4"): 1.5047805942577446,
    (0.2, "right4"): -0.8720099444012313,
    (0.8, "left4"): -0.8720099444012313,
    (0.8, "right4"): 1.5047805942577395,
}


def initial_density(grid: np.ndarray, *, mean: float = 0.5, sd: float = 0.08) -> np.ndarray:
    p = np.exp(-0.5 * ((grid - mean) / sd) ** 2)
    return p / p.sum()


def parental_fitness(
    investment: np.ndarray,
    masses: np.ndarray,
    *,
    access: float,
    visitor_optima: np.ndarray,
    capacity: float = 48.0,
    adult_mass: float = 48.0,
    activity: float = 0.4,
    assurance: float = 0.5,
    depression: float = 0.5,
    investment_cost: float = 0.5,
    ovule_budget: float = 8.0,
    pollen_budget: float = 20.0,
    pollen_scale: float = 1.0,
    background_ratio: float = 1.0,
    visitor_breadth: float = 0.2,
    visitor_effectiveness: float = 1.0,
) -> np.ndarray:
    """Expected parental-genome contribution for the reduced investment density."""
    investment = np.asarray(investment, dtype=float)
    masses = np.asarray(masses, dtype=float)
    visitor_optima = np.asarray(visitor_optima, dtype=float)
    if investment.ndim != 1 or masses.shape != investment.shape:
        raise ValueError("investment and masses must be aligned vectors")
    if not np.isclose(masses.sum(), 1.0):
        raise ValueError("masses must sum to one")

    affinity = (0.1 + investment[:, None]) * np.exp(
        -((access - visitor_optima[None, :]) / visitor_breadth) ** 2
    )
    channels = affinity / affinity.sum(axis=1, keepdims=True)
    removed = pollen_budget * (1.0 - np.exp(-activity * affinity.mean(axis=1)))

    denominator = (
        adult_mass * (masses[:, None] * affinity).sum(axis=0)
        + capacity * background_ratio
    )
    recipient = affinity / denominator[None, :]
    donor_channel_total = adult_mass * (
        masses[:, None] * removed[:, None] * channels * visitor_effectiveness
    ).sum(axis=0)
    receipt = recipient @ donor_channel_total

    ovules = ovule_budget * np.exp(-investment_cost * investment**2)
    female = ovules * (1.0 - np.exp(-receipt / (2.0 * pollen_scale)))
    self_viable = assurance * (ovules - female) * (1.0 - depression)

    recipient_seed_mass = adult_mass * masses * female
    recipient_factor = np.divide(
        recipient * recipient_seed_mass[:, None],
        receipt[:, None],
        out=np.zeros_like(recipient),
        where=receipt[:, None] > 0,
    )
    paternal = removed * (
        (channels * visitor_effectiveness) @ recipient_factor.sum(axis=0)
    )

    # Same estimand as investment_assay: half maternal + half paternal
    # outcross contribution, plus the full selfed genome contribution.
    return 0.5 * (female + paternal) + self_viable


def mean_investment_velocity(
    access: float,
    community: str,
    *,
    n_nodes: int = 401,
    initial_mean: float = 0.5,
    initial_sd: float = 0.08,
) -> float:
    grid = np.linspace(0.0, 1.0, n_nodes)
    p = initial_density(grid, mean=initial_mean, sd=initial_sd)
    fitness = parental_fitness(
        grid, p, access=access, visitor_optima=COMMUNITIES[community]
    )
    mean = float(grid @ p)
    # Under dp/dt=(w-wbar)p, d mean(i)/dt = Cov(i,w).
    return float(np.sum((grid - mean) * fitness * p))


def sign(value: float) -> int:
    return 0 if value == 0 else int(copysign(1, value))


def run_audit() -> dict:
    rows = []
    for (access, community), fixed_gradient in KNOWN_FIXED_GRADIENTS.items():
        velocity = mean_investment_velocity(access, community)
        rows.append(
            {
                "access": access,
                "community": community,
                "fixed_state_gradient": fixed_gradient,
                "reduced_pde_initial_mean_velocity": velocity,
                "sign_match": sign(fixed_gradient) == sign(velocity),
            }
        )
    all_match = all(row["sign_match"] for row in rows)
    return {
        "status": "reduced_selection_pde_local_sign_gate_passed" if all_match else "failed",
        "equation": "dp/dt=(w(i;p,V)-mean_w)p + D*d2p/di2",
        "frozen_operator_test_mutation_D": 0.0,
        "rows": rows,
        "all_known_fixed_gradient_signs_recovered": all_match,
        "claim_boundary": [
            "This is a one-dimensional continuous investment-density reduction with access held fixed.",
            "It tests local selection direction only, not Mendelian segregation, diploid genotype structure, or 60-year density magnitudes.",
            "No free time-scale or per-context coefficient is fitted to the four sign tests.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
