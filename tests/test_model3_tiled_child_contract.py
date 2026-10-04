import numpy as np
import pytest
from scripts.model3_tiled_child_contract import tiled_child_contract

def test_tiling_recovers_bounded_binary_contractions():
    rng=np.random.default_rng(591);dc=rng.normal(size=(6,6,6));rc=rng.normal(size=(6,6,6));ts=[rng.normal(size=(4,6,6)) for _ in range(3)]
    expected=np.einsum('abc,def,iad,jbe,kcf->ijk',dc,rc,*ts,optimize=True)
    actual,r=tiled_child_contract(dc,rc,ts,budget=500)
    np.testing.assert_allclose(actual,expected,atol=1e-10,rtol=1e-12)
    assert r['tiles']>1
    assert actual.size<=500

def test_output_larger_than_cap_is_rejected():
    with pytest.raises(MemoryError):tiled_child_contract(np.ones((2,2,2)),np.ones((2,2,2)),[np.ones((10,2,2))]*3,budget=100)
