"""Exploratory secondary-colonisation experiment using unchanged finite Model3.

NOT confirmation, a natural island history, or a proof of reverse migration.
A mainland analogue means a prescribed functional-visitor environment, not
geography. Trait-locus ancestry does not identify neutral migrant ancestry.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.model3_island.history import reach_probability, reflect_unit
from scripts.model3_island.population import advance, concatenate, inherit, subset
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.types import Config, PlantState, VisitorState
from scripts.readaptation_assay_20261019 import assay_population

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/model3_island_v2.json"
FROZEN_PROTOCOL = ROOT / "docs/CHAPTER2_SECONDARY_COLONIZATION_PILOT_20261020.md"
FOUNDER_SEEDS = (202610201, 202610202)
VISITOR_SEEDS = (202610211, 202610212)
CHECKPOINTS = (10, 25)
HISTORY_HORIZON = 25
FUTURE_HORIZON = 20
FUTURE_REPEATS = 2
PROPAGULE_CAP = 8
ESTABLISHMENT = 0.8
DISTANCES = (0.0, 1.5)
DESTINATIONS = ("island_like_vacant", "mainland_like_vacant", "mainland_like_resident")
ANCESTRY_LIMIT = 100_000_000
STATUS = "EXPLORATORY_SECONDARY_COLONISATION_NO_CONFIRMATORY_CLAIM"


def master_seed(*tokens: int) -> int:
    return int(np.random.SeedSequence([20261020, *tokens]).generate_state(1)[0])


def streams(seed: int) -> dict:
    return {key: stream(seed, key, 0) for key in STREAM_IDS}


def configuration(policy: str, years: int = HISTORY_HORIZON + FUTURE_HORIZON) -> Config:
    base = json.loads(DESIGN.read_text(encoding="utf-8"))["base_config"]
    base.update(
        capacity=48, years=years, survival=0., ovule_budget=8.,
        investment_cost=.5, depression=.5, mutation_rate=0.,
        assurance_mode=policy, fixed_assurance=.5,
        assurance_timing="delayed", assurance_cost=.5,
        activity=.4, activity_mode="count_scaled",
        reference_visitor_count=6.,
    )
    base["seed_arrival"]["supply"] = 0.
    base["visitor_arrival"]["supply"] = 0.
    return Config.from_dict(base)


def make_founders(seed: int, founder_index: int) -> PlantState:
    rng = stream(seed, "founders", 0)
    alleles = reflect_unit(
        np.array([.5, .5, .5])[None, :, None]
        + rng.normal(0., .08, size=(48, 3, 2))
    )
    alleles[:, 1, :] = rng.choice([.375, .5, .625], size=(48, 2))
    alleles[:, 2, :] = rng.choice([.25, .5, .75], size=(48, 2))
    origins = np.arange(48 * 6, dtype=np.int64).reshape(48, 3, 2) + (founder_index + 1) * 1_000_000
    assert origins.max() < ANCESTRY_LIMIT
    return PlantState(
        alleles, origins, np.zeros((48, 3, 2), dtype=bool),
        np.arange(48, dtype=np.int64), np.zeros(48, dtype=np.int64),
    )


def visitors_for(seed: int) -> tuple[VisitorState, VisitorState]:
    rng = stream(seed, "visitor_initial", 0)
    optima = rng.uniform(.35, .65, 6)
    full = VisitorState(
        np.arange(6, dtype=np.int64), optima,
        np.full(6, .2), np.ones(6),
    )
    sparse = VisitorState(
        full.ids[:1], full.optima[:1],
        full.breadths[:1], full.effectiveness[:1],
    )
    return full, sparse


def historical_donors(
    founders: PlantState, full: VisitorState, sparse: VisitorState, seed: int
) -> dict[tuple[int, str], PlantState]:
    result = {(0, "ancestral"): founders}
    for policy in ("fixed", "evolving"):
        cfg = configuration(policy)
        random_streams = streams(seed)
        current = founders
        empty = subset(founders, slice(0, 0))
        for year in range(HISTORY_HORIZON):
            visitors = full if year < 5 else sparse
            current, _ = advance(
                current, reproduce(current, visitors, cfg), empty,
                cfg, random_streams, year=year, mutation_traits=(False, False, False),
            )
            if year + 1 in CHECKPOINTS:
                result[(year + 1, policy)] = current
    assert len(result) == 1 + 2 * len(CHECKPOINTS)
    return result


def seed_cohort(
    donor: PlantState, cfg: Config, common_source_visitors: VisitorState, seed: int
) -> tuple[PlantState, dict]:
    """Native sexual offspring production; identical visitor context for all origins.

    Using a shared pollen environment for production isolates inherited donor
    differences. It does not model natural dispersal from each source habitat.
    """
    empty = subset(donor, slice(0, 0))
    if not len(donor.ids):
        return empty, {"seed_potential": 0, "cohort_size": 0}
    rnd = streams(seed)
    ledger = reproduce(donor, common_source_visitors, cfg)
    parent_weights = ledger.outcross.copy()
    np.fill_diagonal(parent_weights, ledger.self_viable)
    total = float(parent_weights.sum())
    potential = int(rnd["recruitment"].poisson(total))
    count = min(PROPAGULE_CAP, potential)
    if count:
        choices = rnd["parents"].choice(
            len(donor.ids) ** 2, size=count, p=(parent_weights / total).ravel()
        )
        fathers, mothers = np.unravel_index(choices, parent_weights.shape)
    else:
        mothers = fathers = np.empty(0, dtype=np.int64)
    children = inherit(
        donor, mothers, fathers, cfg,
        segregation_rng=rnd["segregation"], mutation_rng=rnd["mutation"],
        year=HISTORY_HORIZON + 1, mutation_traits=(False, False, False),
    )
    rebased = replace(
        children, ids=np.arange(count, dtype=np.int64),
        birth_years=np.zeros(count, dtype=np.int64),
    )
    return rebased, {"seed_potential": potential, "cohort_size": count}


def reference_residents() -> PlantState:
    n = 40
    return PlantState(
        np.full((n, 3, 2), .5),
        np.arange(n * 6, dtype=np.int64).reshape(n, 3, 2) + 1_000_000_000_000,
        np.zeros((n, 3, 2), dtype=bool),
        np.arange(100, 100 + n, dtype=np.int64),
        np.zeros(n, dtype=np.int64),
    )


def source_allele_mask(state: PlantState) -> np.ndarray:
    return state.allele_origin < ANCESTRY_LIMIT


def ancestry_summary(state: PlantState) -> dict:
    mask = source_allele_mask(state)
    carriers = mask.any(axis=(1, 2))
    focal_I = state.alleles[:, 1, :][mask[:, 1, :]]
    return {
        "population": len(state.ids),
        "source_carriers": int(carriers.sum()),
        "source_allele_copies": int(mask.sum()),
        "source_I_max": float(focal_I.max()) if len(focal_I) else None,
        "source_I_polymorphic": bool(len(np.unique(focal_I)) > 1),
        "source_carrier_mean_I": (
            float(state.alleles[carriers, 1, :].mean()) if carriers.any() else None
        ),
        "source_carrier_mean_A": (
            float(state.alleles[carriers, 2, :].mean()) if carriers.any() else None
        ),
    }


def destination_visitors(full: VisitorState, sparse: VisitorState, destination: str) -> VisitorState:
    if destination not in DESTINATIONS:
        raise ValueError("unknown destination")
    return sparse if destination == "island_like_vacant" else full


def lineage_assay(state: PlantState, cfg: Config, visitors: VisitorState) -> float | None:
    carriers = source_allele_mask(state).any(axis=(1, 2))
    if not carriers.any():
        return None
    return assay_population(subset(state, carriers), cfg, visitors)["mean_genetic_return"]


def destination_future(
    cohort: PlantState, full: VisitorState, sparse: VisitorState,
    destination: str, distance: float, arrival_seed: int, future_seed: int,
    founder_mean_I: float,
) -> dict:
    """One seed arrival, then local reproduction with no subsequent immigration."""
    if distance not in DISTANCES:
        raise ValueError("distance outside frozen grid")
    cfg = configuration("evolving")
    visitors = destination_visitors(full, sparse, destination)
    p_arrival = ESTABLISHMENT * reach_probability(distance, 1., "exponential")
    mask = stream(arrival_seed, "seed_settlement", 0).random(len(cohort.ids)) < p_arrival
    settlers = subset(cohort, mask)
    if destination == "mainland_like_resident":
        state = concatenate((reference_residents(), settlers))
    else:
        state = settlers
    if len(state.ids) > cfg.capacity:
        raise AssertionError("overfilled target habitat")
    initial = ancestry_summary(state)
    initial_return = lineage_assay(state, cfg, visitors)
    rnd = streams(future_seed)
    empty = subset(state, slice(0, 0))
    censuses = [initial]
    lost_at = 0 if not initial["source_allele_copies"] else None
    for year in range(FUTURE_HORIZON):
        state, _ = advance(
            state, reproduce(state, visitors, cfg), empty, cfg, rnd,
            year=year, mutation_traits=(False, False, False),
        )
        record = ancestry_summary(state)
        censuses.append(record)
        if record["source_allele_copies"] == 0 and lost_at is None:
            lost_at = year + 1
        if record["source_allele_copies"] > censuses[-2]["source_allele_copies"] * 6:
            # No bound on overall expansion of descendant alleles; this is
            # deliberately not treated as population or mutation conservation.
            pass
        previous_max = censuses[-2]["source_I_max"]
        if previous_max is not None and record["source_I_max"] is not None:
            if record["source_I_max"] > previous_max + 1e-12:
                raise AssertionError("new source I alleles without mutation/immigration")
    final = censuses[-1]
    final_return = lineage_assay(state, cfg, visitors)
    return {
        "destination": destination,
        "distance": distance,
        "arrival_probability_per_seed": p_arrival,
        "settled_seeds": len(settlers.ids),
        "initial": initial,
        "final": final,
        "source_lineage_present_at_horizon": final["source_allele_copies"] > 0,
        "source_I_above_founder_at_end": (
            final["source_I_max"] >= founder_mean_I - 1e-12
            if final["source_I_max"] is not None else None
        ),
        "first_source_allele_absence": lost_at,
        "entry_common_context_return": initial_return,
        "final_common_context_return": final_return,
        "return_change_given_lineage_present": (
            final_return - initial_return
            if initial_return is not None and final_return is not None else None
        ),
        "censuses": censuses,
    }


def source_fingerprint() -> dict[str, str]:
    paths = [
        Path(__file__), FROZEN_PROTOCOL, DESIGN,
        ROOT / "scripts/model3_island/types.py",
        ROOT / "scripts/model3_island/population.py",
        ROOT / "scripts/model3_island/reproduction.py",
        ROOT / "scripts/model3_island/randomness.py",
        ROOT / "scripts/model3_island/history.py",
        ROOT / "scripts/readaptation_assay_20261019.py",
    ]
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in paths}


def run_experiment(
    founder_seeds=FOUNDER_SEEDS, visitor_seeds=VISITOR_SEEDS,
    repeats=FUTURE_REPEATS,
) -> dict:
    if not founder_seeds or not visitor_seeds or not (1 <= repeats <= FUTURE_REPEATS):
        raise ValueError("invalid bounded pilot allocation")
    rows = []
    sources = []
    for fi, fseed in enumerate(founder_seeds):
        founders = make_founders(fseed, fi)
        founder_mean_I = float(founders.alleles[:, 1, :].mean())
        for vi, vseed in enumerate(visitor_seeds):
            full, sparse = visitors_for(vseed)
            donor_states = historical_donors(
                founders, full, sparse, master_seed(0, fi, vi)
            )
            for si, ((epoch, policy), donor) in enumerate(donor_states.items()):
                cfg = configuration("evolving" if policy == "ancestral" else policy)
                cohort, seed_info = seed_cohort(
                    donor, cfg, full, master_seed(1, fi, vi, si)
                )
                sources.append({
                    "founder": fi, "visitor_history": vi, "source_index": si,
                    "history_epoch": epoch, "historical_A_policy": policy,
                    "donor_alive": bool(len(donor.ids)),
                    "donor_population": len(donor.ids),
                    "donor_max_I": (
                        float(donor.alleles[:, 1, :].max()) if len(donor.ids) else None
                    ),
                    "founder_mean_I": founder_mean_I, **seed_info,
                })
                for di, destination in enumerate(DESTINATIONS):
                    for li, distance in enumerate(DISTANCES):
                        for repeat in range(repeats):
                            future = destination_future(
                                cohort, full, sparse, destination, distance,
                                master_seed(2, fi, vi, di, li, repeat),
                                master_seed(3, fi, vi, di, li, repeat),
                                founder_mean_I,
                            )
                            rows.append({
                                "founder": fi, "visitor_history": vi,
                                "source_index": si, "history_epoch": epoch,
                                "historical_A_policy": policy,
                                "replicate": repeat,
                                "source_seed_production": seed_info,
                                **future,
                            })
    expected = (len(founder_seeds) * len(visitor_seeds)
                * (1 + 2 * len(CHECKPOINTS))
                * len(DESTINATIONS) * len(DISTANCES) * repeats)
    assert len(rows) == expected
    # Counts are descriptive across nested descendants, not IID replicates.
    summaries = []
    for epoch, policy in ((0, "ancestral"), *(
        (t, a) for t in CHECKPOINTS for a in ("fixed", "evolving")
    )):
        for destination in DESTINATIONS:
            for distance in DISTANCES:
                selected = [
                    r for r in rows if r["history_epoch"] == epoch
                    and r["historical_A_policy"] == policy
                    and r["destination"] == destination
                    and r["distance"] == distance
                ]
                summaries.append({
                    "epoch": epoch, "policy": policy, "destination": destination,
                    "distance": distance, "nested_paths": len(selected),
                    "original_founder_visitor_blocks": len(founder_seeds) * len(visitor_seeds),
                    "any_seed_settled": sum(r["settled_seeds"] > 0 for r in selected),
                    "source_allele_survival": sum(
                        r["source_lineage_present_at_horizon"] for r in selected
                    ),
                    "destination_occupied": sum(
                        r["final"]["population"] > 0 for r in selected
                    ),
                    "successful_lineage_assay_pairs": sum(
                        r["return_change_given_lineage_present"] is not None
                        for r in selected
                    ),
                })
    return {
        "status": STATUS,
        "scientific_unit": "crossed founder and visitor histories; futures nested",
        "founders": list(founder_seeds), "visitor_histories": list(visitor_seeds),
        "history_checkpoints": list(CHECKPOINTS),
        "historical_updates": HISTORY_HORIZON,
        "future_updates_per_path": FUTURE_HORIZON,
        "future_paths": len(rows), "sources": sources, "summary": summaries,
        "paths": rows, "source_sha256": source_fingerprint(),
        "limitations": [
            "Artificial mainland analogue; not documented geographical reverse migration",
            "Historical fixed A still permits selfing; recipient A expression evolves in every treatment",
            "Seed production standardised to same pollen service; not native-source dispersal supply",
            "Arrival probability is an imposed kernel and all settled seeds enter available slots",
            "Resident group is a fixed initial synthetic reference, not a coevolved mainland community",
            "Tracked origins are three selected loci, not neutral whole-genome ancestry",
            "No new seed immigration or mutation after settlement",
            "Trait shift is not by itself evidence of improved adaptation",
            "Nested futures cannot be treated as independent founder or island histories",
            "No inferential interval, causal A mediation, or natural generality claim",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--exploratory-pilot", action="store_true")
    args = parser.parse_args()
    if not args.exploratory_pilot:
        parser.error("explicit --exploratory-pilot acknowledgement required")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists():
        parser.error("result already exists; refusing overwrite")
    result = run_experiment()
    with args.output.open("x", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, allow_nan=False)
        fh.write("\n")
    print(json.dumps({
        "status": result["status"], "future_paths": result["future_paths"],
        "independent_crossed_blocks": len(result["founders"]) * len(result["visitor_histories"]),
        "summary": result["summary"], "sha256": result["source_sha256"],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
