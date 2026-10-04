import numpy as np
import pytest
from scripts.model3_rank_hint_projection import project_columns
from scripts.model3_direct_stream_projection import project_columns as original

def test_rank_hint_skips_failed_trials_without_changing_accepted_projection():
    rng=np.random.default_rng(808);a=rng.normal(size=(50,10))@rng.normal(size=(10,100))
    read=lambda s,t:a[:,s:t]
    q,b,old=original(read,a.shape,absolute_frobenius=1e-10,budget=10000,block_columns=10)
    h,c,new=project_columns(read,a.shape,absolute_frobenius=1e-10,budget=10000,block_columns=10,initial_rank=16)
    assert old['rank']==new['rank']==16
    np.testing.assert_array_equal(q,h);np.testing.assert_array_equal(b,c)
    assert new['block_reads']<old['block_reads']

def test_large_hint_respects_allocation_cap():
    a=np.ones((20,50))
    q,b,r=project_columns(lambda s,t:a[:,s:t],a.shape,absolute_frobenius=1e-10,budget=300,initial_rank=128)
    assert b.size<=300
    assert r['residual_frobenius']<=1e-10

def test_invalid_hint_rejected():
    with pytest.raises(ValueError):project_columns(lambda s,t:np.ones((4,t-s)),(4,10),absolute_frobenius=1e-9,initial_rank=0)
