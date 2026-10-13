"""Run the *already registered* Model 3 two-axis pilot; NEVER choose cases from outcomes.

Production is deliberately gated: exact original biological source Git blobs,
exact original t0 typed fixture and registration, NumPy2.2.6, fixed shards
(6 x 256 cases), no overwrite/retries, complete genome/parentage outputs.

Use `--technical` with a distinct debug RNG salt for 3-update smoke fixtures.
Do not promote a producer result before independent raw-source reader admission.
"""
from __future__ import annotations
import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import os
import re
import zipfile
import numpy as np

from scripts.audit_chapter2_clock_native_birth_technical_20261013 import (
    FIELDS, MUTATION_MASK, load_original_source, source_fixture,
    initial_state, visitor_and_config, state_hash,
)

REGISTERED_INPUTS=Path('data/design/chapter2_clock_factorial_pilot_registered_inputs_20261013.json')
REGISTERED_INPUTS_GIT_BLOB='0721517f7bf69eee1c2daf040f4781873ba3c3ea'
FULL_HORIZON=200
TECH_HORIZON=3
TECH_SEED_SALT='chapter2-clock-factorial-producer-debug-only-20261013'
ALLOWED_MODELS=(0.,3.,4.)
CATEGORY_NAMES=('assurance_first','investment_first','near_simultaneous','assurance_only','investment_only','neither')
CASE_RE=re.compile(r'^(main|confirmation)_c([034])_w(24|40)_i([01])_r(\d{3})$')
RETURN_FIELDS=('maternal','paternal','self_raw','self_viable','ovules','exported','delivered','outcross')
SERIAL_FIELDS=('ids','alleles','allele_origin','mutation_flags','birth_years')


def hashbytes(raw:bytes)->str:
    return hashlib.sha256(raw).hexdigest()


def git_blob(raw:bytes)->str:
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()


def canonical(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)


def safe_write(path:Path,payload:bytes):
    with path.open('xb') as w:w.write(payload)


def load_input_inventory(path:Path=REGISTERED_INPUTS):
    raw=path.read_bytes()
    if git_blob(raw)!=REGISTERED_INPUTS_GIT_BLOB:
        raise ValueError('Registered immutable 1536-case input inventory SHA mismatch')
    d=json.loads(raw)
    if d['status']!='FROZEN_INPUT_INVENTORY_ONLY_DO_NOT_DISPATCH' or d['n_cases']!=1536 or d['cluster_count']!=128 or d['n_updates_if_executed']!=307200:
        raise ValueError('Pilot registration dimensions drifted')
    if len(d['pilot_case_keys'])!=1536 or len(d['source_configs'])!=6 or len(d['genetic_treatments'])!=8:
        raise ValueError('Incomplete frozen input inventory')
    return d


