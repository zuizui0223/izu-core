"""Full joint-state distance without allocating the physical genotype tensor.

Exact-arithmetic L1 upper bound from Frobenius norm; roundoff excluded.
"""
from math import prod,sqrt
import numpy as np
from scripts.model3_compressed_step import contract,check_size


def joint_distance(left,right,*,budget=2_000_000):
    states=[]
    for core,factors in [left,right]:
        core=np.asarray(core,dtype=float);fs=[np.asarray(f,dtype=float) for f in factors]
        if core.ndim!=3 or len(fs)!=3 or not core.size or not np.isfinite(core).all():raise ValueError('finite joint state required')
        for k,f in enumerate(fs):
            if f.ndim!=2 or not f.size or f.shape[1]!=core.shape[k] or not np.isfinite(f).all():raise ValueError('invalid factors')
        states.append((core,fs))
    a,af=states[0];b,bf=states[1];transforms=[];physical=[]
    for k in range(3):
        if af[k].shape[0]!=bf[k].shape[0]:raise ValueError('different physical grids')
        physical.append(af[k].shape[0]);check_size(physical[-1]*(a.shape[k]+b.shape[k]),budget)
        q,r=np.linalg.qr(np.concatenate([af[k],bf[k]],axis=1),mode='reduced')
        transforms.append((r[:,:a.shape[k]],r[:,a.shape[k]:]))
    check_size(prod(t[0].shape[0] for t in transforms),budget)
    delta=contract('abc,ia,jb,kc->ijk',a,*(t[0] for t in transforms),budget=budget)
    delta-=contract('abc,ia,jb,kc->ijk',b,*(t[1] for t in transforms),budget=budget)
    norm=float(np.linalg.norm(delta))
    return dict(frobenius=norm,l1_upper=sqrt(prod(physical))*norm,physical_shape=physical,
                comparison_core_shape=list(delta.shape),scope='full joint difference; exact-arithmetic bound, roundoff excluded')
