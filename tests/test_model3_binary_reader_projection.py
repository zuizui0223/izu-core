import numpy as np
from scripts.model3_binary_reader_projection import project_child_core

def test_two_axes_reduce_output_that_cannot_be_materialized_within_budget(monkeypatch):
    import scripts.model3_binary_reader_projection as model
    calls=[];original=model.tiled_child_contract
    def traced(*a,**k):
        calls.append(1);return original(*a,**k)
    def forbidden(*a,**k):raise AssertionError("unbounded general reader contract")
    monkeypatch.setattr(model,"tiled_child_contract",traced)
    monkeypatch.setattr(model,"contract",forbidden,raising=False)
    rng=np.random.default_rng(991);dc=rng.normal(size=(2,2,2));rc=rng.normal(size=(2,2,2))
    transforms=[rng.normal(size=(n,2,2)) for n in [20,30,10]]
    exact=np.einsum('abc,def,iad,jbe,kcf->ijk',dc,rc,*transforms,optimize=True)
    core,bases,r=project_child_core(dc,rc,transforms,absolute_frobenius=1e-10,budget=500,initial_rank=4)
    assert core.size<=500
    fs=[np.eye(exact.shape[k]) if b is None else b for k,b in enumerate(bases)]
    recovered=np.einsum('abc,ia,jb,kc->ijk',core,*fs,optimize=True)
    assert np.linalg.norm(exact-recovered)<=r['residual_frobenius_upper']+1e-10
    assert len(r['projections'])>=2

    assert len(calls)>1
