"""Response-blind visitor interventions; frozen reproduction is unchanged."""
from dataclasses import replace
import numpy as np
from scripts.model3_island.types import VisitorState


def _compatible(histories):
    if not histories or any(len(h.visitors)!=len(histories[0].visitors) or h.event_order!=histories[0].event_order for h in histories):
        raise ValueError('history length and reproductive order must agree')


def richness_match(a,b,*,seed):
    """Uniformly thin each annual visitor set to the smaller size, before reproduction.

    This deliberately changes turnover as well as count. No plant or outcome is
    accepted by this interface. Empty matched years are retained as intervention.
    """
    _compatible([a,b]);paths=[[],[]];counts=[]
    for year,(va,vb) in enumerate(zip(a.visitors,b.visitors)):
        n=min(len(va.ids),len(vb.ids));counts.append(n)
        for arm,v in enumerate((va,vb)):
            rng=np.random.default_rng(np.random.SeedSequence([int(seed),92731,year,arm]))
            ix=np.sort(rng.choice(len(v.ids),n,replace=False))
            paths[arm].append(VisitorState(v.ids[ix],v.optima[ix],v.breadths[ix],v.effectiveness[ix]))
    return replace(a,visitors=tuple(paths[0])),replace(b,visitors=tuple(paths[1])),dict(
        matched_counts=counts,empty_matched_years=counts.count(0),
        ceiling='annual thinning also changes identity persistence; not a pure count intervention')


def pool_histories(histories):
    """Pool same-year independent visitor communities, retaining first seed schedule.

    Caller must scale reference_visitor_count by number pooled in count_scaled
    mode. This is an environmental averaging diagnostic, not lifespan or islands.
    """
    _compatible(histories);path=[]
    for year in range(len(histories[0].visitors)):
        vs=[h.visitors[year] for h in histories]
        ids=np.concatenate([v.ids for v in vs])
        if len(np.unique(ids))!=len(ids):raise ValueError('pooled visitor IDs overlap')
        path.append(VisitorState(ids,*[np.concatenate([getattr(v,key) for v in vs]) for key in ('optima','breadths','effectiveness')]))
    return replace(histories[0],visitors=tuple(path))


def prepare_arms(base,*,seed,pool_size=8):
    """Two island connectivities x four prespecified mechanism interventions."""
    from scripts.model3_island.run import history_from_spec
    if base.activity_mode!='count_scaled' or base.seed_arrival.supply!=0 or base.capacity!=48:
        raise ValueError('bridge requires count-scaled activity, closed plant population and capacity 48')
    if not isinstance(pool_size,int) or pool_size<1:raise ValueError('positive integer pool size required')
    configs=[replace(base,visitor_arrival=replace(base.visitor_arrival,distance=d)) for d in (0.,3.)]
    ensembles=[[history_from_spec(c,{'kind':'assembly'},seed+j*100000) for j in range(pool_size)] for c in configs]
    a,b=ensembles[0][0],ensembles[1][0]
    ma,mb,_=richness_match(a,b,seed=seed)
    out={}
    for c,h,m,ensemble,side in zip(configs,(a,b),(ma,mb),ensembles,('near','far')):
        out[side]=(c,h)
        out['matched_'+side]=(c,m)
        out['pool_'+side]=(replace(c,reference_visitor_count=c.reference_visitor_count*pool_size),pool_histories(ensemble))
        out['large_'+side]=(replace(c,capacity=192),h)
    return out
