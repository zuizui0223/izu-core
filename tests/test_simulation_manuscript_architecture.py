import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT / "data/design/simulation_manuscript_results_architecture.json"


def test_manuscript_architecture_keeps_island_ecology_primary():
    arch = json.loads(ARCH.read_text(encoding="utf-8"))
    assert arch["study_type"] == "island_ecology_simulation_with_qualitative_external_island_challenges"
    assert len(arch["main_results"]) == 5
    assert [f["figure"] for f in arch["main_figures"]] == ["Fig1", "Fig2", "Fig3", "Fig4"]
    assert arch["core_story"] == "docs/ISLAND_ECOLOGY_CORE_STORY_20260824.md"
    assert arch["primary_manuscript"] == "docs/SIMULATION_MANUSCRIPT_DRAFT_20260824.md"
    assert arch["manuscript_end_state"] == "island_ecology_primary_story_recentered_on_state_dependent_branching_propagation_and_buffering"
    assert "universal post-establishment" in arch["primary_claim"]
    assert arch["main_results"][0]["question"].startswith("Does a common island-like pollinator functional perturbation")
    assert arch["main_results"][3]["question"].startswith("Does this response-state diversity recur across independent island")
    assert arch["main_results"][4]["role"] == "inference_boundary_not_primary_novelty"
    assert arch["main_tables"][1]["source"] == "data/design/simulation_manuscript_external_system_reference_matrix.json"
    assert "state-separability sensitivity specificity and inverse-identification diagnostics" in arch["supplement"]
    assert "claim that all islands follow one reproductive syndrome after establishment" in arch["explicit_exclusions_from_primary_results"]
    assert "claim that all thirteen systems share the same empirical causal mechanism" in arch["explicit_exclusions_from_primary_results"]
    assert "retuning of the Dominica failed mapping" in arch["explicit_exclusions_from_primary_results"]
