import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data/design/simulation_study_mainline_20260824.json"


def test_island_ecology_primary_claim_has_no_field_blocker():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    assert state["study_type"] == "island_ecology_simulation_with_qualitative_external_island_challenges"
    assert state["field_data_required_for_primary_claim"] is False
    assert state["empirical_mechanism_mapping_required_for_primary_claim"] is False
    assert state["external_system_role"] == "comparative_held_out_island_response_state_challenge_not_parameter_calibration"
    assert state["active_gate"]["name"] == "island_ecology_manuscript_reassembly"
    assert state["primary_ecological_contribution"].startswith("a_state_dependent_island_response_model")
    assert state["core_story"] == "docs/ISLAND_ECOLOGY_CORE_STORY_20260824.md"
    assert state["primary_manuscript"] == "docs/SIMULATION_MANUSCRIPT_DRAFT_20260824.md"

    mechanism = state["ecological_mechanism_readout"]
    assert mechanism["branch_generator_independent_replication"] == "replicated_minimal_generator"
    assert mechanism["original_full_mixed_sign_run_fraction"] == 0.4166666666666667
    assert mechanism["independent_full_mixed_sign_run_fraction"] == 0.4166666666666667
    assert mechanism["original_initial_trait_off_mixed_sign_run_fraction"] == 0.0
    assert mechanism["independent_initial_trait_off_mixed_sign_run_fraction"] == 0.0
    assert mechanism["network_context_sign_rescue_count"] == 16
    assert mechanism["network_context_worsening_count"] == 11
    assert mechanism["assurance_attenuation_count"] == 207
    assert mechanism["assurance_sign_rescue_count_independent"] == 0
    assert mechanism["universal_post_establishment_island_syndrome_supported"] is False

    current = state["current_state"]
    assert current["strict_external_systems"] == 13
    assert current["branching_systems"] == 3
    assert current["same_direction_systems"] == 6
    assert current["buffering_or_alternative_systems"] == 2
    assert current["empirical_axis_decoupling_constraints"] == 1
    assert current["retained_falsifications"] == 1

    supporting = state["supporting_method_layer"]
    assert supporting["role"] == "inference_guard_and_supplement_not_primary_scientific_novelty"
    assert state["archived_alternative_framings"]["status"] == "not_current_mainline_method_first_spin_off_only"

    assert "method_first_MEE_framing_as_primary_story" in state["not_mainline"]
    assert "claim_that_all_islands_follow_one_post_establishment_reproductive_syndrome" in state["not_mainline"]
    assert "claim_that_all_thirteen_systems_share_one_empirical_mechanism" in state["not_mainline"]
    assert "collecting_field_data_before_the_primary_simulation_manuscript_is_resolved" in state["not_mainline"]
    assert "retuning_dominica_signed_position_mapping" in state["not_mainline"]
    assert state["next_executable_task"].startswith("freeze_island_ecology_title_abstract_discussion")
