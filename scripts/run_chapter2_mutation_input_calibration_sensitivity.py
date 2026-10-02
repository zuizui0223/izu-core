"""Empirically anchored mutation-input sensitivity for the Chapter 2 vNext genetic filter."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from scripts.model3_island.history import reflect_unit
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.types import ArrivalConfig, Config, EVENT_ORDER, History, PlantState, VisitorState
from scripts.prospective_trait_accessibility import advance_trait_accessibility

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "data/design/chapter2_mutation_input_calibration_sensitivity_20261002.json"


def _empty_state(year: int) -> PlantState:
    return PlantState(
        alleles=np.empty((0, 3, 2), dtype=float),
        allele_origin=np.empty((0, 3, 2), dtype=np.int64),
        mutation_flags=np.empty((0, 3, 2), dtype=bool),
        ids=np.empty(0, dtype=np.int64),
        birth_years=np.empty(0, dtype=np.int64),
    )


def _visitors(optima) -> VisitorState:
    x = np.asarray(optima, dtype=float)
    return VisitorState(
        ids=np.arange(40_000, 40_000 + len(x), dtype=np.int64),
        optima=x,
        breadths=np.full(len(x), 0.18),
        effectiveness=np.ones(len(x)),
    )


def _history(visitors: VisitorState, years: int) -> History:
    return History(
        visitors=(visitors,) * years,
        seed_candidates=tuple(_empty_state(y + 1) for y in range(years)),
        event_order=EVENT_ORDER,
    )


def _config(design: dict, capacity: int) -> Config:
    b = design["baseline"]
    zero_seed = ArrivalConfig(0.0, 0.0, 1.0, "exponential", 0.0, 0.0)
    zero_visitor = ArrivalConfig(0.0, 0.0, 1.0, "exponential", 0.0, 0.0)
    return Config(
        schema_version=1,
        event_order=EVENT_ORDER,
        time_unit="reproductive_year",
        capacity=int(capacity),
        years=int(b["years"]),
        survival=float(b["survival"]),
        ovule_budget=8.0,
        pollen_budget=20.0,
        investment_cost=float(b["investment_cost"]),
        pollen_scale=1.0,
        depression=float(b["depression"]),
        mutation_rate=0.0,
        mutation_sd=0.0,
        assurance_mode="fixed",
        fixed_assurance=float(b["fixed_assurance"]),
        assurance_timing="delayed",
        pollen_discount=0.0,
        assurance_cost=0.0,
        activity=float(b["activity"]),
        activity_mode="fixed",
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


def _founders(design: dict, *, capacity: int, founder_seed: int, investment_sd: float) -> PlantState:
    b = design["baseline"]
    access_rng = np.random.default_rng(np.random.SeedSequence([int(founder_seed), 9101]))
    investment_rng = np.random.default_rng(np.random.SeedSequence([int(founder_seed), 9102]))
    alleles = np.empty((capacity, 3, 2), dtype=float)
    alleles[:, 0, :] = reflect_unit(
        float(b["founder_mean_access"])
        + access_rng.normal(0, float(b["standing_sd_access"]), size=(capacity, 2))
    )
    alleles[:, 1, :] = reflect_unit(
        float(b["founder_mean_investment"])
        + investment_rng.normal(0, float(investment_sd), size=(capacity, 2))
    )
    alleles[:, 2, :] = 0.5
    return PlantState(
        alleles=alleles,
        allele_origin=np.arange(capacity * 6, dtype=np.int64).reshape(capacity, 3, 2),
        mutation_flags=np.zeros((capacity, 3, 2), dtype=bool),
        ids=np.arange(capacity, dtype=np.int64),
        birth_years=np.zeros(capacity, dtype=np.int64),
    )


def _va_proxy(state: PlantState) -> float | None:
    if not len(state.ids):
        return None
    return float(np.var(state.alleles[:, 1, :].ravel()) / 2.0)


def _trait_mean(state: PlantState) -> float | None:
    if not len(state.ids):
        return None
    return float(state.alleles[:, 1, :].mean())


def _simulate(design: dict, *, capacity: int, founders: PlantState, visitors: VisitorState,
              founder_seed: int, demographic_seed: int, ratio: float):
    cfg = _config(design, capacity)
    history = _history(visitors, cfg.years)
    state = founders
    streams = {
        name: stream(
            int(np.random.SeedSequence([int(founder_seed), int(demographic_seed), 9201]).generate_state(1)[0]),
            name,
            0,
        )
        for name in STREAM_IDS
    }

    va0 = _va_proxy(state)
    if va0 is None or va0 <= 0:
        raise ValueError("initial additive-variance proxy must be positive")
    mu = float(design["mutation_input"]["per_copy_mutation_rate"]) if ratio > 0 else 0.0
    sigma = float(np.sqrt(2.0 * float(ratio) * va0 / mu)) if mu > 0 else 0.0
    mutation_spec = {
        "mutation_rate_access": float(design["mutation_input"]["access_mutation_rate"]),
        "mutation_rate_investment": mu,
        "mutation_sd_access": 0.0,
        "mutation_sd_investment": sigma,
    }

    report_years = set(int(x) for x in design["baseline"]["report_years"])
    reports = []
    initial_mean = _trait_mean(state)

    def record(year):
        if year in report_years:
            reports.append({
                "year": int(year),
                "population": int(len(state.ids)),
                "investment_mean": _trait_mean(state),
                "investment_va_proxy": _va_proxy(state),
            })

    record(0)
    for year in range(cfg.years):
        ledger = reproduce(state, history.visitors[year], cfg)
        state, _ = advance_trait_accessibility(
            state,
            ledger,
            history.seed_candidates[year],
            cfg,
            streams,
            mutation_spec=mutation_spec,
            coupling=0.0,
            year=year,
        )
        record(year + 1)

    by_year = {r["year"]: r for r in reports}
    def response(year):
        x = by_year[year]["investment_mean"]
        return None if x is None or initial_mean is None else float(x - initial_mean)

    return {
        "initial_va_proxy": va0,
        "target_VM_over_VG0": float(ratio),
        "mutation_rate": mu,
        "mutation_sd": sigma,
        "approx_VM": float(mu * sigma * sigma / 2.0),
        "realized_input_ratio_approx": float((mu * sigma * sigma / 2.0) / va0) if va0 else None,
        "legacy_sigma_0_04_input_ratio": float((0.001 * 0.04 * 0.04 / 2.0) / va0),
        "response_y400": response(400),
        "response_y800": response(800),
        "terminal_occupancy": int(len(state.ids) > 0),
        "reports": reports,
    }


def _mean(values):
    x = np.asarray([v for v in values if v is not None and np.isfinite(v)], dtype=float)
    return None if not len(x) else float(x.mean())


def run(design: dict) -> dict:
    if design["status"] != "prospective_frozen_before_execution":
        raise ValueError("design must be frozen before execution")

    rows = []
    for capacity in design["capacities"]:
        for standing_name, investment_sd in design["standing_regimes"].items():
            ratios = (
                design["mutation_input"]["low_standing_VM_over_VG0"]
                if standing_name == "low"
                else design["mutation_input"]["high_reference_VM_over_VG0"]
            )
            for founder_seed in design["baseline"]["founder_seeds"]:
                founders = _founders(
                    design,
                    capacity=int(capacity),
                    founder_seed=int(founder_seed),
                    investment_sd=float(investment_sd),
                )
                for demographic_seed in design["baseline"]["demographic_seeds"]:
                    for history_name, optima in design["baseline"]["visitor_histories"].items():
                        visitors = _visitors(optima)
                        for ratio in ratios:
                            x = _simulate(
                                design,
                                capacity=int(capacity),
                                founders=founders,
                                visitors=visitors,
                                founder_seed=int(founder_seed),
                                demographic_seed=int(demographic_seed),
                                ratio=float(ratio),
                            )
                            rows.append({
                                "capacity": int(capacity),
                                "standing_regime": standing_name,
                                "standing_sd_investment": float(investment_sd),
                                "visitor_history": history_name,
                                "founder_seed": int(founder_seed),
                                "demographic_seed": int(demographic_seed),
                                **x,
                            })

    def select(*, standing, ratio):
        return [
            r for r in rows
            if r["standing_regime"] == standing
            and np.isclose(r["target_VM_over_VG0"], ratio)
        ]

    central = float(design["predeclared_decisions"]["central_anchor"])
    high = select(standing="high_reference", ratio=0.0)
    low_central = select(standing="low", ratio=central)

    summaries = {}
    for standing_name in design["standing_regimes"]:
        ratios = (
            design["mutation_input"]["low_standing_VM_over_VG0"]
            if standing_name == "low"
            else design["mutation_input"]["high_reference_VM_over_VG0"]
        )
        for capacity in design["capacities"]:
            for history in design["baseline"]["visitor_histories"]:
                for ratio in ratios:
                    cell = [
                        r for r in rows
                        if r["standing_regime"] == standing_name
                        and r["capacity"] == int(capacity)
                        and r["visitor_history"] == history
                        and np.isclose(r["target_VM_over_VG0"], float(ratio))
                    ]
                    key = f"{standing_name}|N{capacity}|{history}|r{ratio}"
                    va_by_year = {}
                    for year in design["baseline"]["report_years"]:
                        va_by_year[str(year)] = _mean([
                            next(q["investment_va_proxy"] for q in r["reports"] if q["year"] == int(year))
                            for r in cell
                        ])
                    v600 = va_by_year["600"]
                    v800 = va_by_year["800"]
                    denom = None if v600 is None or v800 is None else (v600 + v800) / 2.0
                    plateau_relative_change = (
                        None if denom is None or denom <= 0 else abs(v800 - v600) / denom
                    )
                    summaries[key] = {
                        "n": len(cell),
                        "mean_initial_va_proxy": _mean([r["initial_va_proxy"] for r in cell]),
                        "mean_mutation_sd": _mean([r["mutation_sd"] for r in cell]),
                        "mean_legacy_sigma_0_04_input_ratio": _mean([
                            r["legacy_sigma_0_04_input_ratio"] for r in cell
                        ]),
                        "mean_abs_response_y400": _mean([
                            abs(r["response_y400"]) for r in cell if r["response_y400"] is not None
                        ]),
                        "mean_abs_response_y800": _mean([
                            abs(r["response_y800"]) for r in cell if r["response_y800"] is not None
                        ]),
                        "mean_terminal_occupancy": _mean([r["terminal_occupancy"] for r in cell]),
                        "va_proxy_by_year": va_by_year,
                        "plateau_relative_change_600_800": plateau_relative_change,
                        "near_plateau": None if plateau_relative_change is None else plateau_relative_change < 0.1,
                    }

    high400 = _mean([abs(r["response_y400"]) for r in high if r["response_y400"] is not None])
    low400 = _mean([abs(r["response_y400"]) for r in low_central if r["response_y400"] is not None])
    high800 = _mean([abs(r["response_y800"]) for r in high if r["response_y800"] is not None])
    low800 = _mean([abs(r["response_y800"]) for r in low_central if r["response_y800"] is not None])

    decisions = {
        "standing_dominates_at_400": bool(high400 is not None and low400 is not None and high400 > low400),
        "standing_dominates_at_800": bool(high800 is not None and low800 is not None and high800 > low800),
        "ranking_reversal_at_400": bool(high400 is not None and low400 is not None and low400 > high400),
        "ranking_reversal_at_800": bool(high800 is not None and low800 is not None and low800 > high800),
    }
    headline = (
        "retain_standing_variation_dominates_with_finite_horizon_qualification"
        if decisions["standing_dominates_at_400"]
        else "drop_standing_variation_dominance_claim"
    )

    return {
        "status": "complete_mutation_input_calibration_sensitivity",
        "n_trajectories": len(rows),
        "central_anchor_comparison": {
            "high_standing_no_mutation_abs_response_y400": high400,
            "low_standing_r0_01_abs_response_y400": low400,
            "high_standing_no_mutation_abs_response_y800": high800,
            "low_standing_r0_01_abs_response_y800": low800,
        },
        "decisions": decisions,
        "headline_decision": headline,
        "cell_summaries": summaries,
        "rows": rows,
        "claim_boundary": design["claim_boundary"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--design", default=str(DEFAULT_DESIGN))
    parser.add_argument("--out")
    args = parser.parse_args()
    design = json.loads(Path(args.design).read_text(encoding="utf-8"))
    result = run(design)
    encoded = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.out:
        path = Path(args.out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(encoded, encoding="utf-8")
    print(encoded)


if __name__ == "__main__":
    main()
