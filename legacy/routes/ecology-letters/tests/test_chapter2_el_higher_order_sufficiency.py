from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from scripts import audit_chapter2_el_higher_order_sufficiency as audit


ROOT = Path(__file__).resolve().parents[1]
HIGHER_FREEZE = ROOT / "data/design/chapter2_el_higher_order_sufficiency_freeze_20260913.json"
FEEDBACK_FREEZE = ROOT / "data/design/chapter2_el_mixed_feedback_validation_freeze_20260913.json"
RESULT = ROOT / "data/results/chapter2_el_higher_order_sufficiency_20260913.json"


def test_equal_keff_fixes_variance_but_not_higher_cumulants() -> None:
    for k_eff, ks in ((2.0, (2, 4, 8, 16)), (4.0, (4, 8, 16, 32))):
        variance = []
        kappa3 = []
        kappa4 = []
        for k in ks:
            rho = audit.rho_for_keff(k, k_eff)
            variance.append(audit.variance_factor(k, rho))
            kappa3.append(audit.cumulant_factor(3, k, rho))
            kappa4.append(audit.cumulant_factor(4, k, rho))
        assert variance == pytest.approx([1.0 / k_eff] * len(ks), rel=1e-14, abs=1e-14)
        assert max(kappa3) - min(kappa3) > 1e-3
        assert max(kappa4) - min(kappa4) > 1e-3


def test_quadratic_extension_identifies_curvature_alignment_condition() -> None:
    assert audit.symmetric_ratio_derivative_sign(b=1.0, c=1.0, d=2.0, e=2.0) == 0.0
    assert audit.symmetric_ratio_derivative_sign(b=1.0, c=1.0, d=1.0, e=2.0) > 0.0

    low = audit.quadratic_components(
        var_x=1.0, tau=0.5, mu3=0.0, kappa4=-0.10,
        b=1.0, c=1.0, d=1.0, e=2.0,
    )
    high = audit.quadratic_components(
        var_x=1.0, tau=0.5, mu3=0.0, kappa4=0.10,
        b=1.0, c=1.0, d=1.0, e=2.0,
    )
    assert high["I_over_C"] > low["I_over_C"]


def test_holling_fourth_order_predictor_was_frozen_and_falsified() -> None:
    freeze = json.loads(HIGHER_FREEZE.read_text(encoding="utf-8"))
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert freeze["status"] == "fixed_before_setting_level_predictor_read"
    assert freeze["decision_rules"]["no_retuning_after_setting_level_read"] is True

    handling = result["prespecified_handling_only_prediction"]
    assert handling["decision"] == "not_supported"
    assert handling["matched_h4_minus_h1"] == {
        "blocks": 18,
        "positive": 0,
        "zero": 16,
        "negative": 2,
        "mean_difference": -0.5,
        "median_difference": 0.0,
    }
    assert handling["by_handling"]["1.0"]["sum_seed_flips"] == 41
    assert handling["by_handling"]["2.0"]["sum_seed_flips"] == 38
    assert handling["by_handling"]["4.0"]["sum_seed_flips"] == 32


def test_fresh_feedback_prediction_was_frozen_before_unused_seeds_and_supported() -> None:
    freeze = json.loads(FEEDBACK_FREEZE.read_text(encoding="utf-8"))
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert freeze["status"] == "fixed_before_fresh_seed_execution"
    assert freeze["retuning_after_result"] is False
    assert result["retuning_after_fresh_result"] is False

    primary = result["fresh_mixed_feedback_validation"]["primary"]
    assert primary == {
        "alpha_0_flip_count": 0,
        "alpha_0_15_flip_count": 52,
        "positive_pairs": 52,
        "zero_pairs": 56,
        "negative_pairs": 0,
        "sum_paired_difference": 52,
        "decision": "supported",
    }

    medians = result["fresh_mixed_feedback_validation"]["secondary"]["component_medians"]
    alpha0_k1 = next(row for row in medians if row["alpha"] == 0.0 and row["k"] == 1)
    alpha015_k1 = next(row for row in medians if row["alpha"] == 0.15 and row["k"] == 1)
    alpha015_k4 = next(row for row in medians if row["alpha"] == 0.15 and row["k"] == 4)
    assert alpha0_k1["C_gt_I_count"] == 0
    assert alpha0_k1["I_gt_C_count"] == 108
    assert alpha015_k1["C_gt_I_count"] == 52
    assert alpha015_k4["I_gt_C_count"] == 108


def test_full_audit_regenerates_frozen_decisions_on_canonical_python() -> None:
    if sys.version_info[:2] != (3, 11):
        pytest.skip("full stochastic regeneration is pinned to the canonical Python 3.11 CI lane")

    rebuilt = audit.build()
    frozen = json.loads(RESULT.read_text(encoding="utf-8"))

    assert rebuilt["analytic"]["decision"] == frozen["analytic"]["decision"] == "pass"
    assert rebuilt["prespecified_handling_only_prediction"]["matched_h4_minus_h1"] == frozen[
        "prespecified_handling_only_prediction"
    ]["matched_h4_minus_h1"]
    assert rebuilt["prespecified_handling_only_prediction"]["decision"] == "not_supported"
    assert rebuilt["fresh_mixed_feedback_validation"]["primary"] == frozen[
        "fresh_mixed_feedback_validation"
    ]["primary"]
