import math

import numpy as np
import pytest

from scripts.model3_island.expectation import capped_poisson_mean, expected_recruits


def test_capped_poisson_boundary_and_exact_one_slot():
    assert capped_poisson_mean(0, 8) == 0
    assert capped_poisson_mean(20, 0) == 0
    assert capped_poisson_mean(1, 1) == pytest.approx(1-math.exp(-1), abs=1e-12)
    assert capped_poisson_mean(1e6, 3) == pytest.approx(3)


@pytest.mark.parametrize('n', range(4))
@pytest.mark.parametrize('survival', [0., .3, 1.])
@pytest.mark.parametrize('rate', [0., .1, 1., 4.])
def test_expected_recruits_matches_direct_enumeration(n, survival, rate):
    capacity = n+1
    value = 0.
    for j in range(n+1):
        prob = math.comb(n, j)*survival**j*(1-survival)**(n-j)
        poisson_mean = sum(min(b, capacity-j)*math.exp(-rate)*rate**b/math.factorial(b)
                           for b in range(70))
        value += prob*poisson_mean
    actual = expected_recruits(n, survival, capacity, rate)
    assert actual == pytest.approx(value, abs=1e-12)
    assert 0 <= actual <= min(rate, capacity-n*survival)+1e-12


def test_no_vacancy_and_empty_population():
    assert expected_recruits(4, 1, 4, 10) == 0
    assert expected_recruits(0, 0, 2, 0) == 0
    assert expected_recruits(1, 0, 1, 1) == pytest.approx(1-math.exp(-1))


@pytest.mark.parametrize('rate,vacancies', [(-1, 2), (np.nan, 2), (np.inf, 2),
                                         (1, -1), (1, 2.5), (1, True)])
def test_invalid_poisson_settings_rejected(rate, vacancies):
    with pytest.raises(ValueError):
        capped_poisson_mean(rate, vacancies)


@pytest.mark.parametrize('args', [(3,.5,2,1), (2.1,.5,4,1), (True,.5,4,1),
                                 (2,-.1,4,1), (2,np.nan,4,1), (2,1.1,4,1)])
def test_invalid_survival_and_population_rejected(args):
    with pytest.raises(ValueError):
        expected_recruits(*args)
