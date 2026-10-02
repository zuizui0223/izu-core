"""Prospective trait-accessibility pilot using the unchanged Model 3 operator.

Only founder standing variation differs across regimes. Ecological selection,
inheritance, density and finite-population rules are unchanged.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.model3_island.density import make_grid
from scripts.model3_island.history import reflect_unit
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
DEFAULT_DESIGN = ROOT / "data/design/chapter2_trait_accessibility_pilot_20261002.json"


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


def _founders(design: dict, *, sd_access: float, sd_investment: float) -> PlantState:
    b = design["base"]
    n = int(b["capacity"])
    rng = np.random.default_rng(int(b["founder_seed"]))
    z_access = rng.normal(size=(n, 2))
    z_investment = rng.normal(size=(n, 2))

    alleles = np.empty((n, 3, 2), dtype=float)
    alleles[:, 0, :] = reflect_unit(
        float(b["founder_mean_access"]) + float(sd_access) * z_access
    )
    alleles[:, 1, :] = reflect_unit(
        float(b["founder_mean_investment"]) + float(sd_investment) * z_investment
    )
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
        ids=np.arange(20_000, 20_000 + n, dtype=np.int64),
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


def _config(design: dict) -> Config:
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
        investment_cost=float(b["investment_cost"]),
        pollen_scale=1.0,
        depression=float(b["depression"]),
        mutation_rate=float(design["operator"]["mutation_rate"]),
        mutation_sd=0.025,
        assurance_mode="fixed",
        fixed_assurance=float(b["fixed_assurance"]),
        assurance_timing="delayed",
        pollen_discount=0.0,
        assurance_cost=0.0,
        activity=float(b["activity"]),
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


def _mean(values):
    x = np.asarray(values, dtype=float)
    x = x[np.isfinite(x)]
    return None if not len(x) else float(x.mean())


def run(design: dict) -> dict:
    if design["status"] != "prospective_pilot_frozen_before_execution":
        raise ValueError("pilot design must be frozen before execution")
    if design["operator"]["operator_changes_allowed"]:
        raise ValueError("pilot must leave Model 3 operator unchanged")
    if float(design["operator"]["mutation_rate"]) != 0.0:
        raise ValueError("this pilot isolates standing variation only")

    cfg = _config(design)
    nodes = [float(x) for x in design["base"]["grid_nodes"]]
    grid = make_grid((nodes, nodes, [0.5]))
    rows = []

    for regime, spec in design["accessibility_regimes"].items():
        founders = _founders(
            design,
            sd_access=float(spec["standing_sd_access"]),
            sd_investment=float(spec["standing_sd_investment"]),
        )
        for history_name, optima in design["visitor_histories"].items():
            history = _history(_visitors(optima), cfg.years)
            abm_access = []
            abm_investment = []
            occupancy = []
            density_access = None
            density_investment = None
            initial_access_var = None
            initial_investment_var = None

            for rep in design["base"]["demographic_replicates"]:
                result = simulate(
                    cfg,
                    history,
                    founders,
                    replicate=int(rep),
                    grid=grid,
                    projection_mode="continuous",
                    immigration_mode="source",
                )
                if density_access is None:
                    density_access = float(
                        result["density_traits"][-1, 0] - result["density_traits"][0, 0]
                    )
                    density_investment = float(
                        result["density_traits"][-1, 1] - result["density_traits"][0, 1]
                    )
                    initial_access_var = float(result["density_trait_variance"][0, 0])
                    initial_investment_var = float(result["density_trait_variance"][0, 1])

                if np.isfinite(result["trait_mean"][-1, 0]):
                    abm_access.append(
                        float(result["trait_mean"][-1, 0] - result["trait_mean"][0, 0])
                    )
                if np.isfinite(result["trait_mean"][-1, 1]):
                    abm_investment.append(
                        float(result["trait_mean"][-1, 1] - result["trait_mean"][0, 1])
                    )
                occupancy.append(bool(result["population"][-1] > 0))

            rows.append({
                "regime": regime,
                "visitor_history": history_name,
                "standing_sd_access": float(spec["standing_sd_access"]),
                "standing_sd_investment": float(spec["standing_sd_investment"]),
                "initial_density_access_variance": initial_access_var,
                "initial_density_investment_variance": initial_investment_var,
                "density_access_change": density_access,
                "density_investment_change": density_investment,
                "abm_mean_access_change": _mean(abm_access),
                "abm_mean_investment_change": _mean(abm_investment),
                "terminal_occupancy": float(np.mean(occupancy)),
            })

    def row(regime, history):
        return next(
            r for r in rows
            if r["regime"] == regime and r["visitor_history"] == history
        )

    histories = list(design["visitor_histories"])
    access_effects = []
    investment_effects = []
    finite_access_effects = []
    finite_investment_effects = []
    for history in histories:
        equal = row("equal_high", history)
        access_low = row("access_constrained", history)
        investment_low = row("investment_constrained", history)
        access_effects.append(
            abs(equal["density_access_change"]) - abs(access_low["density_access_change"])
        )
        investment_effects.append(
            abs(equal["density_investment_change"]) - abs(investment_low["density_investment_change"])
        )
        if equal["abm_mean_access_change"] is not None and access_low["abm_mean_access_change"] is not None:
            finite_access_effects.append(
                abs(equal["abm_mean_access_change"]) - abs(access_low["abm_mean_access_change"])
            )
        if equal["abm_mean_investment_change"] is not None and investment_low["abm_mean_investment_change"] is not None:
            finite_investment_effects.append(
                abs(equal["abm_mean_investment_change"]) - abs(investment_low["abm_mean_investment_change"])
            )

    contrasts = {
        "access_variation_effect_deterministic": float(np.mean(access_effects)),
        "investment_variation_effect_deterministic": float(np.mean(investment_effects)),
        "access_variation_effect_finite_abm": _mean(finite_access_effects),
        "investment_variation_effect_finite_abm": _mean(finite_investment_effects),
    }
    supported = bool(
        contrasts["access_variation_effect_deterministic"] > 0
        and contrasts["investment_variation_effect_deterministic"] > 0
    )

    return {
        "status": "complete_trait_accessibility_pilot",
        "design_sha256": hashlib.sha256(_canonical_bytes(design)).hexdigest(),
        "rows": rows,
        "contrasts": contrasts,
        "standing_variation_filter_supported": supported,
        "interpretation": (
            "A supported result shows that unequal available standing variation can "
            "filter the speed/magnitude of response under the same unchanged ecological "
            "operator. It does not identify natural colour or morphology genetics."
        ),
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
