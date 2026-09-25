import numpy as np
import pytest

from scripts.model3_evolution import pollen_transfer, inherit, neutralize


def test_no_reproduction_annual_population_goes_extinct():
    from scripts.model3_evolution import next_population
    genotype = np.full((4,2,2), .5)
    new, info = next_population(genotype, np.zeros((4,4)), 0, 4, np.random.default_rng(4))
    assert new.shape == (0,2,2)
    assert info == dict(survivors=0, potential_recruits=0, established=0)


def test_perennial_survivors_keep_their_genotypes_without_reproduction():
    from scripts.model3_evolution import next_population
    genotype = np.arange(16).reshape(4,2,2)/16
    new, info = next_population(genotype, np.zeros((4,4)), 1, 4, np.random.default_rng(4))
    np.testing.assert_array_equal(new, genotype)
    assert info['survivors'] == 4


def test_recruitment_is_capacity_limited_and_inherited():
    from scripts.model3_evolution import next_population
    genotype = np.array([[[.1,.1],[.2,.2]],[[.7,.7],[.8,.8]]])
    # Only father 0 x mother 1 can reproduce.
    pairs = np.array([[0.,1000.],[0.,0.]])
    new, info = next_population(genotype, pairs, 0, 5, np.random.default_rng(4))
    assert len(new) == 5
    np.testing.assert_allclose(new.mean(axis=2), np.tile([.4,.5],(5,1)))
    assert info['potential_recruits'] > info['established'] == 5


def test_empty_population_is_absorbing():
    from scripts.model3_evolution import next_population
    new, info = next_population(np.empty((0,2,2)), np.empty((0,0)), .75, 48, np.random.default_rng(4))
    assert len(new) == 0 and info['established'] == 0


def test_simulation_records_extinction_not_zero_traits():
    from scripts.model3_evolution import simulate
    result = simulate(seed=17, years=3, activity=0, selfing=0, survival=0)
    assert result['population'].tolist() == [48,0,0,0]
    assert np.isnan(result['trait_mean'][1:]).all()
    assert result['extinction_year'] == 1


def test_simulation_selfing_is_separate_from_outcross_and_repeatable():
    from scripts.model3_evolution import simulate
    kwargs = dict(seed=17, years=3, activity=0, selfing=1, survival=0)
    first, second = simulate(**kwargs), simulate(**kwargs)
    assert first['expected_selfed'].sum() > 0
    assert first['expected_outcross'].sum() == 0
    np.testing.assert_array_equal(first['trait_mean'],second['trait_mean'])


def test_fixed_trait_control_cannot_evolve():
    from scripts.model3_evolution import simulate
    result = simulate(seed=17,years=4,selfing=1,control='fixed')
    alive = result['population'] > 0
    np.testing.assert_allclose(result['trait_mean'][alive], np.tile(result['trait_mean'][0],(alive.sum(),1)),atol=1e-14)
    assert (result['population'] <= 48).all()


def test_no_mutation_cannot_restore_lost_alleles():
    from scripts.model3_evolution import simulate
    result = simulate(seed=17,years=4,selfing=1)
    assert (np.diff(result['allele_count'],axis=0) <= 0).all()
    for locus in range(2):
        assert np.isin(result['final_genotype'][:,locus],result['initial_genotype'][:,locus]).all()


def test_empty_visitors_and_zero_activity_deliver_no_pollen():
    traits = np.array([[.2,.4],[.8,.7]])
    assert not pollen_transfer(traits, np.empty(0), .2, 1, 10, 48).any()
    assert not pollen_transfer(traits, np.array([.3]), .2, 0, 10, 48).any()


def test_pollen_is_finite_and_self_pollen_excluded():
    traits = np.array([[.2,.4],[.8,.7],[.5,.5]])
    result = pollen_transfer(traits, np.array([.2,.8]), .2, 100, 10, 48)
    assert np.diag(result).sum() == 0
    assert (result >= 0).all()
    assert (result.sum(axis=1) <= 10).all()
    assert result.sum() > 0


def test_absolute_activity_matters_and_type_duplication_does_not():
    traits = np.array([[.2,.4],[.8,.7],[.5,.5]])
    visitors = np.array([.2,.8])
    lo = pollen_transfer(traits, visitors, .2, .1, 10, 48)
    hi = pollen_transfer(traits, visitors, .2, 1, 10, 48)
    assert hi.sum() > lo.sum()
    np.testing.assert_allclose(hi, pollen_transfer(traits, np.tile(visitors,3), .2, 1, 10, 48))


def test_mendelian_offspring_only_take_parental_alleles():
    genotype = np.array([[[.1,.2],[.3,.4]],[[.6,.7],[.8,.9]]])
    offspring = inherit(genotype, np.zeros(500,dtype=int), np.ones(500,dtype=int), np.random.default_rng(7))
    assert offspring.shape == (500,2,2)
    for locus in range(2):
        assert np.isin(offspring[:,locus,0], genotype[0,locus]).all()
        assert np.isin(offspring[:,locus,1], genotype[1,locus]).all()
    assert abs(offspring[:,0,0].mean()-.15) < .015


def test_selfing_samples_two_independent_gametes():
    genotype = np.array([[[0.,1.],[0.,1.]]])
    offspring = inherit(genotype, np.zeros(10000,dtype=int), np.zeros(10000,dtype=int), np.random.default_rng(7))
    dosage = offspring[:,0].sum(axis=1)
    np.testing.assert_allclose(np.bincount(dosage.astype(int),minlength=3)/10000, [.25,.5,.25], atol=.015)


def test_neutral_control_preserves_selfing_and_outcross_totals():
    reproductive_pairs = np.array([[1.,2.,0.],[0.,3.,0.],[1.,0.,2.]])
    neutral = neutralize(reproductive_pairs)
    assert np.trace(neutral) == pytest.approx(6)
    assert neutral.sum()-np.trace(neutral) == pytest.approx(3)
    np.testing.assert_allclose(np.diag(neutral), [2,2,2])
    np.testing.assert_allclose(neutral[~np.eye(3,dtype=bool)], .5)


@pytest.mark.parametrize('activity',[-1,np.nan,np.inf])
def test_invalid_activity_fails(activity):
    with pytest.raises(ValueError):
        pollen_transfer(np.array([[.5,.5]]),np.array([.5]),.2,activity,10,48)
