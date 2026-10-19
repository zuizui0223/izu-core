"""Frozen exploratory demographic companion to PR597; NOT confirmation.

Pinned native Model3 operators; no source mutation or parameter fitting.
Replay every original case and verify event summaries before new futures.
All histories count, including extinct ones. No restored-pollinator futures.
"""
from __future__ import annotations
import argparse
from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path
import platform
import numpy as np
from scripts.model3_island.types import Config, PlantState, VisitorState
from scripts.model3_island.randomness import stream, STREAM_IDS
from scripts.model3_island.history import reflect_unit
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.population import advance
from scripts.audit_chapter2_equalA_precision_20261018 import exact_pigeonhole, variance_components

ROOT=Path(__file__).resolve().parents[1]
EVENTS=ROOT/'docs/audits/CHAPTER2_EQUALA_PILOT_EVENT_SOURCE_20261018.json'
FROZEN=ROOT/'docs/protocols/CHAPTER2_BUDGET_COMPANION_EXPLORATORY_FROZEN_20261018.json'
FREEZE_COMMIT='0c5b549888b130b086c171fc2be2ed5924dfe66b'
NATIVE_SHA={
 'types.py':'a572e1e7f4fded181585871a63582b16f40292bd07b13e8efc9d6b6234eb21c5',
 'randomness.py':'63522ae3c5ff8e11f114b5649a989945fa4ba2480fdca0f74857601b0e4b211f',
 'history.py':'28d22c7fde81d9be6a604fa9dd4cb6b48d78d388d4db85f798a935cf81415488',
 'population.py':'c959d18816da6666dbfb4e91bd9582c94af5453b25498d033f5747305b05fe0f',
 'reproduction.py':'885957edb8a165ee8528781ed1d2574c44143c608496b505f9663cbfac2c4081',
}
FIELDS=('alleles','allele_origin','mutation_flags','ids','birth_years')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def validate_native_sources():
    actual={n:sha(ROOT/'scripts/model3_island'/n) for n in NATIVE_SHA}
    if actual!=NATIVE_SHA: raise ValueError('native source bytes differ from pinned producer')
    return actual


def validate_design():
    d=json.loads(FROZEN.read_text())
    expect={'checkpoint':35,'followup_updates':45,'budget_arms':[8.0,4.5],
            'unique_source_histories':144,'new_future_paths':288,'max_new_future_updates':12960,
            'new_future_master_seed_prefix':[20261018,90]}
    if any(d[k]!=v for k,v in expect.items()):raise ValueError('frozen scope changed')
    if d['source_founders']!=list(range(301001,301007)) or d['source_visitors']!=list(range(302001,302007)):
        raise ValueError('source axes changed')
    return d


def make_config(policy,budget=8.0):
    """Exact source base_config after the equal-A pilot overrides, explicit here."""
    if policy not in ('fixed','evolving') or budget not in (8.,4.5):
        raise ValueError('unsupported policy or unregistered budget')
    d=dict(schema_version=1,event_order='reproduce-survive-arrive-recruit-v1',
        time_unit='reproductive_year',capacity=48,years=80,survival=0.,ovule_budget=budget,
        pollen_budget=20.,investment_cost=.5,pollen_scale=1.,depression=.5,
        mutation_rate=0.,mutation_sd=.025,assurance_mode=policy,fixed_assurance=.5,
        assurance_timing='delayed',pollen_discount=0.,assurance_cost=.5,
        activity=.4,activity_mode='count_scaled',reference_visitor_count=4.,
        background_ratio=1.,background_resources=1.,island_history='founding',initial_visitors=4,
        visitor_breadth=.2,visitor_effectiveness=1.,source_allele_means=[.5,.5,.5],source_allele_sd=.15,
        seed_arrival=dict(supply=0.,distance=1.,scale=1.,kernel='exponential',establishment=.5,loss_hazard=0.),
        visitor_arrival=dict(supply=0.,distance=1.,scale=1.,kernel='exponential',establishment=.8,loss_hazard=.05))
    return Config.from_dict(d)


