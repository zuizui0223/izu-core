from channel_id.guide_photo_review import ReviewBundleConfig, build_review_bundle


def _gbif_candidate(record_id: str, candidate_id: str) -> dict[str, str]:
    return {
        "candidate_id": candidate_id,
        "source_type": "GBIF",
        "record_id": record_id,
        "target_id": "campanula_microdonta",
        "query_taxon_name": "Campanula microdonta Koidz.",
        "observed_taxon_name": "Campanula microdonta Koidz.",
        "observed_on": "2024-07-29",
        "latitude": "33.11",
        "longitude": "139.79",
        "positional_accuracy_m": "40",
        "quality_grade": "HUMAN_OBSERVATION",
        "media_index": "1",
        "photo_url": f"https://images.example/{candidate_id}.jpg",
        "observation_source_url": f"https://www.gbif.org/occurrence/{record_id}",
        "nearest_declared_proxy": "Hachijo",
        "nearest_proxy_distance_km": "4",
        "second_nearest_declared_proxy": "Miyake",
        "second_nearest_proxy_distance_km": "46",
        "nearest_proxy_gap_km": "42",
    }


def test_source_specific_quality_gate_and_record_identity_are_preserved() -> None:
    rows = [_gbif_candidate("77", "one"), _gbif_candidate("77", "two")]
    config = ReviewBundleConfig(allowed_quality_grades=("HUMAN_OBSERVATION",), seed=4)

    geographic, trait_a, trait_b, key = build_review_bundle(rows, config)

    assert len(geographic) == 1
    assert geographic[0]["source_type"] == "GBIF"
    assert geographic[0]["observation_unit_id"] == "gbif_record:77"
    assert geographic[0]["photo_urls"].count(";") == 1
    assert len(trait_a) == len(trait_b) == len(key) == 1
    assert "GBIF" not in trait_a[0]
    assert key[0]["source_type"] == "GBIF"
