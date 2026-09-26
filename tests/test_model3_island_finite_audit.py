from itertools import product

import numpy as np
import pytest

from scripts.model3_evolution import pollen_transfer
from scripts.model3_island.finite_audit import aggregate_transfer, expected_genotype_counts


@pytest.mark.parametrize('genotype', [np.full((1,2,2),.5), np.full((2,2,2),.5),
    np.array([[[.2,.4],[.3,.5]],[[.7,.8],[.8,.9]],[[.2,.4],[.3,.5]]]),
    np.empty((0,2,2))])
@pytest.mark.parametrize('visitors', [np.array([]), np.array([.5]), np.array([.1,.5,.8])])
def test_aggregate_matches_individual_matrix_and_conserves_pollen(genotype, visitors):
    kw=dict(breadth=.2, activity=.4, budget=20., background=48.)
    result=aggregate_transfer(genotype, visitors, **kw)
    individual=pollen_transfer(genotype.mean(axis=2),visitors,**kw)
    expected=np.zeros_like(result['transfer'])
    for i,j in product(range(len(genotype)),repeat=2):
        expected[result['class_index'][i],result['class_index'][j]]+=individual[i,j]
    np.testing.assert_allclose(result['transfer'],expected,atol=1e-12)
    np.testing.assert_allclose(result['exported'],result['transfer'].sum(axis=1)
                              +result['self_loss']+result['background_loss'],atol=1e-12)
    assert (result['background_loss']>=-1e-12).all()
    if len(genotype)==2 and len(visitors):
        assert result['transfer'][0,0]>0  # Same genotype, two different plants.
    if len(genotype)==1:
        assert result['transfer'].sum()==0


def test_exact_offspring_counts_for_two_homozygotes():
    genotype=np.array([[[.1,.1],[.2,.2]],[[.7,.7],[.8,.8]]])
    result=expected_genotype_counts(genotype,np.array([[0.,1.],[0.,0.]]),survival=0,capacity=1+len(genotype))
    expected_births=3-5.5*np.exp(-1)  # E[min(Pois(1),3)]
    target=np.array([[.1,.7],[.2,.8]])
    idx=np.flatnonzero((result['genotypes']==target).all(axis=(1,2)))
    assert len(idx)==1
    assert result['expected_counts'][idx[0]]==pytest.approx(expected_births)
    assert result['expected_counts'].sum()==pytest.approx(expected_births)


def test_heterozygous_selfing_enumeration_and_survival():
    genotype=np.array([[[.2,.8],[.3,.7]]])
    result=expected_genotype_counts(genotype,np.array([[1.]]),survival=.5,capacity=2)
    # Independently enumerate 16 possible combinations of maternal/paternal alleles.
    probabilities={}
    for a,b,c,d in product(range(2),repeat=4):
        child=(tuple(sorted([genotype[0,0,a],genotype[0,0,b]])),
               tuple(sorted([genotype[0,1,c],genotype[0,1,d]])))
        probabilities[child]=probabilities.get(child,0)+1/16
    mean_births=.5*(1-np.exp(-1))+.5*(2-3*np.exp(-1))
    for child,count in zip(result['genotypes'],result['expected_counts']):
        key=tuple(map(tuple,child))
        expected=mean_births*probabilities[key]+(.5 if np.array_equal(child,genotype[0]) else 0)
        assert count==pytest.approx(expected)
    assert result['expected_counts'].sum()<=2


def test_empty_zero_birth_and_no_mutation_support():
    result=expected_genotype_counts(np.empty((0,2,2)),np.empty((0,0)),survival=.5,capacity=2)
    assert result['genotypes'].shape==(0,2,2)
    assert result['expected_counts'].size==0
    g=np.array([[[.4,.6],[.3,.7]]])
    r=expected_genotype_counts(g,np.zeros((1,1)),survival=1,capacity=1)
    np.testing.assert_array_equal(r['genotypes'],g)
    np.testing.assert_array_equal(r['expected_counts'],[1])


def test_invalid_state_rejected():
    with pytest.raises(ValueError):
        expected_genotype_counts(np.full((2,2,2),.5),np.ones((2,2)),survival=.5,capacity=1)
    with pytest.raises(ValueError):
        expected_genotype_counts(np.full((1,2,2),.5),np.array([[-1.]]),survival=.5,capacity=1)
