"""Raw archive/statistical readback, with zero native transitions.

Independent of the producer and of the primary summary implementation. Native
replay receipts are checked against raw inventory; replay is not repeated here.
"""
from collections import Counter
import hashlib
import json
import math
import zipfile

import numpy as np

from q3_futures_contract_20261014 import FIELDS, arrays
from q3_triangle_contract_20261014 import require
from q3_triangle_execution_gate_20261014 import PREFLIGHT_SHA, validate_document
from q3_triangle_io_20261014 import verify_container
from verify_q3_futures_paths_20261014 import validate_layout


def archive_endpoints(original, future, trigger):
    """Separate endpoint algorithm; no shared replay endpoint implementation."""
    require(len(original['offsets']) == 202 and len(future['offsets']) == 202-trigger,
            'archive full-history census counts')
    values = []
    for year in range(201):
        data = original if year < trigger else future
        position = year if year < trigger else year-trigger
        lo, hi = map(int, data['offsets'][position:position+2])
        values.append(None if lo == hi else float(np.mean(data['alleles'][lo:hi, 1, :])))
    a, b = map(int, original['offsets'][:2])
    require(b > a, 'occupied original baseline')
    baseline = float(np.mean(original['alleles'][a:b, 1, :]))
    event = any(all(values[j] is not None and baseline-values[j] >= .05
                    for j in range(start, start+20)) for start in range(182))
    return dict(I=values[200], survived=values[200] is not None, event=event)


def verify_summary(claim, records, cases):
    blocks = ('causal_main', 'causal_confirmation')
    lookup = {c['key']: c for c in cases}
    require(len(cases) == len(lookup) == 64, 'independent original slots')
    expected = {(c['key'], r) for c in cases if c['trigger'] is not None for r in range(144)}
    require(len(records) == len(expected) == 8784 and
            all(type(r['replicate']) is int for r in records) and
            {(r['key'], r['replicate']) for r in records} == expected, 'independent complete inventory')
    patterns = {format(n, '03b'): 0 for n in range(8)}
    counts = {b: {p: 0 for p in 'ABC'} for b in blocks}
    per_state = {c['key']: {n: [] for n in ('D_A', 'D_C', 'G_A', 'G_C')} for c in cases}
    for r in records:
        require(set(r['arms']) == set('ABC'), 'independent arm inventory')
        c = lookup[r['key']]
        for p, a in r['arms'].items():
            require(type(a['survived']) is bool and type(a['event']) is bool and
                    a['survived'] == (a['I'] is not None), 'independent endpoint types')
            if a['survived']:
                w = 1/8 if p == 'C' else 1/16
                require(not isinstance(a['I'], bool) and math.isfinite(a['I']) and
                        c['fixed_I']-w <= a['I'] <= c['fixed_I']+w, 'independent endpoint support')
            counts[c['block']][p] += a['event']
        pattern = ''.join('1' if r['arms'][p]['survived'] else '0' for p in 'ABC')
        patterns[pattern] += 1
        if pattern == '111':
            for p in ('A', 'C'):
                per_state[r['key']]['D_'+p].append(r['arms']['B']['I']-r['arms'][p]['I'])
                per_state[r['key']]['G_'+p].append(int(r['arms'][p]['event'])-int(r['arms']['B']['event']))
    require(claim['triplets'] == 8784 and claim['original_slots'] == 64 and claim['policy_zero_slots'] == 3,
            'independent denominator fields')
    require(claim['original_primary'] == claim['old_confirmation_margin_0_01'] == 'unresolved_unchanged',
            'prior conclusions unchanged')
    require(claim['survival_patterns'] == patterns and claim['raw_event_counts'] == counts,
            'independent survival/event counts')
    for b, n in zip(blocks, (31, 30)):
        rows = [c for c in cases if c['block'] == b]
        require(len(rows) == 32 and sum(c['trigger'] is not None for c in rows) == n,
                'independent original block weights')
    if patterns['111'] != 8784:
        require(claim['decision'] == 'not_evaluable_joint_survival_gate' and claim['blocks'] is None,
                'independent whole-family extinction gate')
    else:
        require(claim['decision'] == 'evaluated_joint_survivor_conditional' and
                claim['interval_family_size'] == 8 and claim['conditional_alpha'] == .05, 'independent family')
        directions = {}
        for b, n in zip(blocks, (31, 30)):
            actual = claim['blocks'][b]
            require(actual['slots'] == 32 and actual['triggered_states'] == n, 'independent block denominators')
            directions[b] = {}
            for contrast, length, margin in [('D_A', .25, .01), ('D_C', .375, .01),
                                             ('G_A', 2, .05), ('G_C', 2, .05)]:
                mean = math.fsum(math.fsum(per_state[c['key']][contrast])/144
                                 for c in cases if c['block'] == b)/32
                width = length*math.sqrt(n*math.log(320)/(288*32*32))
                lo, hi = mean-width, mean+width
                direction = 'positive' if lo > 0 else 'negative' if hi < 0 else 'unresolved'
                practical = ('positive' if lo > margin else 'negative' if hi < -margin else
                             'operationally_equivalent' if -margin <= lo and hi <= margin else 'unresolved')
                got = actual['contrasts'][contrast]
                require(len(got['interval']) == 2, 'two interval endpoints')
                require(all(abs(a-v) <= 1e-14 for a,v in zip(
                    [got['estimate'], got['half_width'], *got['interval']], [mean, width, lo, hi])),
                    'independent estimate/interval')
                require(got['direction'] == direction and got['practical'] == practical and
                        got['operational_margin'] == margin, 'independent classification')
                directions[b][contrast] = direction
        for contrast in directions[blocks[0]]:
            d = {directions[b][contrast] for b in blocks}
            expected_direction = (next(iter(d)) if len(d) == 1 and 'unresolved' not in d else
                                  'opposed' if d == {'positive', 'negative'} else 'unresolved')
            require(claim['directional_replication'][contrast] == expected_direction, 'independent replication')
    return dict(status='INDEPENDENT_SUMMARY_MATCH', triplets=8784, original_slots=64, native_updates=0)


