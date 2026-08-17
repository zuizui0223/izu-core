import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/dominica_heliconia_selection_dryad_source.json"
RESULT = ROOT / "data/results/dominica_heliconia_selection_summary.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_source_xls_is_byte_locked_after_legacy_dryad_recovery():
    config = load(CONFIG)
    assert config["legacy_version_id"] == 23509
    assert config["source_file_lock"]["bytes"] == 71168
    assert config["source_file_lock"]["sha256"] == "0e185cffb902bdae4267a3e2754e1e6d2f9c85f95da0d62ad7c1d712079df30b"


def test_source_native_scale_is_preserved_by_unit():
    result = load(RESULT)
    assert result["scale"] == {
        "plant_rows": 99,
        "plant_years": [2017, 2018],
        "bird_measurement_rows": 115,
        "nectar_visit_rows": 23,
        "post_hurricane_visitor_plant_rows": 56,
    }
    assert "different source-native units" in result["analysis_unit_boundary"]


def test_post_hurricane_raw_alignment_is_stronger_and_negative():
    result = load(RESULT)
    before = result["plant_response_by_year"]["2017"]["raw_alignment"]
    after = result["plant_response_by_year"]["2018"]["raw_alignment"]
    assert after["corolla_vs_seeds_per_plant_pearson"] < -0.6
    assert after["corolla_vs_seeds_per_flower_pearson"] < -0.6
    assert after["corolla_vs_visits_per_hour_per_flower_pearson"] < -0.6
    assert abs(before["corolla_vs_seeds_per_flower_pearson"]) < 0.1


def test_hummingbird_sex_difference_and_post_visitor_corolla_are_retained():
    result = load(RESULT)
    birds = result["hummingbird_morphology_by_period_and_sex"]
    assert birds["Before_Hurricane"]["by_sex"]["Female"]["mean_culmen_mm"] > birds["Before_Hurricane"]["by_sex"]["Male"]["mean_culmen_mm"]
    post = result["post_hurricane_visitor_x_plant_traits"]
    assert post["Male"]["mean_corolla_length_mm"] < post["Female"]["mean_corolla_length_mm"]
    assert post["Male"]["mean_corolla_length_mm"] < post["Unvisited"]["mean_corolla_length_mm"]


def test_source_selection_model_is_not_recreated_from_descriptive_correlations():
    result = load(RESULT)
    assert "not reconstructed" in result["source_level_selection_context"]
    assert "not selection gradients or causal effects" in result["analysis_unit_boundary"]
    assert "does not recreate the primary selection model" in result["claim_boundary"]
