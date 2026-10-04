from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_MANUSCRIPT_EL_REPEATABILITY_20261003.md"
SI = ROOT / "docs/CHAPTER2_EL_THEORY_SI_20261004.md"
FINITE_JOINT = ROOT / "data/results/model3_joint_syndrome_finite_frozen_20261004.json"


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


def test_el_submission_end_matter_is_present_and_human_fields_fail_closed():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    for heading in (
        "# Data and code availability",
        "# Author contributions",
        "# Funding",
        "# Conflict of interest",
        "# Acknowledgements",
    ):
        assert heading in manuscript
    assert "cfa0754823817591fab15ef1b36eecd7a3a3ef10" in manuscript
    assert "**REQUIRES AUTHOR INPUT.** Insert final CRediT roles before submission." in manuscript
    assert "**REQUIRES AUTHOR CONFIRMATION.**" in manuscript
    assert "AI-use disclosure only after the author confirms its exact scope" in manuscript


def test_finite_joint_endpoint_control_contrast_is_not_misread_as_generic_tradeoff_effect():
    import json
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    si = SI.read_text(encoding="utf-8")
    result = json.loads(FINITE_JOINT.read_text(encoding="utf-8"))
    addendum = result["posthoc_control_contrast_interpretation"]

    assert addendum["frozen_adjudication_unchanged"] is True
    assert addendum["structural_control_max_syndrome_frequency"] > addendum["tradeoff_max_syndrome_frequency"]["prior_selfing"]
    assert addendum["tradeoff_max_syndrome_frequency"]["assurance_cost"] > 2 * addendum["structural_control_max_syndrome_frequency"]
    assert "16.4% in the structural delayed-selfing control" in manuscript
    assert "assurance cost produced the marked increase" in manuscript
    assert "not a causal contrast against this control" in si