def make_founders(seed):
    """Reproduce source RNG consumption, then its balanced A-carrier construction."""
    n=48;rng=stream(seed,'founders',0)
    a=reflect_unit(np.array([.5,.5,.5])[None,:,None]+rng.normal(0,.08,(n,3,2)))
    a[:,1,:]=rng.choice(np.array([.375,.5,.625]),size=(n,2))
    a[:,2,:]=rng.choice(np.array([.25,.5,.75]),size=(n,2))
    first=np.tile(np.array([.25,.5,.75]),16)
    np.random.default_rng((seed+39110)%(2**32)).shuffle(first)
    a[:,2,0]=first;a[:,2,1]=1-first
    return PlantState(a,np.arange(n*6,dtype=np.int64).reshape(n,3,2),
        np.zeros((n,3,2),dtype=bool),np.arange(n,dtype=np.int64),np.zeros(n,dtype=np.int64))


def visitor_community(seed):
    rng=stream(seed,'visitor_initial',0);ids=np.arange(6,dtype=np.int64)+(seed+1)*100
    opts=rng.uniform(.3,.7,6)
    return (VisitorState(ids,opts,np.full(6,.2),np.ones(6)),
            VisitorState(ids[:1],opts[:1],np.full(1,.2),np.ones(1)),
            VisitorState(np.empty(0,dtype=np.int64),np.empty(0),np.empty(0),np.empty(0)))


def fresh_seed(fi,vi,rep):
    if any(type(x) is not int or not 0<=x<lim for x,lim in ((fi,6),(vi,6),(rep,2))):
        raise ValueError('source index outside frozen grid')
    return int(np.random.SeedSequence([20261018,90,fi,vi,rep]).generate_state(1)[0])


def streams(seed):
    return {name:stream(seed,name,0) for name in STREAM_IDS}


def empty_plants(st):
    return PlantState(**{n:getattr(st,n)[:0].copy() for n in FIELDS})


def step(st,vis,cfg,rng,t):
    ledger=reproduce(st,vis,cfg)
    child,_=advance(st,ledger,empty_plants(st),cfg,rng,year=t,mutation_traits=(False,False,False))
    if not len(st.ids) and len(child.ids):raise AssertionError('unallowed resurrection')
    if len(child.ids):
        for j in range(3):
            if not set(np.unique(child.alleles[:,j,:]))<=set(np.unique(st.alleles[:,j,:])):
                raise AssertionError('new allele without mutation/immigration')
    return child


def state_hash(st):
    h=hashlib.sha256()
    for name in FIELDS:
        a=getattr(st,name)
        h.update(name.encode()+str(a.shape).encode()+a.dtype.str.encode()+a.tobytes())
    return h.hexdigest()


def describe(st,cfg,t,target):
    n=len(st.ids)
    a=(st.alleles[:,2,:].mean(axis=1) if cfg.assurance_mode=='evolving' else np.full(n,.5))
    return dict(t=t,n=n,alive=bool(n),
        mean_I=float(st.alleles[:,1,:].mean()) if n else None,
        max_I=float(st.alleles[:,1,:].max()) if n else None,
        mean_A=float(a.mean()) if n else None,
        accessible=bool(st.alleles[:,1,:].max()>=target-1e-12) if n else None)


def replay_history(fi,vi,rep,policy):
    initial=make_founders(301001+fi);full,sparse,empty=visitor_community(302001+vi)
    cfg=make_config(policy);target=float(initial.alleles[:,1,:].mean());a0=.5
    old_seed=int(np.random.SeedSequence([20261018,89,fi,vi,rep]).generate_state(1)[0])
    rng=streams(old_seed);st=initial;g=None;ga=None;snap=None
    for t in range(81):
        if len(st.ids):
            if g is None and st.alleles[:,1,:].max()<target-1e-12:g=t
            if policy=='evolving' and ga is None and st.alleles[:,2,:].min()>a0+1e-12:ga=t
        if t==35:snap=st
        if t==80:break
        st=step(st,full if t<5 else sparse if t<35 else empty,cfg,rng,t)
    return dict(checkpoint=snap,target=target,first_I_loss=g,first_A_loss=ga,
                final_alive=bool(len(st.ids)),old_seed=old_seed)


def save_state(path,st):
    np.savez_compressed(path,**{n:getattr(st,n) for n in FIELDS})


def load_state(path):
    with np.load(path,allow_pickle=False) as z:
        return PlantState(**{n:z[n] for n in FIELDS})


