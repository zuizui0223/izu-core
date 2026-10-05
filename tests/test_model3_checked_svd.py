import numpy as np
import pytest
from scripts.model3_checked_svd import checked_svd

def test_fallback_reconstructs_when_primary_driver_fails(monkeypatch):
 def fail(*a,**k):raise np.linalg.LinAlgError('forced primary failure')
 monkeypatch.setattr(np.linalg,'svd',fail)
 a=np.random.default_rng(53).normal(size=(17,9))
 u,s,v,info=checked_svd(a)
 assert np.allclose((u*s)@v,a,rtol=1e-12,atol=1e-12)
 assert info['driver']=='gesvd'
 assert info['relative_residual']<1e-10

def test_corrupt_fallback_is_rejected(monkeypatch):
 import scipy.linalg
 def fail(*a,**k):raise np.linalg.LinAlgError('forced primary failure')
 monkeypatch.setattr(np.linalg,'svd',fail)
 monkeypatch.setattr(scipy.linalg,'svd',lambda *a,**k:(np.eye(3),np.ones(3),np.eye(3)))
 with pytest.raises(ArithmeticError):checked_svd(np.ones((3,3)))

@pytest.mark.parametrize('a',[np.array([[float('nan')]]),np.array([[float('inf')]]),np.ones(3)])
def test_invalid_input_is_rejected(a):
 with pytest.raises(ValueError):checked_svd(a)
