"""Source-bound exploratory A/I dissociation in the original 384 Model3 paths."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path

import pytest

from scripts.audit_chapter2_r2_cross_locus_outcomes_20261023 import (
    classify_cross_locus, analyze, OUTCOME, ZIP_SHA, PROTOCOL_SHA
)

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "docs/audits/CHAPTER2_R2_CROSS_LOCUS_ORIGINAL_384_20261023.json"
PARENT = ROOT / "docs/audits/CHAPTER2_R2_ORIGINAL_384_PAIR_CONVERGENCE_20261023.json"


def test_source_bound_receipt_is_descriptive_and_reconciles_parent():
    x = json.loads(RECEIPT.read_text())
    p = json.loads(PARENT.read_text())
    assert x["status"] == OUTCOME
    assert x["source_zip_sha256"] == ZIP_SHA == p["source_artifact_zip_sha256"]
    assert x["protocol_sha256"] == PROTOCOL_SHA == p["protocol_sha256"]
    assert x["source_commit"] == p["source_commit"]
    assert x["n_independent_founders"] == p["n_independent_founders"] == 12
    assert x["n_original_paths"] == p["n_paths"] == 384
    assert x["n_original_paired_futures"] == p["n_paired_futures"] == 192
    assert x["n_A_zero_pairs"] == p["total_zero"] == 103
    assert x["n_A_nonzero_pairs"] == 89
    assert x["new_population_updates"] == x["new_statistical_tests"] == 0
    assert x["evidence_grade"] == "POST_OUTCOME_SOURCE_DESCRIPTIVE_NO_NEW_EVOLUTION"


def test_each_old_A_cofixed_stratum_retains_independent_I_responses():
    x = json.loads(RECEIPT.read_text())
    p = json.loads(PARENT.read_text())
    old = {(r["initial_A"], r["baseline"]): r for r in p["strata"]}
    assert len(x["strata"]) == len(old) == 4
    for r in x["strata"]:
        key = r["initial_A"], r["baseline"]
        assert r["n_matched_futures"] == 48
        assert r["n_A_treatment_contrast_exact_zero"] == old[key]["n_exact_zero"]
        assert r["n_A_zero_but_I_allele_support_differs"] == (
            r["n_A_zero_but_I_negative"] + r["n_A_zero_but_I_positive"]
        )
        assert sum([r["n_A_zero_but_I_negative"], r["n_A_zero_but_I_exact_zero"],
                    r["n_A_zero_but_I_positive"]]) == r["n_A_treatment_contrast_exact_zero"]
        assert r["n_A_treatment_contrast_nonzero"] == 48-r["n_A_treatment_contrast_exact_zero"]
        assert r["n_A_prefix_polymorphic_then_A_zero_and_I_nonzero"] <= (
            old[key]["n_zero_started_polymorphic"]
        )
        assert sum(r["A_nonzero_terminal_fixation_phases"].values()) == (
            r["n_A_treatment_contrast_nonzero"]
        )
    total = x["totals"]
    assert total == {
        "A_zero_I_nonzero": 54,
        "A_zero_I_allele_support_differs": 54,
        "A_zero_I_zero": 49,
        "A_prefix_polymorphic_A_zero_I_nonzero": 36,
        "A_fixed_at_shock_A_zero_I_nonzero": 18,
        "A_and_M_fixed_I_polymorphic_at_shock_I_nonzero": 14,
        "strict_A_M_frozen_I_negative": 13,
        "strict_A_M_frozen_I_positive": 1,
        "A_nonzero_both_fixed_to_distinct_values": 1,
        "A_nonzero_only_one_future_fixed": 44,
        "A_nonzero_both_futures_polymorphic": 44,
    }
    assert total["A_zero_I_nonzero"] + total["A_zero_I_zero"] == 103
    assert (total["A_prefix_polymorphic_A_zero_I_nonzero"]
            + total["A_fixed_at_shock_A_zero_I_nonzero"]) == 54
    assert total["A_and_M_fixed_I_polymorphic_at_shock_I_nonzero"] == (
        total["strict_A_M_frozen_I_negative"] + total["strict_A_M_frozen_I_positive"]
    ) == 14
    strict = {
        (0.3, "strong_baseline_limitation"): (12, 10, 10, 0),
        (0.3, "weak_baseline_limitation"): (1, 1, 1, 0),
        (0.5, "strong_baseline_limitation"): (4, 2, 2, 0),
        (0.5, "weak_baseline_limitation"): (1, 1, 0, 1),
    }
    for row in x["strata"]:
        expected = strict[(row["initial_A"], row["baseline"])]
        assert (
            row["n_A_already_fixed_at_shock_but_I_nonzero"],
            row["n_A_M_already_fixed_I_polymorphic_at_shock_but_I_nonzero"],
            row["strict_A_M_frozen_I_negative"],
            row["strict_A_M_frozen_I_positive"],
        ) == expected
    assert (total["A_nonzero_both_fixed_to_distinct_values"]
            + total["A_nonzero_only_one_future_fixed"]
            + total["A_nonzero_both_futures_polymorphic"]) == 89


def _fake_state(A, I):
    def locus(z):
        vals = list(z)
        return {
            "allele_values": vals,
            "allele_counts": [96//len(vals)] * len(vals),
            "genotype_mean_variance": 0.0 if len(vals) == 1 else 0.012,
        }
    return {"A": sum(A)/len(A), "I": sum(I)/len(I), "M": .5, "n": 48,
            "genetic_support": {"A": locus(A), "I": locus(I), "M": locus((.5,))}}


def _fake_pair(cA=(.75,),dA=(.75,),cI=(.5,),dI=(.25,)):
    shared = {
        "start_A": .3, "baseline": "strong_baseline_limitation",
        "founder_seed": 810101, "demography_repeat": 1,
        "initial_state_hash": "shared_initial", "prefix_state_hash": "shared_prefix",
        "t0": {"n": 48}, "t_prefix": _fake_state((.5,.75),(.25,.5)),
        "q_first": .1, "q_pre_last": .12,
        "reproduction_records": [{"year": i} for i in range(30)],
        "updates": 80, "prefix_updates": 30, "alive_at_end": True,
    }
    c=copy.deepcopy(shared);d=copy.deepcopy(shared)
    c.update(arm="control",t_end=_fake_state(cA,cI),terminal_state_hash="c")
    d.update(arm="decline",t_end=_fake_state(dA,dI),terminal_state_hash="d")
    return c,d


def test_A_convergence_can_coexist_with_I_allele_and_mean_difference():
    c,d=_fake_pair()
    r=classify_cross_locus(c,d)
    assert r["A_zero"] and r["A_prefix_polymorphic"]
    assert r["A_terminal_stage"] == "both_fixed_same_A_value"
    assert r["I_diff"] == pytest.approx(-.25)
    assert r["I_support_different"] and r["I_negative"]
    assert not r["A_fixed_at_shock"]
    assert r["M_fixed_at_shock"]


def test_strict_native_fixed_A_and_M_does_not_prevent_I_difference():
    c, d = _fake_pair()
    for row in (c, d):
        row["t_prefix"] = _fake_state((.75,), (.25, .5))
        row["t_prefix"]["genetic_support"]["M"] = {
            "allele_values": [.5], "allele_counts": [96], "genotype_mean_variance": 0.0
        }
        row["t_prefix"]["M"] = .5
    r = classify_cross_locus(c, d)
    assert r["A_zero"] and r["A_fixed_at_shock"] and r["M_fixed_at_shock"]
    assert r["I_polymorphic_at_shock"] and r["I_negative"]
    assert r["M_same_numeric_endpoint"]
    d["t_end"]["genetic_support"]["M"]["allele_values"] = [.75]
    with pytest.raises(AssertionError, match="M numeric fixation"):
        classify_cross_locus(c, d)


def test_mean_A_same_does_not_imply_identical_A_support():
    c,d=_fake_pair(cA=(.5,),dA=(.25,.75))
    with pytest.raises(AssertionError,match="without joint same-A fixation"):
        classify_cross_locus(c,d)


def test_nonzero_A_endpoint_can_mean_unfinished_fixation_not_distinct_fixed_alleles():
    c,d=_fake_pair(cA=(.5,.75),dA=(.75,))
    r=classify_cross_locus(c,d)
    assert not r["A_zero"]
    assert r["A_terminal_stage"] == "only_decline_fixed"
    c,d=_fake_pair(cA=(.5,),dA=(.75,))
    r=classify_cross_locus(c,d)
    assert not r["A_zero"]
    assert r["A_terminal_stage"] == "both_fixed_to_distinct_values"


def test_wrong_I_support_is_fail_closed():
    c,d=_fake_pair()
    d["t_end"]["genetic_support"]["I"]["allele_counts"]=[95]
    with pytest.raises(AssertionError,match="terminal I allele support"):
        classify_cross_locus(c,d)


def test_optional_original_ZIP_replay_matches_exact_compact_receipt():
    source=os.getenv("CHAPTER2_R2_384_ORIGINAL_ZIP")
    if source is None:
        pytest.skip("Original immutable 1.86 MB Actions artifact is external")
    assert analyze(Path(source)) == json.loads(RECEIPT.read_text())
