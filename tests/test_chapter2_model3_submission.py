import json
from pathlib import Path

from scripts.build_island_ecology_submission_bundle import validate_scientific_gate
from scripts.render_chapter2_oikos_generality_overlay import render_submission_manuscript

ROOT = Path(__file__).resolve().parents[1]
UNIFIED_LOCK = ROOT / "data/design/chapter2_unified_model3_lock_20260927.json"


def test_active_submission_is_model3_only():
    text = render_submission_manuscript()
    lower = text.lower()
    assert "reproductive selection before demographic change" in lower
    assert "conditional deterministic genotype-density propagation without demographic sampling" in lower
    assert "realized evolution in finite populations" in lower
    assert "annual response-blind richness matching" in lower
    assert "pooling eight independent visitor histories" in lower
    assert "increasing plant capacity from 48 to 192" in lower
    assert "legacy reduced response-geometry analyses" not in lower


def test_abstract_preserves_denominator_and_claim_ceiling():
    text = render_submission_manuscript()
    abstract = text.split("## Abstract", 1)[1].split("## Keywords", 1)[0]
    words = abstract.split()
    assert 180 <= len(words) <= 300
    lower = abstract.lower()
    assert "24,576-case bridge" in lower
    assert "128 independent visitor histories" in lower
    assert "eight demographic repeats nested" in lower
    assert "stable latent branch prevalence" in lower
    assert "source-audited island systems" in lower


def test_scientific_gate_is_unified_model3():
    lock = json.loads(UNIFIED_LOCK.read_text(encoding="utf-8"))
    assert lock["status"] == "active_chapter2_unified_model3_bridge_complete"
    validated = validate_scientific_gate()
    assert validated["unification_audit"]["decision"] == "model2_not_required_as_active_scientific_model_or_control_gate"
    assert validated["prospective_bridge"]["status"] == "complete"
    assert validated["prospective_bridge"]["cases_verified"] == 24576
    assert validated["submission_state"]["new_field_data_required"] is False
