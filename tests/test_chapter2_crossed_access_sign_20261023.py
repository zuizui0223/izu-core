"""Source-grounded tests of the post-outcome crossed source sign reversal.

The original 32 sealed records were admitted offline against frozen original
SUMMARY160 and archive SHA. Routine CI checks the compact result and the
reusable analysis methods; it does NOT claim re-download of the large archive.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from scripts.audit_chapter2_crossed_access_sign_20261023 import (
    F, V, ORIGINAL_ACTIONS_ARTIFACT_SHA256, RUN_ID, STATUS, SUMMARY_SHA256,
    crossed_bootstrap, derive, ph_summary,
)

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "docs/audits/CHAPTER2_CROSSED_ACCESS_SIGN_REVERSAL_20261023.json"
REGISTERED = ROOT / "docs/audits/CHAPTER2_CONFIRM160_COMPACT_RESULTS_20261019.json"


def receipt():
    return json.loads(RECEIPT.read_text(encoding="utf8"))


def test_original_source_identity_and_no_new_confirmation():
    x = receipt()
    source = json.loads(REGISTERED.read_text(encoding="utf8"))
    p = x["original_provenance"]
    assert x["status"] == STATUS
    assert p["original_summary_sha256"] == SUMMARY_SHA256
    assert p["original_actions_artifact_sha256"] == ORIGINAL_ACTIONS_ARTIFACT_SHA256
    assert p["source_run"] == RUN_ID == 39193074847
    assert p["source_artifact_id"] == 12161199381
    assert p["sealed_source_shards"] == 32
    assert p["original_cell_count"] == F*V == 25600
    assert p["complete_arm_totals"] == source["arms"]
    assert x["new_biological_simulations"] == 0
    assert x["new_preregistered_endpoints"] == 0
    assert not x["new_confirmatory_test"]
    assert x["source_bound_post_outcome"]
    assert x["source_marginal_signs_not_independent_sign_tests"]
    assert not x["independent_biological_reimplementation"]


def test_marginal_contrasts_and_original_registered_variance():
    x = receipt()["pointwise"]
    main = json.loads(REGISTERED.read_text(encoding="utf8"))
    registered_g = next(y for y in main["primary"]["endpoints"]
                        if y["name"] == "genetic_loss")
    assert x["B8"]["estimate_pp"] == -100*registered_g["estimate"]
    assert x["B8"]["pigeonhole_conditional_variance"] == pytest.approx(
        registered_g["variance"], abs=2e-17)
    assert x["B4p5"]["estimate_pp"] == 35.56640625
    assert x["interaction"]["estimate_pp"] == 43.89453125
    assert x["B4p5"]["estimate_pp"] - x["B8"]["estimate_pp"] == x["interaction"]["estimate_pp"]
    for budget in ("B8", "B4p5", "interaction"):
        r = x[budget]
        assert r["nominal_97p5_t_interval_pp"][0] < r["estimate_pp"] < r["nominal_97p5_t_interval_pp"][1]
        assert sum(r["founder_marginal_signs"].values()) == 160
        assert sum(r["visitor_marginal_signs"].values()) == 160
        assert sum(r["paired_cell_effect_counts"].values()) == 25600
    assert x["B8"]["founder_marginal_signs"] == {"positive":7,"zero":2,"negative":151}
    assert x["B8"]["visitor_marginal_signs"] == {"positive":9,"zero":4,"negative":147}
    for budget in ("B4p5","interaction"):
        assert x[budget]["founder_marginal_signs"] == {
            "positive":160,"zero":0,"negative":0}
        assert x[budget]["visitor_marginal_signs"] == {
            "positive":160,"zero":0,"negative":0}


def test_paired_source_cell_budget_sign_reversals_and_no_cherry_picked_arms():
    report = receipt()
    d = report["paired_budget_effects"]
    assert sum(d.values()) == 25_600
    assert set(d) == {f"{a}_{b}" for a in (-1,0,1) for b in (-1,0,1)}
    assert d["-1_1"] == 995 and d["1_-1"] == 6
    for b in ("B8","B4p5","interaction"):
        r = report["pointwise"][b]
        # Read-only source-weighted crossed bootstrap; post-outcome sensitivity.
        bootstrap = report["crossed_bootstrap"][b]
        assert bootstrap["crossed_resamples"] == 10_000
        assert bootstrap["seed"] == 20261023
        assert bootstrap["interval_is_exploratory_post_outcome"]
        assert bootstrap["percentile95_pp"][0] < r["estimate_pp"] < bootstrap["percentile95_pp"][1]
    assert report["pointwise"]["interaction"]["paired_cell_effect_counts"]["2"] == 995
    assert report["pointwise"]["interaction"]["paired_cell_effect_counts"]["-2"] == 6


def test_pigeonhole_two_way_formula_matches_additive_and_interaction_examples():
    matrix = np.zeros((F, V), dtype=float)
    matrix[:F//2,:] = 1.
    result = ph_summary(matrix)
    assert result["estimate_pp"] == 50.
    assert result["pigeonhole_conditional_variance"] == pytest.approx(
        40./(F*F), abs=1e-15)
    assert result["founder_marginal_signs"] == {"positive":80,"zero":80,"negative":0}
    matrix = np.outer(np.tile([1.,-1.], F//2), np.tile([1.,-1.], V//2))
    out = ph_summary(matrix)
    assert out["estimate_pp"] == pytest.approx(0.)
    assert out["pigeonhole_conditional_variance"] == pytest.approx(
        1/(F*V), abs=1e-15)


def test_bootstrap_uses_paired_source_axis_resampling_reproducibly():
    a = np.zeros((F,V), dtype=float)
    a[:60,:] = 1
    d = {"a": a, "twice": a*2}
    x = crossed_bootstrap(d, draws=100, seed=20261023)
    y = crossed_bootstrap(d, draws=100, seed=20261023)
    assert x == y
    assert x["twice"]["percentile95_pp"] == pytest.approx(
        [2*v for v in x["a"]["percentile95_pp"]], abs=1e-10)
    with pytest.raises(ValueError):
        crossed_bootstrap(d, draws=9)


def test_accepts_source_indicators_not_claims_of_general_reversibility():
    note=(ROOT/"docs/CHAPTER2_CROSSED_ACCESS_SIGN_REVERSAL_20261023.md").read_text(encoding="utf8")
    for phrase in ("post-outcome descriptive", "995/25,600", "6/25,600",
                   "no I mutation or immigration", "not", "t159",
                   "not a third registered endpoint"):
        assert phrase.lower() in note.lower()
    assert "source run" in note.lower() or "Actions #39193074847" in note
