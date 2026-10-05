"""Blockwise joint weighting, with measured projection residuals if needed."""
from math import prod, sqrt
import numpy as np
from scripts.model3_compressed_step import check_size
from scripts.model3_streamed_basis import project_basis


def exact_core(core, left, right, *, budget):
    shape=(left.shape[0],right.shape[0],core.shape[2])
    check_size(prod(shape),budget)
    result=np.zeros(shape)
    # Sum weight components and third-axis slices without a four-way intermediate.
    for c in range(shape[2]):
        for s in range(left.shape[2]):
            if left.shape[0]*core.shape[1] <= core.shape[0]*right.shape[0]:
                check_size(left.shape[0]*core.shape[1],budget)
                term=(left[:,:,s]@core[:,:,c])@right[:,:,s].T
            else:
                check_size(core.shape[0]*right.shape[0],budget)
                term=left[:,:,s]@(core[:,:,c]@right[:,:,s].T)
            result[:,:,c]+=term
    return result


def project_weighted(core, transforms, bases, third, *, absolute_l1, budget):
    physical=prod([len(bases[0]),len(bases[1]),len(third)])
    scale=sqrt(physical)*float(np.linalg.norm(third,2))
    if not np.isfinite(scale) or scale<=0:raise ArithmeticError('invalid projection norm')
    if not np.isfinite(absolute_l1) or absolute_l1<=0:raise ValueError('positive residual budget required')
    current=list(transforms);factors=list(bases);records=[]
    for axis in sorted([0,1],key=lambda k:current[k].shape[0],reverse=True):
        if current[0].shape[0]*current[1].shape[0]*core.shape[2]<=budget:break
        a=axis;b=1-axis
        local=core if a==0 else core.transpose(1,0,2)
        m,n,k=current[a].shape[0],current[b].shape[0],core.shape[2]
        def read(start,stop):
            check_size(m*(stop-start),budget)
            block=np.empty((m,stop-start));cursor=start
            while cursor<stop:
                row=cursor//k;end=min(stop,(row+1)*k)
                piece=exact_core(local[:,:,cursor-row*k:end-row*k],current[a],current[b][row:row+1],budget=budget)
                block[:,cursor-start:end-start]=piece.reshape(m,-1)
                cursor=end
            return block
        q,info=project_basis(read,(m,n*k),absolute_frobenius=absolute_l1/(2*scale),budget=budget,block_columns=k*8,initial_rank=min(128,m,max(1,budget//(n*k))))
        current[a]=np.einsum('iu,ias->uas',q,current[a],optimize=True)
        factors[a]=factors[a]@q
        records.append(dict(axis=a,**info))
    value=exact_core(core,*current,budget=budget)
    bound=scale*sum(r['residual_frobenius'] for r in records)
    if bound>absolute_l1:raise ArithmeticError('weight projection exceeds tolerance')
    return (value,tuple(factors+[third])),dict(absolute_l1_bound=bound,streamed=bool(records),projections=records,scope='measured joint-core projection residual; excludes roundoff')
