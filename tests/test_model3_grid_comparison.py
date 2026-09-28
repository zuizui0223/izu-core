import numpy as np
import pytest


def test_paired_initial_moments_and_external_history_are_identical():
    from scripts.model3_grid_comparison import simulate_grid_pair
    from scripts.model3_meanfield import genotype_grid
    result=simulate_grid_pair(seed=47,years=5,capacity=48,start=.3,selfing=.5)
    grid,_=genotype_grid(.3,3)
    density=result['density'][0]
    np.testing.assert_allclose(density.sum(),1)
    np.testing.assert_allclose(density @ grid.mean(axis=2),result['trait_mean'][0])
    assert result['density'].shape==(6,36)
    neutral=simulate_grid_pair(seed=47,years=5,capacity=48,start=.3,selfing=.5,control='neutral')
    np.testing.assert_array_equal(result['visitor_count'],neutral['visitor_count'])


def test_paired_zero_pollen_without_selfing_causes_annual_extinction():
    from scripts.model3_grid_comparison import simulate_grid_pair
    result=simulate_grid_pair(seed=47,years=3,activity=0,selfing=0,survival=0)
    np.testing.assert_array_equal(result['population'][1:],0)
    np.testing.assert_array_equal(result['density'][1:],0)


def test_unsupported_effort_does_not_silently_mismatch_density_model():
    from scripts.model3_grid_comparison import simulate_grid_pair
    with pytest.raises(ValueError,match='baseline reproductive settings'):
        simulate_grid_pair(seed=47,years=2,pollen_effort='annual')


def test_grid_campaign_freeze_has_complete_declared_crossing(tmp_path):
    from scripts.run_model3_grid_comparison import build_cases,freeze,verify_freeze
    cases=build_cases()
    assert len(cases)==2560
    assert len({c['case_id'] for c in cases})==2560
    assert sum(c['points']==3 for c in cases)==2048
    path=tmp_path/'design.json'
    freeze(path)
    assert len(verify_freeze(path)['cases'])==2560


def test_grid_validation_rejects_mismatched_initial_distribution():
    from scripts.model3_grid_comparison import simulate_grid_pair
    from scripts.validate_model3_evolution import check_run
    case=dict(seed=47,years=5,capacity=48,start=.3,selfing=.5,survival=0.,control='selected',
              points=3,depression=.5)
    result=simulate_grid_pair(**case)
    padded=np.full((48,2,2),np.nan)
    padded[:len(result['final_genotype'])]=result['final_genotype']
    result['final_genotype']=padded
    result['extinction_year']=-1 if result['extinction_year'] is None else result['extinction_year']
    check_run(result,case)
    result['density'][0]=0
    result['density'][0,0]=1
    with pytest.raises(AssertionError):
        check_run(result,case)
