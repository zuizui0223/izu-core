"""Discrete genotype-density counterpart with exact unlinked inheritance.

This is a conditional deterministic closure, not a PDE or the stochastic mean.
Genotype-class outcross diagonals are valid (different plants, same genotype).
"""
from dataclasses import dataclass, replace
from functools import lru_cache
from itertools import combinations_with_replacement, product
from types import MappingProxyType

import numpy as np
from scipy.special import ndtr


def _readonly(array):
    array=np.asarray(array); array.setflags(write=False); return array


@dataclass(frozen=True)
class GeneticGrid:
    axes: tuple
    genotypes: np.ndarray
    gamete_probabilities: np.ndarray
    child_lookup: np.ndarray
    genotype_lookup: object


def make_grid(axes) -> GeneticGrid:
    if len(axes)!=3:
        raise ValueError('grid needs three allele axes')
    for axis in axes:
        a=np.asarray(axis)
        if a.ndim!=1 or not len(a) or not np.isfinite(a).all() or (a<0).any() or (a>1).any() or (np.diff(a)<=0).any():
            raise ValueError('allele nodes must be finite, increasing and in [0,1]')
    return _make_grid(tuple(tuple(float(x) for x in a) for a in axes))


@lru_cache(maxsize=8)
def _make_grid(axes):
    pairs=[list(combinations_with_replacement(range(len(a)),2)) for a in axes]
    states=list(product(*pairs))
    lookup={s:i for i,s in enumerate(states)}
    gametes=list(product(*(range(len(a)) for a in axes)))
    gamete_lookup={g:i for i,g in enumerate(gametes)}
    probabilities=np.zeros((len(states),len(gametes)))
    for i,s in enumerate(states):
        for g in product(*s):
            probabilities[i,gamete_lookup[g]]+=1/8
    genotypes=np.array([[[axes[k][a],axes[k][b]] for k,(a,b) in enumerate(s)] for s in states])
    child=np.array([[lookup[tuple(tuple(sorted((a,b))) for a,b in zip(g,h))]
                     for h in gametes] for g in gametes],dtype=int)
    return GeneticGrid(tuple(_readonly(np.array(a)) for a in axes),_readonly(genotypes),
        _readonly(probabilities),_readonly(child),MappingProxyType(lookup))


def mutation_matrix(nodes, rate, sd):
    nodes=np.asarray(nodes,dtype=float)
    if (nodes.ndim!=1 or not len(nodes) or not np.isfinite(nodes).all()
            or (np.diff(nodes)<=0).any() or (nodes<0).any() or (nodes>1).any()
            or not np.isfinite([rate,sd]).all() or not 0<=rate<=1 or sd<0):
        raise ValueError('invalid mutation kernel settings')
    if rate==0 or sd==0:
        return np.eye(len(nodes))
    if nodes[0]!=0 or nodes[-1]!=1:
        raise ValueError('mutating axes must span [0,1]')
    bounds=np.r_[0,(nodes[:-1]+nodes[1:])/2,1]
    low,high=bounds[:-1],bounds[1:]
    if sd>=.25:
        # Integrated reflected-normal cosine expansion; tail below roundoff.
        m=int(np.ceil(np.sqrt(-2*np.log(1e-16))/(np.pi*sd)))
        harmonics=np.arange(1,m+1)*np.pi
        raw=np.broadcast_to(high-low,(len(nodes),len(nodes))).copy()
        raw+=2*(np.cos(nodes[:,None]*harmonics)*np.exp(-.5*(harmonics*sd)**2)) @ (
            (np.sin(harmonics[:,None]*high)-np.sin(harmonics[:,None]*low))/harmonics[:,None])
    else:
        raw=np.zeros((len(nodes),len(nodes)))
        radius=int(np.ceil((8*sd+1)/2))+1
        for k in range(-radius,radius+1):
            for a,b in ((2*k+low,2*k+high),(2*k-high,2*k-low)):
                raw+=ndtr((b[None,:]-nodes[:,None])/sd)-ndtr((a[None,:]-nodes[:,None])/sd)
    if (raw< -1e-12).any() or not np.allclose(raw.sum(axis=1),1,atol=1e-12,rtol=0):
        raise ArithmeticError('mutation probability integration failed')
    raw=np.maximum(raw,0); raw/=raw.sum(axis=1,keepdims=True)
    return (1-rate)*np.eye(len(nodes))+rate*raw


