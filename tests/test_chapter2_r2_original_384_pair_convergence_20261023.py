"""Archive-frozen readback guards; no raw source ZIP is needed in default CI.

The original SHA-verified GitHub Actions artifact can be replayed separately:
  CHAPTER2_R2_384_ORIGINAL_ZIP=/path/to/archive.zip pytest -q ...
CI tests archived compact receipt, original independent review and paired logic,
NOT a fresh unarchived simulation or an independent island sample.
"""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path

import pytest

from scripts.audit_chapter2_r2_original_384_pair_convergence_20261023 import (
    classify_pair, readback, ZIP_SHA, PROTOCOL_SHA, SOURCE_SHA,
)

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "docs/audits/CHAPTER2_R2_ORIGINAL_384_PAIR_CONVERGENCE_20261023.json"
INDEPENDENT = ROOT / "docs/audits/CHAPTER2_BASELINE_POLLEN_384_INDEPENDENT_REVIEW_20261019.json"


def test_compact_receipt_preserves_source_identity_and_nonconfirmation():
    x = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert x["status"] == "PASS_ORIGINAL_384_SHA_VERIFIED_EXACT_PAIR_R2_CONVERGENCE"
    assert x["source_actions_run_id"] == 39233450099
    assert x["source_artifact_id"] == 12178257738
    assert x["source_artifact_zip_sha256"] == ZIP_SHA
    assert x["source_commit"] == SOURCE_SHA
    assert x["protocol_sha256"] == PROTOCOL_SHA
    assert x["n_paths"] == 384 and x["n_paired_futures"] == 192
    assert x["n_independent_founders"] == 12
    assert x["n_demographic_repeats_nested_in_founders"] == 4
    assert x["new_population_updates"] == x["new_statistical_tests"] == 0
    assert x["claim_rank"] == "POST_OUTCOME_DESCRIPTIVE_MODEL_SOURCE_NOT_INDEPENDENT_CONFIRMATION"


def test_original_raw_pairs_establish_exact_cofixation_not_just_lower_bound():
    x = json.loads(RECEIPT.read_text(encoding="utf-8"))
    old = json.loads(INDEPENDENT.read_text(encoding="utf-8"))
    independent = {(z["start_A"], z["baseline"]): z for z in old["pair_contrasts"]}
    assert len(independent) == 4 and len(x["strata"]) == 4
    assert x["total_zero"] == x["total_zero_both_fixed_same_allele"] == 103
    assert x["total_zero_polymorphic_at_shock"] == 69
    assert x["total_zero_with_different_full_terminal_hashes"] == 96
    expected = {
        (0.3, "strong_baseline_limitation"): (45, 23, 42, 23, 0),
        (0.3, "weak_baseline_limitation"): (8, 7, 8, 3, 4),
        (0.5, "strong_baseline_limitation"): (42, 32, 38, 31, 1),
        (0.5, "weak_baseline_limitation"): (8, 7, 8, 1, 6),
    }
    for z in x["strata"]:
        key = z["initial_A"], z["baseline"]
        zero, newfixed, differ, up, down = expected[key]
        old_z = independent[key]
        assert z["n_paired_futures"] == 48
        assert z["n_exact_zero"] == zero
        assert z["n_exact_zero"] == z["n_zero_both_fixed_same_allele"]
        assert z["n_zero_started_polymorphic"] == newfixed
        assert z["n_zero_started_polymorphic_then_both_fixed_same"] == newfixed
        assert z["n_zero_with_different_full_terminal_hashes"] == differ
        assert z["n_postshock_converged_A_up"] == up
        assert z["n_postshock_converged_A_down"] == down
        assert up + down == newfixed
        assert z["n_positive"] + z["n_negative"] + zero == 48
        assert z["n_zero_with_same_A_allele_distribution"] == zero
        assert z["n_zero_with_both_A_arms_changed_from_prefix"] == newfixed
        assert z["n_prefix_A_fixed"] == old_z["prefix_fixed_A_pairs"]
        assert z["n_exact_zero"] == old_z["zero_A_contrast_pairs"]
        assert abs(z["mean_A_decline_minus_control"] - old_z["A_decline_minus_control"]) < 1e-12


def _mock_pair(prefix_alleles=(0.25, 0.5), final_alleles=(0.5,),
               same_terminal_hash=False):
    def state(alleles, mean):
        return {
            "n": 48, "A": mean,
            "genetic_support": {"A": {
                "allele_values": list(alleles),
                "allele_counts": [96 // len(alleles)] * len(alleles),
                "genotype_mean_variance": 0.0 if len(alleles) == 1 else 0.01,
            }},
        }
    first = state(prefix_alleles, sum(prefix_alleles) / len(prefix_alleles))
    last = state(final_alleles, sum(final_alleles) / len(final_alleles))
    common = {
        "start_A": 0.3, "baseline": "strong_baseline_limitation",
        "founder_seed": 810101, "demography_repeat": 1,
        "initial_state_hash": "same-initial", "prefix_state_hash": "same-prefix",
        "t0": {"n": 48}, "t_prefix": first,
        "q_first": .1, "q_pre_last": .2,
        "reproduction_records": [{"year": k} for k in range(30)],
        "updates": 80, "prefix_updates": 30, "alive_at_end": True,
        "t_end": last,
    }
    c, d = copy.deepcopy(common), copy.deepcopy(common)
    c["arm"] = "control"
    d["arm"] = "decline"
    c["terminal_state_hash"] = "genomic-state-one"
    d["terminal_state_hash"] = "genomic-state-one" if same_terminal_hash else "genomic-state-two"
    return c, d


def test_zero_mean_A_contrast_does_not_mean_same_full_population_state():
    c, d = _mock_pair()
    z = classify_pair(c, d)
    assert z["zero"]
    assert not z["prefix_fixed"]
    assert z["same_fixed_A"] and z["same_A_support"]
    assert z["both_futures_A_changed"]
    assert not z["full_terminal_hash_same"]


def test_mean_equality_alone_does_not_force_same_fixed_allele():
    c, d = _mock_pair(final_alleles=(0.25, 0.75))
    z = classify_pair(c, d)
    assert z["zero"] and not z["same_fixed_A"]
    assert z["same_A_support"]
    assert not z["full_terminal_hash_same"]


def test_source_pairing_or_genetic_absorbing_rule_mismatch_is_rejected():
    c, d = _mock_pair()
    d["prefix_state_hash"] = "wrong-prefix"
    with pytest.raises(AssertionError, match="unmatched"):
        classify_pair(c, d)
    c, d = _mock_pair(prefix_alleles=(0.5,), final_alleles=(0.75,))
    with pytest.raises(AssertionError, match="absorbing"):
        classify_pair(c, d)
    c, d = _mock_pair()
    d["updates"] = 79
    with pytest.raises(AssertionError, match="paired living futures"):
        classify_pair(c, d)


def test_wrong_source_zip_is_rejected(tmp_path):
    broken = tmp_path / "fake.zip"
    broken.write_bytes(b"not the source")
    with pytest.raises(AssertionError, match="SHA256"):
        readback(broken)


def test_optional_original_actions_zip_full_recomputation():
    path = os.getenv("CHAPTER2_R2_384_ORIGINAL_ZIP")
    if not path:
        pytest.skip("Original 1.86 MB ZIP is external; supply environment variable to replay")
    assert readback(Path(path)) == json.loads(RECEIPT.read_text(encoding="utf-8"))
