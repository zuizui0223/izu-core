"""Cross-platform interval arithmetic must not mask biological differences."""
import copy

import pytest

from scripts.summarize_readaptation_results_20261019 import compare_readback


def records():
    return {'groups': [{'occupancy': {'count': 7, 'denominator': 32,
        'interval_95': [0.09277153228471931, 0.39972826371210757]},
        'endpoints_by_repeat': [[0.5, 0.625, 0.75]]}]}


def test_observed_cross_platform_beta_roundoff_is_recorded():
    original = records()
    local = copy.deepcopy(original)
    local['groups'][0]['occupancy']['interval_95'] = [0.09277153228471932, 0.39972826371210746]
    differences = compare_readback(local, original)
    assert len(differences) == 2
    assert all(d['path'].startswith('/groups/0/occupancy/interval_95/') for d in differences)


@pytest.mark.parametrize('field,value', [('count', 8), ('denominator', 33)])
def test_counts_are_never_tolerated(field, value):
    original = records()
    local = copy.deepcopy(original)
    local['groups'][0]['occupancy'][field] = value
    with pytest.raises(ValueError):
        compare_readback(local, original)


def test_even_tiny_trait_change_is_not_an_interval_roundoff():
    original = records()
    local = copy.deepcopy(original)
    local['groups'][0]['endpoints_by_repeat'][0][1] += 1e-15
    with pytest.raises(ValueError):
        compare_readback(local, original)


def test_large_interval_difference_and_missing_records_fail():
    original = records()
    local = copy.deepcopy(original)
    local['groups'][0]['occupancy']['interval_95'][0] += 1e-8
    with pytest.raises(ValueError):
        compare_readback(local, original)
    with pytest.raises(ValueError):
        compare_readback({'groups': []}, original)


def test_json_types_are_exact_even_when_python_values_compare_equal():
    with pytest.raises(ValueError):
        compare_readback({'occupied': True}, {'occupied': 1})
    with pytest.raises(ValueError):
        compare_readback({'count': 7.0}, {'count': 7})


def test_exact_probability_boundaries_cannot_change():
    original = records()
    original['groups'][0]['occupancy']['interval_95'] = [0.0, 1.0]
    for i, value in ((0, 1e-15), (1, 1.0-1e-15)):
        local = copy.deepcopy(original)
        local['groups'][0]['occupancy']['interval_95'][i] = value
        with pytest.raises(ValueError):
            compare_readback(local, original)
