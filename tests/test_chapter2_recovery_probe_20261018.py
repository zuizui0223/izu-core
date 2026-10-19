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

def test_no_return_clock_has_explicit_zero_success_precision_floor():
    """No biological draw: exact Wilson width and strict 0.2 cutoff arithmetic."""
    gate=probe.threshold_precision_feasibility(8,.2,6)
    assert gate['future_replicates_per_occupied_state']==8
    assert gate['minimum_nested_futures_for_zero_success_upper_strictly_below_cutoff']==28
    assert abs(gate['best_possible_zero_success_upper_95']-0.4652549912165375)<1e-12
    assert gate['any_candidate_threshold_possible_at_this_replicate_count'] is False
    resolved=probe.threshold_precision_feasibility(28,.2,6)
    assert resolved['any_candidate_threshold_possible_at_this_replicate_count'] is True
    assert resolved['best_possible_zero_success_upper_95']<.2
    with pytest.raises(ValueError):
        probe.threshold_precision_feasibility(0,.2,6)


def test_static_genotype_pollen_service_assay_has_no_population_updates():
    """Technical fake ledger: fixed census, no mutation, parentage or advance."""
    from types import SimpleNamespace
    state=object()
    cfg=object()
    calls=[]
    class Ledger:
        def reproduce(self, resident, visitor, conf):
            assert resident is state and conf is cfg
            calls.append(visitor)
            return SimpleNamespace(outcross=np.array([[float(visitor)]]))
    observed=probe.fixed_genotype_service_assay(state,(0,2,4),cfg,Ledger())
    assert observed==6.
    assert calls==[0,2,4]


def test_visitor_histories_start_from_same_exact_assigned_original_community():
    """Uses the existing exogenous history kernel only; NO plant updates."""
    import json
    from dataclasses import replace
    from pathlib import Path
    from scripts.model3_island.types import Config, VisitorState
    from scripts.model3_island.history import make_history

    base=Path(__file__).resolve().parents[1]/'data/design/model3_island_v2.json'
    config=Config.from_dict(json.loads(base.read_text())['base_config'])
    config=replace(config,years=20,island_history='separation',initial_visitors=3)
    initial=VisitorState(
        np.array([10,11,12],dtype=np.int64),
        np.array([.3,.5,.7]),
        np.full(3,.2),np.ones(3))
    sham=make_history(config,seed=172941,inherited_visitors=initial)
    stronger=replace(config,visitor_arrival=replace(config.visitor_arrival,supply=.3,distance=0.))
    return_arm=make_history(stronger,seed=172941,inherited_visitors=initial)
    for name in ('ids','optima','breadths','effectiveness'):
        np.testing.assert_array_equal(getattr(sham.visitors[0],name),
                                      getattr(return_arm.visitors[0],name))
    np.testing.assert_array_equal(
        np.array([len(v.ids) for v in return_arm.visitors]),
        np.array([len(v.ids) for v in make_history(
            stronger,seed=172941,inherited_visitors=initial).visitors]))
    assert len(sham.visitors)==len(return_arm.visitors)==20
