import importlib
import numpy as np
import pytest


@pytest.mark.parametrize('start,stop', [(0,56),(1,55),(7,28),(6,8),(34,35),(0,91)])
def test_aligned_and_partial_reads_match_full_signed_tensor(start,stop):
    read=importlib.import_module('scripts.model3_weighted_block_read').read_columns
    rng=np.random.default_rng(183)
    core=rng.normal(size=(5,4,7));left=rng.normal(size=(17,5,3));right=rng.normal(size=(13,4,3))
    expected=np.einsum('abc,ias,jbs->ijc',core,left,right).reshape(17,-1)[:,start:stop]
    actual=read(core,left,right,start,stop,budget=2000)
    np.testing.assert_allclose(actual,expected,rtol=1e-12,atol=1e-12)


def test_aligned_rows_use_one_contraction(monkeypatch):
    module=importlib.import_module('scripts.model3_weighted_block_read')
    original=module.exact_core; calls=[]
    def counted(core,left,right,**kwargs):
        calls.append(right.shape[0]);return original(core,left,right,**kwargs)
    monkeypatch.setattr(module,'exact_core',counted)
    module.read_columns(np.ones((5,4,7)),np.ones((17,5,3)),np.ones((13,4,3)),7,63,budget=2000)
    assert calls==[8]


def test_budget_rejected_before_allocation():
    read=importlib.import_module('scripts.model3_weighted_block_read').read_columns
    with pytest.raises(MemoryError):
        read(np.ones((5,4,7)),np.ones((17,5,3)),np.ones((13,4,3)),0,91,budget=1500)


@pytest.mark.parametrize('start,stop',[(-1,7),(7,7),(0,92),(0.5,7)])
def test_bad_intervals_rejected(start,stop):
    read=importlib.import_module('scripts.model3_weighted_block_read').read_columns
    with pytest.raises(ValueError):
        read(np.ones((5,4,7)),np.ones((17,5,3)),np.ones((13,4,3)),start,stop,budget=2000)
