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
    assert state["active_gate"]["name"] == "full_manuscript_draft_assembly"
    assert state["core_simulation_robustness"]["status"] == "core_simulation_robustness_closed_for_primary_claim"
    assert state["mechanism_readout"]["branch_generator_independent_replication"] == "replicated_minimal_generator"
    assert state["final_results_prose"] == "docs/SIMULATION_MANUSCRIPT_RESULTS_FROZEN_20260824.md"
    assert state["final_methods_prose"] == "docs/SIMULATION_MANUSCRIPT_METHODS_FROZEN_20260824.md"
    assert state["falsification_table"] == "data/results/simulation_manuscript_falsification_table_frozen.json"
    assert state["figure_layout"] == "data/design/simulation_manuscript_figure_layout_v1.json"
    assert "collecting_field_data_before_the_primary_simulation_manuscript_is_resolved" in state["not_mainline"]
    assert "requiring_zero_of_twelve_empirical_network_context_mapping_to_be_closed_before_the_simulation_claim" in state["not_mainline"]
    assert "rerunning_independent_branch_generator_seeds_until_a_more_favorable_frequency_is_obtained" in state["not_mainline"]
    assert "adding_new_simulation_only_to_make_the_manuscript_story_cleaner" in state["not_mainline"]
