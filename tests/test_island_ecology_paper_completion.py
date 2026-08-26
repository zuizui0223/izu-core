import re
from pathlib import Path

from scripts.build_island_ecology_manuscript_v3 import SOURCE, build_text

ROOT = Path(__file__).resolve().parents[1]
SUPPLEMENT = ROOT / "docs/ISLAND_ECOLOGY_JECOLOGY_SUPPLEMENT_20260824.md"
COVER = ROOT / "docs/ISLAND_ECOLOGY_JECOLOGY_COVER_LETTER_20260824.md"


def manuscript_text() -> str:
    return build_text(SOURCE.read_text(encoding="utf-8"))


def test_completed_manuscript_has_main_display_crossreferences():
    text = manuscript_text()
    for token in ["Fig. 1", "Fig. 2", "Fig. 3", "Fig. 4", "Table 1", "Table 2", "Table 3"]:
        assert token in text
    for token in ["Fig. S1", "Table S1", "Table S2", "Table S3"]:
        assert token in text


def test_completed_manuscript_integrates_h2_analytical_explanation():
    text = manuscript_text()
    assert "sign(Δ reproduction) = sign(Δ service) = sign(Δ functional opportunity)" in text
    assert "downstream transforms preserved response sign" in text
    assert "could not be manufactured downstream" in text


def test_supporting_information_contains_frozen_blocks_and_external_contract():
    text = SUPPLEMENT.read_text(encoding="utf-8")
    for heading in [
        "# Appendix S1. Frozen study architecture and claim boundary",
        "# Appendix S2. Experimental block inventory",
        "# Appendix S7. State-separability diagnostics",
        "# Appendix S8. Strict external island-system challenge",
        "# Appendix S9. Protected falsifications and stop rules",
        "# Appendix S10. Reproducibility map",
    ]:
        assert heading in text
    for token in [
        "## Table S1.",
        "## Table S2.",
        "## Table S3.",
        "0.4167",
        "16/96",
        "11/96",
        "207/216",
        "0/525",
        "Dominica *Heliconia*",
        "Puerto Rico–Mona *Guaiacum sanctum*",
    ]:
        assert token in text


def test_supporting_information_does_not_promote_future_empirical_mapping():
    text = SUPPLEMENT.read_text(encoding="utf-8").lower()
    assert "does not claim that one synthetic mechanism has been empirically identified in every island system" in text
    assert "not post-hoc equivalent" in text
    assert "not prevalence estimates" in text
    assert "no new simulation" in text


def test_cover_letter_is_ecology_first_and_keeps_failure():
    text = COVER.read_text(encoding="utf-8")
    lower = text.lower()
    assert "Journal of Ecology" in text
    assert "aggregate island syndromes can coexist with lineage-level branching" in text
    assert "failed signed-position prediction" in lower
    assert "method-first" not in lower
    assert "state-separability" not in lower
    assert "[Corresponding author name]" in text


def test_completed_manuscript_abstract_and_scale():
    text = manuscript_text()
    abstract = text.split("## Abstract", 1)[1].split("**Keywords:**", 1)[0]
    words = re.findall(r"\b[\w’'-]+\b", abstract)
    assert len(words) <= 350
    assert "5. **Synthesis.**" in abstract
    whole = re.findall(r"\b[\w’'-]+\b", text)
    assert 3000 < len(whole) < 8000
