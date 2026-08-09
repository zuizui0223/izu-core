import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "predictive_meta" / "hiraiwa_ushimaru_continuous_functional_exposure.json"


def load_data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_source_model_has_positive_fdq_trait_matching_coefficient():
    source = load_data()["source_native_model"]
    assert source["source_figure_best_model_fdq_coefficient"] == 1.554
    assert source["source_figure_best_model_feve_coefficient"] == -9.2976
    assert "(1|season)" in source["source_full_candidate_formula"]
    assert "(1|site)" in source["source_full_candidate_formula"]


def test_fdq_direction_persists_with_site_and_season_fixed_effects():
    subsets = load_data()["fixed_effect_subsets"]
    all_sites = subsets["all_eight_sites"]
    assert all_sites["n_site_season_rows"] == 40
    assert all_sites["n_sites"] == 8
    assert all_sites["n_seasons"] == 5
    assert all_sites["fdq_coefficient"] > 1.8
    assert all_sites["r_squared"] > 0.60
    assert all_sites["site_centered_fdq_tm_correlation"] > 0.30


def test_fdq_relationship_does_not_require_mainland_or_oshima():
    subsets = load_data()["fixed_effect_subsets"]
    mainland = subsets["mainland_three_sites"]
    islands = subsets["izu_five_islands"]
    post = subsets["post_oshima_four_islands"]
    assert mainland["fdq_coefficient"] > 1.5
    assert islands["fdq_coefficient"] > 1.9
    assert post["fdq_coefficient"] > 2.0
    assert islands["site_centered_fdq_tm_correlation"] > 0.40
    assert post["site_centered_fdq_tm_correlation"] > 0.34
    assert post["n_sites"] == 4
    assert post["n_site_season_rows"] == 20


def test_island_subset_fdq_direction_survives_every_single_site_omission():
    sensitivity = load_data()["leave_one_site_sensitivity"]
    islands = sensitivity["izu_five_islands"]
    post = sensitivity["post_oshima_four_islands"]
    assert islands["all_positive"] is True
    assert post["all_positive"] is True
    assert islands["fdq_coefficient_range"][0] > 1.4
    assert post["fdq_coefficient_range"][0] > 1.4
    assert set(islands["fdq_coefficients_by_omitted_site"]) == {
        "oshima", "niijima", "kozu", "miyake", "hachijo"
    }
    assert set(post["fdq_coefficients_by_omitted_site"]) == {
        "niijima", "kozu", "miyake", "hachijo"
    }


def test_sampled_post_boundary_network_has_zero_observed_bombus_rows_without_claiming_absence():
    context = load_data()["sampled_bombus_context"]
    assert context["bombus_species_site_season_rows"] == 12
    assert context["bombus_site_seasons"] == 10
    assert context["mainland_bombus_rows"] == 10
    assert context["mainland_bombus_site_seasons"] == 8
    assert context["oshima_bombus_rows"] == 2
    assert context["oshima_bombus_site_seasons"] == 2
    assert context["post_oshima_bombus_rows"] == 0
    assert context["post_oshima_bombus_site_seasons"] == 0
    assert set(context["observed_bombus_taxa"]) == {
        "Bombus ardens ardens", "Bombus diversus diversus"
    }
    assert "not a biological absence assertion" in context["reading"]


def test_continuous_exposure_is_beyond_sampled_bombus_boundary_but_not_bombus_causal_proof():
    data = load_data()
    relation = data["relation_to_binary_boundary"]
    claim = data["claim_boundary"]
    assert "zero observed Bombus" in relation
    assert "binary observed-Bombus label" in relation
    assert "Observational contemporary association only" in claim
    assert "time-varying weather/resources" in claim
    assert "sampled Bombus audit is not an archipelago-wide biological absence statement" in claim
    assert "does not identify Bombus loss as the cause" in claim
    assert "binary sampled-network contrast" in claim
