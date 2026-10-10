"""Protect source maternal resource/receipt Shapley algebra and negative evidence."""
import json
from dataclasses import replace
from pathlib import Path
import numpy as np
import pytest

from scripts.audit_chapter2_original_evolved_resource_receipt_shapley import (
    source_viable_seed, source_shapley,
)
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.types import PlantState, VisitorState
from scripts.run_chapter2_assurance_generality import config,load_design,DEFAULT_DESIGN

ROOT=Path(__file__).resolve().parents[1]
RECEIPT=ROOT/"data/results/chapter2_original_evolved_resource_receipt_shapley_receipt_20261010.json"


def fixture_state():
    n=8
    a=np.zeros((n,3,2),dtype=float)
    a[:,0,:]=np.linspace(.15,.85,n)[:,None]
    a[:,1,:]=np.linspace(.3,.6,n)[:,None]
    a[:,2,:]=np.linspace(.2,.8,n)[:,None]
    return PlantState(alleles=a,
      allele_origin=np.arange(n*6,dtype=np.int64).reshape(n,3,2),
      mutation_flags=np.zeros((n,3,2),dtype=bool),
      ids=np.arange(n,dtype=np.int64),birth_years=np.zeros(n,dtype=np.int64))


def visitor_state(n=4):
    return VisitorState(ids=np.arange(n,dtype=np.int64),
      optima=np.array([.15,.35,.55,.75])[:n],
      breadths=np.full(n,.18), effectiveness=np.ones(n))


@pytest.mark.parametrize("setting",["delayed_control","prior_selfing",
                                    "pollen_discount","assurance_cost"])
@pytest.mark.parametrize("nvisitors",[0,4])
def test_two_factor_ovule_receipt_partition_is_exact_for_native_source(setting,nvisitors):
    cfg=config(load_design(DEFAULT_DESIGN),setting,.01,"evolving")
    e=fixture_state()
    c=replace(e,alleles=np.stack([
       e.alleles[:,0,:],np.full((8,2),.4),e.alleles[:,2,:]
       ],axis=1))
    v=visitor_state(nvisitors)
    le=reproduce(e,v,cfg)
    lc=reproduce(c,v,cfg)
    parts=source_shapley(le,lc,e.alleles[:,2,:].mean(axis=1),cfg)
    np.testing.assert_allclose(
      parts["group_viable_seed_difference"],
      parts["ovule_resource_effect"]+parts["pollen_receipt_effect"],
      rtol=0,atol=3e-11)
    if nvisitors==0:
        np.testing.assert_allclose(parts["pollen_receipt_effect"],0.,rtol=0,atol=1e-12)
        np.testing.assert_allclose(parts["delivered_pollen_difference"],0.,rtol=0,atol=1e-12)


def test_errors_cannot_create_false_benefit():
    cfg=config(load_design(DEFAULT_DESIGN),"assurance_cost",.01,"evolving")
    with pytest.raises(ValueError):
        source_viable_seed(np.ones(2),np.ones(3),np.ones(2)*.5,cfg)
    with pytest.raises(ValueError):
        source_viable_seed(np.ones(2),np.ones(2),np.ones(2)*1.2,cfg)


def test_archived_original_genome_result_preserves_all_signs_and_denominators():
    r=json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert r["status"]=="POST_OUTCOME_VERIFIED_ORIGINAL_GENOME_MATERNAL_SHAPLEY_NOT_MEDIATION"
    assert r["original_raw_full_json_sha256"]==(
      "6fdd8ed45af9f7b9c65b513cb20fa1f3ba224519695ec37940421a7a6d60ae5e")
    assert r["n_history_setting_blocks"]==256
    assert r["n_original_visitors_histories"]==64
    assert r["n_of_8_original_demographic_repeats_used"]==1
    assert r["independent_histories_new"]==0
    assert len(r["rows"])==4
    assert [x["setting"] for x in r["rows"]]==[
       "delayed_control","prior_selfing","pollen_discount","assurance_cost"]
    for x in r["rows"]:
        np.testing.assert_allclose(x["resource"]+x["receipt"],x["seed"],atol=2e-11,rtol=0)
        assert x["delivered"]<0
        assert 0<x["nRescuing"]<64
        assert x["negReceipt"]+x["posReceipt"]+x["zeroReceipt"]==64
    assert sum(x["seed"]>0 for x in r["rows"])==3
    # Downward total pollen delivery does not mechanically imply a
    # negative recipient-specific pollen contribution.
    assert next(x for x in r["rows"] if x["setting"]=="prior_selfing")["receipt"]>0
    assert "not causal mediation" not in r["causal_limit"].lower() or "not" in r["causal_limit"].lower()
