from pathlib import Path

from scripts.audit_chapter2_nee_submission_v01 import audit


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_NEE_ARTICLE_DRAFT_V0_1_20260915.md"


def test_nee_article_submission_limits():
    result = audit(MANUSCRIPT)
    assert result["abstract_pass"], result
    assert result["main_text_pass"], result
    assert result["display_items_pass"], result
