from channel_id.guide_photo_review import ReviewBundleConfig, build_review_bundle, reconcile_reviews


def _candidate(record_id: str, candidate_id: str, *, quality: str = "research", accuracy: str = "20", gap: str = "25") -> dict[str, str]:
    return {
        "candidate_id": candidate_id,
        "record_id": record_id,
        "target_id": "campanula_microdonta",
        "query_taxon_name": "Campanula microdonta",
        "observed_taxon_name": "Campanula microdonta",
        "observed_on": "2024-07-01",
        "latitude": "34.7",
        "longitude": "139.4",
        "positional_accuracy_m": accuracy,
        "quality_grade": quality,
        "photo_index": "1",
        "photo_url": f"https://example.test/{candidate_id}.jpg",
        "observation_source_url": f"https://example.test/observations/{record_id}",
        "nearest_declared_proxy": "Oshima",
        "nearest_proxy_distance_km": "5",
        "second_nearest_declared_proxy": "Toshima",
        "second_nearest_proxy_distance_km": "30",
        "nearest_proxy_gap_km": gap,
    }


def test_bundle_deduplicates_photo_angles_and_keeps_trait_sheets_blind() -> None:
    rows = [
        _candidate("1", "one-a"),
        _candidate("1", "one-b"),
        _candidate("2", "two"),
        _candidate("3", "excluded-quality", quality="needs_id"),
        _candidate("4", "excluded-gap", gap="3"),
    ]

    geographic, trait_a, trait_b, key = build_review_bundle(rows, ReviewBundleConfig(seed=8))

    assert len(geographic) == 2
    observation_one = next(row for row in geographic if row["record_id"] == "1")
    assert observation_one["candidate_ids"] == "one-a;one-b"
    assert observation_one["photo_urls"].count(";") == 1
    assert len(trait_a) == len(trait_b) == len(key) == 2
    assert set(trait_a[0]).isdisjoint({"latitude", "longitude", "nearest_declared_proxy", "observation_source_url"})
    assert trait_a == trait_b


def _accepted_trait(blind_id: str, score: int) -> dict[str, str]:
    return {
        "blind_unit_id": blind_id,
        "focal_taxon_consistent": "yes",
        "inner_corolla_visibility": "adequate",
        "flower_open_stage": "open",
        "image_comparable": "yes",
        "guide_ordinal_0_to_3": str(score),
        "trait_review_status": "accepted",
    }


def test_reconciliation_requires_two_reviews_and_makes_nonbinding_direction_draft() -> None:
    geographic = []
    key = []
    review_a = []
    review_b = []
    for island, scores in (("Hachijo", (0, 1, 1)), ("Oshima", (2, 3, 3))):
        for index, score in enumerate(scores, start=1):
            observation = f"inat_observation:{island}-{index}"
            blind = f"blind-{island}-{index}"
            geographic.append({
                "observation_unit_id": observation,
                "record_id": observation,
                "verified_island_id": island,
                "geographic_review_status": "accepted",
                "taxon_review_status": "accepted",
            })
            key.append({"blind_unit_id": blind, "observation_unit_id": observation, "record_id": observation, "target_id": "campanula_microdonta"})
            review_a.append(_accepted_trait(blind, score))
            review_b.append(_accepted_trait(blind, score))

    eligible, summary, drafts = reconcile_reviews(geographic, review_a, review_b, key, min_units_per_island=3)

    assert len(eligible) == 6
    assert {row["island_id"] for row in summary} == {"Hachijo", "Oshima"}
    assert len(drafts) == 1
    assert drafts[0]["left_island"] == "Hachijo"
    assert drafts[0]["right_island"] == "Oshima"
    assert drafts[0]["suggested_relation"] == "lt"
    assert drafts[0]["draft_status"] == "requires_manual_biological_confirmation"


def test_reconciliation_excludes_one_reviewer_or_ineligible_records() -> None:
    geographic = [{
        "observation_unit_id": "inat_observation:1",
        "record_id": "1",
        "verified_island_id": "Oshima",
        "geographic_review_status": "accepted",
        "taxon_review_status": "accepted",
    }]
    key = [{"blind_unit_id": "blind-1", "observation_unit_id": "inat_observation:1", "record_id": "1", "target_id": "campanula_microdonta"}]
    accepted = _accepted_trait("blind-1", 2)
    rejected = dict(accepted)
    rejected["inner_corolla_visibility"] = "partial"

    eligible, summary, drafts = reconcile_reviews(geographic, [accepted], [rejected], key, min_units_per_island=1)

    assert eligible == []
    assert summary == []
    assert drafts == []
