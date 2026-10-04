"""Exact bounded-rank outcross births; not a complete compressed solver."""
from itertools import combinations_with_replacement
from math import prod
import numpy as np
from scripts.model3_island.density import birth_mutation_matrix


def outcross_tucker(donor_core, donor_factors, recipient_core, recipient_factors,
                    axes, rate, sd, scheme='jump', *, max_output_values=2_000_000):
    dc = np.asarray(donor_core,dtype=float)
    rc = np.asarray(recipient_core,dtype=float)
    if (dc.ndim!=3 or rc.ndim!=3 or not dc.size or not rc.size
            or not np.isfinite(dc).all() or not np.isfinite(rc).all()
            or len(axes)!=3 or len(donor_factors)!=3 or len(recipient_factors)!=3):
        raise ValueError('three finite joint axes required')
    nodes = [np.asarray(a,dtype=float) for a in axes]
    for a in nodes:
        if (a.ndim!=1 or not a.size or not np.isfinite(a).all()
                or np.any(np.diff(a)<=0) or a.min()<0 or a.max()>1):
            raise ValueError('invalid allele nodes')
    df = [np.asarray(f,dtype=float) for f in donor_factors]
    rf = [np.asarray(f,dtype=float) for f in recipient_factors]
    sizes = [len(a)*(len(a)+1)//2 for a in nodes]
    for k in range(3):
        if (df[k].shape!=(sizes[k],dc.shape[k]) or rf[k].shape!=(sizes[k],rc.shape[k])
                or not np.isfinite(df[k]).all() or not np.isfinite(rf[k]).all()):
            raise ValueError('factor and joint core dimensions do not match')
    ranks = [int(a)*int(b) for a,b in zip(dc.shape,rc.shape)]
    output_values = prod(ranks)+sum(n*r for n,r in zip(sizes,ranks))
    if not isinstance(max_output_values,int) or max_output_values<1:
        raise ValueError('positive integer output budget required')
    if output_values>max_output_values:
        raise MemoryError(f'outcross output requires {output_values} values; budget {max_output_values}')
    factors = []
    for k,a in enumerate(nodes):
        pairs = np.array(list(combinations_with_replacement(range(len(a)),2)))
        kernel = birth_mutation_matrix(a,rate,sd,scheme)
        gametes = (kernel[pairs[:,0]]+kernel[pairs[:,1]])/2
        donor = gametes.T@df[k]
        recipient = gametes.T@rf[k]
        first = donor[pairs[:,0],:,None]*recipient[pairs[:,1],None,:]
        second = donor[pairs[:,1],:,None]*recipient[pairs[:,0],None,:]
        first += (pairs[:,0]!=pairs[:,1])[:,None,None]*second
        factors.append(first.reshape(sizes[k],ranks[k]))
    core = np.einsum('abc,def->adbecf',dc,rc).reshape(ranks)
    return core,tuple(factors)