def replay_all(out):
    validate_design();validate_native_sources()
    src=json.loads(EVENTS.read_text());out.mkdir(parents=True,exist_ok=False)
    records=[]
    for fi in range(6):
        for vi in range(6):
            for rep in range(2):
                for p in ('fixed','evolving'):
                    r=replay_history(fi,vi,rep,p)
                    if r['first_I_loss']!=src['first_I_loss_'+p][fi][2*vi+rep]:raise AssertionError('old I event mismatch')
                    if p=='evolving' and r['first_A_loss']!=src['first_A_loss_evolving'][fi][2*vi+rep]:raise AssertionError('old A event mismatch')
                    if not r['final_alive']:raise AssertionError('old survival mismatch')
                    snap=r.pop('checkpoint');sid=f'f{fi}v{vi}r{rep}_{p}'
                    save_state(out/(sid+'.npz'),snap)
                    records.append(dict(fi=fi,vi=vi,rep=rep,policy=p,id=sid,
                        checkpoint_sha256=state_hash(snap),checkpoint_n=len(snap.ids),**r))
        print('SOURCE_REPLAY_FOUNDER',fi,'passed',flush=True)
    doc=dict(status='144_ORIGINAL_EVENT_HISTORIES_REPRODUCED',source_events_sha256=sha(EVENTS),
        source_native_sha256=validate_native_sources(),freeze_commit=FREEZE_COMMIT,
        freeze_sha256=sha(FROZEN),python=platform.python_version(),numpy=np.__version__,records=records)
    (out/'SOURCE_REPLAY.json').write_text(json.dumps(doc,indent=2,allow_nan=False)+'\n')
    return doc


def follow_future(st,policy,budget,seed,target,first_loss):
    cfg=make_config(policy,budget);rng=streams(seed);empty=visitor_community(302001)[2]
    rows=[];raw=[];g=first_loss;death=None
    for t in range(35,81):
        d=describe(st,cfg,t,target);rows.append(d);raw.append(st)
        if d['alive'] and not d['accessible'] and g is None:g=t
        if not d['alive'] and death is None:death=t
        if t<80:st=step(st,empty,cfg,rng,t)
    first_kind=('genetic_loss' if g is not None and (death is None or g<death)
                else 'extinction' if death is not None else None)
    r=dict(final=rows[-1],first_I_loss=g,first_extinction=death,first_competing_event=first_kind,
           alive_accessible_censuses=sum(x['alive'] and x['accessible'] for x in rows),series=rows)
    return r,raw


def save_future(path,states):
    # Padded arrays use n[t] to delimit living rows; padding is never a phenotype.
    sizes=np.array([len(x.ids) for x in states],dtype=np.int16);nmax=48
    data={'n':sizes}
    for name in FIELDS:
        ref=getattr(states[0],name);shape=(len(states),nmax)+ref.shape[1:]
        fill=np.nan if name=='alleles' else False if name=='mutation_flags' else -1
        arr=np.full(shape,fill,dtype=ref.dtype)
        for i,st in enumerate(states):arr[i,:sizes[i]]=getattr(st,name)
        data[name]=arr
    np.savez_compressed(path,**data)


def run_futures(source_dir,out):
    validate_design();validate_native_sources()
    src=json.loads((source_dir/'SOURCE_REPLAY.json').read_text())
    if len(src['records'])!=144 or src['freeze_sha256']!=sha(FROZEN):raise ValueError('unadmitted source')
    out.mkdir(parents=True,exist_ok=False);events=[]
    for k,r in enumerate(src['records']):
        st=load_state(source_dir/(r['id']+'.npz'))
        if state_hash(st)!=r['checkpoint_sha256']:raise ValueError('checkpoint corrupted')
        seed=fresh_seed(r['fi'],r['vi'],r['rep'])
        for budget in (8.,4.5):
            before=state_hash(st)
            # Carry any already-occurred genetic loss forward; never discard it.
            g=r['first_I_loss'] if r['first_I_loss'] is not None and r['first_I_loss']<=35 else None
            future,raw=follow_future(st,r['policy'],budget,seed,r['target'],g)
            if state_hash(st)!=before:raise AssertionError('mutated shared checkpoint')
            name=r['id']+'_B'+str(budget)
            save_future(out/(name+'.npz'),raw)
            events.append(dict(fi=r['fi'],vi=r['vi'],rep=r['rep'],policy=r['policy'],budget=budget,
                source_checkpoint_sha256=before,target=r['target'],future_seed=seed,
                raw_npz=name+'.npz',raw_sha256=sha(out/(name+'.npz')),**future))
        if (k+1)%24==0:print('FUTURES_SOURCE_COUNT',k+1,'of144',flush=True)
    doc=dict(status='EXPLORATORY_SAME_COHORT_BUDGET_COMPANION_NOT_CONFIRMATORY',
        freeze_commit=FREEZE_COMMIT,freeze_sha256=sha(FROZEN),source_replay_sha256=sha(source_dir/'SOURCE_REPLAY.json'),
        runner_sha256=sha(__file__),native_source_sha256=validate_native_sources(),
        paths=288,max_updates=12960,new_founder_draws=0,restored_pollinator_paths=0,
        python=platform.python_version(),numpy=np.__version__,records=events)
    (out/'FUTURES.json').write_text(json.dumps(doc,indent=2,allow_nan=False)+'\n')
    return doc


