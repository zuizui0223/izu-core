from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_MANUSCRIPT_EL_REPEATABILITY_20261003.md"
SI = ROOT / "docs/CHAPTER2_EL_THEORY_SI_20261004.md"


def _words(text):
    return re.findall(r"\b[\w’'–—.-]+\b", text, flags=re.UNICODE)


def test_el_theory_integration_claim_ceiling_and_format():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    si = SI.read_text(encoding="utf-8")

    abstract = manuscript.split("## Abstract\n\n", 1)[1].split("\n\n## Keywords", 1)[0]
    body = manuscript.split("# Introduction", 1)[1].split("\n# Figure captions", 1)[0]

    assert len(_words(abstract)) <= 300
    assert len(_words(body)) <= 5000

    assert "Price identity" in manuscript
    assert "B(i)-C(i)" in manuscript
    assert "full continuous system is not a PDE" in si
    assert "The third level is not a PDE" in si
    assert "Model 3 is a PDE" not in manuscript
    assert "Model 3 is a PDE" not in si

    assert "Natural variance components" in manuscript
    assert "does not calibrate any named island system" in si


def test_el_theory_integration_uses_corrected_joint_selection_with_claim_ceiling():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    si = SI.read_text(encoding="utf-8")

    assert "w_mut=0.5F_mut+0.5P_mut+S_mut" in manuscript
    assert "post-hoc continuous reduction" in manuscript
    assert "frozen a rare-mutant decision contract" in manuscript
    assert "The frozen follow-up branching criterion failed." in manuscript
    assert "16.4% in the structural delayed-selfing control" in manuscript
    assert "assurance cost produced the marked increase" in manuscript
    assert "0.164" in si and "0.430" in si
    assert "not a causal contrast against this control" in si
    assert "maximum absolute error 7.2e-16" in si
    assert "No setting met the alternative-endpoint branching rule" in si
    assert "purging feedback" in si

    forbidden = [
        "we demonstrate bistability",
        "two stable attractors",
        "universal selfing syndrome",
        "Model 3 is a PDE",
    ]
    for token in forbidden:
        assert token not in manuscript
        assert token not in si
