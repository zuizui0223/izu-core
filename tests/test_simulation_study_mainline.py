import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data/design/simulation_study_mainline_20260824.json"


def test_simulation_primary_claim_has_no_field_blocker():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    assert state["study_type"] == "methodological_simulation_with_qualitative_external_challenges"
    assert state["field_data_required_for_primary_claim"] is False
    assert state["empirical_mechanism_mapping_required_for_primary_claim"] is False
    assert state["external_system_role"] == "worked_held_out_state_challenge_not_parameter_calibration"
    assert state["active_gate"]["name"] == "submission_release_preparation"
    assert state["active_gate"]["required_outputs"] == [
        "anonymized_review_archive",
        "title_page_authorship_and_affiliations",
        "immutable_versioned_code_archive_with_doi",
    ]
    assert state["primary_method_contribution"].startswith("frozen_state_separability_analysis")
    assert state["core_simulation_robustness"]["status"] == "core_simulation_robustness_closed_for_primary_claim"
    assert state["mechanism_readout"]["branch_generator_independent_replication"] == "replicated_minimal_generator"
    assert state["final_results_prose"] == "docs/SIMULATION_MANUSCRIPT_RESULTS_FROZEN_20260824.md"
    assert state["final_methods_prose"] == "docs/SIMULATION_MANUSCRIPT_METHODS_FROZEN_20260824.md"
    assert state["ecology_first_full_draft"] == "docs/SIMULATION_MANUSCRIPT_DRAFT_20260824.md"
    assert state["mee_method_first_draft"] == "docs/SIMULATION_MANUSCRIPT_DRAFT_MEE_20260824.md"
    assert state["mee_submission_draft"] == "docs/SIMULATION_MANUSCRIPT_DRAFT_MEE_SUBMISSION_20260824.md"
    assert state["state_separability_api"] == "channel_id/state_separability.py"
    assert state["journal_strategy"]["first_target"] == "Methods in Ecology and Evolution"
    assert state["journal_strategy"]["no_new_analysis_for_journal_fit"] is True

    validation = state["submission_package_validation"]
    assert validation["pull_request"] == 269
    assert validation["merge_commit"] == "07c67978941f335cecc8a0ba816e2c6157e43d11"
    assert validation["ci"] == "passed_python_3_10_3_11_3_12"
    assert validation["exact_frozen_state_separability_regeneration"] is True
    assert validation["external_reference_matrix_13_systems_validated"] is True
    assert validation["mee_submission_format_guards_validated"] is True

    completed = {row["name"]: row["status"] for row in state["completed_gates"]}
    assert completed["mee_method_first_reframing_and_reusable_state_separability_api"] == "validated"
    assert completed["source_level_13_system_reference_supplement"] == "validated"
    assert completed["mee_standard_article_structure_and_anonymous_peer_review_draft"] == "validated"
    assert completed["data_code_availability_statement"] == "validated"
    assert completed["mee_submission_package_validation"] == "completed"

    assert state["next_executable_task"] == "prepare_submission_time_anonymized_review_archive_title_page_and_versioned_archival_doi_only"
    assert "collecting_field_data_before_the_primary_simulation_manuscript_is_resolved" in state["not_mainline"]
    assert "requiring_zero_of_twelve_empirical_network_context_mapping_to_be_closed_before_the_simulation_claim" in state["not_mainline"]
    assert "rerunning_independent_branch_generator_seeds_until_a_more_favorable_frequency_is_obtained" in state["not_mainline"]
    assert "adding_new_simulation_only_to_make_the_manuscript_story_cleaner" in state["not_mainline"]
    assert "adding_new_simulation_only_to_fit_a_target_journal" in state["not_mainline"]
    assert "reopening_scientific_analysis_during_submission_release_preparation" in state["not_mainline"]
