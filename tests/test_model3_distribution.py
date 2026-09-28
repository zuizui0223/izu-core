import numpy as np
import pytest

from scripts.model3_distribution import expected_transition_moments
from scripts.model3_evolution import next_population


def test_poisson_recruitment_at_one_vacancy_is_not_minimum_of_mean():
    genotype = np.full((1,2,2),.5)
    result = expected_transition_moments(genotype,np.array([[2.]]),0,1)
    assert result['population'] == pytest.approx(1-np.exp(-2))
    np.testing.assert_allclose(result['trait_total'], .5*(1-np.exp(-2)))


def test_exact_conditional_moments_agree_with_individual_transitions():
    genotype = np.array([[[.1,.3],[.2,.4]],[[.6,.8],[.5,.9]],[[.3,.7],[.4,.6]]])
    pairs = np.array([[.1,.2,.05],[.3,.1,.1],[0.,.2,.1]])
    expected = expected_transition_moments(genotype,pairs,.4,4)
    rng = np.random.default_rng(7469)
    populations, trait_totals = [],[]
    for _ in range(4096):
        output,_ = next_population(genotype,pairs,.4,4,rng)
        populations.append(len(output))
        trait_totals.append(output.mean(axis=2).sum(axis=0))
    assert np.mean(populations) == pytest.approx(expected['population'],abs=.05)
    np.testing.assert_allclose(np.mean(trait_totals,axis=0),expected['trait_total'],atol=.04)


def test_empty_population_has_zero_mass_not_normalized_trait():
    result = expected_transition_moments(np.empty((0,2,2)),np.empty((0,0)),.75,48)
    assert result['population'] == 0
    np.testing.assert_array_equal(result['trait_total'],[0,0])
