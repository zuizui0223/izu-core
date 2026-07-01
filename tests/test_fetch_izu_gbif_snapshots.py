import importlib.util
from pathlib import Path

import pytest


def load_module():
    path = Path(__file__).parents[1] / "scripts" / "fetch_izu_gbif_snapshots.py"
    spec = importlib.util.spec_from_file_location("fetch_izu_gbif_snapshots", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def target() -> dict[str, object]:
    return {
        "target_id": "bombus_ardens",
        "scientific_name": "Bombus ardens Smith, 1879",
        "taxon_key": 1340541,
        "expected_rank": "SPECIES",
        "expected_canonical_name": "Bombus ardens",
    }


def test_occurrence_url_keeps_declared_spatial_scope():
    module = load_module()
    geometry = "POLYGON((138.90 32.80, 140.00 32.80, 140.00 35.10, 138.90 35.10, 138.90 32.80))"

    url = module.occurrence_url(1340541, geometry, 300, 600)

    assert "taxon_key=1340541" in url
    assert "country=JP" in url
    assert "has_coordinate=true" in url
    assert "geometry=POLYGON" in url
    assert "offset=600" in url


def test_fetch_target_records_total_and_truncation(monkeypatch):
    module = load_module()
    geometry = "POLYGON((138.90 32.80, 140.00 32.80, 140.00 35.10, 138.90 35.10, 138.90 32.80))"
    taxon_query = module.taxon_url(1340541)
    occurrence_query = module.occurrence_url(1340541, geometry, 1, 0)
    responses = {
        taxon_query: {
            "key": 1340541,
            "taxonomicStatus": "ACCEPTED",
            "rank": "SPECIES",
            "canonicalName": "Bombus ardens",
        },
        occurrence_query: {
            "count": 2,
            "endOfRecords": False,
            "results": [
                {
                    "key": 1,
                    "scientificName": "Bombus ardens",
                    "decimalLatitude": 34.0,
                    "decimalLongitude": 139.0,
                }
            ],
        },
    }
    monkeypatch.setattr(module, "fetch_json", lambda url: responses[url])

    result = module.fetch_target(target(), geometry, max_records=1)

    assert result["reported_total_records"] == 2
    assert result["retrieved_candidate_records"] == 1
    assert result["truncated_by_max_records"]


def test_validate_target_refuses_mismatched_name():
    module = load_module()

    with pytest.raises(ValueError, match="canonical name"):
        module.validate_target(
            target(),
            {
                "key": 1340541,
                "taxonomicStatus": "ACCEPTED",
                "rank": "SPECIES",
                "canonicalName": "Bombus diversus",
            },
        )
