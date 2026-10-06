import numpy as np
import pytest
from scripts.audit_model3_resolution_screen import exact_decay, assess, memory_floor


def test_exact_reference_retains_operator_distinction():
    modes=np.arange(1,9)
    np.testing.assert_array_equal(exact_decay(modes,0,.05,'jump'),np.ones(8))
    np.testing.assert_allclose(exact_decay(modes,1,.05,'jump'),exact_decay(modes,1,.05,'heat_fv'))
    assert np.max(abs(exact_decay(modes,.01,.05,'jump')**200-exact_decay(modes,.01,.05,'heat_fv')**200))>.01


def test_refinement_reduces_mutation_discretization_error():
    coarse=assess(9,'jump',horizons=(1,200))
    fine=assess(65,'jump',horizons=(1,200))
    assert fine['primary_max_error']<coarse['primary_max_error']
    assert fine['variance_relative_error']<.01
    assert coarse['variance_relative_error']>.1


def test_memory_floor_accounts_for_diploid_joint_space():
    r=memory_floor(17)
    assert r['genotypes']==3581577
    assert r['gamete_pairs']==17**6
    assert r['bytes_lower_bound']==3581577*(6*8+8)+17**6*(8+4)


def test_reference_rejects_unknown_scheme():
    with pytest.raises(ValueError):exact_decay([1],.01,.05,'unknown')
