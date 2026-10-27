"""Source-only guard for the completed Chapter 2 Article's editorial abstract.

No simulation, statistical inference, model import, or submission action.
The historical NEE working manuscript remains a historical source, but its
abstract and the unsent editorial enquiry must agree with the active master.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def _between(content: str, start: str, end: str) -> str:
    assert content.count(start) == 1, f"missing/ambiguous start: {start!r}"
    section = content.split(start, 1)[1]
    assert end in section, f"missing end: {end!r}"
    return section.split(end, 1)[0].strip()


def _abstracts() -> tuple[str, str, str]:
    master = (DOCS / "CHAPTER2_NEE_SUPPORTED_RESULTS_ARTICLE_EXTRACT_20261019.md").read_text(
        encoding="utf-8"
    )
    historical = (DOCS / "CHAPTER2_UNIFIED_NEE_ARTICLE_WORKING_20261017.md").read_text(
        encoding="utf-8"
    )
    enquiry = (DOCS / "CHAPTER2_NEE_SUBMISSION_PREPARATION_20261021.md").read_text(
        encoding="utf-8"
    )
    return (
        _between(master, "## Abstract\n", "## Introduction\n"),
        _between(
            historical,
            "## Abstract — provisional, existing evidence only; NOT for submission\n",
            "## Introduction\n",
        ),
        _between(
            enquiry,
            "The manuscript uses five Results sections and six main figures. "
            "Its abstract follows below.\n\n",
            "\n\nSincerely,",
        ),
    )


def test_exact_source_parity_and_174_word_nee_abstract():
    master, historical, enquiry = _abstracts()
    assert master == historical == enquiry
    assert len(master.split()) == 174
    assert len(master.split()) <= 200


def test_abstract_preserves_registered_vs_exploratory_evidence_ceiling():
    master, _, _ = _abstracts()
    for expected in (
        "Exploratory matched-history analyses",
        "twelve model conditions",
        "40.15% versus 0.36%",
        "these differences do not isolate stochastic drift",
        "Registered experiments showed",
        "8.33 percentage points",
        "92.71-point policy-by-resource interaction",
        "population persistence does not guarantee genetic options",
    ):
        assert expected in master, expected
    assert "neither value quantifies stochastic drift" not in master
    assert "although fixation and inherited variation limit a deterministic interpretation" not in master
    assert "100%" not in master


def test_main_results_are_still_the_five_completed_evidence_sections():
    master = (DOCS / "CHAPTER2_NEE_SUPPORTED_RESULTS_ARTICLE_EXTRACT_20261019.md").read_text(
        encoding="utf-8"
    )
    historical = (DOCS / "CHAPTER2_UNIFIED_NEE_ARTICLE_WORKING_20261017.md").read_text(
        encoding="utf-8"
    )
    m = _between(master, "## Results\n", "## Discussion\n")
    h = _between(
        historical,
        "## Results — existing source-admitted evidence\n",
        "## Planned new decisive Results — PENDING, not observations",
    )
    assert m == h
    assert [line.split(" — ", 1)[0] for line in m.splitlines()
            if line.startswith("### R")] == [
        "### R1", "### R2", "### R3", "### R4", "### R5"
    ]
    assert "registered" in m.lower() and "post-outcome" in m
    assert "## Planned new decisive Results" not in master
