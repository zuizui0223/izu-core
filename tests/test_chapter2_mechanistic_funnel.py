import json
from pathlib import Path

from scripts.render_chapter2_oikos_generality_overlay import render_submission_manuscript
from scripts.render_chapter2_supporting_information import render_supporting_information

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
NARRATIVE_LOCK = ROOT / "docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md"
HISTORICAL_THREE_RESULT = ROOT / "docs/CHAPTER2_THREE_RESULT_NARRATIVE_LOCK_20260908.md"
RELATIONAL = ROOT / "data/results/chapter2_relational_robustness_audit_frozen_20260831.json"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260831.json"
MATERIAL_MAP = ROOT / "docs/CHAPTER2_MAIN_SUPP_MATERIAL_MAP_20260907.md"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_active_submission_uses_mechanism_mainline_and_preserves_history():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    narrative = NARRATIVE_LOCK.read_text(encoding="utf-8")
    historical = HISTORICAL_THREE_RESULT.read_text(encoding="utf-8")
    submission = render_submission_manuscript()
    lower = submission.lower()

    assert manuscript.startswith("# Response geometry under community reorganization")
    assert "conditional response geometry" in lower
    assert "realized richness differences therefore help position the ensemble mean regime" in lower
    assert "ordering of response determinants is itself regime dependent" in lower
    assert "55.84%" in submission and "12.72%" in submission
    assert "deterministic mean-field kernel contrast was all-positive" in lower
    assert "optional future validation programme" in lower

    assert "coarse regime placement → relational branch identity → determinant-rank crossover → downstream modification" in narrative
    assert "field e3/e4 remains future/optional validation" in narrative.lower()

    # Historical contracts remain readable provenance but are no longer active routing.
    assert historical.startswith("# Chapter 2 three-result narrative lock")
    assert "**mechanistic prediction → real-world compositional exposure → biological consequence**" in historical
    assert "result 1—mechanistic prediction" not in lower
    assert "result 2—real-world exposure" not in lower
    assert "result 3—biological consequence" not in lower


def test_relational_audit_remains_frozen_baseline_not_universal_rank_claim():
    audit = _load(RELATIONAL)
    assert audit["status"] == "frozen_complete_20260831"
    assert audit["seed_ensemble"]["community_realization_fraction_range"] == [
        0.6933825278526522,
        0.8017383395125494,
    ]
    assert audit["seed_ensemble"]["baseline_seed_is_maximum_community_fraction_in_this_prespecified_ensemble"] is True
    assert all(row["largest_component"] == "community_realization" for row in audit["structural_horizon"])

    # This historical finite-regime audit is retained, but later system-size work
    # changes the paper-level interpretation from universal community dominance.
    submission = render_submission_manuscript().lower()
    assert "community realization dominates in small stochastic communities" in submission
    assert "starting state becomes dominant in a larger finite-community regime" in submission
    assert "numerical crossover is model-specific" in submission


def test_manifest_routes_mechanism_mainline_and_demotes_field_validation():
    manifest = _load(MANIFEST)
    assert manifest["journal_target"] == "Oikos"
    assert manifest["fallback_route"] == "Journal of Ecology Research Article"
    assert manifest["narrative_lock"] == "docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md"
    assert manifest["historical_three_result_narrative_lock"] == "docs/CHAPTER2_THREE_RESULT_NARRATIVE_LOCK_20260908.md"
    assert manifest["story"] == "conditional_geometry_to_richness_control_to_determinant_rank_crossover_to_bounded_empirical_claim_ceiling"
    assert manifest["claim_ceiling"]["determinant_ordering"] == "regime_dependent_across_declared_system_size_audit"
    assert manifest["claim_ceiling"]["field_e3_e4_required_for_current_paper"] is False
    assert manifest["oikos_initial_submission_contract"]["mechanism_mainline_submission_narrative"] is True
    assert manifest["oikos_initial_submission_contract"]["three_result_submission_narrative"] is False
    assert manifest["world_saturation_and_izu_continuity"]["izu_e3_e4_status"] == "future_optional_validation_not_completion_gate"


def test_supporting_information_retains_empirical_and_structural_audit_layers():
    supporting = render_supporting_information()
    lower = supporting.lower()
    assert "# appendix s16. prespecified relational-robustness audit" in lower
    assert "# appendix s17. geography-first saturation and final world synthesis" in lower
    assert "# appendix s18. contemporary izu functional-chain sensitivity" in lower
    assert "69.34–80.17%" in supporting
    assert "partner arrival/replacement `2/25`" in supporting
    assert "+1.9426" in supporting and "+2.0590" in supporting
    assert "cell-level simulation variation" not in lower


def test_main_supp_material_map_matches_current_paper():
    material = MATERIAL_MAP.read_text(encoding="utf-8")
    lower = material.lower()
    assert "conditional response geometry" in lower
    assert "scale-dependent determinant ordering" in lower
    assert "main figure 4 — empirical claim boundary and future validation" in lower
    assert "future/optional validation" in lower
    assert "replace(base, steps=240, trait_adjustment=0.0)" in lower
    assert "75/96" in material
    assert "55.84%" in material and "12.72%" in material
    assert "raw visitor richness or hill diversity is synthetic `k`" in lower
