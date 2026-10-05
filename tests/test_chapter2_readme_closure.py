from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


def test_readme_separates_current_process_work_from_historical_bridge():
    text = README.read_text(encoding="utf-8")
    lower = text.lower()
    assert "the older oikos bridge submission is a historical snapshot" in lower
    assert "positive-mutation genotype-grid fidelity remains unresolved" in lower
    assert "docs/chapter2_process_mainline_20261005.md" in lower
    assert "all 13,312 cases" in lower
    assert "24,576 computational cases" in lower
    assert "128 independent visitor histories" in lower
    assert "docs/chapter2_manuscript_active_20260831.md" in lower
    assert "docs/chapter2_canonical_story_20260927.md" in lower
    assert "docs/chapter1_chapter2_canonical_bridge_20260927.md" in lower
    assert "data/design/chapter2_unified_model3_lock_20260927.json" in lower
    assert "evolutionary sequence and finite realization" in lower


def test_readme_demotes_all_retired_routes():
    lower = README.read_text(encoding="utf-8").lower()
    assert "legacy/model2/" in lower
    assert "legacy/routes/nee/" in lower
    assert "legacy/routes/ecology-letters/" in lower
    assert "legacy files must not be cited as current manuscript surfaces" in lower
