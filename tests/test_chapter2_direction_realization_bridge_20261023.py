"""Read-only regression tests for R1–R5 payoff/finite-response boundary.

No population steps, newly fitted hypotheses, or changes to registered biology.
"""
import json
import scripts.audit_chapter2_direction_realization_bridge_20261023 as bridge

import pytest

from scripts.audit_chapter2_direction_realization_bridge_20261023 import (
    crossed_competing_event_identity,
    read_only_audit,
    source_no_visitor_payoff,
    transfer_source_signs,
)


@pytest.mark.parametrize("timing", ["delayed", "prior"])
@pytest.mark.parametrize("mode", ["fixed", "evolving"])
def test_no_visitor_payoff_decreases_with_floral_investment(timing, mode):
    result = source_no_visitor_payoff(timing=timing, mode=mode)
    assert result["log_relative_fitness_high_minus_low_I"] == pytest.approx(-0.16, abs=1e-12)
    assert result["source_gradient_at_I_0p5"] == pytest.approx(-0.4, abs=1e-12)


def test_strict_source_comparison_rejects_invalid_assumptions():
    with pytest.raises(ValueError):
        source_no_visitor_payoff(timing="invalid", mode="fixed")
    with pytest.raises(ValueError):
        source_no_visitor_payoff(timing="delayed", mode="fixed", investment_cost=0)


def test_R5_archived_no_visitor_signs_stay_distinct_from_selection():
    d = transfer_source_signs()
    assert d["fixed"]["positive_I_exact_signs"] == 27
    assert d["evolving"]["positive_I_exact_signs"] == 29
    assert d["fixed"]["occupied_futures"] == 704
    assert d["evolving"]["occupied_futures"] == 1024
    assert d["fixed"]["cohorts"] == d["evolving"]["cohorts"] == 32
    assert d["fixed"]["not_an_independent_founder_count"]
    assert d["fixed"]["signs_do_not_establish_biologically_large_changes"]


def test_R4_original_sealed_competing_event_partition():
    r = crossed_competing_event_identity()
    assert r["B8"]["first_genetic_loss_diff_count"] == 2132
    assert r["B8"]["first_extinction_diff_count"] == 0
    assert r["B8"]["alive_with_I_support_diff_pp"] == -8.328125
    assert r["B4p5"]["first_genetic_loss_diff_count"] == 3122
    assert r["B4p5"]["first_extinction_diff_count"] == -12227
    assert r["B4p5"]["alive_with_I_support_diff_pp"] == 35.56640625
    assert r["B8"]["post_outcome_not_registered"]
    assert r["B4p5"]["post_outcome_not_registered"]


def test_cannot_promote_exploratory_bridge_to_new_biology():
    report = read_only_audit()
    assert report["new_biological_simulations"] == 0
    assert report["new_preregistered_endpoints"] == 0
    assert len(report["source_payoffs"]) == 4
    assert report["status"] == "EXPLORATORY_READ_ONLY_NO_NEW_BIOLOGY"


def test_original_R1_R2_and_exploratory_pollen_baseline_are_distinct():
    x = bridge.original_R1_R2_readback()
    rows = x["original_registered_four_setting"]
    assert len(rows) == 4
    assert {r["setting"] for r in rows} == {
        "delayed_control", "prior_selfing", "pollen_discount", "assurance_cost"
    }
    assert all(r["fixed_A_far_I_change_from_founder"] < 0 for r in rows)
    assert all(r["A_evolution_attenuation_near_far"] > 0 for r in rows)
    assert x["independent_fresh_founder_four_setting_overall"] == "INCONCLUSIVE"
    assert len(x["exploratory_384_baseline_regime_sign_reversal"]) == 2
    for row in x["exploratory_384_baseline_regime_sign_reversal"]:
        assert row["strong_baseline_I_decline_minus_control"] < 0
        assert row["weak_baseline_I_decline_minus_control"] > 0
        assert row["absolute_pollen_delivery_was_not_matched"]


