import json
from pathlib import Path

from scripts.build_island_ecology_submission_bundle import validate_scientific_gate
from scripts.render_chapter2_process_manuscript import render_manuscript as render_submission_manuscript

ROOT = Path(__file__).resolve().parents[1]
UNIFIED_LOCK = ROOT / "data/design/chapter2_unified_model3_lock_20260927.json"


def test_active_submission_is_model3_only():
    text = render_submission_manuscript()
    lower = text.lower()
    assert "evolutionary memory after pollinator isolation does not imply evolutionary arrest" in lower
    assert "exactly the same visitor environment" in lower
    assert "all three plant traits" in lower
    assert "persistent history does not diagnose evolutionary arrest" in lower
    assert "maintained-isolation" in lower
    assert "positive-mutation" in lower
    assert "legacy reduced response-geometry analyses" not in lower


def test_abstract_preserves_denominator_and_claim_ceiling():
    text = render_submission_manuscript()
    abstract = text.split("## Abstract", 1)[1].split("## Keywords", 1)[0]
    words = abstract.split()
    assert 180 <= len(words) <= 300
    lower = abstract.lower()
    assert "64 independent visitor histories" in lower
    assert "eight nested demographic repeats per history" in lower
    assert "4,096 core trajectories" in lower
    assert "evolutionary memory is not equivalent to evolutionary arrest" in lower
    assert "irreversibility" in lower
    assert "not established" in lower


def test_scientific_gate_is_unified_model3():
    lock = json.loads(UNIFIED_LOCK.read_text(encoding="utf-8"))
    assert lock["status"] == "active_chapter2_unified_model3_bridge_complete"
    validated = validate_scientific_gate()
    assert validated["unification_audit"]["decision"] == "model2_not_required_as_active_scientific_model_or_control_gate"
    assert validated["prospective_bridge"]["status"] == "complete"
    assert validated["prospective_bridge"]["cases_verified"] == 24576
    assert validated["submission_state"]["new_field_data_required"] is False
