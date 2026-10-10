"""Frozen source and feasibility tests WITHOUT reading reserved future cohort outcomes."""
import json
import numpy as np
import pytest

from scripts.audit_chapter2_t20_assurance_new_future_multidraw import (
    contract,new_future_history,mapped_new_future_seed,
    sample_eight_individuals,paired_interval,TEST_FUTURE_SEED,
    FUTURE_SEEDS,SOURCE_HISTORIES,DRAWS,ARMS,
)
from scripts.audit_chapter2_selected_vs_neutral_parentage_new64 import (
    initial_genotypes,visitor_history
)
from scripts.audit_chapter2_t20_joint_genome_transplant import original_contract,run_future
from scripts.audit_chapter2_t20_assurance_locus_hybrid import genotypes_by_module


def test_exact_transfer_contract_still_preserves_original_donor_eligibility():
    d,digest=contract()
    assert len(digest)==64
    assert d["prior_exposure"]["selected_t20_alive"]==58
    assert d["prior_exposure"]["neutral_t20_alive"]==52
    assert d["prior_exposure"]["both_alive"]==50
    assert d["experiment"]["future_trajectories_expected"]==1200
    assert list(FUTURE_SEEDS) == list(range(61026001,61026065))
    assert mapped_new_future_seed(61024001)==61026001
    assert mapped_new_future_seed(61024064)==61026064
    with pytest.raises(ValueError):
        mapped_new_future_seed(990892)


def test_new_future_visitors_inherit_old_t20_but_have_new_seed():
    orig,_=original_contract()
    source_hist=visitor_history(orig,990892)  # not exposed donor ecology
    new=new_future_history(orig,source_hist,TEST_FUTURE_SEED)
    assert len(new.visitors)==len(new.seed_candidates)==80
    for i in range(20):
        assert new.visitors[i] is source_hist.visitors[i]
    np.testing.assert_array_equal(
        new.visitors[20].ids,source_hist.visitors[20].ids)
    np.testing.assert_array_equal(
        new.visitors[20].optima,source_hist.visitors[20].optima)
    assert all(len(x.ids)==0 for x in new.seed_candidates)
    with pytest.raises(ValueError):
        new_future_history(orig,source_hist,61027001)


def test_three_draws_of_whole_three_locus_diploid_genomes_stay_nested():
    orig,_=original_contract()
    donor=initial_genotypes(orig)
    for label in ("neutral_pre20","selected_pre20"):
        genotype_sets=[]
        for draw in range(DRAWS):
            sampled,idx=sample_eight_individuals(
                donor,source_history_seed=61024001,
                donor_label=label,draw=draw)
            assert len(sampled.ids)==len(idx)==8
            assert (sampled.birth_years==20).all()
            np.testing.assert_array_equal(sampled.alleles,donor.alleles[idx])
            np.testing.assert_array_equal(
                sampled.allele_origin,donor.allele_origin[idx])
            np.testing.assert_array_equal(
                sampled.mutation_flags,donor.mutation_flags[idx])
            genotype_sets.append(sampled)
        assert len(genotype_sets)==3
    neutral,_=sample_eight_individuals(
        donor,source_history_seed=61024001,
        donor_label="neutral_pre20",draw=1)
    selected,_=sample_eight_individuals(
        donor,source_history_seed=61024001,
        donor_label="selected_pre20",draw=1)
    hybrids=genotypes_by_module(neutral,selected)
    assert set(hybrids)==set(ARMS)
    with pytest.raises(ValueError):
        sample_eight_individuals(donor,source_history_seed=61024001,
                                 donor_label="neutral_pre20",draw=3)


def test_future_sham_with_identical_genomic_state_and_rng():
    orig,_=original_contract()
    history=visitor_history(orig,990892)
    new=new_future_history(orig,history,TEST_FUTURE_SEED)
    source=initial_genotypes(orig)
    from scripts.model3_island.types import PlantState
    neutral=PlantState(
        alleles=source.alleles,allele_origin=source.allele_origin,
        mutation_flags=source.mutation_flags,
        ids=source.ids,birth_years=np.full(8,20,dtype=np.int64)
    )
    hybrids=genotypes_by_module(neutral,neutral)
    a=run_future(orig,new,TEST_FUTURE_SEED,hybrids["neutral_all"],8,
                 "selected_source")
    b=run_future(orig,new,TEST_FUTURE_SEED,hybrids["selected_all"],8,
                 "selected_source")
    assert a==b


def test_nested_history_uncertainty_not_one_hundred_fifty_independent_sources():
    z=paired_interval(np.zeros(50))
    assert z["effect"]==0
    assert z["classification"]=="inconclusive"
    assert z["n_independent_old_donor_history_units"]==50
    assert z["independent_genotype_draws_per_source_history"]==3
    assert z["cluster_bootstrap_95"]==[0,0]
    assert z["hoeffding_95_for_cluster_means"][0]<-.05
    assert z["hoeffding_95_for_cluster_means"][1]>.05
    positive=paired_interval(np.ones(50))
    assert positive["classification"]=="resolved_positive"
    assert positive["hoeffding_95_for_cluster_means"][0]>.05
    json.dumps(positive,allow_nan=False)
    with pytest.raises(ValueError):
        paired_interval([1.1,0])
