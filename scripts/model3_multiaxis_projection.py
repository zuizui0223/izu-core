"""Multiaxis child projection before allocating a large joint core."""
from math import prod
import numpy as np
from scripts.model3_compressed_step import contract,check_size
from scripts.model3_streamed_basis import project_basis


def project_child_core(dc,rc,transforms,*,absolute_frobenius,budget=2_000_000,initial_rank=128):
    if not np.isfinite(absolute_frobenius) or absolute_frobenius<=0:raise ValueError('positive tolerance required')
    equation='abc,def,iad,jbe,kcf->ijk';shape=[t.shape[0] for t in transforms]
    bases=[None]*3;reduced=list(transforms);receipts=[]
    for axis in sorted(range(3),key=lambda k:shape[k],reverse=True):
        order=[axis]+[k for k in range(3) if k!=axis]
        original=[dc.transpose(order),rc.transpose(order),*[transforms[k] for k in order]]
        m,n,k=[shape[j] for j in order]
        def read(start,stop):
            lo=start//k;hi=(stop+k-1)//k
            if m*(hi-lo)*k<=budget:
                args=original.copy();args[3]=args[3][lo:hi]
                b=contract(equation,*args,budget=budget).reshape(m,-1)
                return b[:,start-lo*k:stop-lo*k]
            check_size(m*(stop-start),budget);b=np.empty((m,stop-start));cursor=start
            while cursor<stop:
                j=cursor//k;end=min(stop,(j+1)*k);args=original.copy()
                args[3]=args[3][j:j+1];args[4]=args[4][cursor-j*k:end-j*k]
                b[:,cursor-start:end-start]=contract(equation,*args,budget=budget).reshape(m,-1);cursor=end
            return b
        basis,info=project_basis(read,(m,n*k),absolute_frobenius=absolute_frobenius/3,
            budget=budget,block_columns=4*k,initial_rank=initial_rank)
        bases[axis]=basis
        reduced[axis]=(basis.T@transforms[axis].reshape(m,-1)).reshape(basis.shape[1],*transforms[axis].shape[1:])
        receipts.append(dict(axis=axis,**info))
        if prod(t.shape[0] for t in reduced)<=budget:
            path,_=np.einsum_path(equation,dc,rc,*reduced,optimize=('greedy',budget))
            if all(len(p)==2 for p in path[1:]):break
    check_size(prod(t.shape[0] for t in reduced),budget)
    path,_=np.einsum_path(equation,dc,rc,*reduced,optimize=('greedy',budget))
    if any(len(p)>2 for p in path[1:]):raise MemoryError('no bounded binary final contraction path')
    core=contract(equation,dc,rc,*reduced,budget=budget)
    error=sum(r['residual_frobenius'] for r in receipts)
    if error>absolute_frobenius:raise ArithmeticError('combined projection error exceeds budget')
    return core,tuple(bases),dict(residual_frobenius_upper=error,projections=receipts,
        scope='sum of direct orthogonal projection residuals; roundoff excluded')
