"""No-visitor ecological falsifier, tested against the ORIGINAL Model3 ledger."""
import numpy as np
import pytest

from scripts.audit_chapter2_q3q4_no_visitor_20261011 import (
    STATUS,SETTINGS,BUDGETS,SCENARIOS,states,visitors,mu_and_q,transition,audit
)


def test_zero_visitor_means_exactly_zero_outcross_and_external_delivery():
    assert len(visitors("visitors0").ids)==0
    for s in SETTINGS:
        for b in BUDGETS:
            mu,q,delivered,outcross=mu_and_q((0,8,0),s,b,"visitors0","native")
            assert mu>0
            assert delivered == 0 and outcross == 0
            np.testing.assert_allclose(q,[.25,.5,.25],atol=1e-12,rtol=0)
    with pytest.raises(ValueError):
        visitors("invented")


def test_original_source_no_visitor_rule_equivalences_and_own_cost_control():
    for b in BUDGETS:
        mu=[mu_and_q((0,8,0),s,b,"visitors0","native")[0] for s in SETTINGS]
        assert mu[0]==pytest.approx(mu[1],abs=1e-11)
        assert mu[0]==pytest.approx(mu[2],abs=1e-11)
        assert mu[3]<mu[0]


def test_source_transition_conservation_and_identical_first_generation():
    Tn=transition("delayed_control",6.,"visitors0","native")
    Tf=transition("delayed_control",6.,"visitors0","fixed_expression")
    assert Tn.shape==Tf.shape==(165,165)
    np.testing.assert_allclose(Tn.sum(axis=1),1.,atol=1e-12,rtol=0)
    np.testing.assert_allclose(Tf.sum(axis=1),1.,atol=1e-12,rtol=0)
    assert Tn[0,0]==1. and Tf[0,0]==1.
    ix=states().index((0,8,0))
    np.testing.assert_allclose(Tn[ix],Tf[ix],atol=1e-12,rtol=0)


def test_original_no_visitor_source_reverses_budget6_q3q4_result():
    r=audit()
    assert r["status"]==STATUS
    assert r["n_cases"]==16 and r["states"]==165
    assert r["new_history_draws"]==0
    assert r["independent_confirmation"] is False
    rows={(x["setting"],x["resource_budget"],x["visitor_scenario"]):x for x in r["results"]}
    assert len(rows)==16
    for s in SETTINGS:
        a=rows[s,6.,"visitors4"]
        b=rows[s,6.,"visitors0"]
        assert a["P80_native_minus_fixed"]<0
        assert b["P80_native_minus_fixed"]>0
        assert b["source_N8_total_delivered_pollen"] == 0
        assert b["source_N8_outcross_seeds"] == 0
        assert abs(b["trajectory"][0])<1e-12
        assert abs(b["trajectory"][1])<1e-12

    expected_positive={
      "delayed_control":.0032565042540895,
      "prior_selfing":.0032565042540895,
      "pollen_discount":.0032565042540895,
      "assurance_cost":.0003329641387714,
    }
    for s,v in expected_positive.items():
        assert rows[s,6.,"visitors0"]["P80_native_minus_fixed"]==pytest.approx(v,abs=3e-8)
    assert rows["delayed_control",6.,"visitors4"]["P80_native_minus_fixed"]==pytest.approx(
        -.0039708198486585,abs=2e-10
    )


def test_source_absence_does_not_guarantee_positive_effect_at_other_budget():
    d=audit()
    lookup={(x["setting"],x["resource_budget"],x["visitor_scenario"]):x for x in d["results"]}
    for s in SETTINGS[:3]:
        assert lookup[s,8.,"visitors0"]["P80_native_minus_fixed"] == pytest.approx(
            -.01256875349766029,abs=1e-7
        )
    assert lookup["assurance_cost",8.,"visitors0"]["P80_native_minus_fixed"]==pytest.approx(
        +.012284231329036943,abs=1e-7
    )
    for s in SETTINGS:
        assert lookup[s,8.,"visitors4"]["P80_native_minus_fixed"]<0


def test_invalid_source_controls_fail_closed():
    with pytest.raises(ValueError):
        mu_and_q((0,8,0),"invented",6.,"visitors0","native")
    with pytest.raises(ValueError):
        mu_and_q((0,8,0),"prior_selfing",4.5,"visitors0","native")
    with pytest.raises(ValueError):
        mu_and_q((0,8,0),"prior_selfing",6.,"visitors7","native")
