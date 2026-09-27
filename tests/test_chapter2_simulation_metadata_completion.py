import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "data/design/chapter2_simulation_metadata_completion_lock_20260912.json"
DOC = ROOT / "docs/CHAPTER2_SIMULATION_METADATA_COMPLETION_20260912.md"
THESIS = ROOT / "THESIS_CHAPTER_POSITIONING.md"
README = ROOT / "README.md"
MANUSCRIPT = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
LEGACY_FIGURES = ROOT / "scripts/generate_chapter2_manuscript_figures_realized_richness.py"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260927.json"
WORLD = ROOT / "data/results/chapter2_global_master_manuscript_value_review_audit_20260906.json"
IZU = ROOT / "data/results/chapter2_izu_final_mechanistic_zoom_audit_20260906.json"
WANSHAN = ROOT / "data/results/wanshan_yongxing/effect_rows.json"
OGASAWARA = ROOT / "data/results/ogasawara/context_analysis/effect_rows.json"


def test_historical_completion_lock_requires_no_new_focal_data() -> None:
    data = json.loads(LOCK.read_text(encoding="utf-8"))
    assert data["status"] == "chapter2_complete_without_new_focal_data"
    basis = data["completion_basis"]
    assert basis["new_focal_field_data_required"] is False
    assert basis["chapter3_phenotype_required"] is False
    assert basis["nee_stage1_required"] is False
    assert basis["additional_world_search_required"] is False


def test_historical_metadata_layer_is_constraint_not_full_validation() -> None:
    data = json.loads(LOCK.read_text(encoding="utf-8"))
    m1 = data["metadata_evidence_stack"]["M1_formal_source_audit"]
    assert m1["full_outcome_independent_contracts"] == "0_of_25"
    assert m1["formal_external_prediction"] == "not_evaluable"
    assert data["claim_ceiling"]["metadata_counts_as_full_mechanism_validation"] is False


def test_historical_completion_lock_matches_world_and_izu_audits() -> None:
    data = json.loads(LOCK.read_text(encoding="utf-8"))
    world = json.loads(WORLD.read_text(encoding="utf-8"))
    izu = json.loads(IZU.read_text(encoding="utf-8"))
    m1 = data["metadata_evidence_stack"]["M1_formal_source_audit"]
    m2 = data["metadata_evidence_stack"]["M2_descriptive_world_breadth"]
    m4 = data["metadata_evidence_stack"]["M4_izu_existing_secondary_data"]

    assert m1["research_entries"] == world["active_manuscript_boundary"]["formal_identifiability_research_entries"]
    assert m1["full_outcome_independent_contracts"] == world["active_manuscript_boundary"]["formal_full_contracts"]
    assert m2["research_entries"] == world["active_manuscript_boundary"]["descriptive_research_entries"]
    assert m2["exact_geographic_labels"] == world["active_manuscript_boundary"]["exact_geographic_labels"]
    assert m4["functional_exposure_to_corrected_matching_supported"] is izu["izu_current_evidence"]["current_functional_exposure_to_matching"]["supported"]
    assert m4["matching_to_pollen_leave_one_island_sign_stable"] is izu["izu_current_evidence"]["matching_to_pollen"]["leave_one_island_sign_stable"]
    assert m4["historical_signed_position_null_corrected_supported"] is izu["izu_current_evidence"]["signed_position"]["null_corrected_supported"]


def test_source_native_external_composition_examples_remain_frozen_provenance() -> None:
    wanshan = json.loads(WANSHAN.read_text(encoding="utf-8"))
    ogasawara = json.loads(OGASAWARA.read_text(encoding="utf-8"))
    w = {row["effect_id"]: row for row in wanshan["effects"]}
    o = {row["effect_id"]: row for row in ogasawara["effects"]}

    assert round(w["wanshan_yongxing_partner_turnover"]["estimate"], 3) == 0.980
    assert round(w["wanshan_yongxing_pollinator_richness_lrr"]["estimate"], 3) == -0.105
    assert w["wanshan_yongxing_partner_turnover"]["causal_claim_allowed"] is False
    assert round(o["ogasawara_anijima_partner_turnover"]["estimate"], 3) == 0.682
    assert round(o["ogasawara_anijima_pollinator_richness_lrr"]["estimate"], 3) == -0.315
    assert o["ogasawara_anijima_partner_turnover"]["causal_claim_allowed"] is False


def test_active_oikos_manifest_uses_bridge_gated_unified_model3_and_no_field_completion_gate() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["scientific_state"] == "unified_model3_core_mechanism_with_open_original_ch2_bridge_controls"
    assert manifest["prospective_unification_audit"]["decision"] == "model2_not_required_as_separate_biological_mechanism_but_legacy_controls_not_fully_redundant"
    assert manifest["real_island_confrontation"]["principal_gap"] == "B_inherited_longitudinal_response_under_measured_visitor_regime"
    assert manifest["current_submission_state"]["new_field_data_required"] is False
    assert manifest["current_submission_state"]["scientific_question_closed"] is False
    assert manifest["current_submission_state"]["model3_bridge_campaign_required_for_original_control_equivalence"] is True
    assert manifest["formal_natural_evidence_boundary"]["complete_A_to_B_to_C_contracts"] == "0_of_25"


def test_human_surfaces_preserve_no_field_completion_rule_and_chapter1_bridge() -> None:
    doc = DOC.read_text(encoding="utf-8")
    thesis = THESIS.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    assert "Chapter 2 is complete without new focal field data" in doc
    assert "does **not** require a same-block field chain" in thesis
    assert "Chapter 1 unresolved-problem handoff" in thesis
    assert "CHAPTER1_CHAPTER2_CANONICAL_BRIDGE_20260927.md" in thesis
    assert "not a submission gate or completion criterion" in readme
    assert "inherited longitudinal layer mostly missing" in readme


def test_active_manuscript_contains_layer_specific_real_island_confrontation() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    lower = text.lower()
    assert "## layer-specific confrontation with real island systems" in lower
    assert "## real islands occupy different stages of the same response architecture" in lower
    assert "21/25" in text and "2/25" in text and "0/25" in text
    assert "all eight shared oshima-to-post targets" in lower
    assert "four lower and four higher" in lower
    assert "three shorter, four longer and one unchanged" in lower
    assert "same-direction propagation case" in lower
    assert "counterdirectional case" in lower
    assert "the main natural-data gap" in lower
    assert "inherited longitudinal" in lower


def test_legacy_figure4_generator_remains_provenance_until_unified_figures_are_regenerated() -> None:
    text = LEGACY_FIGURES.read_text(encoding="utf-8")
    assert "Source-native composition ≠ richness" in text
    assert "Existing Izu stress test" in text
    assert '"figure4_external_systems": ["wanshan_yongxing", "ogasawara_anijima"]' in text
    assert "metadata_confrontation_and_empirical_claim_ceiling" in text
