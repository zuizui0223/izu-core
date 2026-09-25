import numpy as np
import pytest

from scripts.validate_model3_evolution import check_run
from scripts.model3_evolution import simulate


def test_valid_short_run_and_corrupt_demography_are_distinguished():
    result = simulate(seed=17,years=4,selfing=1)
    case = dict(years=4,capacity=48,control='selected')
    check_run(result,case)
    result['population'][1] -= 1
    with pytest.raises(ValueError,match='demographic'):
        check_run(result,case)


def test_extinction_cannot_be_encoded_as_zero_trait():
    result = simulate(seed=17,years=4,activity=0,selfing=0,survival=0)
    case = dict(years=4,capacity=48,control='selected')
    check_run(result,case)
    result['trait_mean'][1:] = 0
    with pytest.raises(ValueError,match='extinct'):
        check_run(result,case)


def test_uninherited_allele_is_detected():
    result = simulate(seed=17,years=2,selfing=1)
    result['final_genotype'][0,0,0] = .999
    with pytest.raises(ValueError,match='allele'):
        check_run(result,dict(years=2,capacity=48,control='selected'))


@pytest.mark.parametrize('key,value', [('trait_mean',.99),('allele_count',np.nan),('visitor_count',.5)])
def test_intermediate_corruption_is_rejected(key,value):
    result=simulate(seed=17,years=3,selfing=1)
    result[key]=result[key].astype(float)
    result[key][1]=value
    with pytest.raises(ValueError):
        check_run(result,dict(years=3,capacity=48,control='selected'))


def test_extinct_population_cannot_produce_expected_offspring():
    result=simulate(seed=17,years=3,activity=0,selfing=0,survival=0)
    result['expected_outcross'][1]=1
    with pytest.raises(ValueError):
        check_run(result,dict(years=3,capacity=48,control='selected'))


def test_robustness_inbreeding_loss_is_conserved():
    from scripts.model3_robustness import simulate_scenario
    result=simulate_scenario(seed=17,years=3,selfing=.5,depression=.9)
    case=dict(years=3,capacity=48,control='selected',selfing=.5,depression=.9)
    check_run(result,case)
    result['inbreeding_loss'][0]+=1
    with pytest.raises((ValueError,AssertionError)):
        check_run(result,case)
