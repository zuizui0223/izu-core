"""Independent assignment/replay implementation; never imports triangle producer."""
import hashlib
import json
from pathlib import Path
import time

import numpy as np

from q3_futures_contract_20261014 import FIELDS, arrays, checked_bytes, load_native, require
from verify_q3_futures_paths_20261014 import validate_layout


def read_endpoints(original, future, trigger):
    """Full original prefix plus policy future; literal archived threshold."""
    values = []
    for data, stop in ((original, trigger), (future, 201-trigger)):
        for j in range(stop):
            lo, hi = data['offsets'][j:j+2]
            values.append(float(data['alleles'][lo:hi, 1].mean()) if hi > lo else None)
    require(len(values) == 201 and values[0] is not None, 'full history')
    a, b = original['offsets'][:2]
    baseline = float(original['alleles'][a:b, 1].mean())
    streak, event = 0, False
    for value in values:
        streak = streak+1 if value is not None and baseline-value >= .05 else 0
        event = event or streak >= 20
    return dict(I=values[-1], survived=values[-1] is not None, event=event)


def verify_triplet(case, replicate, out, execution_sha, deadline, saved):
    out = Path(out)
    original = arrays(checked_bytes(out/'original'/(case['key']+'.npz'), case['original_npz_sha256']))
    meta = json.loads(str(original['metadata']))
    types, pop, repro, randomness = load_native(out/'frozen_source')
    cfg = types.Config.from_dict(meta['config'])
    optima = json.loads((out/'campaign.json').read_text(encoding='utf-8'))['compositions'][meta['task']['composition']]
    visitors = types.VisitorState(np.arange(len(optima), dtype=np.int64), np.asarray(optima),
                                 np.full(len(optima), .2), np.ones(len(optima)))
    require(type(replicate) is int and 0 <= replicate < 144, 'independent replicate')
    seeds = {}
    for purpose in ('allocation', 'dynamics'):
        text = f"izu-q3-distribution-triangle-v1-20261014\0{case['key']}\0{replicate}\0{purpose}"
        seeds[purpose] = int.from_bytes(hashlib.sha256(text.encode('utf-8')).digest()[:16], 'big')
    require(case['seeds'][replicate] == dict(replicate=replicate, **{p: str(s) for p,s in seeds.items()}),
            'independent registered seeds')
    permutation = np.random.Generator(np.random.PCG64(seeds['allocation'])).permutation(48).tolist()
    trigger = case['trigger']
    lo, hi = original['offsets'][trigger:trigger+2]
    require(hi-lo == 48 and np.all(original['alleles'][lo:hi, 1] == case['fixed_I']), 'fixed original')
    require(set(saved) == set('ABC'), 'exact arm inventory')
    result = dict(key=case['key'], replicate=replicate, arms={}, permutation=permutation,
                  native_updates=0, state_field_checks=0, parent_checks=0, artifacts=saved)
    for arm, count, width in [('A', 24, 1/16), ('B', 12, 1/16), ('C', 3, 1/8)]:
        name = f"{case['key']}__r{replicate:03d}__{arm}.npz"
        require(saved[arm]['name'] == name, 'raw name identity')
        path = out/'raw'/name
        require(path.stat().st_size == saved[arm]['bytes'], 'raw byte count')
        raw = arrays(checked_bytes(path, saved[arm]['sha256']))
        expected_meta = dict(key=case['key'], replicate=replicate, arm=arm, trigger=trigger,
                             seeds={p: str(v) for p,v in seeds.items()}, permutation=permutation,
                             artificial_edit=dict(trait='I', carrier_indices=permutation[:count], width=width,
                                                  historical_mutation_flags_unchanged=True),
                             original_sha256=case['original_npz_sha256'], execution_sha256=execution_sha)
        require(json.loads(str(raw['metadata'])) == expected_meta, 'raw metadata identity')
        validate_layout(raw, trigger)
        fields = {k: original[k][lo:hi].copy() for k in FIELDS}
        v = float(fields['alleles'][0, 1, 0])
        fields['alleles'][permutation[:count], 1, :] = [v-width, v+width]
        state = types.PlantState(**fields)
        empty = types.PlantState(**{k: fields[k][:0].copy() for k in FIELDS})
        streams = {n: randomness.stream(seeds['dynamics'], n, 0) for n in randomness.STREAM_IDS}
        for j, year in enumerate(range(trigger, 201)):
            require(time.monotonic() < deadline and not (out/'ABORT').exists(), 'deadline/abort')
            a, b = raw['offsets'][j:j+2]
            for field in FIELDS:
                require(np.array_equal(getattr(state, field), raw[field][a:b]), 'independent state replay '+field)
                result['state_field_checks'] += 1
            require(np.isin(raw['alleles'][a:b, 1], [v-width, v, v+width]).all(), 'policy I support')
            if year == 200:
                break
            state, info = pop.advance(state, repro.reproduce(state, visitors, cfg), empty, cfg, streams,
                                      year=year, mutation_traits=(False, False, True))
            p, q = raw['parent_offsets'][j:j+2]
            require(np.array_equal(info['parentage'], raw['parentage'][p:q]), 'independent parent replay')
            result['native_updates'] += 1
            result['parent_checks'] += 1
        result['arms'][arm] = read_endpoints(original, raw, trigger)
    return result
