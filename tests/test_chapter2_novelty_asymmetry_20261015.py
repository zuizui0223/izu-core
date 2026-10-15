"""Guard the source-derived evidence rank of the Ch2 asymmetry novelty candidate.

These tests examine already-frozen values and source note provenance;
they do not run the reproductive ABM or validate claims of literature priority.
"""
import pytest

from scripts.audit_chapter2_novelty_asymmetry_20261015 import audit, SETTINGS


def test_all_four_original_sources_and_distinct_inference_units():
    report = audit()
    assert report["checks_passed"] == 4
    assert report["new_evolutionary_trajectories"] == 0
    assert "8 nested" in report["main_inference_unit"]
    assert "1 of 8" in report["checkpoint_inference_unit"]
    assert [x["setting"] for x in report["findings"]] == list(SETTINGS)


def test_far_is_relative_relief_but_total_investment_still_declines():
    for row in audit()["findings"]:
        assert row["main_64history_8repeat_evolving_minus_fixed_near"] < 0
        assert row["main_64history_8repeat_evolving_minus_fixed_far"] > 0
        assert row["main_far_fixed_I_change_from_founder"] < 0
        assert row["main_far_evolving_I_change_from_founder"] < 0
        assert row["main_64history_8repeat_differential_attenuation"] == pytest.approx(
            row["main_64history_8repeat_evolving_minus_fixed_far"]
            - row["main_64history_8repeat_evolving_minus_fixed_near"],
            abs=1e-12,
        )


def test_original_checkpoint_and_one_step_are_not_endpoint_estimates():
    for row in audit()["findings"]:
        assert row["source_64history_1repeat_far_EminusF_t200"] > 0
        assert row["source_64history_1repeat_far_EminusF_t400"] > 0
        assert row["source_64history_1repeat_far_EminusF_t1000"] > 0
        assert row["source_64history_1repeat_far_conditional_Price_EminusF_t400"] < 0
        assert (
            row["static_assurance_higher_minus_lower_gradient_near_t400"]
            < row["static_assurance_higher_minus_lower_gradient_far_t400"]
            < 0
        )
    assert "historical cause of positive far E-F is not identified" in audit()["claim_ceiling"]


def test_original_named_attenuations_without_adding_novel_confirmations():
    by_setting = {r["setting"]: r for r in audit()["findings"]}
    assert by_setting["delayed_control"]["main_64history_8repeat_differential_attenuation"] == pytest.approx(0.1605393791, abs=1e-8)
    assert by_setting["prior_selfing"]["main_64history_8repeat_differential_attenuation"] == pytest.approx(0.2200155005, abs=1e-8)
    assert by_setting["pollen_discount"]["main_64history_8repeat_differential_attenuation"] == pytest.approx(0.1915008068, abs=1e-8)
    assert by_setting["assurance_cost"]["main_64history_8repeat_differential_attenuation"] == pytest.approx(0.1007488748, abs=1e-8)
