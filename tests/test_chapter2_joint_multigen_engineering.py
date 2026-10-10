"""Bounded synthetic only: multi-generation source-matched reproducibility gates."""
import numpy as np
import pytest

from scripts.audit_chapter2_joint_multigen_engineering import (
    STATUS, VISITOR_REGIMES, engineering_fixture, condition_run, run_pilot,
)


def test_source_preserves_assurance_allele_variation_not_constant_fixed_half():
    state, cfg, visitors=engineering_fixture()
    assert len(state.ids)==8
    assert cfg.mutation_rate==0
    assert cfg.seed_arrival.supply==0
    assert state.alleles[:,:,0].shape==(8,3)
    assert np.var(state.alleles[:,2,:])>0, (
        "Cannot study assurance genetic transmission from a constant-allele fixture"
    )
    assert len(visitors["two_hand_authored"].ids)==2
    assert len(visitors["no_visitors"].ids)==0


def test_multigen_run_preserves_unconditional_occupancy_and_conditional_traits():
    report=run_pilot(draws=2,years=3)
    assert report["status"]==STATUS
    assert report["design"]["independent_ecological_visitor_histories"]==0
    assert report["design"]["prospective_chapter2_cohorts_accessed"] is False
    assert report["design"]["assigned_order_schedule"] is False
    for regime in VISITOR_REGIMES:
        r=report["results"][regime]
        for gate in ("baseline","half_self","half_outcross"):
            k8=r[f"K8_{gate}"]
            k48=r[f"K48_{gate}"]
            assert k8["first_step_expected_direction"]==k48["first_step_expected_direction"]
            for out in (k8,k48):
                assert 0<=out["occupied_count"]<=2
                assert out["n_occupied_genetic_endpoints"]==out["occupied_count"]
                if out["occupied_count"]==0:
                    assert out["end_genetic_mean_conditional_on_occupancy"] is None
                else:
                    assert len(out["end_genetic_mean_conditional_on_occupancy"])==3
                assert len(out["occupied_by_demographic_rep"])==2
        assert (
            r["comparisons"]["K8_minus_K48_half_self"][
                "not_equivalent_to_451_A_minus_I_estimand"
            ] is True
        )


def test_no_visitors_outcross_ablation_is_a_strict_negative_control():
    report=run_pilot(draws=3,years=4)
    r=report["results"]["no_visitors"]
    for k in (8,48):
        a=r[f"K{k}_baseline"]
        b=r[f"K{k}_half_outcross"]
        assert a["occupied_by_demographic_rep"]==b["occupied_by_demographic_rep"]
        assert a["first_step_expected_direction"]==b["first_step_expected_direction"]
        assert a["end_genetic_mean_conditional_on_occupancy"]==b["end_genetic_mean_conditional_on_occupancy"]
        assert a["cumulative_self_recruits_descriptive"]==b["cumulative_self_recruits_descriptive"]
        assert a["cumulative_outcross_recruits_descriptive"]==0
        assert b["cumulative_outcross_recruits_descriptive"]==0
        assert r["comparisons"][f"K{k}_half_outcross"]["baseline_minus_gate_occupancy"]==0


def test_one_path_reproducible_and_keeps_absorbing_extinction():
    state,cfg,visitors=engineering_fixture()
    a=condition_run(
        state,cfg,visitors["two_hand_authored"],
        gate="half_self",draw=1,master=8904103,years=4,
    )
    b=condition_run(
        state,cfg,visitors["two_hand_authored"],
        gate="half_self",draw=1,master=8904103,years=4,
    )
    assert a==b
    assert len(a["census"])==5
    assert len(a["expected_directions_when_occupied"])==4
    assert len(a["realized_directions_when_occupied"])==4
    if a["first_extinction"] is not None:
        assert a["occupied"] is False
        assert a["end_genetic_mean_given_occupied"] is None
        assert all(n==0 for n in a["census"][a["first_extinction"]:])


@pytest.mark.parametrize("draws,years",[(0,4),(1,0),(257,4),(2,81)])
def test_fail_closed_invalid_scope(draws,years):
    with pytest.raises(ValueError,match="restricted engineering pilot"):
        run_pilot(draws=draws,years=years)



def test_nondefault_budget_valid_and_differs_from_stress_fixture():
    state, cfg, visitors=engineering_fixture(ovule_budget=6.0)
    assert cfg.ovule_budget==6.0
    out=run_pilot(draws=1,years=2,ovule_budget=6.0)
    assert out["design"]["ovule_budget"]==6.0
    assert out["design"]["independent_ecological_visitor_histories"]==0


@pytest.mark.parametrize("bad",[-2.0,0,13.0,float("nan"),True])
def test_invalid_budget_not_accepted_in_engineering_grid(bad):
    with pytest.raises(ValueError,match="restricted ovule budget"):
        run_pilot(draws=1,years=2,ovule_budget=bad)
