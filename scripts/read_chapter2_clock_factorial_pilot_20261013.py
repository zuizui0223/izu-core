"""Independent original-operator admission of a *completed* pilot provider ZIP.

This readback imports no producer / event-reader helper. It replays every
registered parent lottery and diploid birth using the original Model3 code,
independently calculates six event categories, and refuses partial shards.
No re-run or reinterpretation of failed original experiments.
"""
from __future__ import annotations
import argparse
from dataclasses import asdict
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile
import numpy as np

from scripts.audit_chapter2_clock_native_birth_technical_20261013 import (
    FIELDS, MUTATION_MASK, load_original_source, source_fixture,
    initial_state, visitor_and_config,
)

REGISTRY=Path('data/design/chapter2_clock_factorial_pilot_registered_inputs_20261013.json')
REGISTRY_BLOB='0721517f7bf69eee1c2daf040f4781873ba3c3ea'
CASE=re.compile(r'^(main|confirmation)_c([034])_w(24|40)_i([01])_r(\d{3})$')
RETURN=('maternal','paternal','self_raw','self_viable','ovules','exported','delivered','outcross')
CATEGORIES=('assurance_first','investment_first','near_simultaneous','assurance_only','investment_only','neither')
TECH_SALT='chapter2-clock-factorial-producer-debug-only-20261013'


def hashbytes(raw):return hashlib.sha256(raw).hexdigest()


