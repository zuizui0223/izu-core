"""Stream the common-core sum, then project without allocating that full core."""
from math import prod,sqrt
import numpy as np
from scripts.model3_compressed_step import contract,check_size
from scripts.model3_streamed_basis import project_basis


def streamed_sum(states,*,absolute_l1,budget=2_000_000,initial_rank=128):
    if not states or not np.isfinite(absolute_l1) or absolute_l1<=0:raise ValueError('positive tolerance and states required')
    physical=tuple(f.shape[0] for f in states[0][1]);bases=[];transforms=[]
    for k in range(3):
        if any(fs[k].shape[0]!=physical[k] for _,fs in states):raise ValueError('different physical grids')
        widths=[core.shape[k] for core,_ in states];check_size(physical[k]*sum(widths),budget)
        q,r=np.linalg.qr(np.concatenate([fs[k] for _,fs in states],axis=1),mode='reduced')
        bases.append(q);transforms.append(np.split(r,np.cumsum(widths)[:-1],axis=1))
    shape=[q.shape[1] for q in bases];reduced=[list(t) for t in transforms];receipts=[]
    for axis in sorted(range(3),key=lambda k:shape[k],reverse=True):
        order=[axis]+[j for j in range(3) if j!=axis];m,n,k=[shape[j] for j in order]
        def read(start,stop):
            check_size(m*(stop-start),budget);block=np.zeros((m,stop-start));cursor=start
            while cursor<stop:
                j=cursor//k;end=min(stop,(j+1)*k)
                for i,(core,_) in enumerate(states):
                    args=[transforms[a][i] for a in order]
                    piece=contract('abc,ia,jb,kc->ijk',core.transpose(order),args[0],args[1][j:j+1],args[2][cursor-j*k:end-j*k],budget=budget)
                    block[:,cursor-start:end-start]+=piece.reshape(m,-1)
                cursor=end
            return block
        p,info=project_basis(read,(m,n*k),absolute_frobenius=absolute_l1/(3*sqrt(prod(physical))),budget=budget,block_columns=k,initial_rank=initial_rank)
        reduced[axis]=[p.T@t for t in transforms[axis]];bases[axis]=bases[axis]@p
        receipts.append(dict(axis=axis,**info))
        if prod(t[0].shape[0] for t in reduced)<=budget:break
    outshape=tuple(t[0].shape[0] for t in reduced);check_size(prod(outshape),budget);result=np.zeros(outshape)
    for i,(core,_) in enumerate(states):result+=contract('abc,ia,jb,kc->ijk',core,*(t[i] for t in reduced),budget=budget)
    bound=sqrt(prod(physical))*sum(v['residual_frobenius'] for v in receipts)
    if bound>absolute_l1:raise ArithmeticError('sum projection error exceeds budget')
    return (result,tuple(bases)),dict(absolute_l1_bound=bound,ranks=list(outshape),projections=receipts,scope='sum of measured orthogonal projection residuals; roundoff excluded')