def test_R3_existing_heldout_skill_is_not_stochastic_variance_fraction():
    x = bridge.R3_known_source_predictability_readback()
    d = x["known_source_prediction_not_unseen_founders"]
    assert d["evolving_I_change"]["founder_only_loo_skill"] == pytest.approx(
        -0.004590203340453236, abs=1e-12
    )
    assert d["evolving_I_change"]["history_only_loo_skill"] == pytest.approx(
        0.003590596591794837, abs=1e-12
    )
    assert d["evolving_M_change"]["history_only_loo_skill"] == pytest.approx(
        0.4014623432390878, abs=1e-12
    )
    assert d["evolving_I_change"]["interaction_plus_realization_ss_fraction"] == pytest.approx(
        0.9762196648572834
    )
    assert x["endpoint_repeatability_cohort_is_separate"]
    assert x["interaction_plus_realization_not_pure_drift"]


def test_R4_decomposition_recovers_original_first_event_counts():
    x = bridge.crossed_competing_event_identity()
    assert x["B8"]["alive_with_I_support_diff_count"] == -2132
    assert x["B4p5"]["alive_with_I_support_diff_count"] == 9105
    assert x["B4p5"]["alive_with_I_support_diff_pp"] - x["B8"][
        "alive_with_I_support_diff_pp"
    ] == pytest.approx(43.89453125)


def test_R5_no_visitor_exact_signs_keep_negative_zero_and_extinction():
    x = bridge.transfer_source_signs()
    assert x["fixed"]["negative_I_exact_signs"] == 37
    assert x["fixed"]["zero_I_exact_signs"] == 640
    assert x["fixed"]["extinct_futures_I_undefined"] == 320
    assert x["fixed"]["cohorts_with_any_I_change"] == 2
    assert x["evolving"]["negative_I_exact_signs"] == 99
    assert x["evolving"]["zero_I_exact_signs"] == 896
    assert x["evolving"]["extinct_futures_I_undefined"] == 0
    assert x["evolving"]["cohorts_with_any_I_change"] == 4


def test_invalid_R3_score_is_detected(tmp_path, monkeypatch):
    original = json.loads(bridge.PREDICTION.read_text(encoding="utf-8"))
    original["results"]["evolving_I_change"]["loo_skill"]["founder"] += 0.01
    path = tmp_path / "prediction.json"
    path.write_text(json.dumps(original), encoding="utf-8")
    monkeypatch.setattr(bridge, "PREDICTION", path)
    with pytest.raises(AssertionError, match="PRESS"):
        bridge.R3_known_source_predictability_readback()


def test_mutated_R4_first_event_partition_is_detected(tmp_path, monkeypatch):
    original = json.loads(bridge.CROSSED.read_text(encoding="utf-8"))
    original["original_provenance"]["complete_arm_totals"]["fixed_B8"]["genetic_first"] += 1
    path = tmp_path / "crossed.json"
    path.write_text(json.dumps(original), encoding="utf-8")
    monkeypatch.setattr(bridge, "CROSSED", path)
    with pytest.raises(AssertionError, match="non-partitioning"):
        bridge.crossed_competing_event_identity()


def test_mutated_R5_sign_denominator_is_detected(tmp_path, monkeypatch):
    original = json.loads(bridge.TRANSFER.read_text(encoding="utf-8"))
    row = next(r for r in original["tables"]
               if r["destination"] == 0 and r["policy"] == "fixed")
    row["directions"]["I"]["positive"] += 1
    path = tmp_path / "transfer.json"
    path.write_text(json.dumps(original), encoding="utf-8")
    monkeypatch.setattr(bridge, "TRANSFER", path)
    with pytest.raises(AssertionError, match="denominator mismatch"):
        bridge.transfer_source_signs()


def test_complete_bridge_contains_all_five_result_but_no_new_confirmation():
    result = bridge.read_only_audit()
    for key in ("R1_R2_original_and_baseline", "R3_known_source_predictability",
                "R4_competing_event_arithmetic", "R5_no_visitor_transfer"):
        assert key in result
    assert result["new_biological_simulations"] == 0
    assert result["new_preregistered_endpoints"] == 0
