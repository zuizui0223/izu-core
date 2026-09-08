from scripts.build_island_ecology_review_archive import CORE_REVIEW_FILES, render_submission_manuscript


def test_review_archive_uses_final_oikos_generality_manuscript():
    text = render_submission_manuscript()
    first_line = text.splitlines()[0].lower()
    assert "response geometry under community reorganization: richness-sensitive regimes and state-dependent branching" in first_line
    assert "70/96" in text
    assert "65.61%" in text


def test_review_archive_includes_equal_turnover_provenance():
    assert "data/results/chapter2_equal_turnover_control_20260908.json" in CORE_REVIEW_FILES
    assert "scripts/audit_chapter2_equal_turnover_control.py" in CORE_REVIEW_FILES
