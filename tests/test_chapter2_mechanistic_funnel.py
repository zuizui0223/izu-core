import json
from pathlib import Path

import scripts.generate_chapter2_manuscript_figures_relational as figures
from scripts.render_chapter2_realized_richness_reframe import render_submission_manuscript
from scripts.render_chapter2_supporting_information import render_supporting_information

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
NARRATIVE_LOCK = ROOT / "docs/CHAPTER2_THREE_RESULT_NARRATIVE_LOCK_20260908.md"
RELATIONAL = ROOT / "data/results/chapter2_relational_robustness_audit_frozen_20260831.json"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260831.json"
JOURNAL_AUDIT = ROOT / "docs/CHAPTER2_JOURNAL_FIT_AUDIT_20260828.md"
MATERIAL_MAP = ROOT / "docs/CHAPTER2_MAIN_SUPP_MATERIAL_MAP_20260907.md"
TABLES = ROOT / "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_TABLES_20260827.md"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_active_submission_uses_three_linked_results_and_keeps_historical_source_frozen():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    narrative = NARRATIVE_LOCK.read_text(encoding="utf-8")
    submission = render_submission_manuscript()
    lower_submission = submission.lower()

    # The source manuscript remains a frozen upstream surface; the final renderer owns the reframe.
    assert manuscript.startswith("# Response geometry under community reorganization")
    assert "53/96" in manuscript
    assert "64/96" in manuscript
    assert "partner arrival/replacement in 2/25" in manuscript
    assert "prespecified Oshima-source bridge was unsupported" in manuscript
    assert "cell-level simulation variation" not in manuscript

    assert "**mechanistic prediction → real-world compositional exposure → biological consequence**" in narrative
    assert "Identifiability is now deliberately demoted" in narrative
    assert "Wanshan–Yongxing" in narrative
    assert "Ogasawara" in narrative

    assert "result 1—mechanistic prediction" in lower_submission
    assert "result 2—real-world exposure" in lower_submission
    assert "result 3—biological consequence" in lower_submission
    assert "## result 1 — community reorganization separated coarse regime placement from branch identity" in lower_submission
    assert "## result 2 — real island systems undergo compositional reorganization beyond richness loss" in lower_submission
    assert "## result 3 — functional community structure in izu propagated into divergent plant responses" in lower_submission
    assert "pollinator assemblage turnover was 0.9796" in lower_submission
    assert "matched-plant turnover was 0.6817" in lower_submission
    assert "### result 2 claim boundary" in lower_submission
    assert "### historical boundary check" in lower_submission
    assert "## identifiability:" not in lower_submission
    assert "## global confrontation:" not in lower_submission
    assert "## izu mechanistic zoom:" not in lower_submission
    assert "response direction is therefore relational rather than intrinsic" not in lower_submission

    abstract = submission.split("## Abstract", 1)[1].split("**Keywords:**", 1)[0]
    assert 240 <= len(abstract.split()) <= 300


def test_relational_audit_preserves_ordering_without_stable_magnitude_claim():
    audit = _load(RELATIONAL)
    assert audit["status"] == "frozen_complete_20260831"
    assert audit["seed_ensemble"]["community_realization_fraction_range"] == [
        0.6933825278526522,
        0.8017383395125494,
    ]
    assert audit["seed_ensemble"]["baseline_seed_is_maximum_community_fraction_in_this_prespecified_ensemble"] is True
    assert all(row["largest_component"] == "community_realization" for row in audit["structural_horizon"])
    zero = next(row for row in audit["trait_adjustment_context"] if row["trait_adjustment"] == 0.0)
    assert zero["realization_class_counts"]["mixed_sign"] == 64
    assert zero["sum_of_squares_fraction"]["starting_position_by_community_nonadditivity"] > 0.32
    equal = audit["equal_initial_pollinator_richness"]
    assert equal["realization_class_counts"]["mixed_sign"] == 53
    assert equal["mainland_initial_pollinator_types"] == 9
    assert equal["island_initial_pollinator_types"] == 9


