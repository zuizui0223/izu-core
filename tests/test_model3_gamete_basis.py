import numpy as np
import pytest
from itertools import combinations_with_replacement
from scripts.model3_gamete_basis import gamete_basis
from scripts.model3_island.density import birth_mutation_matrix

@pytest.mark.parametrize('scheme',['jump','heat_fv'])
def test_gamete_basis_is_exact_and_rank_capped(scheme):
 rng=np.random.default_rng(149);axes=([0,.5,1],)*3
 state=(rng.normal(size=(5,5,5)),[rng.normal(size=(6,5)) for _ in range(3)])
 result=gamete_basis(state,axes,.01,.05,scheme,budget=2000)
 pairs=np.array(list(combinations_with_replacement(range(3),2)))
 kernel=birth_mutation_matrix(np.array(axes[0]),.01,.05,scheme)
 g=(kernel[pairs[:,0]]+kernel[pairs[:,1]])/2
 direct=np.einsum('abc,ia,jb,kc->ijk',state[0],*[g.T@f for f in state[1]],optimize=True)
 actual=np.einsum('abc,ia,jb,kc->ijk',result[0],*result[1],optimize=True)
 np.testing.assert_allclose(actual,direct,rtol=1e-12,atol=1e-12)
 assert result[0].shape==(3,3,3)
