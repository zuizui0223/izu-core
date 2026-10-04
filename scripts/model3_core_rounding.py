"""Joint-core HOSVD truncation with an exact-arithmetic L1 error bound.

Not positivity preserving; no hidden clipping. Roundoff is outside the bound.
"""
from math import prod,sqrt
import numpy as np
from scripts.model3_compressed_step import contract,mass,check_size


def rounded(state,*,relative_l1=1e-8,budget=2_000_000):
    if not np.isfinite(relative_l1) or not 0<relative_l1<1:
        raise ValueError('relative tolerance must be between zero and one')
    core,factors=state;core=np.asarray(core,dtype=float)
    factors=[np.asarray(f,dtype=float) for f in factors]
    if core.ndim!=3 or not core.size or len(factors)!=3 or not np.isfinite(core).all():
        raise ValueError('finite three-dimensional core required')
    for k,f in enumerate(factors):
        if f.ndim!=2 or not f.size or f.shape[1]!=core.shape[k] or not np.isfinite(f).all():
            raise ValueError('invalid factor')
        check_size(f.size,budget)
    original_mass=mass((core,factors))
    if not np.any(core):
        return (np.zeros((1,1,1)),tuple(np.zeros((f.shape[0],1)) for f in factors)),dict(
            absolute_l1_bound=0.,mass_before=0.,ranks=[1,1,1])
    if not np.isfinite(original_mass) or original_mass<=0:
        raise ValueError('nonzero represented density must have positive mass')
    decomposed=[np.linalg.qr(f,mode='reduced') for f in factors]
    orth=contract('abc,ia,jb,kc->ijk',core,*(r for q,r in decomposed),budget=budget)
    n=prod(f.shape[0] for f in factors)
    tail_budget=(relative_l1*original_mass/(8*sqrt(3*n)))**2
    projections=[];discarded=0.
    for axis in range(3):
        unfolding=np.moveaxis(orth,axis,0).reshape(orth.shape[axis],-1)
        u,s,_=np.linalg.svd(unfolding,full_matrices=False)
        tails=np.r_[np.cumsum((s*s)[::-1])[::-1],0.]
        rank=max(1,int(np.flatnonzero(tails<=tail_budget)[0]))
        discarded+=float(tails[rank]);projections.append(u[:,:rank])
    reduced=contract('abc,ai,bj,ck->ijk',orth,*projections,budget=budget)
    new_factors=tuple(q@p for (q,r),p in zip(decomposed,projections))
    approximate_mass=mass((reduced,new_factors))
    if approximate_mass<=0 or not np.isfinite(approximate_mass):
        raise ArithmeticError('invalid post-projection mass')
    scale=original_mass/approximate_mass
    bound=sqrt(n*discarded)+abs(scale-1)*sqrt(n)*float(np.linalg.norm(reduced))
    if not np.isfinite(bound) or bound>relative_l1*original_mass:
        raise ArithmeticError('rank-reduction bound exceeds tolerance')
    return (reduced*scale,new_factors),dict(absolute_l1_bound=bound,
        mass_before=original_mass,ranks=list(reduced.shape),
        relative_l1_bound=bound/original_mass,
        bound_scope='truncation and mass rescaling; excludes floating-point roundoff')
