import numpy as np
import pytest

from scripts.model3_reproduction import reproductive_ledger


def ledger(transfer, **changes):
    n = len(transfer)
    args = dict(transfer=transfer, ovules=np.full(n, 10.), pollen_scale=np.ones(n),
                autonomous_selfing=np.zeros(n), inbreeding_depression=np.zeros(n))
    args.update(changes)
    return reproductive_ledger(**args)


def test_outcross_accounting():
    r = ledger([[0., 2.], [1., 0.]], ovules=[10., 20.])
    expected = np.array([10 * -np.expm1(-1), 20 * -np.expm1(-2)])
    np.testing.assert_allclose(r['female_outcross'], expected)
    np.testing.assert_allclose(r['male_outcross'], expected[::-1])
    np.testing.assert_allclose(r['genome_equivalents'].sum(), expected.sum())


def test_delayed_selfing_viability_applied_once():
    r = ledger([[0.]], autonomous_selfing=[.5], inbreeding_depression=[.2])
    assert r['selfed_raw'][0] == 5
    assert r['selfed_viable'][0] == 4
    assert r['genome_equivalents'][0] == 4
    assert r['female_outcross'][0] == r['male_outcross'][0] == 0


@pytest.mark.parametrize('a,d', [(0, 0), (1, 1)])
def test_no_viable_reproduction_not_rescued(a, d):
    r = ledger([[0.]], autonomous_selfing=[a], inbreeding_depression=[d])
    assert r['maternal_viable'].sum() == 0


def test_donor_shares_and_total_genome_accounting():
    r = ledger([[0., 1., 3.], [2., 0., 1.], [2., 3., 0.]],
               autonomous_selfing=[.2, .3, .9], inbreeding_depression=[.1, .2, .3])
    offspring = r['outcross_by_donor_recipient']
    np.testing.assert_allclose(offspring[:, 0], [0, r['female_outcross'][0]/2, r['female_outcross'][0]/2])
    np.testing.assert_allclose(offspring.sum(axis=0), r['female_outcross'])
    np.testing.assert_allclose(offspring.sum(axis=1), r['male_outcross'])
    np.testing.assert_allclose(r['genome_equivalents'].sum(), r['maternal_viable'].sum())
    assert np.all(r['female_outcross'] + r['selfed_raw'] <= 10)


def test_zero_ovules_and_saturation():
    r = ledger([[0., 1e6], [1e6, 0.]], ovules=[0, 10], autonomous_selfing=[1, 1])
    np.testing.assert_array_equal(r['female_outcross'], [0, 10])
    np.testing.assert_array_equal(r['selfed_raw'], [0, 0])
    assert r['male_outcross'][0] == 10  # ovules are not a pollen-production proxy


@pytest.mark.parametrize('changes', [
    {'transfer': [[1.]]}, {'transfer': [[-1.]]}, {'transfer': [[np.nan]]},
    {'transfer': [[0., 1.]]}, {'transfer': []}, {'ovules': [-1.]},
    {'ovules': [np.inf]}, {'ovules': [[1.]]}, {'ovules': [1, 2]},
    {'pollen_scale': [0.]}, {'pollen_scale': [-1.]},
    {'autonomous_selfing': [1.1]}, {'inbreeding_depression': [-.1]},
])
def test_invalid_inputs_are_rejected(changes):
    args = dict(transfer=[[0.]], ovules=[1.], pollen_scale=[1.],
                autonomous_selfing=[0.], inbreeding_depression=[0.])
    args.update(changes)
    with pytest.raises(ValueError):
        reproductive_ledger(**args)


def test_tiny_pollen_uses_stable_saturation():
    r = ledger([[0., 1e-20], [0., 0.]])
    assert r['female_outcross'][1] > 0
    np.testing.assert_allclose(r['female_outcross'][1], 1e-19, rtol=1e-12, atol=0)
