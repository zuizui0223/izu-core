"""Synthetic test only: two disjoint old/new cohorts, no biological simulation."""
import ast
from pathlib import Path

import numpy as np
import pytest

from scripts.chapter2_order_two_cohort_signature import (
    SOURCES, bootstrap_two_cohorts, paired_effects, summarize,
)
from scripts.chapter2_order_budget_window_followup import load_followup
from scripts.chapter2_order_payoff_recruitment_posthoc import METRICS


def synthetic():
    _,d=load_followup()
    shape=(64,4,2,2,2,7,2,2)
    return d,{key:np.zeros(shape,dtype=float) for key in METRICS}


def test_new_vs_old_64_history_bootstrap_is_not_branch_pseudoreplication():
    a=np.ones(64)*0.02
    b=np.ones(64)*0.04
    v=bootstrap_two_cohorts(a,b,draws=300)
    assert v["independent_minus_original"]==pytest.approx(0.02)
    assert v["independent_minus_original_bootstrap95"]==pytest.approx([0.02,0.02])
    assert v["both_cohorts_equal_weight_mean"]==pytest.approx(0.03)
    assert v["direction_reproduced"]
    with pytest.raises(ValueError):
        bootstrap_two_cohorts(np.ones(57344),np.ones(64),draws=100)


def test_a_first_absolute_advantage_can_be_shared_and_did_zero():
    d,x=synthetic()
    x["occupied"][:,:,:,0,:,:,:,:]=1
    x["cumulative_selfed_recruits"][:,:,:,0,:,:,:,:]=3
    x["cumulative_outcross_recruits"][:,:,:,1,:,:,:,:]=5
    arr=paired_effects(d,x)
    r=arr["eight_founders_capacity8"]
    assert np.allclose(r["occupied"]["near"],1)
    assert np.allclose(r["occupied"]["far"],1)
    assert np.allclose(r["occupied"]["DID"],0)
    assert np.allclose(r["cumulative_selfed_recruits"]["common"],3)
    assert np.allclose(r["cumulative_outcross_recruits"]["common"],-5)


def test_summarize_does_not_claim_confirmation():
    d,a=synthetic()
    b={k:z.copy() for k,z in a.items()}
    first=paired_effects(d,a)
    second=paired_effects(d,b)
    x=summarize(first,second)
    assert x["source_groups_audited"]==[3072,2048]
    assert x["future_branches_audited"]==[86016,57344]
    assert "POST_OUTCOME" in x["status"]
    assert x["original_synchronous_arm_verified_not_used_in_AB_comparison"]


def test_no_new_simulation_paths():
    path=Path("scripts/chapter2_order_two_cohort_signature.py")
    tree=ast.parse(path.read_text())
    calls={node.func.id for node in ast.walk(tree)
           if isinstance(node,ast.Call) and isinstance(node.func,ast.Name)}
    assert not {"simulate_prehistory","one_future","persist_one","advance"} & calls
    assert SOURCES["original"]["last"] < SOURCES["independent"]["first"]
