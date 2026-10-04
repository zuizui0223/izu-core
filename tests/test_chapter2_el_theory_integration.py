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


def test_el_theory_integration_keeps_joint_assurance_out_of_locked_main_text():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    # The separate rare-mutant joint-assurance extension remains exploratory
    # until its frozen gates complete.
    forbidden = [
        "rare-mutant joint selection",
        "classic_sign_reversal",
        "joint syndrome selection vector",
    ]
    for token in forbidden:
        assert token not in manuscript
