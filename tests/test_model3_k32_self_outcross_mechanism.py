"""Exact source ledger: selfing, within-self and pollen-outcross strata."""
import numpy as np
import pytest

from scripts.audit_model3_k32_self_outcross_mechanism import (
    conditional_pair_child_law, matched_tilt_pair_mixture,
    exact_ledger_decomposition,run_ledger,
)
from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_stochastic_bridge import genotype_counts_to_canonical_state
from scripts.audit_model3_k32_pathwise_selection_drift import allele_frequency_basis
from scripts.model3_island.reproduction import reproduce


def test_ledger_self_and_outcross_reconstruct_exact_source_genotype_kernel():
    first,grid,v,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    state=genotype_counts_to_canonical_state(first,grid,0,32)
    ledger=reproduce(state,v,cfg)
    sp=np.diag(ledger.self_viable)
    op=ledger.outcross
    s=sp.sum()/(sp.sum()+op.sum())
    qs=conditional_pair_child_law(state,sp,grid)
    qo=conditional_pair_child_law(state,op,grid)
    q=conditional_pair_child_law(state,sp+op,grid)
    np.testing.assert_allclose(q,s*qs+(1-s)*qo,atol=1e-12,rtol=0)
    assert np.diag(op).sum()==0
    assert 0<s<1


def test_tilted_all_pairs_self_outcross_heterozygosity_exact():
    b=np.array([0.,.5,1.])
    qs=np.array([.4,.5,.1])
    qo=np.array([.1,.2,.7])
    s0=.25
    result=matched_tilt_pair_mixture(qs,qo,s0,b,.65)
    assert result["status"]=="MATCHED"
    assert result["q"]@b==pytest.approx(.65,abs=1e-8)
    h=result["q"][1]
    assert h==pytest.approx(
        result["self_fraction"]*result["self_heterozygote"]+
        (1-result["self_fraction"])*result["outcross_heterozygote"],
        abs=1e-12)
    at_one=matched_tilt_pair_mixture(qs,qo,s0,b,1.)
    assert at_one["status"]=="MATCHED"
    assert at_one["q"]@b==pytest.approx(1.)
    assert at_one["self_heterozygote"]==0


def test_single_source_parent_self_only_no_invented_outcross():
    first,grid,v,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    isolated=np.zeros_like(first)
    isolated[np.flatnonzero(first)[0]]=1
    r=exact_ledger_decomposition(isolated,grid,v,cfg,0)
    assert r["status"]=="EXACT_LEDGER_STRATIFIED"
    assert r["source_selfing_fraction_of_viable_seed_intensity"]==pytest.approx(1.)
    assert r["mean_matched_null_selfing_fraction"]==pytest.approx(1.)
    assert r["exact_three_term_next_frequency_variance"]["self_vs_outcross_fraction_contrast"]==pytest.approx(0.)


def test_full_source_state_three_components_sum_to_direct_matched_mean_variance():
    first,grid,v,cfg=fixed_support_problem(capacity=32,ovule_budget=3.)
    r=exact_ledger_decomposition(first,grid,v,cfg,0)
    assert r["status"]=="EXACT_LEDGER_STRATIFIED"
    for label in ("exact_three_term_heterozygosity","exact_three_term_next_frequency_variance"):
        assert len(r[label])==3
    assert sum(r["exact_three_term_next_frequency_variance"].values())==pytest.approx(
        r["source_minus_null_next_frequency_variance"],abs=1e-12)
    assert r["max_absolute_identity_error"]<1e-12
    assert 0<r["mean_matched_null_selfing_fraction"]<1


@pytest.mark.parametrize("budget",[3.,8.])
def test_old_history_eight_generations_and_provenance(budget):
    r=run_ledger(budget=budget,draws=16,seed=261010)
    assert r["status"]=="EXACT_SELF_OUTCROSS_DECOMPOSITION_VERIFIED"
    c=r["conditions"]
    assert (c["K"],c["mutation_rate"],c["generations"],c["ovule_budget"])==(32,0,8,budget)
    assert c["independent_visitor_histories"]==1
    assert c["old_visitor_history"]==26110601
    assert c["canonical_model3_biology_modified"] is False
    assert c["confirmatory_history_used"] is False
    assert c["reference_is_autonomous_population_simulation"] is False
    assert len(r["per_generation"])==8
    for row in r["per_generation"]:
        assert row["n_source_parent_states"]>0
        assert row["max_absolute_analytic_identity_error"]<1e-10
        assert sum(row["terms"].values())==pytest.approx(row["mean_source_minus_null_frequency_variance"],abs=1e-12)


def test_rejects_other_budgets_and_invalid_draws():
    with pytest.raises(ValueError):
        run_ledger(budget=4.,draws=16)
    with pytest.raises(ValueError):
        run_ledger(budget=8.,draws=8)
