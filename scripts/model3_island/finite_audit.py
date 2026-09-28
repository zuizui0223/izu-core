"""Finite-state pollen and offspring benchmarks for the archived two-locus model.

Genotype classes retain within-class mating between distinct individuals.
These conditional one-step expectations are not a long-run moment closure.
"""
from __future__ import annotations

from itertools import product

import numpy as np

from .expectation import expected_recruits


def _genotypes(genotype):
    genotype=np.asarray(genotype,dtype=float)
    if (genotype.ndim!=3 or genotype.shape[1:]!=(2,2)
            or not np.isfinite(genotype).all() or ((genotype<0)|(genotype>1)).any()):
        raise ValueError('genotype must have shape N x 2 x 2 in [0,1]')
    return np.sort(genotype,axis=2)


def aggregate_transfer(genotype: np.ndarray, visitors: np.ndarray, *, breadth: float,
                       activity: float, budget: float, background: float) -> dict:
    genotype=_genotypes(genotype)
    visitors=np.asarray(visitors,dtype=float)
    if (visitors.ndim!=1 or not np.isfinite(visitors).all()
            or ((visitors<0)|(visitors>1)).any()):
        raise ValueError('visitors must be a vector in [0,1]')
    settings=np.asarray([breadth,activity,budget,background],dtype=float)
    if (not np.isfinite(settings).all() or breadth<=0 or background<=0 or activity<0 or budget<0):
        raise ValueError('invalid transfer settings')
    classes,index,counts=np.unique(genotype,axis=0,return_inverse=True,return_counts=True)
    size=len(classes)
    transfer=np.zeros((size,size))
    exported=np.zeros(size)
    self_loss=np.zeros(size)
    background_loss=np.zeros(size)
    if size and len(visitors) and activity and budget:
        traits=classes.mean(axis=2)
        affinity=(.1+traits[:,1,None])*np.exp(-((traits[:,0,None]-visitors)/breadth)**2)
        total=affinity.sum(axis=1,keepdims=True)
        channels=np.divide(affinity,total,out=np.zeros_like(affinity),where=total>0)
        removed=budget*(-np.expm1(-activity*affinity.mean(axis=1)))
        denominator=(counts[:,None]*affinity).sum(axis=0)+background
        per_pair=(removed[:,None]*channels) @ (affinity/denominator).T
        transfer=counts[:,None]*counts[None,:]*per_pair
        self_loss=counts*np.diag(per_pair)
        transfer[np.diag_indices(size)]-=self_loss
        exported=counts*removed
        background_loss=counts*removed*(channels*(background/denominator)).sum(axis=1)
    return dict(genotypes=classes,class_index=index,counts=counts,transfer=transfer,
                exported=exported,self_loss=self_loss,background_loss=background_loss)


def expected_genotype_counts(genotype: np.ndarray, pairs: np.ndarray, *, survival: float,
                             capacity: int) -> dict:
    genotype=_genotypes(genotype)
    pairs=np.asarray(pairs,dtype=float)
    n=len(genotype)
    if pairs.shape!=(n,n) or not np.isfinite(pairs).all() or (pairs<0).any():
        raise ValueError('pairs must be a finite nonnegative N x N matrix')
    total=float(pairs.sum())
    recruits=expected_recruits(n,survival,capacity,total)
    output={}
    def key(g):
        return tuple(g.ravel())
    for g in genotype:
        k=key(g)
        output[k]=output.get(k,0.)+survival
    if total>0 and recruits>0:
        # This diagnostic is deliberately exact, not a production large-N kernel.
        for father,mother in zip(*np.nonzero(pairs)):
            weight=recruits*(pairs[father,mother]/total)/16
            for a,b,c,d in product(range(2),repeat=4):
                child=np.sort([[genotype[mother,0,a],genotype[father,0,b]],
                               [genotype[mother,1,c],genotype[father,1,d]]],axis=1)
                k=key(child)
                output[k]=output.get(k,0.)+weight
    keys=sorted(output)
    classes=np.array(keys,dtype=float).reshape(-1,2,2)
    return dict(genotypes=classes,expected_counts=np.array([output[k] for k in keys]),
                expected_recruits=recruits,expected_survivors=n*survival)
