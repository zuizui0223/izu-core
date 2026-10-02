"""Run the prospectively frozen mutation/pleiotropy accessibility extension."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.model3_island.history import reflect_unit
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.types import (
    ArrivalConfig,
    Config,
    EVENT_ORDER,
    History,
    PlantState,
    VisitorState,
)
from scripts.prospective_trait_accessibility import advance_trait_accessibility

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "data/design/chapter2_trait_accessibility_mutation_pleiotropy_next_20261002.json"


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


def _founders(design: dict, founder_seed: int) -> PlantState:
    b = design["baseline"]
    n = int(b["capacity"])
    rng = np.random.default_rng(int(founder_seed))
    alleles = np.empty((n, 3, 2), dtype=float)
    alleles[:, 0, :] = reflect_unit(
        float(b["founder_mean_access"])
        + rng.normal(0, float(b["standing_sd_access"]), size=(n, 2))
    )
    alleles[:, 1, :] = reflect_unit(
        float(b["founder_mean_investment"])
        + rng.normal(0, float(b["standing_sd_investment"]), size=(n, 2))
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
    x = np.asarray(optima, dtype=float)
    n = len(x)
    return VisitorState(
        ids=np.arange(30_000, 30_000 + n, dtype=np.int64),
        optima=x,
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
    b = design["baseline"]
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
        depression=0.5,
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


def _first_sustained(series, initial: float, *, threshold: float, window: int):
    x = np.asarray(series, dtype=float)
    good = np.isfinite(x) & (np.abs(x - initial) >= threshold)
    if len(good) < window:
        return None
    runs = np.convolve(good.astype(int), np.ones(window, dtype=int), mode="valid")
    hits = np.flatnonzero(runs == window)
    return None if not len(hits) else int(hits[0])


def _simulate_one(
    design: dict,
    *,
    founders: PlantState,
    visitors: VisitorState,
    mutation_spec: dict,
    coupling: float,
    master_seed: int,
):
    cfg = _config(design)
    history = _history(visitors, cfg.years)
    state = founders
    streams = {name: stream(int(master_seed), name, 0) for name in STREAM_IDS}

    traits = np.full((cfg.years + 1, 2), np.nan)
    population = np.zeros(cfg.years + 1, dtype=int)

    def record(t):
        population[t] = len(state.ids)
        if len(state.ids):
            m = state.alleles.mean(axis=2).mean(axis=0)
            traits[t] = m[:2]

    record(0)
    extinction_year = None
    for year in range(cfg.years):
        old_n = len(state.ids)
        ledger = reproduce(state, history.visitors[year], cfg)
        state, _ = advance_trait_accessibility(
            state,
            ledger,
            history.seed_candidates[year],
            cfg,
            streams,
            mutation_spec=mutation_spec,
            coupling=float(coupling),
            year=year,
        )
        if old_n and not len(state.ids) and extinction_year is None:
            extinction_year = year + 1
        record(year + 1)

    tdef = design["threshold_definition"]
    ta = _first_sustained(
        traits[:, 0],
        traits[0, 0],
        threshold=float(tdef["magnitude"]),
        window=int(tdef["sustained_years"]),
    )
    tz = _first_sustained(
        traits[:, 1],
        traits[0, 1],
        threshold=float(tdef["magnitude"]),
        window=int(tdef["sustained_years"]),
    )
    censor = cfg.years + 1
    sa = censor if ta is None else ta
    sz = censor if tz is None else tz
    coordinated = bool(
        ta is not None
        and tz is not None
        and abs(ta - tz) <= int(tdef["sustained_years"])
    )
    single = bool((ta is None) != (tz is None))
    return {
        "initial_access": float(traits[0, 0]),
        "initial_investment": float(traits[0, 1]),
        "terminal_access_change": (
            None if not np.isfinite(traits[-1, 0]) else float(traits[-1, 0] - traits[0, 0])
        ),
        "terminal_investment_change": (
            None if not np.isfinite(traits[-1, 1]) else float(traits[-1, 1] - traits[0, 1])
        ),
        "access_crossing_year": ta,
        "investment_crossing_year": tz,
        "access_crossing_score": int(sa),
        "investment_crossing_score": int(sz),
        "timing_gap_access_minus_investment": int(sa - sz),
        "absolute_timing_gap": int(abs(sa - sz)),
        "coordinated_crossing": coordinated,
        "single_trait_crossing": single,
        "terminal_occupancy": int(population[-1] > 0),
        "extinction_year": extinction_year,
    }


def _median(values):
    x = np.asarray(values, dtype=float)
    return float(np.median(x)) if len(x) else None


def _mean(values):
    x = np.asarray(values, dtype=float)
    return float(np.mean(x)) if len(x) else None


def run(design: dict) -> dict:
    if design["status"] != "prospective_frozen_before_execution":
        raise ValueError("design must be frozen before execution")
    if design["implementation_boundary"]["ecological_reproduction_rules_changed"]:
        raise ValueError("ecological reproduction must remain unchanged")
    if design["implementation_boundary"]["demographic_rules_changed"]:
        raise ValueError("demography must remain unchanged")

    cfg = _config(design)
    rows = []
    for founder_seed in design["baseline"]["founder_seeds"]:
        founders = _founders(design, int(founder_seed))
        for demographic_seed in design["baseline"]["demographic_seeds"]:
            master = int(
                np.random.SeedSequence([int(founder_seed), int(demographic_seed)])
                .generate_state(1)[0]
            )
            for history_name, optima in design["baseline"]["visitor_histories"].items():
                visitors = _visitors(optima)
                for mut_name, mut in design["mutation_supply_regimes"].items():
                    for pleio_name, coupling in design["pleiotropy_regimes"].items():
                        row = _simulate_one(
                            design,
                            founders=founders,
                            visitors=visitors,
                            mutation_spec=mut,
                            coupling=float(coupling),
                            master_seed=master,
                        )
                        row.update(
                            founder_seed=int(founder_seed),
                            demographic_seed=int(demographic_seed),
                            visitor_history=history_name,
                            mutation_regime=mut_name,
                            pleiotropy_regime=pleio_name,
                            pleiotropy=float(coupling),
                        )
                        rows.append(row)

    def keyed(history, mutation, pleio):
        return {
            (r["founder_seed"], r["demographic_seed"]): r
            for r in rows
            if r["visitor_history"] == history
            and r["mutation_regime"] == mutation
            and r["pleiotropy_regime"] == pleio
        }

    mutation_tests = {}
    for history in design["baseline"]["visitor_histories"]:
        inv_shifts = []
        acc_shifts = []
        for pleio in design["pleiotropy_regimes"]:
            eq = keyed(history, "equal", pleio)
            inv = keyed(history, "investment_accessible", pleio)
            acc = keyed(history, "access_accessible", pleio)
            if set(eq) != set(inv) or set(eq) != set(acc):
                raise ValueError("paired mutation support differs")
            for key in sorted(eq):
                base_gap = eq[key]["timing_gap_access_minus_investment"]
                inv_shifts.append(
                    inv[key]["timing_gap_access_minus_investment"] - base_gap
                )
                acc_shifts.append(
                    acc[key]["timing_gap_access_minus_investment"] - base_gap
                )
        mutation_tests[history] = {
            "investment_accessible_gap_shift_median": _median(inv_shifts),
            "access_accessible_gap_shift_median": _median(acc_shifts),
            "n_paired": len(inv_shifts),
        }

    mutation_supported = bool(
        any(v["investment_accessible_gap_shift_median"] > 0 for v in mutation_tests.values())
        and any(v["access_accessible_gap_shift_median"] < 0 for v in mutation_tests.values())
    )

    pleiotropy_tests = {}
    for history in design["baseline"]["visitor_histories"]:
        coord_diff = []
        gap_diff = []
        for mut in design["mutation_supply_regimes"]:
            independent = keyed(history, mut, "independent")
            strong = keyed(history, mut, "strong_positive")
            if set(independent) != set(strong):
                raise ValueError("paired pleiotropy support differs")
            for key in sorted(independent):
                coord_diff.append(
                    int(strong[key]["coordinated_crossing"])
                    - int(independent[key]["coordinated_crossing"])
                )
                gap_diff.append(
                    strong[key]["absolute_timing_gap"]
                    - independent[key]["absolute_timing_gap"]
                )
        pleiotropy_tests[history] = {
            "strong_minus_independent_coordinated_fraction": _mean(coord_diff),
            "strong_minus_independent_absolute_gap_median": _median(gap_diff),
            "n_paired": len(coord_diff),
        }

    right = pleiotropy_tests["right4"]
    left = pleiotropy_tests["left4"]
    right_facilitated = bool(
        right["strong_minus_independent_coordinated_fraction"] > 0
        or right["strong_minus_independent_absolute_gap_median"] < 0
    )
    left_constrained = bool(
        left["strong_minus_independent_coordinated_fraction"] < 0
        or left["strong_minus_independent_absolute_gap_median"] > 0
    )

    cell_summary = []
    for history in design["baseline"]["visitor_histories"]:
        for mut in design["mutation_supply_regimes"]:
            for pleio in design["pleiotropy_regimes"]:
                cell = [
                    r for r in rows
                    if r["visitor_history"] == history
                    and r["mutation_regime"] == mut
                    and r["pleiotropy_regime"] == pleio
                ]
                cell_summary.append({
                    "visitor_history": history,
                    "mutation_regime": mut,
                    "pleiotropy_regime": pleio,
                    "n": len(cell),
                    "mean_terminal_occupancy": _mean([r["terminal_occupancy"] for r in cell]),
                    "median_access_crossing_score": _median([r["access_crossing_score"] for r in cell]),
                    "median_investment_crossing_score": _median([r["investment_crossing_score"] for r in cell]),
                    "median_timing_gap_access_minus_investment": _median(
                        [r["timing_gap_access_minus_investment"] for r in cell]
                    ),
                    "mean_coordinated_crossing": _mean(
                        [int(r["coordinated_crossing"]) for r in cell]
                    ),
                    "mean_single_trait_crossing": _mean(
                        [int(r["single_trait_crossing"]) for r in cell]
                    ),
                    "mean_terminal_access_change": _mean([
                        r["terminal_access_change"]
                        for r in cell
                        if r["terminal_access_change"] is not None
                    ]),
                    "mean_terminal_investment_change": _mean([
                        r["terminal_investment_change"]
                        for r in cell
                        if r["terminal_investment_change"] is not None
                    ]),
                })

    return {
        "status": "complete_mutation_pleiotropy_accessibility_extension",
        "design_sha256": hashlib.sha256(_canonical_bytes(design)).hexdigest(),
        "n_trajectories": len(rows),
        "mutation_accessibility_tests": mutation_tests,
        "mutation_accessibility_supported": mutation_supported,
        "pleiotropy_tests": pleiotropy_tests,
        "right_aligned_pleiotropy_facilitated": right_facilitated,
        "left_antagonistic_pleiotropy_constrained": left_constrained,
        "context_dependent_pleiotropy_supported": bool(
            right_facilitated and left_constrained
        ),
        "cell_summary": cell_summary,
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
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(encoded, encoding="utf-8")
    print(encoded)


if __name__ == "__main__":
    main()
