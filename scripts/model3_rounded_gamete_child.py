"""Streamed outcross core with a shared local approximation budget."""
from math import prod,sqrt
from itertools import combinations_with_replacement
import numpy as np
from scripts.model3_compressed_step import contract,check_size,mass
from scripts.model3_exact_gamete_factors import reduce_gamete_factors
from scripts.model3_island.density import birth_mutation_matrix
from scripts.model3_binary_reader_projection import project_child_core
from scripts.model3_rounded_gametes import rounded_gametes


def streamed_outcross(donor,recipient,axes,rate,sd,scheme,*,relative_l1,budget,force_stream=False):
    dc,df=donor;rc,rf=recipient
    expected=mass(donor)*mass(recipient)
    if expected<0 or not np.isfinite(expected):raise ArithmeticError('invalid channel mass')
    if expected==0 and (not np.any(dc) or not np.any(rc)):
        return (np.zeros((1,1,1)),tuple(np.zeros((len(f),1)) for f in df)),dict(absolute_l1_bound=0.)
    if expected<=0:raise ArithmeticError('zero signed channel mass')
    (dc,dg),(rc,rg),gamete_receipt=rounded_gametes(donor,recipient,axes,rate,sd,scheme,relative_l1=relative_l1,budget=budget)
    gamete_bound=gamete_receipt["absolute_l1_bound"]
    q,transforms,receipt=reduce_gamete_factors(dc,rc,dg,rg,absolute_l1=(expected*relative_l1-gamete_bound)/2,max_values=budget)
    receipt=dict(receipt,absolute_l1_bound=receipt["absolute_l1_bound"]+gamete_bound,gamete_receipt=gamete_receipt)
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
    result,bases,info=project_child_core(dc,rc,transforms,
        absolute_frobenius=remaining/sqrt(physical),budget=budget,initial_rank=128)
    factors=tuple(f if b is None else f@b for f,b in zip(q,bases))
    total=receipt['absolute_l1_bound']+sqrt(physical)*info['residual_frobenius_upper']
    if total>expected*relative_l1:raise ArithmeticError('combined local error exceeds budget')
    return (result,tuple(factors)),dict(absolute_l1_bound=total,streamed=True,
        factor_receipt=receipt,projection_receipt=info,
        bound_scope='factor truncation plus directly measured projection residual; excludes roundoff')

