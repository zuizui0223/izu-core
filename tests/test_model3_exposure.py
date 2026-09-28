import numpy as np
import pytest

from scripts.model3_exposure import flowering_schedule, effective_exposure


def test_survival_schedule():
    r = flowering_schedule([1, 1, 1], [1, 1, 1], [.5, .5])
    np.testing.assert_allclose(r['alive_probability'], [1, .5, .25])
    np.testing.assert_allclose(r['expected_effort'], [1, .5, .25])
    assert r['total_expected_effort'] == 1.75
    np.testing.assert_allclose(r['normalized_weights'], np.array([1, .5, .25])/1.75)


def test_independence_is_not_lifespan():
    assert effective_exposure([.5, .5], np.eye(2))['k_eff'] == 2
    assert effective_exposure([.5, .5], np.ones((2, 2)))['k_eff'] == 1
    assert effective_exposure([1.], [[1.]])['k_eff'] == 1


def test_unequal_effort():
    assert effective_exposure([.9, .1], np.eye(2))['k_eff'] == pytest.approx(1/.82)


def test_zero_effort_is_not_evaluable():
    r = flowering_schedule([0, 0], [1, 1], [1])
    assert r['status'] == 'not_evaluable'
    assert r['normalized_weights'] is None
    z = effective_exposure([0, 0], np.eye(2))
    assert z['status'] == 'not_evaluable' and z['k_eff'] is None


def test_maturity_and_survival():
    r = flowering_schedule([1, 1, 1], [0, 1, 1], [1, 0])
    np.testing.assert_array_equal(r['expected_effort'], [0, 1, 0])
    assert flowering_schedule([2], [.5], [])['total_expected_effort'] == 1


def test_schedule_inputs_remain_auditable_and_copied():
    effort = np.array([1., 2., 3.])
    r = flowering_schedule(effort, [1., .5, 0.], [0., .7])
    effort[0] = 99
    np.testing.assert_array_equal(r['effort'], [1, 2, 3])
    np.testing.assert_array_equal(r['flowering_probability'], [1, .5, 0])
    np.testing.assert_array_equal(r['interval_survival'], [0, .7])


@pytest.mark.parametrize('effort,flowering,survival,expected', [
    ([0, 1e300], [0, 1e-200], [1e-200], [0, 1e-100]),
    ([0, 0, 1e300], [0, 0, 1], [1e-200, 1e-200], [0, 0, 1e-100]),
])
def test_representable_effort_survives_intermediate_underflow(effort, flowering, survival, expected):
    r = flowering_schedule(effort, flowering, survival)
    assert r['status'] == 'evaluable'
    np.testing.assert_allclose(r['expected_effort'], expected, rtol=1e-12, atol=0)
    assert r['normalized_weights'][-1] == 1


def test_smallest_representable_effort_is_not_erased_by_log_roundtrip():
    tiny = np.nextafter(0., 1.)
    r = flowering_schedule([tiny], [1], [])
    assert r['total_expected_effort'] == tiny
    assert r['status'] == 'evaluable'
    assert r['normalized_weights'][0] == 1


def test_negative_correlation_not_silently_capped():
    r = effective_exposure([.5, .5], [[1, -.5], [-.5, 1]])
    assert r['k_eff'] == 4
    z = effective_exposure([.5, .5], [[1, -1], [-1, 1]])
    assert z['status'] == 'zero_variance_diagnostic' and z['k_eff'] is None


@pytest.mark.parametrize('e,f,s', [([], [], []), ([1], [1], [1]),
    ([-1], [1], []), ([np.nan], [1], []), ([1], [2], []),
    ([1, 1], [1, 1], [-.1]), ([1, 1], [1], [.5])])
def test_invalid_schedule(e, f, s):
    with pytest.raises(ValueError):
        flowering_schedule(e, f, s)


@pytest.mark.parametrize('w,r', [([], []), ([1, 1], np.eye(2)),
    ([-.1, 1.1], np.eye(2)), ([np.nan], [[1]]), ([1], [[2]]),
    ([.5,.5], [[1, 0], [.1, 1]]), ([.5,.5], [[1, 2], [2, 1]]),
    ([1], [[np.inf]]), ([1], np.eye(2))])
def test_invalid_exposure(w, r):
    with pytest.raises(ValueError):
        effective_exposure(w, r)
