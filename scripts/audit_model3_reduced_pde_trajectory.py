"""Multi-generation fidelity audit for the reduced Model 3 selection equation.

Compares three descriptions under the frozen 60-year unified-reduction audit:

1. exact deterministic diploid genotype-density dynamics;
2. a discrete phenotype replicator map p' proportional to p*w;
3. the continuous-time replicator PDE weak solution on the initial atomic
   investment support, dp/dt=(w/mean(w)-1)p.

The frozen audit has mutation=0, survival=0, immigration=0, fixed access and
fixed assurance.  Therefore D=0 in the reduced PDE and its weak solution can be
integrated through the masses on the initial investment support.

This is an exploratory reduction-fidelity diagnostic, not a replacement for
the exact sexual inheritance operator.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

from scripts.audit_model3_reduced_pde_selection import parental_fitness
from scripts.audit_model3_unified_reduction import _config, _empty_state, _founders, _visitors
from scripts.model3_island.density import density_step, make_grid, project_state

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/model3_unified_reduction_audit_20260927.json"

SOURCE_LOCKED_DENSITY_EXTREMES = {
    (0.2, "left4"): 0.0896619162599484,
    (0.2, "right4"): -0.09946198189063737,
    (0.8, "left4"): -0.09946198189063737,
    (0.8, "right4"): 0.08966191625994852,
}


def _initial_phenotype_support(grid, counts):
    investment = grid.genotypes.mean(axis=2)[:, 1]
    values = []
    masses = []
    for value in np.unique(investment[counts > 0]):
        mask = np.isclose(investment, value)
        values.append(float(value))
        masses.append(float(counts[mask].sum()))
    masses = np.asarray(masses, dtype=float)
    masses /= masses.sum()
    return np.asarray(values, dtype=float), masses


def _exact_density_change(counts, grid, visitors, cfg) -> float:
    current = counts.copy()
    investment = grid.genotypes.mean(axis=2)[:, 1]
    initial_mean = float(investment @ current / current.sum())
    for year in range(cfg.years):
        current, _ = density_step(
            current,
            grid,
            visitors,
            _empty_state(year + 1),
            cfg,
            immigration_mode="source",
        )
    final_mean = float(investment @ current / current.sum())
    return final_mean - initial_mean


def _replicator_map_change(values, masses, *, access, optima, years) -> float:
    p = masses.copy()
    initial_mean = float(values @ p)
    for _ in range(years):
        w = parental_fitness(values, p, access=access, visitor_optima=optima)
        mean_w = float(w @ p)
        if mean_w <= 0:
            raise ArithmeticError("nonpositive reduced mean fitness")
        p = p * w / mean_w
    return float(values @ p - initial_mean)


def _replicator_pde_change(values, masses, *, access, optima, years) -> float:
    initial_mean = float(values @ masses)

    def rhs(_time, raw):
        p = np.maximum(raw, 0.0)
        p /= p.sum()
        w = parental_fitness(values, p, access=access, visitor_optima=optima)
        mean_w = float(w @ p)
        return p * (w / mean_w - 1.0)

    result = solve_ivp(
        rhs,
        (0.0, float(years)),
        masses,
        method="RK45",
        rtol=1e-10,
        atol=1e-12,
    )
    if not result.success:
        raise ArithmeticError(result.message)
    p = np.maximum(result.y[:, -1], 0.0)
    p /= p.sum()
    return float(values @ p - initial_mean)


def run_audit() -> dict:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    cfg = _config(design)
    if not (
        cfg.years == 60
        and cfg.survival == 0
        and cfg.mutation_rate == 0
        and cfg.seed_arrival.supply == 0
        and cfg.assurance_mode == "fixed"
    ):
        raise ValueError("frozen reduction design no longer satisfies reduction conditions")

    rows = []
    for access in map(float, design["starting_access_states"]):
        founders = _founders(access, design["initial_investment_genotypes"])
        grid = make_grid(([access], [0.4, 0.5, 0.6], [0.5]))
        _, counts = project_state(founders, grid)
        values, masses = _initial_phenotype_support(grid, counts)

        for community, raw_optima in design["communities"].items():
            optima = np.asarray(raw_optima, dtype=float)
            visitors = _visitors(optima)
            exact = _exact_density_change(counts, grid, visitors, cfg)
            mapped = _replicator_map_change(
                values, masses, access=access, optima=optima, years=cfg.years
            )
            pde = _replicator_pde_change(
                values, masses, access=access, optima=optima, years=cfg.years
            )
            rows.append(
                {
                    "access": access,
                    "community": community,
                    "exact_density_change": exact,
                    "replicator_map_change": mapped,
                    "replicator_pde_change": pde,
                    "map_abs_error": abs(mapped - exact),
                    "pde_abs_error": abs(pde - exact),
                    "map_sign_match": bool(
                        np.sign(mapped) == np.sign(exact)
                        or (abs(mapped) < 1e-12 and abs(exact) < 1e-12)
                    ),
                    "pde_sign_match": bool(
                        np.sign(pde) == np.sign(exact)
                        or (abs(pde) < 1e-12 and abs(exact) < 1e-12)
                    ),
                }
            )

    for key, expected in SOURCE_LOCKED_DENSITY_EXTREMES.items():
        access, community = key
        observed = next(
            row["exact_density_change"]
            for row in rows
            if row["access"] == access and row["community"] == community
        )
        if abs(observed - expected) > 1e-12:
            raise AssertionError((key, observed, expected))

    map_errors = np.asarray([row["map_abs_error"] for row in rows])
    pde_errors = np.asarray([row["pde_abs_error"] for row in rows])
    map_signs = sum(row["map_sign_match"] for row in rows)
    pde_signs = sum(row["pde_sign_match"] for row in rows)

    # These are exploratory fidelity criteria.  The 0.01 mean-error target uses
    # the repository's existing trait numerical tolerance; 0.025 is the
    # existing bridge mean-contrast precision target.  They are not a
    # preregistered biological success criterion.
    criteria = {
        "all_25_signs": map_signs == 25 and pde_signs == 25,
        "map_mean_abs_error_below_0p01": float(map_errors.mean()) < 0.01,
        "pde_mean_abs_error_below_0p01": float(pde_errors.mean()) < 0.01,
        "map_max_abs_error_below_0p025": float(map_errors.max()) < 0.025,
        "pde_max_abs_error_below_0p025": float(pde_errors.max()) < 0.025,
    }
    return {
        "status": (
            "reduced_multi_generation_mean_fidelity_passed"
            if all(criteria.values())
            else "reduced_multi_generation_mean_fidelity_failed"
        ),
        "n_cells": len(rows),
        "years": cfg.years,
        "replicator_map": {
            "sign_matches": map_signs,
            "mean_abs_error": float(map_errors.mean()),
            "max_abs_error": float(map_errors.max()),
        },
        "replicator_pde": {
            "sign_matches": pde_signs,
            "mean_abs_error": float(pde_errors.mean()),
            "max_abs_error": float(pde_errors.max()),
        },
        "criteria": criteria,
        "rows": rows,
        "claim_boundary": [
            "post-hoc exploratory reduction-fidelity diagnostic",
            "mean investment only; the reduced models do not reproduce diploid genotype frequencies or heterozygosity",
            "fixed visitor communities, fixed access, fixed assurance, mutation=0, survival=0, immigration=0",
            "success here does not establish the full island bridge or historical-repeatability result as a PDE",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
