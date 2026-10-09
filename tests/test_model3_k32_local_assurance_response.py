"""Locked old-history assurance one-copy perturbation source-operator checks."""
import numpy as np
import pytest

from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_k32_pathwise_selection_drift import allele_frequency_basis
from scripts.audit_model3_k32_local_assurance_response import (
    flip_one_assurance_copy, paired_local_slope, run_local,
)


def test_one_copy_flip_preserves_census_and_other_loci():
    initial,grid,vis,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    b=allele_frequency_basis(grid)[:,2]
    for direction,sign in (("high_to_low",-1),("low_to_high",1)):
        old=initial.copy()
        new=flip_one_assurance_copy(initial,grid,direction,
                                     np.random.default_rng(100))
        assert new is not None
        assert new.sum()==old.sum()==32
        assert np.min(new)>=0
        delta=(new-old)@grid.genotypes.mean(axis=2)
        np.testing.assert_allclose(delta,[0.,0.,sign*.25],atol=1e-12,rtol=0)
        assert ((new-old)@b/32)==pytest.approx(sign/64)
        np.testing.assert_array_equal(initial,old)


def test_matched_baseline_means_and_exact_discrete_slope():
    initial,grid,vis,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    changed=flip_one_assurance_copy(
        initial,grid,"high_to_low",np.random.default_rng(9))
    o=paired_local_slope(initial,changed,grid,vis,cfg,0)
    assert o["status"]=="BASELINE_MEAN_MATCHED_LOCAL_DERIVATIVE"
    assert o["baseline_source_next_allele_frequency"]==pytest.approx(
        o["baseline_null_next_allele_frequency"],abs=1e-8)
    assert o["delta_parent_assurance_frequency"]==pytest.approx(-1/64)
    assert o["source_minus_null_response_slope"]==pytest.approx(
        o["source_response_slope"]-o["baseline_mean_matched_tilt_slope"],
        abs=1e-12)
    assert o["source_reproductive_intensity_original"]>0
    assert o["source_reproductive_intensity_changed"]>0


def test_fully_fixed_assurance_baseline_is_excluded_not_faked():
    original,grid,vis,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    high=allele_frequency_basis(grid)[:,2]
    chosen=int(np.flatnonzero(high==1)[0])
    all_high=np.zeros_like(original)
    all_high[chosen]=32
    changed=flip_one_assurance_copy(
        all_high,grid,"high_to_low",np.random.default_rng(22))
    assert changed is not None
    r=paired_local_slope(all_high,changed,grid,vis,cfg,0)
    assert r["status"]=="BASELINE_FIXED_TILT_UNIDENTIFIABLE"
    assert r["p"]==1.
    assert flip_one_assurance_copy(
        all_high,grid,"low_to_high",np.random.default_rng(22)) is None
    with pytest.raises(ValueError):
        flip_one_assurance_copy(all_high,grid,"not_a_direction",
                                np.random.default_rng(22))


@pytest.mark.parametrize("budget",[3.,8.])
def test_same_old_history_and_two_direction_local_audits(budget):
    r=run_local(budget=budget,draws=16,seed=24391)
    c=r["conditions"]
    assert (c["K"],c["mutation_rate"],c["generations"])==(32,0,8)
    assert c["old_visitor_history"]==26110601
    assert c["independent_visitor_histories"]==1
    assert c["confirmatory_history_reused"] is False
    assert c["canonical_model3_biology_modified"] is False
    assert c["counterfactual_alters_reproductive_operator"] is True
    assert c["boundary_states_excluded_from_matched_tilt"] is True
    assert set(r["checkpoints"])=={"3","5","7","8"}
    for row in r["checkpoints"].values():
        assert row["n_occupied_parent_states"]<=16
        assert row["n_assurance_frequency_boundary_states_excluded"]<=16
        for name in ("assurance_high_to_low","assurance_low_to_high"):
            summary=row[name]
            assert 0<=summary["n"]<=16
            if summary["n"]:
                assert np.isfinite(summary["mean_source_slope"])
                assert np.isfinite(summary["mean_control_slope"])
                assert summary["mean_source_minus_control"]==pytest.approx(
                    summary["mean_source_slope"]-summary["mean_control_slope"],
                    abs=1e-10)


def test_rejects_outside_fixed_design():
    with pytest.raises(ValueError):
        run_local(budget=4.,draws=16)
    with pytest.raises(ValueError):
        run_local(budget=8.,draws=5)