def git_blob(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()


def one_events(means,census,threshold):
    if len(census)!=201 or means.shape!=(201,3):raise ValueError('Full official 200 updates required')
    labels=[]
    for axis,sign in ((2,1),(1,-1)):
        start=None
        for t in range(201-19):
            if all(census[j]>0 and sign*(means[j,axis]-means[0,axis])>=threshold
                   for j in range(t,t+20)):
                start=t;break
        labels.append(start)
    a,i=labels
    if a is None:cat='investment_only' if i is not None else 'neither'
    elif i is None:cat='assurance_only'
    elif abs(a-i)<=5:cat='near_simultaneous'
    else:cat='assurance_first' if a<i else 'investment_first'
    return {'A':a,'I':i,'category':cat}


def decode_case(key):
    match=CASE.fullmatch(key)
    if not match:raise ValueError('Bad source-registered pilot case ID')
    b,c,w,h,rep=match.groups()
    return {'key':key,'block':b,'context':int(c),'width':int(w)/512,
            'hidden':float(h),'replicate':int(rep)}


def source_inventory():
    raw=REGISTRY.read_bytes()
    if git_blob(raw)!=REGISTRY_BLOB:raise ValueError('Source pilot registry Git blob differs')
    d=json.loads(raw)
    if (d['n_cases'],d['cluster_count'],d['n_updates_if_executed'])!=(1536,128,307200):
        raise ValueError('Wrong frozen source registry dimensions')
    return d


def archive_read_one(z,task,receipt,identity,fixture,modules,registered,*,technical=False):
    horizon=3 if technical else 200
    raw=z.read(task['key']+'.npz')
    if hashbytes(raw)!=receipt['case_sha256']:raise ValueError('Original saved case SHA mismatch')
    with np.load(io.BytesIO(raw),allow_pickle=False) as data:
        meta=json.loads(str(data['metadata'].item()))
        if meta['identity']!=identity or meta['case']!=task:
            raise ValueError('Native source/output identity metadata differs')
        if meta['metadata']['task']!=task or meta['metadata']['mutation_traits']!=list(MUTATION_MASK):
            raise ValueError('Source producer full-case mutation/task metadata drift')
        if meta['metadata']['runtime_numpy']!=identity['numpy_runtime'] or (not technical and meta['metadata']['runtime_numpy']!='2.2.6'):
            raise ValueError('Unregistered output numerical runtime')
        expected={'ids','alleles','allele_origin','mutation_flags','birth_years',
                  'offsets','means','population','parentage','parent_offsets','returns','sexual_selection','metadata'}
        if set(data.files)!=expected:raise ValueError('Original annual-record field inventory')
        a={k:data[k] for k in data.files if k!='metadata'}
    if len(a['population'])!=horizon+1 or a['offsets'].shape!=(horizon+2,) or a['parent_offsets'].shape!=(horizon+1,):
        raise ValueError('Original full annual census/parent offsets missing')
    if len(a['returns'])!=horizon or a['returns'].shape!=(horizon,8) or a['sexual_selection'].shape!=(horizon,3,3):
        raise ValueError('Original full reproductive/genetic response inventory missing')
    if a['population'][0]!=48 or np.any(a['population']<0) or np.any(a['population']>48):
        raise ValueError('Original genotype model K48 count inventory')
    if not np.array_equal(np.diff(a['offsets']),a['population']):
        raise ValueError('Recorded census offsets do not match populations')
    if len(a['parentage'])!=int(a['parent_offsets'][-1]) or not np.array_equal(np.diff(a['parent_offsets']),a['population'][1:]):
        raise ValueError('Recorded next-generation parentage inventory differs')
    initial,_=initial_state(fixture,task['block'],task['width'],task['hidden'],modules)
    expected={(r['block'],r['A_width'],r['I_hidden_homolog']):r for r in registered['genetic_treatments']}
    if hashbytes(initial.alleles.tobytes())!=expected[task['block'],task['width'],task['hidden']]['genotype_sha256']:
        raise ValueError('Source founding diploid genome does not match registry')
    cfg,vis,source_repro=visitor_and_config(fixture,task['block'],task['context'],modules)
    state=initial
    pop=modules['population'];repro=modules['reproduction'];randomness=modules['randomness']
    streams={name:randomness.stream(task['master'],name,0) for name in randomness.STREAM_IDS}
    empty=pop.subset(initial,np.array([],dtype=int))
    counts=[];selchecks=0;sourcechecks=0;statechecks=0;geneticchecks=0
    for t in range(horizon+1):
        lo=int(a['offsets'][t]);hi=int(a['offsets'][t+1]);n=hi-lo
        if len(state.ids)!=n:raise ValueError('Replayed population census differs')
        for field in FIELDS:
            if not np.array_equal(getattr(state,field),a[field][lo:hi]):
                raise ValueError('Independently replayed diploid genotype/parent/birth field differs: '+field)
            statechecks+=1
        if len(set(map(int,state.ids)))!=n:raise ValueError('Original unique genome IDs')
        if n:
            np.testing.assert_allclose(state.alleles.mean(axis=(0,2)),a['means'][t],atol=1e-14,rtol=0)
        elif not np.isnan(a['means'][t]).all():raise ValueError('Extinct genotype means must be missing')
        if t==horizon:break
        ledger=repro.reproduce(state,vis,cfg)
        values=np.array([float(np.asarray(getattr(ledger,k)).sum()) for k in RETURN])
        np.testing.assert_allclose(values,a['returns'][t],atol=1e-10,rtol=0)
        if t==0:np.testing.assert_allclose(values,source_repro,atol=1e-12,rtol=0)
        sourcechecks+=1
        w=np.stack((ledger.outcross.sum(axis=0)/2,ledger.outcross.sum(axis=1)/2,ledger.self_viable))
        total=float(w.sum())
        traits=state.alleles.mean(axis=2) if n else np.zeros((0,3))
        selection=w@(traits-traits.mean(axis=0))/total if total>0 else np.full((3,3),np.nan)
        np.testing.assert_allclose(selection,a['sexual_selection'][t],atol=1e-12,rtol=0,equal_nan=True)
        selchecks+=1
        child,info=pop.advance(state,ledger,empty,cfg,streams,year=t,mutation_traits=MUTATION_MASK)
        s,e=map(int,a['parent_offsets'][t:t+2])
        if not np.array_equal(info['parentage'],a['parentage'][s:e]):
            raise ValueError('Original recorded child/father/mother pair differs')
        if (info['immigrant_recruits'],info['survivors'])!=(0,0):
            raise ValueError('Immigration/adult survival unexpectedly permitted')
        if info['resident_recruits']!=len(child.ids):raise ValueError('Resident birth-count accounting')
        geneticchecks+=1
        state=child
    events=None if technical else {str(th):one_events(a['means'],a['population'],th) for th in (.025,.05,.1)}
    if not technical and receipt.get('events')!=events:raise ValueError('Independent six-class original threshold readout mismatch')
    if technical and 'events' in receipt:raise ValueError('Technical smoke must not report evolution outcomes')
    if receipt['censuses']!=horizon+1 or receipt['parentage_events']!=len(a['parentage']):
        raise ValueError('Original independent source lengths differ')
    return {'key':task['key'],'events':None if technical else events['0.05'],'censuses':horizon+1,
            'parentage_events':len(a['parentage']),'state_field_checks':statechecks,
            'native_reproduction_checks':sourcechecks,'native_selection_checks':selchecks,
            'native_parentage_checks':geneticchecks}


def admit(shard:int,archive:Path,*,technical:bool=False)->dict:
    if not technical and np.__version__!='2.2.6':raise ValueError('Historical original source replay requires exact NumPy 2.2.6')
    if not isinstance(shard,int) or shard not in range(6):raise ValueError('Only six registered shards')
    registry=source_inventory()
    fixture=source_fixture()
    modules=load_original_source()
    block=('main','confirmation')[shard//3];ctx=(0,3,4)[shard%3]
    expected=[k for k in registry['pilot_case_keys'] if decode_case(k)['block']==block and decode_case(k)['context']==ctx
              and (not technical or decode_case(k)['replicate']==0)]
    nexpected=4 if technical else 256
    if len(expected)!=nexpected:raise ValueError('Incomplete source shard roster')
    clusters={(c['block'],c['replicate']):int(c['master']) for c in registry['rng_clusters']}
    result=[];counts=Counter()
    with zipfile.ZipFile(archive) as z:
        members=z.namelist()
        if len(members)!=nexpected+3 or len(members)!=len(set(members)):
            raise ValueError('Missing or duplicate original 256-case ZIP members')
        if set(members)!={x+'.npz' for x in expected}|{'REGISTRATION.json','_COMPLETION.json','EXECUTION_COMMIT.txt'}:
            raise ValueError('Unregistered source ZIP payload')
        registered=json.loads(z.read('REGISTRATION.json'))
        complete=json.loads(z.read('_COMPLETION.json'))
        required_status=('TECHNICAL_ONLY_CLOCK_FACTORIAL_SHARD' if technical else 'COMPLETE_FROZEN_CLOCK_FACTORIAL_SHARD')
        if complete['status']!=required_status or complete['cases']!=nexpected:
            raise ValueError('Incomplete original pilot shard')
        if complete['identity']!=registered['identity'] or registered['expected']!=nexpected:
            raise ValueError('Original cohort registration/producer identity drift')
        identity=complete['identity']
        if identity['technical']!=technical or identity['numpy_runtime']!=np.__version__ or identity['input_registry_git_blob']!=REGISTRY_BLOB:
            raise ValueError('Provider is not registered original source pilot')
        if identity['model_git_blobs']!=registry['original_source_git_blobs']:
            raise ValueError('Original source biological modules differ')
        if z.read('EXECUTION_COMMIT.txt').decode().strip()!=identity['execution_commit']:
            raise ValueError('Original producer execution commit lost')
        tasks={x['key']:x for x in registered['tasks']}
        receipts={x['task']['key']:x for x in complete['records']}
        if set(tasks)!=set(expected) or set(receipts)!=set(expected):
            raise ValueError('Original case coverage or tuple registration incomplete')
        for key in expected:
            task=tasks[key]
            original=decode_case(key)
            if any(task[k]!=original[k] for k in original):raise ValueError('Unregistered genetic case factor')
            required_master=(int.from_bytes(hashlib.sha256((TECH_SALT+'\0'+key).encode()).digest()[:16],'big')
                             if technical else clusters[original['block'],original['replicate']])
            if task['master']!=required_master:raise ValueError('Pilot/technical history master seed changed')
            if receipts[key]['task']!=task:raise ValueError('Registered case/receipt mismatch')
            if receipts[key]['mutation_mask']!=list(MUTATION_MASK):raise ValueError('Unexpected I/M mutation')
            row=archive_read_one(z,task,receipts[key],identity,fixture,modules,registry,technical=technical)
            result.append(row)
            if not technical:counts[row['events']['category']]+=1
    if not technical and sum(counts.values())!=nexpected:raise ValueError('Original six-class all-start denominator changed')
    return {'schema':'chapter2_clock_pilot_independent_original_source_replay_v1',
            'status':'TECHNICAL_FOUR_CASES_ORIGINAL_BIRTHS_ADMITTED' if technical else 'ALL256_ORIGINAL_SOURCE_GENOME_COHORT_ADMITTED',
            'shard':shard,'source_zip_sha256':hashbytes(archive.read_bytes()),
            'source_member_count':nexpected+3,'cases':nexpected,'updates':nexpected*(3 if technical else 200),
            'category_counts':{k:counts[k] for k in CATEGORIES},
            'source_field_checks':sum(x['state_field_checks'] for x in result),
            'birth_parent_checks':sum(x['native_parentage_checks'] for x in result),
            'reproductive_checks':sum(x['native_reproduction_checks'] for x in result),
            'selection_checks':sum(x['native_selection_checks'] for x in result),
            'provenance':{'execution_commit':identity['execution_commit'],
                          'input_registry_blob':REGISTRY_BLOB,
                          'original_biology_blobs':registry['original_source_git_blobs']},
            'new_biological_histories_generated_by_reader':0,
            'technical_only':technical,
            'independent_pilot_confirmation_claim':False}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--shard',type=int,required=True)
    p.add_argument('--archive',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--technical',action='store_true')
    args=p.parse_args()
    r=admit(args.shard,args.archive,technical=args.technical)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open('x',encoding='utf8',newline='\n') as f:
        f.write(json.dumps(r,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':r['status'],'shard':r['shard'],'cases':r['cases']}))

if __name__=='__main__':main()
