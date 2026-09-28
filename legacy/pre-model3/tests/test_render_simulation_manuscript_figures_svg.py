from pathlib import Path

from scripts.render_simulation_manuscript_figures_svg import render_all


def test_svg_renderer_produces_three_manuscript_figures(tmp_path: Path):
    paths = render_all(tmp_path)
    assert [path.name for path in paths] == [
        "Fig2_minimal_branch_generator.svg",
        "Fig3_branch_allocation_buffering_attenuation.svg",
        "Fig4_external_state_identifiability.svg"
    ]
    for path in paths:
        content = path.read_text(encoding="utf-8")
        assert content.startswith("<svg")
        assert content.rstrip().endswith("</svg>")

    fig2 = paths[0].read_text(encoding="utf-8")
    assert "Initial trait OFF" in fig2
    assert "0.417" in fig2

    fig3 = paths[1].read_text(encoding="utf-8")
    assert "network_context" in fig3
    assert "autonomous_assurance" in fig3
    assert "sign rescue 0" in fig3

    fig4 = paths[2].read_text(encoding="utf-8")
    assert "dominica_heliconia" in fig4
    assert "retained failure" in fig4
    assert "mixed_sign_branching_for_trait_heterogeneity" in fig4
