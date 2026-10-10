"""Read-only source and mathematical checks for Q3→Q4 inference boundaries."""
import math

import pytest

from scripts.audit_chapter2_four_question_q3q4_feasibility import (
    SETTINGS, SCALES, STATUS, audit, one_step_occupancy, poisson_capped_mean
)


def test_exact_capped_poisson_recruitment_and_K_independent_binary_occupancy():
    mu = 8.99442
    assert poisson_capped_mean(mu, 8) == pytest.approx(7.268042675, abs=1e-7)
    assert poisson_capped_mean(mu, 48) == pytest.approx(mu, abs=1e-8)
    assert one_step_occupancy(mu) == pytest.approx(1-math.exp(-mu), abs=1e-14)
    assert poisson_capped_mean(0, 8) == 0
    assert one_step_occupancy(0) == 0
    assert poisson_capped_mean(1000, 48) == 48
    assert one_step_occupancy(1000) == 1.0
    assert poisson_capped_mean(1.25, 1) == pytest.approx(one_step_occupancy(1.25))


@pytest.mark.parametrize("mu,k", [(-1,8), (float("nan"),8), (float("inf"),8), (0,0), (2,2.5), (2,True)])
def test_bad_demographic_inputs_are_rejected(mu, k):
    with pytest.raises(ValueError):
        poisson_capped_mean(mu,k)


def test_read_only_feasibility_from_full_original_main_receipts():
    a = audit()
    assert a["status"] == STATUS
    assert a["n_new_independent_histories"] == 0
    assert a["n_new_stochastic_trajectories"] == 0
    assert a["n_original_reused_histories"] == 64
    assert a["n_old_nested_repeats_per_history"] == 1
    assert a["n_exposed_one_year_cells"] == 1536
    assert a["source_original_shapley_raw_sha256"] == (
        "6fdd8ed45af9f7b9c65b513cb20fa1f3ba224519695ec37940421a7a6d60ae5e"
    )
    assert a["source_original_paired_raw_sha256"] == (
        "34846d5ea2b758c7123af42130cceec7b3581c4c9a95dcbd0de52c651a599b57"
    )
    assert a["source_original_shapley_raw_sha256"] != a["source_original_paired_raw_sha256"]
    assert a["source_original_reproductive_biology_sha256"] == (
        "885957edb8a165ee8528781ed1d2574c44143c608496b505f9663cbfac2c4081"
    )
    assert a["tested_scale_grid_post_outcome"] == list(SCALES)
    assert len(a["by_scale"]) == 6
    assert a["n_settings_with_mean_seed_increase_despite_delivered_pollen_loss"] == 3
    assert a["n_source_E_history_scale_cells_with_intermediate_one_year_occupancy"] == 6
    assert a["n_total_E_history_scale_cells"] == 1536
    assert a["max_intermediate_E_per_64_history_setting"] == 6
    assert a["minimum_setting_mean_E_one_year_occupancy"] == pytest.approx(.945796, abs=1e-7)
    assert a["original_min_viable_seed_mean_across_original_source_arms"] == pytest.approx(
        67.279434303, abs=1e-8
    )
    u = a["rigorous_max_absolute_conditional_one_step_occupancy_change_by_scale"]
    assert u[str(.125)] == pytest.approx(math.exp(-.125 * 67.279434303))
    assert 0 < u[str(.125)] < .000223
    assert 0 < u[str(.25)] < 5e-8
    assert 0 < u[str(1.0)] < 7e-30
    assert all(u[str(b)] > u[str(2*b)] for b in (.025, .125, .25))
    assert "not a CI" in a["bound_note"]
    assert a["decision"].startswith("NO_GO")
    assert "80-update" in a["scientific_interpretation"]
    assert "unmerged" in a["census_example_unmerged_source"]["provenance"]


def test_census_interior_is_not_occupancy_interior():
    out = audit()
    s125 = next(r for r in out["by_scale"] if r["budget_multiplier"] == .125)
    assert set(s125["intermediate_expected_N_both_arms_per_setting"]) == set(SETTINGS)
    assert all(v == 64 for v in s125["intermediate_expected_N_both_arms_per_setting"].values())
    assert all(v == 0 for v in s125["E_histories_with_one_year_occupancy_0p1_to_0p9"].values())
    assert s125["min_occupancy_across_settings"] > .99999

    s05 = next(r for r in out["by_scale"] if r["budget_multiplier"] == .05)
    assert min(s05["intermediate_expected_N_both_arms_per_setting"].values()) >= 52
    assert s05["min_occupancy_across_settings"] > .995
    assert s05["E_minus_clamp_expected_next_N_mean"]["delayed_control"] < 0
    assert all(s05["E_minus_clamp_expected_next_N_mean"][name] > 0 for name in SETTINGS[1:])


def test_postoutcome_source_universality_and_pilot_conflation_are_blocked():
    out = audit()
    assert "no new experiment" in out["limits"][0].lower()
    assert "NOT_IN_MAIN" in out["census_example_unmerged_source"]["provenance"]
    assert out["fixed_K"] == out["fixed_B"] == 48
    assert "longitudinal" in out["decision"].lower()
