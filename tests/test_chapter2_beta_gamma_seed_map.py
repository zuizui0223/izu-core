"""Exact-source synthetic beta/Gamma(seed) audit; no prospective biology runs."""
import json

import numpy as np
import pytest

from scripts.audit_chapter2_beta_gamma_seed_map import (
    STATUS, audit, classify, ledger_stats, load_contract,
    local_slopes, state_of_clones, visitors_for,
)
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config, load_design,
)
from dataclasses import replace


def test_finite_F_P_S_identity_and_zero_visitor_negative_control():
    d,_=load_contract()
    conf=replace(source_config(load_design(DEFAULT_DESIGN),
                 "delayed_control",0.0,"evolving"),capacity=8)
    for condition in ("none","matched4"):
        visitors=visitors_for(condition,d)
        state=state_of_clones((.2,.35,.65),8)
        ref=ledger_stats(state,visitors,conf,48)
        np.testing.assert_allclose(ref["F"].sum(),ref["P"].sum(),rtol=0,atol=1e-12)
        np.testing.assert_allclose(ref["W"].sum(),ref["total"],rtol=0,atol=1e-12)
        for trait in (1,2):
            slopes=local_slopes(state,visitors,conf,trait,.005)
            np.testing.assert_allclose(
                sum(slopes["beta_components"].values()),
                slopes["beta_one_individual"],atol=1e-11,rtol=0)
            assert np.isfinite(slopes["gamma_group_seed"])
            if condition=="none":
                assert ref["total_outcross"]==0
                assert slopes["beta_components"]["maternal_outcross_F"]==0
                assert slopes["beta_components"]["paternal_outcross_P"]==0


def test_complete_grid_is_not_survival_or_prospectively_confirmatory():
    data=audit()
    assert data["status"]==STATUS
    assert data["n_rows"]==384
    assert data["independent_visitor_histories"]==0
    assert sum(data["full_grid_class_counts"].values())==384
    assert all(r["B"]==48 for r in data["rows"])
    assert set(r["K"] for r in data["rows"])=={8,48}
    assert set(r["trait"] for r in data["rows"])=={"investment","assurance"}
    assert set(r["classification"] for r in data["rows"]) <= {
        "aligned","individual_advantage_group_harm",
        "individual_disadvantage_group_benefit","inconclusive"}
    for r in data["rows"]:
        np.testing.assert_allclose(
            r["beta_F"]+r["beta_P"]+r["beta_S"],
            r["beta_one_individual"],atol=1e-11,rtol=0)
    for row in (r for r in data["rows"] if r["visitor_regime"]=="none"):
        assert row["no_visitor_strict_outcross_zero"] is True
        assert row["beta_F"]==0.
        assert row["beta_P"]==0.
    json.dumps(data,allow_nan=False)


def test_deadband_is_not_assigned_to_alignment_or_discordance():
    assert classify(.005,-.8,.005,-.8,.02)[0]=="inconclusive"
    assert classify(.2,.2,-.2,.2,.02)[0]=="inconclusive"
    assert classify(.2,-.2,.2,-.2,.02)[0]=="individual_advantage_group_harm"
    assert classify(-.2,.2,-.2,.2,.02)[0]=="individual_disadvantage_group_benefit"
    assert classify(-.2,-.2,-.2,-.2,.02)[0]=="aligned"


@pytest.mark.parametrize("n", [0,7,49])
def test_refuse_outside_finite_capacity_contract(n):
    with pytest.raises(ValueError):
        state_of_clones((.2,.5,.5),n)


def test_contract_lock_rejects_modified_beta_gamma_grid(tmp_path):
    d,_=load_contract()
    d["central_difference_steps"]=[.1,.05]
    p=tmp_path/"altered.json"
    p.write_text(json.dumps(d),encoding="utf-8")
    with pytest.raises(ValueError,match="engineering source contract"):
        load_contract(p)
