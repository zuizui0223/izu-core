import json
from pathlib import Path

from scripts.render_simulation_manuscript_fig1_svg import write as write_fig1

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "docs/SIMULATION_MANUSCRIPT_RESULTS_FROZEN_20260824.md"
TRACE = ROOT / "data/design/simulation_manuscript_methods_traceability.json"
FALSIFICATION = ROOT / "data/results/simulation_manuscript_falsification_table_frozen.json"
LAYOUT = ROOT / "data/design/simulation_manuscript_figure_layout_v1.json"


def test_final_results_prose_preserves_core_frozen_numbers_and_boundary():
    text = RESULTS.read_text(encoding="utf-8")
    for token in [
        "0.4167",
        "16 of 96",
        "11 of 96",
        "207 of 216",
        "0 of 525",
        "44 paired lineage sign changes",
        "54 geographic/system units",
        "13 strict external systems",
        "11 are generative state challenges",
        "retained falsification"
    ]:
        assert token in text
    assert "complete without new field data" in text
    assert "one mechanism has been empirically identified across 13 island systems" in text


def test_methods_traceability_points_only_to_existing_repository_files():
    trace = json.loads(TRACE.read_text(encoding="utf-8"))
    assert trace["primary_study_boundary"]["field_data_required"] is False
    assert trace["primary_study_boundary"]["system_specific_retuning_allowed"] is False
    file_keys = {
        "implementation", "result_anchor", "frozen_result", "freeze", "provenance",
        "initial_result", "independent_result", "broadened_result", "global_screen",
        "strict_gate", "figure_data_exporter", "figure_data", "figure_renderer_2_to_4",
        "falsification_table"
    }
    checked = 0
    for section in trace["sections"]:
        for key, value in section.items():
            if key not in file_keys:
                continue
            values = value if isinstance(value, list) else [value]
            for path_value in values:
                assert (ROOT / path_value).exists(), path_value
                checked += 1
    assert checked >= 20


def test_falsification_table_keeps_failures_and_future_miss_rule():
    table = json.loads(FALSIFICATION.read_text(encoding="utf-8"))
    rows = {row["claim_id"]: row for row in table["rows"]}
    assert len(rows) == 5
    assert rows["F1_minimal_branch_generator"]["status"] == "survives_two_independently_seeded_frozen_blocks"
    assert rows["F2_universal_network_buffer"]["status"] == "rejected"
    assert rows["F3_assurance_strong_sign_buffer"]["status"] == "rejected"
    assert rows["F4_dominica_signed_position_mapping"]["status"] == "failed_and_retained"
    assert rows["F4_dominica_signed_position_mapping"]["retuning_allowed"] is False
    assert rows["F5_future_state_space_coverage"]["if_triggered"].startswith("record_state_space_miss")


def test_final_figure_layout_has_four_distinct_main_figures_and_fig1_renders(tmp_path: Path):
    layout = json.loads(LAYOUT.read_text(encoding="utf-8"))
    figures = layout["main_figures"]
    assert [row["figure"] for row in figures] == ["Fig1", "Fig2", "Fig3", "Fig4"]
    assert len({row["role"] for row in figures}) == 4
    for row in figures:
        assert (ROOT / row["renderer"]).exists()
    output = write_fig1(tmp_path / "Fig1_frozen_model_logic.svg")
    content = output.read_text(encoding="utf-8")
    assert content.startswith("<svg")
    assert "initial functional-position heterogeneity OFF" in content
    assert "sign rescue: 16 / 96" in content
    assert "0 / 216; 0 / 525" in content
    assert "not a prevalence sample" in content
    assert "does not imply one shared empirical mechanism" in content
