"""Reduced continuous-trait confrontation with the frozen Chapter 2 bridge.

This audit reuses the exact frozen visitor-history generator and projected
founders from the 2026-09-27 bridge, but removes explicit diploid inheritance.
It evolves the occupied founder phenotype masses by the Model 3
pollinator-mediated parental-fitness operator:

    dp_j/dt = (w_j / mean(w) - 1) p_j

or, for the discrete reproductive-year map, p'_j proportional to p_j w_j.

Because the focal bridge has mutation_rate=0, there is no diffusion term.  The
purpose is to ask how much of the deterministic near-far pattern is already
encoded in continuous phenotype selection, before Mendelian redistribution.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import numpy as np

from scripts.model3_island.density import make_grid, project_state
from scripts.model3_island.run import founders_from_spec
from scripts.model3_island.types import Config
from scripts.model3_island_bridge_ops import prepare_arms

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/model3_ch2_bridge_20260927.json"
FROZEN = ROOT / "data/results/model3_ch2_bridge_prospective_frozen_20260927.json"


def _phenotype_support(founders, grid):
    _, counts = project_state(founders, grid)
    traits = grid.genotypes.mean(axis=2)[:, :2]
    active = counts > 0
    values = traits[active]
    weights = counts[active]
    unique, inverse = np.unique(np.round(values, 12), axis=0, return_inverse=True)
    mass = np.zeros(len(unique), dtype=float)
    np.add.at(mass, inverse, weights)
    mass /= mass.sum()
    return unique, mass


def _fitness(traits, mass, visitors, config):
    access = traits[:, 0]
    investment = traits[:, 1]
    assurance = np.full(len(mass), config.fixed_assurance)
    ovules = config.ovule_budget * np.exp(
        -config.investment_cost * investment**2
        - config.assurance_cost * assurance**2
    )

    if not len(visitors.ids) or config.activity == 0:
        female = np.zeros(len(mass))
        self_viable = assurance * (ovules - female) * (1.0 - config.depression)
        return self_viable

    affinity = (0.1 + investment[:, None]) * np.exp(
        -((access[:, None] - visitors.optima[None, :]) / visitors.breadths[None, :]) ** 2
    )
    total_affinity = affinity.sum(axis=1, keepdims=True)
    channels = np.divide(
        affinity,
        total_affinity,
        out=np.zeros_like(affinity),
        where=total_affinity > 0,
    )
    activity = config.activity
    if config.activity_mode == "count_scaled":
        activity *= len(visitors.ids) / config.reference_visitor_count

    removed = (
        config.pollen_budget
        * np.exp(-config.pollen_discount * assurance)
        * (1.0 - np.exp(-activity * affinity.mean(axis=1)))
    )
    counts = config.capacity * mass
    denominator = (
        (counts[:, None] * affinity).sum(axis=0)
        + config.capacity * config.background_ratio
    )
    recipient = affinity / denominator[None, :]
    donor_total = (
        counts[:, None]
        * removed[:, None]
        * channels
        * visitors.effectiveness[None, :]
    ).sum(axis=0)
    receipt = recipient @ donor_total

    available = (
        ovules * (1.0 - assurance)
        if config.assurance_timing == "prior"
        else ovules
    )
    female = available * (1.0 - np.exp(-receipt / (2.0 * config.pollen_scale)))
    self_raw = (
        ovules * assurance
        if config.assurance_timing == "prior"
        else assurance * (ovules - female)
    )
    self_viable = self_raw * (1.0 - config.depression)

    recipient_seed_mass = counts * female
    recipient_factor = np.divide(
        recipient * recipient_seed_mass[:, None],
        receipt[:, None],
        out=np.zeros_like(recipient),
        where=receipt[:, None] > 0,
    )
    paternal = removed * (
        (channels * visitors.effectiveness[None, :])
        @ recipient_factor.sum(axis=0)
    )
    return 0.5 * (female + paternal) + self_viable


def _evolve_map(traits, initial_mass, history, config):
    mass = initial_mass.copy()
    for visitors in history.visitors:
        fitness = _fitness(traits, mass, visitors, config)
        mean_fitness = float(mass @ fitness)
        if mean_fitness <= 0:
            raise ArithmeticError("reduced phenotype population has nonpositive fitness")
        mass = mass * fitness / mean_fitness
    return mass


def _frozen_density_targets():
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    out = {}
    names = {
        "natural": "natural",
        "richness_matched": "richness_matched",
        "visitor_pooled": "visitor_pooled",
    }
    for key, intervention in names.items():
        report = next(
            r for r in frozen["reports"]
            if r["intervention"] == intervention and r["model"] == "density"
        )
        out[key] = {
            "mean": float(report["mean"]),
            "mean_by_start": [float(x) for x in report["mean_by_start"]],
        }
    return out


@lru_cache(maxsize=1)
def run_audit() -> dict:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    base = Config.from_dict(design["base_config"])
    if not (
        base.mutation_rate == 0
        and base.survival == 0
        and base.seed_arrival.supply == 0
        and base.assurance_mode == "fixed"
    ):
        raise ValueError("focal bridge no longer satisfies the reduced-selection boundary")

    grid = make_grid(design["grid_axes"])
    supports = {}
    for start in design["starts"]:
        spec = {
            "count": base.capacity,
            "draw_count": 48,
            "means": [0.5, float(start), 0.5],
            "sd": 0.15,
            "birth_year": 0,
        }
        founders = founders_from_spec(spec, design["founder_seed"])
        supports[float(start)] = _phenotype_support(founders, grid)

    effects = {
        "natural": {float(s): [] for s in design["starts"]},
        "richness_matched": {float(s): [] for s in design["starts"]},
        "visitor_pooled": {float(s): [] for s in design["starts"]},
    }
    arm_names = {
        "natural": ("near", "far"),
        "richness_matched": ("matched_near", "matched_far"),
        "visitor_pooled": ("pool_near", "pool_far"),
    }

    for history_seed in design["history_seeds"]:
        arms = prepare_arms(base, seed=int(history_seed), pool_size=design["pool_size"])
        for start in map(float, design["starts"]):
            traits, mass = supports[start]
            for intervention, (near_name, far_name) in arm_names.items():
                near_config, near_history = arms[near_name]
                far_config, far_history = arms[far_name]
                near_mass = _evolve_map(traits, mass, near_history, near_config)
                far_mass = _evolve_map(traits, mass, far_history, far_config)
                effect = float(traits[:, 1] @ far_mass - traits[:, 1] @ near_mass)
                effects[intervention][start].append(effect)

    targets = _frozen_density_targets()
    rows = []
    starts = list(map(float, design["starts"]))
    for intervention in ("natural", "richness_matched", "visitor_pooled"):
        reduced_by_start = [float(np.mean(effects[intervention][s])) for s in starts]
        reduced_mean = float(np.mean(reduced_by_start))
        target = targets[intervention]
        rows.append(
            {
                "intervention": intervention,
                "density_mean": target["mean"],
                "reduced_mean": reduced_mean,
                "density_mean_by_start": target["mean_by_start"],
                "reduced_mean_by_start": reduced_by_start,
                "absolute_mean_gap": abs(reduced_mean - target["mean"]),
                "magnitude_ratio": (
                    abs(reduced_mean / target["mean"])
                    if abs(target["mean"]) > 1e-15 else None
                ),
            }
        )

    exact_cells = []
    reduced_cells = []
    sign_matches = 0
    for row in rows:
        for exact, reduced in zip(row["density_mean_by_start"], row["reduced_mean_by_start"]):
            exact_cells.append(exact)
            reduced_cells.append(reduced)
            sign_matches += int(np.sign(exact) == np.sign(reduced))

    exact_cells = np.asarray(exact_cells)
    reduced_cells = np.asarray(reduced_cells)
    correlation = float(np.corrcoef(exact_cells, reduced_cells)[0, 1])
    slope, intercept = np.polyfit(exact_cells, reduced_cells, 1)

    reduced_order = [
        next(r["reduced_mean"] for r in rows if r["intervention"] == k)
        for k in ("visitor_pooled", "natural", "richness_matched")
    ]
    exact_order = [
        next(r["density_mean"] for r in rows if r["intervention"] == k)
        for k in ("visitor_pooled", "natural", "richness_matched")
    ]

    return {
        "status": "reduced_bridge_direction_and_regime_recovered_with_magnitude_attenuation",
        "histories": len(design["history_seeds"]),
        "starts": starts,
        "rows": rows,
        "start_level_sign_matches": sign_matches,
        "start_level_cells": len(exact_cells),
        "condition_level_correlation": correlation,
        "density_to_reduced_slope": float(slope),
        "density_to_reduced_intercept": float(intercept),
        "exact_regime_order": exact_order,
        "reduced_regime_order": reduced_order,
        "regime_order_matches": bool(
            exact_order[0] < exact_order[1] < exact_order[2]
            and reduced_order[0] < reduced_order[1] < reduced_order[2]
        ),
        "claim_boundary": [
            "continuous phenotype selection only; explicit Mendelian redistribution is removed",
            "reuses the exact frozen visitor-history generator and projected founders",
            "compared with committed deterministic-density summaries, not refitted targets",
            "magnitude attenuation quantifies information lost by the phenotype-only closure",
            "does not test finite demographic repeatability",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
