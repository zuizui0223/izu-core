"""Exact one-step locus marginals from a joint input, not a marginal closure.

Does not propagate joint correlations or replace a full genotype solver.
"""
from itertools import combinations_with_replacement
import numpy as np
from scripts.model3_compressed_ecology import ecological_weights
from scripts.model3_compressed_selfing import local_selfing
from scripts.model3_island.density import birth_mutation_matrix


def weighted_marginals(state,xy,assurance,maps):
    core,fs=state;ca=np.broadcast_to(assurance,(len(fs[2]),))
    grouped=[]
    for k in range(2):
        g=np.zeros((xy.shape[k],core.shape[k]));np.add.at(g,maps[k],fs[k]);grouped.append(g)
    ab=np.einsum('abc,c->ab',core,ca@fs[2],optimize=True)
    x=np.einsum('ia,ab,ib->i',fs[0],ab,(xy@grouped[1])[maps[0]],optimize=True)
    y=np.einsum('jb,ab,ja->j',fs[1],ab,(xy.T@grouped[0])[maps[1]],optimize=True)
    z=ca*(fs[2]@np.einsum('abc,ab->c',core,grouped[0].T@xy@grouped[1],optimize=True))
    return [x,y,z]


def exact_next_marginals(state,axes,visitors,config,*,scheme='jump'):
    if config.assurance_mode!='evolving':raise ValueError('requires evolving assurance')
    w=ecological_weights(*state,axes,visitors,config)
    def parents(name,ch=None):
        xy=w[name+'_xy'] if ch is None else w[name+'_xy'][:,:,ch]
        return weighted_marginals(state,xy,w[name+'_a'],w['maps'])
    sm=parents('self');out=[];gametes=[];pairsets=[]
    for k,axis in enumerate(axes):
        axis=np.asarray(axis);pairs=np.array(list(combinations_with_replacement(range(len(axis)),2)))
        kernel=birth_mutation_matrix(axis,config.mutation_rate,config.mutation_sd,scheme)
        gametes.append((kernel[pairs[:,0]]+kernel[pairs[:,1]])/2);pairsets.append(pairs)
        out.append(local_selfing(axis,config.mutation_rate,config.mutation_sd,scheme).T@sm[k])
    for ch in range(w['donor_xy'].shape[2]):
        dm=parents('donor',ch);rm=parents('recipient',ch)
        for k,(g,pairs) in enumerate(zip(gametes,pairsets)):
            d=g.T@dm[k];r=g.T@rm[k]
            out[k]+=d[pairs[:,0]]*r[pairs[:,1]]+(pairs[:,0]!=pairs[:,1])*d[pairs[:,1]]*r[pairs[:,0]]
    core,fs=state;sums=[f.sum(axis=0) for f in fs];old=[]
    for k in range(3):
        vec=np.einsum('abc,'+','.join('abc'[j] for j in range(3) if j!=k)+'->'+'abc'[k],core,*[sums[j] for j in range(3) if j!=k],optimize=True)
        old.append(fs[k]@vec)
    total=float(out[0].sum());space=max(0.,config.capacity-config.survival*old[0].sum())
    if not np.isfinite(total) or total<0:raise ArithmeticError('invalid offspring mass')
    retention=min(1.,space/total) if total>0 else 0.
    return [v*retention+config.survival*p for v,p in zip(out,old)]
