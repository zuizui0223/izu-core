"""Five technical recovery-probe fixtures; no new biological histories."""
import numpy as np
import pytest
from scripts import chapter2_recovery_probe_20261018 as probe


def alleles(values):
    v=np.asarray(values,dtype=float)
    a=np.full((len(v),3,2),.5)
    a[:,1,:]=v[:,None]
    return a


def test_upper_support_theorem_and_mutation_exclusion():
    assert probe.investment_support(alleles([.3,.4]),.5,mutation_I=False,seed_immigration=False)['closed']
    assert not probe.investment_support(alleles([.3,.5]),.5,mutation_I=False,seed_immigration=False)['closed']
    assert probe.investment_support(alleles([.3,.4]),.5,mutation_I=True,seed_immigration=False)['closed'] is None
    assert probe.investment_support(alleles([.3,.4]),.5,mutation_I=False,seed_immigration=True)['closed'] is None
    assert probe.investment_support(np.zeros((0,3,2)),.5,mutation_I=False,seed_immigration=False)['closed'] is None
    with pytest.raises(ValueError):probe.investment_support(alleles([.5]),float('nan'),mutation_I=False,seed_immigration=False)


def test_recovery_requires_sustained_run_not_just_final_point():
    assert not probe.first_sustained_recovery([.51,.49,.52,.48],.5,2)
    assert probe.first_sustained_recovery([.51,.49,.52,.52],.5,2)
    assert not probe.first_sustained_recovery([.51,None,.51],.5,2)
    with pytest.raises(ValueError):probe.first_sustained_recovery([.5],.5,0)


def test_t_star_requires_persistent_upper_ci_crossing():
    rows=[dict(t=25,conditional_interval=[0,.12]),dict(t=50,conditional_interval=[0,.30]),
          dict(t=100,conditional_interval=[0,.1])]
    assert probe.threshold_window(rows)==100
    assert probe.threshold_window([dict(t=25,conditional_interval=None)]+rows[1:])==100
    assert probe.threshold_window([dict(t=100,conditional_interval=[0,.3])]) is None
    assert probe.wilson(0,8)[1]>.2
    assert probe.wilson(0,32)[1]<.2


def test_cause_ledger_preserves_unresolved_and_overlapping_cases():
    assert probe.classify_failure(was_occupied=False,genetic_closed=None,local_gradient_sign='positive',success=False)=='extinct_before_restoration'
    assert probe.classify_failure(was_occupied=True,genetic_closed=True,local_gradient_sign='positive',success=False)=='genetically_inaccessible_target'
    assert probe.classify_failure(was_occupied=True,genetic_closed=True,local_gradient_sign='negative',success=False)=='genetic_and_other_or_selection'
    assert probe.classify_failure(was_occupied=True,genetic_closed=False,local_gradient_sign='positive',success=False)=='unresolved_finite_time_or_polymorphic_selection'
    assert probe.classify_failure(was_occupied=True,genetic_closed=False,local_gradient_sign='negative',success=False)=='nonpositive_local_selection_proxy'


def test_fresh_seed_namespace_unique_and_repeatable():
    seeds=[probe.seed_for('a',t,r,kind) for kind in ('visitors','population') for t in (25,50) for r in range(10)]
    assert len(set(seeds))==len(seeds)
    assert seeds==[probe.seed_for('a',t,r,kind) for kind in ('visitors','population') for t in (25,50) for r in range(10)]
    assert all(0<x<2**31-1 for x in seeds[:20])
    with pytest.raises(ValueError):probe.seed_for('a',25,0,'undefined')