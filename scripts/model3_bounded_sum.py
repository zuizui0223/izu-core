"""Project shared factor spaces before allocating a sum's common core."""
from math import prod,sqrt
import numpy as np
from scripts.model3_compressed_step import contract,check_size


def bounded_sum(states,*,absolute_l1,budget=2_000_000):
    if not states or not np.isfinite(absolute_l1) or absolute_l1<=0:
        raise ValueError('nonempty states and positive tolerance required')
    physical=tuple(f.shape[0] for f in states[0][1])
    norms=[];weights=[]
    for core,fs in states:
        if core.ndim!=3 or len(fs)!=3 or tuple(f.shape[0] for f in fs)!=physical:
            raise ValueError('incompatible states')
        if not np.isfinite(core).all() or any(not np.isfinite(f).all() or f.shape[1]!=core.shape[k] for k,f in enumerate(fs)):
            raise ValueError('invalid factors')
        check_size(core.size,budget)
        norms.append([float(np.linalg.norm(f,2)) for f in fs]);weights.append(float(np.linalg.norm(core)))
    coefficients=[sum(w*prod(ns[j] for j in range(3) if j!=k) for w,ns in zip(weights,norms)) for k in range(3)]
    bases=[];transforms=[];terms=[];root_n=sqrt(prod(physical))
    for k in range(3):
        width=sum(fs[k].shape[1] for _,fs in states);check_size(physical[k]*width,budget)
        u,s,_=np.linalg.svd(np.concatenate([fs[k] for _,fs in states],axis=1),full_matrices=False)
        threshold=absolute_l1/(3*root_n*coefficients[k]) if coefficients[k]>0 else float('inf')
        rank=max(1,int(np.count_nonzero(s>threshold)))
        tail=float(s[rank]) if rank<len(s) else 0.
        bases.append(u[:,:rank]);transforms.append([u[:,:rank].T@fs[k] for _,fs in states])
        terms.append(root_n*coefficients[k]*tail)
    shape=tuple(b.shape[1] for b in bases);check_size(prod(shape),budget)
    result=np.zeros(shape)
    for i,(core,_) in enumerate(states):
        result+=contract('abc,ia,jb,kc->ijk',core,*(t[i] for t in transforms),budget=budget)
    bound=sum(terms)
    if not np.isfinite(bound) or bound>absolute_l1:raise ArithmeticError('sum projection bound exceeds tolerance')
    return (result,tuple(bases)),dict(absolute_l1_bound=bound,axis_bounds=terms,ranks=list(shape),scope='orthogonal factor projections with telescoping bound; roundoff excluded')
