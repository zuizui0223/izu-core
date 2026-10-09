"""Experimental genetic-locus reassignment firewall and source consistency."""
import numpy as np
import pytest

from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_stochastic_bridge import genotype_counts_to_canonical_state
from scripts.audit_model3_k32_locus_reassignment import (
    VARIANTS, founder_diplotype_distribution,reassign_one_locus,
    evaluate_original_reproduction,run_locus_reassignment,
)
from scripts.audit_model3_k32_state_visitor_cross import exact_original_crossed_direction


def test_founder_diplotype_distribution_and_biallelic_marginal():
    first,grid,v,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    for locus in range(3):
        types,freq=founder_diplotype_distribution(first,grid,locus)
        assert len(types)==3
        assert types.shape==(3,2)
        assert np.isclose(freq.sum(),1.)
        assert np.sum(types.mean(axis=1)*freq)==pytest.approx(.5,abs=1e-12)
    with pytest.raises(ValueError):
        founder_diplotype_distribution(first,grid,3)


@pytest.mark.parametrize("locus",[0,1,2])
def test_shuffle_breaks_joint_alignment_but_preserves_every_marginal(locus):
    first,grid,v,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    state=genotype_counts_to_canonical_state(first,grid,7,32)
    types,prob=founder_diplotype_distribution(first,grid,locus)
    edited=reassign_one_locus(state,locus,"shuffle",types,prob,
                              np.random.default_rng(337))
    assert np.array_equal(state.ids,edited.ids)
    assert len(state.ids)==len(edited.ids)
    np.testing.assert_allclose(state.alleles.mean(axis=(0,2)),
                               edited.alleles.mean(axis=(0,2)),atol=1e-12)
    for k in range(3):
        before=np.unique(state.alleles[:,k,:],axis=0,return_counts=True)
        after=np.unique(edited.alleles[:,k,:],axis=0,return_counts=True)
        np.testing.assert_array_equal(before[0],after[0])
        np.testing.assert_array_equal(before[1],after[1])


def test_reset_founder_distribution_is_quota_matched_not_genetic_source_step():
    first,grid,v,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    state=genotype_counts_to_canonical_state(first,grid,7,32)
    types,p=founder_diplotype_distribution(first,grid,2)
    edited=reassign_one_locus(state,2,"reset",types,p,
                              np.random.default_rng(26))
    np.testing.assert_allclose(
        edited.alleles.mean(axis=(0,2)),state.alleles.mean(axis=(0,2)),
        atol=1e-12)
    one=genotype_counts_to_canonical_state(first,grid,1,32)
    # Artificially make all source plants homozygous high at assurance.
    homo=one.alleles.copy()
    homo[:,2,:]=.75
    from dataclasses import replace
    fixed=replace(one,alleles=homo)
    edited2=reassign_one_locus(fixed,2,"reset",types,p,
                               np.random.default_rng(13))
    assert np.mean(edited2.alleles[:,2,:]==.75)==pytest.approx(.5)
    assert np.mean(fixed.alleles[:,2,:]==.75)==pytest.approx(1.)
    np.testing.assert_array_equal(fixed.alleles[:,:2,:],
                                  edited2.alleles[:,:2,:])
    with pytest.raises(ValueError):
        reassign_one_locus(one,2,"change_biology",types,p,np.random.default_rng(2))


def test_unchanged_original_reproduction_matches_prior_source_checker():
    first,grid,vis,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    s=genotype_counts_to_canonical_state(first,grid,7,32)
    observed=evaluate_original_reproduction(s,vis,cfg,grid)
    ref=exact_original_crossed_direction(first,grid,vis,cfg,7)
    np.testing.assert_allclose(observed,ref["expected_allele_direction"],
                               atol=1e-12,rtol=0)


@pytest.mark.parametrize("budget",[3.,8.])
def test_late_parent_assurance_shuffle_and_reset_strict_provenance(budget):
    r=run_locus_reassignment(budget=budget,draws=16,permutations=2,
                              seed=420261017)
    assert r["status"]=="K32_ORIGINAL_REPRODUCTION_LATE_SOURCE_LOCUS_REASSIGNMENT_EVALUATED"
    c=r["conditions"]
    assert (c["K"],c["mutation_rate"],c["generations"],c["budget"])==(32,0,8,budget)
    assert c["old_visitor_history"]==26110601
    assert c["independent_visitor_histories"]==1
    assert c["n_permutation_reassignments_per_locus_variant"]==2
    assert c["source_original_biological_code_modified"] is False
    assert c["counterfactual_alters_parental_locus_genotypes"] is True
    assert c["founder_diplotype_reset_can_reintroduce_lost_alleles"] is True
    assert c["shuffle_preserves_all_three_marginal_diplotype_distributions"] is True
    assert c["future_confirmatory_history_used"] is False
    assert set(r["locus_variants"])==set(VARIANTS)
    for name,v in r["locus_variants"].items():
        marg=v["parent_high_allele_marginal_change"]["mean"]
        assert len(marg)==3
        if name.startswith("shuffle_"):
            np.testing.assert_allclose(marg,np.zeros(3),atol=1e-12,rtol=0)
        locus={"matching":0,"investment":1,"assurance":2}[name.split("_")[1]]
        assert abs(sum(abs(marg[j]) for j in range(3) if j!=locus))<1e-12
        for snap in ("early_visitor_counterfactual_minus_original",
                     "late_visitor_counterfactual_minus_original"):
            assert len(v[snap]["mean"])==3
            assert v[snap]["n_source_parent_states"]==c["n_late_source_survivor_states"]
    assert set(r["founder_reset_after_shuffle_sequential_contrasts"])=={
        "matching","investment","assurance"
    }


def test_forbid_outside_old_history_budgets():
    with pytest.raises(ValueError):
        run_locus_reassignment(budget=4.,draws=16)
    with pytest.raises(ValueError):
        run_locus_reassignment(budget=8.,draws=8)
    with pytest.raises(ValueError):
        run_locus_reassignment(budget=8.,draws=16,permutations=0)
