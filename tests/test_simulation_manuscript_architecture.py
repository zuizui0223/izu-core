import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT / "data/design/simulation_manuscript_results_architecture.json"


def test_manuscript_architecture_keeps_simulation_story_primary():
    arch = json.loads(ARCH.read_text(encoding="utf-8"))
    assert arch["study_type"] == "simulation_with_qualitative_external_island_challenges"
    assert len(arch["main_results"]) == 5
    assert [f["figure"] for f in arch["main_figures"]] == ["Fig1", "Fig2", "Fig3", "Fig4"]
    assert arch["manuscript_end_state"] == "primary_simulation_story_is_ready_for_figure_generation_and_results_prose_without_new_field_data"
    assert "new field raw bundle requirement" in arch["explicit_exclusions_from_primary_results"]
    assert "retuning of the Dominica failed mapping" in arch["explicit_exclusions_from_primary_results"]