@lru_cache(maxsize=24)
def _mutated_gametes(axes,rate,sd,mode):
    grid=_make_grid(axes)
    kernels=[mutation_matrix(a,0 if k==2 and mode=='fixed' else rate,sd) for k,a in enumerate(axes)]
    mutation=np.kron(np.kron(kernels[0],kernels[1]),kernels[2])
    return _readonly(grid.gamete_probabilities @ mutation)


def project_state(state, grid):
    alleles=state.alleles.copy()
    indices=np.empty(alleles.shape,dtype=int)
    for k,nodes in enumerate(grid.axes):
        indices[:,k]=np.argmin(abs(alleles[:,k,:,None]-nodes),axis=2)
        alleles[:,k]=nodes[indices[:,k]]
    sorted_indices=np.sort(indices,axis=2)
    ids=[grid.genotype_lookup[tuple(map(tuple,row))] for row in sorted_indices]
    return replace(state,alleles=alleles),np.bincount(ids,minlength=len(grid.genotypes)).astype(float)


@dataclass(frozen=True)
class DensityLedger:
    outcross: np.ndarray
    self_viable: np.ndarray
    self_raw: np.ndarray
    ovules: np.ndarray
    exported: np.ndarray
    delivered: np.ndarray
    lost: np.ndarray
    maternal: np.ndarray
    paternal: np.ndarray
    resident_recruits: float
    immigrant_recruits: float


def density_step(counts, grid, visitors, immigrants, config):
    counts=np.asarray(counts,dtype=float)
    if (counts.shape!=(len(grid.genotypes),) or not np.isfinite(counts).all()
            or (counts<0).any() or counts.sum()>config.capacity+1e-9):
        raise ValueError('invalid density counts')
    traits=grid.genotypes.mean(axis=2)
    a=traits[:,2] if config.assurance_mode=='evolving' else np.full(len(counts),config.fixed_assurance)
    ovules=config.ovule_budget*np.exp(-config.investment_cost*traits[:,1]**2-config.assurance_cost*a*a)
    transfer=np.zeros((len(counts),len(counts)))
    exported=np.zeros(len(counts))
    if len(visitors.ids) and config.activity:
        affinity=(.1+traits[:,1,None])*np.exp(-((traits[:,0,None]-visitors.optima)/visitors.breadths)**2)
        total=affinity.sum(axis=1,keepdims=True)
        channels=np.divide(affinity,total,out=np.zeros_like(affinity),where=total>0)
        activity=config.activity*(len(visitors.ids)/config.reference_visitor_count if config.activity_mode=='count_scaled' else 1)
        removed=config.pollen_budget*np.exp(-config.pollen_discount*a)*(-np.expm1(-activity*affinity.mean(axis=1)))
        recipient=affinity/((counts[:,None]*affinity).sum(axis=0)+config.capacity*config.background_ratio)
        # Dose received by one recipient of each genotype class.
        transfer=(counts[:,None]*removed[:,None]*channels*visitors.effectiveness) @ recipient.T
        exported=counts*removed
    receipt=transfer.sum(axis=0)
    available=ovules*(1-a) if config.assurance_timing=='prior' else ovules
    female=available*(-np.expm1(-receipt/(2*config.pollen_scale)))
    conversion=np.divide(counts*female,receipt,out=np.zeros_like(counts),where=receipt>0)
    outcross=transfer*conversion[None,:]
    self_raw=counts*(ovules*a if config.assurance_timing=='prior' else a*(ovules-female))
    self_viable=self_raw*(1-config.depression)
    parents=outcross.copy(); parents[np.diag_indices(len(counts))]+=self_viable
    axes=tuple(tuple(a) for a in grid.axes)
    gametes=_mutated_gametes(axes,config.mutation_rate,config.mutation_sd,config.assurance_mode)
    child_gametes=gametes.T @ parents @ gametes
    births=np.bincount(grid.child_lookup.ravel(),weights=child_gametes.ravel(),minlength=len(counts))
    _,incoming=project_state(immigrants,grid)
    incoming*=config.seed_arrival.establishment
    total=float(births.sum()+incoming.sum())
    space=max(0.,config.capacity-config.survival*counts.sum())
    retention=min(1.,space/total) if total>0 else 0.
    result=config.survival*counts+retention*(births+incoming)
    delivered=transfer*counts[None,:]
    lost=exported-delivered.sum(axis=1)
    if not np.isfinite(result).all() or (lost< -1e-10).any():
        raise ArithmeticError('invalid density arithmetic')
    return result,DensityLedger(outcross,self_viable,self_raw,counts*ovules,exported,delivered,
        np.maximum(0,lost),counts*female+self_viable,outcross.sum(axis=1)+self_viable,
        retention*births.sum(),retention*incoming.sum())
