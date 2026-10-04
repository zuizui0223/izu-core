"""Bound ecological weighting error before allocating its expanded core.

Joint genotype dependence is retained; no positivity or roundoff guarantee.
"""
from math import prod,sqrt
import numpy as np
from scripts.model3_compressed_step import contract,check_size


def bounded_weighted(state,xy,assurance,maps,*,absolute_l1,budget=2_000_000):
    core,factors=state;core=np.asarray(core,dtype=float)
    fs=[np.asarray(f,dtype=float) for f in factors];xy=np.asarray(xy,dtype=float)
    if not np.isfinite(absolute_l1) or absolute_l1<=0:
        raise ValueError('positive finite absolute L1 budget required')
    if core.ndim!=3 or not core.size or len(fs)!=3 or not np.isfinite(core).all():
        raise ValueError('finite joint core required')
    for k,f in enumerate(fs):
        if f.ndim!=2 or not f.size or f.shape[1]!=core.shape[k] or not np.isfinite(f).all():
            raise ValueError('factor dimensions invalid')
        check_size(f.size,budget)
    if xy.ndim!=2 or not xy.size or not np.isfinite(xy).all() or len(maps)!=2:
        raise ValueError('finite XY weight and two maps required')
    check_size(xy.size,budget)
    indices=[np.asarray(m) for m in maps]
    for k,m in enumerate(indices):
        if m.shape!=(fs[k].shape[0],) or m.dtype.kind not in 'iu' or m.min()<0 or m.max()>=xy.shape[k]:
            raise ValueError('invalid weight map')
    a=np.broadcast_to(np.asarray(assurance,dtype=float),(fs[2].shape[0],))
    if not np.isfinite(a).all():raise ValueError('finite assurance weights required')
    p=min(xy.shape)
    for k in range(2):check_size(fs[k].shape[0]*core.shape[k]*p,budget)
    u,s,v=np.linalg.svd(xy,full_matrices=False)
    raw=[(fs[k][:,:,None]*w[indices[k],None,:]).reshape(fs[k].shape[0],-1)
         for k,w in enumerate((u*s,v.T))]
    third=fs[2]*a[:,None]
    svds=[np.linalg.svd(f,full_matrices=False) for f in raw]
    leading=[float(s[0]) for u,s,v in svds]
    prefactor=sqrt(prod(f.shape[0] for f in fs))*sqrt(p)*float(np.linalg.norm(core))*prod(leading)*float(np.linalg.norm(third,2))
    if not np.isfinite(prefactor):raise ArithmeticError('nonfinite bound')
    if prefactor==0:
        return (np.zeros((1,1,1)),tuple(np.zeros((f.shape[0],1)) for f in fs)),dict(absolute_l1_bound=0.,ranks=[1,1,1])
    limit=absolute_l1/(2*prefactor);bases=[];transforms=[];tails=[]
    for k,((u,s,v),scale) in enumerate(zip(svds,leading)):
        rank=max(1,int(np.flatnonzero(np.r_[s/scale,0.]<=limit)[0]))
        bases.append(u[:,:rank]);transforms.append((s[:rank,None]*v[:rank]).reshape(rank,core.shape[k],p))
        tails.append(float(s[rank]/scale) if rank<len(s) else 0.)
    bound=prefactor*sum(tails)
    if bound>absolute_l1:raise ArithmeticError('weighting bound exceeds tolerance')
    result=contract('abc,ias,jbs->ijc',core,*transforms,budget=budget)
    return (result,tuple(bases+[third])),dict(absolute_l1_bound=bound,ranks=list(result.shape),prefactor=prefactor,
        bound_scope='exact-arithmetic factor truncation; excludes roundoff')
