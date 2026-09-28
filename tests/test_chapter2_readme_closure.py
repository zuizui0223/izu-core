from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


def test_readme_routes_to_bridge_complete_model3_state():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert "chapter 2 is scientifically closed at the declared synthetic claim ceiling" in lower
    assert "24,576 computational cases" in lower
    assert "128 independent visitor histories" in lower
    assert "docs/chapter2_manuscript_active_20260831.md" in lower
    assert "docs/chapter2_canonical_story_20260927.md" in lower
    assert "docs/chapter1_chapter2_canonical_bridge_20260927.md" in lower
    assert "data/design/chapter2_unified_model3_lock_20260927.json" in lower
    assert "realized floral evolution" in lower


def test_readme_demotes_all_retired_routes():
    lower = README.read_text(encoding="utf-8").lower()
    assert "legacy/model2/" in lower
    assert "legacy/routes/nee/" in lower
    assert "legacy/routes/ecology-letters/" in lower
    assert "legacy files must not be cited as current manuscript surfaces" in lower
