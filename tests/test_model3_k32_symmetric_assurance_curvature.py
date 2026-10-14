"""Model3 exact matched-background assurance curvature and source safety."""
import numpy as np
import pytest

from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_k32_pathwise_selection_drift import allele_frequency_basis
from scripts.audit_model3_k32_symmetric_assurance_curvature import (
    symmetric_heterozygote_variants, symmetric_response, run_symmetric,
)


def test_same_diploid_heterozygote_perturbed_both_ways_no_other_locus_change():
    first,grid,vis,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    pair=symmetric_heterozygote_variants(first,grid,np.random.default_rng(100))
    assert pair is not None
    low,high=pair
    b=allele_frequency_basis(grid)[:,2]
    h=1/(2*32)
    assert first.sum()==low.sum()==high.sum()==32
    assert low.dtype.kind in "iu" and high.dtype.kind in "iu"
    assert np.min(low)>=0 and np.min(high)>=0
    assert (low-first)@b/32==pytest.approx(-h)
    assert (high-first)@b/32==pytest.approx(h)
    g=grid.genotypes.mean(axis=2)
    np.testing.assert_allclose((low-first)@g,[0.,0.,-.25],atol=1e-12)
    np.testing.assert_allclose((high-first)@g,[0.,0.,.25],atol=1e-12)
    np.testing.assert_array_equal(first,
        fixed_support_problem(capacity=32,ovule_budget=8.)[0])


def test_matched_control_uses_identical_source_parent_and_calibration():
    first,grid,vis,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    result=symmetric_response(first,grid,vis,cfg,0,np.random.default_rng(15))
    assert result["status"]=="SYMMETRIC_HETEROZYGOTE_DIRECTIONAL_RESPONSE"
    assert result["parent_n"]==32
    assert result["source_versus_control_central_slope"]==pytest.approx(
        .5*(result["down_source_minus_control_slope"]+
            result["up_source_minus_control_slope"]))
    assert result["source_symmetric_second_difference"]==pytest.approx(
        (result["source_up_response_slope"]-
         result["source_down_response_slope"])/(2*32),abs=1e-12)
    assert result["control_symmetric_second_difference"]==pytest.approx(
        (result["control_up_response_slope"]-
         result["control_down_response_slope"])/(2*32),abs=1e-12)


def test_fixed_assurance_population_has_no_heterozygote_not_promoted():
    first,grid,vis,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    basis=allele_frequency_basis(grid)[:,2]
    all_high=np.zeros_like(first)
    all_high[int(np.flatnonzero(basis==1)[0])]=32
    assert symmetric_heterozygote_variants(
        all_high,grid,np.random.default_rng(2)) is None
    result=symmetric_response(all_high,grid,vis,cfg,0,
                              np.random.default_rng(1))
    assert result["status"]=="NO_HETEROZYGOTE_FOR_TWO_SIDED_RESPONSE"


@pytest.mark.parametrize("budget",[3.,8.])
def test_source_old_history_symmetric_comparison_never_promotes_biology(budget):
    result=run_symmetric(budget=budget,draws=16,seed=17242)
    c=result["conditions"]
    assert (c["K"],c["mutation_rate"],c["generations"])==(32,0,8)
    assert c["old_visitor_history"]==26110601
    assert c["independent_visitor_histories"]==1
    assert c["original_model3_biology_modified"] is False
    assert c["comparator_deliberately_alters_reproduction"] is True
    assert c["new_confirmatory_cohorts_reused"] is False
    assert c["parent_genotype_identical_in_two_flip_orientations"] is True
    assert set(result["checkpoints"])=={"3","5","7","8"}
    for k,v in result["checkpoints"].items():
        assert 0<=v["n_comparable_heterozygote_states"]<=16
        assert v["n_comparable_heterozygote_states"]<=v["n_occupied"]
        assert v["n_comparable_heterozygote_states"]+sum(
            v["ineligible_states"].values())==v["n_occupied"]
        s=v["same_genotype_bidirectional_summary"]
        assert s["n"]==v["n_comparable_heterozygote_states"]
        if s["n"]:
            assert np.isfinite(s["mean_source_versus_control_central_slope"])
            assert np.isfinite(s["mean_source_minus_control_second_difference"])
        else:
            assert s["mean_source_versus_control_central_slope"] is None


def test_reject_unapproved_budget_sample_scope():
    with pytest.raises(ValueError):
        run_symmetric(budget=4.,draws=16)
    with pytest.raises(ValueError):
        run_symmetric(budget=8.,draws=4)
