"""Three-policy trajectory writer. Only the authorized coordinator may call workers."""
import argparse
from concurrent.futures import ProcessPoolExecutor, wait, FIRST_COMPLETED
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import sys
import time

import numpy as np

from q3_futures_contract_20261014 import FIELDS, arrays, checked_bytes, load_native
from q3_distribution_triangle_20261014 import construct, POLICIES
from q3_triangle_contract_20261014 import require, seed_for, validate_cases
from q3_triangle_execution_gate_20261014 import authorize, digest, exclusive_json, ShardBudget, LIMITS, ACTIVATION, job_deadline
from q3_triangle_io_20261014 import admit, package, tree_bytes
from verify_q3_triangle_paths_20261014 import verify_triplet


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


def append_journal(handle, state, parents, year, metadata):
    """Durable, checksummed census before allowing the next transition."""
    buffer = io.BytesIO()
    np.savez(buffer, **{k: getattr(state, k) for k in FIELDS}, parentage=parents,
             year=np.array(year), metadata=np.array(json.dumps(metadata, sort_keys=True)))
    raw = buffer.getvalue()
    require(handle.tell()+len(raw)+40 <= 8*1024**2, 'active journal eight-MiB ceiling')
    handle.write(len(raw).to_bytes(8, 'big')+hashlib.sha256(raw).digest()+raw)
    handle.flush();os.fsync(handle.fileno())


def read_journal(path):
    """Recover intact censuses from a HOLD, ignoring a truncated final record."""
    with Path(path).open('rb') as handle:
        while True:
            header = handle.read(40)
            if len(header) < 40:
                return
            size = int.from_bytes(header[:8], 'big')
            require(0 < size <= 8*1024**2, 'journal record size')
            raw = handle.read(size)
            if len(raw) < size:
                return
            require(hashlib.sha256(raw).digest() == header[8:], 'journal record hash')
            yield arrays(raw)


def produce_triplet(case, replicate, out, execution_sha, deadline):
    """Private worker: coordinator reserves this triplet before submission."""
    out = Path(out)
    names = {p: f"{case['key']}__r{replicate:03d}__{p}.npz" for p in 'ABC'}
    if any((out/'raw'/name).exists() or (out/'partial'/name.replace('.npz', '.journal')).exists()
           for name in names.values()):
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
        metadata = dict(key=case['key'], replicate=replicate, arm=arm, trigger=case['trigger'],
                        seeds={p: str(v) for p, v in seeds.items()}, permutation=permutation,
                        artificial_edit=dict(trait='I', carrier_indices=permutation[:POLICIES[arm]['heterozygotes']],
                                             width=POLICIES[arm]['width'], historical_mutation_flags_unchanged=True),
                        original_sha256=case['original_npz_sha256'], execution_sha256=execution_sha)
        snapshots, parents = [], []
        (out/'partial').mkdir(exist_ok=True)
        journal = out/'partial'/names[arm].replace('.npz', '.journal')
        with journal.open('xb') as handle:
            append_journal(handle, state, np.empty((0, 3), dtype=np.int64), case['trigger'], metadata)
            snapshots.append({k: getattr(state, k).copy() for k in FIELDS})
            for year in range(case['trigger'], 200):
                require(time.monotonic() < deadline and not (out/'ABORT').exists(), 'deadline/abort')
                state, info = pop.advance(state, repro.reproduce(state, visitors, cfg), empty, cfg,
                                          streams, year=year, mutation_traits=(False, False, True))
                append_journal(handle, state, info['parentage'], year+1, metadata)
                parents.append(info['parentage'].copy())
                snapshots.append({k: getattr(state, k).copy() for k in FIELDS})
        result = {k: np.concatenate([s[k] for s in snapshots]) for k in FIELDS}
        result.update(offsets=np.r_[0, np.cumsum([len(s['ids']) for s in snapshots])],
                      parent_offsets=np.r_[0, np.cumsum([len(p) for p in parents])].astype(np.int64),
                      parentage=np.concatenate(parents) if parents else np.empty((0, 3), dtype=np.int64),
                      metadata=np.array(json.dumps(metadata, sort_keys=True)))
        path = out/'raw'/names[arm]
        with path.open('xb') as handle:
            np.savez_compressed(handle, **result)
            handle.flush();os.fsync(handle.fileno())
        t = case['remaining_updates']
        require(path.stat().st_size <= (t+1)*5664+t*1152+131072, 'per-path storage ceiling')
        saved[arm] = dict(name=names[arm], sha256=digest(path), bytes=path.stat().st_size)
        journal.unlink()  # Consolidated immutable NPZ is now durable.
    return saved