def verify_campaign(rows):
    require(len(rows) == 18 and all(type(r['shard']) is int for r in rows) and
            {r['shard'] for r in rows} == set(range(18)), 'all 18 unique shards')
    require(len({r['run_id'] for r in rows}) == len({r['execution_sha256'] for r in rows}) == 1,
            'single approved run/execution')
    for r in rows:
        require((r['triplets'], r['trajectories'], r['production_updates'], r['replay_updates']) ==
                (488, 1464, 185760, 185760), 'complete per-shard counts')
        require(type(r['fixture_updates']) is int and r['fixture_updates'] >= 0 and
                r['reserved_native_updates'] == 371520+r['fixture_updates'], 'per-shard reserved calls')
    fixtures = sum(r['fixture_updates'] for r in rows)
    require(fixtures <= 32, 'campaign fixture ceiling')
    return dict(status='ALL_SHARDS_ACCOUNTED', shards=18, trajectories=26352, triplets=8784,
                production_updates=3343680, replay_updates=3343680, fixture_updates=fixtures,
                native_updates=6687360+fixtures)


def read_triplet(z, case, replicate, execution_sha, manifest):
    """Read three original-bound raw paths; regenerate only the assigned permutation."""
    original_bytes = z.read('original/'+case['key']+'.npz')
    require(hashlib.sha256(original_bytes).hexdigest() == case['original_npz_sha256'], 'raw original hash')
    original = arrays(original_bytes)
    name = f"triplets/{case['key']}__r{replicate:03d}.json"
    receipt = json.loads(z.read(name))
    require(receipt['key'] == case['key'] and type(receipt['replicate']) is int and
            receipt['replicate'] == replicate and set(receipt['artifacts']) == set('ABC'), 'triplet receipt identity')
    seeds = {}
    for purpose in ('allocation', 'dynamics'):
        text = f"izu-q3-distribution-triangle-v1-20261014\0{case['key']}\0{replicate}\0{purpose}"
        seeds[purpose] = str(int.from_bytes(hashlib.sha256(text.encode()).digest()[:16], 'big'))
    require(case['seeds'][replicate] == dict(replicate=replicate, **seeds), 'raw seed registration')
    permutation = np.random.Generator(np.random.PCG64(int(seeds['allocation']))).permutation(48).tolist()
    require(receipt['permutation'] == permutation, 'raw assigned permutation')
    endpoints = {}
    t = case['trigger'];lo, hi = original['offsets'][t:t+2]
    require(hi-lo == 48 and np.all(original['alleles'][lo:hi, 1] == case['fixed_I']), 'raw fixed initial state')
    for p, count, width in [('A', 24, 1/16), ('B', 12, 1/16), ('C', 3, 1/8)]:
        filename = f"{case['key']}__r{replicate:03d}__{p}.npz"
        path = 'raw/'+filename
        artifact = receipt['artifacts'][p]
        require(artifact == dict(name=filename, sha256=manifest[path], bytes=z.getinfo(path).file_size),
                'raw artifact receipt')
        raw = arrays(z.read(path))
        metadata = dict(key=case['key'], replicate=replicate, arm=p, trigger=t, seeds=seeds,
                        permutation=permutation, artificial_edit=dict(trait='I', carrier_indices=permutation[:count],
                        width=width, historical_mutation_flags_unchanged=True),
                        original_sha256=case['original_npz_sha256'], execution_sha256=execution_sha)
        require(json.loads(str(raw['metadata'])) == metadata, 'raw metadata binding')
        validate_layout(raw, t)
        for field in FIELDS:
            expected = original[field][lo:hi].copy()
            if field == 'alleles':
                expected[permutation[:count], 1] = [case['fixed_I']-width, case['fixed_I']+width]
            require(np.array_equal(raw[field][:48], expected), 'raw original/assignment binding '+field)
        require(np.isin(raw['alleles'][:, 1], [case['fixed_I']-width, case['fixed_I'], case['fixed_I']+width]).all(),
                'raw investment support')
        endpoints[p] = archive_endpoints(original, raw, t)
    require(receipt['arms'] == endpoints, 'raw endpoints disagree with replay receipt')
    require(receipt['native_updates'] == receipt['production_updates'] == receipt['parent_checks'] == 3*(200-t)
            and receipt['state_field_checks'] == 15*(201-t), 'raw replay accounting')
    return dict(key=case['key'], replicate=replicate, arms=endpoints)


