import numpy as np
import pytest
from scripts.model3_rounded_gametes import rounded_gametes
from scripts.model3_gamete_basis import gamete_basis

def full(s):return np.einsum('abc,ia,jb,kc->ijk',s[0],*s[1],optimize=True)

@pytest.mark.parametrize('scheme',['jump','heat_fv'])
def test_transport_bound_covers_joint_product_error(scheme):
 rng=np.random.default_rng(519)
 donor=(rng.random((3,3,3)),[rng.random((6,3)) for _ in range(3)])
 recipient=(rng.random((3,3,3)),[rng.random((6,3)) for _ in range(3)])
 donor[0][:]*=48/full(donor).sum();recipient[0][:]/=full(recipient).sum()
 axes=([0,.5,1],)*3
 d,r,info=rounded_gametes(donor,recipient,axes,.01,.05,scheme,relative_l1=1e-8,budget=10000)
 before=[full(gamete_basis(s,axes,.01,.05,scheme,budget=10000)).ravel() for s in (donor,recipient)]
 after=[full(s).ravel() for s in (d,r)]
 error=np.abs(np.outer(*before)-np.outer(*after)).sum()
 assert error<=info['absolute_l1_bound']+1e-10
 assert info['absolute_l1_bound']<=48e-8/4
 assert full(d).sum()==pytest.approx(48)
 assert full(r).sum()==pytest.approx(1)

@pytest.mark.parametrize('tolerance',[0,-1,float('nan'),1])
def test_rejects_invalid_error_budget(tolerance):
 with pytest.raises(ValueError):rounded_gametes(None,None,None,0,0,'jump',relative_l1=tolerance,budget=100)
