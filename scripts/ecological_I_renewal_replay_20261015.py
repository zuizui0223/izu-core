"""Independent scratch trajectory consumer; shares frozen native kernels only."""
import hashlib
import numpy as np

FIELDS=('ids','alleles','allele_origin','mutation_flags','birth_years')

def independent_seed(task):
    pieces=[b'ecological-order-v1-20261013',task['block'].encode(),str(task['replicate']).encode(),b'0']
    return int.from_bytes(hashlib.sha256(bytes([0]).join(pieces)).digest()[:16],'big')

def replay(task,initial,modules,*,horizon=200):
    types,pop,reproduction,randomness,_,_=modules
    config,source,visitors=initial
    state=types.PlantState(**{k:getattr(source,k).copy() for k in FIELDS})
    master=independent_seed(task)
    streams={n:randomness.stream(master,n,0) for n in randomness.STREAM_IDS}
    empty=pop.subset(state,np.array([],dtype=int))
    records={k:[] for k in FIELDS};sizes=[];edges=[0];centres=[];parent_records=[];parent_edges=[0];totals=[];responses=[]
    for census in range(horizon+1):
        sizes.append(len(state.ids));edges.append(edges[-1]+len(state.ids))
        for k in FIELDS:records[k].append(getattr(state,k).copy())
        centres.append(state.alleles.mean((0,2)) if len(state.ids) else np.full(3,np.nan))
        if census==horizon:break
        ledger=reproduction.reproduce(state,visitors,config)
        totals.append([float(getattr(ledger,n).sum()) for n in ('maternal','paternal','self_raw','self_viable','ovules','exported','delivered','outcross')])
        weights=np.stack((ledger.outcross.sum(0)/2,ledger.outcross.sum(1)/2,ledger.self_viable));denom=weights.sum()
        traits=state.alleles.mean(2)
        responses.append(weights@(traits-traits.mean(0))/denom if denom else np.full((3,3),np.nan))
        state,info=pop.advance(state,ledger,empty,config,streams,year=census,mutation_traits=(False,True,True))
        parent_records.append(info['parentage']);parent_edges.append(parent_edges[-1]+len(info['parentage']))
    data={k:np.concatenate(v) for k,v in records.items()}
    data.update(population=np.asarray(sizes),offsets=np.asarray(edges),means=np.asarray(centres),parentage=np.concatenate(parent_records),parent_offsets=np.asarray(parent_edges),returns=np.asarray(totals),sexual_selection=np.asarray(responses))
    return data
