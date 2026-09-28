"""Prospective Model 3 reduction audit for Chapter 2 unification.

Uses one biological operator at three nested levels:
1) fixed-state reproductive selection assay;
2) deterministic discrete genotype-density trajectory;
3) finite-population ABM trajectory.

The audit is synthetic and does not calibrate natural islands.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.model3_island.assays import investment_assay
from scripts.model3_island.density import make_grid
from scripts.model3_island.simulate import simulate
from scripts.model3_island.types import (
    ArrivalConfig, Config, EVENT_ORDER, History, PlantState, VisitorState,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "data/design/model3_unified_reduction_audit_20260927.json"


def _empty_state(year: int = 1) -> PlantState:
    return PlantState(
        alleles=np.empty((0, 3, 2), dtype=float),
        allele_origin=np.empty((0, 3, 2), dtype=np.int64),
        mutation_flags=np.empty((0, 3, 2), dtype=bool),
        ids=np.empty(0, dtype=np.int64),
        birth_years=np.empty(0, dtype=np.int64),
    )


def _founders(access: float, genotypes) -> PlantState:
    genotypes = np.asarray(genotypes, dtype=float)
    if genotypes.shape != (3, 2):
        raise ValueError("expected three investment genotypes")
    n = 48
    alleles = np.empty((n, 3, 2), dtype=float)
    alleles[:, 0, :] = access
    alleles[:, 2, :] = 0.5
    alleles[:, 1, :] = np.repeat(genotypes, n // len(genotypes), axis=0)
    return PlantState(
        alleles=alleles,
        allele_origin=np.arange(n * 6, dtype=np.int64).reshape(n, 3, 2),
        mutation_flags=np.zeros((n, 3, 2), dtype=bool),
        ids=np.arange(n, dtype=np.int64),
        birth_years=np.zeros(n, dtype=np.int64),
    )


def _visitors(optima) -> VisitorState:
    optima = np.asarray(optima, dtype=float)
    n = len(optima)
    return VisitorState(
        ids=np.arange(10_000, 10_000 + n, dtype=np.int64),
        optima=optima,
        breadths=np.full(n, 0.18),
        effectiveness=np.ones(n),
    )


def _history(visitors: VisitorState, years: int) -> History:
    empty = tuple(_empty_state(y + 1) for y in range(years))
    return History((visitors,) * years, empty, EVENT_ORDER)


def _config(design: dict) -> Config:
    d = design["config"]
    zero_seed = ArrivalConfig(0.0, 0.0, 1.0, "exponential", 0.0, 0.0)
    zero_visitor = ArrivalConfig(0.0, 0.0, 1.0, "exponential", 0.0, 0.0)
    return Config(
        1, EVENT_ORDER, "reproductive_year",
        int(d["capacity"]), int(d["years"]), float(d["survival"]),
        8.0, 20.0, float(d["investment_cost"]), 1.0, float(d["depression"]),
        float(d["mutation_rate"]), 0.025, "fixed", float(d["fixed_assurance"]),
        "delayed", 0.0, 0.0, float(d["activity"]), d["activity_mode"], 4.0,
        1.0, 1.0, zero_seed, zero_visitor, "founding", 0, 0.18, 1.0,
        (0.5, 0.5, 0.5), 0.15,
    )


def _mean_or_none(values):
    values = [float(x) for x in values if np.isfinite(x)]
    return None if not values else float(np.mean(values))


def _signs(values, eps=1e-10):
    out = []
    for x in values:
        if x is None or not np.isfinite(x):
            out.append(None)
        elif x > eps:
            out.append(1)
        elif x < -eps:
            out.append(-1)
        else:
            out.append(0)
    return out


def _mixed(values):
    s = {x for x in _signs(values) if x is not None and x != 0}
    return 1 in s and -1 in s


def _difference(a, b):
    return None if a is None or b is None else float(a - b)


def run_audit(design: dict) -> dict:
    cfg = _config(design)
    starts = [float(x) for x in design["starting_access_states"]]
    contexts = {k: _visitors(v) for k, v in design["communities"].items()}
    histories = {k: _history(v, cfg.years) for k, v in contexts.items()}
    reps = [int(x) for x in design["demographic_replicates"]]
    genotypes = design["initial_investment_genotypes"]

    fixed_rows = []
    trajectory_rows = []
    raw_abm = {}
    raw_density = {}

    for start in starts:
        founders = _founders(start, genotypes)
        grid = make_grid(([start], [0.4, 0.5, 0.6], [0.5]))
        initial_investment = float(founders.alleles[:, 1].mean())

        for name, visitors in contexts.items():
            assay = investment_assay(founders, visitors, cfg, step=0.05)
            fixed_rows.append({
                "start_access": start,
                "context": name,
                "mean_outcross_gradient": float(np.mean(assay["outcross_gradient"])),
                "mean_total_gradient": float(np.mean(assay["total_gradient"])),
            })

            abm_changes = []
            density_change = None
            survivors = 0
            per_rep = {}
            for rep in reps:
                result = simulate(
                    cfg, histories[name], founders, replicate=rep, grid=grid,
                    projection_mode="grid", immigration_mode="source",
                )
                d_final = result["density_traits"][-1, 1]
                if density_change is None and np.isfinite(d_final):
                    density_change = float(d_final - initial_investment)
                a_final = result["trait_mean"][-1, 1]
                value = float(a_final - initial_investment) if np.isfinite(a_final) else np.nan
                per_rep[rep] = value
                if np.isfinite(value):
                    abm_changes.append(value)
                    survivors += 1
            raw_abm[(start, name)] = per_rep
            raw_density[(start, name)] = density_change
            trajectory_rows.append({
                "start_access": start,
                "context": name,
                "density_investment_change": density_change,
                "abm_mean_investment_change": _mean_or_none(abm_changes),
                "abm_survivors": survivors,
                "abm_total": len(reps),
            })

    def row_lookup(rows, start, context):
        return next(r for r in rows if r["start_access"] == start and r["context"] == context)

    contrasts = []
    for start in starts:
        fref = row_lookup(fixed_rows, start, "reference8")
        tref = row_lookup(trajectory_rows, start, "reference8")
        for context in ("left4", "right4", "center4"):
            f = row_lookup(fixed_rows, start, context)
            t = row_lookup(trajectory_rows, start, context)
            paired = []
            for rep in reps:
                a = raw_abm[(start, context)][rep]
                b = raw_abm[(start, "reference8")][rep]
                if np.isfinite(a) and np.isfinite(b):
                    paired.append(a - b)
            contrasts.append({
                "start_access": start,
                "context": context,
                "fixed_total_gradient_minus_reference": float(
                    f["mean_total_gradient"] - fref["mean_total_gradient"]
                ),
                "density_change_minus_reference": _difference(
                    t["density_investment_change"], tref["density_investment_change"]
                ),
                "abm_paired_change_minus_reference": _mean_or_none(paired),
                "abm_eligible_pairs": len(paired),
            })

    def series(rows, field, context):
        return [row_lookup(rows, s, context)[field] for s in starts]

    fixed_mixed = {
        k: _mixed(series(fixed_rows, "mean_total_gradient", k))
        for k in ("left4", "right4", "center4")
    }
    density_mixed = {
        k: _mixed(series(trajectory_rows, "density_investment_change", k))
        for k in ("left4", "right4", "center4")
    }
    abm_mixed = {
        k: _mixed(series(trajectory_rows, "abm_mean_investment_change", k))
        for k in ("left4", "right4", "center4")
    }

    fixed_comp = [
        abs(row_lookup(fixed_rows, s, "left4")["mean_total_gradient"]
            - row_lookup(fixed_rows, s, "right4")["mean_total_gradient"])
        for s in starts
    ]
    density_comp = [
        abs(row_lookup(trajectory_rows, s, "left4")["density_investment_change"]
            - row_lookup(trajectory_rows, s, "right4")["density_investment_change"])
        for s in starts
        if row_lookup(trajectory_rows, s, "left4")["density_investment_change"] is not None
        and row_lookup(trajectory_rows, s, "right4")["density_investment_change"] is not None
    ]

    count_fixed = [
        abs(row_lookup(fixed_rows, s, "left4")["mean_total_gradient"]
            - row_lookup(fixed_rows, s, "leftdup8")["mean_total_gradient"])
        for s in starts
    ]
    count_density = [
        abs(row_lookup(trajectory_rows, s, "left4")["density_investment_change"]
            - row_lookup(trajectory_rows, s, "leftdup8")["density_investment_change"])
        for s in starts
    ]
    count_abm = []
    for s in starts:
        for rep in reps:
            a = raw_abm[(s, "left4")][rep]
            b = raw_abm[(s, "leftdup8")][rep]
            if np.isfinite(a) and np.isfinite(b):
                count_abm.append(abs(a - b))

    det_abm_sign = []
    for row in trajectory_rows:
        if row["context"] == "reference8":
            continue
        d = row["density_investment_change"]
        a = row["abm_mean_investment_change"]
        if d is not None and a is not None and abs(d) > 1e-10 and abs(a) > 1e-10:
            det_abm_sign.append(int(np.sign(d) == np.sign(a)))

    ref_mixed = {
        layer: {
            context: _mixed([
                next(x[field] for x in contrasts if x["start_access"] == s and x["context"] == context)
                for s in starts
            ])
            for context in ("left4", "right4", "center4")
        }
        for layer, field in (
            ("fixed", "fixed_total_gradient_minus_reference"),
            ("density", "density_change_minus_reference"),
            ("abm", "abm_paired_change_minus_reference"),
        )
    }

    max_count_error = max(count_fixed + count_density + count_abm)
    structural = {
        "fixed_state_branching_present": any(fixed_mixed.values()),
        "deterministic_density_branching_present": any(density_mixed.values()),
        "finite_abm_branching_present": any(abm_mixed.values()),
        "fixed_richness_composition_effect_max": float(max(fixed_comp)),
        "deterministic_composition_effect_max": float(max(density_comp)),
        "duplicate_count_control_max_abs_error": float(max_count_error),
        "duplicate_count_control_pass": bool(max_count_error < 1e-12),
        "deterministic_vs_abm_sign_agreement_fraction": (
            float(np.mean(det_abm_sign)) if det_abm_sign else None
        ),
        "reference_contrast_mixed_by_layer": ref_mixed,
    }
    role_not_required = (
        structural["fixed_state_branching_present"]
        and structural["fixed_richness_composition_effect_max"] > 1e-8
        and structural["deterministic_density_branching_present"]
        and structural["duplicate_count_control_pass"]
    )
    decision = (
        "model2_not_required_as_independent_mechanistic_model"
        if role_not_required else
        "model2_retains_unique_role_pending_unresolved_model3_reduction"
    )

    return {
        "status": "complete_prospective_model3_reduction_audit",
        "design": design,
        "fixed_state_rows": fixed_rows,
        "trajectory_rows": trajectory_rows,
        "reference_contrasts": contrasts,
        "diagnostics": {
            "fixed_state_mixed_by_context": fixed_mixed,
            "density_mixed_by_context": density_mixed,
            "abm_mixed_by_context": abm_mixed,
            **structural,
        },
        "decision": decision,
        "interpretation": (
            "Model 3 is evaluated as one nested eco-evolutionary model: fixed-state assay "
            "locates pre-demographic selection branching, deterministic genotype density "
            "tests whether branching survives removal of demographic sampling, and the "
            "finite ABM quantifies realized finite-population departures."
        ),
        "claim_boundary": design["claim_boundary"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--design", default=str(DEFAULT_DESIGN))
    parser.add_argument("--out")
    args = parser.parse_args()
    design = json.loads(Path(args.design).read_text(encoding="utf-8"))
    result = run_audit(design)
    encoded = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists():
            raise FileExistsError(out)
        out.write_text(encoded, encoding="utf-8")
    print(encoded)


if __name__ == "__main__":
    main()
