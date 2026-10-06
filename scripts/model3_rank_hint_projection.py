"""Direct-sketch blockwise mode projection with directly measured Frobenius residual.

Resource cap applies per array. Floating-point roundoff is not bounded.
The callback must return the same matrix blocks on every pass.
"""
from math import sqrt
import numpy as np
from scripts.model3_compressed_step import check_size


def project_columns(read,shape,*,absolute_frobenius,budget=2_000_000,block_columns=64,seed=997,initial_rank=8):
    if len(shape)!=2 or any(not isinstance(n,(int,np.integer)) or n<1 for n in shape):raise ValueError('positive matrix shape required')
    if not np.isfinite(absolute_frobenius) or absolute_frobenius<=0:raise ValueError('positive finite tolerance required')
    if not isinstance(block_columns,int) or block_columns<1:raise ValueError('positive block width required')
    if not isinstance(initial_rank,int) or initial_rank<1:raise ValueError('positive initial rank required')
    m,n=map(int,shape);check_size(1,budget)
    width=min(block_columns,budget//m,n)
    if width<1:raise MemoryError('one column exceeds budget')
    max_rank=min(m,n,budget//n)
    if max_rank<1:raise MemoryError('one projected row exceeds budget')
    def get(start,stop):
        b=np.asarray(read(start,stop),dtype=float)
        if b.shape!=(m,stop-start) or not np.isfinite(b).all():raise ValueError('invalid block')
        return b
    reads=0
    rank=min(initial_rank,max_rank);attempts=[]
    while True:
        check_size(m*rank,budget)
        rng=np.random.default_rng(seed);sketch=np.zeros((m,rank))
        for start in range(0,n,width):
            stop=min(n,start+width);b=get(start,stop)
            sketch+=b@rng.normal(size=(stop-start,rank));reads+=1
        q,_=np.linalg.qr(sketch,mode='reduced');residual2=0.
        for start in range(0,n,width):
            b=get(start,min(n,start+width));residual=b-q@(q.T@b)
            residual2+=float(np.sum(residual*residual));reads+=1
        error=sqrt(residual2);attempts.append(dict(rank=rank,residual_frobenius=error))
        if error<=absolute_frobenius:break
        if rank==max_rank:raise MemoryError(f'residual {error} exceeds {absolute_frobenius} at maximum admissible rank {rank}')
        rank=min(max_rank,rank*2)
    check_size(rank*n,budget);projected=np.empty((rank,n))
    for start in range(0,n,width):
        stop=min(n,start+width);projected[:,start:stop]=q.T@get(start,stop);reads+=1
    return q,projected,dict(residual_frobenius=error,rank=rank,attempts=attempts,block_reads=reads,
        seed=seed,initial_rank=initial_rank,method='direct Gaussian sketch plus QR; acceptance by full block residual',
        scope='directly measured projection residual; excludes floating-point roundoff')
