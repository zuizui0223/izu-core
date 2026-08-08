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
    sensitivity = load_data()["fixed_effect_sensitivity"]
    assert sensitivity["n_site_season_rows"] == 40
    assert sensitivity["n_sites"] == 8
    assert sensitivity["n_seasons"] == 5
    assert sensitivity["fdq_coefficient"] > 1.8
    assert sensitivity["r_squared"] > 0.60
    assert "time-invariant site difference" in sensitivity["reading"]


def test_site_centered_association_is_positive():
    sensitivity = load_data()["within_site_model_free_sensitivity"]
    assert sensitivity["site_centered_fdq_tm_correlation"] > 0.30
    assert "above-site-average FDQ" in sensitivity["reading"]


def test_continuous_exposure_is_not_promoted_to_historical_causation():
    data = load_data()
    assert "less confounded with island identity" in data["relation_to_binary_boundary"]
    assert "Observational contemporary association only" in data["claim_boundary"]
    assert "time-varying weather/resources" in data["claim_boundary"]
    assert "does not identify the historical cause" in data["claim_boundary"]
