"""Pathwise mean/martingale decomposition from original Model3 source law."""
import numpy as np
import pytest

from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_k32_pathwise_selection_drift import (
    allele_frequency_basis, one_step_decomposition, run_pathwise,
)
from scripts.audit_model3_stochastic_bridge import (
    genotype_count_markov_step, offspring_genotype_distribution,
    genotype_counts_to_canonical_state,
)
from scripts.model3_island.reproduction import reproduce


def test_fixed_source_alleles_and_exact_trait_conversion():
    init,grid,vis,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    b=allele_frequency_basis(grid)
    assert b.shape==(27,3)
    np.testing.assert_allclose(init@b/init.sum(),[.5,.5,.5],atol=.3,rtol=0)
    np.testing.assert_allclose(grid.genotypes.mean(axis=2),.25+.5*b,atol=1e-12)


def test_single_step_conditional_finite_identity_and_covariance():
    init,grid,vis,cfg=fixed_support_problem(capacity=32,ovule_budget=3.)
    state=genotype_counts_to_canonical_state(init,grid,0,32)
    ledger=reproduce(state,vis,cfg)
    parents=ledger.outcross.copy()
    parents[np.diag_indices(len(state.ids))]+=ledger.self_viable
    q=offspring_genotype_distribution(state,parents/parents.sum(),grid)
    children=genotype_count_markov_step(init,grid,vis,cfg,np.random.default_rng(99),year=0)
    assert children.sum()>0
    d,s,e,c=one_step_decomposition(init,children,q,allele_frequency_basis(grid))
    np.testing.assert_allclose(d,s+e,atol=1e-12)
    assert c.shape==(3,3)
    np.testing.assert_allclose(c,c.T,atol=1e-13)
    assert np.linalg.eigvalsh(c).min()>=-1e-12


def test_absorbing_extinction_never_fabricates_allele_frequency():
    init,grid,vis,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    with pytest.raises(ValueError):
        one_step_decomposition(init,np.zeros_like(init),
                               np.ones(27)/27,allele_frequency_basis(grid))


@pytest.mark.parametrize("budget",[3.,8.])
def test_eight_generation_nested_history_exact_telescoping(budget):
    r=run_pathwise(budget=budget,draws=32,seed=261009420)
    c=r["conditions"]
    assert c["K"]==32 and c["generations"]==8 and c["mutation_rate"]==0
    assert c["old_visitor_history"]==26110601
    assert c["independent_visitor_histories"]==1
    assert c["new_confirmatory_histories_used"] is False
    assert c["canonical_model3_biology_modified"] is False
    assert len(r["per_generation"])==8
    assert r["n_surviving_through_eight"]+r["n_extinct_by_eight"]==32
    x=r["surviving_trajectories"]
    assert x["pathwise_max_absolute_identity_error"]<1e-11
    a=x["cumulative_source_reproductive_filter_shift"]["mean"]
    b=x["cumulative_finite_offspring_sampling_shift"]["mean"]
    total=x["observed_eight_generation_frequency_shift"]["mean"]
    np.testing.assert_allclose(np.asarray(a)+b,total,atol=1e-12,rtol=0)
    v=x["cumulative_component_variances"]
    np.testing.assert_allclose(
        np.asarray(v["between_survivor_variance_filter_shift"])+
        np.asarray(v["between_survivor_variance_sampling_shift"])+
        np.asarray(v["two_times_covariance"]),
        v["total_allele_frequency_change_variance"],
        atol=1e-12,rtol=0)
    for step in r["per_generation"]:
        assert step["single_step_source_identity_max_error"] is None or step["single_step_source_identity_max_error"]<1e-11
        assert step["new_extinctions"]>=0
        if step["n_occupied_end"]:
            assert len(step["expected_reproductive_filter_shift"]["mean"])==3
            m=np.asarray(step["average_exact_sampling_covariance_conditional_N"])
            assert m.shape==(3,3)
            assert np.linalg.eigvalsh(m).min()>=-1e-12


def test_source_guards_reject_unplanned_scope():
    with pytest.raises(ValueError):
        run_pathwise(budget=4.,draws=32)
    with pytest.raises(ValueError):
        run_pathwise(budget=8.,draws=5)
