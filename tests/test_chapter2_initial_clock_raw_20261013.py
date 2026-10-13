import numpy as np
import pytest

from scripts.audit_chapter2_initial_clock_raw_20261013 import _initial_features, _task_key


def example():
    a = np.full((48, 3, 2), 0.5)
    a[:, 2, 0] = 0.4375
    a[:, 2, 1] = 0.5625
    a[:24, 1, :] = 0.25
    a[24:, 1, :] = 0.75
    return dict(alleles=a, offsets=np.r_[0, np.full(201, 48)],
                means=np.r_[a.mean(axis=(0, 2))[None, :], np.zeros((200, 3))],
                sexual_selection=np.zeros((200, 3, 3)), population=np.full(201, 48),
                ids=np.arange(48))


def test_t0_is_unchanged_by_future_genotypes_or_events():
    a = example()
    f0, source = _initial_features(a)
    assert np.isclose(f0['A_expected_F1_Mendelian_variance_no_mutation'], 0.001953125)
    assert f0['t0_expected_A_response'] == 0
    assert f0['A_variance_expressed'] == 0
    assert f0['I_variance_expressed'] > 0
    a['alleles'] = np.r_[a['alleles'], np.zeros((48, 3, 2))]
    a['offsets'][-1] = 96
    assert _initial_features(a)[0] == f0


def test_focal_selection_must_not_be_confused_with_gene_covar():
    a = example()
    a['sexual_selection'][0, 0, 1] = -0.04
    a['sexual_selection'][0, 1, 1] = +0.01
    f, _ = _initial_features(a)
    assert np.isclose(f['t0_expected_investment_decline'], 0.03)
    assert f['t0_I_in_decline_direction']


def test_fails_on_assurance_response_drift():
    a = example()
    a['sexual_selection'][0, 0, 2] = 0.02
    with pytest.raises(ValueError, match='zero at t0'):
        _initial_features(a)


def test_fails_on_unrelated_founder_genotype():
    a = example()
    a['alleles'][0, 2, 0] = 0.3
    with pytest.raises(ValueError, match='Assurance founder'):
        _initial_features(a)


def test_rejects_future_or_missing_task_identity():
    base = {'block': 'main', 'context': 3, 'replicate': 12,
            'supply': 0.125, 'composition': 'matched'}
    assert _task_key(base) == ('main', 3, 12)
    for v in [{'replicate': 128}, {'supply': 0.5}, {'block': 'other'}, {'context': 9}]:
        b = {**base, **v}
        with pytest.raises(ValueError): _task_key(b)