def verify_shard(path, plan, execution_sha, run_id, guard):
    manifest = verify_container(path, guard)
    with zipfile.ZipFile(path) as z:
        require(hashlib.sha256(z.read('PREFLIGHT.json')).hexdigest() == PREFLIGHT_SHA, 'archived preflight')
        execution = json.loads(z.read('EXECUTION.json'))
        activation = z.read('ACTIVATION.json')
        require(hashlib.sha256(activation).hexdigest() == execution_sha and
                json.loads(activation) == execution['execution'], 'exact activation bytes')
        require(execution['execution_sha256'] == execution_sha and execution['identity']['run_id'] == run_id,
                'shard execution identity')
        doc = execution['execution'];validate_document(doc)
        shard = execution['shard']
        require(type(shard) is int and 0 <= shard < 18, 'archive shard ID')
        header = json.loads(z.read('SHARD.json'))
        require(header['status'] == 'ALL_1464_PATHS_REPLAYED' and header['shard'] == shard and
                header['run_id'] == run_id and header['execution_sha256'] == execution_sha, 'shard completion header')
        registered = dict(plan['frozen_source_sha256'])
        registered.update({'original/'+c['key']+'.npz': c['original_npz_sha256'] for c in plan['cases']})
        registered['campaign.json'] = plan['campaign_sha256']
        require(all(manifest[n] == h for n,h in registered.items()), 'archived original/source hash binding')
        require(all(manifest['execution_source/'+n] == h for n,h in doc['code_sha256'].items()), 'archived executable hash binding')
        admission = json.loads(z.read('ADMISSION.json'))
        require(admission['extracted_sha256'] == registered and admission['bytecode_extracted'] is False,
                'source admission receipt')
        start = json.loads(z.read('budget/START.json'))
        require(start == dict(shard=shard, execution_sha256=execution_sha, run_id=run_id), 'durable shard start')
        expected = set(registered) | {'execution_source/'+n for n in doc['code_sha256']} | {
            'ADMISSION.json', 'PREFLIGHT.json', 'ACTIVATION.json', 'EXECUTION.json', 'SHARD.json', 'budget/START.json'}
        fixture_updates = 4 if shard == 0 else 0
        if shard == 0:
            expected.update(('FIXTURES.json', 'FIXTURE_RESERVATION.json'))
            fixture = json.loads(z.read('FIXTURES.json'))
            seed = str(int.from_bytes(hashlib.sha256(b'izu-q3-distribution-triangle-v1-20261014\0synthetic-fixture').digest()[:16], 'big'))
            require(fixture == dict(status='PASS', native_updates=4, scientific_trajectories=0, seed=seed,
                                    equal_state_parentage=True, empty_continuation=True), 'native fixture receipt')
            require(json.loads(z.read('FIXTURE_RESERVATION.json')) == dict(native_updates_reserved=4,
                    execution_sha256=execution_sha, run_id=run_id), 'durable fixture reservation')
        rows = []
        for case in plan['cases']:
            if case['trigger'] is None:
                continue
            for r in range(shard*8, (shard+1)*8):
                guard()
                stem = f"{case['key']}__r{r:03d}"
                expected.add('triplets/'+stem+'.json')
                expected.update('raw/'+stem+'__'+p+'.npz' for p in 'ABC')
                claim_name = f"budget/claim-{case['key']}-{r:03d}.json"
                expected.add(claim_name)
                claim = json.loads(z.read(claim_name))
                require(claim == dict(key=case['key'], replicate=r, shard=shard,
                        native_updates_reserved=6*case['remaining_updates'], execution_sha256=execution_sha,
                        run_id=run_id), 'raw durable reservation')
                rows.append(read_triplet(z, case, r, execution_sha, manifest))
        require(set(manifest) == expected and len(rows) == 488, 'exact complete shard members')
        require(header['fixture_updates'] == fixture_updates and header['reserved_native_updates'] == 371520+fixture_updates and
                header['triplets'] == 488 and header['trajectories'] == 1464 and
                header['production_updates'] == header['replay_updates'] == header['parent_checks'] == 185760 and
                header['state_field_checks'] == 15*8*sum(201-c['trigger'] for c in plan['cases'] if c['trigger'] is not None),
                'raw-derived shard totals')
    return header, rows
