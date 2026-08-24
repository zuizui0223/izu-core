import json
from pathlib import Path

from scripts.render_island_ecology_external_figures_svg import render_all as render_external
from scripts.render_simulation_manuscript_fig1_svg import render as render_fig1

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / "data/design/simulation_manuscript_figure_layout_v1.json"


def test_main_figure_layout_is_ecology_first():
    layout = json.loads(LAYOUT.read_text(encoding="utf-8"))
    assert layout["study_type"] == "island_ecology_simulation_with_qualitative_external_island_challenges"
    assert [row["figure"] for row in layout["main_figures"]] == ["Fig1", "Fig2", "Fig3", "Fig4"]
    fig4 = layout["main_figures"][3]
    assert fig4["role"] == "external_island_ecological_synthesis"
    assert fig4["renderer"] == "scripts/render_island_ecology_external_figures_svg.py"
    assert fig4["output"] == "Fig4_cross_island_response_architecture.svg"
    assert layout["main_tables"][1]["source"] == "data/design/simulation_manuscript_external_system_reference_matrix.json"
    assert layout["supplement_figures"][0]["figure"] == "FigS1"
    assert layout["supplement_figures"][0]["role"] == "supporting_inference_guard"
    main_text = json.dumps(layout["main_figures"]).lower()
    assert "inverse_problem" not in main_text
    assert "diagnostic asymmetry" not in main_text
    assert "state-separability" not in main_text


def test_fig1_ends_in_cross_island_ecology_not_inverse_problem():
    content = render_fig1()
    assert "Island ecological response architecture" in content
    assert "Cross-island ecological challenge" in content
    assert "13 strict systems" in content
    assert "3 branching / 6 propagation / 2 buffering-alternative" in content
    assert "Inverse problem" not in content
    assert "high-specificity" not in content


def test_external_renderer_separates_main_fig4_from_supplement(tmp_path: Path):
    paths = render_external(tmp_path)
    assert [path.name for path in paths] == [
        "Fig4_cross_island_response_architecture.svg",
        "FigS1_state_separability.svg",
    ]

    fig4 = paths[0].read_text(encoding="utf-8")
    assert "Cross-island recurrence of response states" in fig4
    assert "Izu multi-taxon" in fig4
    assert "Dominica Heliconia" in fig4
    assert "retained falsification" in fig4
    assert "strict challenge set, not a prevalence sample" in fig4
    assert "mixed_sign_branching_for_trait_heterogeneity" not in fig4
    assert "false-positive" not in fig4

    figs1 = paths[1].read_text(encoding="utf-8")
    assert "State-separability diagnostics" in figs1
    assert "mixed_sign_branching_for_trait_heterogeneity" in figs1
    assert "false-positive" in figs1
