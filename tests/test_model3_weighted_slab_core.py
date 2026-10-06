import importlib
import numpy as np
import pytest
from scripts.model3_weighted_core_stream import exact_core


@pytest.mark.parametrize('shape',[(4,5,7,9,2,3),(4,5,7,2,9,3),(4,5,7,6,6,2)])
def test_signed_both_contraction_orders_match_original(shape):
    a,b,k,m,n,s=shape;rng=np.random.default_rng(94)
    core=rng.normal(size=(a,b,k));left=rng.normal(size=(m,a,s));right=rng.normal(size=(n,b,s))
    candidate=importlib.import_module('scripts.model3_weighted_slab_core')
    budget=max(m*n*k,m*b,a*n,a*b)
    observed=candidate.exact_core(core,left,right,budget=budget)
    np.testing.assert_allclose(observed,exact_core(core,left,right,budget=budget),rtol=2e-13,atol=2e-13)


def test_rejects_output_above_budget():
    candidate=importlib.import_module('scripts.model3_weighted_slab_core')
    with pytest.raises(MemoryError):candidate.exact_core(np.ones((2,2,4)),np.ones((5,2,1)),np.ones((5,2,1)),budget=99)
