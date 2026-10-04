"""Exact selfed birth transform for a joint Tucker representation.

Input represents viable selfed births, after fecundity/inbreeding depression.
This component neither computes ecological weights nor closes a full solver.
"""
from itertools import combinations_with_replacement
import numpy as np
from scripts.model3_island.density import birth_mutation_matrix


def local_selfing(nodes, rate, sd, scheme='jump'):
    nodes = np.asarray(nodes,dtype=float)
    if (nodes.ndim != 1 or nodes.size == 0 or not np.isfinite(nodes).all()
            or np.any(np.diff(nodes)<=0) or np.min(nodes)<0 or np.max(nodes)>1
            or not np.isfinite(rate) or not 0<=rate<=1
            or not np.isfinite(sd) or sd<0):
        raise ValueError('invalid nodes or mutation parameters')
    kernel = birth_mutation_matrix(nodes,rate,sd,scheme)
    pairs = np.array(list(combinations_with_replacement(range(len(nodes)),2)))
    gametes = (kernel[pairs[:,0]]+kernel[pairs[:,1]])/2
    multiplier = np.where(pairs[:,0]==pairs[:,1],1.,2.)
    transition = gametes[:,pairs[:,0]]*gametes[:,pairs[:,1]]*multiplier
    return transition


def selfed_factors(factors, transitions):
    """Keep the input joint core; transform only its three factor matrices."""
    if len(factors)!=3 or len(transitions)!=3:
        raise ValueError('three traits required')
    result = []
    for factor, transition in zip(factors,transitions):
        u = np.asarray(factor,dtype=float)
        local = np.asarray(transition,dtype=float)
        if (u.ndim!=2 or local.ndim!=2 or not u.size or not local.size
                or u.shape[0]!=local.shape[0] or not np.isfinite(u).all()
                or not np.isfinite(local).all() or np.any(local<0)
                or not np.allclose(local.sum(axis=1),1,atol=1e-12,rtol=0)):
            raise ValueError('finite factors and compatible row-stochastic transitions required')
        result.append(local.T@u)
    return tuple(result)
