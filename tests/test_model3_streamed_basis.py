import numpy as np
from scripts.model3_streamed_basis import project_basis

def test_basis_can_fit_when_projected_matrix_cannot():
    rng=np.random.default_rng(342);a=rng.normal(size=(50,10))@rng.normal(size=(10,400))
    q,r=project_basis(lambda s,t:a[:,s:t],a.shape,absolute_frobenius=1e-10,budget=1500,block_columns=10,initial_rank=16)
    assert q.size<=1500
    assert q.shape[1]*a.shape[1]>1500
    assert np.linalg.norm(a-q@(q.T@a))<=r['residual_frobenius']+1e-11
    assert r['residual_frobenius']<=1e-10

def test_two_axis_projection_residual_is_bounded_by_sum():
    rng=np.random.default_rng(734);core=rng.normal(size=(3,4,2));u=[rng.normal(size=(n,k)) for n,k in [(20,3),(25,4),(8,2)]]
    tensor=np.einsum('abc,ia,jb,kc->ijk',core,*u)
    projections=[];errors=[]
    for axis in [0,1]:
        mat=np.moveaxis(tensor,axis,0).reshape(tensor.shape[axis],-1)
        q,r=project_basis(lambda s,t:mat[:,s:t],mat.shape,absolute_frobenius=1e-10,budget=3000,block_columns=10,initial_rank=8)
        projections.append(q);errors.append(r['residual_frobenius'])
    compressed=np.einsum('ijk,ia,jb->abk',tensor,*projections,optimize=True)
    recovered=np.einsum('abk,ia,jb->ijk',compressed,*projections,optimize=True)
    assert np.linalg.norm(tensor-recovered)<=sum(errors)+1e-10
