import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_MANUSCRIPT_JOE_20261006.md"
LOCK = ROOT / "data/design/chapter2_joe_submission_lock_20261006.json"


def test_joe_submission_preserves_confirmed_claim_and_scope():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    normalized = " ".join(text.split())
    lock = json.loads(LOCK.read_text(encoding="utf-8"))

    assert text.startswith("# " + lock["title"])
    assert "51/64" in normalized
    assert "0.6875–0.8906" in normalized
    assert "−0.3060" in normalized
    assert "−0.4354" in normalized
    assert "30/64" in normalized
    assert "not universal" in normalized.lower()
    assert "64 new visitor histories" in normalized
    assert "eight nested demographic repeats" in normalized


def test_joe_abstract_and_structure_match_route():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    abstract = text.split("## Abstract", 1)[1].split("## Keywords", 1)[0]
    words = abstract.split()
    assert len(words) <= 350
    for number in ["1.", "2.", "3.", "4.", "5."]:
        assert number in abstract
    assert "**Synthesis.**" in abstract
    for section in ["# Introduction", "# Materials and Methods", "# Results", "# Discussion", "# Conclusion", "# References"]:
        assert text.splitlines().count(section) == 1


def test_joe_submission_keeps_methodological_overgrowth_out_of_main_text():
    text = MANUSCRIPT.read_text(encoding="utf-8").lower()
    assert "13-rate replenishment" not in text
    assert "positive-mutation high-resolution deterministic/pde comparison" not in text
    assert "finite-versus-deterministic bridge" not in text
    assert "repeatability analyses" in text  # SI routing note only
    assert "fixed-plant reproductive-return assay" in text
