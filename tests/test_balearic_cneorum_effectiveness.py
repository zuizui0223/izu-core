import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/balearic_cneorum_effectiveness_summary.json"
CONFIG = ROOT / "config/balearic_cneorum_effectiveness_dryad_source.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_extracted_csvs_are_the_provenance_lock_not_dynamic_zip():
    config = load(CONFIG)
    assert config["package_transport"]["byte_stability"] == "not_assumed"
    locks = config["source_file_locks"]
    assert len(locks) == 7
    assert locks["Exclusions.csv"]["sha256"] == "e3d9763144fae5584673abab0f392a87fdccb99695b21a2e91b5b91ec04f109d"
    assert locks["Pollination_censues_2015_16.csv"]["bytes"] == 52881


def test_real_data_scale_is_locked():
    scale = load(RESULT)["scale"]
    assert scale["pollination_census_rows"] == 373
    assert scale["pollination_census_plants"] == 41
    assert scale["flower_selection_interactions"] == 334
    assert scale["exclusion_pollination_rows"] == 585
    assert scale["breeding_rows_kept_separate"] == 246


def test_lizard_access_adds_reproductive_output_beyond_insect_only():
    result = load(RESULT)
    treatments = result["pollination_exclusion"]["by_source_label"]
    assert treatments["Control"]["weighted_flower_fruit_set"] > treatments["Insects"]["weighted_flower_fruit_set"]
    assert treatments["Control"]["weighted_seeds_per_flower"] > treatments["Insects"]["weighted_seeds_per_flower"]
    contrast = result["pollination_exclusion"]["main_control_vs_insects_only_contrast"]
    assert contrast["insects_only_to_open_weighted_fruit_set_ratio"] < 0.9
    assert contrast["open_minus_insects_only_mean_plant_fruit_set"] > 0.1


def test_lizard_interactions_contact_more_flowers_despite_fewer_census_visits():
    result = load(RESULT)
    census = result["pollination_census"]
    assert census["lizard_visits"] < census["insect_visits"]
    assert census["lizard_flowers_contacted"] > census["insect_flowers_contacted"]
    select = result["flower_selection_interactions"]
    assert select["Lizards"]["mean_flowers_contacted_per_interaction"] > select["Insect"]["mean_flowers_contacted_per_interaction"]
    assert select["Lizards"]["hermaphrodite_fraction_of_contacted_flowers"] > select["Insect"]["hermaphrodite_fraction_of_contacted_flowers"]


def test_seed_dispersal_and_pollination_claims_remain_separate():
    result = load(RESULT)
    assert result["separate_seed_dispersal_context"]["germination_rows"] == 1387
    assert "not mixed into the pollination-effectiveness contrast" in result["separate_seed_dispersal_context"]["reading"]
    assert "not a distinct archipelago from Malva arborea" in result["claim_boundary"]
    assert "not treated as paired plants" in result["analysis_unit_boundary"]
