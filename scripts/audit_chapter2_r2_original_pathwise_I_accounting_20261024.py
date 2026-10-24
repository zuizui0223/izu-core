"""Pathwise conditional expected I sorting versus realized sampling residual.

Replays only the ORIGINAL 24 source populations, their original 30-prefix and
2 x 50 source futures, using original model source/operators/RNG (no new seeded
experiments). Each source future MUST finish with the exact original Actions
ZIP terminal state SHA256; failure is fatal.

At each visited state: realized dI = E[dI | original current diploid
population and one-year source parentage] + (realized - expectation).
This is a *descriptive conditional pathwise identity*, NOT a causal
selection/drift partition, an independent biological experiment or a
generalized island-ecology inference.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import json
from math import isfinite
from pathlib import Path
from typing import Any

import numpy as np

from scripts.audit_chapter2_r2_shock_genome_expected_I_20261023 import (
    load_roster, ORIGINAL_PROTOCOL_SHA256, SOURCE_ZIP_SHA256, SOURCE_COMMIT,
)
from scripts.chapter2_pollen_baseline_factorial_20261019 import (
    admit, config, founders, visitors, streams, step, clone, fingerprint,
)
from scripts.model3_island.reproduction import reproduce

STATUS = "SOURCE_EXACT_24_ORIGINAL_FUTURES_PATHWISE_EXPECTATION_RESIDUAL_NO_NEW_EXPERIMENT"
EPS = 1e-10


def conditional_parental_I(state, ledger) -> tuple[float, float, float]:
    """Mean I among expected original resident offspring, conditional on >0 recruits.

    Source native mating: outcross[f,m] is ordered father f / mother m; viable
    autonomous selfing adds to diagonal in both Mendelian parental slots.
    No adult survival, immigration or mutation in the original source fixture.
    This is the conditional expectation of the next *offspring cohort mean*,
    not the derivative of population-wide fitness or an invasion probability.
    """
    ids = state.ids
    n = len(ids)
    if n < 1:
        raise AssertionError("original occupied model state required")
    I = np.asarray(state.alleles[:, 1, :].mean(axis=1), dtype=float)
    outcross = np.asarray(ledger.outcross, dtype=float)
    selfed = np.asarray(ledger.self_viable, dtype=float)
    if (I.shape != (n,) or outcross.shape != (n,n) or selfed.shape != (n,)
        or not np.isfinite(I).all() or not np.isfinite(outcross).all()
        or not np.isfinite(selfed).all() or (outcross < 0).any()
        or (selfed < 0).any() or (I < 0).any() or (I > 1).any()):
        raise AssertionError("invalid native source genotype or reproductive ledger")
    total = float(outcross.sum() + selfed.sum())
    ovules = float(np.asarray(ledger.ovules).sum())
    if not (total > 0 and ovules > 0 and isfinite(total)):
        raise AssertionError("original source has no viable expected resident reproduction")
    parent_half_contrib = (0.5 * outcross.sum(axis=0) +
                           0.5 * outcross.sum(axis=1) + selfed)
    expected_mean = float(np.dot(I, parent_half_contrib) / total)
    # Independent ordered parentage formula including selfing on diagonal.
    P = outcross.copy()
    P[np.diag_indices(n)] += selfed
    independent = float(
        np.sum(P * (I[:,None] + I[None,:]) / 2) / np.sum(P)
    )
    if not np.isclose(expected_mean, independent, atol=1e-12, rtol=0):
        raise AssertionError("donor/maternal versus ordered pair I expectation differs")
    q = float(outcross.sum() / ovules)
    if not (0 <= q <= 1 and 0 <= expected_mean <= 1):
        raise AssertionError("invalid native one-generation I expectancy / q")
    parent_mean = float(I.mean())
    return expected_mean-parent_mean, expected_mean, q


def _native_model_gate(d: dict):
    m = d["model"]
    if (d["status"] != "FROZEN_EXPLORATORY_MECHANISM_PILOT_NOT_INDEPENDENT_CONFIRMATION"
        or d["factorial"]["freeze_prefix_updates"] != 30
        or d["factorial"]["future_updates"] != 50
        or m["capacity"] != 48 or m["adult_survival"] != 0.
        or m["mutation_rate"] != 0. or m["seed_immigration"] != 0.
        or m["visitor_immigration"] != 0. or m["assurance_mode"] != "evolving"):
        raise AssertionError("original source assumptions not admissible")


def replay_source_pathwise() -> dict[str,Any]:
    d = admit()  # Verifies full immutable protocol SHA and native operator blob SHAs.
    _native_model_gate(d)
    roster = load_roster()  # Same SHA-locked 24 original ZIP-sourced prefix/terminal states.
    results = []
    for cell in roster:
        baseline, a = cell["baseline"], cell["initial_A"]
        v = visitors(d, baseline)
        prefix_config = config(d,baseline,0.4)
        state = founders(d,cell["founder_seed"],a)
        rng = streams(cell["founder_seed"],cell["demographic_repeat"])
        for year in range(30):
            state,_ = step(state,v,prefix_config,rng,year)
        if fingerprint(state) != cell["prefix_sha"]:
            raise AssertionError("original census30 full diploid fingerprint mismatch")
        before_I=float(state.alleles[:,1,:].mean())
        if (len(np.unique(state.alleles[:,0,:])) != 1
            or len(np.unique(state.alleles[:,2,:])) != 1
            or len(np.unique(state.alleles[:,1,:])) <= 1):
            raise AssertionError("strict original A/M fixed and I polymorphic shock gate failed")
        source_rng = clone(rng)
        arms = {}
        for name, activity in (("control",0.4),("decline",0.04)):
            rr = clone(source_rng)
            cfg = config(d,baseline,activity)
            st = state
            generations = []
            sum_expected = 0.0
            sum_realization = 0.0
            n_below_capacity = 0
            for year in range(30,80):
                led = reproduce(st,v,cfg)
                expected_shift, expected_child_I, q = conditional_parental_I(st,led)
                current = float(st.alleles[:,1,:].mean())
                if len(st.ids) < cfg.capacity:
                    n_below_capacity += 1
                nxt, q_step = step(st,v,cfg,rr,year)
                if not len(nxt.ids):
                    raise AssertionError("original source survival disagrees: empty population")
                if abs(q-q_step)>EPS:
                    raise AssertionError("source reproduction ledger q changed within a single step")
                realized = float(nxt.alleles[:,1,:].mean())
                realized_delta = realized-current
                residual = realized-expected_child_I
                if abs(realized_delta-(expected_shift+residual))>EPS:
                    raise AssertionError("one-step conditional expectation identity broken")
                sum_expected += expected_shift
                sum_realization += residual
                generations.append({
                    "year_from_original_founding":year,
                    "N_before_reproduction":len(st.ids),
                    "N_after_recruitment":len(nxt.ids),
                    "current_I":current,
                    "next_I":realized,
                    "current_I_allele_values":np.unique(st.alleles[:,1,:]).tolist(),
                    "q_pre_selfing":q,
                    "expected_I_shift_from_parentage":expected_shift,
                    "realization_residual":residual,
                    "realized_I_shift":realized_delta,
                })
                st=nxt
            expected_hash = cell["control_sha"] if name=="control" else cell["decline_sha"]
            if fingerprint(st) != expected_hash:
                raise AssertionError(
                    "original t80 source-genotype fingerprint mismatch in "+
                    str((cell["initial_A"],baseline,cell["founder_seed"],
                         cell["demographic_repeat"],name))
                )
            end_I = float(st.alleles[:,1,:].mean())
            if abs((sum_expected+sum_realization)-(end_I-before_I))>EPS:
                raise AssertionError("full 50-step source pathwise accounting failed to telescope")
            if any(len(np.unique(st.alleles[:,x,:])) != 1 for x in (0,2)):
                raise AssertionError("genetically fixed A/M changed under original zero mutation")
            arms[name] = {
                "original_terminal_full_state_sha256":expected_hash,
                "I_start":before_I,
                "I_end":end_I,
                "sum_path_conditional_expected_I":sum_expected,
                "sum_path_realization_residual_I":sum_realization,
                "sum_path_realized_I_change":end_I-before_I,
                "N_below_K_at_beginning_of_steps":n_below_capacity,
                "n_generations_with_segregating_I":sum(
                    len(row["current_I_allele_values"]) > 1 for row in generations),
                "generations":generations,
            }
        delta_I=arms["decline"]["I_end"]-arms["control"]["I_end"]
        delta_expect=(
            arms["decline"]["sum_path_conditional_expected_I"]-
            arms["control"]["sum_path_conditional_expected_I"])
        delta_realization=(
            arms["decline"]["sum_path_realization_residual_I"]-
            arms["control"]["sum_path_realization_residual_I"])
        if abs(delta_I-(delta_expect+delta_realization))>EPS:
            raise AssertionError("paired terminal I contrast not reproduced by source path accounting")
        results.append({
            "initial_A":a,"baseline":baseline,
            "founder_seed":cell["founder_seed"],
            "demographic_repeat":cell["demographic_repeat"],
            "original_prefix_full_state_sha256":cell["prefix_sha"],
            "I_at_shock":before_I,
            "paired_terminal_I_decline_minus_control":delta_I,
            "paired_accumulated_conditional_expectation_difference":delta_expect,
            "paired_accumulated_realization_residual_difference":delta_realization,
            "arms":arms,
        })
    summaries=[]
    for baseline in ("strong_baseline_limitation","weak_baseline_limitation"):
        grp=[row for row in results if row["baseline"]==baseline]
        if len(grp) != (22 if baseline=="strong_baseline_limitation" else 2):
            raise AssertionError("original 24 source cohort not complete")
        values=lambda key:np.asarray([r[key] for r in grp],dtype=float)
        dI=values("paired_terminal_I_decline_minus_control")
        dE=values("paired_accumulated_conditional_expectation_difference")
        dR=values("paired_accumulated_realization_residual_difference")
        if not np.allclose(dE+dR,dI,atol=EPS,rtol=0):
            raise AssertionError("source population-mean I path components do not sum")
        founder=defaultdict(list)
        for row in grp:
            founder[row["founder_seed"]].append(row["paired_terminal_I_decline_minus_control"])
        summaries.append({
            "baseline":baseline,
            "n_original_shock_genomes":len(grp),
            "n_distinct_founders":len(founder),
            "mean_terminal_paired_I":float(dI.mean()),
            "mean_path_conditional_expected_I":float(dE.mean()),
            "mean_path_realization_residual_I":float(dR.mean()),
            "n_terminal_I_negative":int(np.sum(dI<0)),
            "n_terminal_I_zero":int(np.sum(dI==0)),
            "n_terminal_I_positive":int(np.sum(dI>0)),
            "n_path_expected_I_difference_negative":int(np.sum(dE<0)),
            "n_path_expected_I_difference_zero":int(np.sum(dE==0)),
            "n_path_expected_I_difference_positive":int(np.sum(dE>0)),
            "n_path_realization_difference_negative":int(np.sum(dR<0)),
            "n_path_realization_difference_zero":int(np.sum(dR==0)),
            "n_path_realization_difference_positive":int(np.sum(dR>0)),
            "n_founders_negative_terminal_mean":sum(np.mean(v)<0 for v in founder.values()),
            "n_founders_zero_terminal_mean":sum(np.mean(v)==0 for v in founder.values()),
            "n_founders_positive_terminal_mean":sum(np.mean(v)>0 for v in founder.values()),
            "n_reproduced_future_generations":100*len(grp),
            "n_future_states_below_capacity":sum(
                arm["N_below_K_at_beginning_of_steps"] for row in grp
                for arm in row["arms"].values()),
        })
    strong=next(r for r in summaries if r["baseline"]=="strong_baseline_limitation")
    if (strong["n_distinct_founders"] != 11
        or strong["n_terminal_I_negative"] != 12
        or strong["n_terminal_I_zero"] != 10
        or strong["n_terminal_I_positive"] != 0
        or abs(strong["mean_terminal_paired_I"]-(-.08913352272727272))>EPS):
        raise AssertionError("original finite 50-year I outcome mismatch")
    return {
        "status":STATUS,
        "original_actions_run_id":39233450099,
        "original_source_commit":SOURCE_COMMIT,
        "original_zip_sha256":SOURCE_ZIP_SHA256,
        "original_protocol_sha256":ORIGINAL_PROTOCOL_SHA256,
        "source_genomes_exactly_recovered_and_terminal_hashes_matched":24,
        "replayed_original_prefix_updates":720,
        "replayed_original_stored_future_updates":2400,
        "new_independent_biological_futures":0,
        "new_preregistered_tests":0,
        "source_founders":11,
        "source_original_biological_cases":24,
        "summaries":summaries,
        "rows":results,
        "interpretation":"An exact conditional expectation + realized sampling-residual decomposition along the originally realized 50-update paths. Components depend on the realized state sequence and are NOT causal effects or independent selection-versus-drift variance fractions.",
        "claim_rank":"POST_OUTCOME_EXACT_PATHWISE_ACCOUNTING_ONLY_NOT_CAUSAL_SELECTION_DRIFT",
    }


if __name__=="__main__":
    print(json.dumps(replay_source_pathwise(),ensure_ascii=False,sort_keys=True,indent=2))
