"""Frozen middle-rate extension; exact endpoint replay gates production."""
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import replace
from functools import lru_cache
from pathlib import Path
from time import perf_counter
import argparse
import hashlib
import json
import os
import zipfile
import numpy as np
from scripts.run_model3_persistent_isolation import config
from scripts.model3_island.run import founders_from_spec, history_from_spec
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import stream, STREAM_IDS

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT/'data/design/model3_replenishment_evolution_20261005.json'
OUT = ROOT/'outputs/model3_replenishment_evolution_20261005'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write_json(p, d):
    temp = p.with_suffix('.tmp')
    temp.write_text(json.dumps(d, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    os.replace(temp, p)


@lru_cache(maxsize=8)
def history(seed, distance):
    c = config('assurance_cost', .01)
    c = replace(c, visitor_arrival=replace(c.visitor_arrival, distance=distance))
    return history_from_spec(c, {'kind':'assembly'}, seed)


def trajectory(setting, distance, seed, rep):
    c = config(setting, .01); h = history(seed, distance)
    state = founders_from_spec(dict(count=48, draw_count=48, means=[.5,.5,.5],
                                    sd=.15, birth_year=0), 74001)
    rseed = int(np.random.SeedSequence([seed,rep]).generate_state(1)[0])
    streams = {name:stream(rseed,name,0) for name in STREAM_IDS}
    trace = np.full((1001,10), np.nan)
    for t in range(1001):
        trace[t,0] = len(state.ids)
        if len(state.ids):
            traits = state.alleles.mean(axis=2)
            trace[t,1:4] = traits.mean(axis=0)
            trace[t,4:7] = traits.var(axis=0)
            trace[t,7:] = [len(np.unique(state.alleles[:,k])) for k in range(3)]
        if t == 1000: break
        state,_ = advance(state,reproduce(state,h.visitors[t],c),h.seed_candidates[t],c,streams,year=t)
    return trace


def case(task):
    setting,distance,seed,rep = task
    name = f'{setting}_d{distance:.2f}_h{seed}_r{rep}'
    p = OUT/(name+'.npz'); rec = OUT/(name+'.json')
    if rec.exists():
        r = json.loads(rec.read_text())
        assert r['task']==list(task) and p.exists() and sha(p)==r['sha256']
        return name, r['seconds']
    t = perf_counter(); a = trajectory(*task)
    tmp = p.with_suffix('.tmp')
    with tmp.open('wb') as f: np.savez_compressed(f,trace=a)
    os.replace(tmp,p)
    elapsed = perf_counter()-t
    write_json(rec,dict(task=list(task),sha256=sha(p),seconds=elapsed))
    return name,elapsed


def preflight():
    rows = []
    for setting in ['assurance_cost','prior_selfing']:
        for distance in [0.,3.]:
            for seed in [76001,76064]:
                rep = 7101
                if distance == 0:
                    folder = ROOT/'outputs/model3_full_mutation_20261004'
                    key = f'core_{setting}_u0.01_h{seed}_r{rep}_near'
                else:
                    folder = ROOT/'outputs/model3_persistent_isolation_20261005'
                    key = f'persistent_core_{setting}_u0.01_h{seed}_r{rep}_far'
                p = folder/(key+'.npz'); record = json.loads((folder/(key+'.json')).read_text())
                assert sha(p)==record['sha256']
                expected = ['abm',setting,.01,seed,rep,'near' if distance==0 else 'far',0,'jump',False]
                assert record['task']==expected
                with np.load(p) as d: original = d['trace']
                np.testing.assert_array_equal(trajectory(setting,distance,seed,rep), original)
                rows.append(dict(setting=setting,distance=distance,seed=seed,rep=rep,source_sha256=sha(p)))
    write_json(OUT/'preflight.json',dict(status='exact_all_trace_columns_endpoint_replay',cases=rows))


def main():
    parser = argparse.ArgumentParser();parser.add_argument('--workers',type=int,default=4)
    parser.add_argument('--preflight-only',action='store_true');args=parser.parse_args()
    plan = json.loads(DESIGN.read_text(encoding='utf-8'))
    for name,digest in plan['source_sha256'].items(): assert sha(ROOT/name)==digest,name
    OUT.mkdir(parents=True,exist_ok=True)
    identity={'design_sha256':sha(DESIGN),'runner_sha256':sha(Path(__file__)),
              'source_sha256':plan['source_sha256']}
    manifest=OUT/'manifest.json'
    if manifest.exists(): assert json.loads(manifest.read_text())==identity
    else:
        write_json(manifest,identity)
        with zipfile.ZipFile(OUT/'sources.zip','w',zipfile.ZIP_DEFLATED) as z:
            for name in [*plan['source_sha256'],DESIGN.relative_to(ROOT).as_posix(),Path(__file__).relative_to(ROOT).as_posix()]:
                z.write(ROOT/name,name)
    if not (OUT/'preflight.json').exists(): preflight()
    assert json.loads((OUT/'preflight.json').read_text())['status']=='exact_all_trace_columns_endpoint_replay'
    if args.preflight_only: print('Endpoint replay passed: 8 full 1,000-update traces',flush=True);return
    tasks=[(s,d,h,r) for d in plan['new_coordinates'] for h in plan['history_seeds']
           for s in plan['settings'] for r in plan['demographic_repeats']]
    assert len(tasks)==plan['new_cases']
    started=perf_counter();completed=0
    write_json(OUT/'progress.json',dict(status='running',pid=os.getpid(),completed=0,total=len(tasks)))
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        jobs=[pool.submit(case,t) for t in tasks]
        for job in as_completed(jobs):
            name,seconds=job.result();completed+=1
            if completed%64==0 or completed==len(tasks):
                progress=dict(status='running',pid=os.getpid(),completed=completed,total=len(tasks),
                              elapsed_seconds=perf_counter()-started,last_case=name,last_case_seconds=seconds)
                write_json(OUT/'progress.json',progress);print(json.dumps(progress),flush=True)
    write_json(OUT/'progress.json',dict(status='complete',completed=completed,total=len(tasks),elapsed_seconds=perf_counter()-started))


if __name__=='__main__': main()
