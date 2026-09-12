from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "data" / "design" / "chapter2_nee_predata_promotion_lock_20260912.json"
UPGRADE = ROOT / "docs" / "CHAPTER2_NEE_PREDATA_UPGRADE_CONTRACT_20260912.md"
TRIAGE = ROOT / "docs" / "CHAPTER2_EXTERNAL_TRANSPORT_TRIAGE_20260912.md"
STAGE1 = ROOT / "docs" / "CHAPTER2_NEE_REGISTERED_REPORT_STAGE1_V0_1.md"


def test_promotion_lock_preserves_closed_oikos_fallback() -> None:
    data = json.loads(LOCK.read_text(encoding="utf-8"))
    assert data["status"] == "frozen_before_new_focal_field_outcomes"
    assert data["fallback_surface"]["status"] == "immutable_scientifically_closed"
    assert data["fallback_surface"]["submission_route"] == "Oikos"
    assert data["fallback_surface"]["manuscript"] == "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
    assert data["fallback_surface"]["narrative_lock"] == "docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md"


def test_promotion_lock_is_a_wrapper_over_existing_frozen_designs() -> None:
    data = json.loads(LOCK.read_text(encoding="utf-8"))
    assert data["parents"] == {
        "transition_chain": "data/design/izu_transition_linked_chain_freeze_20260909.json",
        "estimands": "data/design/izu_transition_linked_estimand_lock_20260909.json",
        "rank_order": "data/design/izu_effective_service_rank_crossover_lock_20260911.json",
        "field_readiness": "data/design/effective_pollinator_dependency_field_readiness.json",
    }
    for path in data["parents"].values():
        assert (ROOT / path).exists(), path


def test_prediction_set_and_primary_relation_are_frozen() -> None:
    data = json.loads(LOCK.read_text(encoding="utf-8"))
    assert set(data["predictions"]) == {
        "P1_composition_beyond_amount",
        "P2_state_by_community",
        "P3_functional_bridge",
        "P4_dependency_consequence",
        "P5_determinant_order",
        "P6_transport",
    }
    assert data["predictions"]["P2_state_by_community"]["primary_for_neescope"] is True
    assert data["strict_unit"] == "block_id x plant_id"


def test_no_literal_field_mapping_to_synthetic_k() -> None:
    data = json.loads(LOCK.read_text(encoding="utf-8"))
    p5 = data["predictions"]["P5_determinant_order"]
    assert p5["directional_not_threshold"] is True
    assert p5["no_literal_mapping_to_synthetic_k"] is True
    assert "do not map visitor richness or Hill diversity literally to synthetic k" in data[
        "external_public_data_before_own_data"
    ]["firewall"]


def test_stage1_contract_requires_predata_sampling_and_archiving_commitments() -> None:
    data = json.loads(LOCK.read_text(encoding="utf-8"))
    req = data["stage1_requirements"]
    assert req["experimental_procedures"] == "required"
    assert req["analysis_pipeline"] == "required"
    assert "power analysis" in req["sampling_plan"]
    assert req["data_material_code_commitment"] is True
    assert req["protocol_registration_after_aip"] is True
    assert req["confirmatory_data_before_aip"].startswith("not allowed")


def test_sampling_plan_inherits_existing_precision_state_machine() -> None:
    data = json.loads(LOCK.read_text(encoding="utf-8"))
    sampling = data["sampling_and_precision_inheritance"]
    assert sampling["independent_unit"] == "plant"
    assert set(sampling["within_plant_subsamples"]) == {"flowers", "single-visit SVD events"}
    assert sampling["readiness_state_machine"] == "data/design/effective_pollinator_dependency_field_readiness.json"
    assert sampling["precision_planning_cli"] == "scripts/plan_effective_dependency_pilot_precision.py"
    assert sampling["synthetic_design_simulation_is_empirical_power"] is False


def test_quality_gate_failure_cannot_be_rescued_as_biological_null() -> None:
    data = json.loads(LOCK.read_text(encoding="utf-8"))
    assert data["promotion_logic"]["no_upgrade"].startswith("Q2/Q3/Q6 fail")
    assert "not_evaluable" in STAGE1.read_text(encoding="utf-8").lower()


def test_external_transport_is_partial_not_full_validation() -> None:
    text = TRIAGE.read_text(encoding="utf-8")
    for required in (
        "Thespesia populnea",
        "Nicotiana glauca",
        "Guaiacum sanctum",
        "No currently admitted external system closes the full natural chain",
    ):
        assert required in text


def test_stage1_surface_preserves_primary_hypotheses_and_stop_rule() -> None:
    text = STAGE1.read_text(encoding="utf-8")
    for required in (
        "H1 — composition beyond amount",
        "H2 — plant state x realized community",
        "H3 — functional bridge",
        "H4 — dependency consequence",
        "H5 — determinant-order shift with exposure aggregation",
        "The purpose of pre-data work is to make the future result harder to reinterpret",
    ):
        assert required in text


def test_human_readable_upgrade_contract_exists_and_keeps_oikos_closed() -> None:
    text = UPGRADE.read_text(encoding="utf-8")
    assert "does not reopen or supersede the scientifically closed Oikos manuscript" in text
    assert "Do not reopen the synthetic mechanism to chase a higher journal" in text
