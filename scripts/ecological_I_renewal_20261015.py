"""Approved source-conditional I-mutation renewal; frozen native biology unchanged."""
import hashlib
import json
from collections import Counter
import numpy as np
from scripts import run_ecological_order_boundary_20261013 as old

NEW_MASK=(False,True,True)
OLD_MASK=(False,False,True)
SCHEDULED_UPDATES=923216
UPDATE_CAP=923232
CLASSES=('assurance_first','investment_first','near_simultaneous','assurance_only','investment_only','neither')

def digest(b):return hashlib.sha256(b).hexdigest()
def key(t):return f"{t['block']}_c{t['context']}_r{t['replicate']}"
def tasks():return old.tasks()
def references(ts):return [t for t in ts if t['context'] in (0,1) and t['replicate'] in (0,1)]
def check_inventory(ts):
    expected={key(t):t for t in tasks()}
    if len(ts)!=2304 or len({key(t) for t in ts})!=2304 or any(expected.get(key(t))!=t for t in ts):
        raise ValueError('complete original2304 inventory required')

def reserve(used,count):
    if type(used) is not int or type(count) is not int or min(used,count)<0 or used+count>UPDATE_CAP:
        raise ValueError('frozen native update cap')
    return used+count

def cell_readout(counts):
    if set(counts)!=set(CLASSES) or any(type(v) is not int or v<0 for v in counts.values()) or sum(counts.values())!=128:
        raise ValueError('all128 starts/six categories required')
    a,i=counts['assurance_first'],counts['investment_first']
    return dict(categories=counts,D=(a-i)/128,interval=old.interval(a,i,128))

def readout(rows,baseline):
    check_inventory([r['task'] for r in rows]);check_inventory([r['task'] for r in baseline])
    before={key(r['task']):r for r in baseline};cells=[]
    for context,(supply,composition) in enumerate(old.CONTEXTS):
        for block in old.BLOCKS:
            group=[r for r in rows if r['task']['context']==context and r['task']['block']==block]
            counts={c:sum(r['events']['category']==c for r in group) for c in CLASSES}
            delta=[(int(r['events']['category']=='assurance_first')-int(r['events']['category']=='investment_first'))-(int(before[key(r['task'])]['events']['category']=='assurance_first')-int(before[key(r['task'])]['events']['category']=='investment_first')) for r in group]
            cells.append(dict(block=block,context=context,supply=supply,composition=composition,starts=128,
                **cell_readout(counts),paired_D_change_descriptive=sum(delta)/128,
                I_incidence=sum(r['events']['I'] is not None for r in group),
                A_incidence=sum(r['events']['A'] is not None for r in group)))
    from scripts.read_ecological_order_boundary_20261013 import summarize
    original_rule=summarize(rows)
    return dict(cells=cells,supported_supply_pairs=original_rule['supported_supply_pairs'],supported_composition_pairs=original_rule['supported_composition_pairs'],
        scope='Two original fixed founders and original coupled histories, native I-mutation-enabled policy. Exposed prior controls; descriptive paired changes. Original null unchanged; no unique continuous threshold, pure-variance mediation, natural-order survival or independent-founder confirmation.')

def produce(task,modules,*,initial=None,horizon=200,renew=True):
    _,pop,reproduction,randomness,_,_=modules
    config,state,visitors=old.initial(task,modules) if initial is None else initial
    empty=pop.subset(state,np.array([],dtype=int))
    streams={n:randomness.stream(old.seed(task),n,0) for n in randomness.STREAM_IDS}
    saved={k:[] for k in old.FIELDS};offsets=[0];means=[];population=[];parents=[];parent_offsets=[0];returns=[];selection=[]
    for t in range(horizon+1):
        n=len(state.ids);population.append(n);offsets.append(offsets[-1]+n)
        means.append(state.alleles.mean(axis=(0,2)) if n else np.full(3,np.nan))
        for k in old.FIELDS:saved[k].append(getattr(state,k).copy())
        if t==horizon:break
        ledger=reproduction.reproduce(state,visitors,config)
        returns.append([float(getattr(ledger,k).sum()) for k in ('maternal','paternal','self_raw','self_viable','ovules','exported','delivered','outcross')])
        w=np.stack([ledger.outcross.sum(axis=0)/2,ledger.outcross.sum(axis=1)/2,ledger.self_viable]);total=w.sum();traits=state.alleles.mean(axis=2)
        selection.append(w@(traits-traits.mean(axis=0))/total if total else np.full((3,3),np.nan))
        state,info=pop.advance(state,ledger,empty,config,streams,year=t,mutation_traits=NEW_MASK if renew else OLD_MASK)
        parents.append(info['parentage']);parent_offsets.append(parent_offsets[-1]+len(info['parentage']))
    result={k:np.concatenate(v) for k,v in saved.items()}
    result.update(offsets=np.array(offsets),means=np.array(means),population=np.array(population),parentage=np.concatenate(parents),parent_offsets=np.array(parent_offsets),returns=np.array(returns),sexual_selection=np.array(selection))
    return result
