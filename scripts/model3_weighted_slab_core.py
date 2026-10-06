"""Exact weighted contraction over bounded slabs; no low-rank approximation."""
import numpy as np
from scripts.model3_compressed_step import check_size


def exact_core(core,left,right,*,budget):
    a,b,k=core.shape;m=left.shape[0];n=right.shape[0]
    if left.shape[1]!=a or right.shape[1]!=b or left.shape[2]!=right.shape[2]:
        raise ValueError('incompatible weighted factors')
    check_size(m*n*k,budget)
    first_left=m*b<=a*n
    temporary=m*b if first_left else a*n
    # Each contiguous reshape and matrix-product output obeys the array cap.
    per_slice=max(a*b,temporary,m*n)
    check_size(per_slice,budget)
    width=max(1,min(k,budget//per_slice))
    result=np.zeros((m,n,k))
    for start in range(0,k,width):
        stop=min(k,start+width);q=stop-start
        slab=np.ascontiguousarray(core[:,:,start:stop])
        for s in range(left.shape[2]):
            if first_left:
                work=left[:,:,s]@slab.reshape(a,b*q)
                product=work.reshape(m,b,q).transpose(0,2,1).reshape(m*q,b)@right[:,:,s].T
                result[:,:,start:stop]+=product.reshape(m,q,n).transpose(0,2,1)
            else:
                work=slab.transpose(0,2,1).reshape(a*q,b)@right[:,:,s].T
                product=left[:,:,s]@work.reshape(a,q,n).transpose(0,2,1).reshape(a,n*q)
                result[:,:,start:stop]+=product.reshape(m,n,q)
    return result
