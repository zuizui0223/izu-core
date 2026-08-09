import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "predictive_meta" / "hiraiwa_ushimaru_matching_to_pollen.json"


def load_data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_source_figure_has_positive_matching_to_pollen_direction():
    source = load_data()["source_native_model"]
    assert source["source_figure_tm_coefficient"] == 0.04865
    assert source["source_figure_intercept"] == -0.22128
    assert "TM_z * tube" in source["source_candidate_formula"]
    assert "FG_pla_z * tube" in source["source_candidate_formula"]


def test_plant_site_season_aggregation_avoids_flower_pseudoreplication():
    data = load_data()
    assert "plant x site x season" in data["aggregation_unit"]
    all_sites = data["fixed_effect_subsets"]["all_eight_sites"]
    assert all_sites["n_cells"] == 124
    assert all_sites["n_plants"] == 10
    assert all_sites["tm_coefficient"] > 0


def test_mean_matching_to_pollen_direction_is_positive_in_all_geographic_subsets():
    subsets = load_data()["fixed_effect_subsets"]
    assert subsets["mainland_three_sites"]["tm_coefficient"] > 0
    assert subsets["izu_five_islands"]["tm_coefficient"] > 0
    assert subsets["post_oshima_four_islands"]["tm_coefficient"] > 0


def test_downstream_link_is_weaker_than_fdq_matching_and_not_leave_one_island_stable():
    sensitivity = load_data()["leave_one_site_sensitivity"]
    islands = sensitivity["izu_five_islands"]
    post = sensitivity["post_oshima_four_islands"]
    assert islands["all_positive"] is False
    assert post["all_positive"] is False
    assert islands["tm_coefficient_range"][0] < 0 < islands["tm_coefficient_range"][1]
    assert post["tm_coefficient_range"][0] < 0 < post["tm_coefficient_range"][1]
    assert "materially less robust" in load_data()["mechanistic_reading"]


def test_no_mediation_or_historical_causal_claim_is_allowed():
    data = load_data()
    assert "not a mediation analysis" in data["claim_boundary"]
    assert "Time-varying environment" in data["claim_boundary"]
    assert "Do not infer" in data["claim_boundary"]
    assert "uniform reproductive response" in data["relation_to_response_heterogeneity"]
