"""Frozen abrupt vs gradual functional-pollinator loss: source and RNG contract."""
import json
import numpy as np
import pytest

from scripts.run_chapter2_sequence_abrupt_gradual_functional_loss_20261011 import (
    STATUS, SAMPLE_TIMES,
    contract,original_model_config,visitor_profile,functional_visitors,
    calibration,profile_plan,source_reference_state,order_from_trace,simulate,
)
from scripts.model3_island.reproduction import reproduce


def test_design_frozen_before_evolutionary_outcomes_and_complete_scope():
    d,h=contract()
    assert len(h)==64
    assert d["status"]=="FROZEN_BEFORE_EVOLUTIONARY_OUTCOME_EXECUTION"
    f=d["experimental_factorial"]
    n=(f["visitor_profile_history_seeds"]["count"]*
       f["demographic_repeat_seeds"]["count"]*
       len(f["mating_timing"])*len(f["direct_assurance_cost"])*
       len(f["mutation_rate"])*len(d["scheduled_window"]["schedules"]))
    assert n==1024
    assert d["execution_policy"]["current_result"]=="NONE"
    assert d["crossing"]["sustained_updates"]==20
    assert d["crossing"]["near_simultaneous_tolerance"]==5


def test_every_frozen_profile_has_monotone_baseline_loss_and_exact_equal_dose():
    d,_=contract()
    profile=d["experimental_factorial"]["visitor_profile_history_seeds"]
    original=source_reference_state(d)
    cfg=original_model_config("delayed",0.,0.,d)
    for seed in range(profile["first"],profile["last"]+1):
        plan=calibration(seed,d)
        lambdas_a=np.asarray(plan["abrupt_lambdas"])
        lambdas_g=np.asarray(plan["ramp_lambdas"])
        assert lambdas_a.shape==lambdas_g.shape==(100,)
        assert np.all((lambdas_a>=0)&(lambdas_a<=1))
        assert np.all((lambdas_g>=0)&(lambdas_g<=1))
        assert 0<plan["break_index"]<100
        assert abs(plan["baseline_pollen_ramp_total"]-
                   plan["baseline_pollen_abrupt_total"])<1e-9
        assert plan["reference_Dmatched"]>plan["reference_Dshifted"]>0
        start,end=visitor_profile(seed,d)
        sampled=[float(reproduce(
            original,functional_visitors(start,end,t),cfg
        ).delivered.sum()) for t in (0.,.25,.5,.75,1.)]
        assert all(sampled[i]>sampled[i+1] for i in range(4))
        assert np.isclose(sampled[0],plan["reference_Dmatched"],atol=1e-12)
        assert np.isclose(sampled[-1],plan["reference_Dshifted"],atol=1e-12)
        assert len(functional_visitors(start,end,.33).ids)==4


def test_original_biology_and_decoupled_mating_timing_assurance_cost():
    d,_=contract()
    for timing in ("delayed","prior"):
        for cost in (0.,.5):
            for mutation in (0.,.01):
                cfg=original_model_config(timing,cost,mutation,d)
                assert cfg.capacity==48
                assert cfg.years==400
                assert cfg.ovule_budget==8
                assert cfg.assurance_timing==timing
                assert cfg.assurance_cost==cost
                assert cfg.mutation_rate==mutation
                assert cfg.mutation_sd==.05
                assert cfg.assurance_mode=="evolving"
                assert cfg.seed_arrival.supply==0
                assert cfg.survival==0


def test_paired_real_diploid_sources_have_identical_initial_founder_genomes():
    a=simulate(48271001,49271001,"abrupt","delayed",.5,.01,
               years=30,record_gradients=False)
    b=simulate(48271001,49271001,"gradual","delayed",.5,.01,
               years=30,record_gradients=False)
    assert a["status"]==b["status"]==STATUS
    assert a["frozen_design_sha256"]==b["frozen_design_sha256"]
    np.testing.assert_array_equal(a["trace"][0],b["trace"][0])
    assert a["trace"][0][0]==48
    assert a["calibration"]==b["calibration"]
    assert abs(a["calibration"]["baseline_pollen_ramp_total"]-
               a["calibration"]["baseline_pollen_abrupt_total"])<1e-9
    assert len(a["trace"])==len(b["trace"])==31
    assert len(a["pollen_and_price_series"])==len(b["pollen_and_price_series"])==30
    # The sudden arm holds the matching visitor optima at the start, while
    # the gradual arm immediately introduces slight functional change.
    assert a["pollen_and_price_series"][0]["lambda"]==0.
    assert b["pollen_and_price_series"][0]["lambda"]==.005
    assert all(np.isfinite(row["delivered"]) for row in a["pollen_and_price_series"])
    assert all(row["N"]>=0 for row in a["pollen_and_price_series"])
    assert a["order"]["A_crossed_by100"] in (True,False)


def test_gradient_sampling_does_not_change_population_genetic_rng():
    a=simulate(48271001,49271001,"abrupt","prior",0.,0.,
               years=15,record_gradients=True)
    b=simulate(48271001,49271001,"abrupt","prior",0.,0.,
               years=15,record_gradients=False)
    np.testing.assert_array_equal(a["trace"],b["trace"])
    assert len(a["focal_gradient_samples"])==2 # t0 and t10
    assert len(b["focal_gradient_samples"])==0
    for row in a["focal_gradient_samples"]:
        assert row["t"] in SAMPLE_TIMES
        for trait in ("investment","assurance"):
            q=row[trait]
            assert q["n_evaluated"]<=8
            assert (q["n_positive"]+q["n_negative"]+q["n_near_zero"]+
                    q["n_boundary"])==q["n_evaluated"]


def test_sustained_genetic_crossings_not_first_single_noisy_update():
    d,_=contract()
    trace=np.full((48,10),np.nan)
    trace[:,0]=48
    trace[:,1:4]=.5
    trace[3:,3]=.6
    trace[14:,2]=.4
    o=order_from_trace(trace,47,d)
    assert o["A_crossing_update"]==3
    assert o["I_crossing_update"]==14
    assert o["order"]=="assurance_first"
    assert o["A_crossed_by100"] is True
    assert o["I_crossed_by100"] is True
    # An ephemeral change shorter than the 20-update sustained threshold
    # must NOT be recoded as evolutionary adaptation.
    trace[3:19,3]=.6
    trace[19:,3]=.5
    o=order_from_trace(trace,47,d)
    assert o["A_crossing_update"] is None
    assert o["order"]=="investment_only"


def test_design_rejects_unregistered_context():
    d,_=contract()
    with pytest.raises(ValueError):
        calibration(48270000,d)
    with pytest.raises(ValueError):
        functional_visitors(*visitor_profile(48271001,d),1.1)
    with pytest.raises(ValueError):
        original_model_config("invented",0.,.01,d)
    with pytest.raises(ValueError):
        simulate(48271001,49270000,"abrupt","delayed",.5,.01,years=2)
    with pytest.raises(ValueError):
        simulate(48271001,49271001,"jump","delayed",.5,.01,years=2)
    with pytest.raises(ValueError):
        simulate(48271001,49271001,"abrupt","delayed",.5,.01,years=401)
