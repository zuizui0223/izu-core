import json
from pathlib import Path

from scripts.export_simulation_manuscript_figure_data import build

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "data/results/simulation_manuscript_figure_data_frozen.json"


def test_figure_data_regenerates_exactly():
    assert build() == json.loads(FROZEN.read_text(encoding="utf-8"))


def test_figure_data_preserves_core_story():
    payload = build()
    fig2 = {row["configuration"]: row for row in payload["fig2_minimal_branch_generator"]}
    assert fig2["full_residual"]["mixed_sign_run_fraction"] > 0
    assert fig2["initial_trait_heterogeneity_off"]["mixed_sign_run_fraction"] == 0
    assert fig2["trait_adjustment_heterogeneity_off"]["mixed_sign_run_fraction"] == fig2["full_residual"]["mixed_sign_run_fraction"]

    fig3 = payload["fig3_branch_allocation_buffering_attenuation"]
    routes = {row["route"]: row for row in fig3["buffering_and_attenuation"]}
    assert routes["network_context"]["sign_rescue_fraction"] > 0
    assert routes["network_context"]["worsening_fraction"] > 0
    assert routes["autonomous_assurance"]["sign_rescue_fraction"] == 0

    fig4 = payload["fig4_external_state_and_identifiability"]
    assert len(fig4["systems"]) == 13
    assert fig4["retained_falsification_system"] == "dominica_heliconia"
    assert payload["external_systems_used_for_parameter_fitting"] is False
