"""Balanced t0 co-carriage: same reproduction and F1 marginal moments, different joint access."""
import numpy as np
import pytest

from scripts.model3_island import reproduction, types
from scripts.audit_chapter2_original_founder_compatibility_20261014 import (
    original_fixture, original_context,
)
from scripts.audit_chapter2_founder_F1_conditional_moments_20261014 import (
    conditional_f1_moments,
)
from scripts.audit_chapter2_balanced_cocarriage_20261014 import (
    POOL_COUNT, STRATA, COPY_PER_STRATUM, OVERLAPS,
    balanced_source, balanced_cocarriage,
    joint_pre_mutation_segregational_deviations, source_only_audit,
)


def test_every_source_has_four_identical_adult_phenotypes_per_stratum():
    for pool in range(POOL_COUNT):
        baseline=balanced_source(pool)
        assert len(baseline.ids)==48
        assert baseline.alleles.shape==(48,3,2)
        assert np.all(baseline.alleles[:,2,:]==.5)
        assert len(set(baseline.alleles.tobytes()[i:i+1] for i in range(10)))>0
        for g in range(STRATA):
            group=baseline.alleles[4*g:4*g+COPY_PER_STRATUM]
            assert np.array_equal(group,np.repeat(group[0:1],4,axis=0))


def test_each_quartet_reassigns_I_without_changing_A_or_adult_payoffs():
    d=original_fixture()
    for pool in (0,1,8,15):
        source=balanced_source(pool)
        lastA=None
        for m in OVERLAPS:
            state=balanced_cocarriage(source,pool,m)
            A=set(np.flatnonzero(state.alleles[:,2,0]!=state.alleles[:,2,1]))
            I=set(np.flatnonzero(state.alleles[:,1,0]!=state.alleles[:,1,1]))
            assert len(A)==len(I)==12 and len(A&I)==m
            assert lastA is None or A==lastA
            lastA=A
            for g in range(STRATA):
                group=set(range(g*4,g*4+4))
                assert len(A&group)==len(I&group)==1
            assert np.array_equal(state.alleles.mean(axis=2),
                                  source.alleles.mean(axis=2))
            assert np.array_equal(state.alleles[:,0],
                                  source.alleles[:,0])
            for j in (0,3,4):
                config,vis=original_context(d,"main",j)
                l0=reproduction.reproduce(source,vis,config)
                l1=reproduction.reproduce(state,vis,config)
                for field in ("outcross","self_viable","maternal","paternal"):
                    assert np.array_equal(getattr(l0,field),getattr(l1,field))


def test_original_selfing_only_creates_distinct_joint_access_at_matched_marginals():
    fixture=original_fixture()
    cfg,visitor=original_context(fixture,"main",0)
    assert len(visitor.ids)==0
    for pool in range(POOL_COUNT):
        old=balanced_source(pool)
        vals={}
        for m in OVERLAPS:
            edited=balanced_cocarriage(old,pool,m)
            ledger=reproduction.reproduce(edited,visitor,cfg)
            r=joint_pre_mutation_segregational_deviations(edited,ledger)
            vals[m]=r
            assert abs(r["p_nonzero_A_segregation_relative_to_parent_midpoint"]-.125)<1e-14
            assert abs(r["p_nonzero_I_segregation_relative_to_parent_midpoint"]-.125)<1e-14
        assert vals[0]["p_joint_nonzero_A_and_I_segregation"]==0
        assert abs(vals[12]["p_joint_nonzero_A_and_I_segregation"]-.0625)<1e-14
        assert (vals[0]["excess_joint_probability_over_marginal_product"]
                < vals[12]["excess_joint_probability_over_marginal_product"])


def test_direct_four_gamete_copy_enumeration_matches_joint_integral():
    fixture=original_fixture()
    cfg,vis=original_context(fixture,"main",3)
    old=balanced_source(2)
    state=balanced_cocarriage(old,2,3)
    ledger=reproduction.reproduce(state,vis,cfg)
    out=joint_pre_mutation_segregational_deviations(state,ledger)
    weights=ledger.outcross.copy()
    weights[np.diag_indices(48)]+=ledger.self_viable
    weights/=weights.sum()
    pA,pI,pAI=0.,0.,0.
    for father in range(48):
        for mother in range(48):
            weight=weights[father,mother]
            if not weight:continue
            local={}
            for locus in (1,2):
                mid=(state.alleles[father,locus].mean()+
                     state.alleles[mother,locus].mean())/2
                dev=0
                for fcopy in (0,1):
                    for mcopy in (0,1):
                        child=(state.alleles[father,locus,fcopy]+
                               state.alleles[mother,locus,mcopy])/2
                        dev+=child!=mid
                local[locus]=dev/4
            pA+=weight*local[2]
            pI+=weight*local[1]
            pAI+=weight*local[2]*local[1]
    assert abs(pA-out["p_nonzero_A_segregation_relative_to_parent_midpoint"])<1e-13
    assert abs(pI-out["p_nonzero_I_segregation_relative_to_parent_midpoint"])<1e-13
    assert abs(pAI-out["p_joint_nonzero_A_and_I_segregation"])<1e-13


def test_whole_synthetic_pool_grid_has_same_marginal_genetics_across_m():
    r=source_only_audit()
    assert r["status"]=="TECHNICAL_T0_PREMUTATION_ANALYTICAL_MEIOSIS_ONLY"
    assert r["native_static_return_comparisons"]==16*4*3==192
    assert r["native_conditioned_F1_single_offspring_marginal_comparisons"]==192
    assert r["new_biological_genotype_transmission_or_population_histories"]==0
    assert r["independently_observed_natural_source_populations"]==0
    assert r["founder_sample_sizes_intervened"] is False
    assert len(r["rows"])==192
    for pool in range(POOL_COUNT):
        for context in (0,3,4):
            rows=[x for x in r["rows"] if x["artificial_source_pool"]==pool
                  and x["visitor_context"]==context]
            assert len(rows)==4
            for key in ("expected_first_offspring_variance_A",
                        "expected_first_offspring_variance_I",
                        "p_nonzero_A_segregation_relative_to_parent_midpoint",
                        "p_nonzero_I_segregation_relative_to_parent_midpoint"):
                values=[x[key] for x in rows]
                assert max(values)-min(values)<2e-14
            if context==0:
                lookup={x["co_carriers_m"]:x for x in rows}
                assert lookup[0]["p_joint_nonzero_A_and_I_segregation"]==0
                assert abs(lookup[12]["p_joint_nonzero_A_and_I_segregation"]-.0625)<1e-14


@pytest.mark.parametrize("pool,m",[
    (-1,0),(16,0),(0,-1),(0,9),(0,13),(True,0),(0,True),
])
def test_only_registered_source_and_overlap_treatments_are_allowed(pool,m):
    with pytest.raises(ValueError,match="Unregistered"):
        if pool in (-1,16,True):
            balanced_source(pool)
        else:
            balanced_cocarriage(balanced_source(pool),pool,m)


def test_a_missing_or_asymmetric_carrier_is_not_wrongly_admitted():
    base=balanced_source(0)
    bad=base.alleles.copy()
    bad[0,1,0]=.5
    from scripts.model3_island.types import PlantState
    altered=PlantState(alleles=bad,allele_origin=base.allele_origin,
                       mutation_flags=base.mutation_flags,
                       ids=base.ids,birth_years=base.birth_years)
    with pytest.raises(ValueError,match="source phenotype reference drift"):
        balanced_cocarriage(altered,0,3)
