"""Native original-operator technical QA for synthetic source genotypes only."""
import numpy as np
import pytest

from scripts.audit_chapter2_independent_synthetic_source_pools_20261014 import (
    POOL_COUNT, SOURCE_M, SOURCE_I, OVERLAPS, FOUNDER_SIZES,
    input_only_qa, source_state, assign_hidden_heterozygotes, subset,
)


def test_synthetic_source_genotype_inputs_are_distinct_and_model3_typed():
    hashes=[]
    for p in range(POOL_COUNT):
        old=source_state(p)
        assert old.alleles.shape==(48,3,2)
        assert old.allele_origin.shape==(48,3,2)
        assert np.array_equal(old.ids,np.arange(48))
        assert not np.any(old.mutation_flags)
        assert np.all(old.birth_years==0)
        assert np.all(old.alleles[:,:,0]==old.alleles[:,:,1])
        assert np.all(old.alleles[:,2,:]==0.5)
        assert set(np.unique(old.alleles[:,0,:])).issubset(set(SOURCE_M))
        assert set(np.unique(old.alleles[:,1,:])).issubset(set(SOURCE_I))
        hashes.append(old.alleles.tobytes())
    assert len(set(hashes))==POOL_COUNT


def test_stable_synthetic_pool_assignment_and_phenotype_matched_carriers():
    for p in (0,1,7,15):
        original=source_state(p)
        A=None
        chosen={}
        for m in OVERLAPS:
            edited,a,i=assign_hidden_heterozygotes(original,p,m)
            assert len(a)==len(i)==12
            assert len(a&i)==m
            if A is None: A=a
            else: assert A==a
            assert np.array_equal(edited.alleles.mean(axis=2), original.alleles.mean(axis=2))
            assert np.array_equal(edited.alleles[:,0],original.alleles[:,0])
            assert np.array_equal(edited.allele_origin[:,0],original.allele_origin[:,0])
            assert np.all(edited.allele_origin[:,1:] > original.allele_origin[:,1:])
            for n in FOUNDER_SIZES:
                old=subset(original,p,n)
                new=subset(edited,p,n)
                assert np.array_equal(old.ids,new.ids)
                assert np.array_equal(old.alleles.mean(axis=2),new.alleles.mean(axis=2))
                if n in chosen: assert set(old.ids)==chosen[n]
                else: chosen[n]=set(old.ids)


def test_whole_768_t0_static_source_input_grid_not_new_evolution():
    result=input_only_qa()
    assert result["status"]=="SYNTHETIC_INDEPENDENT_SOURCE_INPUT_ONLY_NOT_APPROVED"
    assert result["n_source_genotype_inputs"]==16
    assert result["n_technical_initial_conditions"]==768
    assert result["native_t0_return_parity_checks"]==768
    assert result["n_realized_births_or_biological_future_updates"]==0
    assert result["n_20_census_response_order_events"]==0
    assert len(result["rows"])==768
    assert all(r["expected_single_offspring_A_variance"]>=0 for r in result["rows"])
    assert all(r["expected_single_offspring_I_variance"]>=0 for r in result["rows"])
    assert all(r["expected_single_offspring_A_variance"]>0 or
               r["A_carriers"]==0 for r in result["rows"])


@pytest.mark.parametrize("invalid",[-1,16,1.5,True])
def test_out_of_domain_synthetic_source_pool_cannot_be_loaded(invalid):
    with pytest.raises(ValueError,match="source pool"):
        source_state(invalid)


def test_changed_original_synthetic_source_alleles_do_not_pass_hidden_placement():
    from scripts.model3_island.types import PlantState
    old=source_state(3)
    altered=old.alleles.copy()
    altered[0,1,:]=0.5
    # Its source may already be .5; force a robust discrepancy.
    altered[0,1,:]=0.625 if old.alleles[0,1,0]!=0.625 else 0.375
    fake=PlantState(alleles=altered,allele_origin=old.allele_origin,
                    mutation_flags=old.mutation_flags,ids=old.ids,birth_years=old.birth_years)
    with pytest.raises(ValueError,match="source-authenticated synthetic F0"):
        assign_hidden_heterozygotes(fake,3,0)


def test_carrier_overlap_alone_is_not_a_pure_I_weighted_access_treatment():
    """Same A support, but changing I-carrier identity reweights inherited I."""
    result=input_only_qa()
    count_with_I_weighted_difference=0
    for p in range(POOL_COUNT):
        rows=[r for r in result["rows"]
              if r["synthetic_source_pool"]==p and r["sample_n"]==48
              and r["context"]==0]
        assert len(rows)==4
        assert {r["A_carriers"] for r in rows}=={12}
        assert {r["I_carriers"] for r in rows}=={12}
        A=[r["expected_single_offspring_A_variance"] for r in rows]
        I=[r["expected_single_offspring_I_variance"] for r in rows]
        assert max(A)-min(A)<1e-14
        if max(I)-min(I)>1e-12:
            count_with_I_weighted_difference+=1
    # Source heterogeneity and reproductive weighting mean co-carriage
    # changes I-selected gamete access even with identical marginal counts.
    assert count_with_I_weighted_difference==POOL_COUNT
