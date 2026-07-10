from pathlib import Path

import pytest

from channel_id.prediction_contract_lock import (
    CONTRACT_VERSION,
    load_and_validate_shapes,
    validate_contract_bundle,
)

ROOT = Path(__file__).resolve().parent.parent
SHAPE = ROOT / "data/predictive_meta/campanula_channel_shape_v1.csv"
SCENARIO = ROOT / "data/predictive_meta/two_breakpoint_prediction_contract.csv"
IMAGE = ROOT / "data/predictive_meta/public_visual_signature_contract.csv"


def test_frozen_contract_bundle_is_semantically_consistent():
    result = validate_contract_bundle(SHAPE, SCENARIO, IMAGE)
    assert result.version == CONTRACT_VERSION
    assert result.shape_rows == 6
    assert result.scenario_rows_checked == 6
    assert result.image_rows_checked == 4


def test_visible_signal_is_not_promoted_to_campanula_empirical_calibration():
    shapes = load_and_validate_shapes(SHAPE)
    row = shapes[("campanula_calibration", "specialist", "visible_signal")]
    assert row["evidence_status"] == "blocked_unmeasured"
    assert row["large_to_ardens"] == "not_scored"
    assert row["ardens_to_no_bombus"] == "not_scored"


def test_contract_drift_requires_an_explicit_versioned_change(tmp_path):
    changed = SHAPE.read_text(encoding="utf-8").replace(
        "second_transition_step,flat,increase",
        "continuous_erosion,flat,increase",
    )
    path = tmp_path / "changed.csv"
    path.write_text(changed, encoding="utf-8")
    with pytest.raises(ValueError, match="locked value drift"):
        validate_contract_bundle(path, SCENARIO, IMAGE)
