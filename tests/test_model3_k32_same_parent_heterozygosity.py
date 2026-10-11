"""Same-parent/mean exact conditional Mendelian dosage variance gates."""
import numpy as np
import pytest

from scripts.audit_model3_k32_same_parent_heterozygosity import (
    all_pair_neutral_mendelian_law, offspring_assurance_moments,
    conditional_inverse_positive_census,
    same_parent_exact_contrast,
    run_same_parent,
)
from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_stochastic_bridge import capped_poisson_distribution


def test_biallelic_diploid_heterozygosity_identity_analytic():
    b=np.array([0.,.5,1.])
    q=np.array([.2,.3,.5])
    mu,h,var=offspring_assurance_moments(q,b)
    assert mu==pytest.approx(.65)
    assert h==pytest.approx(.3)
    assert var==pytest.approx(.65*.35-.25*.3,abs=1e-14)
    with pytest.raises(ValueError):
        offspring_assurance_moments(q,np.array([0.,.25,1.]))
    with pytest.raises(ValueError):
        offspring_assurance_moments(np.array([.2,.2,.5]),b)



def test_full_parent_pair_neutral_law_is_martingale_and_contains_source_support():
    from scripts.audit_model3_k32_pathwise_selection_drift import allele_frequency_basis
    from scripts.run_model3_three_arm_k32_old_history import canonical_conditional_kernel
    first,grid,vis,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    basis=allele_frequency_basis(grid)
    # Source can use self-mating; neutral support must include both
    # self and outcross inherited child combinations.
    _,qs=canonical_conditional_kernel(first,grid,vis,cfg,0)
    q=all_pair_neutral_mendelian_law(first,grid)
    assert q.shape==(27,)
    assert np.all(q>=0)
    assert q.sum()==pytest.approx(1.)
    assert np.all(q[qs>1e-12]>0)
    np.testing.assert_allclose(q@basis,first@basis/first.sum(),atol=1e-12)
    np.testing.assert_array_equal(
        all_pair_neutral_mendelian_law(np.zeros_like(first),grid),
        np.zeros_like(first,dtype=float))
    with pytest.raises(ValueError):
        all_pair_neutral_mendelian_law(np.array([2,-1]),grid)


def test_capped_poisson_conditional_frequency_variance_factor():
    pn=capped_poisson_distribution(5.,32)
    v=conditional_inverse_positive_census(5.,32)
    assert v==pytest.approx(
        sum(pn[n]/n for n in range(1,33))/(1-pn[0]),
        abs=1e-14)
    assert 1/32<=v<=1


def test_same_parent_counterfactual_matches_mu_and_census_exactly():
    first,grid,vis,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    result=same_parent_exact_contrast(first,grid,vis,cfg,0)
    assert result["status"]=="MATCHED"
    assert result["same_parent_census"]==32
    assert result["source_assurance_allele_mean"]==pytest.approx(
        result["matched_comparator_assurance_allele_mean"],abs=1e-7)
    assert result["source_minus_comparator_next_frequency_variance"]==pytest.approx(
        result["heterozygosity_explained_next_frequency_variance_contrast"],abs=1e-12)
    assert 0<=result["source_offspring_heterozygote_probability"]<=1
    assert 0<=result["comparator_offspring_heterozygote_probability"]<=1
    assert same_parent_exact_contrast(
        np.zeros_like(first),grid,vis,cfg,0)["status"]=="EXTINCT_PARENT"



def test_exactly_fixed_high_assurance_does_not_exceed_numeric_unit_boundary():
    from scripts.audit_model3_k32_pathwise_selection_drift import allele_frequency_basis
    first,grid,vis,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    assurance=allele_frequency_basis(grid)[:,2]
    genotype=int(np.flatnonzero(assurance==1.)[0])
    fixed=np.zeros_like(first)
    fixed[genotype]=32
    output=same_parent_exact_contrast(fixed,grid,vis,cfg,0)
    assert output["status"]=="MATCHED"
    assert output["source_assurance_allele_mean"]==pytest.approx(1.)
    assert output["matched_comparator_assurance_allele_mean"]==pytest.approx(1.)
    assert output["source_minus_comparator_next_frequency_variance"]==pytest.approx(0.,abs=1e-12)


@pytest.mark.parametrize("budget",[3.,8.])
def test_eight_generation_fixed_history_analytic_conditional_gate(budget):
    r=run_same_parent(budget=budget,draws=16,seed=42000017)
    c=r["conditions"]
    assert r["status"]=="SOURCE_MATCHED_MOMENT_DIAGNOSTIC_COMPLETED"
    assert c["K"]==32 and c["mutation_rate"]==0
    assert c["generations"]==8 and c["old_visitor_history"]==26110601
    assert c["independent_visitor_histories"]==1
    assert c["source_biology_edited"] is False
    assert c["confirmatory_cohorts_accessed"] is False
    assert c["no_outcome_fitted_yearly_trajectory"] is True
    assert c["comparison_parent_state_identical_between_operators"] is True
    assert c["neutral_comparator_parent_pairs_include_self"] is True
    assert c["matched_comparator_source_genotype_support_preserved"] is True
    assert c["comparison_offspring_mean_identical_between_operators"] is True
    assert c["comparison_offspring_census_law_identical_between_operators"] is True
    assert r["support_failures"]==[]
    assert len(r["per_generation"])==8
    for step in r["per_generation"]:
        assert step["n_source_parent_states"]>0
        assert step["exact_identity_max_absolute_error"]<1e-12
        assert step["statuses_not_matched"].get("MATCHED_MEAN_UNATTAINABLE",0)==0
        assert step["source_lower_next_frequency_variance_fraction"]<=1
        assert step["source_higher_next_frequency_variance_fraction"]<=1


def test_forbid_new_ecological_conditions():
    with pytest.raises(ValueError):
        run_same_parent(budget=4.,draws=16)
    with pytest.raises(ValueError):
        run_same_parent(budget=8.,draws=8)
