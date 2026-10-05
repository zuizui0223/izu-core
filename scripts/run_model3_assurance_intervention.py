"""Matched-founder capacity intervention; separate from frozen main campaigns."""
from dataclasses import replace
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import json
import zipfile
import os
import numpy as np
from scripts.run_model3_persistent_isolation import config as base_config, exposure
from scripts.model3_island.run import founders_from_spec
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import stream, STREAM_IDS

ROOT=Path(__file__).resolve().parents[1]


def config(setting,rate,mode):
    if mode not in ('fixed','evolving'):
        raise ValueError('unknown capacity mode')
    return replace(base_config(setting,rate),assurance_mode=mode,fixed_assurance=.5)


def founders():
    state=founders_from_spec(dict(count=48,draw_count=48,means=[.5,.5,.5],sd=.15,birth_year=0),74001)
    alleles=state.alleles.copy();alleles[:,2,:]=.5
    return replace(state,alleles=alleles)


def simulate(setting,rate,seed,rep,arm,mode,*,steps=1000):
    c=config(setting,rate,mode);h=exposure(seed,arm);state=founders()
    master=int(np.random.SeedSequence([seed,rep]).generate_state(1)[0])
    streams={name:stream(master,name,0) for name in STREAM_IDS}
    trace=np.full((steps+1,10),np.nan);states={}
    for t in range(steps+1):
        trace[t,0]=len(state.ids)
        if len(state.ids):
            traits=state.alleles.mean(axis=2)
            trace[t,1:4]=traits.mean(axis=0);trace[t,4:7]=traits.var(axis=0)
            trace[t,7:]=[len(np.unique(state.alleles[:,k])) for k in range(3)]
            if mode=='fixed':assert np.all(traits[:,2]==.5)
        if t in [0,200,400,1000]:states['state_'+str(t)]=state.alleles.copy()
        if t==steps:break
        ledger=reproduce(state,h.visitors[t],c)
        state,_=advance(state,ledger,h.seed_candidates[t],c,streams,year=t,
                        mutation_traits=(True,True,mode=='evolving'))
    return trace,states


def tasks():
    return [(s,u,h,r,a,m) for s in ['assurance_cost','prior_selfing'] for u in [0.,.01]
            for h in range(76001,76065) for r in range(7101,7109)
            for a in ['near','far'] for m in ['fixed','evolving']]


def atomic_json(path,data):
    temp=path.with_suffix('.tmp')
    temp.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    os.replace(temp,path)


def run_case(out,task):
    s,u,h,r,a,m=task
    key=f'{s}_u{u}_h{h}_r{r}_{a}_{m}'
    path=Path(out)/(key+'.npz');receipt=path.with_suffix('.json')
    if receipt.exists():
        saved=json.loads(receipt.read_text(encoding='utf-8'))
        assert saved['task']==list(task)
        assert hashlib.sha256(path.read_bytes()).hexdigest()==saved['sha256']
        return key
    trace,states=simulate(*task)
    temporary=path.with_suffix('.tmp')
    with temporary.open('wb') as handle:np.savez_compressed(handle,trace=trace,**states)
    os.replace(temporary,path)
    atomic_json(receipt,dict(task=list(task),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    return key


def main():
    out=ROOT/'outputs/model3_assurance_intervention_20261005';out.mkdir(parents=True,exist_ok=True)
    sources=list((ROOT/'scripts/model3_island').glob('*.py'))+[Path(__file__),
        ROOT/'scripts/run_model3_persistent_isolation.py',ROOT/'data/design/model3_ch2_bridge_20260927.json',
        ROOT/'data/design/model3_assurance_intervention_20261005.json']
    hashes={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    manifest=out/'sources.json'
    if manifest.exists():assert json.loads(manifest.read_text(encoding='utf-8'))==hashes
    else:
        atomic_json(manifest,hashes)
        with zipfile.ZipFile(out/'sources.zip','w',zipfile.ZIP_DEFLATED) as archive:
            for p in sources:archive.write(p,p.relative_to(ROOT).as_posix())
    todo=tasks();keys=[]
    print('Declared cases',len(todo),flush=True)
    with ProcessPoolExecutor(max_workers=2) as pool:
        futures=[pool.submit(run_case,str(out),t) for t in todo]
        for i,future in enumerate(as_completed(futures),1):
            keys.append(future.result())
            if i%16==0:print(i,'/',len(todo),flush=True)
    atomic_json(out/'complete.json',dict(status='completed',n_cases=len(keys),keys=sorted(keys)))


if __name__=='__main__':main()
