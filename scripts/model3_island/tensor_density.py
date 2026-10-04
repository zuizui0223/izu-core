"""Exact sparse Mendelian inheritance with tensor-factorized birth mutation.

The adult genotype distribution remains fully joint. This is an algebraic
reordering, not a linkage-equilibrium or independent-trait approximation.
"""
from functools import lru_cache
from itertools import combinations_with_replacement,product
from types import MappingProxyType
import numpy as np
from scipy.sparse import coo_matrix
from .density import GeneticGrid,_readonly,birth_mutation_matrix


def make_tensor_grid(axes):
    if len(axes)!=3:raise ValueError('three allele axes required')
    normalized=[]
    for axis in axes:
        a=np.asarray(axis,dtype=float)
        if a.ndim!=1 or not len(a) or not np.isfinite(a).all() or (np.diff(a)<=0).any() or (a<0).any() or (a>1).any():
            raise ValueError('invalid allele axis')
        normalized.append(tuple(a))
    return _grid(tuple(normalized))


@lru_cache(maxsize=2)
def _grid(axes):
    pairs=[list(combinations_with_replacement(range(len(a)),2)) for a in axes]
    states=np.array(list(product(*pairs)),dtype=np.int32)
    sizes=tuple(len(a) for a in axes)
    gametes=np.array(list(product(*(range(n) for n in sizes))),dtype=np.int32)
    indices=[]
    for copy in product([0,1],repeat=3):
        indices.append(np.ravel_multi_index(tuple(states[:,k,j] for k,j in enumerate(copy)),sizes))
    rows=np.tile(np.arange(len(states)),8)
    p=coo_matrix((np.full(len(rows),.125),(rows,np.concatenate(indices))),shape=(len(states),len(gametes))).tocsr()
    genotype=np.stack([np.array(a)[states[:,k,:]] for k,a in enumerate(axes)],axis=1)
    child=np.zeros((len(gametes),len(gametes)),dtype=np.int32)
    stride=1
    for k in reversed(range(3)):
        pair_index=np.zeros((sizes[k],sizes[k]),dtype=np.int32)
        for ix,(a,b) in enumerate(pairs[k]):pair_index[a,b]=pair_index[b,a]=ix
        child+=stride*pair_index[gametes[:,k,None],gametes[None,:,k]]
        stride*=len(pairs[k])
    lookup=MappingProxyType({tuple(tuple(pair) for pair in row):i for i,row in enumerate(states)})
    return GeneticGrid(tuple(_readonly(np.array(a)) for a in axes),_readonly(genotype),p,_readonly(child),lookup)


def tensor_births(grid,outcross,self_viable,config,mutation_traits,scheme):
    p=grid.gamete_probabilities
    donor=p.T@outcross.donors
    recipient=p.T@outcross.recipients
    newborn=donor@recipient.T+(p.T@p.multiply(self_viable[:,None])).toarray()
    dimensions=tuple(len(a) for a in grid.axes)
    tensor=newborn.reshape(dimensions+dimensions)
    for axis in range(6):
        k=axis%3
        rate=config.mutation_rate if mutation_traits[k] and not(k==2 and config.assurance_mode=='fixed') else 0.
        if rate==0 or config.mutation_sd==0:continue
        kernel=_kernel(tuple(grid.axes[k]),rate,config.mutation_sd,scheme)
        moved=np.moveaxis(tensor,axis,-1)
        tensor=np.moveaxis(moved@kernel,-1,axis)
    return np.bincount(grid.child_lookup.ravel(),weights=tensor.ravel(),minlength=len(grid.genotypes))


@lru_cache(maxsize=24)
def _kernel(nodes,rate,sd,scheme):
    return birth_mutation_matrix(nodes,rate,sd,scheme)