def test_rendered_submission_and_si_remove_superseded_internal_wording():
    manuscript = render_submission_manuscript()
    supporting = render_supporting_information()
    lower = manuscript.lower()
    for text in (manuscript, supporting):
        assert "cell-level simulation variation" not in text.lower()
        assert "zuizui0223" not in text.lower()
    assert "all six prespecified matching seeds" in lower
    assert "51–65 of 96 remained mixed-sign" in lower
    assert "pollinator assemblage turnover was 0.9796" in lower
    assert "matched-plant turnover was 0.6817" in lower
    assert "# Appendix S16. Prespecified relational-robustness audit" in supporting
    assert "69.34–80.17%" in supporting
    assert "partner arrival/replacement `2/25`" in supporting
    assert "# Appendix S17. Geography-first saturation and final world synthesis" in supporting
    assert "4,663" in supporting
    assert "42 research entries across 37 exact geographic labels" in supporting
    assert "# Appendix S18. Contemporary Izu functional-chain sensitivity" in supporting
    assert "+1.9426" in supporting and "+2.0590" in supporting
    assert "+0.0353" in supporting
    assert "3 shorter / 4 longer / 1 unchanged" in supporting


def test_relational_main_figures_overlay_only_after_frozen_regeneration(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(figures, "OUT_DIR", tmp_path)
    audit = _load(figures.RELATIONAL)
    why = _load(figures.WHY)
    phase3 = _load(figures.PHASE3)
    izu = _load(figures.IZU)
    contemporary = _load(figures.CONTEMPORARY)
    pollen = _load(figures.POLLEN)
    figures._validate_relational(audit)
    figures._fig1(audit)
    figures._fig3(audit, why, phase3)
    figures._fig4(audit, izu, contemporary, pollen)
    for name in [
        "fig1_mechanistic_resolution_funnel.svg",
        "fig3_proximal_why_hierarchy.svg",
        "fig4_global_to_izu_resolution.svg",
    ]:
        path = tmp_path / name
        assert path.exists() and path.stat().st_size > 10_000


def test_main_supp_material_map_and_supporting_tables_match_current_paper():
    material = MATERIAL_MAP.read_text(encoding="utf-8")
    tables = TABLES.read_text(encoding="utf-8")
    lower_material = material.lower()
    lower_tables = tables.lower()

    assert "main figure 4" in lower_material
    assert "fdq -> corrected matching" in lower_material
    assert "supporting information structure" in lower_material
    assert "s17" in lower_material and "s18" in lower_material and "s19" in lower_material
    assert "table s1" in lower_material and "table s8" in lower_material and "table s9" in lower_material
    assert "wanshan–yongxing" in lower_material
    assert "ogasawara" in lower_material
    assert "not the study objective" in lower_material
    assert "prospective visitor-effectiveness" in lower_material
    assert "not a prerequisite for the present paper" in lower_material

    assert tables.startswith("# Chapter 2 Supporting Tables")
    for label in range(1, 9):
        assert f"Table S{label}." in tables
    assert "cell-level simulation variation" not in lower_tables
    assert "exact non-additive remainder" in lower_tables
    assert "42 research entries / 37 exact labels" in tables
    assert "+1.9426" in tables and "+2.0590" in tables
    assert "3 | 4 | 1" in tables


def test_submission_routing_keeps_oikos_first_and_three_result_contract():
    manifest = _load(MANIFEST)
    journal_audit = JOURNAL_AUDIT.read_text(encoding="utf-8")
    assert manifest["journal_target"] == "Oikos"
    assert manifest["fallback_route"] == "Journal of Ecology Research Article"
    assert manifest["claim_ceiling"]["relational_response_headline"] == "branch_identity_depends_on_state_evaluated_against_realized_community_composition"
    assert manifest["claim_ceiling"]["world_step_projects"] == "response_vocabulary_and_compositional_exposure_not_synthetic_regime_assignments"
    assert manifest["claim_ceiling"]["identifiability_role"] == "claim_boundary_not_primary_result"
    assert manifest["narrative_lock"] == "docs/CHAPTER2_THREE_RESULT_NARRATIVE_LOCK_20260908.md"
    assert manifest["story"] == "mechanistic_prediction_to_real_world_compositional_exposure_to_izu_biological_consequence"
    assert manifest["oikos_initial_submission_contract"]["three_result_submission_narrative"] is True
    assert manifest["oikos_initial_submission_contract"]["four_act_submission_narrative"] is False
    assert manifest["oikos_initial_submission_contract"]["identifiability_is_coequal_study_objective"] is False
    assert manifest["oikos_initial_submission_contract"]["world_step_assigns_empirical_systems_to_synthetic_regimes"] is False
    assert manifest["world_saturation_and_izu_continuity"]["large_island_saturation_rule_met"] is True
    assert manifest["world_saturation_and_izu_continuity"]["chapter3_direct_phenotype_owned_separately"] is True
    assert "project Tier B" in journal_audit
    assert "Oikos — recommended" in journal_audit
