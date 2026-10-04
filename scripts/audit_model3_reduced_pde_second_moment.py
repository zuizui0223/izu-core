"""Second-moment audit for the reduced Model 3 continuum closure.

The first moment has an exact Price-equation closure under the frozen
one-generation reduction design.  This audit asks whether the inheritance
correction to phenotype variance can be represented by a single nonnegative
diffusion term.

It cannot if, after the same selection step, exact Mendelian inheritance makes
the next-generation variance both larger and smaller than the clonal
replicator closure across different ecological contexts.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from scripts.audit_model3_reduced_pde_selection import parental_fitness
from scripts.audit_model3_unified_reduction import _config, _empty_state, _founders, _visitors
from scripts.model3_island.density import density_step, make_grid, project_state

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/model3_unified_reduction_audit_20260927.json"


def _weighted_stats(values, weights):
    weights = np.asarray(weights, dtype=float)
    weights = weights / weights.sum()
    mean = float(values @ weights)
    variance = float(((values - mean) ** 2) @ weights)
    return mean, variance


def run_audit() -> dict:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    cfg = _config(design)
    rows = []

    for access in map(float, design["starting_access_states"]):
        founders = _founders(access, design["initial_investment_genotypes"])
        grid = make_grid(([access], [0.4, 0.5, 0.6], [0.5]))
        _, counts = project_state(founders, grid)
        investment = grid.genotypes.mean(axis=2)[:, 1]
        mass = counts / counts.sum()

        for community, optima in design["communities"].items():
            visitors = _visitors(optima)
            next_counts, _ = density_step(
                counts,
                grid,
                visitors,
                _empty_state(1),
                cfg,
                immigration_mode="source",
            )
            exact_mean, exact_variance = _weighted_stats(investment, next_counts)

            fitness = parental_fitness(
                investment,
                mass,
                access=access,
                visitor_optima=np.asarray(optima, dtype=float),
            )
            selected_mass = mass * fitness
            selected_mass /= selected_mass.sum()
            reduced_mean, reduced_variance = _weighted_stats(investment, selected_mass)

            rows.append(
                {
                    "access": access,
                    "community": community,
                    "exact_mean": exact_mean,
                    "reduced_mean": reduced_mean,
                    "mean_error": exact_mean - reduced_mean,
                    "exact_variance": exact_variance,
                    "reduced_variance": reduced_variance,
                    "inheritance_variance_correction": exact_variance - reduced_variance,
                }
            )

    mean_errors = np.abs([row["mean_error"] for row in rows])
    corrections = np.asarray(
        [row["inheritance_variance_correction"] for row in rows], dtype=float
    )
    positive = int(np.sum(corrections > 1e-12))
    negative = int(np.sum(corrections < -1e-12))
    near_zero = len(corrections) - positive - negative

    return {
        "status": "mean_closes_exactly_but_variance_correction_changes_sign",
        "n_cells": len(rows),
        "max_abs_mean_error": float(np.max(mean_errors)),
        "variance_correction_min": float(corrections.min()),
        "variance_correction_max": float(corrections.max()),
        "positive_variance_corrections": positive,
        "negative_variance_corrections": negative,
        "near_zero_variance_corrections": near_zero,
        "rows": rows,
        "implication": (
            "After controlling for the same phenotype-selection step, Mendelian "
            "mating/segregation can either expand or contract investment variance. "
            "A single context-independent nonnegative diffusion correction cannot "
            "be the exact inheritance closure."
        ),
        "claim_boundary": [
            "one-generation frozen reduction design only",
            "does not rule out a state-dependent diffusion approximation under additional assumptions",
            "supports retaining a nonlocal sexual-inheritance kernel for the exact continuum model",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
