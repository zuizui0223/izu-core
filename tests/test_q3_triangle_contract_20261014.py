import copy
import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from q3_triangle_contract_20261014 import seed_for, build_plan, summarize, R, classify


def cases():
    # Synthetic trigger schedule with the frozen total remaining time, no outcomes.
    rows = []
    for block, triggers in [('causal_main', 31), ('causal_confirmation', 30)]:
        for i in range(32):
            t = 73 if i < triggers else None
            rows.append(dict(key=f'{block}_{i}', block=block, trigger=t, fixed_I=0.5 if t is not None else None,
                             remaining_updates=0 if t is None else 200-t))
    rows[0]['trigger'] = 80
    rows[0]['remaining_updates'] = 120
    return rows


def records(cs):
    return [dict(key=c['key'], replicate=r,
                 arms={p: dict(I=0.5, survived=True, event=False) for p in 'ABC'})
            for c in cs if c['trigger'] is not None for r in range(R)]


def test_seeds_are_stable_separate_and_reject_invalid_purpose():
    assert seed_for('x', 0, 'allocation') == seed_for('x', 0, 'allocation')
    assert len({seed_for('x', r, p) for r in range(R) for p in ('allocation', 'dynamics')}) == 2*R
    assert seed_for('x', 0, 'allocation') != seed_for('y', 0, 'allocation')
    for r, p in [(-1, 'allocation'), (R, 'allocation'), (0, 'other')]:
        with pytest.raises(ValueError):
            seed_for('x', r, p)


def test_plan_exact_counts_bounds_and_full_shard_coverage():
    p = build_plan(cases())
    assert not p['approved']
    assert p['new_trajectories'] == 26352
    assert p['triplets'] == 8784
    assert p['production_updates'] == 3343680
    assert p['max_native_updates'] == 6687392
    assert p['maximum_saved_censuses'] == 3370032
    assert p['archive_bound_per_shard'] == 1616530176
    assert p['remote_two_copy_bound'] == 58195086336
    assert p['R_min_terminal'] == 123 and p['R_min_event'] == 140
    assert [r for sh in p['shards'] for r in sh['replicates']] == list(range(144))
    assert p['local_reservation_per_shard'] < 6*1024**3
    assert p['remote_two_copy_bound'] < p['max_remote_bytes']
    assert p['interval_half_widths']['causal_main']['D_C'] < 0.01
    assert p['interval_half_widths']['causal_main']['G_C'] < 0.05


def test_zero_effect_equivalence_preserves_64_slot_weights():
    cs = cases()
    result = summarize(records(cs), cs)
    assert result['decision'] == 'evaluated_joint_survivor_conditional'
    assert result['policy_zero_slots'] == 3
    for b in result['blocks'].values():
        assert b['slots'] == 32
        for item in b['contrasts'].values():
            assert item['estimate'] == 0
            assert item['direction'] == 'unresolved'
            assert item['practical'] == 'operationally_equivalent'


def test_single_state_effect_is_weighted_by_original_slots():
    cs = cases()
    rr = records(cs)
    for row in rr:
        if row['key'] == cs[0]['key']:
            row['arms']['A']['I'] = 0.4375
            row['arms']['A']['event'] = True
    result = summarize(rr, cs)
    cc = result['blocks']['causal_main']['contrasts']
    assert cc['D_A']['estimate'] == 0.0625/32
    assert cc['G_A']['estimate'] == 1/32


@pytest.mark.parametrize('arm,pattern', [('A', '011'), ('B', '101'), ('C', '110')])
def test_extinction_retained_with_whole_family_not_evaluable(arm, pattern):
    cs = cases()
    rr = records(cs)
    rr[0]['arms'][arm].update(I=None, survived=False, event=True)
    result = summarize(rr, cs)
    assert result['decision'] == 'not_evaluable_joint_survival_gate'
    assert result['blocks'] is None
    assert result['survival_patterns'][pattern] == 1
    assert result['raw_event_counts']['causal_main'][arm] == 1


def test_old_seed_collision_fails_before_any_registration():
    cs = cases()
    cs[0]['pair_seeds'] = [str(seed_for(cs[0]['key'], 0, 'allocation'))]
    with pytest.raises(ValueError, match='reused'):
        build_plan(cs)


@pytest.mark.parametrize('defect', ['missing', 'duplicate', 'foreign', 'support', 'survival', 'event', 'replicate_type'])
def test_invalid_triplets_rejected(defect):
    cs = cases()
    rr = records(cs)
    if defect == 'missing': rr.pop()
    elif defect == 'duplicate': rr[-1] = copy.deepcopy(rr[0])
    elif defect == 'foreign': rr[0]['key'] = 'foreign'
    elif defect == 'support': rr[0]['arms']['C']['I'] = 0.9
    elif defect == 'survival': rr[0]['arms']['A']['I'] = None
    elif defect == 'event': rr[0]['arms']['A']['event'] = 1
    elif defect == 'replicate_type': rr[1]['replicate'] = True
    with pytest.raises(ValueError):
        summarize(rr, cs)


def test_classification_boundaries():
    assert classify(-0.01, 0.01, 0.01)['practical'] == 'operationally_equivalent'
    assert classify(0.01, 0.02, 0.01)['practical'] == 'unresolved'
    assert classify(0.0, 0.01, 0.01)['direction'] == 'unresolved'
    assert classify(-0.02, -0.011, 0.01)['practical'] == 'negative'


def test_opposed_blocks_remain_opposed_without_pooling():
    cs = cases()
    rr = records(cs)
    blocks = {c['key']: c['block'] for c in cs}
    for row in rr:
        main = blocks[row['key']] == 'causal_main'
        row['arms']['A'].update(I=0.4375 if main else 0.5625, event=main)
        row['arms']['B']['event'] = not main
    result = summarize(rr, cs)
    assert result['directional_replication']['D_A'] == 'opposed'
    assert result['directional_replication']['G_A'] == 'opposed'
