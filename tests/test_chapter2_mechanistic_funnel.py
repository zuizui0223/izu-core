import json
from pathlib import Path

import scripts.generate_chapter2_manuscript_figures_relational as figures
from scripts.render_chapter2_supporting_information import render_supporting_information
from scripts.render_island_ecology_submission_manuscript import render_submission_manuscript

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
NARRATIVE_LOCK = ROOT / "docs/CHAPTER2_FOUR_ACT_NARRATIVE_LOCK_20260902.md"
RELATIONAL = ROOT / "data/results/chapter2_relational_robustness_audit_frozen_20260831.json"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260831.json"
JOURNAL_AUDIT = ROOT / "docs/CHAPTER2_JOURNAL_FIT_AUDIT_20260828.md"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_active_science_preserves_relational_results_and_four_act_narrative_lock():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    narrative = NARRATIVE_LOCK.read_text(encoding="utf-8")
    submission = render_submission_manuscript()
    lower_submission = submission.lower()

    assert manuscript.startswith("# Response geometry under community reorganization")
    assert "Response direction is therefore relational rather than intrinsic" in manuscript
    assert "53/96" in manuscript
    assert "64/96" in manuscript
    assert "partner arrival/replacement in only 2/25" in manuscript
    assert "prespecified Oshima-source bridge was unsupported" in manuscript
    assert "cell-level simulation variation" not in manuscript
    assert "chapter2_scientific_gate_final_20260827.json" not in manuscript
    assert "chapter2_scientific_gate_decision_frozen_20260827.json" in manuscript

    assert "**Theory → Global confrontation → Identifiability → Izu mechanistic-resolution zoom**" in narrative
    assert "The world step is not a fitted projection of synthetic regime labels" in narrative
    assert "project or carry the **response vocabulary**" in narrative
    assert "Formal external prediction is therefore `not_evaluable`, not failed." in narrative

    assert "the paper therefore proceeds through four inferential acts" in lower_submission
    assert "## theory — possibility:" in lower_submission
    assert "## global confrontation:" in lower_submission
    assert "## identifiability:" in lower_submission
    assert "## izu mechanistic zoom:" in lower_submission
    assert "five linked questions" not in lower_submission
    assert "## reality:" not in lower_submission
    assert "## resolution:" not in lower_submission

    abstract = manuscript.split("## Abstract", 1)[1].split("**Keywords:**", 1)[0]
    assert 260 <= len(abstract.split()) <= 280


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
    for text in (manuscript, supporting):
        lower = text.lower()
        assert "cell-level simulation variation" not in lower
        assert "zuizui0223" not in lower
    assert "Response direction is therefore relational rather than intrinsic" in manuscript
    assert "53/96" in manuscript
    assert "# Appendix S16. Prespecified relational-robustness audit" in supporting
    assert "69.34–80.17%" in supporting
    assert "partner arrival/replacement `2/25`" in supporting


def test_relational_main_figures_overlay_only_after_frozen_regeneration(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(figures, "OUT_DIR", tmp_path)
    audit = _load(figures.RELATIONAL)
    why = _load(figures.WHY)
    phase3 = _load(figures.PHASE3)
    izu = _load(figures.IZU)
    figures._validate_relational(audit)
    figures._fig1(audit)
    figures._fig3(audit, why, phase3)
    figures._fig4(audit, izu)
    for name in [
        "fig1_mechanistic_resolution_funnel.svg",
        "fig3_proximal_why_hierarchy.svg",
        "fig4_global_to_izu_resolution.svg",
    ]:
        path = tmp_path / name
        assert path.exists() and path.stat().st_size > 10_000


def test_submission_routing_keeps_oikos_first_and_joecology_fallback():
    manifest = _load(MANIFEST)
    journal_audit = JOURNAL_AUDIT.read_text(encoding="utf-8")
    assert manifest["journal_target"] == "Oikos"
    assert manifest["fallback_route"] == "Journal of Ecology Research Article"
    assert manifest["claim_ceiling"]["relational_response_headline"].startswith("response_direction_depends_on_state")
    assert manifest["narrative_lock"] == "docs/CHAPTER2_FOUR_ACT_NARRATIVE_LOCK_20260902.md"
    assert manifest["story"] == "theory_to_global_confrontation_to_identifiability_to_izu_mechanistic_resolution_zoom"
    assert "project Tier B" in journal_audit
    assert "Oikos — recommended" in journal_audit
