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


def test_active_submission_uses_unified_model3_mainline_and_preserves_history():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    narrative = NARRATIVE_LOCK.read_text(encoding="utf-8")
    historical = HISTORICAL_THREE_RESULT.read_text(encoding="utf-8")
    submission = render_submission_manuscript()
    lower = submission.lower()

    assert manuscript.startswith("# Conditional island responses:")
    assert "fixed-state reproductive assay" in lower
    assert "deterministic genotype-density counterpart" in lower
    assert "finite-population abm" in lower
    assert "real islands occupy different stages of the same response architecture" in lower
    assert "the main natural-data gap" in lower

    assert "one nested model 3" in narrative.lower()
    assert "fixed-state selection" in narrative.lower()
    assert "deterministic genotype distribution" in narrative.lower()
    assert "real-island a/b/c confrontation" in narrative.lower()

    # Historical contracts remain readable provenance but are no longer active routing.
    assert historical.startswith("# Chapter 2 three-result narrative lock")
    assert "**mechanistic prediction → real-world compositional exposure → biological consequence**" in historical
    assert "result 1—mechanistic prediction" not in lower
    assert "result 2—real-world exposure" not in lower
    assert "result 3—biological consequence" not in lower

def test_relational_audit_remains_frozen_legacy_robustness():
    audit = _load(RELATIONAL)
    assert audit["status"] == "frozen_complete_20260831"
    assert audit["seed_ensemble"]["community_realization_fraction_range"] == [
        0.6933825278526522,
        0.8017383395125494,
    ]
    assert audit["seed_ensemble"]["baseline_seed_is_maximum_community_fraction_in_this_prespecified_ensemble"] is True
    assert all(row["largest_component"] == "community_realization" for row in audit["structural_horizon"])

    submission = render_submission_manuscript().lower()
    assert "legacy reduced response-geometry" not in submission
    supporting = render_supporting_information().lower()
    assert "prespecified relational-robustness audit" in supporting

def test_manifest_routes_unified_model3_and_demotes_legacy_model2():
    manifest = _load(MANIFEST)
    assert manifest["journal_target"] == "Oikos"
    assert manifest["fallback_route"] == "Journal of Ecology Research Article"
    assert manifest["narrative_lock"] == "docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md"
    assert manifest["scientific_state"] == "unified_model3_nested_ecoevolutionary_response_with_real_island_layer_confrontation"
    assert manifest["unified_model3"]["legacy_model2_role"] == "supporting_information_and_provenance_only"
    assert manifest["real_island_projection"]["B_layer"] == "principal_inherited_longitudinal_gap"
    assert manifest["claim_ceiling"]["field_e3_e4_required_for_current_paper"] is False

def test_supporting_information_retains_empirical_and_structural_audit_layers():
    supporting = render_supporting_information()
    lower = supporting.lower()
    assert "# appendix s16. prespecified relational-robustness audit" in lower
    assert "# appendix s17. geography-first saturation and final world synthesis" in lower
    assert "# appendix s18. contemporary izu functional-chain sensitivity" in lower
    assert "# appendix s18a. unified model 3 projection onto real-island evidence" in lower
    assert "69.34–80.17%" in supporting
    assert "partner arrival/replacement `2/25`" in supporting
    assert "+1.9426" in supporting and "+2.0590" in supporting
    assert "cell-level simulation variation" not in lower


def test_main_supp_material_map_remains_legacy_provenance():
    material = MATERIAL_MAP.read_text(encoding="utf-8")
    lower = material.lower()
    assert "conditional response geometry" in lower
    assert "replace(base, steps=240, trait_adjustment=0.0)" in lower
    assert "75/96" in material
    assert "raw visitor richness or hill diversity is synthetic `k`" in lower
