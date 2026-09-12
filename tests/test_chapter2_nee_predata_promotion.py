from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "data" / "design" / "chapter2_nee_predata_promotion_lock_20260912.json"
H5 = ROOT / "data" / "design" / "chapter2_nee_h5_correlation_stratification_lock_20260912.json"
R5 = ROOT / "data" / "design" / "chapter2_nee_r5_transport_decision_20260912.json"
OC = ROOT / "data" / "results" / "chapter2_nee_h5_prepilot_oc_20260912.json"
STAGE1 = ROOT / "docs" / "CHAPTER2_NEE_REGISTERED_REPORT_STAGE1_V0_1.md"
READINESS = ROOT / "docs" / "CHAPTER2_NEE_STAGE1_READINESS_20260912.md"
DESIGN = ROOT / "docs" / "CHAPTER2_NEE_STAGE1_DESIGN_TABLE_20260912.md"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_promotion_lane_preserves_closed_oikos_surface() -> None:
    data = _load(LOCK)
    assert data["status"] == "frozen_before_new_focal_field_outcomes"
    assert data["fallback_surface"]["status"] == "immutable_scientifically_closed"
    assert data["fallback_surface"]["submission_route"] == "Oikos"
    assert data["target_route"]["not_a_target_change_for_current_paper"] is True
    assert data["predictions"]["P6_transport"]["not_required_for_oikos"] is True


def test_promotion_lock_points_to_all_frozen_stage1_contracts() -> None:
    data = _load(LOCK)
    parents = data["parents"]
    for key in (
        "transition_chain",
        "estimands",
        "rank_order",
        "field_readiness",
        "effective_community",
        "h5_correlation_stratification",
        "r5_transport",
        "h5_prepilot_oc",
    ):
        assert key in parents
        assert (ROOT / parents[key]).exists(), parents[key]


def test_h5_is_conditional_two_sided_and_rho_is_not_a_field_threshold() -> None:
    promotion = _load(LOCK)
    h5 = _load(H5)
    p5 = promotion["predictions"]["P5_determinant_order"]
    assert p5["status"] == "conditional_two_sided_frozen"
    assert "decreases community-realization contribution" in p5["low_shared_dependence_prediction"]
    assert "variance floor" in p5["high_shared_dependence_prediction"]
    assert p5["generic_rho_critical"] == 0.25
    assert p5["generic_rho_critical_is_natural_threshold"] is False
    assert h5["theory_translation"]["natural_cutoff_allowed"] is False
    assert h5["interpretation_firewall"]["no_redistribution_in_high_dependence_is_not_automatic_falsification"] is True
    assert "NOT_EVALUABLE" in h5["H5a_low_dependence"]["not_evaluable"]
    assert "NOT_EVALUABLE" in h5["H5b_high_dependence"]["not_evaluable"]


def test_r5_requires_second_prospective_context_for_nee() -> None:
    promotion = _load(LOCK)
    r5 = _load(R5)
    assert r5["current_secondary_evidence"]["P6_admitted_from_existing_secondary_data"] is False
    assert r5["nee_route_decision"]["independent_transport_required_for_NEE_stage1"] is True
    assert promotion["stage1_requirements"]["second_prospective_context"] == "required for NEE route"
    assert promotion["quality_gates"]["Q7_breadth"].startswith("second prospective independent natural context")
    assert "EL/Ecology" in promotion["promotion_logic"]["general_ecology_strong"]


def test_h5_prepilot_oc_is_scale_screen_not_empirical_power() -> None:
    oc = _load(OC)
    decision = oc["decision"]
    assert decision["H5_is_precision_bottleneck"] is True
    assert decision["independent_block_count_is_primary_design_lever"] is True
    assert decision["near_boundary_shared_dependence_is_hardest_region"] is True
    assert decision["even_1536_recruits_does_not_make_near_boundary_H5_decisive"] is True
    assert decision["final_R3_requires_empirical_pilot"] is True
    assert decision["do_not_weaken_H5_if_R3_infeasible"] is True
    assert "not empirical power" in oc["claim_boundary"].lower()


def test_r_states_leave_r1_r2_r3_r6_open_but_close_r4_r5() -> None:
    states = _load(LOCK)["R_states"]
    assert states == {
        "R1_field_scope_and_transport_context": "OPEN",
        "R2_pilot_dispersion_attrition_dependence_support": "OPEN",
        "R3_confirmatory_precision": "OPEN",
        "R4_effective_community_representation": "CLOSED",
        "R5_breadth_strategy": "CLOSED",
        "R6_admin": "OPEN",
    }


def test_human_surfaces_preserve_two_sided_h5_and_nee_retreat_line() -> None:
    stage1 = STAGE1.read_text(encoding="utf-8")
    readiness = READINESS.read_text(encoding="utf-8")
    design = DESIGN.read_text(encoding="utf-8")
    for text in (stage1, readiness, design):
        lower = text.lower()
        assert "lower shared dependence" in lower or "lower-shared-dependence" in lower
        assert "higher shared dependence" in lower or "higher-shared-dependence" in lower
        assert "not" in lower and "rho=0.25" in lower
        assert "second prospective" in lower
        assert "not_evaluable" in lower
    assert "H1-H4 remain confirmatory" in stage1
    assert "do not weaken H5" in readiness
    assert "REQUIRED FOR NEE ROUTE" in design


def test_stage1_sampling_contract_keeps_final_r3_empirical() -> None:
    data = _load(LOCK)
    sampling = data["sampling_and_precision_inheritance"]
    assert sampling["independent_unit"] == "plant"
    assert sampling["h5_prepilot_oc_is_empirical_power"] is False
    assert sampling["H5_is_precision_bottleneck"] is True
    assert sampling["final_R3_requires_empirical_pilot"] is True
    assert sampling["precision_planning_cli"] == "scripts/plan_effective_dependency_pilot_precision.py"
