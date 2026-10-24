"""Regression and negative controls for original-source R2 expectation/residual accounting.

This test replays only the 24 pre-existing, original-archive-sha-verified
24x30 prefix + 24x2x50 original future updates. It does not draw any NEW
biological histories, derive drift fractions, or promote preregistration.
"""
from __future__ import annotations

from types import SimpleNamespace
import json

import numpy as np
import pytest

from scripts.model3_island.types import PlantState
from scripts.audit_chapter2_r2_original_pathwise_I_accounting_20261024 import (
    STATUS, conditional_parental_I, replay_source_pathwise
)
from scripts.audit_chapter2_r2_shock_genome_expected_I_20261023 import load_roster


def fixture_state() -> PlantState:
    n=3
    a=np.full((n,3,2),.5,dtype=float)
    a[:,1,:]=np.asarray([.25,.5,.75])[:,None]
    return PlantState(
        alleles=a,
        allele_origin=np.arange(n*6,dtype=np.int64).reshape(n,3,2),
        mutation_flags=np.zeros((n,3,2),dtype=bool),
        ids=np.arange(n,dtype=np.int64),
        birth_years=np.zeros(n,dtype=np.int64),
    )


def test_exact_one_year_expected_mendelian_parentage_includes_self_and_both_outcross_parents():
    state=fixture_state()
    outcross=np.zeros((3,3),dtype=float)
    outcross[0,2]=8
    selfed=np.array([2,0,0.])
    ledger=SimpleNamespace(outcross=outcross,self_viable=selfed,ovules=np.full(3,5.))
    sel,e,q=conditional_parental_I(state,ledger)
    assert e==pytest.approx((8*.5+2*.25)/10,abs=1e-14)
    assert sel==pytest.approx(-.05,abs=1e-14)
    assert q==pytest.approx(8/15,abs=1e-14)
    selfed[:]=0
    sel,e,q=conditional_parental_I(state,ledger)
    assert e==pytest.approx(.5,abs=1e-14)
    assert sel==pytest.approx(0,abs=1e-14)


def test_invalid_source_ledger_is_rejected():
    state=fixture_state()
    x=SimpleNamespace(outcross=np.zeros((3,3)),self_viable=np.zeros(3),
                      ovules=np.ones(3))
    with pytest.raises(AssertionError,match="no viable expected"):
        conditional_parental_I(state,x)
    x.outcross[0,1]=-1
    with pytest.raises(AssertionError,match="invalid native"):
        conditional_parental_I(state,x)
    x.outcross=np.ones((2,2))
    with pytest.raises(AssertionError,match="invalid native"):
        conditional_parental_I(state,x)


def test_original_exact_terminal_source_replay_and_pathwise_identity():
    d=replay_source_pathwise()
    assert d["status"]==STATUS
    # Explicitly validate that the actual result artifact is JSON portable;
    # NumPy int64 founder sign counters previously broke the source gate.
    assert json.loads(json.dumps(d,allow_nan=False))["status"]==STATUS
    assert d["original_actions_run_id"]==39233450099
    assert d["source_genomes_exactly_recovered_and_terminal_hashes_matched"]==24
    assert d["source_original_biological_cases"]==24
    assert d["replayed_original_prefix_updates"]==720
    assert d["replayed_original_stored_future_updates"]==2400
    assert d["new_independent_biological_futures"]==0
    assert d["new_preregistered_tests"]==0
    assert d["source_founders"]==11
    assert "NOT_CAUSAL_SELECTION_DRIFT" in d["claim_rank"]
    assert len(d["rows"])==len(load_roster())==24
    assert len(d["summaries"])==2
    strong=next(z for z in d["summaries"] if z["baseline"]=="strong_baseline_limitation")
    assert strong["n_original_shock_genomes"]==22
    assert strong["n_distinct_founders"]==11
    assert strong["n_terminal_I_negative"]==12
    assert strong["n_terminal_I_zero"]==10
    assert strong["n_terminal_I_positive"]==0
    assert strong["mean_terminal_paired_I"]==pytest.approx(-.08913352272727272,abs=1e-12)
    assert (strong["mean_path_conditional_expected_I"]+
            strong["mean_path_realization_residual_I"])==pytest.approx(
                strong["mean_terminal_paired_I"],abs=1e-10
            )
    for r in d["rows"]:
        assert len(r["original_prefix_full_state_sha256"])==64
        assert r["paired_terminal_I_decline_minus_control"]==pytest.approx(
            r["paired_accumulated_conditional_expectation_difference"]+
            r["paired_accumulated_realization_residual_difference"],abs=1e-10)
        assert set(r["arms"])=={"control","decline"}
        for arm in r["arms"].values():
            assert len(arm["original_terminal_full_state_sha256"])==64
            assert len(arm["generations"])==50
            assert arm["sum_path_realized_I_change"]==pytest.approx(
                arm["sum_path_conditional_expected_I"]+
                arm["sum_path_realization_residual_I"],abs=1e-10)
            for y in arm["generations"]:
                assert y["realized_I_shift"]==pytest.approx(
                    y["expected_I_shift_from_parentage"]+y["realization_residual"],abs=1e-10)
                assert 0<=y["current_I"]<=1
                assert 0<=y["next_I"]<=1
                assert 0<=y["q_pre_selfing"]<=1
                assert 1<=y["N_before_reproduction"]<=48
                assert 1<=y["N_after_recruitment"]<=48


def test_no_false_inference_as_causal_drift_share():
    r=replay_source_pathwise()
    assert "NOT causal" in r["interpretation"] or "NOT causal" in r["interpretation"].upper()
    assert "depend on the realized state sequence" in r["interpretation"]
    assert r["new_independent_biological_futures"]==0
    assert r["new_preregistered_tests"]==0
