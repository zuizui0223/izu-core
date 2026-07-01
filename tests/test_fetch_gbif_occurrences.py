import importlib.util
from pathlib import Path

import pytest


def load_script_module():
    path = Path(__file__).parents[1] / "scripts" / "fetch_gbif_occurrences.py"
    spec = importlib.util.spec_from_file_location("fetch_gbif_occurrences", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_gbif_urls_keep_the_declared_taxon_and_coordinate_filter():
    module = load_script_module()

    match = module.species_match_url("Bombus ardens")
    genus_search = module.species_search_url("Ceratina", "GENUS")
    search = module.occurrence_search_url(1234, "JP", 300, 600)

    assert "Bombus+ardens" in match
    assert "Ceratina" in genus_search
    assert "rank=GENUS" in genus_search
    assert "taxon_key=1234" in search
    assert "has_coordinate=true" in search
    assert "country=JP" in search
    assert "limit=300" in search
    assert "offset=600" in search


def test_exact_accepted_genus_fallback_is_auditable(monkeypatch):
    module = load_script_module()
    match_url = module.species_match_url("Ceratina")
    search_url = module.species_search_url("Ceratina", "GENUS")
    responses = {
        match_url: {
            "confidence": 100,
            "note": "Multiple equal matches for Ceratina",
            "matchType": "NONE",
            "synonym": False,
        },
        search_url: {
            "results": [
                {
                    "key": 1342301,
                    "canonicalName": "Ceratina",
                    "scientificName": "Ceratina Jurine, 1807",
                    "rank": "GENUS",
                    "taxonomicStatus": "ACCEPTED",
                },
                {
                    "key": 999,
                    "canonicalName": "Ceratinae",
                    "scientificName": "Ceratinae",
                    "rank": "SUBFAMILY",
                    "taxonomicStatus": "ACCEPTED",
                },
            ]
        },
    }
    monkeypatch.setattr(module, "fetch_json", lambda url: responses[url])

    resolved, resolution, taxon_key, urls = module.resolve_taxon("Ceratina")

    assert taxon_key == 1342301
    assert resolved["usageKey"] == 1342301
    assert resolved["matchType"] == "SPECIES_SEARCH_EXACT_ACCEPTED_GENUS"
    assert resolution["method"] == "species_search_exact_accepted_genus"
    assert resolution["original_species_match"]["matchType"] == "NONE"
    assert urls == [match_url, search_url]


def test_ambiguous_genus_fallback_stops_instead_of_selecting(monkeypatch):
    module = load_script_module()
    match_url = module.species_match_url("Ceratina")
    search_url = module.species_search_url("Ceratina", "GENUS")
    responses = {
        match_url: {"matchType": "NONE"},
        search_url: {
            "results": [
                {
                    "key": 1,
                    "canonicalName": "Ceratina",
                    "rank": "GENUS",
                    "taxonomicStatus": "ACCEPTED",
                },
                {
                    "key": 2,
                    "canonicalName": "Ceratina",
                    "rank": "GENUS",
                    "taxonomicStatus": "ACCEPTED",
                },
            ]
        },
    }
    monkeypatch.setattr(module, "fetch_json", lambda url: responses[url])

    with pytest.raises(ValueError, match="remains ambiguous"):
        module.resolve_taxon("Ceratina")


def test_normalization_retains_candidate_review_status_and_no_effectiveness_claim():
    module = load_script_module()
    row = module.normalize_record(
        {
            "key": 99,
            "scientificName": "Bombus ardens",
            "eventDate": "1985-06-01",
            "decimalLatitude": 34.7,
            "decimalLongitude": 139.3,
            "basisOfRecord": "PRESERVED_SPECIMEN",
            "datasetKey": "dataset",
        },
        "bombus_ardens",
    )

    assert row["review_status"] == "candidate"
    assert row["target_id"] == "bombus_ardens"
    assert row["source_url"].endswith("/99")
    assert "effectiveness" not in row["notes"].lower()
