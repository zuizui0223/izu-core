"""Finite-K necessary-condition screen, not an SDE/SPDE convergence proof."""
from dataclasses import replace

import numpy as np
import pytest

from scripts.audit_model3_stochastic_scaling_limit import (
    CAPACITIES, clone_existing_founder_pool, scaling_screen,
)
from scripts.model3_island.population import subset
from scripts.run_chapter2_assurance_generality import founders,load_design,DEFAULT_DESIGN


def test_cloned_capacity_preserves_exact_joint_diploid_trait_distribution():
    d=load_design(DEFAULT_DESIGN)
    base=subset(founders(d),np.arange(8,dtype=np.int64))
    mean=base.alleles.mean(axis=(0,2))
    original=np.unique(np.sort(base.alleles,axis=2).reshape(8,6),axis=0)
    for k in CAPACITIES:
        x=clone_existing_founder_pool(base,k)
        assert len(x.ids)==k
        assert len(np.unique(x.ids))==k
        np.testing.assert_allclose(x.alleles.mean(axis=(0,2)),mean,atol=1e-14,rtol=0)
        np.testing.assert_array_equal(
            np.unique(np.sort(x.alleles,axis=2).reshape(k,6),axis=0),
            original,
        )
    with pytest.raises(ValueError,match="multiple"):
        clone_existing_founder_pool(base,9)


def test_source_aware_scaling_audit_keeps_drift_and_noise_separate():
    data=scaling_screen(
        settings=("prior_selfing",),
        environments=("near",),
        sizes=(8,16,32)
    )
    assert data["status"]=="FINITE_K_STOCHASTIC_SCALING_DIAGNOSTIC"
    assert data["all_continuous_time_SDE_limits_proved"] is False
    assert data["n_new_visitor_histories"]==0
    assert data["model3_biology_modified"] is False
    assert data["trait_space_SPDE_validated"] is False
    assert len(data["rows"])==3
    original=np.array(data["rows"][0]["current_trait_mean"])
    for row in data["rows"]:
        K=row["K"]
        assert row["dt_fast"]==pytest.approx(1/K)
        assert 0<row["offspring_occupancy_probability"]<=1
        np.testing.assert_allclose(row["current_trait_mean"],original,
                                   rtol=0,atol=1e-14)
        v=np.asarray(row["sample_mean_noise_variance_diagonal"])
        assert (v>=0).all()
        np.testing.assert_allclose(
            K*v,row["K_times_sample_mean_noise_variance_diagonal"],
            rtol=1e-13,atol=1e-13
        )
        assert row["one_generation_drift_l2"]==pytest.approx(
            np.linalg.norm(row["one_generation_drift"]),rel=1e-13
        )
        assert row["fast_time_rescaled_drift_l2"]==pytest.approx(
            K*row["one_generation_drift_l2"],rel=1e-13
        )


def test_scaling_audit_preserves_independent_finite_K_verdict_by_environment():
    data=scaling_screen(
        settings=("prior_selfing","assurance_cost"),
        environments=("near","far"),
        sizes=(8,32,128),
    )
    assert len(data["rows"])==12
    assert data["visitor_snapshot_index"]==400
    assert data["visitor_assembly_is_fixed_not_outcome_selected"] is True
    for setting in ("prior_selfing","assurance_cost"):
        near=next(x for x in data["rows"]
                  if x["setting"]==setting and x["environment"]=="near")
        far=next(x for x in data["rows"]
                 if x["setting"]==setting and x["environment"]=="far")
        assert near["visitor_community_sha256"]!=far["visitor_community_sha256"]
        assert near["visitor_snapshot_index"]==far["visitor_snapshot_index"]==400
    assert set(data["groups"])=={
        "prior_selfing_near","prior_selfing_far",
        "assurance_cost_near","assurance_cost_far"
    }
    for group in data["groups"].values():
        assert group["K_values"]==[8,32,128]
        assert isinstance(group["fast_time_finite_drift_screen_fails"],bool)
        assert group["result_scope"]=="finite_K_necessary_condition_not_limit_theorem"
    with pytest.raises(ValueError):
        scaling_screen(sizes=(8,8,32))
