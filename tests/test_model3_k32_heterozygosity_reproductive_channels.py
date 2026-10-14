"""Original biological ledger channel accounting for fixed-allele HET edits."""
import numpy as np
import pytest

from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_stochastic_bridge import genotype_counts_to_canonical_state
from scripts.audit_model3_k32_fixed_frequency_heterozygosity import (
    controlled_assurance_pairs, assurance_diplotype_multiset,
)
from scripts.audit_model3_k32_parental_marginal_direction import (
    exact_parent_marginal_contributions,
)
from scripts.audit_model3_k32_heterozygosity_reproductive_channels import (
    CHANNELS, RATE_KEYS, canonical_reproductive_channel_vector, run_channels,
)
from scripts.model3_island.reproduction import reproduce


@pytest.mark.parametrize("budget",[3.,8.])
def test_exact_source_channels_and_recruitment_for_same_diploid_parent(budget):
    first,grid,visitor,cfg=fixed_support_problem(capacity=32,ovule_budget=budget)
    state=genotype_counts_to_canonical_state(first,grid,0,32)
    direction,parts,rates=canonical_reproductive_channel_vector(
        state,visitor,cfg,grid)
    assert direction.shape==(3,)
    assert parts.shape==(3,3)
    assert rates.shape==(6,)
    np.testing.assert_allclose(parts.sum(axis=0),direction,atol=1e-12,rtol=0)
    assert rates[0]>0 and rates[1]>0
    assert rates[2]==pytest.approx(rates[0]+rates[1],abs=1e-12)
    assert rates[3]==pytest.approx(rates[0]/rates[2],abs=1e-12)
    assert 0<=rates[4]<=32
    assert 0<=rates[5]<=1
    ledger=reproduce(state,visitor,cfg)
    prior=exact_parent_marginal_contributions(
        state,ledger,ledger.outcross,grid,check_child_genotype_law=True)
    np.testing.assert_allclose(direction,prior["expected_allele_direction"],
                               atol=1e-12,rtol=0)
    for i,key in enumerate(CHANNELS):
        np.testing.assert_allclose(parts[i],prior[key],atol=1e-12,rtol=0)


def test_assurance_edits_keep_current_copies_but_can_change_source_recruitment():
    first,grid,visitor,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    source=genotype_counts_to_canonical_state(first,grid,0,32)
    _,_,classes=assurance_diplotype_multiset(source)
    assert classes[1]>=2 and classes[0]>=1 and classes[2]>=1
    order=np.random.default_rng(719).permutation(32)
    sham=controlled_assurance_pairs(source,"sham",order)
    a=controlled_assurance_pairs(source,"heterozygosity_up",order)
    b=controlled_assurance_pairs(source,"heterozygosity_down",order)
    for candidate in (a,b):
        assert candidate is not None
        np.testing.assert_array_equal(candidate.alleles[:,:2,:],source.alleles[:,:2,:])
        np.testing.assert_allclose(
            np.mean(candidate.alleles==.75,axis=(0,2)),
            np.mean(sham.alleles==.75,axis=(0,2)),atol=1e-12,rtol=0)
        ed,parts,rate=canonical_reproductive_channel_vector(
            candidate,visitor,cfg,grid)
        sd,sp,sr=canonical_reproductive_channel_vector(
            sham,visitor,cfg,grid)
        np.testing.assert_allclose(ed-sd,(parts-sp).sum(axis=0),
                                   atol=1e-12,rtol=0)
        assert rate[2]>0 and sr[2]>0
        assert np.isfinite(rate-sr).all()


@pytest.mark.parametrize("budget",[3.,8.])
def test_canonical_old_history_frozen_3_parent_by_2_visitor_source_channels(budget):
    r=run_channels(budget=budget,draws=16,permutations=2,seed=420261017)
    assert r["status"]=="K32_SOURCE_EXACT_ASSURANCE_HET_EDIT_CHANNEL_AND_DEMOGRAPHY_VERIFIED"
    c=r["conditions"]
    assert (c["K"],c["mutation_rate"],c["generations"],c["budget"])==(32,0,8,budget)
    assert c["old_visitor_history"]==26110601
    assert c["n_independent_ecological_histories"]==1
    assert c["source_reproductive_biology_modified"] is False
    assert c["original_assurance_allele_copy_count_preserved_exactly"] is True
    assert c["original_parental_census_and_other_two_loci_unchanged"] is True
    assert c["prospective_confirmatory_histories_used"] is False
    assert c["parent_start_years"]==[1,4,8]
    assert c["visitor_snapshot_years"]==[1,8]
    assert set(r["source_parent_years"])=={"1","4","8"}
    assert list(r["channels"])==list(CHANNELS)
    assert list(r["demographic_rate_metrics"])==list(RATE_KEYS)
    for row in r["source_parent_years"].values():
        n=row["shared_original_source_parent_count"]
        assert n==c["n_shared_parent_year8_survivors"]
        for op in ("heterozygosity_up","heterozygosity_down"):
            eligible=row["source_edit_eligibility"][op]["eligible_original_source_parent_paths"]
            assert eligible+row["source_edit_eligibility"][op]["ineligible_original_source_parent_paths"]==n
            for year in ("1","8"):
                effect=row["edit_minus_same_sham"][op][year]
                result=effect["expected_allele_direction_difference"]
                assert result["n_eligible_original_source_parent_paths"]==eligible
                if eligible:
                    terms=sum(
                        (np.asarray(effect["channel_differences"][key]["mean"])
                         for key in CHANNELS),np.zeros(3))
                    np.testing.assert_allclose(
                        terms,result["mean"],atol=1e-12,rtol=0)
                    total=effect["viable_seed_mass_recruitment_differences"]
                    assert (total["self_viable_seed_mass"]["mean"][0]+
                            total["outcross_viable_seed_mass"]["mean"][0])==pytest.approx(
                        total["total_viable_seed_mass"]["mean"][0],abs=1e-12)
                    assert effect["max_exact_mendelian_reconstruction_error"]<1e-12


def test_rejects_off_design_cases():
    with pytest.raises(ValueError):
        run_channels(budget=7.,draws=16)
    with pytest.raises(ValueError):
        run_channels(budget=8.,draws=8)
    with pytest.raises(ValueError):
        run_channels(budget=8.,draws=16,permutations=0)
