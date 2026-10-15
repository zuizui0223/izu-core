"""An absent second response is not the opposite sequence."""
import pytest

from scripts.audit_ecological_event_vs_order_20261015 import (
    BLOCKS, CONTEXTS, classify, pair_counts, source_records, support_status,
)


def ev(a, i):
    return {'A': a, 'I': i, 'category': classify(a, i)}


def test_strict_switch_is_separate_from_loss_of_second_event():
    left = {0: ev(3, 20), 1: ev(20, 3), 2: ev(3, 20)}
    right = {0: ev(20, 3), 1: ev(3, 20), 2: ev(3, None)}
    d = pair_counts(left, right, n=3)
    assert d['strict_A_to_I'] == 1 and d['strict_I_to_A'] == 1
    assert d['both_to_nonboth'] == 1 and d['nonboth_to_both'] == 0
    assert d['I_gained'] == 0 and d['I_lost'] == 1
    assert sum(map(sum, d['transition_matrix'])) == 3


def test_onset_zero_is_not_missing_and_near_ties_are_not_strict_switches():
    d = pair_counts({0: ev(0, 4)}, {0: ev(None, 0)}, n=1)
    assert d['strict_A_to_I'] == d['strict_I_to_A'] == 0
    assert d['A_lost'] == 1 and d['I_lost'] == 0
    assert d['both_to_nonboth'] == 1


def test_all_start_pairing_rejects_missing_or_shifted_replicates():
    with pytest.raises(ValueError, match='replicate'):
        pair_counts({0: ev(1, None)}, {1: ev(1, None)}, n=1)
    with pytest.raises(ValueError, match='replicate'):
        pair_counts({0: ev(1, None)}, {0: ev(1, None)}, n=2)


def test_category_tampering_is_rejected():
    bad = {'A': 2, 'I': None, 'category': 'assurance_first'}
    with pytest.raises(ValueError, match='category'):
        pair_counts({0: bad}, {0: ev(2, None)}, n=1)


def test_support_deficit_timing_is_descriptive_not_prior_failure():
    assert support_status(ev(1, None), {'event_onset': None, 'first_deficit': None}) == 'I_absent_no_deficit'
    assert support_status(ev(1, None), {'event_onset': None, 'first_deficit': 181}) == 'I_absent_deficit_by181'
    assert support_status(ev(1, None), {'event_onset': None, 'first_deficit': 182}) == 'I_absent_deficit_after181'
    assert support_status(ev(1, 0), {'event_onset': 0, 'first_deficit': 90}) == 'I_completed'


def test_joined_event_mismatch_and_invalid_times_fail_closed():
    with pytest.raises(ValueError, match='event mismatch'):
        support_status(ev(1, 0), {'event_onset': None, 'first_deficit': None})
    for bad in [-1, 182, True, 1.5]:
        with pytest.raises(ValueError, match='onset'):
            classify(bad, None)


def test_compact_primary_uses_complete_source_bound_baselines():
    baselines = []
    for b, seed in BLOCKS.items():
        for c, (supply, composition) in enumerate(CONTEXTS):
            for r in range(128):
                baselines.append({'task': dict(block=b, block_seed=seed, context=c,
                                               supply=supply, composition=composition,
                                               replicate=r), 'events': ev(1, 20)})
    assert len(source_records({'cases': 2304}, {'baselines': baselines})) == 2304
    with pytest.raises(ValueError, match='inventory'):
        source_records({'cases': 2304}, {'baselines': baselines[:-1]+baselines[:1]})
