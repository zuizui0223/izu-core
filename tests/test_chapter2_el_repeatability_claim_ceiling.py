import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "docs/CHAPTER2_MANUSCRIPT_EL_REPEATABILITY_20261003.md"
POSITIONING = ROOT / "docs/CHAPTER2_EL_REPEATABILITY_POSITIONING_20261003.md"
LOCK = ROOT / "data/design/chapter2_el_repeatability_lock_20261003.json"


def _word_count(text: str) -> int:
    return len(re.findall(r"\\b[\\w–-]+\\b", text))


def _abstract(manuscript: str) -> str:
    return manuscript.split("## Abstract", 1)[1].split("## Keywords", 1)[0].strip()


def _main_without_core_references(manuscript: str) -> str:
    return manuscript.split("# Core references for framing", 1)[0]


def test_el_candidate_keeps_three_inference_levels_separate():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    lower = manuscript.lower()
    assert "## claim hierarchy and simulation inference ceiling" in lower
    assert "model-established result" in lower
    assert "general logical implication" in lower
    assert "empirical prediction" in lower
    assert "within the declared model" in lower
    assert "not an estimate of natural prevalence" in lower
    assert "a recurrent syndrome does not imply recurrent evolutionary trajectories" in lower


def test_el_lock_marks_natural_stage_ordering_as_prediction_not_result():
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    assert lock["active_oikos_submission_replaced"] is False
    assert lock["safe_claim"].startswith("Within the declared Model 3")
    assert "does not, by itself, imply recurrent evolutionary trajectories" in lock["general_logical_implication"]
    assert "If the modeled architecture contributes" in lock["empirical_prediction"]
    assert "natural_prediction_not_result" in lock["claim_levels"]
    prohibited = set(lock["prohibited_claims"])
    assert "natural island systems generally follow the modeled stage ordering" in prohibited
    assert "the model estimates natural prevalence of each evolutionary route" in prohibited
    assert "the model identifies the dominant cause of any named island syndrome" in prohibited


def test_el_candidate_stays_within_declared_compact_format():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    abstract = _abstract(manuscript)
    main = _main_without_core_references(manuscript)
    assert _word_count(abstract) <= 250
    assert _word_count(main) <= 4700


def test_el_positioning_preserves_constructive_not_calibrated_interpretation():
    positioning = POSITIONING.read_text(encoding="utf-8").lower()
    assert "established by simulation" in positioning
    assert "general implication" in positioning
    assert "natural prediction" in positioning
    assert "never convert level 3 into a result" in positioning
    assert "natural branch-frequency estimate" in positioning
