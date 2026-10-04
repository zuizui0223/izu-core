"""Pre-contraction outcross-factor reduction, with a spectral error bound.

Does not allocate the expanded parental core. Not a complete solver.
"""
from math import prod,sqrt
import numpy as np


def reduce_child_factors(dc,rc,factors,*,absolute_l1,max_values=2_000_000):
    if not np.isfinite(absolute_l1) or absolute_l1<=0:
        raise ValueError('positive finite error budget required')
    dc=np.asarray(dc,dtype=float);rc=np.asarray(rc,dtype=float)
    fs=[np.asarray(f,dtype=float) for f in factors]
    if (dc.ndim!=3 or rc.ndim!=3 or not dc.size or not rc.size or len(fs)!=3
            or not np.isfinite(dc).all() or not np.isfinite(rc).all()):
        raise ValueError('finite joint cores required')
    if not isinstance(max_values,int) or max_values<1:
        raise ValueError('positive integer resource budget required')
    for k,f in enumerate(fs):
        if f.ndim!=2 or not f.size or f.shape[1]!=dc.shape[k]*rc.shape[k] or not np.isfinite(f).all():
            raise ValueError('child factor shape mismatch')
        if f.size>max_values:
            raise MemoryError('child factor exceeds resource budget')
    decomposed=[np.linalg.svd(f,full_matrices=False) for f in fs]
    leading=[float(s[0]) for u,s,v in decomposed]
    prefactor=sqrt(prod(f.shape[0] for f in fs))*float(np.linalg.norm(dc))*float(np.linalg.norm(rc))*prod(leading)
    if not np.isfinite(prefactor):
        raise ArithmeticError('nonfinite spectral bound')
    if prefactor==0:
        qs=[];rs=[]
        for f in fs:
            q=np.zeros((f.shape[0],1));q[0]=1;qs.append(q);rs.append(np.zeros((1,f.shape[1])))
        return tuple(qs),tuple(rs),dict(absolute_l1_bound=0.,ranks=[1,1,1])
    relative_tail=absolute_l1/(3*prefactor)
    qs=[];rs=[];ratios=[]
    for (u,s,v),scale in zip(decomposed,leading):
        rank=max(1,int(np.flatnonzero(np.r_[s/scale,0.]<=relative_tail)[0]))
        qs.append(u[:,:rank]);rs.append(s[:rank,None]*v[:rank])
        ratios.append(float(s[rank]/scale) if rank<len(s) else 0.)
    bound=prefactor*sum(ratios)
    if not np.isfinite(bound) or bound>absolute_l1:
        raise ArithmeticError('factor truncation exceeds error budget')
    return tuple(qs),tuple(rs),dict(absolute_l1_bound=bound,ranks=[q.shape[1] for q in qs],
        prefactor=prefactor,spectral_tail_ratios=ratios,
        bound_scope='exact-arithmetic factor truncation; excludes roundoff')
