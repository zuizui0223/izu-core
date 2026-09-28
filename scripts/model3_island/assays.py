"""Fixed-state phenotype interventions; no population updating or inheritance."""
from dataclasses import replace
import numpy as np

from .reproduction import reproduce
from .types import PlantState


def reference_service(visitors,config):
    """Outcross fertilization on an invariant 21-plant access panel.

    Fixed investment .5, assurance disabled, capacity/background scaled to 21.
    This describes external visitor history, never the evolved focal phenotype.
    """
    n=21
    alleles=np.full((n,3,2),.5)
    alleles[:,0,:]=np.linspace(0,1,n)[:,None]
    p=PlantState(alleles,np.arange(n*6).reshape(n,3,2),np.zeros((n,3,2),bool),
                 np.arange(n),np.zeros(n,dtype=int))
    c=replace(config,capacity=n,assurance_mode='fixed',fixed_assurance=0.)
    cache={}; result=[]
    for v in visitors:
        key=(v.optima.tobytes(),v.breadths.tobytes(),v.effectiveness.tobytes())
        if key not in cache:
            ledger=reproduce(p,v,c); ovules=ledger.ovules.sum()
            cache[key]=float(ledger.outcross.sum()/ovules) if ovules else np.nan
        result.append(cache[key])
    return np.asarray(result)


def investment_assay(state, visitors, config, *, step: float) -> dict:
    if not np.isscalar(step) or not np.isfinite(step) or not 0<step<=.5:
        raise ValueError('step must be in (0,.5]')
    traits=state.alleles.mean(axis=2)
    outcross=np.zeros(len(traits))
    total=np.zeros(len(traits))
    schemes=[]
    for i,z in enumerate(traits[:,1]):
        if z<step:
            low,high,scheme=z,z+step,'forward'
        elif z>1-step:
            low,high,scheme=z-step,z,'backward'
        else:
            low,high,scheme=z-step,z+step,'central'
        values=[]
        for x in (low,high):
            alleles=state.alleles.copy()
            # Phenotype assay only: both allele slots express x for this call.
            # No offspring are drawn; this state never enters a trajectory.
            alleles[i,1,:]=x
            ledger=reproduce(replace(state,alleles=alleles),visitors,config)
            cross=.5*(ledger.outcross[i].sum()+ledger.outcross[:,i].sum())
            values.append((cross,cross+ledger.self_viable[i]))
        difference=(np.array(values[1])-np.array(values[0]))/(high-low)
        outcross[i],total[i]=difference
        schemes.append(scheme)
    return dict(outcross_gradient=outcross,total_gradient=total,scheme=schemes,
                step=step,estimand='expected parental genome contributions per year')
