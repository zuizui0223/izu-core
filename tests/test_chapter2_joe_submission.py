from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/JOE_MANUSCRIPT_ANONYMOUS_20261006.md"


def manuscript():
    return MANUSCRIPT.read_text(encoding="utf-8")


def test_joe_structure_and_abstract():
    text = manuscript()
    assert text.startswith(
        "# Reproductive assurance can precede floral investment decline without causing it under pollinator limitation"
    )
    abstract = text.split("## Abstract", 1)[1].split("## Keywords", 1)[0]
    assert len(abstract.split()) <= 350
    assert "**Synthesis.**" in abstract
    for section in [
        "# Introduction",
        "# Materials and Methods",
        "# Results",
        "# Discussion",
        "# Conclusions",
        "# References",
    ]:
        assert text.count(section) == 1


def test_joe_claim_ceiling():
    text = " ".join(manuscript().lower().split())
    assert "51/64" in text
    assert "0.6875–0.890625" in manuscript()
    assert "−0.306021" in manuscript()
    assert "−0.435389" in manuscript()
    assert "30/64" in text
    assert "fixed assurance is not equivalent to zero realized selfing" in text
    assert "not universal" in text
    assert "unresolved high-resolution positive-mutation deterministic/diffusion comparison" in text


def test_joe_anonymous_surface():
    text = manuscript().lower()
    assert "github.com/zuizui0223" not in text
    assert "zhang ruiqi" not in text
    assert "張瑞琪" not in text
