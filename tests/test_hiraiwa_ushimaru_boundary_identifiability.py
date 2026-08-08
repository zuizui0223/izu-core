import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data" / "design" / "hiraiwa_ushimaru_boundary_identifiability.json"


def load_design():
    return json.loads(DESIGN.read_text(encoding="utf-8"))


def test_second_boundary_has_only_one_bridge_geographic_unit():
    data = load_design()
    replication = data["second_boundary_independent_site_replication"]
    assert replication["pre_boundary_oshima_like_sites"] == 1
    assert replication["post_boundary_sites"] == 4
    assert data["n_independent_geographic_units"] == {
        "mainland": 3,
        "oshima_bridge": 1,
        "post_boundary": 4,
        "total": 8,
    }


def test_species_and_seasons_are_not_promoted_to_boundary_replicates():
    ident = load_design()["identifiability"]
    assert ident["species_rows_are_independent_boundary_replicates"] is False
    assert ident["season_rows_are_independent_geographic_boundary_replicates"] is False
    assert ident["temporal_variance_estimable_from_repeated_seasons"] is True


def test_descriptive_contrast_is_allowed_but_causal_boundary_effect_is_not_identified():
    ident = load_design()["identifiability"]
    assert ident["descriptive_oshima_vs_post_contrast_estimable"] is True
    assert ident["oshima_site_effect_separable_from_second_boundary_intercept"] is False
    assert ident["causal_second_boundary_effect_identifiable_from_this_dataset_alone"] is False


def test_next_design_gain_requires_geographic_or_temporal_regime_replication():
    data = load_design()
    text = data["next_design_gain"].lower()
    assert "independent geographic replication" in text
    assert "temporal regime transition" in text
    assert "causal boundary effect" in data["consequence"]
