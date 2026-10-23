"""Original-source fixed A/M and segregating-I subcohort, not prospective science."""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from scripts.audit_chapter2_r2_shock_frozen_AM_I_sorting_20261023 import (
    STATUS, EXPECTED, audit
)
from scripts.audit_chapter2_r2_original_384_pair_convergence_20261023 import (
    ZIP_SHA, SOURCE_SHA, PROTOCOL_SHA
)

ROOT=Path(__file__).resolve().parents[1]
RECEIPT=ROOT/"docs/audits/CHAPTER2_R2_FROZEN_AM_I_SORTING_20261023.json"
PARENT=ROOT/"docs/audits/CHAPTER2_R2_CROSS_LOCUS_ORIGINAL_384_20261023.json"


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_original_provenance_and_exploratory_scope_frozen():
    r=_load(RECEIPT)
    assert r["status"]==STATUS
    assert r["source_zip_sha256"]==ZIP_SHA
    assert r["source_sha"]==SOURCE_SHA
    assert r["source_protocol_sha256"]==PROTOCOL_SHA
    assert r["source_actions_run_id"]==39233450099
    assert r["independent_founders_in_original_study"]==12
    assert r["n_original_paths"]==384 and r["n_original_pairs"]==192
    assert r["new_biological_population_updates"]==r["new_statistical_tests"]==0
    assert r["claim_rank"]=="RETROSPECTIVE_SOURCE_MODEL_NEGATIVE_CONTROL_ONLY"
    assert "not independently randomized" in r["causal_boundary"]


def test_fixed_genetic_A_M_and_initially_polymorphic_I_exact_strata():
    r=_load(RECEIPT);parent=_load(PARENT)
    p={(x["initial_A"],x["baseline"]):x for x in parent["strata"]}
    assert len(r["strata"])==len(EXPECTED)==4
    for row in r["strata"]:
        key=row["initial_A"],row["baseline"]
        expected=EXPECTED[key]
        n,n_cf,n_df,n_neg,n_pos,n_same,n_polydfix,n_diff,mean=expected
        assert row["n_pairs"]==n
        assert row["I_fixed_at_end_control"]==n_cf
        assert row["I_fixed_at_end_decline"]==n_df
        assert row["I_treatment_negative"]==n_neg
        assert row["I_treatment_positive"]==n_pos
        assert row["I_treatment_zero"]==n-n_neg-n_pos
        assert row["I_both_fixed_same"]==n_same
        assert row["I_control_polymorphic_decline_fixed"]==n_polydfix
        assert row["I_both_fixed_different"]==n_diff
        assert row["I_both_fixed_same"]+row["I_control_polymorphic_decline_fixed"]+row[
            "I_both_fixed_different"]+row["I_both_polymorphic"]==n
        assert row["mean_signed_I_treatment_contrast"]==pytest.approx(mean,abs=1e-12)
        assert 0 <= row["I_decreased_from_shock_control"] <= n
        assert 0 <= row["I_decreased_from_shock_decline"] <= n
        assert 0 <= row["mean_first_future_q_decline"] < row["mean_first_future_q_control"] <= 1
        assert row["n_pairs"] <= p[key]["n_A_treatment_contrast_exact_zero"]
        assert row["n_pairs"] <= p[key]["n_A_zero_but_I_negative"] + p[key]["n_A_zero_but_I_exact_zero"] + p[key]["n_A_zero_but_I_positive"]
    assert sum(z["n_pairs"] for z in r["strata"])==24


def test_strong_baseline_I_fixation_contrast_and_founder_nesting():
    r=_load(RECEIPT);t=r["totals"];p=_load(PARENT)
    assert t["all_strict_pairs"]==24
    assert t["all_strict_distinct_founders"]==11
    assert t["strong_pairs"]==22 and t["weak_pairs"]==2
    assert t["strong_distinct_founders"]==11
    assert t["strong_I_fixed_control"]==13
    assert t["strong_I_fixed_decline"]==22
    assert (t["strong_I_treatment_negative"],t["strong_I_treatment_zero"],
            t["strong_I_treatment_positive"])==(12,10,0)
    assert t["strong_I_decrease_from_shock_control"]==11
    assert t["strong_I_decrease_from_shock_decline"]==20
    assert t["strong_founder_mean_I_difference_negative"]==9
    assert t["strong_founder_mean_I_difference_zero"]==2
    assert t["strong_founder_mean_I_difference_positive"]==0
    assert t["strong_mean_I_contrast"]==pytest.approx(-0.08913352272727272,abs=1e-12)
    assert t["strong_q_control"]==pytest.approx(.13920994216147997,abs=1e-12)
    assert t["strong_q_decline"]==pytest.approx(.01689527391924731,abs=1e-12)
    assert 12 + 2 == p["totals"]["A_and_M_fixed_I_polymorphic_at_shock_I_nonzero"]
    assert 12 + 1 == p["totals"]["strict_A_M_frozen_I_negative"]
    assert 1 == p["totals"]["strict_A_M_frozen_I_positive"]


def test_optional_exact_original_actions_archive_replay_with_tolerant_floats():
    path=os.environ.get("CHAPTER2_R2_384_ORIGINAL_ZIP")
    if not path:
        pytest.skip("Original Actions ZIP external. Use environment variable for full source replay.")
    current=audit(Path(path))
    saved=_load(RECEIPT)
    def equal_rec(a,b):
        if isinstance(a,dict):
            assert isinstance(b,dict) and a.keys()==b.keys()
            for key in a: equal_rec(a[key],b[key])
        elif isinstance(a,list):
            assert isinstance(b,list) and len(a)==len(b)
            for x,y in zip(a,b): equal_rec(x,y)
        elif isinstance(a,float):
            assert a==pytest.approx(b,rel=0,abs=1e-12)
        else:
            assert a==b
    equal_rec(current,saved)
