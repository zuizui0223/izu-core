import numpy as np

from scripts.model3_meanfield import genotype_grid, meanfield_step
from scripts.model3_evolution import pollen_transfer
from scripts.model3_reproduction import reproductive_ledger


def test_mendelian_kernel_preserves_probability_and_parental_mean():
    genotypes,kernel=genotype_grid(.3,3)
    assert genotypes.shape==(36,2,2)
    np.testing.assert_allclose(kernel.sum(axis=2),1)
    assert (kernel>=0).all()
    traits=genotypes.mean(axis=2)
    np.testing.assert_allclose(kernel @ traits, .5*(traits[:,None,:]+traits[None,:,:]),atol=1e-14)


def test_no_visitors_or_selfing_annual_population_loses_all_mass():
    genotypes,kernel=genotype_grid(.3,3)
    density=np.full(36,1/36)
    result=meanfield_step(density,genotypes,kernel,np.empty(0),activity=1,survival=0,selfing=0)
    np.testing.assert_array_equal(result['density'],0)


def test_delayed_selfing_reproduces_without_visitors_and_respects_density_cap():
    genotypes,kernel=genotype_grid(.3,3)
    density=np.full(36,1/36)
    result=meanfield_step(density,genotypes,kernel,np.empty(0),activity=1,survival=.75,selfing=.5)
    assert result['selfed']>0
    assert result['outcross']==0
    assert .75<result['density'].sum()<=1+1e-12


def test_duplicate_visitor_types_preserve_total_activity():
    genotypes,kernel=genotype_grid(.3,3)
    density=np.full(36,1/36)
    settings=dict(activity=1,survival=0,selfing=.5)
    one=meanfield_step(density,genotypes,kernel,np.array([.3,.8]),**settings)
    two=meanfield_step(density,genotypes,kernel,np.tile([.3,.8],3),**settings)
    np.testing.assert_allclose(one['density'],two['density'])


def test_depression_can_remove_all_assurance_in_distribution_model():
    genotypes,kernel=genotype_grid(.3,3)
    density=np.full(36,1/36)
    result=meanfield_step(density,genotypes,kernel,np.empty(0),activity=1,
                         survival=0,selfing=1,depression=1)
    assert result['density'].sum()==0
    assert result['selfed']==0


def test_double_heterozygote_selfing_has_mendelian_genotype_probabilities():
    genotypes,kernel=genotype_grid(.3,3)
    index=np.flatnonzero(np.isclose(genotypes[:,0,0],.2)&np.isclose(genotypes[:,0,1],.4)
                         &np.isclose(genotypes[:,1,0],.4)&np.isclose(genotypes[:,1,1],.6))[0]
    offspring=kernel[index,index]
    np.testing.assert_allclose(np.sort(offspring[offspring>0]),[.0625]*4+[.125]*4+[.25])


def test_density_transfer_matches_large_individual_population_limit():
    genotypes,kernel=genotype_grid(.3,3)
    density=np.zeros(36)
    density[0]=1
    visitors=np.array([.2,.5,.8])
    target=meanfield_step(density,genotypes,kernel,visitors,activity=.4,survival=.75,selfing=0)['outcross']
    errors=[]
    for n in [48,192]:
        traits=np.tile(genotypes[0].mean(axis=1),(n,1))
        transfer=pollen_transfer(traits,visitors,.2,.4,2.5,n)
        ledger=reproductive_ledger(transfer,np.exp(-.5*traits[:,1]**2),np.ones(n),np.zeros(n),np.full(n,.5))
        finite=2*ledger['female_outcross'].sum()/n
        assert target>finite
        errors.append(target-finite)
    assert errors[1]<.3*errors[0]
