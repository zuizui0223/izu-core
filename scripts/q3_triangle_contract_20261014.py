"""Pure planning and conditional readout for Q3; no RNG or native imports."""
from collections import Counter
import hashlib
import math

R = 144
SHARD_SIZE = 8
NAMESPACE = 'izu-q3-distribution-triangle-v1-20261014'
BLOCKS = ('causal_main', 'causal_confirmation')
WIDTHS = dict(A=1/16, B=1/16, C=1/8)
RANGES = dict(D_A=1/4, D_C=3/8, G_A=2, G_C=2)
MARGINS = dict(D_A=0.01, D_C=0.01, G_A=0.05, G_C=0.05)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def seed_for(key, replicate, purpose):
    require(isinstance(key, str) and key and '\0' not in key, 'seed key')
    require(type(replicate) is int and 0 <= replicate < R, 'replicate range')
    require(purpose in ('allocation', 'dynamics'), 'seed purpose')
    value = f'{NAMESPACE}\0{key}\0{replicate}\0{purpose}'.encode('utf-8')
    return int.from_bytes(hashlib.sha256(value).digest()[:16], 'big')


def validate_cases(cases):
    require(len(cases) == 64 and len({c['key'] for c in cases}) == 64, '64 unique original slots')
    for block, expected in zip(BLOCKS, (31, 30)):
        rows = [c for c in cases if c['block'] == block]
        require(len(rows) == 32 and sum(c['trigger'] is not None for c in rows) == expected, 'block inventory')
    for c in cases:
        t = c['trigger']
        if t is None:
            require(c['remaining_updates'] == 0 and c['fixed_I'] is None, 'nontrigger zero slot')
        else:
            require(type(t) is int and 0 <= t <= 200 and c['remaining_updates'] == 200-t, 'trigger schedule')
            require(math.isfinite(c['fixed_I']) and 1/8 <= c['fixed_I'] <= 7/8, 'admitted investment support')
    require(sum(c['remaining_updates'] for c in cases) == 7740, 'frozen remaining update total')


def half_width(triggered, contrast):
    return RANGES[contrast]*math.sqrt(triggered*math.log(320)/(2*R*32**2))


