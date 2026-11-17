"""Read-only author-review contracts for the AmNat primary paper/JEB fallback.

Source fidelity and formatting checks only: no simulation, seed replacement,
new statistics, biological inference, data deposit or journal submission.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
AMNAT = DOCS / "CHAPTER2_AMNAT_MAJOR_ARTICLE_DRAFT_20261117.md"
SOURCE = DOCS / "CHAPTER2_NEE_SUPPORTED_RESULTS_ARTICLE_EXTRACT_20261019.md"
SUPP = DOCS / "CHAPTER2_AMNAT_SUPPLEMENT_SOURCE_TABLES_20261117.md"
ROUTE = DOCS / "CHAPTER2_AMNAT_JEB_PUBLICATION_ROUTE_20261117.md"


def contents():
    return (
        AMNAT.read_text(encoding="utf-8"),
        SOURCE.read_text(encoding="utf-8"),
        SUPP.read_text(encoding="utf-8"),
        ROUTE.read_text(encoding="utf-8"),
    )


def section(s: str, start: str, end: str) -> str:
    assert s.count(start) == 1, start
    return s.split(start, 1)[1].split(end, 1)[0].strip()


def test_anonymous_major_article_format_and_identical_source_abstract():
    article, original, _, route = contents()
    assert article.startswith(original.splitlines()[0])
    abstract = section(article, "## Abstract\n", "## Introduction\n")
    source_abstract = section(original, "## Abstract\n", "## Introduction\n")
    assert abstract == source_abstract and len(abstract.split()) == 174
    assert len(abstract.split()) <= 200
    assert article.index("## Introduction\n") < article.index("## Material and Methods\n")
    assert article.index("## Material and Methods\n") < article.index("## Results\n")
    assert article.index("## Results\n") < article.index("## Discussion\n")
    assert article.index("## Discussion\n") < article.index("## Figure Legends\n")
    assert article.index("## Figure Legends\n") < article.index("## Data and Code Accessibility\n")
    assert article.index("## Data and Code Accessibility\n") < article.index("## Literature Cited\n")
    assert "Major Article" in article and "Running head:" in article
    assert "The American Naturalist" in route and "JEB Research Article" in route
    assert "Double anonymous" in route or "double anonymous" in route.lower()
    for identifying in ("zuizui0223", "github.com/zuizui0223", "ZHANG Ruiqi"):
        assert identifying not in article
    assert "not yet double-spaced" in article
    assert "author-approved" in article
    assert "reviewer-accessible" in article


def test_main_length_figures_and_existing_references_unchanged():
    article, original, _, _ = contents()
    main = section(article, "## Introduction\n", "## Data and Code Accessibility\n")
    main_words = len(main.split())
    assert 3000 <= main_words <= 7500
    match = re.search(r"Main-text word count.*?\*\*\s*(\d+)", article)
    assert match and int(match.group(1)) == main_words
    captions = section(article, "## Figure Legends\n", "## Data and Code Accessibility\n")
    numbered = re.findall(r"(?m)^\d+\. Figure ([1-6]),", captions)
    assert numbered == [str(i) for i in range(1, 7)]
    for cap in re.findall(r"(?m)^\d+\. Figure [1-6],.*$", captions):
        assert len(cap.split()) <= 100, cap[:90]
    source_dois = set(re.findall(r"https://doi\.org/([^\s)]+)", original))
    review_dois = set(re.findall(r"https://doi\.org/([^\s)]+)", article))
    assert len(source_dois) == 37
    assert review_dois == source_dois
    assert "## Literature Cited" in article


def test_critical_policy_and_negative_endpoints_are_explicit():
    article, _, supplement, _ = contents()
    pilot = (
        "17/32 native versus 1/32 pooled",
        "P=0.000145",
        "15 native histories only assurance",
    )
    for token in pilot:
        assert token in article, token
    for token in (
        "all-four-settings generality decision",
        "inconclusive",
        "−0.0219",
        "−0.0367",
        "+8.33 percentage points",
        "+92.71",
        "24/32",
        "4/32",
        "Founder",
    ):
        assert token in article or token in supplement, token
    assert "both_inconclusive" in supplement
    assert "25,600 independent founders" in article
    assert "do not establish" in article or "not a causal" in article
    assert "external deposit" in article and "No complete external deposit" in article


def test_blinded_supplement_preserves_cohort_units_and_no_repository_owner():
    article, _, supplement, route = contents()
    assert "## Supplementary Table S1." in supplement
    assert "Supplementary Table S1" in article
    assert "25,600 crossed source cells" in supplement
    assert "private maternal-return" in supplement.lower()
    assert "no new" not in supplement.lower() or "not new analyses" in supplement.lower()
    assert "zuizui0223" not in supplement
    assert "double anonymous" in route.lower()
    assert "not simultaneous submissions" in route.lower()
    assert "HOLD / NO DISPATCH" in route
