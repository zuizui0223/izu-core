"""Exact per-locus loss and unphased diploid-dose association regressions."""
import numpy as np
import pytest

from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_k32_pathwise_selection_drift import allele_frequency_basis
from scripts.audit_model3_k32_locus_architecture import (
    LOCI,PAIRS,PAIR_NAMES,VECTOR_LABELS,
    architecture_snapshot,architecture_vector,pattern_frequencies,
)


def frozen():
    c,g,_,_=fixed_support_problem(capacity=32,ovule_budget=8.)
    return c,allele_frequency_basis(g)


def test_individual_locus_fixation_and_genotype_dosage_moments():
    first,b=frozen()
    assert len(LOCI)==3 and len(PAIRS)==3 and len(PAIR_NAMES)==3
    assert len(VECTOR_LABELS)==19
    a=architecture_snapshot(first,b)
    assert a["fixed_allele_pattern"]=="PPP"
    assert a["high_allele_frequencies"]==pytest.approx([.5,.5,.5],abs=1e-12)
    assert a["high_allele_lost"]==[0,0,0]
    assert a["low_allele_lost"]==[0,0,0]
    assert 0<=a["largest_genotype_frequency"]<=1
    assert all(v>=0 for v in a["dosage_pairwise_mutual_info_nats"])
    assert len(architecture_vector(first,b))==19
    assert architecture_snapshot(np.zeros_like(first),b) is None
    np.testing.assert_array_equal(
        architecture_vector(np.zeros_like(first),b),np.zeros(19))


def test_perfect_positive_cross_locus_dosage_association_has_mutual_information():
    first,b=frozen()
    idx_low=int(np.flatnonzero(np.all(b==0,axis=1))[0])
    idx_high=int(np.flatnonzero(np.all(b==1,axis=1))[0])
    p=np.zeros_like(first)
    p[idx_low]=16
    p[idx_high]=16
    result=architecture_snapshot(p,b)
    assert result["fixed_allele_pattern"]=="PPP"
    assert result["high_allele_frequencies"]==pytest.approx([.5,.5,.5])
    assert result["within_locus_heterozygosity"]==pytest.approx([0,0,0])
    assert result["dosage_pairwise_covariance"]==pytest.approx([.25]*3,abs=1e-12)
    assert result["dosage_pairwise_mutual_info_nats"]==pytest.approx(
        [np.log(2)]*3,abs=1e-12)
    assert result["largest_genotype_frequency"]==pytest.approx(.5)


def test_fixed_assurance_low_allele_loss_no_resurrection():
    first,b=frozen()
    mask=np.flatnonzero(b[:,2]==1)
    c=np.zeros_like(first)
    c[mask[0]]=16
    c[mask[-1]]=16
    res=architecture_snapshot(c,b)
    assert res["low_allele_lost"][2]==1
    assert res["high_allele_lost"][2]==0
    assert res["fixed_allele_pattern"].endswith("H")
    assert res["within_locus_heterozygosity"][2]==pytest.approx(0.)
    summary=pattern_frequencies(
        np.array([c,np.zeros_like(c),c]),b)
    assert summary["n_living"]==2 and summary["n_extinct"]==1
    assert summary["fixed_allele_pattern_counts"][res["fixed_allele_pattern"]]==2
    assert sum(summary["dominant_genotype_dosage_label_counts"].values())==2


def test_disallow_non_diploid_and_invalid_parent_counts():
    first,b=frozen()
    with pytest.raises(ValueError):
        architecture_snapshot(first.astype(float),b)
    with pytest.raises(ValueError):
        architecture_snapshot(first,b[:,0:2])
    with pytest.raises(ValueError):
        architecture_snapshot(first,np.full_like(b,.333))
    with pytest.raises(ValueError):
        pattern_frequencies(first,b)
