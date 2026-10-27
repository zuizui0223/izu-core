"""Source-only NEE bibliography and manuscript-claim checks (2026-10-27).

These read UTF-8 Markdown only: no network, model updates or new inference.
This is *not* an independent verification of all publisher bibliographic metadata,
and it does not certify author approval or final Nature citation styling.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "docs/CHAPTER2_NEE_SUPPORTED_RESULTS_ARTICLE_EXTRACT_20261019.md"
WORKING = ROOT / "docs/CHAPTER2_UNIFIED_NEE_ARTICLE_WORKING_20261017.md"
BIB_HEADER = "## References — preliminary\n"
DOI = re.compile(r"https://doi\.org/([^\s)]+)", re.IGNORECASE)
YEAR = re.compile(r"\(((?:19|20)\d{2})\)")


def source_and_references():
    source = MASTER.read_text(encoding="utf-8")
    assert source.count(BIB_HEADER) == 1
    body, bibliography = source.split(BIB_HEADER, 1)
    entries = [part.strip() for part in bibliography.split("\n\n") if part.strip()]
    return source, body, entries


def test_all_29_doi_refs_are_unique_and_cited_in_current_manuscript():
    source, body, entries = source_and_references()
    assert len(entries) == 29
    seen = set()
    for entry in entries:
        matches = DOI.findall(entry)
        assert len(matches) == 1, entry[:90]
        doi = matches[0].rstrip(".")
        assert doi.lower() not in seen, doi
        seen.add(doi.lower())
        first_surname = entry.split(",", 1)[0].strip()
        year = YEAR.search(entry)
        assert first_surname and year is not None, entry[:90]
        # Permits et al., & coauthors and "Cheptou (2019; online 2018)"
        # but not a surname in another distant section and an unrelated year.
        cite = re.compile(
            re.escape(first_surname) + r"[^\n\)]{0,100}\b" + year.group(1) + r"\b",
            re.IGNORECASE,
        )
        assert cite.search(body), f"Uncited bibliography entry: {first_surname} {year.group(1)}"
    assert source.count("## Results\n") == 1


def test_five_freshly_cited_primary_sources_and_preprint_status():
    source, body, entries = source_and_references()
    for name, year, doi in (
        ("Bodbyl Roels", "2011", "10.1111/j.1558-5646.2011.01326.x"),
        ("Lande", "1985", "10.1111/j.1558-5646.1985.tb04077.x"),
        ("Lande", "2015", "10.1534/genetics.115.176693"),
        ("Teixido", "2019", "10.1093/aob/mcz014"),
        ("Opedal", "2019", "10.1111/nph.15403"),
        ("Acoca-Pidolle", "2025", "10.32942/X2R93P"),
    ):
        assert doi in source
        assert re.search(re.escape(name) + r"[^\n\)]{0,100}\b" + year + r"\b", body)
    preprint_entry = next(part for part in entries if "10.32942/X2R93P" in part)
    assert "preprint" in preprint_entry.lower()
    assert "preprint" in body.lower() and "irreversibility" in body.lower()


def test_article_word_figures_and_results_remain_source_admitted():
    source, _, _ = source_and_references()
    old = WORKING.read_text(encoding="utf-8")
    abstract = source.split("## Abstract\n", 1)[1].split("## Introduction\n", 1)[0]
    main = source.split("## Introduction\n", 1)[1].split("## Online Methods", 1)[0]
    result = source.split("## Results\n", 1)[1].split("## Discussion\n", 1)[0]
    historical_result = old.split(
        "## Results — existing source-admitted evidence\n", 1
    )[1].split("## Planned new decisive Results — PENDING, not observations", 1)[0]
    assert len(abstract.split()) == 174
    assert 2500 <= len(main.split()) <= 3500
    assert result == historical_result
    assert [int(x) for x in re.findall(r"(?m)^\d+\.\s+\*\*Figure\s+(\d+)", source)] == list(range(1, 7))
    for required in (
        "registered four-setting decision remained inconclusive",
        "8.33 percentage points",
        "92.71 points",
        "post-outcome",
    ):
        assert required in result, required
