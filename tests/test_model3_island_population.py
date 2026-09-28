from dataclasses import replace
import numpy as np
import pytest

from test_model3_island_state import config_fixture, plant_fixture
from test_model3_island_assays import visitors
from scripts.model3_island.population import inherit, advance, resident_seed_control
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.randomness import stream, STREAM_IDS


def rngs(seed=2):
    return {name:stream(seed,name,0) for name in STREAM_IDS}


def test_mendelian_support_and_genealogical_origins():
    p=plant_fixture(2)
    a=np.tile([.2,.8],(2,3,1)); origins=np.broadcast_to([10,20],a.shape).copy()
    p=replace(p,alleles=a,allele_origin=origins)
    c=replace(config_fixture(),capacity=4096)
    children=inherit(p,np.zeros(4096,dtype=int),np.ones(4096,dtype=int),c,
        segregation_rng=stream(2,'segregation',0),mutation_rng=stream(2,'mutation',0),year=1)
    assert set(np.unique(children.alleles))=={.2,.8}
    np.testing.assert_array_equal(children.allele_origin,np.where(children.alleles==.2,10,20))
    assert abs((children.alleles[:,0,0]==.2).mean()-.5)<.025
    assert not children.mutation_flags.any()
    assert len(np.unique(children.ids))==4096 and (children.birth_years==1).all()


def test_mutation_does_not_fabricate_new_ancestors():
    p=plant_fixture(2); c=replace(config_fixture(),mutation_rate=1.,mutation_sd=.5,assurance_mode='evolving')
    child=inherit(p,np.array([0]),np.array([1]),c,segregation_rng=stream(4,'segregation',0),
                  mutation_rng=stream(4,'mutation',0),year=1)
    assert child.mutation_flags.all() and not np.array_equal(child.alleles,p.alleles[:1])
    assert ((child.alleles>=0)&(child.alleles<=1)).all()
    assert (child.allele_origin==0).all()


def test_extinction_recolonization_and_no_immediate_immigrant_reproduction():
    c=replace(config_fixture(),fixed_assurance=0.,seed_arrival=replace(config_fixture().seed_arrival,establishment=1.))
    p=plant_fixture(2); empty=plant_fixture(0)
    dead,info=advance(p,reproduce(p,visitors(0),c),empty,c,rngs(),year=0)
    assert len(dead.ids)==0 and info['resident_recruits']==0
    incoming=replace(plant_fixture(1),ids=np.array([2**32]),birth_years=np.array([2]))
    new,info=advance(dead,reproduce(dead,visitors(0),c),incoming,c,rngs(),year=1)
    assert new.ids.tolist()==[2**32] and info['resident_potential']==0
    assert info['immigrant_recruits']==1


def test_capacity_and_genome_conservation_for_homozygous_parents():
    c=replace(config_fixture(),capacity=2,fixed_assurance=1.,ovule_budget=1000.)
    p=plant_fixture(2)
    new,info=advance(p,reproduce(p,visitors(0),c),plant_fixture(0),c,rngs(),year=0)
    assert len(new.ids)==2 and info['resident_potential']>=2
    np.testing.assert_array_equal(new.alleles,p.alleles)
    assert info['immigrant_recruits']==0
    assert (new.birth_years==1).all()


def test_empty_resident_seed_control_is_non_evaluable():
    incoming=replace(plant_fixture(2),ids=np.array([2**32,2**32+1]),birth_years=np.array([1,1]))
    controlled,reason=resident_seed_control(plant_fixture(0),incoming,stream(2,'source_genotypes',0))
    assert controlled is None and reason=='no_resident_genotype_distribution'
    controlled,reason=resident_seed_control(plant_fixture(1),incoming,stream(2,'source_genotypes',0))
    assert reason is None
    np.testing.assert_array_equal(controlled.ids,incoming.ids)
    np.testing.assert_array_equal(controlled.allele_origin,incoming.allele_origin)


def test_invalid_parent_indices_and_duplicate_immigrants_rejected():
    p=plant_fixture(2); c=config_fixture()
    with pytest.raises(ValueError):
        inherit(p,np.array([2]),np.array([0]),c,segregation_rng=stream(2,'segregation',0),
                mutation_rng=stream(2,'mutation',0),year=1)
    with pytest.raises(ValueError):
        advance(p,reproduce(p,visitors(),c),p,c,rngs(),year=0)


def test_inactive_assurance_alleles_are_bit_exact_when_other_loci_mutate():
    p=plant_fixture(1)
    alleles=p.alleles.copy(); alleles[:,2,:]=.1
    p=replace(p,alleles=alleles)
    c=replace(config_fixture(),mutation_rate=1.,mutation_sd=.1,assurance_mode='fixed')
    child=inherit(p,np.array([0]),np.array([0]),c,segregation_rng=stream(8,'segregation',0),
                  mutation_rng=stream(8,'mutation',0),year=1)
    np.testing.assert_array_equal(child.alleles[:,2,:],p.alleles[:,2,:])
    assert not child.mutation_flags[:,2,:].any()


def test_surviving_adults_retain_ids_and_birth_years_without_reproduction():
    c=replace(config_fixture(),survival=1.,fixed_assurance=0.)
    p=plant_fixture(2)
    new,info=advance(p,reproduce(p,visitors(0),c),plant_fixture(0),c,rngs(),year=0)
    np.testing.assert_array_equal(new.ids,p.ids)
    np.testing.assert_array_equal(new.birth_years,p.birth_years)
    assert info['survivors']==2 and info['parent_contributions']==0
