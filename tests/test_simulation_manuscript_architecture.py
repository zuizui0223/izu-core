import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT / "data/design/simulation_manuscript_results_architecture.json"


def test_manuscript_architecture_keeps_island_ecology_primary():
    arch = json.loads(ARCH.read_text(encoding="utf-8"))
    assert arch["study_type"] == "island_ecology_simulation_with_qualitative_external_island_challenges"
    assert len(arch["main_results"]) == 4
    assert [row["id"] for row in arch["main_results"]] == ["R1_H1", "R2_H2", "R3_H3_H4", "R4_H5"]
    assert [f["figure"] for f in arch["main_figures"]] == ["Fig1", "Fig2", "Fig3", "Fig4"]
    assert arch["core_story"] == "docs/ISLAND_ECOLOGY_CORE_STORY_20260824.md"
    assert arch["hypothesis_recovery"] == "data/design/island_ecology_hypothesis_recovery_20260824.json"
    assert arch["primary_manuscript"] == "docs/ISLAND_ECOLOGY_MANUSCRIPT_DRAFT_20260824.md"
    assert arch["legacy_ecology_first_draft"] == "docs/SIMULATION_MANUSCRIPT_DRAFT_20260824.md"
    assert arch["manuscript_end_state"] == "H1_H5_island_ecology_primary_manuscript_assembled_and_ready_for_frozen_result_validation"
    assert "universal post-establishment" in arch["primary_claim"]
    assert arch["main_results"][0]["question"].startswith("Does a common island-like pollinator functional perturbation")
    assert arch["main_results"][3]["question"].startswith("Does this response-state diversity recur across independent island")

    supporting = {row["id"]: row for row in arch["supporting_results"]}
    assert supporting["S1_state_separability"]["role"] == "inference_guard_and_supplement_not_primary_novelty"
    assert supporting["S2_starting_state_morphology_recurrence"]["role"] == "supporting_context_not_direct_pollinator_matching_validation"

    assert arch["main_tables"][1]["source"] == "data/design/simulation_manuscript_external_system_reference_matrix.json"
    assert "state-separability sensitivity specificity and inverse-identification diagnostics" in arch["supplement"]
    assert "pre-v12 starting-state morphology recurrence with measurement-error and EIV boundaries" in arch["supplement"]
    assert "claim that all islands follow one reproductive syndrome after establishment" in arch["explicit_exclusions_from_primary_results"]
    assert "claim that all thirteen systems share the same empirical causal mechanism" in arch["explicit_exclusions_from_primary_results"]
    assert "state-separability diagnostics as a primary biological result" in arch["explicit_exclusions_from_primary_results"]
    assert "retuning of the Dominica failed mapping" in arch["explicit_exclusions_from_primary_results"]
    assert arch["next_executable_task"].startswith("validate_primary_manuscript_headline_numbers")
