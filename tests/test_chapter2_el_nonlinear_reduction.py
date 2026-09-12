from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_chapter2_el_nonlinear_reduction.py"
RESULT = ROOT / "data" / "results" / "chapter2_el_nonlinear_reduction_audit_20260913.json"
POSITIONING = ROOT / "docs" / "CHAPTER2_ECOLOGY_LETTERS_POSITIONING_20260912.md"

spec = importlib.util.spec_from_file_location("lane_b_nonlinear", SCRIPT)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def _result() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_bilinear_exactly_fixes_interaction_to_community_ratio() -> None:
    ratios = []
    for rho in (0.0, 0.1, 0.4, 0.75):
        for k in (1, 2, 4, 8, 16, 32):
            row = mod.exact_bilinear(a=0.5, b=1.0, c=0.8, var_x=1.0, sigma2=1.0, k=k, rho=rho)
            ratios.append(row["I_over_C"])
    assert max(ratios) - min(ratios) < 1e-12


def test_bilinear_forbids_CI_order_reversal_but_not_three_order_regions() -> None:
    exact = _result()["exact_bilinear"]["exact_invariances"]
    assert exact["C_vs_I_relative_order_can_flip"] is False
    assert exact["maximum_S_crossing_events_as_tau_decreases"] == 2
    assert exact["maximum_order_regions_along_monotone_tau"] == 3


def test_existing_chapter2_abm_breaks_first_order_CI_invariance() -> None:
    abm = _result()["chapter2_abm_existing"]
    assert abm["C_over_I_order_reverses"] is True
    assert abm["intermediate_I_winner_present"] is True
    assert abm["order_path"] == ["CIS", "CIS", "ISC", "SIC", "SIC"]
    ratios = [row["I_over_C"] for row in abm["rows"]]
    assert ratios[-1] / ratios[0] > 7.0


def test_second_nonlinear_class_has_broad_intermediate_interaction_phase() -> None:
    summary = _result()["adaptive_consumer_resource"]["grid_summary"]
    assert summary["seed_setting_trajectories"] == 324
    assert summary["trajectories_with_intermediate_I_winner"] == 255
    assert summary["settings_with_intermediate_I_winner_in_at_least_4_of_6_seeds"] == 42
    assert summary["settings_with_CI_order_flip_in_at_least_4_of_6_seeds"] == 18
    assert summary["settings_with_full_C_to_I_to_S_in_at_least_4_of_6_seeds"] == 10
    assert summary["settings_with_full_C_to_I_to_S_in_all_6_seeds"] == 9


def test_identity_preserving_correlation_rejects_keff_sufficiency() -> None:
    corr = _result()["identity_preserving_event_correlation"]
    assert corr["decision"]["k_eff_as_variance_equivalent_count_coordinate_is_sufficient_for_response_decomposition"] is False
    rows = {row["rho_event_latent"]: row for row in corr["rows"]}
    rho_05 = rows[0.5]
    assert 3.5 < rho_05["count_variance_equivalent_k_eff"] < 4.3
    assert rho_05["nearest_independent_k"] == 4
    assert rho_05["orders_across_six_seeds"] == {"SIC": 6}
    assert rho_05["nearest_independent_order"] == "ISC"
    assert rho_05["L1_fraction_distance_to_nearest_independent"] > 0.45
    rho_075 = rows[0.75]
    assert 2.0 < rho_075["count_variance_equivalent_k_eff"] < 2.7
    assert rho_075["nearest_independent_k"] == 2
    assert rho_075["orders_across_six_seeds"] == {"SIC": 6}
    assert rho_075["nearest_independent_order"] == "CIS"
    assert rho_075["L1_fraction_distance_to_nearest_independent"] > 0.8


def test_I_over_C_is_diagnostic_not_a_nonlinear_rho_invariance_law() -> None:
    decision = _result()["identity_preserving_event_correlation"]["decision"]
    assert decision["I_over_C_strictly_rho_invariant_in_nonlinear_ABM"] is False
    assert "diagnostic" in decision["I_over_C_role"]


def test_active_EL_positioning_centers_reduction_failure_not_just_crossover() -> None:
    lower = POSITIONING.read_text(encoding="utf-8").lower()
    assert "variance-equivalent coordinate" in lower
    assert "not a sufficient statistic" in lower
    assert "interaction-dominated intermediate phase" in lower
    assert "c/i" in lower
    assert "lane c" in lower
