"""Exact original Model3 genotype replay and first-generation expected I sorting.

No independent future reproduction, new history simulation, confirmatory p-value,
or causal attribution to selection-versus-drift over 50 generations.
"""
from __future__ import annotations

from types import SimpleNamespace
import json
from pathlib import Path

import numpy as np
import pytest

from scripts.model3_island.types import PlantState
from scripts.audit_chapter2_r2_shock_genome_expected_I_20261023 import (
    load_roster, expected_genetic_I, replay, STATUS, ROSTER_BLOB_SHA,
)


def synthetic_state() -> PlantState:
    n=48
    alleles=np.full((n,3,2),0.5)
    alleles[0,1,:]=0.25
    alleles[1,1,:]=0.75
    return PlantState(
        alleles=alleles,
        allele_origin=np.arange(n*6,dtype=np.int64).reshape(n,3,2),
        mutation_flags=np.zeros((n,3,2),dtype=bool),
        ids=np.arange(n,dtype=np.int64),
        birth_years=np.zeros(n,dtype=np.int64),
    )


def test_24_original_shock_source_roster_immutable():
    x=load_roster()
    assert len(x)==24
    assert ROSTER_BLOB_SHA=="6b04ee9a5cd6c2342e397c6c69539688474b391f"
    assert len({r["founder_seed"] for r in x})==11
    assert sum(r["baseline_code"]=="S" for r in x)==22
    assert sum(r["baseline_code"]=="W" for r in x)==2
    assert all(len(r["prefix_sha"])==len(r["control_sha"])==len(r["decline_sha"])==64 for r in x)
    assert all(810101<=r["founder_seed"]<=810112 for r in x)


def test_genetic_parentage_expected_I_uses_both_outcross_and_self():
    state=synthetic_state()
    n=48
    weights=np.zeros((n,n))
    weights[0,1]=10.0
    viable=np.zeros(n)
    ledger=SimpleNamespace(outcross=weights,self_viable=viable,ovules=np.ones(n)*2)
    gradient,q,pred=expected_genetic_I(state,ledger)
    assert pred==pytest.approx(0.5)
    assert q==pytest.approx(10/(n*2))
    assert gradient==pytest.approx(0.0)
    ledger.self_viable[0]=5.0
    gradient,q,pred=expected_genetic_I(state,ledger)
    assert pred==pytest.approx((10*.5+5*.25)/15,abs=1e-14)
    assert q==pytest.approx(10/(n*2))
    assert gradient==pytest.approx(-1/12,abs=1e-14)


def test_no_observed_allele_signal_if_all_I_monorphic():
    state=synthetic_state()
    uniform=state.alleles.copy()
    uniform[:,1,:]=0.5
    state=PlantState(
        alleles=uniform,allele_origin=state.allele_origin,
        mutation_flags=state.mutation_flags,ids=state.ids,
        birth_years=state.birth_years,
    )
    weights=np.zeros((48,48))
    weights[0,1]=10
    ledger=SimpleNamespace(outcross=weights,self_viable=np.zeros(48),ovules=np.ones(48))
    differential,_,mean=expected_genetic_I(state,ledger)
    assert differential==pytest.approx(0,abs=1e-14)
    assert mean==pytest.approx(.5,abs=1e-14)


def test_source_recovery_is_exact_but_no_new_futures():
    report=replay()
    assert report["status"]==STATUS
    assert report["original_run_id"]==39233450099
    assert report["reproduced_original_prefix_steps"]==24*30
    assert report["new_independent_population_future_steps"]==0
    assert report["new_experiments_or_statistical_tests"]==0
    assert report["original_source_genomes_exactly_recovered"]==24
    assert report["n_source_founders"]==11
    assert report["evidence_rank"]=="POST_OUTCOME_SOURCE_EXACT_STATIC_EXPECTATION_NOT_INDEPENDENT_CONFIRMATION"
    assert len(report["rows"])==24
    assert len(report["summaries"])==2
    strong=next(x for x in report["summaries"] if x["baseline"]=="strong_baseline_limitation")
    assert strong["n_original_source_genomes"]==22
    assert strong["n_distinct_founders"]==11
    assert strong["mean_original_q_control"]==pytest.approx(.13920994216147997,abs=1e-12)
    assert strong["mean_original_q_decline"]==pytest.approx(.01689527391924731,abs=1e-12)
    for r in report["rows"]:
        assert len(r["original_source_prefix_sha"])==64
        assert 0<=r["I_mean_at_shock"]<=1
        assert len(r["I_allele_values_at_shock"])>1
        assert r["native_one_generation"]["decline"]["source_outcross_fraction_q"]<r[
            "native_one_generation"]["control"]["source_outcross_fraction_q"]

    root = Path(__file__).resolve().parents[1]
    receipt=json.loads((root/"docs/audits/CHAPTER2_R2_CENSUS30_EXPECTED_I_SOURCE_RECEIPT_20261023.json").read_text())
    source=json.loads((root/"docs/audits/CHAPTER2_R2_FROZEN_AM_I_SORTING_20261023.json").read_text())
    assert receipt["status"]=="PASS_ORIGINAL_24_CENSUS30_GENOMES_STATIC_EXPECTED_I_SOURCE_READBACK"
    assert receipt["verified_original_GitHub_replay_workflow_run_id"]==39929844856
    assert receipt["verified_original_replay_actions_artifact_id"]==12491490791
    assert receipt["verified_full_replay_JSON_sha256"]=="c53ae7220d5eb4bde3cef84bb73f2f890692edae29ec8f013636f7bdd6500c06"
    assert receipt["reconstructed_full_prefix_genomes_verified_by_SHA256"]==24
    assert receipt["new_independent_future_model_updates"]==0
    assert receipt["new_statistical_tests"]==0
    for z in report["summaries"]:
        s=receipt["one_generation_native_parentage_expected_I"][z["baseline"]]
        rows=[r for r in report["rows"] if r["baseline"]==z["baseline"]]
        assert len(rows)==s["n"]==z["n_original_source_genomes"]
        control=np.mean([r["native_one_generation"]["control"]["expected_one_generation_I_shift"] for r in rows])
        decline=np.mean([r["native_one_generation"]["decline"]["expected_one_generation_I_shift"] for r in rows])
        diff=np.mean([r["decline_minus_control_expected_I_sorting"] for r in rows])
        assert control==pytest.approx(s["mean_expected_shift_control"],abs=1e-12)
        assert decline==pytest.approx(s["mean_expected_shift_decline"],abs=1e-12)
        assert diff==pytest.approx(s["mean_decline_minus_control_expected_shift"],abs=1e-12)
        assert z["n_static_expected_treatment_negative"]==s["n_expected_treatment_difference_negative"]
        assert z["n_static_expected_treatment_positive"]==s["n_expected_treatment_difference_positive"]
    # The known finite-horizon outcome is deliberately NOT overwritten with
    # the new one-generation expectation: 10/22 had exactly zero I contrast.
    assert source["totals"]["strong_I_treatment_negative"]==12
    assert source["totals"]["strong_I_treatment_zero"]==10
    assert source["totals"]["strong_I_treatment_positive"]==0
    assert report["summaries"][0]["n_static_expected_treatment_negative"]==22
