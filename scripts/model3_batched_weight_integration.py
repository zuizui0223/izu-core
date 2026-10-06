"""Bounded joint-genotype reproduction; local bounds are not global bounds."""
from itertools import combinations_with_replacement
import numpy as np
from scripts.model3_compressed_step import contract,check_size,mass,summed
from scripts.model3_compressed_ecology import ecological_weights
from scripts.model3_compressed_selfing import local_selfing,selfed_factors
from scripts.model3_sharp_rounding import rounded
from scripts.model3_bounded_sum import bounded_sum
from scripts.model3_streamed_sum import streamed_sum
from scripts.model3_child_factor_bound import reduce_child_factors
from scripts.model3_batched_weighting import bounded_weighted
from scripts.model3_island.density import birth_mutation_matrix


from scripts.model3_checked_gamete_child import streamed_outcross as bounded_outcross


def bounded_step(state,axes,visitors,config,*,scheme='jump',relative_l1=1e-8,budget=2_000_000):
    if not np.isfinite(relative_l1) or not 0<relative_l1<1:raise ValueError('invalid tolerance')
    if config.assurance_mode!='evolving':raise ValueError('requires evolving assurance')
    weights=ecological_weights(*state,axes,visitors,config);receipts=[]
    def reduce(value,stage,tolerance=None):
        result,info=rounded(value,relative_l1=relative_l1 if tolerance is None else tolerance,budget=budget)
        receipts.append(dict(stage=stage,**info));return result
    def combine(states,stage):
        try:value=summed(states,budget=budget)
        except MemoryError:
            total=sum(mass(s) for s in states)
            if not np.isfinite(total) or total<=0:raise ArithmeticError('invalid sum mass')
            try:value,info=bounded_sum(states,absolute_l1=relative_l1*total/2,budget=budget)
            except MemoryError:
                value,info=streamed_sum(states,absolute_l1=relative_l1*total/2,budget=budget)
            receipts.append(dict(stage='sum_projection:'+stage,**info))
            remaining=relative_l1*total-info['absolute_l1_bound']
            return reduce(value,stage,tolerance=min(relative_l1/2,remaining/mass(value)))
        return reduce(value,stage)
    def apply(name,channel=None):
        xy=weights[name+'_xy'];a=weights[name+'_a']
        if channel is not None:xy=xy[:,:,channel]
        if not np.any(xy) or not np.any(a):
            return reduce((np.zeros((1,1,1)),tuple(np.zeros((len(f),1)) for f in state[1])),f'weight:{name}:{channel}')
        grouped=[]
        for k in range(2):
            f=np.zeros((xy.shape[k],state[0].shape[k]));np.add.at(f,weights['maps'][k],state[1][k]);grouped.append(f)
        ca=np.broadcast_to(a,(len(state[1][2]),))@state[1][2]
        exact_mass=float(np.einsum('abc,ab,c',state[0],grouped[0].T@xy@grouped[1],ca,optimize=True))
        if not np.isfinite(exact_mass) or exact_mass<=0:raise ArithmeticError('invalid weighted mass')
        value,info=bounded_weighted(state,xy,a,weights['maps'],absolute_l1=relative_l1*exact_mass,budget=budget)
        receipts.append(dict(stage=f'weight_factor:{name}:{channel}',**info))
        return reduce(value,f'weight:{name}:{channel}')
    core,factors=apply('self')
    for axis in axes:check_size((len(axis)*(len(axis)+1)//2)**2,budget)
    kernels=[local_selfing(a,config.mutation_rate,config.mutation_sd,scheme) for a in axes]
    births=reduce((core,selfed_factors(factors,kernels)),'selfed_birth')
    for channel in range(weights['donor_xy'].shape[2]):
        donor=apply('donor',channel);recipient=apply('recipient',channel)
        child,info=bounded_outcross(donor,recipient,axes,config.mutation_rate,config.mutation_sd,scheme,relative_l1=relative_l1,budget=budget)
        receipts.append(dict(stage=f'child_factor:{channel}',**info))
        child=reduce(child,f'outcross_birth:{channel}')
        births=combine([births,child],f'sum:{channel}')
    total=mass(births)
    if not np.isfinite(total) or total<0:raise ArithmeticError('invalid offspring mass')
    space=max(0.,config.capacity-config.survival*mass(state));retention=min(1.,space/total) if total>0 else 0.
    result=reduce((births[0]*retention,births[1]),'retained')
    if config.survival:result=combine([result,(state[0]*config.survival,state[1])],'survival')
    return result,receipts
