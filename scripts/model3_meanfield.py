"""Discrete Mendelian distribution limit; not a diffusion PDE.

Density is individuals divided by carrying capacity. Individual diagonal pollen
exclusion vanishes in this large-population limit; genotype-diagonal outcrosses
remain, because different plants can have the same genotype.
"""
from __future__ import annotations

from functools import lru_cache
from itertools import combinations_with_replacement, product

import numpy as np


@lru_cache(maxsize=4)
def genotype_grid(start, points=3):
    """Exact two-unlinked-locus inheritance on a declared finite allele grid."""
    if not np.isfinite(start) or not .1<=start<=.9 or points not in (2,3,4,5):
        raise ValueError('invalid allele grid')
    pairs=list(combinations_with_replacement(range(points),2))
    states=list(product(pairs,pairs))
    lookup={state:i for i,state in enumerate(states)}
    access=np.linspace(start-.1,start+.1,points)
    investment=np.linspace(.4,.6,points)
    genotypes=np.array([[access[list(a)],investment[list(b)]] for a,b in states])
    gametes=list(product(range(points),repeat=2))
    gamete_lookup={g:i for i,g in enumerate(gametes)}
    probabilities=np.zeros((len(states),len(gametes)))
    for i,(access_pair,investment_pair) in enumerate(states):
        for a,b in product(access_pair,investment_pair):
            probabilities[i,gamete_lookup[a,b]]+=.25
    kernel=np.zeros((len(states),len(states),len(states)))
    for i,(a,b) in enumerate(gametes):
        for j,(c,d) in enumerate(gametes):
            child=lookup[tuple(sorted((a,c))),tuple(sorted((b,d)))]
            kernel[:,:,child]+=np.outer(probabilities[:,i],probabilities[:,j])
    genotypes.setflags(write=False)
    kernel.setflags(write=False)
    return genotypes,kernel


def meanfield_step(density,genotypes,kernel,visitors,*,activity,survival,selfing,
                   depression=.5,control='selected'):
    """Density-dependent reproductive map with exact finite-grid inheritance.

    This removes demographic sampling, not external community variability. It
    shares the individual model's abstract dose, costs, saturation and selfing
    rules. It is not the exact expectation of finite-population trajectories.
    """
    density=np.asarray(density,dtype=float)
    genotypes=np.asarray(genotypes,dtype=float)
    kernel=np.asarray(kernel,dtype=float)
    visitors=np.asarray(visitors,dtype=float)
    g=len(density)
    if (density.shape!=(g,) or genotypes.shape!=(g,2,2) or kernel.shape!=(g,g,g)
            or not np.isfinite(density).all() or (density<0).any() or density.sum()>1+1e-12
            or not np.isfinite(genotypes).all() or ((genotypes<0)|(genotypes>1)).any()
            or not np.isfinite(kernel).all() or (kernel<0).any()
            or not np.allclose(kernel.sum(axis=2),1,atol=1e-12,rtol=0)
            or visitors.ndim!=1 or not np.isfinite(visitors).all() or ((visitors<0)|(visitors>1)).any()
            or not np.isfinite([activity,survival,selfing,depression]).all() or activity<0
            or not 0<=survival<1 or not 0<=selfing<=1 or not 0<=depression<=1
            or control not in ('selected','neutral')):
        raise ValueError('invalid distribution state or settings')
    traits=genotypes.mean(axis=2)
    pairs=np.zeros((g,g))
    outcross_total=0.
    selfed_total=0.
    for _episode in range(2):
        if len(visitors):
            affinity=(.1+traits[:,1,None])*np.exp(-((traits[:,0,None]-visitors)/.2)**2)
            total_affinity=affinity.sum(axis=1,keepdims=True)
            channels=np.divide(affinity,total_affinity,out=np.zeros_like(affinity),where=total_affinity>0)
            removed=10*(1-survival)*(-np.expm1(-activity*affinity.mean(axis=1)))
            recipient_share=affinity/(1+(density[:,None]*affinity).sum(axis=0))
            # All donors in class i to ONE recipient in class j, in dose units.
            transfer=(density[:,None]*removed[:,None]*channels) @ recipient_share.T
        else:
            transfer=np.zeros((g,g))
        receipt=transfer.sum(axis=0)
        ovules=4*(1-survival)*np.exp(-.5*traits[:,1]**2)
        female=ovules*(-np.expm1(-receipt))
        conversion=np.divide(density*female,receipt,out=np.zeros(g),where=receipt>0)
        outcross=transfer*conversion[None,:]
        selfed=density*(ovules-female)*selfing*(1-depression)
        if control=='neutral' and density.sum()>0:
            frequencies=density/density.sum()
            outcross=outcross.sum()*np.outer(frequencies,frequencies)
            selfed=selfed.sum()*frequencies
        pairs+=outcross
        pairs[np.diag_indices(g)]+=selfed
        outcross_total+=float(outcross.sum())
        selfed_total+=float(selfed.sum())
    births=np.einsum('ij,ijk->k',pairs,kernel,optimize=True)
    total=float(births.sum())
    vacancies=max(0.,1-survival*density.sum())
    recruits=births*(min(total,vacancies)/total) if total>0 else np.zeros(g)
    result=survival*density+recruits
    if not np.isfinite(result).all() or (result<0).any() or result.sum()>1+1e-10:
        raise ArithmeticError('invalid mean-field density update')
    return dict(density=result,outcross=outcross_total,selfed=selfed_total,
                potential_recruits=total,established=float(recruits.sum()))
