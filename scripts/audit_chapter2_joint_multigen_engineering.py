"""Controlled 80-generation Model3 K/B reproduction pilot; NOT a confirmation cohort.

Two hand-authored FIXED ecological visitor conditions (two visitors vs no
visitors), one deterministic eight-founder genotype state, and paired nested
demographic RNG trajectories. Entirely post-design explanatory exploration.
Never accesses archived Chapter 2 visitor histories or future outcome shards.

Assays allele transmission conditional on occupied parents and UNCONDITIONAL
occupancy across all paths, avoiding extinct-phenotype-zero bias. Does not
impose A-first/I-first phenotype expression schedules, so cannot re-test or
extend the #451 registered expression-order interaction.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import json
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_joint_one_step_genetics_occupancy import GATES
from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.chapter2_postzygotic_viability_gate import gate_postzygotic_seed_viability
from scripts.model3_island.population import advance, subset
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.model3_island.run import founders_from_spec
from scripts.model3_island.types import VisitorState
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as model_config, load_design,
)

STATUS = "POST_OUTCOME_CONTROLLED_MULTIGENERATION_ENGINEERING_PILOT"
CAPACITIES = (8, 48)
GATE_LABELS = ("baseline", "half_self", "half_outcross")
VISITOR_REGIMES = ("two_hand_authored", "no_visitors")
ROOT_FOUNDER_SEED = 8904102
DEFAULT_REPLICATE_MASTER = 8904103


def engineering_fixture(*, ovule_budget=3.0):
    """Independent synthetic founders: retain standing variation at ALL loci."""
    d = load_design(DEFAULT_DESIGN)
    initial = founders_from_spec(
        {"count": 8, "draw_count": 8, "means": [0.5, 0.5, 0.5],
         "sd": 0.15, "birth_year": 0},
        ROOT_FOUNDER_SEED,
    )
    cfg = replace(
        model_config(d, "prior_selfing", 0.0, "evolving"),
        capacity=8, survival=0.0, mutation_rate=0.0, mutation_sd=0.0,
        ovule_budget=float(ovule_budget),
        seed_arrival=replace(
            model_config(d, "prior_selfing", 0.0, "evolving").seed_arrival,
            supply=0.0,
        ),
    )
    v = VisitorState(
        ids=np.array([10, 11], dtype=np.int64),
        optima=np.array([0.3, 0.7]),
        breadths=np.array([0.6, 0.6]),
        effectiveness=np.array([0.9, 0.8]),
    )
    return initial, cfg, {
        "two_hand_authored": v,
        "no_visitors": VisitorState(
            ids=np.empty(0, dtype=np.int64),
            optima=np.empty(0), breadths=np.empty(0),
            effectiveness=np.empty(0),
        ),
    }


def condition_run(initial, config, visitor, *, gate, draw, master, years):
    """One paired demographic path, no archived visitor history."""
    if gate not in GATE_LABELS or not 1 <= years <= 80:
        raise ValueError("unregistered engineering gate or horizon")
    cfg = config
    streams = {name: stream(master, name, draw) for name in STREAM_IDS}
    current = initial
    empty = subset(initial, np.empty(0, dtype=int))
    census = [len(current.ids)]
    expected_direction = []
    realized_direction = []
    recruited_self = recruited_outcross = 0
    first_extinction = None
    for year in range(years):
        if not len(current.ids):
            census.append(0)
            expected_direction.append(None)
            realized_direction.append(None)
            continue
        ancestor_mean = current.alleles.mean(axis=(0, 2))
        pre = reproduce_kb(current, visitor, cfg,
                           background_denominator_capacity=48)
        sf, oc = GATES[gate]
        ledger = gate_postzygotic_seed_viability(
            pre, selfed_fraction=sf, outcross_fraction=oc
        )
        w = ledger.outcross.copy()
        w[np.diag_indices(len(current.ids))] += ledger.self_viable
        mass = float(w.sum())
        if mass:
            dosage = current.alleles.mean(axis=2)
            expectation = (
                .5 * np.einsum("i,ik->k", w.sum(axis=1), dosage)
                + .5 * np.einsum("i,ik->k", w.sum(axis=0), dosage)
            ) / mass
            expected_direction.append((expectation - ancestor_mean).tolist())
        else:
            expected_direction.append(None)
        current, info = advance(
            current, ledger, empty, cfg, streams, year=400 + year,
        )
        census.append(len(current.ids))
        recruited_self += info["resident_selfed_recruits"]
        recruited_outcross += info["resident_outcross_recruits"]
        if len(current.ids):
            new_mean = current.alleles.mean(axis=(0, 2))
            realized_direction.append((new_mean - ancestor_mean).tolist())
        else:
            realized_direction.append(None)
            first_extinction = year + 1
    return {
        "occupied": bool(len(current.ids)),
        "first_extinction": first_extinction,
        "census": census,
        "first_step_expected_direction": expected_direction[0],
        "first_step_realized_direction": realized_direction[0],
        "end_genetic_mean_given_occupied": (
            current.alleles.mean(axis=(0, 2)).tolist()
            if len(current.ids) else None
        ),
        "expected_directions_when_occupied": expected_direction,
        "realized_directions_when_occupied": realized_direction,
        "self_recruits": recruited_self,
        "outcross_recruits": recruited_outcross,
    }


def run_pilot(*, draws=24, years=80, ovule_budget=3.0):
    if (type(draws) is not int or not 1 <= draws <= 256
            or type(years) is not int or not 1 <= years <= 80):
        raise ValueError("restricted engineering pilot only")
    if (isinstance(ovule_budget,bool) or not isinstance(ovule_budget,(int,float))
            or not np.isfinite(ovule_budget) or not 1.0 <= ovule_budget <= 12.0):
        raise ValueError('restricted ovule budget engineering window')
    initial, base_cfg, visitors = engineering_fixture(ovule_budget=ovule_budget)
    reports = {}
    for regime in VISITOR_REGIMES:
        reports[regime] = {}
        v = visitors[regime]
        for k in CAPACITIES:
            for gate in GATE_LABELS:
                key = f"K{k}_{gate}"
                outcomes = [
                    condition_run(
                        initial, replace(base_cfg, capacity=k), v,
                        gate=gate, draw=draw, master=DEFAULT_REPLICATE_MASTER,
                        years=years,
                    )
                    for draw in range(draws)
                ]
                occupied = np.asarray(
                    [int(o["occupied"]) for o in outcomes], dtype=int
                )
                surviving_genetic = [
                    o["end_genetic_mean_given_occupied"]
                    for o in outcomes if o["occupied"]
                ]
                first_dir = [
                    o["first_step_expected_direction"]
                    for o in outcomes
                ]
                assert all(x == first_dir[0] for x in first_dir)
                reports[regime][key] = {
                    "n_demographic_repeats_within_one_fixed_visitor_regime": draws,
                    "occupied_count": int(occupied.sum()),
                    "occupied_probability_descriptive_only": float(occupied.mean()),
                    "first_step_expected_direction": first_dir[0],
                    "end_genetic_mean_conditional_on_occupancy": (
                        np.mean(surviving_genetic, axis=0).tolist()
                        if surviving_genetic else None
                    ),
                    "n_occupied_genetic_endpoints": len(surviving_genetic),
                    "cumulative_self_recruits_descriptive": int(
                        sum(o["self_recruits"] for o in outcomes)
                    ),
                    "cumulative_outcross_recruits_descriptive": int(
                        sum(o["outcross_recruits"] for o in outcomes)
                    ),
                    "occupied_by_demographic_rep": occupied.tolist(),
                }
        # Treat the exact same paired replicate identities across all gates.
        contrasts = {}
        for k in CAPACITIES:
            b = np.array(reports[regime][f"K{k}_baseline"]["occupied_by_demographic_rep"])
            for gate in ("half_self", "half_outcross"):
                g = np.array(reports[regime][f"K{k}_{gate}"]["occupied_by_demographic_rep"])
                contrast = b-g
                contrasts[f"K{k}_{gate}"] = {
                    "baseline_minus_gate_occupancy": float(contrast.mean()),
                    "paired_demographic_difference_counts": {
                        "-1":int(np.sum(contrast==-1)),
                        "0":int(np.sum(contrast==0)),
                        "1":int(np.sum(contrast==1)),
                    },
                }
        for gate in ("half_self", "half_outcross"):
            contrasts[f"K8_minus_K48_{gate}"] = {
                "descriptive_gate_sensitivity_interaction": (
                    contrasts[f"K8_{gate}"]["baseline_minus_gate_occupancy"]
                    - contrasts[f"K48_{gate}"]["baseline_minus_gate_occupancy"]
                ),
                "not_equivalent_to_451_A_minus_I_estimand": True,
            }
        reports[regime]["comparisons"] = contrasts
    return {
        "status": STATUS,
        "design": {
            "model": "unmodified original Model3 advance + independently frozen reproduce_kb",
            "biological_setting": "prior_selfing", "founder_count":8,
            "founder_source": "new deterministic eight-genotype engineering fixture, not prehistory",
            "founder_seed":ROOT_FOUNDER_SEED,
            "shared_demographic_rng_master":DEFAULT_REPLICATE_MASTER,
            "demographic_repeats_per_visitor_regime":draws,
            "independent_ecological_visitor_histories":0,
            "hand_authored_fixed_visitor_regimes":list(VISITOR_REGIMES),
            "same_visitors_each_year_and_condition":True,
            "K":list(CAPACITIES), "B":48, "years":years,
            "ovule_budget":float(ovule_budget),
            "viability_gates":list(GATE_LABELS),
            "no_mutation_no_immigration_no_adult_survival":True,
            "prospective_chapter2_cohorts_accessed":False,
            "natural_island_observations":0,
            "assigned_order_schedule":False,
            "is_original_451_estimand":False,
            "confirmatory_status":"NONE_ENGINEERING_ONLY",
        },
        "results": reports,
        "interpretive_guard": (
            "This is one hand-authored deterministic environment per regime,"
            " not independent ecological histories. Demographic replicates are"
            " not natural island systems. Conditional genetic endpoints exclude"
            " extinction and must not be compared to unconditional occupancy as"
            " a mediation estimate. The A-first/I-first expression schedules of"
            " the registered #451 primary are absent, so the effect is distinct."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draws",type=int,default=24)
    parser.add_argument("--years",type=int,default=80)
    parser.add_argument("--ovule-budget",type=float,default=3.0)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    output=run_pilot(draws=args.draws,years=args.years,ovule_budget=args.ovule_budget)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(output,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print(json.dumps({
        "status":output["status"],"draws":args.draws,"years":args.years,
        "two_visitor_contrasts":output["results"]["two_hand_authored"]["comparisons"],
        "no_visitor_contrasts":output["results"]["no_visitors"]["comparisons"],
    },sort_keys=True))


if __name__=="__main__":
    main()
