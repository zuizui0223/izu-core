"""Exact ecological weight functions from joint Tucker density marginals.

No independent-trait closure. Outputs are weight functions, not a solver.
"""
from itertools import combinations_with_replacement
import numpy as np


def ecological_weights(core,factors,axes,visitors,config):
    core=np.asarray(core,dtype=float)
    if core.ndim!=3 or len(factors)!=3 or len(axes)!=3 or not np.isfinite(core).all():
        raise ValueError('three finite joint dimensions required')
    means=[]; factors=[np.asarray(f,dtype=float) for f in factors]
    for k,axis in enumerate(axes):
        axis=np.asarray(axis,dtype=float)
        if (axis.ndim!=1 or not axis.size or not np.isfinite(axis).all()
                or np.any(np.diff(axis)<=0) or axis.min()<0 or axis.max()>1):
            raise ValueError('invalid allele nodes')
        m=np.array([(a+b)/2 for a,b in combinations_with_replacement(axis,2)])
        if factors[k].shape!=(len(m),core.shape[k]) or not np.isfinite(factors[k]).all():
            raise ValueError('factor shape mismatch')
        means.append(m)
    x,xi=np.unique(means[0],return_inverse=True)
    z,zi=np.unique(means[1],return_inverse=True)
    fx=np.zeros((len(x),core.shape[0]));fz=np.zeros((len(z),core.shape[1]))
    np.add.at(fx,xi,factors[0]);np.add.at(fz,zi,factors[1])
    a=means[2] if config.assurance_mode=='evolving' else np.full_like(means[2],config.fixed_assurance)
    def marginal(weight):
        return fx@np.einsum('abc,c->ab',core,weight@factors[2])@fz.T
    population=marginal(np.ones_like(a))
    if population.min() < -1e-10 or population.sum()>config.capacity+1e-9:
        raise ValueError('invalid marginal population')
    donor_a=np.exp(-config.pollen_discount*a)
    donor_xy=np.zeros((len(x),len(z),0));receiver=donor_xy.copy()
    receipt=np.zeros((len(x),len(z)))
    if len(visitors.ids) and config.activity:
        affinity=(.1+z[None,:,None])*np.exp(-((x[:,None,None]-visitors.optima)/visitors.breadths)**2)
        total=affinity.sum(axis=2,keepdims=True)
        channels=np.divide(affinity,total,out=np.zeros_like(affinity),where=total>0)
        activity=config.activity*(len(visitors.ids)/config.reference_visitor_count if config.activity_mode=='count_scaled' else 1)
        removed=config.pollen_budget*(-np.expm1(-activity*affinity.mean(axis=2)))
        donor_xy=removed[:,:,None]*channels*visitors.effectiveness
        receiver=affinity/((population[:,:,None]*affinity).sum(axis=(0,1))+config.capacity*config.background_ratio)
        donor_totals=(marginal(donor_a)[:,:,None]*donor_xy).sum(axis=(0,1))
        receipt=receiver@donor_totals
    saturated=-np.expm1(-receipt/(2*config.pollen_scale))
    ovule_xy=np.broadcast_to(config.ovule_budget*np.exp(-config.investment_cost*z*z),(len(x),len(z)))
    ovule_a=np.exp(-config.assurance_cost*a*a)
    ratio=np.divide(ovule_xy*saturated,receipt,out=np.zeros_like(receipt),where=receipt>0)
    prior=config.assurance_timing=='prior'
    return dict(maps=(xi,zi),donor_xy=donor_xy,donor_a=donor_a,
        recipient_xy=receiver*ratio[:,:,None],recipient_a=ovule_a*(1-a if prior else 1),
        self_xy=ovule_xy*(1 if prior else 1-saturated)*(1-config.depression),
        self_a=ovule_a*a,receipt_xy=receipt)
