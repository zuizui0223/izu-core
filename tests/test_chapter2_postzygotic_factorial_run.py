"""Plan and algebra-only checks: no fresh biological history outcomes."""
from pathlib import Path

import numpy as np
import pytest

from scripts.chapter2_postzygotic_factorial_common import (
    frozen,hashes,verify_registry,
)
from scripts.chapter2_postzygotic_factorial_readout import adjudicate,paired,METRICS
from scripts.plan_chapter2_order_expression_identification import prehistories


def empty_grid():
    d,_=frozen()
    return d,{k:np.zeros((64,4,2,2,2,7,2,2,4)) for k in METRICS}


def test_frozen_design_units_and_exact_source_reuse():
    d,tasks=frozen()
    assert len(tasks)==2048
    assert {t.visitor_history for t in tasks}==set(range(38110901,38110965))
    assert {t.expression_order for t in tasks}=={
        "assurance_first","investment_first"}
    assert len(set(tasks))==2048
    assert len(hashes()["design"])==64


def test_primary_self_viability_sensitivity_is_paired_by_history():
    d,grid=empty_grid()
    # Assignment A gains occupancy only in untreated baseline.
    grid["occupied"][:,:,:,0,:,:,:,0,0]=0.80
    grid["occupied"][:,:,:,1,:,:,:,0,0]=0.70
    grid["occupied"][:,:,:,0,:,:,:,0,1]=0.78
    grid["occupied"][:,:,:,1,:,:,:,0,1]=0.70
    grid["occupied"][:,:,:,0,:,:,:,0,2]=0.79
    grid["occupied"][:,:,:,1,:,:,:,0,2]=0.70
    grid["occupied"][:,:,:,0,:,:,:,0,3]=0.77
    grid["occupied"][:,:,:,1,:,:,:,0,3]=0.70
    x=adjudicate(d,grid)
    assert x["n_new_perturbed_futures"]==172032
    p=x["primary"]
    assert p["mean"]==pytest.approx(0.02)
    assert p["bootstrap95"]==pytest.approx([0.02,0.02])
    assert p["decision"]=="nonzero_controlled_self_viability_sensitivity"


def test_noncrossing_zero_factorial_is_equivalent():
    d,grid=empty_grid()
    ans=adjudicate(d,grid)
    assert ans["primary"]["decision"]==(
        "controlled_self_viability_sensitivity_practically_equivalent"
    )


def test_single_future_or_one_shard_is_not_independent_history_sample():
    draws=np.zeros((9999,64),dtype=int)
    with pytest.raises(ValueError):
        paired(np.ones(229376),draws)
    with pytest.raises(ValueError):
        paired(np.ones(32),draws)


def test_audit_requires_actual_old_artifact_registries():
    d,tasks=frozen()
    with pytest.raises(FileNotFoundError):
        verify_registry(Path("/missing/pre"),Path("/missing/futures"),0,tasks,d)
    with pytest.raises(ValueError):
        verify_registry(Path("/missing/pre"),Path("/missing/futures"),64,tasks,d)


def test_new_runner_only_reuses_archived_t400_states():
    p=Path("scripts/chapter2_postzygotic_factorial_run.py").read_text()
    assert "simulate_prehistory(" not in p
    assert "persist_prehistory(" not in p
    assert "explicit launch" in p
    assert "old_state_and_future" in p
