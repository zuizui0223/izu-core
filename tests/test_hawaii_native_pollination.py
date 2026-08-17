import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/hawaii_native_pollination_dryad_source.json"
RESULT = ROOT / "data/results/hawaii_native_pollination_summary.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_source_files_are_locked_after_legacy_package_recovery():
    config = load(CONFIG)
    locks = config["source_file_locks"]
    assert config["legacy_version_id"] == 3740
    assert locks["Pollination visitation obs for dryad.xlsx"] == {
        "bytes": 579979,
        "sha256": "2b0ff40226b2a6d511a111ead8a00660532de3d799aed217e4dc30f00c2b3c27",
    }
    assert locks["README_for_Pollination visitation obs for dryad.docx"]["sha256"] == "8a664206390b498618adc23d460d81d77022e70550c5c74e66bf87eeafe9b6cd"


def test_raw_visitation_scale_is_source_native_and_large():
    result = load(RESULT)
    scale = result["raw_visitation_scale"]
    assert scale["focal_plant_sheets"] == 8
    assert scale["raw_rows"] == 4499
    assert scale["observation_sessions"] == 240
    assert scale["focal_visitor_event_rows"] == 1799
    assert scale["flowers_probed_in_focal_rows"] == 8198.0
    assert result["by_plant"]["Stenogyne angustifolia"]["focal_visitor_event_rows"] == 35
    assert result["by_plant"]["Bidens menziesii"]["focal_visitor_event_rows"] == 542


def test_raw_visitor_labels_are_not_promoted_to_species_richness():
    result = load(RESULT)
    assert result["raw_visitation_scale"]["unique_raw_focal_visitor_labels"] == 197
    assert "spelling/synonym variants" in result["analysis_unit_boundary"]
    assert "not automatically collapsed into species richness" in result["analysis_unit_boundary"]


def test_published_bagging_result_remains_separate_from_raw_package():
    result = load(RESULT)
    context = result["source_reported_context"]
    assert context["flower_observation_hours"] == 576.36
    assert context["reported_non_native_share_of_visits"] == 0.85
    assert context["reported_species_with_significant_seed_set_reduction_under_bagging"] == 6
    assert "does not contain a source-native manual-flower-treatment table" in load(CONFIG)["raw_data_scope"]
    assert "not converted into unobserved raw treatment values" in result["claim_boundary"]