def run_triplet(case, replicate, out, execution_sha, deadline):
    started = time.monotonic()
    saved = produce_triplet(case, replicate, out, execution_sha, deadline)
    result = verify_triplet(case, replicate, out, execution_sha, deadline, saved)
    result.update(production_updates=3*case['remaining_updates'], worker_seconds=time.monotonic()-started)
    path = Path(out)/'triplets'/f"{case['key']}__r{replicate:03d}.json"
    exclusive_json(path, result)
    require(path.stat().st_size <= 32768, 'triplet receipt ceiling')
    return result


def native_fixtures(case, out, deadline):
    """Four synthetic transitions, only after shard-zero authorization/reservation."""
    require(time.monotonic() < deadline, 'fixture deadline')
    initial, cfg, visitors, native = context(case, Path(out))
    types, pop, repro, randomness = native
    values = {k: a.copy() for k, a in initial.items()}
    values['alleles'][:] = .5
    values['allele_origin'][:] = 0;values['mutation_flags'][:] = False
    values['ids'][:] = np.arange(48);values['birth_years'][:] = 0
    empty = types.PlantState(**{k: a[:0].copy() for k,a in values.items()})
    seed = int.from_bytes(hashlib.sha256(b'izu-q3-distribution-triangle-v1-20261014\0synthetic-fixture').digest()[:16], 'big')
    results = []
    for _ in range(2):
        state = types.PlantState(**{k: a.copy() for k,a in values.items()})
        streams = {n: randomness.stream(seed, n, 0) for n in randomness.STREAM_IDS}
        require(time.monotonic() < deadline, 'fixture deadline')
        next_state, info = pop.advance(state, repro.reproduce(state, visitors, cfg), empty, cfg, streams,
                                       year=0, mutation_traits=(False, False, True))
        require(time.monotonic() < deadline, 'fixture deadline')
        extinct, extinction_info = pop.advance(empty, repro.reproduce(empty, visitors, cfg), empty, cfg, streams,
                                               year=1, mutation_traits=(False, False, True))
        require(len(extinct.ids) == 0 and extinction_info['parentage'].shape == (0, 3), 'empty native continuation')
        results.append((next_state, info['parentage']))
    require(all(np.array_equal(getattr(results[0][0], f), getattr(results[1][0], f)) for f in FIELDS)
            and np.array_equal(results[0][1], results[1][1]), 'fixture same-seed state/parents')
    return dict(status='PASS', native_updates=4, scientific_trajectories=0, seed=str(seed),
                equal_state_parentage=True, empty_continuation=True)


def dispatch(cases, shard, out, execution_sha, run_id, deadline):
    out = Path(out)
    budget = ShardBudget(out/'budget', shard=shard, execution_sha=execution_sha, run_id=run_id, cases=cases)
    jobs = [(c, r) for c in cases if c['trigger'] is not None for r in range(shard*8, (shard+1)*8)]
    todo = iter(jobs)
    results = []
    with ProcessPoolExecutor(max_workers=2) as pool:
        pending = {}
        def launch():
            require(time.monotonic() < deadline and not (out/'ABORT').exists(), 'worker deadline/abort')
            job = next(todo, None)
            if job is None:
                return
            case, replicate = job
            budget.reserve(case, replicate)
            pending[pool.submit(run_triplet, case, replicate, str(out), execution_sha, deadline)] = job
        try:
            launch();launch()
            while pending:
                done, _ = wait(pending, timeout=5, return_when=FIRST_COMPLETED)
                require(time.monotonic() < deadline, 'worker deadline')
                completed = [f.result() for f in done]  # Any failed job stops further launches.
                for future, result in zip(done, completed):
                    case, replicate = pending.pop(future)
                    require((result['key'], result['replicate']) == (case['key'], replicate), 'worker identity')
                    require(result['production_updates'] == result['native_updates'] == 3*case['remaining_updates'],
                            'worker update accounting')
                    results.append(result)
                if completed and len(results) % 32 == 0:
                    print(f'verified triplets {len(results)}/{len(jobs)}', flush=True)
                for _ in completed:
                    launch()
        except BaseException:
            (out/'ABORT').write_text('Technical HOLD; no new biological work.\n', encoding='utf-8')
            for future in pending:
                future.cancel()
            raise
    require(len(results) == len(jobs) and budget.reserved_updates() ==
            sum(r['production_updates']+r['native_updates'] for r in results), 'complete reserved accounting')
    return sorted(results, key=lambda r:(r['key'], r['replicate']))


