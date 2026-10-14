"""Source-only validation with UNREGISTERED tiny diagnostic histories, not the 64 holdout IDs."""
import json
from dataclasses import replace

import numpy as np
import pytest

from scripts.audit_chapter2_gamma_persist_new_histories import (
    load_contract, base_config, visitors_and_history, run_condition,
    initial_fps, paired_history_summary, _decision,
    FIRST_YEAR_SEED, LAST_YEAR_SEED, STATUS,
)
from scripts.audit_chapter2_beta_gamma_seed_map import state_of_clones, changed_state
from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.chapter2_postzygotic_viability_gate import gate_postzygotic_seed_viability


def test_holdout_contract_fixed_and_unexposed():
    d,sha=load_contract()
    assert len(sha)==64
    assert FIRST_YEAR_SEED==61021001
    assert LAST_YEAR_SEED==61021064
    assert d["conditions"]["n_futures_total"]==1024
    assert d["conditions"]["mutation_rate"]==0
    assert d["conditions"]["initial_census_policy"].startswith("N0=K")
    for K in (8,48):
        cfg=base_config(d,K)
        assert cfg.capacity==K
        assert cfg.survival==0 and cfg.mutation_rate==0
        assert cfg.seed_arrival.supply==0
        assert cfg.years==80
        assert cfg.island_history=="separation"


def test_exact_original_four_visitor_start_and_zero_seed_immigration():
    d,_=load_contract()
    # This seed is outside all frozen new-history IDs.
    h=visitors_and_history(d,990112)
    assert len(h.visitors)==len(h.seed_candidates)==80
    np.testing.assert_array_equal(h.visitors[0].optima,[.15,.35,.55,.75])
    assert all(len(s.ids)==0 for s in h.seed_candidates)
    assert len(h.visitors[0].ids)==4


def test_engineering_biology_is_monomorphic_and_self_gate_accounting():
    d,_=load_contract()
    cfg=base_config(d,8)
    initial=state_of_clones((.2,.35,.65),8)
    shifted=changed_state(initial,1,.05,whole=True)
    h=visitors_and_history(d,990112)
    a=reproduce_kb(shifted,h.visitors[0],cfg,background_denominator_capacity=48)
    b=gate_postzygotic_seed_viability(a,selfed_fraction=.5,outcross_fraction=1.)
    np.testing.assert_array_equal(a.outcross,b.outcross)
    np.testing.assert_array_equal(a.self_raw,b.self_raw)
    np.testing.assert_array_equal(a.self_viable*.5,b.self_viable)


def test_tiny_smoke_reproduces_all_paired_conditions_without_exposing_holdout():
    d,_=load_contract()
    h=visitors_and_history(d,990113)
    rows=[]
    for K in (8,48):
        for assurance in (.35,.65):
            for gate in ("baseline","half_self"):
                for shift in (-.05,.05):
                    rows.append(run_condition(
                        d,history=h,ecological_seed=990113,
                        K=K,assurance=assurance,gate=gate,shift=shift
                    ))
    assert len(rows)==16
    for r in rows:
        assert r["occupied20"] in (0,1)
        assert r["occupied80"] in (0,1)
        assert r["occupied80"]<=r["occupied20"]
        assert r["assigned_A_I_order"] is False
        assert r["evolution_enabled_vs_freeze_test"] is False
        assert r["seed"] not in range(FIRST_YEAR_SEED,LAST_YEAR_SEED+1)
        if r["occupied80"]==0:
            assert r["end_census"]==0
        else:
            assert r["end_census"]<=r["K"]
    s=paired_history_summary(rows,seeds=[990113],d=d)
    assert len(s)==8
    assert all(set(z["horizons"])=={"20","80"} for z in s)
    json.dumps(s,allow_nan=False)


def test_source_FPS_gradient_reconstruction_for_untreated_and_self_halving():
    d,_=load_contract()
    for assurance in (.35,.65):
        for K in (8,48):
            for gate in ("baseline","half_self"):
                v=initial_fps(d,K,assurance,gate)
                assert np.isfinite(v["finite_one_individual_beta_initial"])
                assert np.isfinite(v["collective_gamma_seed_initial"])
                assert np.isclose(
                    v["finite_one_individual_beta_initial"],
                    sum(v["beta_component_FPS"].values()),
                    atol=1e-11,rtol=0,
                )


@pytest.mark.parametrize("d,lo,hi,expected",[
    (.2,.1,.3,"resolved_positive"),
    (-.2,-.3,-.1,"resolved_negative"),
    (0.,-.01,.01,"practically_equivalent"),
    (0.,-.2,.2,"inconclusive"),
    (.05,0,.2,"inconclusive"),
])
def test_no_post_outcome_selection_rule(d,lo,hi,expected):
    assert _decision(d,lo,hi,.05)==expected
