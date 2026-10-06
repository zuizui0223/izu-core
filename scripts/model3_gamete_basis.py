"""Exact QR re-expression after Mendelian gametes and birth mutation."""
from itertools import combinations_with_replacement
import numpy as np
from scripts.model3_island.density import birth_mutation_matrix
from scripts.model3_compressed_step import contract,check_size


def gamete_basis(state,axes,rate,sd,scheme,*,budget):
    core,fs=state;qs=[];rs=[]
    for k,axis in enumerate(axes):
        pairs=np.array(list(combinations_with_replacement(range(len(axis)),2)))
        if fs[k].shape[0]!=len(pairs):raise ValueError('genotype axis mismatch')
        kernel=birth_mutation_matrix(np.asarray(axis),rate,sd,scheme)
        check_size(len(pairs)*len(axis),budget)
        gametes=(kernel[pairs[:,0]]+kernel[pairs[:,1]])/2
        q,r=np.linalg.qr(gametes.T@fs[k],mode='reduced');qs.append(q);rs.append(r)
    new=contract('abc,ia,jb,kc->ijk',core,*rs,budget=budget)
    return new,tuple(qs)
