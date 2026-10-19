"""Read-only exact Bayes-prediction ceiling for preexisting TECHNICAL Model3 sources.

NO new source genotype draws, biological updates, fitted model, p-values,
scientific preregistration, natural-island results or genotype evolution.
Uses the original 6 exposed artificial lineages × two exposed island contexts.
The Bernoulli outcome is initial establishment by one census, with
arrival probability .8. This is an illustrative mathematical audit ONLY.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

from scripts.chapter2_two_origins_technical_20261019 import (
    ESTABLISHMENT_MODES, Island, SourceLineage, _config,
    _expressed_state, _neutral_establishment_state, _visitors,
    source_genotype, source_traits,
)
from scripts.model3_island.reproduction import reproduce

STATUS = "TECHNICAL_EXPECTED_SCORE_IDENTITY_NOT_REGISTERED"


def exposed_sources():
    """Source generator and sample sizes are fixed by the original v3 TECHNICAL run."""
    return tuple(
        SourceLineage(k, a, i, source_seed=73000 + k, arrival_probability=.80)
        for k, (a, i) in enumerate(
            (a, i) for a in (.25, .50, .75) for i in (.35, .65)
        )
    )


def exposed_islands():
    return (Island("no_visitors_harsh", 4.5, 0),
            Island("visitors_milder", 8., 4))


def exact_propensity(lineage, island, establishment_mode):
    if establishment_mode not in ESTABLISHMENT_MODES:
        raise ValueError("unknown establishment expression intervention")
    state = source_genotype(lineage)
    src = source_traits(state)
    freeze_a = establishment_mode in ("neutral_A", "neutral_A_I", "trait_neutral")
    freeze_i = establishment_mode in ("neutral_I", "neutral_A_I", "trait_neutral")
    cfg = _config(island, assurance_mode="fixed" if freeze_a else "evolving",
                  initial_a=.5 if freeze_a else src["A"])
    expressed = (_neutral_establishment_state(state)
                 if establishment_mode == "trait_neutral"
                 else _expressed_state(state, .5, freeze_i))
    ledger = reproduce(expressed, _visitors(island), cfg)
    lam = float(ledger.outcross.sum() + ledger.self_viable.sum())
    if not math.isfinite(lam) or lam < 0:
        raise ValueError("unexpected negative/nonfinite native recruitment")
    p_est_given_arrival = -math.expm1(-lam)
    p_arrived = lineage.arrival_probability * island.arrival_multiplier
    p_est_from_candidate = p_arrived * p_est_given_arrival
    if not (0 <= p_est_given_arrival <= 1 and 0 <= p_est_from_candidate <= p_arrived):
        raise ValueError("invalid initial-stage probabilistic decomposition")
    return dict(
        source_id=lineage.lineage_id,
        source_A=src["A"],
        source_I=src["I"],
        arrival_probability=p_arrived,
        expected_viable_recruits=lam,
        p_establish_given_arrival=p_est_given_arrival,
        p_establish_from_candidate=p_est_from_candidate,
    )


def optimal_source_forecast_scores(p):
    """Exact expected proper-score comparison for Bernoulli(Y|source)=p_j.

    Source labels are EQUALLY weighted, and their probabilities are assumed
    known to a perfect oracle. No actual future outcome labels are used.
    Oracle expected Brier risk is mean[p(1-p)]; constant-mean predictor
    has risk mu(1-mu), hence its improvement is population Var(p).
    This is irreducible binary fate noise vs explainable source propensity,
    NOT a fitted model, held-out predictive accuracy or causal variance share.
    """
    p = np.asarray(p, dtype=np.float64)
    if p.ndim != 1 or not len(p) or not np.isfinite(p).all() or ((p < 0) | (p > 1)).any():
        raise ValueError("source propensity vector must be finite nonempty [0,1]")
    mu = float(np.mean(p))
    base = float(mu * (1. - mu))
    oracle = float(np.mean(p * (1. - p)))
    between = float(np.mean((p - mu) ** 2))
    if abs(base - oracle - between) > 1e-13:
        raise ArithmeticError("Brier predictive information identity broken")
    clip = np.clip(p, 1e-12, 1. - 1e-12)
    ent = float(np.mean(-(p * np.log(clip) + (1. - p) * np.log1p(-clip))))
    base_ent = float(-mu * math.log(max(mu, 1e-12)) -
                     (1. - mu) * math.log(max(1. - mu, 1e-12)))
    return dict(
        sources=len(p), mean_fate_probability=mu,
        baseline_expected_brier=base,
        perfect_source_oracle_expected_brier=oracle,
        expected_brier_gain=between,
        relative_brier_gain=between / base if base > 0 else None,
        oracle_expected_binary_accuracy=float(np.mean(np.maximum(p, 1 - p))),
        constant_expected_binary_accuracy=float(max(mu, 1 - mu)),
        oracle_expected_log_loss=ent,
        constant_expected_log_loss=base_ent,
        expected_log_loss_gain=base_ent-ent,
        inference="KNOWN_PROBABILITY_ORACLE_NOT_LEARNED_HELD_OUT_PREDICTION",
    )


def analyze():
    result = []
    for island in exposed_islands():
        arms = {}
        for mode in ESTABLISHMENT_MODES:
            rows = [exact_propensity(z, island, mode) for z in exposed_sources()]
            source_p = [z["p_establish_from_candidate"] for z in rows]
            conditional_p = [z["p_establish_given_arrival"] for z in rows]
            arms[mode] = dict(
                source_propensities=rows,
                candidate_to_establishment=optimal_source_forecast_scores(source_p),
                arrival_conditional=optimal_source_forecast_scores(conditional_p),
            )
        # The initial A/I/M-normalized negative control should equalize all
        # source-origin reproduction probabilities by construction.
        neutral = arms["trait_neutral"]["source_propensities"]
        if max(x["p_establish_from_candidate"] for x in neutral) - min(
                x["p_establish_from_candidate"] for x in neutral) > 1e-13:
            raise ValueError("original founding neutral-control source variation")
        result.append(dict(island=island.island_id,
                           ovule_budget=island.ovule_budget,
                           visitor_count=island.visitors,
                           mode_results=arms))
    return dict(
        status=STATUS, original_exposed_source_ids=list(range(6)),
        no_new_genotypes_or_biological_updates=True,
        independent_heldout_validation=False,
        actual_establishment_observations_used=False,
        per_island_source_weights="six exposed technical sources equally weighted",
        source_labels_are_independent_islands=False,
        event="one-update establishment; arrival and demographic recruitment may fail",
        result=result,
        claim_boundary=[
            "This oracle knows source-conditional model probabilities; it is not a fitted model.",
            "Explained binary-fate variance may be small despite steep phenotype/probability gradients.",
            "The six exposed source genotypes and two exposed island regimes cannot validate generality.",
            "Post-establishment population persistence and A/I evolution are not tested.",
            "No quantitative result is evidence for natural mainland lineage filtering or self-compatibility.",
        ],
    )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--read-only-technical", action="store_true")
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    if not args.read_only_technical:
        p.error("explicit read-only technical opt-in required; no production action available")
    out = json.dumps(analyze(), sort_keys=True, ensure_ascii=False, indent=2,
                     allow_nan=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(out, encoding="utf-8")
    else:
        print(out, end="")


if __name__ == "__main__":
    main()
