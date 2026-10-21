import numpy as np
import pytest

from scripts.audit_ai_repeatability_causes_20261021 import partition


def test_constant_interior_endpoint_is_not_labelled_fixation():
    r = partition([[.75, .75], [.75, .75]])
    assert r['ss_total'] == 0 and r['within_ss_fraction'] is None
    assert r['identical_contexts'] == 2
    assert r['exact_zero_count'] == r['exact_one_count'] == 0
    assert not any('fixation' in key for key in r)


def test_exact_partition_with_distinct_history_and_repeat_offsets():
    r = partition([[0, 2], [2, 4]])
    assert r['ss_between_history_means'] == 4
    assert r['ss_within_histories'] == 4
    assert r['ss_total'] == 8
    assert r['within_ss_fraction'] == .5
    assert r['within_sample_variance'] == 2


def test_partition_does_not_depend_on_repeat_order():
    x = np.array([[.1, .2, .7], [.3, .4, .9]])
    a, b = partition(x), partition(x[:, ::-1])
    for key in ('ss_total', 'ss_between_history_means', 'ss_within_histories'):
        assert a[key] == pytest.approx(b[key])


@pytest.mark.parametrize('values', [[[1]], [[0, float('nan')], [1, 2]], [1, 2]])
def test_invalid_partition_input_rejected(values):
    with pytest.raises(ValueError):
        partition(values)
