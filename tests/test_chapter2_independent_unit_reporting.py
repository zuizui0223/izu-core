from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_active_manuscript_reports_cases_and_independent_histories_together() -> None:
    text = (ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md").read_text(encoding="utf-8")
    abstract = text.split("## Abstract", 1)[1].split("## Keywords", 1)[0]
    assert "64 independent visitor histories" in abstract
    assert "eight nested demographic repeats per history" in abstract
    assert "4,096 core trajectories" in abstract


def test_canonical_story_keeps_independent_history_denominator_visible() -> None:
    text = (ROOT / "docs/CHAPTER2_CANONICAL_STORY_20260927.md").read_text(encoding="utf-8")
    assert "24,576-case near-versus-far bridge" in text
    assert "128 independent visitor histories" in text


def test_reproduction_guide_explicitly_denies_case_level_independence() -> None:
    text = (ROOT / "REPRODUCE.md").read_text(encoding="utf-8")
    assert "24,576 computational cases" in text
    assert "not independent replicates" in text
    assert "128 independent visitor-history seeds" in text
    assert "do not increase the independent history count" in text
