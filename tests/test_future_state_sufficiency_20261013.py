import numpy as np
import pytest
from scripts import audit_future_state_sufficiency_20261013 as audit
from scripts import persistence_expression_mechanism_20261012 as native
from scripts.model3_island.types import PlantState


def state():
    return PlantState(np.full((2,3,2),.5),np.zeros((2,3,2),dtype=np.int64),np.zeros((2,3,2),dtype=bool),np.arange(2,dtype=np.int64),np.zeros(2,dtype=np.int64))


def test_eight_fixed_technical_pairs_share_origin_free_seeds():
    tasks=audit.technical_tasks()
    assert len(tasks)==8 and len({native.case_key(t) for t in tasks})==8
    for t in tasks:
        assert t['replicate']==0 and t['policy']=='native'
        other=dict(t,origin=native.ORIGINS[1-native.ORIGINS.index(t['origin'])])
        assert native.future_seed(t)==native.future_seed(other)


def test_relabel_preserves_full_ordered_genotypes_not_just_means():
    x=state();y=audit.relabel(x)
    np.testing.assert_array_equal(x.alleles,y.alleles)
    np.testing.assert_array_equal(x.birth_years,y.birth_years)
    assert not np.array_equal(x.ids,y.ids)
    assert not np.array_equal(x.allele_origin,y.allele_origin)
    assert not np.array_equal(x.mutation_flags,y.mutation_flags)


def test_dynamics_check_rejects_changed_genotype_even_same_mean():
    x={'population':np.array([2,2]),'alleles':state().alleles.copy(),'diagnostics':np.zeros((1,11))}
    y={k:v.copy() for k,v in x.items()};audit.assert_dynamics_equal(x,y)
    y['alleles'][0,0]=[.4,.6]
    with pytest.raises(AssertionError):audit.assert_dynamics_equal(x,y)
    y={k:v.copy() for k,v in x.items()};y['population'][1]=0
    with pytest.raises(AssertionError):audit.assert_dynamics_equal(x,y)


def test_registered_manual_workflow_routes_only_technical_pairs():
    from pathlib import Path
    s=Path('.github/workflows/chapter2-pr471-native-verification.yml').read_text(encoding='utf-8')
    assert 'future-state-sufficiency' in s
    assert 'python -m scripts.audit_future_state_sufficiency_20261013' in s
    assert 'cancel-in-progress: false' in s
