"""Exact bounded small-grid reproductive integration on joint Tucker states.

No truncation yet: this validates algebra, not high-resolution scalability.
Scope: evolving assurance, no plant immigration, all three loci mutable.
"""
from math import prod
import numpy as np
from scripts.model3_compressed_ecology import ecological_weights
from scripts.model3_compressed_selfing import local_selfing,selfed_factors
from scripts.model3_compressed_outcross import outcross_tucker


def check_size(size,budget):
    if not isinstance(budget,int) or budget<1:
        raise ValueError('positive integer budget required')
    if size>budget:
        raise MemoryError(f'explicit array size {size} exceeds budget {budget}')


def contract(equation,*arrays,budget):
    labels,output=equation.split('->'); labels=labels.split(',')
    dimensions={}
    for text,array in zip(labels,arrays):
        for label,size in zip(text,array.shape):
            if label in dimensions and dimensions[label]!=size:
                raise ValueError('contraction dimension mismatch')
            dimensions[label]=size
    path,_=np.einsum_path(equation,*arrays,optimize='greedy')
    labels=[set(s) for s in labels]
    for indices in path[1:]:
        selected=set().union(*(labels[i] for i in indices))
        remaining=[s for i,s in enumerate(labels) if i not in indices]
        retained=selected & set().union(set(output),*remaining)
        check_size(prod(dimensions[s] for s in retained),budget)
        labels=remaining+[retained]
    return np.einsum(equation,*arrays,optimize=path)


def weighted(state,xy,assurance,maps,*,budget=2_000_000):
    core,factors=state
    left,s,right=np.linalg.svd(xy,full_matrices=False)
    left=left*s
    p=len(s); new=[]; transforms=[]
    for k,w in enumerate((left[maps[0]],right.T[maps[1]])):
        check_size(factors[k].shape[0]*core.shape[k]*p,budget)
        raw=(factors[k][:,:,None]*w[:,None,:]).reshape(factors[k].shape[0],-1)
        q,r=np.linalg.qr(raw,mode='reduced')
        new.append(q); transforms.append(r.reshape(q.shape[1],core.shape[k],p))
    new.append(factors[2]*np.asarray(assurance)[:,None])
    result=contract('abc,ias,jbs->ijc',core,*transforms,budget=budget)
    return result,tuple(new)


def summed(states,*,budget=2_000_000):
    if not states:
        raise ValueError('at least one channel required')
    bases=[]; transforms=[]
    for k in range(3):
        widths=[c.shape[k] for c,f in states]
        check_size(states[0][1][k].shape[0]*sum(widths),budget)
        q,r=np.linalg.qr(np.concatenate([f[k] for c,f in states],axis=1),mode='reduced')
        bases.append(q); transforms.append(np.split(r,np.cumsum(widths)[:-1],axis=1))
    shape=tuple(b.shape[1] for b in bases);check_size(prod(shape),budget)
    core=np.zeros(shape)
    for index,(c,f) in enumerate(states):
        core+=contract('abc,ia,jb,kc->ijk',c,*(t[index] for t in transforms),budget=budget)
    return core,tuple(bases)


def mass(state):
    core,factors=state
    return float(np.einsum('abc,a,b,c',core,*(f.sum(axis=0) for f in factors)))


def compressed_step(state,axes,visitors,config,*,scheme='jump',budget=2_000_000,rounding=None):
    if config.assurance_mode!='evolving':
        raise ValueError('this integration gate requires evolving assurance')
    weights=ecological_weights(*state,axes,visitors,config)
    def reduce(value,stage):
        return rounding(value,stage) if rounding is not None else value
    def apply(name,channel=None):
        xy=weights[name+'_xy']
        if channel is not None:xy=xy[:,:,channel]
        return reduce(weighted(state,xy,weights[name+'_a'],weights['maps'],budget=budget),f'weight:{name}:{channel}')
    core,factors=apply('self')
    kernels=[local_selfing(a,config.mutation_rate,config.mutation_sd,scheme) for a in axes]
    births=[reduce((core,selfed_factors(factors,kernels)),'selfed_birth')]
    for channel in range(weights['donor_xy'].shape[2]):
        dc,df=apply('donor',channel);rc,rf=apply('recipient',channel)
        births.append(reduce(outcross_tucker(dc,df,rc,rf,axes,config.mutation_rate,
            config.mutation_sd,scheme,orthogonalize=True,max_output_values=budget,
            max_intermediate_values=budget),f'outcross_birth:{channel}'))
        if rounding is not None:
            births=[reduce(summed(births,budget=budget),f'sum:{channel}')]
    offspring=summed(births,budget=budget)
    total=mass(offspring)
    if total < -1e-10 or not np.isfinite(total):
        raise ArithmeticError('invalid offspring mass')
    space=max(0.,config.capacity-config.survival*mass(state))
    retention=min(1.,space/total) if total>0 else 0.
    retained=reduce((offspring[0]*retention,offspring[1]),'retained')
    if config.survival:
        return reduce(summed([retained,(state[0]*config.survival,state[1])],budget=budget),'survival')
    return retained