def main(argv=None):
    parser = argparse.ArgumentParser()
    for name in ('repo', 'out', 'archive'):
        parser.add_argument('--'+name, type=Path, required=True)
    parser.add_argument('--shard', type=int, required=True)
    args = parser.parse_args(argv)
    execution, execution_sha, identity = authorize(args.repo)
    require(type(args.shard) is int and 0 <= args.shard < 18, 'shard range')
    sys.dont_write_bytecode = True
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    repo, out = args.repo.resolve(), args.out.resolve()
    started = time.monotonic()
    deadline = job_deadline(os.environ, minutes=15, tail_seconds=180)
    worker_deadline = deadline-120  # Explicit two-minute packaging allowance.
    require(worker_deadline > time.monotonic()+30, 'insufficient time before biology')
    def guard():
        require(time.monotonic() < deadline, 'shard internal deadline')
    out.mkdir(parents=True, exist_ok=False)
    try:
        require(shutil.disk_usage(out).free >= LIMITS['minimum_free_local_bytes'], 'six GiB free-space admission')
        plan = json.loads((repo/'data/designs/q3_triangle_preflight_20261014.json').read_text(encoding='utf-8'))
        validate_cases(plan['cases'])
        require(plan['shards'][args.shard]['replicates'] == list(range(args.shard*8, (args.shard+1)*8)), 'shard plan')
        inputs = admit(args.archive, plan, out, guard)
        (out/'raw').mkdir();(out/'triplets').mkdir()
        exclusive_json(out/'EXECUTION.json', dict(execution=execution, execution_sha256=execution_sha,
                       identity=identity, shard=args.shard))
        shutil.copyfile(repo/ACTIVATION, out/'ACTIVATION.json')
        shutil.copyfile(repo/'data/designs/q3_triangle_preflight_20261014.json', out/'PREFLIGHT.json')
        for name, expected in execution['code_sha256'].items():
            require(digest(repo/name) == expected, 'executed source identity')
            target = out/'execution_source'/name
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open('xb') as handle:
                handle.write((repo/name).read_bytes())
        # Existing128MiB metadata allowance: reserve16MiB for two active
        # journals and1MiB for later budget/fixture/header/member manifests.
        require(tree_bytes(out)+1024**2 <= 112*1024**2, 'metadata and durable-journal reservation')
        fixture_updates = 0
        if args.shard == 0:
            exclusive_json(out/'FIXTURE_RESERVATION.json', dict(native_updates_reserved=4,
                           execution_sha256=execution_sha, run_id=identity['run_id']))
            fixture_result = native_fixtures(next(c for c in plan['cases'] if c['trigger'] is not None), out, worker_deadline)
            exclusive_json(out/'FIXTURES.json', fixture_result)
            fixture_updates = fixture_result['native_updates']
        records = dispatch(plan['cases'], args.shard, out, execution_sha, identity['run_id'], worker_deadline)
        require(len(records) == 488 and sum(r['native_updates'] for r in records) == 185760,
                'complete shard native accounting')
        for name, expected in inputs.items():
            guard();require(digest(out/name) == expected, 'input/source changed during execution')
        for name, expected in execution['code_sha256'].items():
            guard();require(digest(repo/name) == expected, 'executed source changed during execution')
        exclusive_json(out/'SHARD.json', dict(status='ALL_1464_PATHS_REPLAYED', shard=args.shard,
                       run_id=identity['run_id'], execution_sha256=execution_sha,
                       triplets=488, trajectories=1464, production_updates=185760, replay_updates=185760,
                       fixture_updates=fixture_updates, reserved_native_updates=371520+fixture_updates,
                       state_field_checks=sum(r['state_field_checks'] for r in records),
                       parent_checks=sum(r['parent_checks'] for r in records),
                       elapsed_seconds=time.monotonic()-started))
        guard()
        archive = out.parent/f'Q3_TRIANGLE_SHARD_{args.shard:02d}.zip'
        require(shutil.disk_usage(out).free > tree_bytes(out)+1024*1024, 'packaging free-space ceiling')
        receipt = package(out, archive, guard)
        receipt.update(shard=args.shard, run_id=identity['run_id'], execution_sha256=execution_sha,
                       elapsed_seconds=time.monotonic()-started)
        exclusive_json(out.parent/f'SHARD_{args.shard:02d}_RECEIPT.json', receipt)
        print('COMPLETE_SHARD: all paths independently replayed and archive read back', flush=True)
    except BaseException as exc:
        (out/'ABORT').write_text('Technical HOLD; retain partial records; do not rerun.\n', encoding='utf-8')
        if not (out/'HOLD.json').exists():
            exclusive_json(out/'HOLD.json', dict(status='TECHNICAL_HOLD', shard=args.shard,
                           execution_sha256=execution_sha, exception=type(exc).__name__, reason=str(exc),
                           elapsed_seconds=time.monotonic()-started))
        raise


if __name__ == '__main__':
    main()
