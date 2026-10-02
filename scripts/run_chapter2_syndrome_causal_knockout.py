"""Prospective causal knockout of syndrome-generating routes in frozen Model 3.

This script changes only declared configuration/intervention values. It does not
modify the Model 3 reproductive, inheritance, density, or finite-population
operators.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.model3_island.assays import investment_assay
from scripts.model3_island.design import source_hashes
from scripts.model3_island.density import make_grid
from scripts.model3_island.simulate import simulate
from scripts.model3_island.types import (
    ArrivalConfig,
    Config,
    EVENT_ORDER,
    History,
    PlantState,
    VisitorState,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "data/design/chapter2_syndrome_causal_knockout_20261002.json"


def _canonical_bytes(document: dict) -> bytes:
    return (json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _empty_state(year: int) -> PlantState:
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
    alleles[:, 0, :] = float(access)
    alleles[:, 1, :] = np.repeat(genotypes, n // len(genotypes), axis=0)
    alleles[:, 2, :] = 0.5
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
    return History(
        visitors=(visitors,) * years,
        seed_candidates=tuple(_empty_state(y + 1) for y in range(years)),
        event_order=EVENT_ORDER,
    )


def _config(design: dict, *, activity: float, assurance: float, investment_cost: float) -> Config:
    b = design["base"]
    zero_seed = ArrivalConfig(0.0, 0.0, 1.0, "exponential", 0.0, 0.0)
    zero_visitor = ArrivalConfig(0.0, 0.0, 1.0, "exponential", 0.0, 0.0)
    return Config(
        schema_version=1,
        event_order=EVENT_ORDER,
        time_unit="reproductive_year",
        capacity=int(b["capacity"]),
        years=int(b["years"]),
        survival=float(b["survival"]),
        ovule_budget=8.0,
        pollen_budget=20.0,
        investment_cost=float(investment_cost),
        pollen_scale=1.0,
        depression=float(b["depression"]),
        mutation_rate=float(b["mutation_rate"]),
        mutation_sd=0.025,
        assurance_mode="fixed",
        fixed_assurance=float(assurance),
        assurance_timing="delayed",
        pollen_discount=0.0,
        assurance_cost=0.0,
        activity=float(activity),
        activity_mode=str(b["activity_mode"]),
        reference_visitor_count=4.0,
        background_ratio=1.0,
        background_resources=1.0,
        seed_arrival=zero_seed,
        visitor_arrival=zero_visitor,
        island_history="founding",
        initial_visitors=0,
        visitor_breadth=0.18,
        visitor_effectiveness=1.0,
        source_allele_means=(0.5, 0.5, 0.5),
        source_allele_sd=0.15,
    )


def _mean_or_none(values):
    x = np.asarray(values, dtype=float)
    x = x[np.isfinite(x)]
    return None if not len(x) else float(x.mean())


def _trajectory(design: dict, cfg: Config, *, access: float, optima) -> dict:
    founders = _founders(access, design["base"]["investment_genotypes"])
    visitors = _visitors(optima)
    history = _history(visitors, cfg.years)
    grid = make_grid(([float(access)], [0.4, 0.5, 0.6], [0.5]))
    initial = float(founders.alleles[:, 1].mean())

    density_change = None
    abm = []
    occupied = []
    for rep in design["base"]["demographic_replicates"]:
        result = simulate(
            cfg,
            history,
            founders,
            replicate=int(rep),
            grid=grid,
            projection_mode="grid",
            immigration_mode="source",
        )
        if density_change is None:
            value = result["density_traits"][-1, 1]
            density_change = float(value - initial) if np.isfinite(value) else None
        value = result["trait_mean"][-1, 1]
        abm.append(float(value - initial) if np.isfinite(value) else np.nan)
        occupied.append(bool(result["population"][-1] > 0))

    assay = investment_assay(founders, visitors, cfg, step=0.05)
    return {
        "fixed_total_gradient": float(np.mean(assay["total_gradient"])),
        "fixed_outcross_gradient": float(np.mean(assay["outcross_gradient"])),
        "density_investment_change": density_change,
        "abm_mean_investment_change": _mean_or_none(abm),
        "abm_terminal_occupancy": float(np.mean(occupied)),
        "abm_replicates": len(abm),
    }


def _sign(x: float, eps: float = 1e-12) -> int:
    if x > eps:
        return 1
    if x < -eps:
        return -1
    return 0


def run(design: dict) -> dict:
    if design["status"] != "prospective_frozen_before_execution":
        raise ValueError("design must be prospectively frozen before execution")
    if design["operator"]["operator_changes_allowed"] or design["operator"]["new_trait_axes_allowed"]:
        raise ValueError("Stage A must use the existing Model 3 operator unchanged")

    route_a_rows = []
    a = design["route_A_assurance_cost"]
    for activity in a["activity"]:
        for assurance in a["fixed_assurance"]:
            for cost in a["investment_cost"]:
                cfg = _config(
                    design,
                    activity=float(activity),
                    assurance=float(assurance),
                    investment_cost=float(cost),
                )
                row = _trajectory(
                    design,
                    cfg,
                    access=float(a["starting_access"]),
                    optima=a["visitor_composition"],
                )
                row.update(
                    activity=float(activity),
                    fixed_assurance=float(assurance),
                    investment_cost=float(cost),
                )
                route_a_rows.append(row)

    def arow(activity, assurance, cost):
        return next(
            r for r in route_a_rows
            if r["activity"] == activity
            and r["fixed_assurance"] == assurance
            and r["investment_cost"] == cost
        )

    target = arow(0.05, 0.5, 0.5)
    no_assurance = arow(0.05, 0.0, 0.5)
    no_cost = arow(0.05, 0.5, 0.0)
    high_activity = arow(0.4, 0.5, 0.5)
    route_a_contrasts = {
        "assurance_effect_low_activity_cost_present": (
            target["fixed_total_gradient"] - no_assurance["fixed_total_gradient"]
        ),
        "cost_effect_low_activity_assurance_present": (
            target["fixed_total_gradient"] - no_cost["fixed_total_gradient"]
        ),
        "activity_effect_assurance_cost_present": (
            high_activity["fixed_total_gradient"] - target["fixed_total_gradient"]
        ),
    }
    route_a_supported = bool(
        target["fixed_total_gradient"] < 0
        and route_a_contrasts["assurance_effect_low_activity_cost_present"] < 0
        and route_a_contrasts["cost_effect_low_activity_assurance_present"] < 0
    )

    route_b_rows = []
    b = design["route_B_rematching"]
    cfg_b = _config(
        design,
        activity=float(b["activity"]),
        assurance=float(b["fixed_assurance"]),
        investment_cost=float(b["investment_cost"]),
    )
    for access in b["starting_access"]:
        for name, optima in b["communities"].items():
            row = _trajectory(design, cfg_b, access=float(access), optima=optima)
            row.update(starting_access=float(access), community=name)
            route_b_rows.append(row)

    def brow(access, community):
        return next(
            r for r in route_b_rows
            if r["starting_access"] == access and r["community"] == community
        )

    threshold = float(b["material_gradient_difference_threshold"])
    route_b_contrasts = []
    for access in [float(x) for x in b["starting_access"]]:
        left = brow(access, "left4")
        right = brow(access, "right4")
        diff = left["fixed_total_gradient"] - right["fixed_total_gradient"]
        sign_change = _sign(left["fixed_total_gradient"]) * _sign(right["fixed_total_gradient"]) < 0
        material = abs(diff) >= threshold
        route_b_contrasts.append({
            "starting_access": access,
            "left_minus_right_fixed_gradient": float(diff),
            "fixed_gradient_sign_change": bool(sign_change),
            "material_gradient_difference": bool(material),
            "left_minus_right_density_change": (
                None if left["density_investment_change"] is None or right["density_investment_change"] is None
                else float(left["density_investment_change"] - right["density_investment_change"])
            ),
            "left_minus_right_abm_mean_change": (
                None if left["abm_mean_investment_change"] is None or right["abm_mean_investment_change"] is None
                else float(left["abm_mean_investment_change"] - right["abm_mean_investment_change"])
            ),
        })
    route_b_supported = bool(
        any(r["fixed_gradient_sign_change"] or r["material_gradient_difference"] for r in route_b_contrasts)
    )

    return {
        "status": "complete_prospective_stage_A_causal_knockout",
        "design_sha256": hashlib.sha256(_canonical_bytes(design)).hexdigest(),
        "operator_source_hashes": source_hashes(),
        "route_A_rows": route_a_rows,
        "route_A_contrasts": route_a_contrasts,
        "route_A_supported": route_a_supported,
        "route_B_rows": route_b_rows,
        "route_B_contrasts": route_b_contrasts,
        "route_B_supported": route_b_supported,
        "stage_B_trait_accessibility_allowed": bool(route_a_supported or route_b_supported),
        "interpretation": {
            "route_A": (
                "A supported result isolates an assurance-by-cost route within the existing "
                "reproductive operator; it does not identify a literal selfing-syndrome trait."
            ),
            "route_B": (
                "A supported result isolates functional rematching at equal visitor count; "
                "it is distinct from simple visitor scarcity."
            ),
        },
        "claim_boundary": design["claim_boundary"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--design", default=str(DEFAULT_DESIGN))
    parser.add_argument("--out")
    args = parser.parse_args()
    design = json.loads(Path(args.design).read_text(encoding="utf-8"))
    result = run(design)
    encoded = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(encoded, encoding="utf-8")
    print(encoded)


if __name__ == "__main__":
    main()
