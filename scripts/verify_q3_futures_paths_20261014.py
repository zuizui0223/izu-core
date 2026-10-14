"""Separate native replay from original state and seed; does not import producer."""
import hashlib
import json
from pathlib import Path
import time

import numpy as np

from q3_futures_contract_20261014 import FIELDS, arrays, checked_bytes, load_native, require


def validate_layout(a, start, end=200):
    off, po = a['offsets'], a['parent_offsets']
    require(off.dtype.kind in 'iu' and off.shape==(end-start+2,) and off[0]==0 and np.all(np.diff(off)>=0), 'census offsets')
    require(po.dtype.kind in 'iu' and po.shape==(end-start+1,) and po[0]==0 and np.all(np.diff(po)>=0), 'parent offsets')
    require(off[-1]==len(a['ids']) and po[-1]==len(a['parentage']), 'array lengths')
    require(np.all(np.diff(off)<=48), 'capacity')
    count=len(a['ids'])
    for field in ('alleles','allele_origin','mutation_flags'):
        require(a[field].shape==(count,3,2), 'diploid field shape')
    require(a['birth_years'].shape==(count,) and a['parentage'].shape==(int(po[-1]),3), 'age/parent shape')
    require(a['ids'].dtype.kind in 'iu' and a['birth_years'].dtype.kind in 'iu' and a['parentage'].dtype.kind in 'iu', 'identity dtype')
    require(a['allele_origin'].dtype.kind in 'iu' and a['mutation_flags'].dtype==np.dtype(bool), 'provenance dtype')
    require(np.isfinite(a['alleles']).all() and (a['alleles']>=0).all() and (a['alleles']<=1).all(), 'allele bounds')
    for j,year in enumerate(range(start,end+1)):
        lo,hi=map(int,off[j:j+2]);ids=a['ids'][lo:hi]
        require(len(np.unique(ids))==len(ids) and np.all(a['birth_years'][lo:hi]<=year), 'identity/age')
        if year<end:
            p=a['parentage'][po[j]:po[j+1]]
            next_ids=a['ids'][off[j+1]:off[j+2]]
            require(np.array_equal(p[:,0],next_ids) and np.isin(p[:,1:],ids).all(), 'parent-child identity')


def mean_path(a):
    result=[]
    for lo,hi in zip(a['offsets'][:-1],a['offsets'][1:]):
        result.append(float(a['alleles'][lo:hi,1].mean()) if hi>lo else None)
    return result


def independent_event(values, baseline):
    for start in range(len(values)-19):
        segment=values[start:start+20]
        if all(v is not None and baseline-v>=.05 for v in segment):
            return start
    return None


def verify_pair(case, replicate, out, execution_sha, deadline, saved):
    out=Path(out)
    original=arrays(checked_bytes(out/'original'/(case['key']+'.npz'),case['original_npz_sha256']))
    meta=json.loads(str(original['metadata']))
    types,pop,repro,randomness=load_native(out/'frozen_source')
    cfg=types.Config.from_dict(meta['config'])
    campaign=json.loads((out/'campaign.json').read_text())
    optima=campaign['compositions'][meta['task']['composition']]
    visitors=types.VisitorState(np.arange(len(optima),dtype=np.int64),np.asarray(optima),np.full(len(optima),.2),np.ones(len(optima)))
    trigger=case['trigger'];lo,hi=original['offsets'][trigger:trigger+2]
    expected_seed=int.from_bytes(hashlib.sha256(('izu-q3-conditional-restoration-v1-20261014\0'+case['key']+'\0'+str(replicate)).encode()).digest()[:16],'big')
    require(str(expected_seed)==case['pair_seeds'][replicate], 'independent seed disagreement')
    prefix=mean_path(original)[:trigger]
    baseline=float(original['alleles'][original['offsets'][0]:original['offsets'][1],1].mean())
    result=dict(key=case['key'],replicate=replicate,block=case['block'],trigger=trigger,
                baseline=baseline,native_updates=0,state_field_checks=0,parent_checks=0,artifacts=saved)
    for arm in ('native','restored'):
        raw=checked_bytes(out/'raw'/saved[arm]['name'],saved[arm]['sha256'])
        a=arrays(raw);record=json.loads(str(a['metadata']))
        require(record==dict(key=case['key'],replicate=replicate,arm=arm,trigger=trigger,seed=str(expected_seed),
                            original_sha256=case['original_npz_sha256'],execution_sha256=execution_sha), 'raw metadata identity')
        validate_layout(a,trigger)
        fields={k:original[k][lo:hi].copy() for k in FIELDS}
        v=float(fields['alleles'][0,1,0])
        if arm=='restored':
            fields['alleles'][:,1,0]=v-.0625
            fields['alleles'][:,1,1]=v+.0625
        state=types.PlantState(**fields)
        empty=types.PlantState(**{k:getattr(state,k)[:0].copy() for k in FIELDS})
        streams={n:randomness.stream(expected_seed,n,0) for n in randomness.STREAM_IDS}
        for j,year in enumerate(range(trigger,201)):
            require(time.monotonic()<deadline and not (out/'ABORT').exists(),'execution deadline/abort')
            a0,a1=a['offsets'][j:j+2]
            for field in FIELDS:
                require(np.array_equal(getattr(state,field),a[field][a0:a1]),'independent state replay mismatch: '+field)
                result['state_field_checks']+=1
            copies=a['alleles'][a0:a1,1]
            require(np.all(copies==v) if arm=='native' else np.all((copies==v-.0625)|(copies==v+.0625)), 'I support drift')
            if year==200:break
            state,info=pop.advance(state,repro.reproduce(state,visitors,cfg),empty,cfg,streams,
                                   year=year,mutation_traits=(False,False,True))
            p0,p1=a['parent_offsets'][j:j+2]
            require(np.array_equal(info['parentage'],a['parentage'][p0:p1]),'independent parentage replay mismatch')
            result['native_updates']+=1;result['parent_checks']+=1
        means=mean_path(a)
        result[arm+'_I']=means[-1]
        result[arm+'_survived']=means[-1] is not None
        event=independent_event(prefix+means,baseline)
        result[arm+'_event']=event
        result[arm+'_event_already_complete']=event is not None and event+19<=trigger
    require(result['native_updates']==2*(200-trigger),'independent replay count')
    return result
