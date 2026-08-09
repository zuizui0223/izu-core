import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "data" / "design" / "effective_pollinator_dependency_field_readiness.json"


def load_readiness():
    return json.loads(READINESS.read_text(encoding="utf-8"))


def test_field_dependency_design_is_ready_but_empirical_data_are_missing():
    data = load_readiness()
    assert data["status"] == "implementation_ready_field_data_missing"
    assert data["focal_anchor"] == "Campanula microdonta"
    assert data["structural_readiness_only"] is True
    assert data["sample_size_or_power_threshold_locked"] is False


def test_direct_dependency_design_requires_svd_and_three_core_reproductive_treatments():
    channels = load_readiness()["required_linked_channels"]
    assert any("single-visit pollen deposition" in item for item in channels)
    assert "open_pollinated reproductive treatment" in channels
    assert "bagged_autonomous reproductive treatment" in channels
    assert "supplemental_outcross reproductive treatment" in channels
    assert "no-visit SVD controls" in channels


def test_design_does_not_relabel_floral_form_as_dependency():
    data = load_readiness()
    assert "do not assign specialist/generalist classes from floral syndrome labels" in data["comparator_rule"]
    assert "not preassigned from corolla morphology" in data["high_dependency_endpoint_rule"]


def test_claim_boundary_keeps_selfing_and_historical_causation_separate():
    text = load_readiness()["claim_boundary"].lower()
    assert "does not by itself identify historical bombus loss" in text
    assert "self-compatibility" in text
    assert "realized selfing" in text
    assert "causal oshima-toshima boundary effect" in text
