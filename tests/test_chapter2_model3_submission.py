import json
from pathlib import Path

from scripts.build_island_ecology_submission_bundle import validate_scientific_gate
from scripts.render_chapter2_process_manuscript import render_manuscript as render_submission_manuscript

ROOT = Path(__file__).resolve().parents[1]
UNIFIED_LOCK = ROOT / "data/design/chapter2_unified_model3_lock_20260927.json"


def test_active_submission_is_model3_only():
    text = render_submission_manuscript()
    lower = " ".join(text.lower().split())
    assert "reproductive assurance can evolve first without causing floral attraction loss under pollinator isolation" in lower
    assert "visitor limitation lowers the return on attraction before plant traits evolve" in lower
    assert "assurance evolution is not required for investment decline" in lower
    assert "lower pollen deficit does not necessarily mean greater viable reproduction" in lower
    assert "legacy reduced response-geometry analyses" not in lower


def test_abstract_preserves_denominator_and_claim_ceiling():
    text = render_submission_manuscript()
    abstract = text.split("## Abstract", 1)[1].split("## Keywords", 1)[0]
    words = abstract.split()
    assert 180 <= len(words) <= 300
    lower = " ".join(abstract.lower().split())
    assert "64 independent visitor histories" in lower
    assert "eight nested demographic repeats per setting" in lower
    assert "8,192 matched fixed-versus-evolving-assurance trajectories" in lower
    assert "temporal precedence is not causal necessity" in lower
    assert "conditional synthetic mechanisms" in lower
    assert "not calibrated reconstructions of natural island histories" in lower


def test_scientific_gate_is_unified_model3():
    lock = json.loads(UNIFIED_LOCK.read_text(encoding="utf-8"))
    assert lock["status"] == "active_chapter2_unified_model3_bridge_complete"
    validated = validate_scientific_gate()
    assert validated["unification_audit"]["decision"] == "model2_not_required_as_active_scientific_model_or_control_gate"
    assert validated["prospective_bridge"]["status"] == "complete"
    assert validated["prospective_bridge"]["cases_verified"] == 24576
    assert validated["submission_state"]["new_field_data_required"] is False
