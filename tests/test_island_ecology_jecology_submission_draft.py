import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md"


def _abstract(text: str) -> str:
    return text.split("## Abstract", 1)[1].split("**Keywords:**", 1)[0]


def test_jecology_submission_has_numbered_abstract_and_synthesis():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    abstract = _abstract(text)
    numbered = re.findall(r"(?m)^([1-9])\. ", abstract)
    assert numbered == ["1", "2", "3", "4", "5"]
    assert "5. **Synthesis.**" in abstract
    words = re.findall(r"\b[\w’'-]+\b", abstract)
    assert len(words) <= 350


def test_jecology_submission_is_anonymous_and_has_review_code_statement():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    lower = text.lower()
    assert "## Data and code for peer review" in text
    assert "anonymized review archive" in lower
    assert "zuizui0223" not in lower
    assert "github.com" not in lower
    assert "@" not in text
    assert "affiliation" not in lower


def test_jecology_submission_keeps_ecology_first_sections():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    sections = [
        "# Introduction",
        "# Materials and Methods",
        "# Results",
        "# Discussion",
        "# Conclusion",
        "# References",
    ]
    positions = [text.index(section) for section in sections]
    assert positions == sorted(positions)
    assert "The inverse problem is the main methodological result" not in text
    assert "state-separability" not in _abstract(text).lower()


def test_jecology_submission_preserves_frozen_headline_results():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    for token in [
        "0.4167",
        "105 of 288",
        "16/96",
        "85/96",
        "11/96",
        "207/216",
        "525",
    ]:
        assert token in text

    assert "three branching" in text
    assert "six same-direction propagation" in text
    assert "two buffering" in text
    assert "one reproductive-axis-decoupling constraint" in text
    assert "one retained falsification" in text
    assert "All 11 generative challenges" in text


def test_jecology_submission_preserves_external_claim_boundaries():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    lower = text.lower()
    assert "not a random sample" in lower or "not a prevalence" in lower
    assert "does not establish one shared empirical mechanism" in lower
    assert "Puerto Rico–Mona *Guaiacum*" in text
    assert "reproductive-axis-decoupling" in text
    assert "Dominica *Heliconia*" in text
    assert "not retuned" in text
    assert "None requires reopening the frozen simulation programme before submission" in text


def test_jecology_submission_contains_source_controlled_citations_and_references():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    for citation in [
        "Grossenbacher et al., 2017",
        "Zell et al., 2025",
        "Bascompte & Scheffer, 2023",
        "Hiraiwa & Ushimaru, 2017, 2024",
        "Valido et al., 2019",
        "Anderson et al., 2011",
        "Fumero-Cabán et al., 2022",
        "Temeles et al., 2013",
    ]:
        assert citation in text

    for doi in [
        "10.1111/nph.14534",
        "10.1111/nph.20234",
        "10.1111/1365-2435.14527",
        "10.1098/rspb.2016.2218",
        "10.1038/s41598-019-41271-5",
        "10.1126/science.1199092",
        "10.26786/1920-7603(2022)669",
        "10.1111/jeb.12053",
    ]:
        assert doi in text


def test_jecology_submission_crossreferences_main_and_supplementary_display_items():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    for token in ["Fig. 1", "Fig. 2", "Fig. 3", "Fig. 4", "Table 1", "Table 2", "Table 3", "Fig. S1", "Table S1", "Table S2", "Table S3"]:
        assert token in text


def test_jecology_submission_expands_reproducible_methods_without_new_science():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    for token in [
        "16 factorial cells",
        "eight cells",
        "288 lineage contrasts per cell",
        "seed 90260825",
        "No further seed search was performed",
        "No empirical inputs or Izu target frequencies were loaded",
    ]:
        assert token in text


def test_jecology_submission_stays_within_research_article_scale():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    words = re.findall(r"\b[\w’'-]+\b", text)
    assert len(words) < 8000
    assert len(words) > 3000
