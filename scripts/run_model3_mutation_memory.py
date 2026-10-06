"""Declared one-locus birth-diffusion and common-environment history diagnostic."""
from dataclasses import replace
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from scripts.audit_model3_unified_reduction import _config,_founders,_visitors,_empty_state
from scripts.model3_island.density import make_grid,project_state,density_step
from scripts.model3_island.population import advance
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.randomness import stream,STREAM_IDS

ROOT=Path(__file__).resolve().parents[1]
MASK=(False,True,False)
PAST=200
TOTAL=1000


def founders(capacity):
    source=_founders(.5,[[.4,.4],[.4,.6],[.6,.6]])
    factor=capacity//48
    return replace(source,alleles=np.repeat(source.alleles,factor,axis=0),
        allele_origin=np.repeat(source.allele_origin,factor,axis=0),
        mutation_flags=np.repeat(source.mutation_flags,factor,axis=0),
        ids=np.arange(capacity,dtype=np.int64),birth_years=np.zeros(capacity,dtype=np.int64))


def configuration(capacity,rate):
    d=json.loads((ROOT/'data/design/model3_unified_reduction_audit_20260927.json').read_text())
    return replace(_config(d),capacity=capacity,years=TOTAL,mutation_rate=rate,mutation_sd=.05)


def visitor_history(past):
    common=_visitors([.35,.45,.55,.65])
    earlier=common if past=='present' else _visitors([])
    return [earlier]*PAST+[common]*(TOTAL-PAST)


def run_density(nodes,scheme,rate,past):
    c=configuration(48,rate)
    grid=make_grid(([.5],np.linspace(0,1,nodes),[.5]))
    _,mass=project_state(founders(48),grid)
    values=grid.genotypes.mean(axis=2)[:,1]
    trace=np.full((TOTAL+1,3),np.nan)
    checkpoints=[]
    for t,v in enumerate(visitor_history(past)+[None]):
        total=mass.sum()
        trace[t,0]=total
        if total>0:
            mean=values@mass/total
            trace[t,1:]=mean,(values-mean)**2@mass/total
        if t in [0,200,400,1000]: checkpoints.append(mass.copy())
        if v is not None:
            mass,_=density_step(mass,grid,v,_empty_state(t+1),c,
                mutation_traits=MASK,mutation_scheme=scheme)
    return dict(trace=trace,checkpoints=np.array(checkpoints),genotypes=grid.genotypes)


def run_finite(capacity,rate,past,seed):
    c=configuration(capacity,rate)
    state=founders(capacity)
    streams={name:stream(seed,name,0) for name in STREAM_IDS}
    trace=np.full((TOTAL+1,4),np.nan)
    checkpoints={}
    for t,v in enumerate(visitor_history(past)+[None]):
        trace[t,0]=len(state.ids)
        if len(state.ids):
            values=state.alleles[:,1].mean(axis=1)
            trace[t,1:]=values.mean(),values.var(),len(np.unique(state.alleles[:,1]))
        if t in [0,200,400,1000]: checkpoints['genotypes_'+str(t)]=state.alleles.copy()
        if v is not None:
            ledger=reproduce(state,v,c)
            state,_=advance(state,ledger,_empty_state(t+1),c,streams,year=t,mutation_traits=MASK)
    return dict(trace=trace,**checkpoints)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',required=True)
    args=parser.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    sources=['scripts/run_model3_mutation_memory.py','scripts/model3_island/density.py',
      'scripts/model3_island/population.py','scripts/model3_island/reproduction.py',
      'scripts/model3_island/types.py','docs/superpowers/plans/2026-10-04-model3-mutation-memory.md']
    hashes={p:hashlib.sha256((ROOT/p).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in sources}
    manifest_path=out/'manifest.json'
    if manifest_path.exists():
        if json.loads(manifest_path.read_text())['source_sha256']!=hashes:
            raise ValueError('existing source mismatch: use a new output directory')
    else:manifest_path.write_text(json.dumps(dict(source_sha256=hashes),indent=2))
    completed=[]
    for n in [11,21,41]:
        for scheme in ['jump','heat']:
            for rate in [0.,.01]:
                for past in ['present','absent']:
                    name=f'density_n{n}_{scheme}_u{rate}_{past}'
                    path=out/(name+'.npz')
                    if not path.exists():np.savez_compressed(path,**run_density(n,scheme,rate,past))
                    completed.append(name);print(name,flush=True)
    for capacity in [48,192]:
        for rate in [0.,.01]:
            for seed in range(6101,6109):
                for past in ['present','absent']:
                    name=f'abm_n{capacity}_u{rate}_s{seed}_{past}'
                    path=out/(name+'.npz')
                    if not path.exists():np.savez_compressed(path,**run_finite(capacity,rate,past,seed))
                    completed.append(name);print(name,flush=True)
    result=dict(status='completed',source_sha256=hashes,n_cases=len(completed),
      evidence_sha256={name:hashlib.sha256((out/(name+'.npz')).read_bytes()).hexdigest() for name in completed})
    manifest_path.write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
