"""Sustained-isolation extension; same biology, no common-environment transfer."""
from dataclasses import replace
from concurrent.futures import ProcessPoolExecutor,as_completed
from functools import lru_cache
from pathlib import Path
import argparse,hashlib,json,os,zipfile
import numpy as np
from scripts.model3_island.types import Config
from scripts.model3_island.run import founders_from_spec,history_from_spec
from scripts.model3_island.density import project_state,density_step
from scripts.model3_island.tensor_density import make_tensor_grid
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import stream,STREAM_IDS
ROOT=Path(__file__).resolve().parents[1]
AXES={5:[0,.25,.5,.75,1],7:[0,.125,.25,.5,.75,.875,1],9:list(np.linspace(0,1,9))}


def config(setting,rate):
    c=Config.from_dict(json.loads((ROOT/'data/design/model3_ch2_bridge_20260927.json').read_text())['base_config'])
    return replace(c,years=1000,mutation_rate=rate,mutation_sd=.05,assurance_mode='evolving',
      assurance_cost=.5 if setting=='assurance_cost' else 0.,
      assurance_timing='prior' if setting=='prior_selfing' else 'delayed')


@lru_cache(maxsize=8)
def exposure(seed,arm):
    c=config('assurance_cost',0)
    near=history_from_spec(replace(c,visitor_arrival=replace(c.visitor_arrival,distance=0)),{'kind':'assembly'},seed)
    if arm=='near':return near
    far=history_from_spec(replace(c,visitor_arrival=replace(c.visitor_arrival,distance=3)),{'kind':'assembly'},seed)
    return far


def atomic_json(path,data):
    temporary=path.with_suffix('.tmp');temporary.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n');os.replace(temporary,path)


def run_case(task):
    out,key,kind,setting,rate,seed,rep,arm,n,scheme,projected=task
    out=Path(out);path=out/(key+'.npz');receipt=out/(key+'.json')
    if receipt.exists():
        r=json.loads(receipt.read_text())
        if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest()==r['sha256'] and r['task']==list(task[2:]):return key
        raise ValueError('invalid existing case receipt '+key)
    c=config(setting,rate);h=exposure(seed,arm)
    founders=founders_from_spec(dict(count=48,draw_count=48,means=[.5,.5,.5],sd=.15,birth_year=0),74001)
    if projected:founders,_=project_state(founders,make_tensor_grid((AXES[5],)*3))
    trace=np.full((1001,10),np.nan);checkpoints={}
    if kind=='density':
        grid=make_tensor_grid((AXES[n],)*3);_,state=project_state(founders,grid)
        traits=grid.genotypes.mean(axis=2)
    else:
        state=founders
        rseed=int(np.random.SeedSequence([seed,rep]).generate_state(1)[0])
        streams={name:stream(rseed,name,0) for name in STREAM_IDS}
    for t in range(1001):
        if kind=='density':
            mass=state.sum();trace[t,0]=mass
            if mass>0:
                means=state@traits/mass;trace[t,1:4]=means
                trace[t,4:7]=state@((traits-means)**2)/mass
        else:
            trace[t,0]=len(state.ids)
            if len(state.ids):
                traits=state.alleles.mean(axis=2);trace[t,1:4]=traits.mean(axis=0);trace[t,4:7]=traits.var(axis=0)
                trace[t,7:]=[len(np.unique(state.alleles[:,k])) for k in range(3)]
        if t in [0,200,400,1000]:checkpoints['state_'+str(t)]=state.copy() if kind=='density' else state.alleles.copy()
        if t==1000:break
        if kind=='density':
            if state.sum()==0:continue
            state,_=density_step(state,grid,h.visitors[t],h.seed_candidates[t],c,mutation_scheme=scheme,inheritance_backend='tensor')
        else:
            ledger=reproduce(state,h.visitors[t],c)
            state,_=advance(state,ledger,h.seed_candidates[t],c,streams,year=t)
    temporary=path.with_suffix('.tmp')
    with temporary.open('wb') as handle:np.savez_compressed(handle,trace=trace,**checkpoints)
    os.replace(temporary,path)
    atomic_json(receipt,dict(task=list(task[2:]),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    return key


def tasks(out,mode,histories=32,repeats=4):
    result=[]
    if mode=='density':
        for setting in ['assurance_cost','prior_selfing']:
         for rate in [0.,.01]:
          for seed in range(76001,76005):
           for arm in ['near','far']:
            for n in [5,7,9]:
             for scheme in (['jump'] if rate==0 else ['jump','heat_fv']):
              key=f'density_{setting}_u{rate}_h{seed}_{arm}_n{n}_{scheme}'
              result.append((str(out),key,'density',setting,rate,seed,0,arm,n,scheme,True))
    else:
        projected=mode=='benchmark'
        for setting in ['assurance_cost','prior_selfing']:
         for rate in [0.,.01]:
          for seed in range(76001,76001+(4 if projected else histories)):
           for rep in range(7101,7101+(4 if projected else repeats)):
            for arm in ['near','far']:
             key=f'persistent_{mode}_{setting}_u{rate}_h{seed}_r{rep}_{arm}'
             result.append((str(out),key,'abm',setting,rate,seed,rep,arm,0,'jump',projected))
    return [t for t in result if t[7]=='far']


def snapshot(out):
    sources=sorted(set(list((ROOT/'scripts/model3_island').glob('*.py'))+[Path(__file__),
      ROOT/'data/design/model3_ch2_bridge_20260927.json',
      ROOT/'docs/superpowers/plans/2026-10-04-model3-full-mutation.md',
      ROOT/'docs/superpowers/plans/2026-10-04-model3-full-mutation-execution.md', ROOT/'data/design/model3_persistent_isolation_20261005.json', ROOT/'scripts/run_model3_full_mutation.py']))
    hashes={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    manifest=out/'sources.json'
    if manifest.exists():
        if json.loads(manifest.read_text())!=hashes:raise ValueError('source changed; cannot resume this output')
    else:
        atomic_json(manifest,hashes)
        with zipfile.ZipFile(out/'sources.zip','w',zipfile.ZIP_DEFLATED) as z:
            for p in sources:z.write(p,p.relative_to(ROOT).as_posix())


def main():
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['core'],required=True)
    p.add_argument('--out',required=True);p.add_argument('--workers',type=int,default=2)
    p.add_argument('--histories',type=int,default=32);p.add_argument('--repeats',type=int,default=4)
    a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True);snapshot(out)
    todo=tasks(out,a.mode,a.histories,a.repeats)
    print('Declared cases',len(todo),flush=True)
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        futures=[pool.submit(run_case,t) for t in todo]
        for i,f in enumerate(as_completed(futures),1):
            key=f.result()
            if i%8==0 or i==len(todo):print(i,'/',len(todo),key,flush=True)
    atomic_json(out/f'{a.mode}_{a.histories}_{a.repeats}_complete.json',dict(status='completed',n_cases=len(todo),keys=[t[1] for t in todo]))

if __name__=='__main__':main()
