import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT / "data/design/simulation_manuscript_results_architecture.json"


def test_manuscript_architecture_keeps_simulation_story_primary():
    arch = json.loads(ARCH.read_text(encoding="utf-8"))
    assert arch["study_type"] == "simulation_with_qualitative_external_island_challenges"
    assert len(arch["main_results"]) == 5
    assert [f["figure"] for f in arch["main_figures"]] == ["Fig1", "Fig2", "Fig3", "Fig4"]
    assert arch["manuscript_end_state"] == "primary_results_methods_falsification_and_Fig1_to_Fig4_architecture_frozen_without_new_field_data"
    assert arch["final_results_prose"] == "docs/SIMULATION_MANUSCRIPT_RESULTS_FROZEN_20260824.md"
    assert arch["final_methods_prose"] == "docs/SIMULATION_MANUSCRIPT_METHODS_FROZEN_20260824.md"
    assert arch["falsification_table"] == "data/results/simulation_manuscript_falsification_table_frozen.json"
    assert "new field raw bundle requirement" in arch["explicit_exclusions_from_primary_results"]
    assert "retuning of the Dominica failed mapping" in arch["explicit_exclusions_from_primary_results"]
    assert "additional seed search to increase favorable branch-generator frequencies" in arch["explicit_exclusions_from_primary_results"]
