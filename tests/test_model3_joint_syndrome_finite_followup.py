import json
from pathlib import Path

from scripts.run_model3_joint_syndrome_finite_followup import _classify


ROOT = Path(__file__).resolve().parents[1]


def test_finite_followup_design_is_frozen_and_complete():
    d = json.loads(
        (ROOT / "data/design/model3_joint_syndrome_finite_followup_20261004.json")
        .read_text()
    )
    assert d["status"] == "frozen_before_joint_selection_outcome_readout"
    assert d["cases"] == 12288
    assert d["demographic_seeds"] == [401, 402, 403, 404]
    assert len(d["initial_states"]) == 3
    assert d["branching"]["split_half_agreement_gate"] == 0.70


def test_endpoint_classes_use_frozen_deadbands():
    assert _classify(-0.05, 0.05) == "syndrome"
    assert _classify(0.05, -0.05) == "outcross"
    assert _classify(-0.049, 0.2) == "intermediate"
    assert _classify(-0.2, 0.049) == "intermediate"