def job_cases(registered,shard:int,technical:bool=False):
    if not isinstance(shard,int) or shard<0 or shard>=6:
        raise ValueError('Original fixed six-shard grid only')
    block=('main','confirmation')[shard//3]
    context=(0,3,4)[shard%3]
    clusters={(x['block'],x['replicate']):int(x['master']) for x in registered['rng_clusters']}
    out=[]
    for key in registered['pilot_case_keys']:
        m=CASE_RE.fullmatch(key)
        if m is None:raise ValueError('Unexpected registered case ID')
        kblock,ctx,w,h,rep=m.groups();ctx=int(ctx);rep=int(rep)
        if (kblock,ctx)!=(block,context):continue
        width=int(w)/512;hidden=float(h)
        case={'key':key,'block':block,'context':context,'width':width,'hidden':hidden,
              'replicate':rep,'master':clusters[block,rep]}
        if technical:
            # No real pilot random stream is touched by a smoke test.
            case['master']=int.from_bytes(hashlib.sha256((TECH_SEED_SALT+'\0'+key).encode()).digest()[:16],'big')
            if rep!=0:continue
        out.append(case)
    expected=4 if technical else 256
    if len(out)!=expected or len({r['key'] for r in out})!=len(out):
        raise ValueError('Sharded case inventory incomplete/duplicate')
    return out


def saved_events(means:np.ndarray,census:np.ndarray,delta:float=.05):
    if means.shape!=(FULL_HORIZON+1,3) or census.shape!=(FULL_HORIZON+1,):
        raise ValueError('Official event readout requires complete 200-update paths')
    if census[0]!=48 or np.any(census<0) or np.any(census>48):raise ValueError('Invalid count path')
    alive=census>0
    if not np.isfinite(means[alive]).all() or not np.isnan(means[~alive]).all():
        raise ValueError('Extinct genotype means must be missing, never zero')
    if np.any(np.diff(alive.astype(np.int8))>0):raise ValueError('Invalid recolonization')
    events={}
    for name,j,direction in (('A',2,1),('I',1,-1)):
        flag=alive & (direction*(means[:,j]-means[0,j])>=delta)
        loc=np.flatnonzero(np.convolve(flag.astype(int),np.ones(20,dtype=int),mode='valid')==20)
        events[name]=int(loc[0]) if len(loc) else None
    a,i=events['A'],events['I']
    if a is None:cat='neither' if i is None else 'investment_only'
    elif i is None:cat='assurance_only'
    elif abs(a-i)<=5:cat='near_simultaneous'
    else:cat='assurance_first' if a<i else 'investment_first'
    events['category']=cat
    return events


def simulate(case,registered,fixture,source,horizon:int):
    if horizon not in (TECH_HORIZON,FULL_HORIZON):raise ValueError('Unregistered source horizon')
    if case['context'] not in (0,3,4) or case['width'] not in (.046875,.078125) or case['hidden'] not in (0.,1.):
        raise ValueError('Unregistered pilot biological arm')
    modules=source
    config,vis,archived_returns=visitor_and_config(fixture,case['block'],case['context'],modules)
    initial,geometry=initial_state(fixture,case['block'],case['width'],case['hidden'],modules)
    arrays_ref={(r['block'],r['A_width'],r['I_hidden_homolog']):r for r in registered['genetic_treatments']}
    expected_genotype=arrays_ref[case['block'],case['width'],case['hidden']]['genotype_sha256']
    if hashbytes(initial.alleles.tobytes(order='C'))!=expected_genotype:
        raise ValueError('Original-genotype expected transformed SHA drift')
    configs={(r['block'],r['context']):r for r in registered['source_configs']}
    original_config=fixture['original_founders'][case['block']]['contexts'][str(case['context'])]['config']
    if hashbytes(canonical(original_config).encode())!=configs[case['block'],case['context']]['config_sha256']:
        raise ValueError('Original Model3 typed biological config mismatch')
    if config.capacity!=48 or config.years!=200 or config.survival!=0 or config.seed_arrival.supply!=0:
        raise ValueError('Original population life-cycle parameters are unregistered')
    pop=modules['population'];repro=modules['reproduction'];rngtool=modules['randomness']
    streams={n:rngtool.stream(case['master'],n,0) for n in rngtool.STREAM_IDS}
    empty=pop.subset(initial,np.empty(0,dtype=int))
    state=initial
    allfields={k:[] for k in FIELDS}
    offsets=[0];parentage=[];parent_offsets=[0];census=[];means=[];returns=[];selection=[]
    for t in range(horizon+1):
        census.append(len(state.ids))
        means.append(state.alleles.mean(axis=(0,2)) if len(state.ids) else np.full(3,np.nan))
        for k in FIELDS:allfields[k].append(getattr(state,k).copy())
        offsets.append(offsets[-1]+len(state.ids))
        if t==horizon:break
        ledger=repro.reproduce(state,vis,config)
        ledger_data=np.array([float(np.asarray(getattr(ledger,k)).sum()) for k in RETURN_FIELDS])
        if t==0 and not np.allclose(ledger_data,archived_returns,atol=1e-12,rtol=0):
            raise ValueError('Original founding F/P/S archived totals differ')
        returns.append(ledger_data)
        w=np.stack((ledger.outcross.sum(axis=0)/2,ledger.outcross.sum(axis=1)/2,ledger.self_viable))
        total=float(w.sum())
        traits=state.alleles.mean(axis=2) if len(state.ids) else np.zeros((0,3))
        selected=(w@(traits-traits.mean(axis=0))/total) if total>0 else np.full((3,3),np.nan)
        selection.append(selected)
        nxt,info=pop.advance(state,ledger,empty,config,streams,year=t,mutation_traits=MUTATION_MASK)
        if info['immigrant_recruits'] or info['survivors'] or info['resident_recruits']!=len(nxt.ids):
            raise ValueError('Native source demographic identity drift')
        if len(info['parentage'])!=len(nxt.ids):raise ValueError('Native source parentage count drift')
        parentage.append(info['parentage'])
        parent_offsets.append(parent_offsets[-1]+len(nxt.ids))
        state=nxt
    d={k:np.concatenate(v) for k,v in allfields.items()}
    d.update(offsets=np.asarray(offsets,dtype=np.int64),
             means=np.asarray(means,dtype=np.float64),
             population=np.asarray(census,dtype=np.int64),
             parentage=np.concatenate(parentage).reshape(-1,3),
             parent_offsets=np.asarray(parent_offsets,dtype=np.int64),
             returns=np.asarray(returns,dtype=np.float64),
             sexual_selection=np.asarray(selection,dtype=np.float64))
    if len(d['offsets'])!=horizon+2 or len(d['parent_offsets'])!=horizon+1:
        raise ValueError('Original annual source array inventory incomplete')
    if int(d['offsets'][-1])!=len(d['ids']) or int(d['parent_offsets'][-1])!=len(d['parentage']):
        raise ValueError('Incomplete original all-genome/parentage inventory')
    return d,{'task':case,'config':asdict(config),'original_t0_genotype_sha256':expected_genotype,
              'model_source_git_blobs':registered['original_source_git_blobs'],
              'original_provider_sha256':registered['original_provider_sha256'],
              'mutation_traits':list(MUTATION_MASK),'original_t0_first_annual_return':archived_returns.tolist(),
              'runtime_numpy':np.__version__,'horizon':horizon,
              'technical':horizon==TECH_HORIZON},geometry


def produce(shard:int,out:Path,*,technical:bool=False,registered_path:Path=REGISTERED_INPUTS):
    if not technical and np.__version__!='2.2.6':
        raise ValueError('Full producer must use exact original NumPy 2.2.6 numerical runtime')
    reg=load_input_inventory(registered_path)
    fixture=source_fixture()
    modules=load_original_source()
    cases=job_cases(reg,shard,technical)
    if out.exists():raise ValueError('Refuse existing output directory or partial run overwrite')
    out.mkdir(parents=True,exist_ok=False)
    producer_git=git_blob(Path(__file__).read_bytes())
    run_sha=os.environ.get('GITHUB_SHA') or 'UNBOUND_LOCAL_SOURCE_EXPERIMENT'
    identity={'schema':'chapter2_clock_pilot_original_model3_source_v1',
              'execution_commit':run_sha,'producer_git_blob':producer_git,
              'input_registry_git_blob':REGISTERED_INPUTS_GIT_BLOB,
              'original_genotype_fixture_blob':'4b529cce12bc44e06d43a22b10c325a52bbd967b',
              'model_git_blobs':reg['original_source_git_blobs'],
              'numpy_runtime':np.__version__,'technical':technical,
              'source_providers':reg['original_provider_sha256'],
              'case_count':len(cases),'fixed_updates':TECH_HORIZON if technical else FULL_HORIZON}
    safe_write(out/'REGISTRATION.json',(json.dumps({'identity':identity,'tasks':cases,
            'expected':len(cases)},indent=2,allow_nan=False)+'\n').encode())
    records=[]
    for i,case in enumerate(cases,1):
        d,metadata,geometry=simulate(case,reg,fixture,modules,TECH_HORIZON if technical else FULL_HORIZON)
        m={'identity':identity,'case':case,'metadata':metadata,'genetic_geometry':geometry}
        path=out/(case['key']+'.npz')
        if path.exists():raise ValueError('Refuse to overwrite a pre-existing original case')
        np.savez_compressed(path,**d,metadata=np.asarray(json.dumps(m,sort_keys=True,allow_nan=False)))
        with np.load(path,allow_pickle=False) as rec:
            if set(rec.files)!=set(d)|{'metadata'}:raise ValueError('Saved archive array inventory changed')
            for key in d:
                np.testing.assert_array_equal(rec[key],d[key],strict=True)
        r={'task':case,'case_sha256':hashbytes(path.read_bytes()),
           'censuses':len(d['population']),'parentage_events':len(d['parentage']),
           'mutation_mask':list(MUTATION_MASK)}
        if not technical:r['events']={str(th):saved_events(d['means'],d['population'],th) for th in (.025,.05,.1)}
        records.append(r)
        if i%32==0:print(json.dumps({'complete_cases':i,'shard_cases':len(cases),'technical':technical}),flush=True)
    completion={'status':'COMPLETE_FROZEN_CLOCK_FACTORIAL_SHARD' if not technical else 'TECHNICAL_ONLY_CLOCK_FACTORIAL_SHARD',
                'identity':identity,'cases':len(records),'records':records,
                'no_scientific_decision':technical,
                'not_confirmatory_clock':True}
    safe_write(out/'_COMPLETION.json',(json.dumps(completion,indent=2,allow_nan=False)+'\n').encode())
    safe_write(out/'EXECUTION_COMMIT.txt',(run_sha+'\n').encode())
    return {'status':completion['status'],'shard':shard,'cases':len(records),'updates':len(records)*identity['fixed_updates']}


def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--shard',type=int,required=True)
    a.add_argument('--out',type=Path,required=True)
    a.add_argument('--technical',action='store_true')
    a.add_argument('--registry',type=Path,default=REGISTERED_INPUTS)
    args=a.parse_args()
    print(json.dumps(produce(args.shard,args.out,technical=args.technical,registered_path=args.registry)))

if __name__=='__main__':main()
