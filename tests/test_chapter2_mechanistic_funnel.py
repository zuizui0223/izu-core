import json
from pathlib import Path

from scripts.render_chapter2_oikos_generality_overlay import render_submission_manuscript
from scripts.render_chapter2_supporting_information import render_supporting_information

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
CANONICAL_STORY = ROOT / "docs/CHAPTER2_CANONICAL_STORY_20260927.md"
CH1_BRIDGE = ROOT / "docs/CHAPTER1_CHAPTER2_CANONICAL_BRIDGE_20260927.md"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260927.json"


def test_active_submission_uses_one_model3_ecological_pathway():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    submission = render_submission_manuscript()
    lower = submission.lower()
    assert manuscript.startswith("# From pollination ecology to realized floral evolution")
    assert "reproductive selection before demographic change" in lower
    assert "conditional deterministic genotype-density propagation without demographic sampling" in lower
    assert "realized evolution in finite populations" in lower
    assert "annual response-blind richness matching" in lower
    assert "pooling eight independent visitor histories" in lower
    assert "principal natural-data gap" in lower


def test_canonical_story_and_chapter1_bridge_match_model3_mainline():
    story = CANONICAL_STORY.read_text(encoding="utf-8").lower()
    bridge = CH1_BRIDGE.read_text(encoding="utf-8").lower()
    assert "functional matching + finite pollen transfer" in story
    assert "conditional deterministic inherited trajectory" in story
    assert "stable latent branch frequencies are not identified" in story
    assert "same island problem, recurrent functions, different realized evolutionary solutions" in bridge


def test_manifest_routes_only_current_model3_submission_surface():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["scientific_state"] == "unified_model3_bridge_complete_with_real_island_layer_confrontation"
    assert manifest["prospective_bridge"]["status"] == "complete"
    assert manifest["prospective_bridge"]["cases_verified"] == 24576
    assert manifest["real_island_confrontation"]["principal_gap"] == "B_inherited_longitudinal_response_under_measured_visitor_regime"
    assert manifest["legacy_model2"]["status"] == "historical_archive_provenance_only"
    assert manifest["legacy_model2"]["included_in_current_supporting_information"] is False
    assert manifest["legacy_model2"]["included_in_current_review_archive"] is False


def test_current_supporting_information_is_model3_only():
    lower = render_supporting_information().lower()
    assert "# appendix s1. geography-first saturation and final world synthesis" in lower
    assert "# appendix s2. contemporary izu functional-chain sensitivity" in lower
    assert "# appendix s3. unified model 3 projection onto real-island evidence" in lower
    assert "# appendix s4. prospective model 3 isolation bridge" in lower
    assert "finite-community system-size audit" not in lower
    assert "gaussian mean-field limit" not in lower


def test_density_closure_is_not_stochastic_mean_or_finite_size_target():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8").lower()
    submission = render_submission_manuscript().lower()
    story = CANONICAL_STORY.read_text(encoding="utf-8").lower()
    assert "conditional deterministic closure" in manuscript
    assert "not the stochastic mean" in manuscript
    assert "descriptive only" in manuscript
    assert "conditional deterministic closure" in submission
    assert "not the stochastic mean" in story
    assert "finite-size convergence or attenuation coefficient" in story
