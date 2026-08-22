import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/results/real_data_scale_registry.json"


def load():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def test_current_scale_counts_keep_panels_and_archipelagos_separate():
    data = load()
    counts = data["counts"]
    assert counts["study_panels"] == 10
    assert counts["independent_archipelago_clusters"] == 7
    assert counts["plant_taxa_slots_across_panels"] == 32
    assert set(counts["archipelago_clusters"]) == {"izu", "seychelles", "galapagos", "balearic", "canary", "hawaii", "lesser_antilles"}


def test_new_hawaii_and_dominica_panels_are_present_with_source_native_scale():
    data = load()
    panels = {row["panel_id"]: row for row in data["panels"]}
    hawaii = panels["hawaii_native_pollination_2019"]
    assert hawaii["plant_taxa_slots"] == 8
    assert hawaii["scale"]["raw_rows"] == 4499
    assert hawaii["scale"]["focal_visitor_event_rows"] == 1799
    dominica = panels["dominica_heliconia_2019"]
    assert dominica["scale"] == {"plant_rows": 99, "bird_measurement_rows": 115, "nectar_visit_rows": 23, "post_hurricane_visitor_plant_rows": 56}
    dominica_2013 = panels["dominica_heliconia_2013"]
    assert dominica_2013["plant_taxa_slots"] == 3
    assert dominica_2013["scale"] == {
        "plant_rows": 281,
        "population_year_morph_units": 12,
        "source_selection_models_reconstructed": 12,
    }


def test_evidence_depth_does_not_promote_article_only_hawaii_bagging_to_raw_exclusion():
    data = load()
    counts = data["counts"]
    assert counts["panels_with_pollinator_exclusion_or_bagging_raw"] == 4
    assert counts["panels_with_article_level_dependency_context_only"] == 1
    hawaii = next(row for row in data["panels"] if row["panel_id"] == "hawaii_native_pollination_2019")
    assert "article_level_bagging_context" in hawaii["depth"]
    assert "pollinator_exclusion" not in hawaii["depth"]


def test_no_pseudoreplication_language_is_explicit():
    data = load()
    text = " ".join(data["counting_rules"]) + " " + data["claim_boundary"]
    assert "not independent archipelagos" in text
    assert "not promoted to independent evolutionary replicates" in text
    assert "not an inferential n" in text
    assert "do not substitute for additional independent systems" in text
