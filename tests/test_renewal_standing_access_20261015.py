"""Saved-state support is neither a mean event nor permanent loss under mutation."""
import numpy as np
import pytest

from scripts.audit_renewal_standing_access_20261015 import summarize


def history(values):
    n = np.array([len(v) for v in values], dtype=np.int64)
    off = np.r_[0, n.cumsum()]
    a = np.full((sum(n), 3, 2), .5)
    for t, v in enumerate(values):
        a[off[t]:off[t+1], 1, :] = np.array(v)[:, None]
    flags = np.zeros_like(a, dtype=bool)
    means = np.array([a[off[t]:off[t+1]].mean(axis=(0, 2))
                      if n[t] else [np.nan]*3 for t in range(len(n))])
    return n, off, a, flags, means


def test_reopening_is_not_a_mean_response_and_variance_is_not_support():
    v = history([[.6, .9], [.72, .9], [.65, .85]])
    v[3][4, 1, :] = True
    d = summarize(*v, mutable=True)
    assert d['first_deficit'] == 1 and d['first_reopening'] == 2
    assert d['event_onset'] is None and d['deficit_censuses'] == 1
    assert d['event_after_reopening'] is False


def test_original_no_mutation_reopening_is_a_hard_error():
    v = history([[.6, .9], [.72, .9], [.65, .85]])
    with pytest.raises(ValueError, match='original support reopened'):
        summarize(*v, mutable=False)


def test_reopening_requires_mutated_threshold_capable_homologs():
    v = history([[.6, .9], [.72, .9], [.65, .85]])
    with pytest.raises(ValueError, match='unflagged reopening'):
        summarize(*v, mutable=True)


def test_event_onset_and_completion_are_distinct():
    d = summarize(*history([[.6, 1.]]+[[.6, .6]]*20), mutable=False)
    assert (d['event_onset'], d['event_completion']) == (1, 20)
    assert d['first_deficit'] is None and d['first_reopening'] is None


def test_extinction_is_missing_support_not_deficit():
    d = summarize(*history([[.6, .9], [], []]), mutable=False)
    assert d['occupied_censuses'] == 1 and d['deficit_censuses'] == 0
    assert not d['occupied_final'] and d['event_onset'] is None


def test_reoccupation_and_mean_drift_reject():
    with pytest.raises(ValueError, match='reoccupied'):
        summarize(*history([[.5], [], [.5]]), mutable=False)
    v = history([[.5], [.5]])
    v[4][1, 1] += .1
    with pytest.raises(ValueError, match='saved means'):
        summarize(*v, mutable=False)


def test_original_floating_predicate_not_rewritten_as_subtracted_target():
    d = summarize(*history([[.5], [.45]]), mutable=False)
    assert d['deficit_censuses'] == int(not (.5 - .45 >= .05)) + 1


def test_event_completed_before_deficit_is_not_a_reopening_benefit():
    v = history([[.6, 1.]]+[[.6, .6]]*20+[[.78], [.65]])
    v[3][-1, 1, :] = True
    d = summarize(*v, mutable=True)
    assert d['event_before_deficit'] and not d['event_after_reopening']
    assert (d['first_deficit'], d['first_reopening']) == (21, 22)
