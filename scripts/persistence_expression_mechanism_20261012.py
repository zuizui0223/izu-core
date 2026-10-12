"""Prospectively fixed expression interventions; native inheritance unchanged."""
from __future__ import annotations
import argparse
from dataclasses import replace
import hashlib
import io
import json
from pathlib import Path
import subprocess
import zipfile
import numpy as np

from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.model3_island.types import Config, PlantState, VisitorState
from scripts.model3_island.population import advance, subset
from scripts.model3_island.randomness import stream, STREAM_IDS

POLICIES = ('native', 'A_fixed', 'I_fixed', 'AI_fixed', 'MAI_fixed')
FIELDS = ('alleles', 'allele_origin', 'mutation_flags', 'ids', 'birth_years')
ORIGINS = ('A_access_first', 'I_access_first')
BLOCKS = ('main', 'confirmation')
TARGETS = (1.05, 1.5)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def expression_state(state, policy):
    if policy not in POLICIES:
        raise ValueError('unregistered expression policy')
    if policy == 'native':
        return state
    loci = {'A_fixed': (2,), 'I_fixed': (1,), 'AI_fixed': (1, 2), 'MAI_fixed': (0, 1, 2)}[policy]
    alleles = state.alleles.copy()
    alleles[:, loci, :] = .5
    return replace(state, alleles=alleles)


def expression_ledger(state, visitors, config, policy):
    if config.assurance_mode != 'evolving':
        raise ValueError('expression assay requires native genotype-read mode')
    return reproduce_kb(expression_state(state, policy), visitors, config,
                        background_denominator_capacity=48)


def trajectory(initial, visitors, config, master_seed, policy, *, horizon=200):
    if policy not in POLICIES or type(horizon) is not int or horizon < 1:
        raise ValueError('invalid trajectory request')
    streams = {name: stream(master_seed, name, 0) for name in STREAM_IDS}
    state = initial
    empty = subset(initial, np.empty(0, dtype=int))
    arrays = {f: [] for f in FIELDS}
    population, means, diagnostics, parents = [], [], [], []
    offsets = [0]
    for t in range(horizon + 1):
        n = len(state.ids)
        population.append(n)
        offsets.append(offsets[-1] + n)
        means.append(state.alleles.mean(axis=(0, 2)) if n else np.full(3, np.nan))
        for f in FIELDS:
            arrays[f].append(getattr(state, f).copy())
        if t == horizon:
            break
        ledger = expression_ledger(state, visitors, config, policy)
        state, info = advance(state, ledger, empty, config, streams, year=200 + t,
                              mutation_traits=(False, True, True))
        parents.append(info['parentage'])
        diagnostics.append([ledger.maternal.sum(), ledger.outcross.sum(), ledger.self_raw.sum(),
                            ledger.self_viable.sum(), ledger.ovules.sum(), ledger.exported.sum(),
                            ledger.delivered.sum(), info['resident_potential'], info['resident_recruits'],
                            info['resident_selfed_recruits'], info['resident_outcross_recruits']])
    result = {f: np.concatenate(arrays[f]) for f in FIELDS}
    result.update(population=np.array(population), offsets=np.array(offsets), means=np.array(means),
                  diagnostics=np.array(diagnostics), parentage=np.concatenate(parents))
    assert np.array_equal(np.diff(result['offsets']), result['population'])
    assert result['offsets'][-1] == len(result['alleles'])
    assert len(result['parentage']) == sum(result['population'][1:])
    np.testing.assert_allclose(result['diagnostics'][:, 0], result['diagnostics'][:, 1] +
                               result['diagnostics'][:, 3], atol=1e-10, rtol=0)
    return result


def tasks():
    return [dict(block=b, replicate=r, origin=o, target=t, policy=p)
            for b in BLOCKS for r in range(512) for o in ORIGINS for t in TARGETS for p in POLICIES]


def case_key(task):
    return digest(json.dumps(task, sort_keys=True).encode())[:24]


def shard_for(task):
    return (BLOCKS.index(task['block']) * 512 + task['replicate']) % 16


def future_seed(task):
    original = dict(study='history', block=task['block'], replicate=task['replicate'])
    return int.from_bytes(hashlib.sha256(('resolution-v1-20261011:challenge' +
                                         json.dumps(original, sort_keys=True)).encode()).digest()[:16], 'big')


def paired_difference(first, second):
    x, y = np.asarray(first, float), np.asarray(second, float)
    if x.shape != y.shape or x.ndim != 1 or not len(x) or not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError('all-start outcome pairs required')
    return float((x - y).mean())


def read_inputs(path, expected_sha):
    raw = Path(path).read_bytes()
    if digest(raw) != expected_sha:
        raise ValueError('input digest mismatch')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        if sorted(z.namelist()) != ['baselines.npz', 'manifest.json', 'states.npz']:
            raise ValueError('input inventory mismatch')
        if sum(i.file_size for i in z.infolist()) > 512 * 1024**2:
            raise ValueError('input expansion limit')
        manifest = json.loads(z.read('manifest.json'))
        for name, h in manifest['member_sha256'].items():
            if digest(z.read(name)) != h:
                raise ValueError('input member drift')
        with np.load(io.BytesIO(z.read('states.npz')), allow_pickle=False) as a:
            states = {k: a[k].copy() for k in a.files}
        with np.load(io.BytesIO(z.read('baselines.npz')), allow_pickle=False) as a:
            baselines = {k: a[k].copy() for k in a.files}
    if manifest['schema'] != 'persistence_mechanism_inputs_v1' or len(manifest['states']) != 2048:
        raise ValueError('input schema or cohort size')
    root = Path(__file__).resolve().parents[1]
    for name, h in manifest['normalized_biology_sha256'].items():
        if digest((root / name).read_text(encoding='utf-8').encode()) != h:
            raise ValueError('native biology source drift: ' + name)
    return manifest, states, baselines


