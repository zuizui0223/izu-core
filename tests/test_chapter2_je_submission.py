from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_MANUSCRIPT_JE_20261006.md"


def test_je_manuscript_keeps_confirmed_process_claim_and_scope():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    lower = " ".join(text.lower().split())
    assert text.startswith("# How island isolation generates floral change")
    assert "51/64" in text
    assert "30/64" in text
    assert "−0.3060" in text
    assert "−0.4354" in text
    assert "temporal precedence is not causal necessity" in lower
    assert "not a universal selfing-syndrome sequence" in lower
    assert "fixed assurance blocks assurance evolution but does not remove realized selfing" in lower


def test_je_manuscript_is_submission_length_and_three_figure_mainline():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    main = text.split("# References", 1)[0]
    words = main.split()
    assert len(words) < 8000
    assert text.count("**Figure 1.") == 1
    assert text.count("**Figure 2.") == 1
    assert text.count("**Figure 3.") == 1
    assert "**Figure 4." not in text


def test_je_summary_is_numbered_and_finishes_with_synthesis():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    summary = text.split("## Summary", 1)[1].split("## Keywords", 1)[0]
    for i in range(1, 6):
        assert f"{i}." in summary
    assert "**Synthesis.**" in summary


def test_je_data_availability_does_not_pretend_doi_is_public():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    section = text.split("# Data Availability", 1)[1].split("# Main figures", 1)[0]
    assert "chapter2_1005_confirmatory_primary_sequence_history_20261006.csv" in section
    assert "chapter2_1005_confirmatory_primary_fixed_assurance_history_20261006.csv" in section
    assert "public DOI will be inserted" in section


def test_je_manuscript_has_no_repository_internal_labels():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    main = text.split("# Data Availability", 1)[0]
    assert "Q1" not in main
    assert "Q2" not in main
    assert "bridge-state" not in main
    assert "MODEL3_" not in main
    assert "2026-10-05" not in main
