from scripts.build_island_ecology_review_archive import CORE_REVIEW_FILES, render_submission_manuscript


def test_review_archive_uses_final_oikos_generality_manuscript():
    text = render_submission_manuscript()
    first_line = text.splitlines()[0].lower()
    assert "conditional island responses: from functional matching to finite-population evolutionary realization" in first_line
    assert "fixed-state reproductive assay" in text.lower()
    assert "real islands occupy different stages of the same response architecture" in text.lower()


def test_review_archive_includes_equal_turnover_provenance():
    assert "data/results/chapter2_equal_turnover_control_20260908.json" in CORE_REVIEW_FILES
    assert "scripts/audit_chapter2_equal_turnover_control.py" in CORE_REVIEW_FILES
