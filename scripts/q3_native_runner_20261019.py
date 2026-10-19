"""Technical-only Model3 -> atomic checkpoints -> paired Q3 inference bridge.

This bounded harness does NOT authorize a confirmatory experiment. Only its
3x3 technical source cohort is executable. Native biology and inference are
unchanged. All production sources and all earlier pilot seeds are excluded.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import platform
import tempfile
from pathlib import Path
import numpy as np
from scripts.model3_island.types import Config, PlantState, VisitorState
from scripts.model3_island.history import reflect_unit
from scripts.model3_island.randomness import stream, STREAM_IDS
from scripts.model3_island.population import advance
from scripts.model3_island.reproduction import reproduce
from scripts.chapter2_q3_balanced_assurance_founders_20261018 import (
    balance_founder_assurance_expression, verify_pairing)
from scripts.q3_joint_inference_20261019 import contrasts, summarize

ROOT=Path(__file__).resolve().parents[1]
FIELDS=('alleles','allele_origin','mutation_flags','ids','birth_years')
NATIVE_BLOBS={
 'scripts/model3_island/__init__.py':'b385daf32fb3d1a2435ef97fce62f47c8f56e81f',
 'scripts/model3_island/types.py':'0bc427b3261e7baf1651648ee879b368f9bf935b',
 'scripts/model3_island/history.py':'0c58aee6f73ae133d96d8da4dd6678886ff3061c',
 'scripts/model3_island/randomness.py':'46f1ee55899e729cdd09d9dbb9332694ef1e2071',
 'scripts/model3_island/population.py':'20e90f249f63e9f37e8801d19d9b75cade2fe193',
 'scripts/model3_island/reproduction.py':'95314698a3296b6f13b8c053c36f2df0b7b744ca',
 'scripts/chapter2_q3_balanced_assurance_founders_20261018.py':'5e1c82afd2369c6117f847be8d7f3715814cc102',
 'scripts/q3_joint_inference_20261019.py':'61f10f1bb680310068136ea1b481f0c466c0f314'}


def canonical(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def digest(x): return hashlib.sha256(x).hexdigest()


def technical_plan():
    return dict(schema='q3_native_technical_runner_v1',mode='technical',
        namespace='q3-native-integration-technical-20261019-v1',
        founders=[9100001,9100002,9100003],visitors=[9200001,9200002,9200003],
        policies=['fixed','evolving'],budgets=[8.,4.5],fork=35,end=80,
        capacity=48,margin=.10,confirmation_authorized=False)


def provenance():
    hashes={}
    for path,expected in NATIVE_BLOBS.items():
        raw=(ROOT/path).read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        if blob!=expected:raise ValueError('source or runtime changed: '+path)
        hashes[path]=digest(raw)
    hashes[Path(__file__).relative_to(ROOT).as_posix()]=digest(Path(__file__).read_bytes())
    import scipy
    return dict(base_commit='e131da0376a615bceca8770d5d7236a30a5a36fe',
        files=hashes,python=platform.python_version(),numpy=np.__version__,
        scipy=scipy.__version__,byteorder=__import__('sys').byteorder)


def budget(nf,nv):
    if type(nf) is not int or type(nv) is not int or min(nf,nv)<1:
        raise ValueError('positive integer independent axes required')
    cells=nf*nv
    return dict(crossed_cells=cells,prefix_paths=2*cells,terminal_branches=4*cells,
        unique_updates=250*cells,saved_state_slots=256*cells,
        uncompressed_padded_array_bytes=256*cells*(48*118+8),
        execution_authorized=False)


def initialize(root,plan):
    if plan!=technical_plan():raise ValueError('technical-only plan; confirmation is blocked')
    root=Path(root)
    if root.exists():raise ValueError('new empty output root required')
    info=dict(plan=plan,provenance=provenance())
    info['contract_sha256']=digest(canonical(info))
    root.mkdir(parents=True)
    (root/'states').mkdir()
    with (root/'RUN.json').open('x') as f:json.dump(info,f,sort_keys=True,indent=2)
    return info


def contract(root):
    info=json.loads((Path(root)/'RUN.json').read_text())
    raw={k:v for k,v in info.items() if k!='contract_sha256'}
    if info.get('contract_sha256')!=digest(canonical(raw)) or info.get('plan')!=technical_plan():
        raise ValueError('contract changed or unapproved production plan')
    if info['provenance']!=provenance():raise ValueError('source or runtime changed')
    return info


def master(plan,f,v,stage):
    if f not in plan['founders'] or v not in plan['visitors'] or stage not in ('prefix','fork'):
        raise ValueError('technical namespace bounds')
    raw=f"{plan['namespace']}|{stage}|{f}|{v}".encode()
    return int.from_bytes(hashlib.sha256(raw).digest()[:16],'big')


def rngs(seed):return {k:stream(seed,k,0) for k in STREAM_IDS}


def configuration(policy,b):
    if policy not in ('fixed','evolving') or b not in (8.,4.5):raise ValueError('unsupported arm')
    return Config.from_dict(dict(schema_version=1,event_order='reproduce-survive-arrive-recruit-v1',
        time_unit='reproductive_year',capacity=48,years=80,survival=0.,ovule_budget=b,
        pollen_budget=20.,investment_cost=.5,pollen_scale=1.,depression=.5,
        mutation_rate=0.,mutation_sd=.025,assurance_mode=policy,fixed_assurance=.5,
        assurance_timing='delayed',pollen_discount=0.,assurance_cost=.5,
        activity=.4,activity_mode='count_scaled',reference_visitor_count=4.,
        background_ratio=1.,background_resources=1.,island_history='founding',initial_visitors=4,
        visitor_breadth=.2,visitor_effectiveness=1.,source_allele_means=[.5,.5,.5],source_allele_sd=.15,
        seed_arrival=dict(supply=0.,distance=1.,scale=1.,kernel='exponential',establishment=.5,loss_hazard=0.),
        visitor_arrival=dict(supply=0.,distance=1.,scale=1.,kernel='exponential',establishment=.8,loss_hazard=.05)))


def founder(seed):
    rng=stream(seed,'founders',0)
    a=reflect_unit(np.array([.5,.5,.5])[None,:,None]+rng.normal(0,.08,(48,3,2)))
    a[:,1,:]=rng.choice([.375,.5,.625],size=(48,2))
    a[:,2,:]=rng.choice([.25,.5,.75],size=(48,2))
    s=PlantState(a,np.arange(288,dtype=np.int64).reshape(48,3,2),
        np.zeros((48,3,2),bool),np.arange(48,dtype=np.int64),np.zeros(48,dtype=np.int64))
    s=balance_founder_assurance_expression(s,seed=(seed+39110)%(2**32))
    verify_pairing(s,s)
    return s


def visitors(seed):
    opt=stream(seed,'visitor_initial',0).uniform(.3,.7,6)
    ids=np.arange(6,dtype=np.int64)+(seed+1)*100
    return (VisitorState(ids,opt,np.full(6,.2),np.ones(6)),
        VisitorState(ids[:1],opt[:1],np.full(1,.2),np.ones(1)),
        VisitorState(np.empty(0,dtype=np.int64),np.empty(0),np.empty(0),np.empty(0)))


def empty(s):return PlantState(**{k:getattr(s,k)[:0].copy() for k in FIELDS})


def tasks(plan,cells=None):
    available=[(f,v) for f in plan['founders'] for v in plan['visitors']]
    chosen=available if cells is None else list(cells)
    if len(chosen)!=len(set(chosen)):raise ValueError('duplicate cells')
    if any(x not in available for x in chosen):raise ValueError('unknown technical cell')
    return [dict(founder=f,visitor=v,policy=p,stage=stage,budget=b,start=start,end=end)
        for f,v in chosen for p in plan['policies']
        for stage,b,start,end in [('prefix',8.,0,35),('B8',8.,35,80),('B4p5',4.5,35,80)]]


def task_path(root,s):
    return Path(root)/'states'/f"{s['founder']}_{s['visitor']}_{s['policy']}_{s['stage']}.npz"


def packed(states):
    arrays={'counts':np.array([len(s.ids) for s in states],dtype=np.int64)}
    for k in FIELDS:
        sample=getattr(states[0],k)
        a=np.zeros((len(states),48)+sample.shape[1:],dtype=sample.dtype)
        for t,s in enumerate(states):a[t,:len(s.ids)]=getattr(s,k)
        arrays[k]=a
    return arrays


def state_at(a,t):
    n=int(a['counts'][t])
    return PlantState(**{k:a[k][t,:n] for k in FIELDS})


def payload_hash(meta,arrays):
    h=hashlib.sha256(canonical({k:v for k,v in meta.items() if k!='payload_sha256'}))
    for k in sorted(arrays):
        a=np.asarray(arrays[k]);h.update(canonical([k,a.dtype.str,list(a.shape)]));h.update(a.tobytes())
    return h.hexdigest()


def save_snapshot(path,meta,states):
    path=Path(path);a=packed(states);m=dict(meta);m['payload_sha256']=payload_hash(m,a)
    fd,tmp=tempfile.mkstemp(prefix=path.name+'.partial.',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as f:
            np.savez_compressed(f,_meta=np.frombuffer(canonical(m),dtype=np.uint8),**a)
            f.flush();os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)


def read_snapshot(path,expected_contract=None):
    try:
        with np.load(path,allow_pickle=False) as z:
            if set(z.files)!=set(FIELDS)|{'counts','_meta'}:raise ValueError('unexpected arrays')
            m=json.loads(z['_meta'].tobytes());a={k:z[k].copy() for k in z.files if k!='_meta'}
    except (OSError,EOFError,KeyError) as e:raise ValueError('unreadable checkpoint') from e
    if m.get('payload_sha256')!=payload_hash(m,a):raise ValueError('checkpoint checksum mismatch')
    if expected_contract is not None and m['contract_sha256']!=expected_contract:
        raise ValueError('checkpoint contract mismatch')
    if (a['counts'].dtype!=np.dtype('int64') or a['counts'].ndim!=1 or
        len(a['counts'])!=m['current']-m['task']['start']+1 or
        np.any((a['counts']<0)|(a['counts']>48))):raise ValueError('checkpoint shape/count mismatch')
    if set(m['rng'])!=set(STREAM_IDS):raise ValueError('incomplete RNG registry')
    for k in FIELDS:
        tail=(3,2) if k in ('alleles','allele_origin','mutation_flags') else ()
        if a[k].shape!=(len(a['counts']),48)+tail:raise ValueError('state array shape mismatch')
    return m,a


def run(root,*,max_updates=None,save_every=10,cells=None):
    root=Path(root);c=contract(root);plan=c['plan'];todo=tasks(plan,cells)
    if type(save_every) is not int or save_every<1:raise ValueError('positive save interval')
    if max_updates is not None and (type(max_updates) is not int or max_updates<1):
        raise ValueError('positive bounded update count required')
    lock=root/'RUN.lock'
    fd=os.open(lock,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);os.close(fd)
    used=0
    try:
        for spec in todo:
            path=task_path(root,spec)
            seed=master(plan,spec['founder'],spec['visitor'],'prefix' if spec['stage']=='prefix' else 'fork')
            rng=rngs(seed)
            if path.exists():
                meta,arrays=read_snapshot(path,c['contract_sha256'])
                if meta['task']!=spec or meta['master']!=seed:raise ValueError('checkpoint task mismatch')
                if meta['current']==spec['end']:continue
                if not spec['start']<=meta['current']<spec['end']:raise ValueError('invalid checkpoint year')
                states=[state_at(arrays,t) for t in range(len(arrays['counts']))]
                for k in rng:rng[k].bit_generator.state=meta['rng'][k]
            else:
                parent=None
                if spec['stage']=='prefix':s=founder(spec['founder'])
                else:
                    pre=dict(spec,stage='prefix',budget=8.,start=0,end=35)
                    pm,pa=read_snapshot(task_path(root,pre),c['contract_sha256'])
                    if pm['current']!=35:raise ValueError('incomplete prefix')
                    s=state_at(pa,-1);parent=pm['payload_sha256']
                states=[s]
                meta=dict(task=spec,current=spec['start'],master=seed,
                    contract_sha256=c['contract_sha256'],parent_payload_sha256=parent,
                    target_I=float(founder(spec['founder']).alleles[:,1,:].mean()))
            cfg=configuration(spec['policy'],spec['budget']);full,sparse,none=visitors(spec['visitor'])
            for t in range(meta['current'],spec['end']):
                s=states[-1];v=full if t<5 else sparse if t<35 else none
                next_s,_=advance(s,reproduce(s,v,cfg),empty(s),cfg,rng,year=t,
                                  mutation_traits=(False,False,False))
                states.append(next_s);meta['current']=t+1;used+=1
                stop=max_updates is not None and used>=max_updates
                if stop or (t+1)%save_every==0 or t+1==spec['end']:
                    meta['rng']={k:g.bit_generator.state for k,g in rng.items()}
                    save_snapshot(path,meta,states)
                if stop:return dict(new_updates=used,complete=False,confirmation_seeds_consumed=0)
        return dict(new_updates=used,complete=len(todo)==54,confirmation_seeds_consumed=0)
    finally:lock.unlink()


def events(upper,target):
    g=e=None;last=None
    for t,u in enumerate(upper):
        if u is None:
            if e is None:e=t
        else:
            if e is not None:raise ValueError('resurrection after extinction')
            if not np.isfinite(u):raise ValueError('nonfinite trait')
            if last is not None and u>last+1e-12:raise ValueError('support increase')
            if g is None and u<target-1e-12:g=t
            last=u
    return dict(first_G=g,first_E=e,G_first=g is not None,E_first=e is not None and g is None)


def collect(root):
    root=Path(root);c=contract(root);p=c['plan'];loaded={};slots=0
    specs=tasks(p)
    if {x.name for x in (root/'states').glob('*.npz')}!={task_path(root,s).name for s in specs}:
        raise ValueError('incomplete or unexpected task inventory')
    for s in specs:
        m,a=read_snapshot(task_path(root,s),c['contract_sha256'])
        if m['task']!=s or m['current']!=s['end']:raise ValueError('incomplete task')
        states=[state_at(a,t) for t in range(len(a['counts']))]
        initial=founder(s['founder']);origin_map=initial.alleles.reshape(-1)
        for t,st in enumerate(states):
            year=s['start']+t
            if len(st.ids):
                if np.any(st.birth_years!=year) or np.any(st.mutation_flags):raise ValueError('invalid birth/mutation')
                if not np.array_equal(st.ids,np.arange(year*48,year*48+len(st.ids))):raise ValueError('invalid IDs')
                if np.any(st.allele_origin>=288) or not np.array_equal(st.alleles,origin_map[st.allele_origin]):
                    raise ValueError('genotype/origin mismatch')
            if t:
                prev=states[t-1]
                for loc in range(3):
                    if not set(st.alleles[:,loc,:].ravel())<=set(prev.alleles[:,loc,:].ravel()):
                        raise ValueError('new allele without mutation')
        if s['stage']=='prefix':
            for k in FIELDS:
                if not np.array_equal(getattr(states[0],k),getattr(initial,k)):raise ValueError('founder mismatch')
        else:
            pm,ps=loaded[(s['founder'],s['visitor'],s['policy'],'prefix')]
            if m['parent_payload_sha256']!=pm['payload_sha256']:raise ValueError('wrong fork ancestry')
            for k in FIELDS:
                if not np.array_equal(getattr(states[0],k),getattr(ps[-1],k)):raise ValueError('fork state mismatch')
        loaded[(s['founder'],s['visitor'],s['policy'],s['stage'])]=(m,states);slots+=len(states)
    g=np.zeros((3,3,2),dtype=np.int64);occ=np.zeros((3,3,2,2),dtype=np.int64)
    out=[]
    for pi,policy in enumerate(p['policies']):
        for bi,stage in enumerate(('B8','B4p5')):
            counts=dict(alive_accessible=0,alive_closed=0,extinct=0,genetic_first=0,extinction_first=0)
            for fi,f in enumerate(p['founders']):
                for vi,v in enumerate(p['visitors']):
                    _,pre=loaded[f,v,policy,'prefix'];m,s=loaded[f,v,policy,stage]
                    seq=pre+s[1:];upper=[float(x.alleles[:,1,:].max()) if len(x.ids) else None for x in seq]
                    ev=events(upper,m['target_I']);alive=upper[-1] is not None
                    closed=alive and upper[-1]<m['target_I']-1e-12
                    counts['alive_closed' if closed else 'alive_accessible' if alive else 'extinct']+=1
                    counts['genetic_first']+=int(ev['G_first']);counts['extinction_first']+=int(ev['E_first'])
                    if bi==0:g[fi,vi,pi]=int(ev['G_first'])
                    occ[fi,vi,pi,bi]=int(alive)
            out.append(dict(policy=policy,budget=p['budgets'][bi],**counts))
    return dict(status='TECHNICAL_PIPELINE_ONLY_NOT_SCIENTIFIC_EVIDENCE',
        confirmation_seeds_consumed=0,saved_genotype_censuses=slots,
        arms=out,genetic_loss_inputs=g.tolist(),occupancy_inputs=occ.tolist(),
        endpoint_analysis=summarize(contrasts(g,occ),margin=p['margin']))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('init','run','collect','budget'))
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--max-updates',type=int)
    args=parser.parse_args()
    if args.action=='init':answer=initialize(args.out,technical_plan())
    elif args.action=='run':answer=run(args.out,max_updates=args.max_updates)
    elif args.action=='collect':answer=collect(args.out)
    else:answer=budget(160,160)
    print(json.dumps(answer,sort_keys=True,indent=2,allow_nan=False))
