"""Audit the one-generation mean-trait closure behind the reduced PDE.

For the frozen Model 3 unified-reduction design, survival=0, immigration=0,
mutation=0, and access/assurance are fixed within each run.  Under those
conditions the expected offspring mean investment has an exact Price-equation
form:

    zbar' = zbar + Cov(z, w) / mean(w),

where w is expected parental-genome contribution per adult computed from the
same pollen-transfer/reproductive operator.

This audit compares that reduced mean update with one exact deterministic
genotype-density step for every starting-access x visitor-community cell.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from scripts.audit_model3_reduced_pde_selection import price_mean_step
from scripts.audit_model3_unified_reduction import _config, _empty_state, _founders, _visitors
from scripts.model3_island.density import density_step, make_grid, project_state

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/model3_unified_reduction_audit_20260927.json"


def run_audit() -> dict:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    cfg = _config(design)
    if not (
        cfg.survival == 0
        and cfg.mutation_rate == 0
        and cfg.seed_arrival.supply == 0
        and cfg.assurance_mode == "fixed"
    ):
        raise ValueError("frozen reduction design no longer satisfies the exact mean-closure conditions")

    rows = []
    for access in map(float, design["starting_access_states"]):
        founders = _founders(access, design["initial_investment_genotypes"])
        grid = make_grid(([access], [0.4, 0.5, 0.6], [0.5]))
        state, counts = project_state(founders, grid)
        traits = grid.genotypes.mean(axis=2)
        investment = traits[:, 1]
        masses = counts / counts.sum()
        initial_mean = float(investment @ masses)

        for name, optima in design["communities"].items():
            visitors = _visitors(optima)
            next_counts, _ = density_step(
                counts,
                grid,
                visitors,
                _empty_state(1),
                cfg,
                immigration_mode="source",
            )
            density_next_mean = float(investment @ next_counts / next_counts.sum())
            price_next_mean = price_mean_step(
                investment,
                masses,
                access=access,
                visitor_optima=np.asarray(optima, dtype=float),
            )
            error = abs(density_next_mean - price_next_mean)
            rows.append(
                {
                    "access": access,
                    "community": name,
                    "initial_mean": initial_mean,
                    "density_next_mean": density_next_mean,
                    "price_next_mean": price_next_mean,
                    "density_change": density_next_mean - initial_mean,
                    "price_change": price_next_mean - initial_mean,
                    "abs_error": error,
                }
            )

    max_error = max(row["abs_error"] for row in rows)
    sign_match = all(
        np.sign(row["density_change"]) == np.sign(row["price_change"])
        or (abs(row["density_change"]) < 1e-14 and abs(row["price_change"]) < 1e-14)
        for row in rows
    )
    return {
        "status": "exact_one_generation_mean_closure_passed" if max_error < 1e-12 and sign_match else "failed",
        "n_cells": len(rows),
        "max_abs_mean_error": max_error,
        "all_change_signs_match": sign_match,
        "rows": rows,
        "mathematical_identity": "zbar_next = zbar + Cov(z,w)/mean(w)",
        "scope": [
            "exact for expected mean investment under the frozen reduction design",
            "requires additive expressed investment, mutation=0, survival=0, immigration=0, fixed access and fixed assurance",
            "does not close the full offspring distribution or multi-generation genotype dynamics",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
