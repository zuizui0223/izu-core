"""Three-policy trajectory writer. Only the authorized coordinator may call workers."""
import argparse
import json
from pathlib import Path
import time

import numpy as np

from q3_futures_contract_20261014 import FIELDS, arrays, checked_bytes, load_native
from q3_distribution_triangle_20261014 import construct, POLICIES
from q3_triangle_contract_20261014 import require, seed_for
from q3_triangle_execution_gate_20261014 import authorize, digest


def context(case, out):
    original = arrays(checked_bytes(out/'original'/(case['key']+'.npz'), case['original_npz_sha256']))
    meta = json.loads(str(original['metadata']))
    native = load_native(out/'frozen_source')
    types, _, _, _ = native
    cfg = types.Config.from_dict(meta['config'])
    campaign = json.loads((out/'campaign.json').read_text(encoding='utf-8'))
    optima = campaign['compositions'][meta['task']['composition']]
    visitors = types.VisitorState(np.arange(len(optima), dtype=np.int64), np.asarray(optima),
                                 np.full(len(optima), .2), np.ones(len(optima)))
    lo, hi = original['offsets'][case['trigger']:case['trigger']+2]
    state = {k: original[k][lo:hi].copy() for k in FIELDS}
    require(len(state['ids']) == 48 and np.all(state['alleles'][:, 1] == case['fixed_I']),
            'original fixed state binding')
    return state, cfg, visitors, native


def produce_triplet(case, replicate, out, execution_sha, deadline):
    """Private worker: coordinator reserves this triplet before submission."""
    out = Path(out)
    names = {p: f"{case['key']}__r{replicate:03d}__{p}.npz" for p in 'ABC'}
    if any((out/'raw'/name).exists() for name in names.values()):
        raise FileExistsError('partial or complete triplet already exists; no retry')
    seeds = {p: seed_for(case['key'], replicate, p) for p in ('allocation', 'dynamics')}
    require(case['seeds'][replicate] == dict(replicate=replicate,
            **{p: str(v) for p, v in seeds.items()}), 'registered seed identity')
    require(time.monotonic() < deadline and not (out/'ABORT').exists(), 'deadline/abort')
    initial, cfg, visitors, native = context(case, out)
    types, pop, repro, randomness = native
    permutation = np.random.Generator(np.random.PCG64(seeds['allocation'])).permutation(48).tolist()
    saved = {}
    for arm in 'ABC':
        edited = construct(initial, arm, permutation[:POLICIES[arm]['heterozygotes']])
        state = types.PlantState(**edited)
        empty = types.PlantState(**{k: edited[k][:0].copy() for k in FIELDS})
        streams = {n: randomness.stream(seeds['dynamics'], n, 0) for n in randomness.STREAM_IDS}
        snapshots, parents = [], []
        for year in range(case['trigger'], 201):
            require(time.monotonic() < deadline and not (out/'ABORT').exists(), 'deadline/abort')
            snapshots.append({k: getattr(state, k).copy() for k in FIELDS})
            if year == 200:
                break
            state, info = pop.advance(state, repro.reproduce(state, visitors, cfg), empty, cfg,
                                      streams, year=year, mutation_traits=(False, False, True))
            parents.append(info['parentage'].copy())
        metadata = dict(key=case['key'], replicate=replicate, arm=arm, trigger=case['trigger'],
                        seeds={p: str(v) for p, v in seeds.items()}, permutation=permutation,
                        artificial_edit=dict(trait='I', carrier_indices=permutation[:POLICIES[arm]['heterozygotes']],
                                             width=POLICIES[arm]['width'], historical_mutation_flags_unchanged=True),
                        original_sha256=case['original_npz_sha256'], execution_sha256=execution_sha)
        result = {k: np.concatenate([s[k] for s in snapshots]) for k in FIELDS}
        result.update(offsets=np.r_[0, np.cumsum([len(s['ids']) for s in snapshots])],
                      parent_offsets=np.r_[0, np.cumsum([len(p) for p in parents])].astype(np.int64),
                      parentage=np.concatenate(parents) if parents else np.empty((0, 3), dtype=np.int64),
                      metadata=np.array(json.dumps(metadata, sort_keys=True)))
        path = out/'raw'/names[arm]
        with path.open('xb') as handle:
            np.savez_compressed(handle, **result)
        t = case['remaining_updates']
        require(path.stat().st_size <= (t+1)*5664+t*1152+131072, 'per-path storage ceiling')
        saved[arm] = dict(name=names[arm], sha256=digest(path), bytes=path.stat().st_size)
    return saved


def main(argv=None):
    parser = argparse.ArgumentParser()
    for name in ('repo', 'out', 'archive'):
        parser.add_argument('--'+name, type=Path, required=True)
    parser.add_argument('--shard', type=int, required=True)
    args = parser.parse_args(argv)
    authorize(args.repo)
    # Task 3 adds source admission, durable reservations, worker dispatch and
    # publication. Explicitly inert until the complete campaign is reviewed.
    raise RuntimeError('HOLD: shard coordinator and publication are not implemented')


if __name__ == '__main__':
    main()
