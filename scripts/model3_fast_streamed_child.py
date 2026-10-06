"""Streamed outcross core with a shared local approximation budget."""
from math import prod,sqrt
from itertools import combinations_with_replacement
import numpy as np
from scripts.model3_compressed_step import contract,check_size,mass
from scripts.model3_child_factor_bound import reduce_child_factors
from scripts.model3_island.density import birth_mutation_matrix
from functools import partial
from scripts.model3_rank_hint_projection import project_columns as _project_columns
project_columns=partial(_project_columns,initial_rank=128)


def streamed_outcross(donor,recipient,axes,rate,sd,scheme,*,relative_l1,budget,force_stream=False):
    dc,df=donor;rc,rf=recipient
    expected=mass(donor)*mass(recipient)
    if expected<0 or not np.isfinite(expected):raise ArithmeticError('invalid channel mass')
    if expected==0 and (not np.any(dc) or not np.any(rc)):
        return (np.zeros((1,1,1)),tuple(np.zeros((len(f),1)) for f in df)),dict(absolute_l1_bound=0.)
    if expected<=0:raise ArithmeticError('zero signed channel mass')
    child=[]
    for k,axis in enumerate(axes):
        pairs=np.array(list(combinations_with_replacement(range(len(axis)),2)))
        check_size(len(pairs)*dc.shape[k]*rc.shape[k],budget)
        kernel=birth_mutation_matrix(np.asarray(axis),rate,sd,scheme)
        gametes=(kernel[pairs[:,0]]+kernel[pairs[:,1]])/2
        d=gametes.T@df[k];r=gametes.T@rf[k]
        f=d[pairs[:,0],:,None]*r[pairs[:,1],None,:]
        f+=(pairs[:,0]!=pairs[:,1])[:,None,None]*(d[pairs[:,1],:,None]*r[pairs[:,0],None,:])
        child.append(f.reshape(len(pairs),-1))
    q,transforms,receipt=reduce_child_factors(dc,rc,child,absolute_l1=expected*relative_l1/2,max_values=budget)
    transforms=[t.reshape(t.shape[0],dc.shape[k],rc.shape[k]) for k,t in enumerate(transforms)]
    equation='abc,def,iad,jbe,kcf->ijk'
    operands=[dc,rc,*transforms];shape=tuple(t.shape[0] for t in transforms)
    path,_=np.einsum_path(equation,*operands,optimize=('greedy',budget))
    use_stream=force_stream or prod(shape)>budget or any(len(step)>2 for step in path[1:])
    if not use_stream:
        result=contract(equation,*operands,budget=budget)
        return (result,q),dict(receipt,streamed=False)
    physical=prod(f.shape[0] for f in q)
    remaining=expected*relative_l1-receipt['absolute_l1_bound']
    if remaining<=0:raise ArithmeticError('no residual budget remains')
    def read(start,stop):
        lo=start//shape[2];hi=(stop+shape[2]-1)//shape[2]
        args=operands.copy();args[3]=args[3][lo:hi]
        block=contract(equation,*args,budget=budget).reshape(shape[0],-1)
        return block[:,start-lo*shape[2]:stop-lo*shape[2]]
    projection,flat,info=project_columns(read,(shape[0],shape[1]*shape[2]),
        absolute_frobenius=remaining/sqrt(physical),budget=budget,block_columns=4*shape[2])
    factors=list(q);factors[0]=factors[0]@projection
    result=flat.reshape(flat.shape[0],shape[1],shape[2])
    total=receipt['absolute_l1_bound']+sqrt(physical)*info['residual_frobenius']
    if total>expected*relative_l1:raise ArithmeticError('combined local error exceeds budget')
    return (result,tuple(factors)),dict(absolute_l1_bound=total,streamed=True,
        factor_receipt=receipt,projection_receipt=info,
        bound_scope='factor truncation plus directly measured projection residual; excludes roundoff')