def assemble_summary(doc):
    rows=doc['records']
    if len(rows)!=288:raise ValueError('incomplete cohort')
    keys=[(x['fi'],x['vi'],x['rep'],x['policy'],x['budget']) for x in rows]
    expected={(f,v,r,p,b) for f in range(6) for v in range(6) for r in range(2) for p in ('fixed','evolving') for b in (8.,4.5)}
    if len(set(keys))!=288 or set(keys)!=expected:raise ValueError('duplicate or missing case')
    idx=dict(zip(keys,rows));arms={}
    for p in ('fixed','evolving'):
        for b in (8.,4.5):
            sub=[x for x in rows if x['policy']==p and x['budget']==b]
            alive=sum(x['final']['alive'] for x in sub)
            accessible=sum(x['final']['alive'] and x['final']['accessible'] for x in sub)
            arms[p+'_B'+str(b)]=dict(n=72,alive=alive,alive_accessible=accessible,alive_closed=alive-accessible,
                extinct=72-alive,genetic_loss_first=sum(x['first_competing_event']=='genetic_loss' for x in sub),
                extinction_first=sum(x['first_competing_event']=='extinction' for x in sub),
                mean_alive_accessible_censuses=sum(x['alive_accessible_censuses'] for x in sub)/72)
    differences={}
    for metric in ('survival','alive_accessible','accessible_census_count'):
        grid=np.zeros((6,6,2),dtype=int)
        for f in range(6):
            for v in range(6):
                for r in range(2):
                    def value(p,b):
                        x=idx[f,v,r,p,b]
                        if metric=='survival':return int(x['final']['alive'])
                        if metric=='alive_accessible':return int(x['final']['alive'] and x['final']['accessible'])
                        return x['alive_accessible_censuses']
                    grid[f,v,r]=(value('evolving',4.5)-value('fixed',4.5))-(value('evolving',8.)-value('fixed',8.))
        differences[metric]=dict(estimate=float(grid.mean()),exploratory_crossed_interval=exact_pigeonhole(grid),
            variance_components=variance_components(grid),by_founder=grid.mean((1,2)).tolist(),paired_scores=grid.tolist())
    return dict(status='EXPLORATORY_COMPANION_DESCRIPTIVE_NOT_CONFIRMATION',freeze_commit=FREEZE_COMMIT,
        source_history_count=144,future_count=288,founders=6,visitors=6,old_demographic_repeats=2,
        checkpoint=35,followup_updates=45,arms=arms,interaction_evolving_effect_under_challenge_minus_control=differences,
        limits=['Same source histories; not independent confirmation or 288 independent islands.',
        'Only budget manipulated in companion; no returning-pollinator evolution or genetic rescue.',
        'Positive survival interaction is whole historical-policy effect; no direct A-only mediation identified.',
        'Genetic access necessary bound, not realized recovery probability. Extinction kept separate.',
        'Bootstrap percentile intervals are exploratory; six independent levels per axis do not guarantee coverage.',
        'No #585-approved SESOI or prospective joint-power claim.'])


def main():
    p=argparse.ArgumentParser();p.add_argument('stage',choices=('replay','futures','summary'))
    p.add_argument('--source',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    if a.out.exists():p.error('refuse overwrite')
    if a.stage=='replay':replay_all(a.out)
    elif a.stage=='futures':run_futures(a.source,a.out)
    else:
        d=json.loads((a.source/'FUTURES.json').read_text());s=assemble_summary(d)
        a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(s,indent=2,allow_nan=False)+'\n')
        print(json.dumps({k:v for k,v in s.items() if k!='interaction_evolving_effect_under_challenge_minus_control'},indent=2))

if __name__=='__main__':main()
