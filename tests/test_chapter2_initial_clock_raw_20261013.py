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

def test_admitted_full_source_t0_profile_summary_when_repository_checkout_has_it():
    import json
    from pathlib import Path
    p = Path('data/results/chapter2_initial_clock_t0_raw_20261013.json')
    if not p.exists():
        pytest.skip('Source-admitted compact t0 readout not staged in standalone source tests')
    d = json.loads(p.read_text())
    assert d['status'] == 'ALL2304_ORIGINAL_INITIAL_FEATURES_ADMITTED'
    assert d['original_starts'] == 2304 and d['founder_contexts'] == 18
    assert d['execution']['conclusion'] == 'success'
    assert d['execution']['job_id'] == 115102169482
    assert len({(x['block'], x['context']) for x in d['original_raw_t0_feature_rows']}) == 18
    assert d['t0_investment_genetic_expected_response_signs'] == {
        'toward_decline': 12, 'away_from_decline': 6, 'zero': 0,
    }
    for x in d['original_raw_t0_feature_rows']:
        f = x['time0_only']
        assert f['t0_expected_A_response'] == 0.0
        assert f['A_variance_expressed'] == 0.0
        assert f['A_expected_F1_Mendelian_variance_no_mutation'] == 0.001953125
    assert (d['exploratory_response_order_association']
            ['initial_in_decline_contexts_mean_event_rate']) == 1060 / 1536
    assert (d['exploratory_response_order_association']
            ['initial_against_decline_contexts_mean_event_rate']) == 78 / 768
