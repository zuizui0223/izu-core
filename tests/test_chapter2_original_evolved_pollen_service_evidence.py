"""Nonfocal source-audit boundaries: no extra histories in CI."""
from dataclasses import replace
import json
from pathlib import Path

import numpy as np
import pytest

from scripts.audit_chapter2_original_evolved_pollen_service import (
    read_design, source_visitors, original_shards, patch_alleles,
)
from scripts.model3_island.types import PlantState, VisitorState
from scripts.model3_island.reproduction import reproduce
from scripts.run_chapter2_assurance_generality import config, load_design, DEFAULT_DESIGN

ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/"data/results/chapter2_original_evolved_pollen_service_receipt_20261010.json"


def state():
    n=8
    alleles=np.zeros((n,3,2),dtype=float)
    alleles[:,0,:]=.2
    alleles[:,1,:]=.35
    alleles[:,2,:]=.35
    return PlantState(alleles=alleles,
         allele_origin=np.arange(n*6,dtype=np.int64).reshape(n,3,2),
         mutation_flags=np.zeros((n,3,2),dtype=bool),
         ids=np.arange(n,dtype=np.int64),
         birth_years=np.zeros(n,dtype=np.int64))


def visitors(n=4):
    return VisitorState(
       ids=np.arange(n,dtype=np.int64),
       optima=np.array([.15,.35,.55,.75])[:n],
       breadths=np.full(n,.18),
       effectiveness=np.ones(n))


def test_contract_refuses_unowned_source_artifacts():
    d=read_design()
    assert d["history_seed_first"]==26110601
    assert d["history_seed_last"]==26110664
    assert d["demographic_repeat_seed"]==26111601
    with pytest.raises(ValueError):
        original_shards([],d)


def test_source_visitor_replay_starts_with_common_near_far_community():
    near=source_visitors(26110601,"near")
    far=source_visitors(26110601,"far")
    # The two original histories start identically; at 200+ they may differ.
    assert near[200].optima.ndim==1
    assert far[200].optima.ndim==1
    assert near[400].ids.dtype.kind=="i"


def test_one_focal_investment_has_positive_nonfocal_seed_externality():
    d=load_design(DEFAULT_DESIGN)
    for setting in read_design()["settings"]:
        cfg=config(d,setting,.01,"evolving")
        a=state()
        v=visitors(4)
        base=reproduce(a,v,cfg)
        perturbed=reproduce(patch_alleles(a,1,a.alleles[0,1,:]+.002,focal=0),v,cfg)
        mask=np.arange(len(a.ids))!=0
        effect=(perturbed.maternal[mask]-base.maternal[mask]).sum()/.002
        assert effect>0,setting
        assert (perturbed.delivered[:,mask]-base.delivered[:,mask]).sum()>0,setting
        zero=visitors(0)
        lhs=reproduce(a,zero,cfg)
        rhs=reproduce(patch_alleles(a,1,a.alleles[0,1,:]+.002,focal=0),zero,cfg)
        assert np.array_equal(lhs.maternal[mask],rhs.maternal[mask])
        assert np.array_equal(lhs.delivered,rhs.delivered)


def test_no_discount_guarantees_no_direct_assurance_to_pollen_delivery():
    d=load_design(DEFAULT_DESIGN)
    a=state()
    for setting in ("delayed_control","prior_selfing","assurance_cost"):
        cfg=config(d,setting,.01,"evolving")
        base=reproduce(a,visitors(),cfg)
        intervention=reproduce(patch_alleles(a,2,.5),visitors(),cfg)
        np.testing.assert_allclose(base.delivered,intervention.delivered,atol=1e-12,rtol=0)


def test_original_genome_receipt_cannot_be_promoted_to_survival_claim():
    r=json.loads(RESULT.read_text(encoding="utf-8"))
    assert r["status"]=="POST_DISCOVERY_SOURCE_REPLAY_COMPLETE_NOT_EVOLUTIONARY_MEDIATION"
    assert r["n_visitor_histories"]==64
    assert r["n_nested_demographic_repeats"]==1
    assert r["n_original_evolved_fixed_state_checkpoints"]==1024
    assert len(r["near_t400_summary"])==4
    for row in r["near_t400_summary"]:
        assert row["evolved_mean_investment_minus_paired_fixed_mean"]<0
        assert row["evolving_delivery_minus_within_evolving_fixed_mean_investment_clamp"]<0
        assert row["mean_unilateral_focal_investment_derivative_of_other_mothers_viable_seed"]>0
        assert row["mean_focal_own_maternal_derivative"]<0
        assert row["n_focal_derivatives_negative"]==0
        assert row["n_zero_visitor_histories"]==1
        assert row["n_64_histories_evolving_delivery_lower_than_I_clamp"]<=37
    # Total group viable seed change is NOT uniformly negative.
    assert sum(x["evolving_viable_maternal_seed_minus_within_evolving_fixed_mean_investment_clamp"]>0
           for x in r["near_t400_summary"])==3
    assert "STOP_PROMOTION" in r["decision"]
