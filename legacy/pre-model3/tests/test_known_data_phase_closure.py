from copy import deepcopy
from pathlib import Path

import pytest

from channel_id.known_data_phase_closure import (
    read_known_data_phase_lock,
    render_known_data_phase_closure_markdown,
    validate_known_data_phase_lock,
)

ROOT = Path(__file__).parents[1]
LOCK_PATH = ROOT / "data" / "known_data_phase_lock.json"


def test_known_data_phase_lock_matches_current_pre_field_source_inventory() -> None:
    lock = read_known_data_phase_lock(LOCK_PATH)
    closure = validate_known_data_phase_lock(lock, ROOT)

    assert closure.phase_id == "izu_pre_field_known_data_closure_2026_07_03"
    assert closure.source_counts == {
        "outcrossing": 17,
        "bagging": 7,
        "flower": 6,
        "guide_constraints": 0,
        "guide_registry_records": 1,
    }
    assert closure.guide_registry_routes == ("not_eligible",)
    assert closure.candidate_rows[0]["scenario"] == "isolation_order"
    assert closure.candidate_rows[1]["scenario"] == "ardens_step_persistence"
    assert any(row["claim_id"] == "KD05" for row in closure.unsupported_claims)


def test_closure_render_exposes_results_and_boundaries() -> None:
    lock = read_known_data_phase_lock(LOCK_PATH)
    closure = validate_known_data_phase_lock(lock, ROOT)
    text = render_known_data_phase_closure_markdown(lock, closure)

    assert "# Pre-field known-data phase closure" in text
    assert "isolation_order" in text
    assert "ardens_step_persistence" in text
    assert "## Claims explicitly not supported" in text
    assert "Nectar-guide loss" in text
    assert "## Freeze rule" in text


def test_source_count_change_requires_explicit_new_phase() -> None:
    lock = read_known_data_phase_lock(LOCK_PATH)
    changed = deepcopy(lock)
    changed["expected_source_row_counts"]["outcrossing"] = 18

    with pytest.raises(ValueError, match="open a new phase"):
        validate_known_data_phase_lock(changed, ROOT)


def test_lock_rejects_unexpected_candidate_set() -> None:
    lock = read_known_data_phase_lock(LOCK_PATH)
    changed = deepcopy(lock)
    changed["six_candidate_smc"]["candidate_results"][0]["scenario"] = "made_up_model"

    with pytest.raises(ValueError, match="unexpected candidate set"):
        read_known_data_phase_lock_from_object(changed)


def read_known_data_phase_lock_from_object(lock: dict) -> dict:
    """Exercise the same validation through a temporary on-disk JSON fixture."""
    import json
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "lock.json"
        path.write_text(json.dumps(lock), encoding="utf-8")
        return read_known_data_phase_lock(path)