def census(trace, t):
    lo, hi = trace['offsets'][t:t + 2]
    return PlantState(**{f: trace[f][lo:hi].copy() for f in FIELDS})


def verify_native(trace, expected, index):
    np.testing.assert_array_equal(trace['population'], expected['population'][index])
    np.testing.assert_allclose(trace['means'], expected['means'][index], atol=1e-12, rtol=0, equal_nan=True)
    np.testing.assert_allclose(trace['diagnostics'], expected['diagnostics'][index], atol=1e-12, rtol=0)
    final = census(trace, 200)
    n = len(final.ids)
    for f in FIELDS:
        ref = expected['final_' + f][index, :n]
        if f == 'alleles':
            np.testing.assert_allclose(getattr(final, f), ref, atol=1e-12, rtol=0)
        else:
            np.testing.assert_array_equal(getattr(final, f), ref)


def run_shard(path, sha, shard, output, *, technical=False):
    if type(shard) is not int or shard not in range(16):
        raise ValueError('unregistered shard')
    manifest, states, expected = read_inputs(path, sha)
    lookup = {(r['block'], r['replicate'], r['origin']): i for i, r in enumerate(manifest['states'])}
    if len(lookup) != 2048:
        raise ValueError('duplicate input states')
    config_by_target = {float(t): Config.from_dict(c) for t, c in manifest['configs'].items()}
    visitors = VisitorState(np.arange(4), np.full(4, .5), np.full(4, .2), np.ones(4))
    selected = [t for t in tasks() if shard_for(t) == shard]
    if technical:
        selected = [t for t in selected if t['block'] == 'main' and t['replicate'] == 0
                    and t['policy'] in ('native', 'MAI_fixed')]
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    records = []
    native_checks = 0
    for t in selected:
        ix = lookup[(t['block'], t['replicate'], t['origin'])]
        s = PlantState(**{f: states[f][ix].copy() for f in FIELDS})
        c = config_by_target[t['target']]
        trace = trajectory(s, visitors, c, future_seed(t), t['policy'])
        bi = ix * 2 + TARGETS.index(t['target'])
        if t['policy'] == 'native':
            verify_native(trace, expected, bi)
            native_checks += 1
        key = case_key(t)
        dest = output / (key + '.npz')
        meta = dict(task=t, input_sha256=sha, config=manifest['configs'][str(t['target'])])
        if dest.exists():
            raise ValueError('refuse output overwrite')
        with dest.open('xb') as f:
            np.savez_compressed(f, metadata=np.array(json.dumps(meta, sort_keys=True)), **trace)
        archive_sha = digest(dest.read_bytes())
        rec = dict(task=t, archive=dest.name, sha256=archive_sha,
                   terminal_occupied=bool(trace['population'][-1]),
                   occupied_fraction=float((trace['population'][1:] > 0).mean()),
                   viable_self=float(trace['diagnostics'][:, 3].sum()),
                   viable_outcross=float(trace['diagnostics'][:, 1].sum()))
        # Immediate ledger is a descriptive mechanism assay, not another trajectory outcome.
        l = expression_ledger(s, visitors, c, t['policy'])
        rec['immediate'] = dict(viable_self=float(l.self_viable.sum()),
                                viable_outcross=float(l.outcross.sum()), ovules=float(l.ovules.sum()),
                                zero_recruits_probability=float(np.exp(-l.maternal.sum())))
        (output / (key + '.json')).write_text(json.dumps(rec, sort_keys=True) + '\n', encoding='utf-8')
        records.append(rec)
        if len(records) % 100 == 0:
            print('verified', len(records), '/', len(selected), flush=True)
    # Exact all-fixed occupancy/viability control over both origins, no genotype-equality claim.
    indexed = {(r['task']['block'], r['task']['replicate'], r['task']['origin'],
                r['task']['target'], r['task']['policy']): r for r in records}
    for t in selected:
        if t['origin'] != ORIGINS[0] or t['policy'] != 'MAI_fixed':
            continue
        other = dict(t, origin=ORIGINS[1])
        with np.load(output / (case_key(t) + '.npz')) as x, np.load(output / (case_key(other) + '.npz')) as y:
            np.testing.assert_array_equal(x['population'], y['population'])
            np.testing.assert_array_equal(x['diagnostics'], y['diagnostics'])
    receipt = dict(status='technical_verified' if technical else 'complete_verified', shard=shard,
                   input_sha256=sha, native_checks=native_checks, cases=len(records), records=records,
                   execution_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], encoding='utf-8').strip(),
                   numpy=np.__version__, full_fixed_negative_control='passed')
    (output / 'SHARD.json').write_text(json.dumps(receipt, sort_keys=True, indent=2) + '\n', encoding='utf-8')
    print(receipt['status'], 'cases', len(records), 'native checks', native_checks, flush=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--sha256', required=True)
    p.add_argument('--shard', type=int, required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--technical', action='store_true')
    args = p.parse_args()
    run_shard(args.input, args.sha256, args.shard, args.output, technical=args.technical)


if __name__ == '__main__':
    main()
