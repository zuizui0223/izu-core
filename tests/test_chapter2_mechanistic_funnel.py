import json
from pathlib import Path

from scripts.render_chapter2_oikos_generality_overlay import render_submission_manuscript
from scripts.render_chapter2_supporting_information import render_supporting_information

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
NARRATIVE_LOCK = ROOT / "docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md"
CANONICAL_STORY = ROOT / "docs/CHAPTER2_CANONICAL_STORY_20260927.md"
CH1_BRIDGE = ROOT / "docs/CHAPTER1_CHAPTER2_CANONICAL_BRIDGE_20260927.md"
HISTORICAL_THREE_RESULT = ROOT / "docs/CHAPTER2_THREE_RESULT_NARRATIVE_LOCK_20260908.md"
RELATIONAL = ROOT / "data/results/chapter2_relational_robustness_audit_frozen_20260831.json"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260927.json"
MATERIAL_MAP = ROOT / "docs/CHAPTER2_MAIN_SUPP_MATERIAL_MAP_20260907.md"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_active_submission_uses_unified_model3_and_preserves_history():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    narrative = NARRATIVE_LOCK.read_text(encoding="utf-8")
    canonical = CANONICAL_STORY.read_text(encoding="utf-8")
    bridge = CH1_BRIDGE.read_text(encoding="utf-8")
    historical = HISTORICAL_THREE_RESULT.read_text(encoding="utf-8")
    submission = render_submission_manuscript()
    lower = submission.lower()

    assert manuscript.startswith("# Conditional island responses:")
    assert "fixed-state reproductive assay" in lower
    assert "deterministic genotype-density counterpart" in lower
    assert "finite-population abm" in lower
    assert "real islands occupy different stages of the same response architecture" in lower
    assert "all eight shared oshima-to-post targets" in lower
    assert "the main natural-data gap" in lower

    assert "one nested model 3 + completed isolation bridge + layer-specific real-island confrontation" in narrative.lower()
    assert "field e3/e4 remains post-chapter-2 future validation" in narrative.lower()
    assert "visitor amount/richness strongly shifts the coarse mean response" in canonical.lower()
    assert "same island problem, recurrent functions, different realized evolutionary solutions" in bridge.lower()

    # Historical contracts remain readable provenance but are no longer active routing.
    assert historical.startswith("# Chapter 2 three-result narrative lock")
    assert "**mechanistic prediction → real-world compositional exposure → biological consequence**" in historical
    assert "result 1—mechanistic prediction" not in lower
    assert "result 2—real-world exposure" not in lower
    assert "result 3—biological consequence" not in lower


def test_relational_audit_remains_frozen_legacy_not_current_si():
    audit = _load(RELATIONAL)
    assert audit["status"] == "frozen_complete_20260831"
    assert audit["seed_ensemble"]["community_realization_fraction_range"] == [
        0.6933825278526522,
        0.8017383395125494,
    ]
    assert audit["seed_ensemble"]["baseline_seed_is_maximum_community_fraction_in_this_prespecified_ensemble"] is True
    assert all(row["largest_component"] == "community_realization" for row in audit["structural_horizon"])

    submission = render_submission_manuscript().lower()
    assert "legacy reduced response-geometry analyses" not in submission
    supporting = render_supporting_information().lower()
    assert "prespecified relational-robustness audit" not in supporting
    assert (ROOT / "legacy/model2/README.md").is_file()


def test_manifest_routes_bridge_complete_unified_model3_and_real_island_confrontation():
    manifest = _load(MANIFEST)
    assert manifest["journal_target"] == "Oikos"
    assert manifest["fallback_route"] == "Journal of Ecology Research Article"
    assert manifest["scientific_state"] == "unified_model3_bridge_complete_with_real_island_layer_confrontation"
    assert manifest["story"] == "coarse_isolation_regime_to_finite_visitor_and_plant_realization_to_real_island_ABC_confrontation"
    assert manifest["prospective_bridge"]["status"] == "complete"
    assert manifest["prospective_bridge"]["cases_verified"] == 24576
    assert manifest["real_island_confrontation"]["principal_gap"] == "B_inherited_longitudinal_response_under_measured_visitor_regime"
    assert manifest["legacy_model2"]["status"] == "historical_archive_provenance_only"
    assert manifest["legacy_model2"]["included_in_current_supporting_information"] is False
    assert manifest["legacy_model2"]["included_in_current_review_archive"] is False
    assert manifest["legacy_model2"]["active_benchmarks"] == []
    assert manifest["current_submission_state"]["new_field_data_required"] is False
    assert manifest["current_submission_state"]["scientific_question_closed"] is True
    assert manifest["current_submission_state"]["original_chapter2_controls_closed"] is True

def test_supporting_information_retains_current_model3_and_natural_layers_only():
    supporting = render_supporting_information()
    lower = supporting.lower()
    assert "# appendix s1. geography-first saturation and final world synthesis" in lower
    assert "# appendix s2. contemporary izu functional-chain sensitivity" in lower
    assert "# appendix s3. unified model 3 projection onto real-island evidence" in lower
    assert "# appendix s4. prospective model 3 isolation bridge" in lower
    assert "prespecified relational-robustness audit" not in lower
    assert "finite-community system-size audit" not in lower
    assert "same-direction propagation 1" in lower
    assert "0/25` complete a -> b -> c contracts" in lower
    assert "partner arrival/replacement `2/25`" in supporting
    assert "+1.9426" in supporting and "+2.0590" in supporting
    assert "cell-level simulation variation" not in lower
    assert "stable latent branch prevalence" in lower
    assert "separable contributors to realized branching" not in lower


def test_legacy_main_supp_material_map_remains_provenance():
    material = MATERIAL_MAP.read_text(encoding="utf-8")
    lower = material.lower()
    assert "replace(base, steps=240, trait_adjustment=0.0)" in lower
    assert "75/96" in material
    assert "53.53%" in material and "14.05%" in material
    assert "raw visitor richness or hill diversity is **not** synthetic `k`" in lower
