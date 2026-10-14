import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from q3_event_conditions_20261014 import (
    event, support_class, history, restrictions, investment_path,
    refixation, inventory,
)


def test_legacy_threshold_arithmetic():
    boundary = 0.5 - 0.05
    assert event([boundary] * 20, 0.5)['start'] is None
    assert event([np.nextafter(boundary, -np.inf)] * 20, 0.5)['start'] == 0


def test_event_windows_and_history_at_trigger():
    assert event([0.3] * 19, 0.5) == dict(start=None, completion=None, longest=19)
    assert event([0.3] * 20, 0.5) == dict(start=0, completion=19, longest=20)
    path = [0.5] + [0.3] * 200
    assert history(path, 20)['preexisting'] is True
    h = history(path, 19)
    assert h['preexisting'] is False and h['trailing'] == 19
    assert h['native_event'] is True


@pytest.mark.parametrize('baseline,v,expected', [
    (0.53125, 0.625, 'support_excluded'),
    (0.53125, 0.5, 'gain_possible'),
    (0.4609375, 0.375, 'loss_possible'),
    (0.53125, 0.375, 'all_support_eligible'),
])
def test_support_classes(baseline, v, expected):
    assert support_class(baseline, v) == expected


def test_insufficient_remaining_time_and_preexisting_exception():
    p = [0.5] * 190 + [0.3] * 11
    h = history(p, 197)
    assert h['trailing'] == 8 and h['window_excluded']
    assert not h['native_event']
    with pytest.raises(ValueError, match='window'):
        restrictions('loss_possible', h, False, True)
    old = history([0.5] + [0.3] * 200, 197)
    assert old['preexisting'] and not old['window_excluded']
    restrictions('all_support_eligible', old, True, True)


@pytest.mark.parametrize('cls,n,r', [
    ('support_excluded', False, True),
    ('gain_possible', True, False),
    ('loss_possible', False, True),
    ('all_support_eligible', True, False),
])
def test_forbidden_discordances(cls, n, r):
    with pytest.raises(ValueError):
        restrictions(cls, dict(preexisting=False, window_excluded=False), n, r)


def test_preexisting_event_cannot_be_lost():
    with pytest.raises(ValueError, match='preexisting'):
        restrictions('loss_possible', dict(preexisting=True, window_excluded=False), True, False)


def raw(censuses):
    a = np.zeros((sum(len(x) for x in censuses), 3, 2))
    if len(a):
        a[:, 1, :] = np.concatenate(censuses, axis=0)
    return dict(alleles=a, offsets=np.cumsum([0] + [len(x) for x in censuses]))


def test_path_support_occupancy_and_refixation():
    a = raw([[[0.3125, 0.4375]], [[0.3125, 0.3125]], [[0.3125, 0.3125]]])
    means, fixed = investment_path(a, (0.3125, 0.4375), 3)
    assert means.tolist() == [0.375, 0.3125, 0.3125]
    assert refixation(fixed, 5, 0.375, 5)['event_complete_at_refixation'] is True
    assert refixation(fixed, 5, 0.375, 8)['event_complete_at_refixation'] is False
    assert refixation([None, None], 5, 0.375, None)['year'] is None
    with pytest.raises(ValueError, match='absorbing'):
        refixation([None, 0.3125, None], 5, 0.375, None)
    with pytest.raises(ValueError, match='support'):
        investment_path(a, (0.375,), 3)
    with pytest.raises(ValueError, match='occupied'):
        investment_path(raw([np.empty((0, 2))]), None, 1)


def test_inventory_missing_duplicate_and_foreign():
    inventory(['a', 'b'], {'a', 'b'})
    for names in (['a'], ['a', 'a', 'b'], ['a', 'b', 'c']):
        with pytest.raises(ValueError, match='inventory'):
            inventory(names, {'a', 'b'})
