"""Source-safe exact heterozygote perturbation at fixed assurance copy count."""
from dataclasses import replace

import numpy as np
import pytest

from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_stochastic_bridge import genotype_counts_to_canonical_state
from scripts.audit_model3_k32_fixed_frequency_heterozygosity import (
    LOW,HIGH,assurance_diplotype_multiset,
    controlled_assurance_pairs,run_fixed_frequency,
)


def source():
    c,g,v,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    state=genotype_counts_to_canonical_state(c,g,0,32)
    return state


def test_original_founder_both_perturbation_directions_conserve_exact_copy_counts():
    state=source()
    original,pairs,genetic_classes=None,None,None
    pairs,dosage,classes=assurance_diplotype_multiset(state)
    assert classes.tolist()==[8,16,8]
    seed=np.random.default_rng(417).permutation(len(state.ids))
    sham=controlled_assurance_pairs(state,"sham",seed)
    up=controlled_assurance_pairs(state,"heterozygosity_up",seed)
    down=controlled_assurance_pairs(state,"heterozygosity_down",seed)
    assert sham is not None and up is not None and down is not None
    for candidate,expected_change in [(sham,0),(up,2),(down,-2)]:
        assert len(candidate.ids)==len(state.ids)
        np.testing.assert_array_equal(candidate.alleles[:,:2,:],state.alleles[:,:2,:])
        assert np.count_nonzero(candidate.alleles[:,2,:]==HIGH)==np.count_nonzero(
            state.alleles[:,2,:]==HIGH)
        assert np.mean(candidate.alleles==HIGH,axis=(0,2))==pytest.approx(
            np.mean(state.alleles==HIGH,axis=(0,2)))
        assert np.count_nonzero(candidate.alleles[:,2,0]!=candidate.alleles[:,2,1])==classes[1]+expected_change
        assert sum(np.any(candidate.alleles[:,2,:]!=sham.alleles[:,2,:],axis=1))==abs(expected_change)
    np.testing.assert_array_equal(
        controlled_assurance_pairs(state,"sham",seed).alleles,sham.alleles)


def test_near_fixation_infeasibility_does_not_resurrect_lost_allele():
    state=source()
    original=state.alleles.copy()
    original[:,2,:]=HIGH
    fixed=replace(state,alleles=original)
    order=np.arange(len(state.ids))
    assert controlled_assurance_pairs(fixed,"heterozygosity_up",order) is None
    assert controlled_assurance_pairs(fixed,"heterozygosity_down",order) is None
    np.testing.assert_allclose(
        controlled_assurance_pairs(fixed,"sham",order).alleles,fixed.alleles)
    with pytest.raises(ValueError):
        controlled_assurance_pairs(fixed,"invalid",order)
    with pytest.raises(ValueError):
        controlled_assurance_pairs(fixed,"sham",np.ones(len(state.ids),int))


@pytest.mark.parametrize("budget",[3.,8.])
def test_8year_source_locus_sensitivity_with_3_parent_years_2_visitor_years(budget):
    r=run_fixed_frequency(budget=budget,draws=16,permutations=2,seed=420261017)
    assert r["status"]=="MODEL3_FIXED_ASSURANCE_ALLELE_COPIES_HETEROZYGOSITY_PERTURBATION_VERIFIED"
    c=r["conditions"]
    assert (c["K"],c["generations"],c["mutation_rate"],c["budget"])==(32,8,0,budget)
    assert c["old_visitor_history"]==26110601
    assert c["independent_ecological_visitor_histories"]==1
    assert c["source_paths_alive_before_eighth_reproduction"]<=16
    assert c["assurance_high_allele_copies_conserved_exactly"] is True
    assert c["single_assurance_diploid_locus_changed_only"] is True
    assert c["complete_source_biological_reproduction_unchanged"] is True
    assert c["no_future_confirmatory_histories_used"] is True
    assert c["parent_state_years"]==[1,4,8]
    assert c["visitor_snapshot_years"]==[1,8]
    for year in r["cell_by_source_parent_year"].values():
        assert year["total_original_shared_source_parents"]==c["source_paths_alive_before_eighth_reproduction"]
        for op,entry in year["operators"].items():
            assert 0<=entry["n_eligible_source_parent_paths"]<=c["source_paths_alive_before_eighth_reproduction"]
            assert entry["parent_assurance_high_allele_frequency_difference"]==0
            assert entry["eligible_source_paths_same_for_two_visitor_conditions"] is True
            if entry["n_eligible_source_parent_paths"]>0:
                sign=1 if op=="heterozygosity_up" else -1
                assert sign*entry["expected_parent_heterozygote_frequency_shift"]["mean"][0]>0
                for visitor_year in ("1","8"):
                    assert len(entry["counterfactual_minus_same_permutation_sham"][visitor_year]["mean"])==3
        assert 0<=year["bidirectional_common_feasibility"]["n_source_parent_paths_feasible_both_directions"]<=c["source_paths_alive_before_eighth_reproduction"]


def test_reject_unapproved_demographic_inputs():
    with pytest.raises(ValueError):
        run_fixed_frequency(budget=4.,draws=16)
    with pytest.raises(ValueError):
        run_fixed_frequency(budget=8.,draws=8)
    with pytest.raises(ValueError):
        run_fixed_frequency(budget=8.,draws=16,permutations=0)
