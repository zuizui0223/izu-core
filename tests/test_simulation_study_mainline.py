import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data/design/simulation_study_mainline_20260824.json"


def test_simulation_primary_claim_has_no_field_blocker():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    assert state["study_type"] == "simulation_with_qualitative_external_challenges"
    assert state["field_data_required_for_primary_claim"] is False
    assert state["empirical_mechanism_mapping_required_for_primary_claim"] is False
    assert state["external_system_role"] == "qualitative_held_out_state_challenge_not_parameter_calibration"
    assert state["active_gate"]["name"] == "main_figure_generation_and_stale_blocker_cleanup"
    assert "collecting_field_data_before_the_primary_simulation_manuscript_is_resolved" in state["not_mainline"]
    assert "requiring_zero_of_twelve_empirical_network_context_mapping_to_be_closed_before_the_simulation_claim" in state["not_mainline"]
