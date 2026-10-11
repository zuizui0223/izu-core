"""Original-source vs autonomous donor/routing/maternal factor intervention gates."""
import numpy as np
import pytest

from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_stochastic_bridge import (
    genotype_counts_to_canonical_state, genotype_count_markov_step,
    offspring_genotype_distribution,
)
from scripts.model3_island.reproduction import reproduce
from scripts.run_model3_k32_outcross_ablation import (
    SOURCE, ARMS, reweighted_outcross, step_with_intervention, run_ablation,
)


@pytest.mark.parametrize("budget",[3.,8.])
def test_one_factor_changes_only_original_outcross_edges_and_preserves_seed_intensity(budget):
    c,g,v,cfg=fixed_support_problem(capacity=32,ovule_budget=budget)
    state=genotype_counts_to_canonical_state(c,g,0,32)
    ledger=reproduce(state,v,cfg)
    selfmass=float(ledger.self_viable.sum())
    outmass=float(ledger.outcross.sum())
    assert outmass>0 and selfmass>0
    original=ledger.outcross.copy()
    assert np.count_nonzero(original)>0
    for arm in ARMS:
        mat=reweighted_outcross(ledger,arm)
        assert mat.shape==original.shape
        assert np.all(mat>=0)
        assert np.all(np.diag(mat)==0)
        assert not np.any((original==0)&(mat>1e-12))
        assert mat.sum()==pytest.approx(outmass,abs=1e-10)
        assert (selfmass+mat.sum())==pytest.approx(selfmass+outmass,abs=1e-10)
    np.testing.assert_allclose(reweighted_outcross(ledger,SOURCE),original,atol=1e-12)


def test_original_arm_exactly_replays_canonical_finite_source_transition():
    counts,g,visitor,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    seed=5817
    observed=step_with_intervention(
        counts,g,visitor,cfg,np.random.default_rng(seed),0,SOURCE)
    expected=genotype_count_markov_step(
        counts,g,visitor,cfg,np.random.default_rng(seed),year=0)
    np.testing.assert_array_equal(observed,expected)


def test_at_least_one_counterfactual_changes_offspring_genotype_law():
    c,g,v,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    state=genotype_counts_to_canonical_state(c,g,0,32)
    ledger=reproduce(state,v,cfg)
    orig_pair=ledger.outcross.copy()
    orig_pair[np.diag_indices(len(state.ids))]+=ledger.self_viable
    q_source=offspring_genotype_distribution(state,orig_pair/orig_pair.sum(),g)
    deltas=[]
    for arm in ARMS[1:]:
        mat=reweighted_outcross(ledger,arm)
        mat[np.diag_indices(len(state.ids))]+=ledger.self_viable
        q=offspring_genotype_distribution(state,mat/mat.sum(),g)
        deltas.append(np.linalg.norm(q-q_source,ord=1))
    assert max(deltas)>1e-12


def test_absorbing_extinction_and_single_parent_no_outcross():
    c,g,v,cfg=fixed_support_problem(capacity=32,ovule_budget=3.)
    zero=np.zeros_like(c)
    for arm in ARMS:
        np.testing.assert_array_equal(
            step_with_intervention(zero,g,v,cfg,np.random.default_rng(8),1,arm),
            zero)
    singleton=zero.copy()
    singleton[int(np.flatnonzero(c)[0])]=1
    state=genotype_counts_to_canonical_state(singleton,g,0,32)
    ledger=reproduce(state,v,cfg)
    for arm in ARMS:
        np.testing.assert_allclose(
            reweighted_outcross(ledger,arm),ledger.outcross,atol=1e-12)


@pytest.mark.parametrize("budget",[3.,8.])
def test_eight_generations_counterfactual_scope_conservation_and_paired_endpoints(budget):
    r=run_ablation(budget=budget,draws=16,seed=778829)
    c=r["conditions"]
    assert r["status"]=="K32_SOURCE_VS_ONE_FACTOR_OUTCROSS_ABLATIONS_COMPLETED"
    assert (c["K"],c["mutation_rate"],c["generations"])==(32,0,8)
    assert c["old_visitor_history"]==26110601
    assert c["independent_visitor_histories"]==1
    assert c["source_biological_code_edited"] is False
    assert c["counterfactual_intentionally_modifies_reproduction"] is True
    assert c["source_conditional_total_viable_seed_intensity_preserved"] is True
    assert c["source_conditional_selfed_seed_mass_and_fraction_preserved"] is True
    assert c["original_mating_edge_support_preserved"] is True
    assert c["confirmatory_visitor_cohorts_used"] is False
    assert set(r["per_generation"])=={str(i) for i in range(1,9)}
    assert list(r["arms"])==list(ARMS)
    assert set(r["year8_paired_contrasts"])==set(ARMS[1:])
    for year in r["per_generation"].values():
        assert set(year)==set(ARMS)
        for arm in ARMS:
            x=year[arm]
            assert x["n_survivors"]+x["n_extinct"]==16
            assert 0<=x["mean_census_all"]<=32
            assert 0<=x["mean_lost_allele_types_all"]<=6
            assert 0<=x["mean_genotype_richness_all"]<=27
            if x["n_survivors"]:
                assert 0<=x["mean_assurance_high_allele_survivors"]<=1
                assert 0<=x["mean_assurance_heterozygote_fraction_survivors"]<=1
    for v in r["year8_paired_contrasts"].values():
        assert v["difference_direction"]=="counterfactual_minus_original"
        assert v["n_pairwise_survivors"]<=16


def test_counterfactual_rejects_other_budgets():
    with pytest.raises(ValueError):
        run_ablation(budget=7.,draws=16)
    with pytest.raises(ValueError):
        run_ablation(budget=8.,draws=8)
    c,g,v,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    state=genotype_counts_to_canonical_state(c,g,0,32)
    with pytest.raises(ValueError):
        reweighted_outcross(reproduce(state,v,cfg),"random_ablation")
