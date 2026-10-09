"""Postzygotic viability gates for a planned Chapter 2 mechanistic intervention.

Only expected viable SEED contributions change at recruitment. Pollen transfer,
ovule budget, pre-intervention genotype and parental source arrays remain
unchanged. Baseline (1,1) returns the original ledger without reconstruction,
which permits exact numeric/trajectory parity checks on old visitor histories.

Not a genetic-order mediation estimator or natural-island calibration.
"""
from __future__ import annotations

import math
import numpy as np

from scripts.model3_island.types import Ledger

FACTORIAL_GATES = {
    "baseline": (1.0, 1.0),
    "attenuate_self": (0.5, 1.0),
    "attenuate_outcross": (1.0, 0.5),
    "attenuate_both": (0.5, 0.5),
}


def gate_postzygotic_seed_viability(
        ledger: Ledger, *, selfed_fraction: float,
        outcross_fraction: float) -> Ledger:
    """Experimentally lower offspring seed viability without replacing genotypes.

    The action is downstream of pollination; `self_raw` still records seeds
    before viability loss and `exported` still records donor pollen output.
    Neither is an expected recruitment/paternity substitute.
    """
    if not isinstance(ledger, Ledger):
        raise TypeError("Expected validated model Ledger")
    for label, fraction in (
        ("selfed_fraction", selfed_fraction),
        ("outcross_fraction", outcross_fraction),
    ):
        if (isinstance(fraction, (bool, np.bool_))
                or not isinstance(fraction, (int,float,np.number))
                or not math.isfinite(float(fraction))
                or not 0.0 <= float(fraction) <= 1.0):
            raise ValueError(label + " must be a finite fraction in [0, 1]")
    if selfed_fraction == 1 and outcross_fraction == 1:
        return ledger

    self_viable = np.asarray(ledger.self_viable) * float(selfed_fraction)
    outcross = np.asarray(ledger.outcross) * float(outcross_fraction)
    female_viable = outcross.sum(axis=0)
    maternal = female_viable + self_viable
    paternal = outcross.sum(axis=1) + self_viable

    # Recheck the physical bookkeeping before constructing immutable arrays.
    if ((self_viable > ledger.self_viable + 1e-12).any()
            or (outcross > ledger.outcross + 1e-12).any()
            or (maternal > ledger.maternal + 1e-9).any()
            or (maternal > ledger.ovules + 1e-9).any()
            or not np.isfinite(maternal).all()):
        raise AssertionError("Viability gate violates reproductive mass accounting")

    updated = Ledger(
        outcross=outcross,
        self_raw=ledger.self_raw,
        self_viable=self_viable,
        ovules=ledger.ovules,
        exported=ledger.exported,
        delivered=ledger.delivered,
        lost=ledger.lost,
        maternal=maternal,
        paternal=paternal,
    )
    if (not np.array_equal(updated.exported, ledger.exported)
            or not np.array_equal(updated.delivered, ledger.delivered)
            or not np.array_equal(updated.self_raw, ledger.self_raw)
            or not np.allclose(updated.maternal,
                               updated.outcross.sum(axis=0)+updated.self_viable,
                               rtol=0,atol=1e-12)
            or not np.allclose(updated.paternal,
                               updated.outcross.sum(axis=1)+updated.self_viable,
                               rtol=0,atol=1e-12)):
        raise AssertionError("Ledger gate changed prezygotic state or bookkeeping")
    return updated


def apply_named_gate(ledger: Ledger, arm: str) -> Ledger:
    """Only the four prospectively frozen interventions are admitted."""
    if arm not in FACTORIAL_GATES:
        raise ValueError("Unknown or post-outcome added viability arm")
    selfed, outcross = FACTORIAL_GATES[arm]
    return gate_postzygotic_seed_viability(
        ledger, selfed_fraction=selfed, outcross_fraction=outcross,
    )


def analyze_factorial_schedule_interactions(
        history_order_by_gate: np.ndarray) -> dict[str,np.ndarray]:
    """Pure algebra: 64 visitor history × 4 gate arms, with A-I contrasts.

    Input A-first-minus-I-first probabilities are already paired/averaged
    within each history. No resampling or biological simulations performed.
    """
    x=np.asarray(history_order_by_gate,dtype=float)
    if x.shape!=(64,4) or not np.isfinite(x).all():
        raise ValueError("The paired causal sensitivity unit must be 64 histories × 4 arms")
    baseline,self_half,outcross_half,both_half = [x[:,i] for i in range(4)]
    return {
        "common_untreated_absolute_order_effect":baseline,
        "primary_selfed_viability_sensitivity":baseline-self_half,
        "secondary_outcross_viability_sensitivity":baseline-outcross_half,
        "secondary_joint_gate_absolute_order_effect":both_half,
        "factorial_nonadditivity":baseline-self_half-outcross_half+both_half,
    }


