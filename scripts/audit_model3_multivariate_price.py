"""Exact multivariate Price identity for the Model 3 density operator.

Under mutation=0, immigration=0 and survival=0, additive expressed traits obey

    mean(z)' = mean(z) + Cov(z, w) / mean(w),

where w is total parental-genome contribution per adult.  For an outcrossed
seed each parent contributes one half; a selfed seed contributes both halves
from the same parent.

This audit validates access, investment and evolving assurance simultaneously.
"""
from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path

import numpy as np

from scripts.model3_island.density import density_step, make_grid, project_state
from scripts.model3_island.run import founders_from_spec
from scripts.model3_island.types import Config, PlantState, VisitorState

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "data/design/model3_ch2_bridge_20260927.json"
JOINT = ROOT / "data/design/model3_joint_syndrome_rare_mutant_20261004.json"

COMMUNITIES = {
    "left4": [0.15, 0.25, 0.35, 0.45],
    "right4": [0.55, 0.65, 0.75, 0.85],
    "center4": [0.35, 0.45, 0.55, 0.65],
    "reference8": [0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85],
}


def _empty():
    return PlantState(
        alleles=np.empty((0, 3, 2), dtype=float),
        allele_origin=np.empty((0, 3, 2), dtype=np.int64),
        mutation_flags=np.empty((0, 3, 2), dtype=bool),
        ids=np.empty(0, dtype=np.int64),
        birth_years=np.empty(0, dtype=np.int64),
    )


def _visitor(optima, config):
    optima = np.asarray(optima, dtype=float)
    n = len(optima)
    return VisitorState(
        ids=np.arange(1000, 1000 + n, dtype=np.int64),
        optima=optima,
        breadths=np.full(n, config.visitor_breadth),
        effectiveness=np.full(n, config.visitor_effectiveness),
    )


def _settings(base, decision):
    return {
        name: replace(
            base,
            assurance_mode="evolving",
            assurance_timing=patch["assurance_timing"],
            pollen_discount=float(patch["pollen_discount"]),
            assurance_cost=float(patch["assurance_cost"]),
        )
        for name, patch in decision["settings"].items()
    }


def _price_prediction(counts, traits, ledger):
    mass = counts / counts.sum()
    paternal = ledger.outcross.sum(axis=1)
    maternal_outcross = ledger.maternal - ledger.self_viable
    genome = 0.5 * maternal_outcross + 0.5 * paternal + ledger.self_viable
    w = np.divide(
        genome,
        counts,
        out=np.zeros_like(genome),
        where=counts > 0,
    )
    mean_w = float(mass @ w)
    current = mass @ traits
    covariance = ((traits - current) * (mass * w)[:, None]).sum(axis=0)
    return current + covariance / mean_w


def run_audit():
    bridge = json.loads(BRIDGE.read_text(encoding="utf-8"))
    decision = json.loads(JOINT.read_text(encoding="utf-8"))
    base = Config.from_dict(bridge["base_config"])
    settings = _settings(base, decision)
    grid = make_grid((
        [0.0, 0.25, 0.5, 0.75, 1.0],
        [0.0, 0.25, 0.5, 0.75, 1.0],
        [0.0, 0.25, 0.5, 0.75, 1.0],
    ))
    traits = grid.genotypes.mean(axis=2)

    founder_means = [
        (0.35, 0.5, 0.35),
        (0.5, 0.5, 0.5),
        (0.65, 0.5, 0.65),
    ]
    rows = []
    for founder_mean in founder_means:
        founders = founders_from_spec(
            {
                "count": base.capacity,
                "draw_count": base.capacity,
                "means": list(founder_mean),
                "sd": 0.15,
                "birth_year": 0,
            },
            bridge["founder_seed"],
        )
        _, counts0 = project_state(founders, grid)

        for setting_name, config in settings.items():
            if config.mutation_rate != 0 or config.survival != 0 or config.seed_arrival.supply != 0:
                raise ValueError("Price identity conditions changed")
            for community, optima in COMMUNITIES.items():
                visitors = _visitor(optima, config)
                next_counts, ledger = density_step(
                    counts0,
                    grid,
                    visitors,
                    _empty(),
                    config,
                    immigration_mode="source",
                )
                exact = next_counts @ traits / next_counts.sum()
                price = _price_prediction(counts0, traits, ledger)
                error = np.abs(exact - price)
                rows.append({
                    "founder_mean": list(founder_mean),
                    "setting": setting_name,
                    "community": community,
                    "exact_next_mean": exact.tolist(),
                    "price_next_mean": price.tolist(),
                    "abs_error": error.tolist(),
                    "max_abs_error": float(error.max()),
                })

    max_error = max(r["max_abs_error"] for r in rows)
    tolerance = float(decision["price_validation"]["max_abs_error"])
    return {
        "status": (
            "exact_multivariate_price_identity_passed"
            if max_error <= tolerance
            else "failed"
        ),
        "cells": len(rows),
        "traits": ["access", "investment", "assurance"],
        "max_abs_error": max_error,
        "tolerance": tolerance,
        "rows": rows,
        "claim_boundary": [
            "identity concerns expected one-generation means, not higher moments",
            "requires mutation=0, immigration=0 and survival=0",
            "does not assume diagonal G or independent trait responses",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
