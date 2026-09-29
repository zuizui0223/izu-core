import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/SIMULATION_MANUSCRIPT_DRAFT_MEE_SUBMISSION_20260824.md"
DATA_CODE = ROOT / "docs/SIMULATION_MANUSCRIPT_DATA_CODE_AVAILABILITY_20260824.md"
REFERENCE_MATRIX = ROOT / "data/design/simulation_manuscript_external_system_reference_matrix.json"
REFERENCE_DOC = ROOT / "docs/SIMULATION_MANUSCRIPT_EXTERNAL_SYSTEM_REFERENCES_20260824.md"


def test_mee_submission_abstract_has_exactly_four_numbered_parts():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    abstract = text.split("## Abstract", 1)[1].split("## Data/Code for peer review", 1)[0]
    numbered = re.findall(r"(?m)^([1-9])\. ", abstract)
    assert numbered == ["1", "2", "3", "4"]
    assert "5. " not in abstract


def test_mee_submission_has_peer_review_code_statement_and_at_most_eight_keywords():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert "## Data/Code for peer review" in text
    assert text.index("## Data/Code for peer review") < text.index("**Keywords:**")
    keyword_line = next(line for line in text.splitlines() if line.startswith("**Keywords:**"))
    keywords = [item.strip() for item in keyword_line.split(":", 1)[1].split(";") if item.strip()]
    assert len(keywords) <= 8
    assert len(keywords) == 8


def test_mee_submission_is_anonymous_and_within_standard_article_maximum():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert "zuizui0223" not in text
    assert "github.com/" not in text.lower()
    # Conservative Markdown word count including headings, tables and references.
    words = re.findall(r"\b[\w’'-]+\b", text)
    assert len(words) < 8000
    assert len(words) > 2500


def test_submission_support_files_exist_and_keep_primary_boundary():
    assert DATA_CODE.exists()
    assert REFERENCE_MATRIX.exists()
    assert REFERENCE_DOC.exists()
    data_code = DATA_CODE.read_text(encoding="utf-8")
    assert "requires no new unpublished field dataset" in data_code
    assert "versioned archival DOI" in data_code
