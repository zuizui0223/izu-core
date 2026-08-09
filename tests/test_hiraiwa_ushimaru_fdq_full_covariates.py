import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "predictive_meta" / "hiraiwa_ushimaru_fdq_full_covariates.json"


def load_data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_full_source_functional_predictor_set_is_used():
    data = load_data()
    assert data["source_candidate_predictors"] == ["richness", "D", "FDQ", "FRic", "FEve"]
    assert "richness + D + FDQ + FRic + FEve" in data["model_formula"]
    assert "site_fixed_effects" in data["model_formula"]
    assert "season_fixed_effects" in data["model_formula"]


def test_fdq_remains_positive_with_all_source_functional_covariates():
    subsets = load_data()["subsets"]
    assert subsets["all_eight_sites"]["fdq_coefficient"] > 1.8
    assert subsets["izu_five_islands"]["fdq_coefficient"] > 1.9
    assert subsets["post_oshima_four_islands"]["fdq_coefficient"] > 2.0
    assert subsets["izu_five_islands"]["fdq_partial_r_squared"] > 0.50
    assert subsets["post_oshima_four_islands"]["fdq_partial_r_squared"] > 0.48


def test_full_covariate_fdq_direction_survives_every_island_omission():
    sensitivity = load_data()["leave_one_site_sensitivity"]
    islands = sensitivity["izu_five_islands"]
    post = sensitivity["post_oshima_four_islands"]
    assert islands["all_positive"] is True
    assert post["all_positive"] is True
    assert islands["range"][0] > 1.49
    assert post["range"][0] > 1.20


def test_partial_r2_is_not_causal_variance_attribution():
    text = load_data()["claim_boundary"]
    assert "correlated" in text
    assert "incremental model fit" in text
    assert "rather than variance causally attributable to FDQ" in text
    assert "No coefficient identifies historical pollinator causation" in text