def build_plan(cases):
    validate_cases(cases)
    triggered = [c for c in cases if c['trigger'] is not None]
    source_seeds = {str(s) for c in cases for s in c.get('pair_seeds', [])}
    planned = []
    seen = set()
    for c in cases:
        item = {k: c[k] for k in ('key', 'block', 'trigger', 'remaining_updates', 'fixed_I')}
        if 'original_npz_sha256' in c:
            item['original_npz_sha256'] = c['original_npz_sha256']
        item['seeds'] = []
        if c['trigger'] is not None:
            for r in range(R):
                seeds = {p: str(seed_for(c['key'], r, p)) for p in ('allocation', 'dynamics')}
                for s in seeds.values():
                    require(s not in seen and s not in source_seeds, 'reused or duplicate seed')
                    seen.add(s)
                item['seeds'].append(dict(replicate=r, **seeds))
        planned.append(item)
    raw = sum(3*SHARD_SIZE*((201-c['trigger'])*5664+c['remaining_updates']*1152+131072) for c in triggered)
    receipts = len(triggered)*SHARD_SIZE*32768
    archive_bound = raw+receipts+128*1024**2
    shards = [dict(shard=s, replicates=list(range(s*SHARD_SIZE, (s+1)*SHARD_SIZE)),
                   trajectories=len(triggered)*SHARD_SIZE*3, triplets=len(triggered)*SHARD_SIZE,
                   production_updates=3*SHARD_SIZE*7740, replay_updates=3*SHARD_SIZE*7740)
              for s in range(R//SHARD_SIZE)]
    minimum_terminal = math.ceil(31*(3/8)**2*math.log(320)/(2*32**2*0.01**2))
    minimum_event = math.ceil(31*2**2*math.log(320)/(2*32**2*0.05**2))
    require(R == SHARD_SIZE*math.ceil(max(minimum_terminal, minimum_event)/SHARD_SIZE), 'minimal precision allocation')
    plan = dict(approved=False, status='PROSPECTIVE_PREFLIGHT_NO_BIOLOGY', namespace=NAMESPACE,
        original_slots=64, triggered_states=61, policy_zero_slots=3, replicates_per_state=R,
        triplets=61*R, new_trajectories=61*R*3, production_updates=3*R*7740,
        replay_updates=3*R*7740, max_fixture_updates=32, max_native_updates=6*R*7740+32,
        maximum_saved_censuses=3*R*(7740+61),
        R_min_terminal=minimum_terminal, R_min_event=minimum_event,
        interval_family_size=8, conditional_alpha=0.05, operational_margins=MARGINS.copy(),
        interval_half_widths={b: {k: half_width(t, k) for k in RANGES} for b, t in zip(BLOCKS, (31, 30))},
        archive_bound_per_shard=archive_bound, remote_two_copy_bound=2*len(shards)*archive_bound,
        local_reservation_per_shard=2*archive_bound+410326692+512*1024**2,
        minimum_free_local_bytes=6*1024**3, max_remote_bytes=64*1024**3,
        max_hosted_runner_minutes=len(shards)*15+30, max_parallel_shards=1, native_workers=2,
        python='3.11.14', numpy='2.2.6', cases=planned, shards=shards,
        new_random_draws=0, native_updates_during_preflight=0)
    require(plan['local_reservation_per_shard'] < plan['minimum_free_local_bytes'], 'local reservation')
    require(plan['remote_two_copy_bound'] < plan['max_remote_bytes'], 'remote reservation')
    require(archive_bound < 2*1024**3, 'shard archive bound')
    return plan


def classify(lo, hi, margin):
    direction = 'positive' if lo > 0 else 'negative' if hi < 0 else 'unresolved'
    practical = ('positive' if lo > margin else 'negative' if hi < -margin else
                 'operationally_equivalent' if lo >= -margin and hi <= margin else 'unresolved')
    return dict(direction=direction, practical=practical)


def summarize(records, cases):
    validate_cases(cases)
    lookup = {c['key']: c for c in cases}
    expected = {(c['key'], r) for c in cases if c['trigger'] is not None for r in range(R)}
    require(all(type(r['replicate']) is int and isinstance(r['key'], str) for r in records), 'triplet identity types')
    ids = [(r['key'], r['replicate']) for r in records]
    require(len(ids) == len(expected) and len(set(ids)) == len(ids) and set(ids) == expected, 'complete unique triplet inventory')
    survival = {format(i, '03b'): 0 for i in range(8)}
    event_counts = {b: {p: 0 for p in 'ABC'} for b in BLOCKS}
    differences = {c['key']: {k: [] for k in RANGES} for c in cases}
    for row in records:
        case = lookup[row['key']]
        arms = row['arms']
        require(set(arms) == set('ABC'), 'exact three arms')
        for p, arm in arms.items():
            value, alive = arm['I'], arm['survived']
            require(type(alive) is bool and alive == (value is not None), 'survival/mean consistency')
            require(type(arm['event']) is bool, 'boolean historical event')
            if alive:
                require(isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value), 'finite terminal I')
                v, w = case['fixed_I'], WIDTHS[p]
                require(v-w <= value <= v+w, 'terminal investment support')
            event_counts[case['block']][p] += arm['event']
        pattern = ''.join(str(int(arms[p]['survived'])) for p in 'ABC')
        survival[pattern] += 1
        if pattern == '111':
            dst = differences[row['key']]
            for p in ('A', 'C'):
                dst['D_'+p].append(arms['B']['I']-arms[p]['I'])
                dst['G_'+p].append(int(arms[p]['event'])-int(arms['B']['event']))
    result = dict(triplets=len(records), original_slots=64, policy_zero_slots=3,
        target='fixed_state_allocation_averaged_coupling_specific_joint_three_arm_survivor_conditional',
        survival_patterns=survival, raw_event_counts=event_counts,
        original_primary='unresolved_unchanged', old_confirmation_margin_0_01='unresolved_unchanged',
        blocks=None)
    if survival['111'] != len(records):
        result['decision'] = 'not_evaluable_joint_survival_gate'
        return result
    blocks = {}
    for block in BLOCKS:
        rows = [c for c in cases if c['block'] == block]
        n_triggered = sum(c['trigger'] is not None for c in rows)
        contrasts = {}
        for name in RANGES:
            state_means = [math.fsum(differences[c['key']][name])/R if c['trigger'] is not None else 0.0 for c in rows]
            estimate = math.fsum(state_means)/32
            half = half_width(n_triggered, name)
            lo, hi = estimate-half, estimate+half
            contrasts[name] = dict(estimate=estimate, half_width=half, interval=[lo, hi],
                                   operational_margin=MARGINS[name], **classify(lo, hi, MARGINS[name]))
        blocks[block] = dict(slots=32, triggered_states=n_triggered, contrasts=contrasts)
    replication = {}
    for name in RANGES:
        directions = {blocks[b]['contrasts'][name]['direction'] for b in BLOCKS}
        replication[name] = (next(iter(directions)) if len(directions) == 1 and 'unresolved' not in directions else
                             'opposed' if directions == {'positive', 'negative'} else 'unresolved')
    result.update(decision='evaluated_joint_survivor_conditional', blocks=blocks,
                  directional_replication=replication, interval_family_size=8, conditional_alpha=0.05)
    return result