def simulate_gated_future(
        task, state, selected_eight, d: dict, biology: dict,
        regime: str, future: str, budget: float, *,
        intervention: str) -> dict:
    """Replay the frozen future biology with one explicit postzygotic gate.

    Every t400 inherited allele, ancestry, visitor history, and demographic
    stream ID is retained. Only the seed-viability ledger presented to advance
    is experimentally attenuated. No natural mediation claim follows.
    """
    from dataclasses import replace
    from scripts.chapter2_order_postshock_runner import one_future, paired_streams
    from scripts.run_chapter2_assurance_generality import config as source_config
    from scripts.run_model3_persistent_isolation import exposure
    from scripts.model3_island.population import advance
    from scripts.model3_island.reproduction import reproduce

    if intervention not in FACTORIAL_GATES:
        raise ValueError("Unregistered postzygotic intervention")
    # Crucial bit-for-bit comparison against original audited future:
    # never recompute the no-attenuation reference.
    if intervention == "baseline":
        return one_future(task,state,selected_eight,d,biology,
                          regime,future,budget)

    if regime not in d["postshock"]["arms"]:
        raise ValueError("Unfrozen postshock regime")
    cap = 48 if regime == "unbottlenecked_capacity48" else 8
    initial = state if cap == 48 else selected_eight
    if len(initial.ids) > cap:
        raise AssertionError("Wrong frozen founder count/capacity")
    cfg = replace(
        source_config(biology,task.setting,d["postshock"]["post_mutation_rate"],
                      "evolving"),
        capacity=cap, ovule_budget=float(budget), assurance_mode="evolving",
    )
    if cfg.seed_arrival.supply != 0:
        raise AssertionError("Plant immigration is forbidden")
    visitors = exposure(
        task.visitor_history+d["postshock"]["future_visitor_seed_offset"],
        future,
    )
    streams = paired_streams(task,d,regime,future,budget)
    if len(initial.ids):
        ledger0 = apply_named_gate(
            reproduce(initial,visitors.visitors[0],cfg), intervention
        )
        payoff = {
            "maternal_viable_per_plant": float(ledger0.maternal.mean()),
            "female_outcross_per_plant":float(ledger0.outcross.sum()/len(initial.ids)),
            "paternal_export_per_plant":float(ledger0.exported.mean()),
            "viable_selfed_per_plant":float(ledger0.self_viable.mean()),
        }
    else:
        payoff = None

    current = initial
    first_extinction = 0 if not len(current.ids) else None
    recruits_self = recruits_outcross = 0
    for year in range(d["postshock"]["updates"]):
        if not len(current.ids):
            break
        candidate=visitors.seed_candidates[year]
        if len(candidate.ids):
            raise AssertionError("No external plant seed candidates allowed")
        ledger=apply_named_gate(
            reproduce(current,visitors.visitors[year],cfg), intervention
        )
        current, info=advance(
            current,ledger,candidate,cfg,streams,
            year=d["prehistory"]["updates"]+year,
            mutation_traits=(True,True,True),
        )
        recruits_self += info["resident_selfed_recruits"]
        recruits_outcross += info["resident_outcross_recruits"]
        if first_extinction is None and not len(current.ids):
            first_extinction = year+1
    if len(current.ids):
        means=current.alleles.mean(axis=2)
        endpoint={
            "means":means.mean(axis=0).tolist(),
            "variances":means.var(axis=0).tolist(),
        }
    else:
        endpoint=None
    return {
        "regime":regime,"future_visitor":future,"budget":float(budget),
        "t0_population":int(len(initial.ids)),
        "end_population":int(len(current.ids)),
        "occupied":int(bool(len(current.ids))),
        "first_extinction":first_extinction,
        "immediate_reproductive_payoff":payoff,
        "surviving_genetic_endpoint":endpoint,
        "selfed_recruits":int(recruits_self),
        "outcross_recruits":int(recruits_outcross),
        "future_assurance_mode":"evolving",
        "future_expression_offsets":[0,0],
    }
