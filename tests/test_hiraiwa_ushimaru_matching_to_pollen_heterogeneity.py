import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data" / "predictive_meta" / "hiraiwa_ushimaru_matching_to_pollen_heterogeneity.json"


def load_result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_cluster_aware_intervals_keep_positive_direction_but_include_zero():
    data = load_result()
    inference = data["site_season_cluster_inference"]
    for subset in (
        "all_eight_sites",
        "mainland_three_sites",
        "izu_five_islands",
        "post_oshima_four_islands",
    ):
        row = inference[subset]
        assert row["tm_coefficient"] > 0
        assert row["interval_95"][0] < 0 < row["interval_95"][1]
        assert row["interval_excludes_zero"] is False


def test_estimable_leave_one_plant_models_do_not_identify_a_single_taxon_driver():
    data = load_result()["omission_localization"]
    for subset in ("izu_five_islands", "post_oshima_four_islands"):
        row = data[subset]["leave_one_plant"]
        assert row["estimable_omissions"] == 9
        assert row["positive_estimable_omissions"] == 9
        assert row["range"][0] > 0
        assert row["non_estimable"] == {
            "Oxalis corniculata var. trichocaulon": "singular design matrix"
        }


def test_post_oshima_fragility_localizes_to_hachijo_season_three():
    data = load_result()["omission_localization"]["post_oshima_four_islands"]
    assert data["leave_one_site"]["negative_when_omitted"] == ["hachijo"]
    assert data["leave_one_season"]["negative_when_omitted"] == [3]
    site_season = data["leave_one_site_season"]
    assert site_season["negative_when_omitted"] == ["hachijo|season_3"]
    assert site_season["coefficient_when_hachijo_season_3_omitted"] < 0
    assert site_season["positive_estimable_omissions"] == 18


def test_oshima_inclusion_buffers_single_network_state_sign_reversal():
    izu = load_result()["omission_localization"]["izu_five_islands"]
    assert izu["leave_one_site_season"]["estimable_omissions"] == 24
    assert izu["leave_one_site_season"]["positive_estimable_omissions"] == 24
    assert izu["leave_one_site_season"]["negative_when_omitted"] == []
    assert izu["leave_one_season"]["negative_when_omitted"] == [3]
    assert izu["leave_one_site"]["negative_when_omitted"] == ["hachijo"]


def test_result_is_not_promoted_to_mediation_or_historical_causation():
    data = load_result()
    assert data["decision_state"] == "directional_positive_but_cluster_uncertain_and_network_state_sensitive"
    assert "not an experimental treatment" in data["claim_boundary"]
    assert "non-estimable" in data["claim_boundary"]
    assert "causal mediation" in data["claim_boundary"]
    assert "historical pollinator-loss causation" in data["claim_boundary"]
