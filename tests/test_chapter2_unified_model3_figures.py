from pathlib import Path

from scripts.generate_chapter2_unified_model3_figures import build_figures

ROOT = Path(__file__).resolve().parents[1]


def test_unified_model3_figure_set_regenerates_from_frozen_results():
    payload = build_figures()
    assert payload["status"] == "unified_model3_bridge_complete_figure_set"
    assert payload["prospective_bridge_result"].endswith("model3_ch2_bridge_prospective_frozen_20260927.json")
    assert payload["real_island_projection"].endswith("chapter2_unified_model3_real_island_projection_20260927.json")
    expected = {
        "figures/chapter2/fig1_unified_model3_nested_levels.svg",
        "figures/chapter2/fig2_model3_prospective_isolation_bridge.svg",
        "figures/chapter2/fig3_model3_history_assurance_connectivity.svg",
        "figures/chapter2/fig4_real_island_abc_confrontation.svg",
    }
    assert expected <= set(payload["figure_outputs"])
    for rel in payload["figure_outputs"]:
        path = ROOT / rel
        assert path.exists() and path.stat().st_size > 1000


def test_figure_roles_match_active_manuscript_story():
    payload = build_figures()
    roles = payload["figure_roles"]
    assert "branch capacity" in roles["figure1"]
    assert "visitor amount" in roles["figure2"]
    assert "history" in roles["figure3"]
    assert "real-island" in roles["figure4"]
