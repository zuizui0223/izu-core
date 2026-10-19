"""No-biology test of matched t0 A expression and heritable standing carriers."""
from __future__ import annotations

from dataclasses import replace

import numpy as np
import pytest

from scripts.chapter2_q3_balanced_assurance_founders_20261018 import (
    balance_founder_assurance_expression,verify_pairing)


def source_founder(n=48):
    from scripts.model3_island.types import PlantState
    a=np.full((n,3,2),.5)
    a[:,1,:]=.375
    a[:,0,:]=.55
    return PlantState(
        alleles=a,allele_origin=np.arange(n*6).reshape(n,3,2),
        mutation_flags=np.zeros((n,3,2),dtype=bool),
        ids=np.arange(n,dtype=np.int64),
        birth_years=np.zeros(n,dtype=np.int64))


def test_equal_t0_assurance_expression_with_standing_Mendelian_alleles():
    old=source_founder()
    balanced=balance_founder_assurance_expression(old,seed=831991)
    np.testing.assert_array_equal(old.alleles[:,:2,:],balanced.alleles[:,:2,:])
    np.testing.assert_array_equal(old.allele_origin,balanced.allele_origin)
    assert np.var(balanced.alleles[:,2,:])>0
    np.testing.assert_array_equal(
        balanced.alleles[:,2,:].mean(axis=1),np.full(48,.5))
    assert np.var(balanced.alleles[:,2,:].mean(axis=1))==0
    np.testing.assert_array_equal(
        np.unique(balanced.alleles[:,2,:]),np.array([.25,.5,.75]))
    assert balanced is not old
    info=verify_pairing(balanced,balanced)
    assert info["source_genotypes_identical"]
    assert info["initially_expressed_A_between_adult_variance"]==0
    assert info["standing_A_allele_variance"]>0


def test_pairing_fails_if_phenotype_distribution_differs_even_with_equal_population_mean():
    source=source_founder()
    bad=source.alleles.copy()
    bad[:24,2,:]=.25
    bad[24:,2,:]=.75
    original=replace(source,alleles=bad)
    assert original.alleles[:,2,:].mean()==.5
    with pytest.raises(ValueError,match="initial expressed A not matched"):
        verify_pairing(original,original)
    good=balance_founder_assurance_expression(source,seed=110239)
    with pytest.raises(ValueError,match="starting genotypes differ"):
        verify_pairing(good,original)


def test_design_is_seeded_and_fails_closed_for_nonmatching_or_unbalanced_sources():
    f=source_founder()
    x=balance_founder_assurance_expression(f,seed=123)
    y=balance_founder_assurance_expression(f,seed=123)
    np.testing.assert_array_equal(x.alleles,y.alleles)
    with pytest.raises(ValueError,match="founders"):
        balance_founder_assurance_expression(source_founder(47),seed=123)
    with pytest.raises(ValueError,match="seed"):
        balance_founder_assurance_expression(f,seed=-1)
    with pytest.raises(ValueError,match="fixed assurance"):
        verify_pairing(x,x,fixed_A=.3)
