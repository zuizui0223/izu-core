"""No prospective simulations: ledger algebra and OLD history 26110601 only."""
from dataclasses import fields

import numpy as np
import pytest

from scripts.chapter2_postzygotic_viability_gate import (
    FACTORIAL_GATES,apply_named_gate,gate_postzygotic_seed_viability,
    analyze_factorial_schedule_interactions,simulate_gated_future,
)
from scripts.model3_island.types import Ledger
from scripts.plan_chapter2_order_expression_identification import (
    Prehistory,load_protocol,
)
from scripts.chapter2_order_prehistory_runner import simulate_prehistory
from scripts.chapter2_order_postshock_runner import one_future,sampled_eight
from scripts.run_chapter2_assurance_generality import DEFAULT_DESIGN,load_design


def ledger_example():
    out=np.array([[0.,3.],[2.,0.]])
    viable=np.array([1.,4.])
    delivered=np.array([[0.,4.],[5.,0.]])
    exported=np.array([12.,10.])
    return Ledger(
        outcross=out, self_raw=np.array([2.,5.]), self_viable=viable,
        ovules=np.array([5.,9.]), exported=exported, delivered=delivered,
        lost=exported-delivered.sum(axis=1),
        maternal=out.sum(axis=0)+viable,
        paternal=out.sum(axis=1)+viable,
    )


def test_identity_does_not_reconstruct_or_round_original_reproductive_ledger():
    obj=ledger_example()
    assert apply_named_gate(obj,"baseline") is obj
    with pytest.raises(ValueError):
        apply_named_gate(obj,"posthoc_best")


def test_self_and_outcross_postzygotic_blocks_preserve_mass_accounting():
    original=ledger_example()
    snap={x.name:np.array(getattr(original,x.name),copy=True) for x in fields(Ledger)}
    for name,(s,o) in FACTORIAL_GATES.items():
        actual=apply_named_gate(original,name)
        assert np.allclose(actual.self_viable,original.self_viable*s)
        assert np.allclose(actual.outcross,original.outcross*o)
        assert np.allclose(actual.maternal,
                           actual.outcross.sum(axis=0)+actual.self_viable)
        assert np.allclose(actual.paternal,
                           actual.outcross.sum(axis=1)+actual.self_viable)
        assert np.all(actual.maternal <= actual.ovules+1e-9)
        for key in ("self_raw","ovules","exported","delivered","lost"):
            assert np.array_equal(getattr(original,key),getattr(actual,key))
    for key,value in snap.items():
        assert np.array_equal(getattr(original,key),value),key


@pytest.mark.parametrize("bad",[-0.5,1.1,float("nan"),float("inf"),True])
def test_invalid_or_unregistered_fraction_fails_closed(bad):
    with pytest.raises(ValueError):
        gate_postzygotic_seed_viability(
            ledger_example(),selfed_fraction=bad,outcross_fraction=1)


def test_factorial_history_pairing_cannot_resample_branch_pseudoreplicates():
    x=np.ones((64,4))
    x[:,0]=0.04
    x[:,1]=0.02
    x[:,2]=0.03
    x[:,3]=0.015
    eff=analyze_factorial_schedule_interactions(x)
    assert eff["primary_selfed_viability_sensitivity"].shape == (64,)
    assert np.allclose(eff["primary_selfed_viability_sensitivity"],0.02)
    assert np.allclose(eff["secondary_outcross_viability_sensitivity"],0.01)
    assert np.allclose(eff["factorial_nonadditivity"],0.005)
    with pytest.raises(ValueError):
        analyze_factorial_schedule_interactions(np.ones((172032,4)))


def test_old_archival_history_only_baseline_replay_and_gated_run():
    """No visitor ID from fresh 37110801 or 38110901 cohorts is sampled."""
    d=load_protocol()
    biology=load_design(DEFAULT_DESIGN)
    old=Prehistory("delayed_control","near","assurance_first",
                   26110601,26111601)
    assert old.visitor_history not in range(37110801,37110865)
    assert old.visitor_history not in range(38110901,38110965)
    state,_,_=simulate_prehistory(old,d,biology)
    selected=sampled_eight(old,state,d)
    genotype=np.array(state.alleles,copy=True)
    regime="eight_founders_capacity8"
    env="near"
    budget=3.
    original=one_future(old,state,selected,d,biology,regime,env,budget)
    exact=simulate_gated_future(
        old,state,selected,d,biology,regime,env,budget,
        intervention="baseline"
    )
    assert exact == original
    for arm in ("attenuate_self","attenuate_outcross","attenuate_both"):
        result=simulate_gated_future(
            old,state,selected,d,biology,regime,env,budget,intervention=arm
        )
        assert result["t0_population"]==original["t0_population"]
        assert result["budget"]==original["budget"]
        assert result["future_expression_offsets"]==[0,0]
        assert result["occupied"] in (0,1)
        assert result["selfed_recruits"]>=0
        assert result["outcross_recruits"]>=0
    assert np.array_equal(state.alleles,genotype)
