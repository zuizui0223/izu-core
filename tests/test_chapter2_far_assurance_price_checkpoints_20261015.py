"""Source identity/Price/null guards; historical ZIP replay belongs to the audit workflow."""
from __future__ import annotations

from dataclasses import replace
import numpy as np
import pytest

from scripts.audit_chapter2_far_assurance_price_checkpoints_20261015 import (
    full_parent_price, protocol,
)
from scripts.model3_island.types import PlantState, VisitorState
from scripts.run_chapter2_assurance_generality import (
    config, load_design, DEFAULT_DESIGN,
)


def original_fixture():
    n = 4
    vals=np.array([.2,.35,.65,.8])
    avals=np.array([.25,.45,.7,.95])
    genes=np.zeros((n,3,2))
    genes[:,0,:]=.5
    genes[:,1,:]=vals[:,None]
    genes[:,2,:]=avals[:,None]
    return PlantState(
        genes, np.arange(n*6,dtype=np.int64).reshape(n,3,2),
        np.zeros((n,3,2),dtype=bool),np.arange(n,dtype=np.int64),
        np.zeros(n,dtype=np.int64),
    )


def visitor(n):
    return VisitorState(
        np.arange(n,dtype=np.int64),
        np.array([.3,.5,.7],dtype=float)[:n],
        np.full(n,.2),np.ones(n),
    )


def test_frozen_protocol_is_exact_source_campaign():
    p,d=protocol()
    assert p["original_nested_demographic_repeat"] == 26111601
    assert p["original_shard_ids_ordered"] == [
        11411031490,11410452132,11411051762,11411155493,
    ]
    assert p["checkpoint_trait_periods"]==[0,200,400,1000]
    assert p["price_assay_periods"] == [200,400]
    assert d["source_reproduction_sha256"] == (
        "885957edb8a165ee8528781ed1d2574c44143c608496b505f9663cbfac2c4081"
    )


@pytest.mark.parametrize("setting", (
    "delayed_control","prior_selfing","pollen_discount","assurance_cost",
))
@pytest.mark.parametrize("n", (0,3))
def test_one_step_full_parent_price_against_original_FPS(setting,n):
    d=load_design(DEFAULT_DESIGN)
    state=original_fixture()
    c=config(d,setting,.01,"evolving")
    result=full_parent_price(state,visitor(n),c)
    assert result["n_adults"]==4
    assert result["n_visitors"]==n
    assert abs(result["expected_next_I_if_occupied"]
               -result["genetic_mean_I"]-result["price_shift_I"]) <1e-12
    if n==0:
        expected=result["zero_visitor"]
        assert abs(expected["expected_next_I_from_source_factorization"]
                   -result["expected_next_I_if_occupied"])<1e-12
        assert expected["A_weight_alignment_effect"]>0


@pytest.mark.parametrize("setting", (
    "delayed_control","prior_selfing","pollen_discount","assurance_cost",
))
def test_zero_visitors_fixed_assurance_always_has_no_A_alignment(setting):
    d=load_design(DEFAULT_DESIGN)
    state=original_fixture()
    c=config(d,setting,.01,"fixed")
    out=full_parent_price(state,visitor(0),c)
    assert abs(out["zero_visitor"]["A_weight_alignment_effect"])<1e-12


def test_cannot_classify_an_extinct_original_checkpoint_as_zero_trait():
    d=load_design(DEFAULT_DESIGN)
    c=config(d,"assurance_cost",.01,"evolving")
    empty=PlantState(np.empty((0,3,2)),
        np.empty((0,3,2),dtype=np.int64),
        np.empty((0,3,2),dtype=bool),
        np.empty(0,dtype=np.int64),np.empty(0,dtype=np.int64))
    with pytest.raises(ValueError,match="occupied"):
        full_parent_price(empty,visitor(0),c)
