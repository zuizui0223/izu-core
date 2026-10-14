"""Exact original Model3 pollen export, visitor routing, maternal Shapley audits."""
import numpy as np
import pytest

from scripts.audit_model3_k32_outcross_factors import (
    FACTORS, REFERENCE_KEY, _shapley,
    decompose_outcross_factors,run_outcross_factors,
)
from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_stochastic_bridge import genotype_counts_to_canonical_state
from scripts.model3_island.reproduction import reproduce


def test_shapley_average_independent_of_three_factor_order():
    v={}
    for bits in range(8):
        a=bool(bits&1);b=bool(bits&2);c=bool(bits&4)
        v[bits]=2.*a+3.*b+5.*c+4.*(a and b)
    result=_shapley(v)
    assert result[FACTORS[0]]==pytest.approx(4.)
    assert result[FACTORS[1]]==pytest.approx(5.)
    assert result[FACTORS[2]]==pytest.approx(5.)
    assert sum(result.values())==pytest.approx(v[7]-v[0])
    with pytest.raises(ValueError):
        _shapley({0:0,7:1})


@pytest.mark.parametrize("budget",[3.,8.])
def test_source_outcross_original_ledger_reconstruction_and_4_terms(budget):
    initial,grid,visitor,cfg=fixed_support_problem(capacity=32,ovule_budget=budget)
    item=decompose_outcross_factors(initial,grid,visitor,cfg,0)
    assert item["status"]=="EXACT_OUTCROSS_FACTORIZATION"
    assert item["source_outcross_fraction"]>0
    assert item["max_exact_reconstruction_error"]<1e-11
    assert set(item["terms_variance"])=={REFERENCE_KEY,*FACTORS}
    assert sum(item["terms_variance"].values())==pytest.approx(
        item["source_within_outcross_variance"],abs=1e-11)
    state=genotype_counts_to_canonical_state(initial,grid,0,32)
    ledger=reproduce(state,visitor,cfg)
    receipt=ledger.delivered.sum(axis=0)
    female=ledger.maternal-ledger.self_viable
    ratio=np.divide(female,receipt,out=np.zeros_like(receipt),where=receipt>0)
    np.testing.assert_allclose(
        ledger.outcross,ledger.delivered*ratio[None,:],
        atol=1e-12,rtol=0)


def test_zero_source_outcross_is_fully_audited_without_invented_mates():
    initial,grid,visitor,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    c=np.zeros_like(initial)
    c[int(np.flatnonzero(initial)[0])]=1
    item=decompose_outcross_factors(c,grid,visitor,cfg,0)
    assert item["status"]=="ZERO_SOURCE_OUTCROSS"
    assert item["source_outcross_fraction"]==0.
    assert all(v==0 for v in item["terms_variance"].values())


@pytest.mark.parametrize("budget",[3.,8.])
def test_old_history_exact_shapley_8_generations_source_firewall(budget):
    r=run_outcross_factors(budget=budget,draws=16,seed=88343)
    assert r["status"]=="EXACT_MODEL3_OUTCROSS_SHAPLEY_LEDGER_VERIFIED"
    c=r["conditions"]
    assert (c["K"],c["mutation_rate"],c["generations"],c["ovule_budget"])==(32,0,8,budget)
    assert c["old_visitor_history"]==26110601
    assert c["independent_visitor_histories"]==1
    assert c["source_biological_reproduction_changed"] is False
    assert c["prospective_confirmatory_histories_used"] is False
    assert c["no_autonomous_comparator_trajectory"] is True
    assert c["shapley_computed_across_three_factors"] is True
    assert len(r["per_generation"])==8
    assert r["unmatched_source_states"]==[]
    for yr in r["per_generation"]:
        assert yr["n_evaluable_source_parent_states"]>0
        assert yr["max_absolute_state_identity_error"]<1e-10
        assert set(yr["shapley_and_reference_components_mean"])==set(r["components"])
        assert sum(yr["shapley_and_reference_components_mean"].values())==pytest.approx(
            yr["mean_source_within_outcross_delta_variance"],abs=1e-10)


def test_guards_inadmissible_other_histories_and_invalid_draw_count():
    with pytest.raises(ValueError):
        run_outcross_factors(budget=4.,draws=16)
    with pytest.raises(ValueError):
        run_outcross_factors(budget=8.,draws=8)
