"""Frozen post-discovery pollen sufficiency feasibility guards."""
import json
from pathlib import Path

import numpy as np
import pytest

from scripts.audit_chapter2_near_pollen_sufficiency_feasibility import (
    DESIGN, load_contract, run_all,
)


def test_source_contract_separates_snapshot_from_evolved_state():
    d=load_contract()
    assert d["source_history_first"]==76001
    assert d["source_history_last"]==76064
    assert d["visitor_snapshot"]==400
    assert d["pollen_budget_multipliers"]==[1,2,4,8,16]
    assert d["status"]=="POST_DISCOVERY_DIAGNOSTIC_NO_EVOLUTIONARY_CONCLUSIONS"


@pytest.fixture(scope="module")
def report():
    return run_all()


def test_all_640_source_rows_and_original_near_far_replay(report):
    assert report["n_rows"]==640
    assert report["n_source_history_blocks"]==64
    assert report["n_independent_new_histories"]==0
    assert len(report["summary_rows"])==10
    assert all(v["n_histories"]==64 for v in report["summary_rows"])
    for arm, original in (("near",.39014861544866286),
                           ("far",.4948351849471593)):
        s=next(v for v in report["summary_rows"]
            if v["arm"]==arm and v["multiplier"]==1)
        np.testing.assert_allclose(s["mean_raw_deficit"],original,
            rtol=0,atol=1e-10)
        np.testing.assert_allclose(s["mean_outcross_fraction"],
            1-2*original,rtol=0,atol=1e-10)


def test_sufficiency_admission_rules_are_strict(report):
    eligible=[v["multiplier"] for v in report["summary_rows"]
        if v["arm"]=="near" and v["mean_outcross_fraction"]>=.9
        and v["n_outcross_ge_0p90"]>=60]
    assert report["candidate_multiplier"]==(
        min(eligible) if eligible else None)
    assert report["status"]==(
        "SUFFICIENCY_FEASIBLE_FOR_EVOLUTIONARY_DESIGN" if eligible
        else "SUFFICIENCY_NOT_REACHED_IN_FROZEN_FEASIBILITY_GRID")
    for r in report["rows"]:
        assert 0<=r["outcross_ovule_fraction"]<=1
        np.testing.assert_allclose(
            r["outcross_ovule_fraction"],
            1-2*r["raw_deficit_after_selfing"],atol=1e-11,rtol=0)


def test_manuscript_is_finite_horizon_and_nonstationarity_is_not_transferred():
    t=(Path(__file__).resolve().parents[1]/
      "docs/CHAPTER2_MANUSCRIPT_ECOLOGY_LETTERS_20261006.md").read_text()
    for marker in (
        "0.3901", "0.4948", "0.2197", "0.0103",
        "cost-free delayed", "assurance-cost setting is more discriminating",
        "finite-horizon response", "not a rerun of the four-setting",
    ):
        assert marker.lower() in t.lower(),marker
    assert "where pollination remains effective" not in t.lower()
