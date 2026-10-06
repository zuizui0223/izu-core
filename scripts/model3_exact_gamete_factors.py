"""Exact square-gamete child bases; bounded SVD only on rectangular modes."""
from itertools import combinations_with_replacement
from math import prod,sqrt
import numpy as np

def reduce_gamete_factors(dc,rc,dg,rg,*,absolute_l1,max_values=2_000_000):
    if not np.isfinite(absolute_l1) or absolute_l1<=0:raise ValueError('positive error budget required')
    if not isinstance(max_values,int) or max_values<1:raise ValueError('positive resource budget required')
    if len(dg)!=3 or len(rg)!=3 or dc.ndim!=3 or rc.ndim!=3:raise ValueError('three joint modes required')
    if not np.isfinite(dc).all() or not np.isfinite(rc).all():raise ValueError('finite cores required')
    modes=[];leading=[];physical=[];exact=[]
    for k,(d,r) in enumerate(zip(dg,rg)):
        d=np.asarray(d);r=np.asarray(r)
        if d.ndim!=2 or r.ndim!=2 or d.shape[0]!=r.shape[0] or d.shape[1]!=dc.shape[k] or r.shape[1]!=rc.shape[k]:raise ValueError('gamete shape mismatch')
        n=len(d)
        for f in (d,r):
            if not np.isfinite(f).all() or not np.allclose(f.T@f,np.eye(f.shape[1]),rtol=0,atol=1e-12):raise ValueError('orthonormal gamete basis required')
        m=n*(n+1)//2
        if m*d.shape[1]*r.shape[1]>max_values:raise MemoryError('child factor exceeds resource budget')
        pairs=np.array(list(combinations_with_replacement(range(n),2)));a,b=pairs.T
        f=d[a,:,None]*r[b,None,:]
        f+=(a!=b)[:,None,None]*(d[b,:,None]*r[a,None,:])
        f=f.reshape(m,-1);physical.append(m)
        if d.shape==(n,n) and r.shape==(n,n):
            if m*m>max_values:raise MemoryError('identity factor exceeds resource budget')
            modes.append((None,None,f));leading.append(sqrt(2.) if n>1 else 1.);exact.append(k)
        else:
            u,s,v=np.linalg.svd(f,full_matrices=False);modes.append((u,s,v));leading.append(float(s[0]))
    prefactor=sqrt(prod(physical))*float(np.linalg.norm(dc))*float(np.linalg.norm(rc))*prod(leading)
    if not np.isfinite(prefactor):raise ArithmeticError('nonfinite spectral bound')
    q=[];t=[];ratios=[]
    for k,((u,s,v),scale,m) in enumerate(zip(modes,leading,physical)):
        if k in exact:
            q.append(np.eye(m));t.append(v);ratios.append(0.)
        elif prefactor==0:
            q.append(u);t.append(s[:,None]*v);ratios.append(0.)
        else:
            cutoff=absolute_l1/(3*prefactor)
            rank=max(1,int(np.flatnonzero(np.r_[s/scale,0.]<=cutoff)[0]))
            q.append(u[:,:rank]);t.append(s[:rank,None]*v[:rank]);ratios.append(float(s[rank]/scale) if rank<len(s) else 0.)
    bound=prefactor*sum(ratios)
    if not np.isfinite(bound) or bound>absolute_l1:raise ArithmeticError('factor error exceeds budget')
    return tuple(q),tuple(t),dict(absolute_l1_bound=bound,ranks=[f.shape[1] for f in q],exact_square_modes=exact,prefactor=prefactor,spectral_tail_ratios=ratios,bound_scope='exact square basis plus rectangular factor truncation; excludes roundoff')
