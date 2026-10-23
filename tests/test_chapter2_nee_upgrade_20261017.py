"""The NEE upgrade is ONE active developing article, not a new submitted result."""
import json
import shutil

import pytest

from scripts.validate_chapter2_nee_upgrade_20261017 import (
    ROOT, ROUTE, OLD, SOURCE_CASES,
    NEEUpgradeMismatch, validate,
)


def isolate(tmp_path):
    items = [ROUTE, OLD,
             "docs/CHAPTER2_UNIFIED_NEE_ARTICLE_WORKING_20261017.md",
             *SOURCE_CASES.values()]
    for rel in items:
        dst = tmp_path / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / rel, dst)
    return tmp_path


def test_single_nee_route_and_original_results_are_not_promoted():
    result = validate()
    assert result["status"] == "PASS_EDITORIAL_NEE_DEVELOPMENT_ONLY"
    assert result["article_type"] == "Article"
    assert result["journal_target"] == "Nature Ecology & Evolution"
    assert result["effective_active_paper_count"] == 1
    assert 100 < result["source_abstract_whitespace_words"] <= 200
    assert 700 <= result["source_main_whitespace_words_excluding_online_methods"] <= 3500
    assert result["planned_display_figures"] == 6
    assert result["old_el_renderer_is_historical_only"] is True
    assert result["restoration_experiment_executed"] is False
    assert result["external_island_prediction_confirmed"] is False
    assert result["submission_ready"] is False


def test_cannot_claim_submission_readiness_without_new_evidence(tmp_path):
    root = isolate(tmp_path)
    path = root / ROUTE
    d = json.loads(path.read_text(encoding="utf-8"))
    d["ready_for_nee_submission"] = True
    path.write_text(json.dumps(d), encoding="utf-8")
    with pytest.raises(NEEUpgradeMismatch, match="unrun recoverability"):
        validate(root)


def test_source_inconclusive_registered_Q2_cannot_be_promoted(tmp_path):
    root = isolate(tmp_path)
    path = root / SOURCE_CASES["q2"]
    d = json.loads(path.read_text(encoding="utf-8"))
    d["registered_inference"]["result"] = "both_confirmed"
    path.write_text(json.dumps(d), encoding="utf-8")
    with pytest.raises(NEEUpgradeMismatch, match="384-source"):
        validate(root)


def test_future_recoverability_cannot_be_made_up(tmp_path):
    root = isolate(tmp_path)
    path = root / "docs/CHAPTER2_UNIFIED_NEE_ARTICLE_WORKING_20261017.md"
    s = path.read_text(encoding="utf-8")
    path.write_text(s.replace("**NOT EXECUTED.**", "**RESULT SUPPORTED.**"),
                    encoding="utf-8")
    with pytest.raises(NEEUpgradeMismatch, match="unobserved main recoverability"):
        validate(root)


def test_seventh_main_figure_is_rejected(tmp_path):
    root = isolate(tmp_path)
    path = root / "docs/CHAPTER2_UNIFIED_NEE_ARTICLE_WORKING_20261017.md"
    s = path.read_text(encoding="utf-8")
    insertion = "7. **Figure 7, post-hoc extra** — invalid extra display item.\n"
    path.write_text(s.replace("## Data accessibility",
                              insertion + "\n## Data accessibility"),
                    encoding="utf-8")
    with pytest.raises(NEEUpgradeMismatch, match="display figure cap"):
        validate(root)


def test_old_el_original_route_is_not_removed(tmp_path):
    root = isolate(tmp_path)
    (root / OLD).unlink()
    with pytest.raises(FileNotFoundError):
        validate(root)


def test_historical_pending_proposals_are_retained_but_not_counted_as_article_text():
    """Archived nonexecuted Results are not part of completed NEE Article length."""
    route = json.loads((ROOT / ROUTE).read_text(encoding="utf-8"))
    source = (ROOT / route["active_manuscript"]).read_text(encoding="utf-8")
    intro = "## Introduction"
    pending = "## Planned new decisive Results — PENDING, not observations"
    discussion = "## Discussion"
    methods = "## Online Methods"
    assert source.count(pending) == 1
    preserved = source.split(pending, 1)[1].split(discussion, 1)[0]
    assert "NOT EXECUTED" in preserved
    completed = (source.split(intro, 1)[1].split(pending, 1)[0]
                 + source.split(discussion, 1)[1].split(methods, 1)[0])
    expected = len(completed.split())
    result = validate()
    assert result["source_main_whitespace_words_excluding_online_methods"] == expected
    assert expected <= route["article_guidelines"][
        "main_text_max_words_excluding_abstract_methods_references_figure_legends"]
    assert len(preserved.split()) > 0
