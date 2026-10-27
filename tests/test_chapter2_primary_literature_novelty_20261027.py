"""Read-only guards for Chapter 2's expanded external-literature/novelty comparison.

No biological producer, external network call or statistical test is executed.
The new audit cannot promote exploratory metrics or natural-island associations
to registered causal results.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def get_text(name: str) -> str:
    return (DOCS / name).read_text(encoding="utf-8")


def test_current_article_includes_new_primary_context_and_citable_dois():
    s = get_text("CHAPTER2_NEE_SUPPORTED_RESULTS_ARTICLE_EXTRACT_20261019.md")
    refs = s.split("## References — preliminary\n", 1)[1]
    for doi in (
        "10.1111/nph.20234",       # Zell 2025, island colonization filter
        "10.1093/aob/mcaf005",    # Ciarle et al. 2025, pollination-mode floral size
        "10.1111/nph.20373",      # Moir 2025, functional flower/pollinator matching
        "10.1093/evolut/qpag030", # Torres-Vanegas et al. 2026
        "10.1111/nph.71605",      # Acoca-Pidolle et al. 2026
        "10.1093/evlett/qrag026", # Bishop et al. 2026
        "10.1016/j.tree.2026.04.015", # Balstad et al 2026 rescue review
        "10.1016/j.tree.2026.08.010", # Christie et al 2026 rescue types review
        "10.1093/evolut/qpag095", # Deraje and Uecker 2026 stochastic Allee
        "10.1111/nph.70880", # Schoen and Toczydlowski 2026 recovery/genetic diversity
    ):
        assert refs.count(doi) == 1, doi
    intro = s.split("## Introduction\n", 1)[1].split("## Results\n", 1)[0]
    assert "colonization filtering" in intro
    assert "pollination-mode-dependent" in intro
    assert "establishment" in intro
    assert "evolution after arrival" in intro


def test_bounded_novelty_not_universal_trait_determinism():
    s = get_text("CHAPTER2_NEE_SUPPORTED_RESULTS_ARTICLE_EXTRACT_20261019.md")
    d = s.split("## Discussion\n", 1)[1].split("## Online Methods", 1)[0]
    assert "one founder-relative high-I target" in d
    assert "but not different within-survivor census histories" in d
    assert "complete survival excludes differential extinction" in d
    assert "different within-survivor census histories" in d
    assert "no separate M allocation cost" in d
    assert "not natural speciation" in d
    assert "many loci, pleiotropy and genetic covariances" in d
    assert "Retained target support is not general evolvability" in d


def test_results_and_negative_rank_remain_in_place():
    s = get_text("CHAPTER2_NEE_SUPPORTED_RESULTS_ARTICLE_EXTRACT_20261019.md")
    w = get_text("CHAPTER2_UNIFIED_NEE_ARTICLE_WORKING_20261017.md")
    r1 = s.split("## Results\n", 1)[1].split("## Discussion\n", 1)[0]
    r2 = w.split("## Results — existing source-admitted evidence\n", 1)[1].split(
        "## Planned new decisive Results — PENDING, not observations", 1)[0]
    assert r1 == r2
    for token in (
        "registered four-setting decision remained inconclusive",
        "66–111 of 128 histories",
        "103/128 contexts had unanimous",
        "97.622% combined residual",
        "8.33 percentage points",
        "92.71 points",
        "post-outcome",
    ):
        assert token in r1, token
    assert "## Planned new decisive Results" not in s


def test_novelty_review_records_contrary_primary_papers_and_limits():
    d = get_text("CHAPTER2_PRIMARY_LITERATURE_NOVELTY_AUDIT_20261027.md")
    for marker in (
        "non-exhaustive scoping review",
        "Ciarle, Burns & Mologni (2025)",
        "Torres-Vanegas et al. (2026)",
        "Peterson & Kay (2015)",
        "Busch et al. (2022)",
        "Bishop, Stinchcombe & Baucom (2026)",
        "Hartfield & Glémin (2024)",
        "Christie, Fitzpatrick & Searle (2026)",
        "Schoen & Toczydlowski (2026)",
        "MODEL-SPECIFIC DISTINCTIVE REGISTERED RESULT",
        "NOT SHOWN",
        "not a registered systematic review",
    ):
        assert marker.lower() in d.lower(), marker
