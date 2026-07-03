import csv
from pathlib import Path

import pytest

from channel_id.field_guide_photo_review import (
    FIELD_MANIFEST_COLUMNS,
    FieldReviewBundleConfig,
    build_field_review_bundle,
    read_field_manifest,
    write_field_review_bundle,
)
from channel_id.field_guide_reconcile import reconcile_field_reviews
from channel_id.guide_photo_review import read_completed_reviews


def _row(*, island: str = "Oshima", site: str = "S01", plant: str = "P01", flower: str = "F01", photo: str = "IMG001") -> dict[str, str]:
    return {
        "field_event_id": "izu_20260704",
        "island_id": island,
        "site_id": site,
        "plant_id": plant,
        "flower_id": flower,
        "photo_id": photo,
        "photo_uri": f"photos/{photo}.jpg",
        "captured_at": "2026-07-04T10:30:00+09:00",
        "latitude": "34.7500",
        "longitude": "139.3600",
        "field_taxon_label": "Campanula microdonta",
        "field_taxon_confidence": "field_high",
        "open_flower_field": "yes",
        "inner_corolla_view_field": "yes",
        "image_standardization_status": "diffuse_light_reference_frame",
        "photographer_id": "observer_1",
        "voucher_or_sample_id": "",
        "notes": "",
    }


def _write_manifest(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELD_MANIFEST_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def _accepted_trait(rows: list[dict[str, str]], reviewer: str, scores: list[int]) -> None:
    for row, score in zip(rows, scores):
        row.update({
            "trait_reviewer_id": reviewer,
            "focal_taxon_consistent": "yes",
            "inner_corolla_visibility": "adequate",
            "flower_open_stage": "open",
            "image_comparable": "yes",
            "guide_ordinal_0_to_3": str(score),
            "trait_review_status": "accepted",
        })


def test_field_bundle_groups_photos_by_tagged_plant_and_hides_provenance() -> None:
    rows = [
        _row(photo="IMG001"),
        _row(flower="F02", photo="IMG002"),
        _row(plant="P02", flower="F01", photo="IMG003"),
    ]
    bundle = build_field_review_bundle(rows, FieldReviewBundleConfig(seed=19))

    assert len(bundle.geographic_rows) == 2
    assert len(bundle.trait_a_rows) == 2
    first = next(row for row in bundle.geographic_rows if row["observation_unit_id"].endswith(":P01"))
    assert first["source_type"] == "field_photo"
    assert first["photo_urls"] == "photos/IMG001.jpg;photos/IMG002.jpg"
    assert first["geographic_review_status"] == "unreviewed"
    assert all("island" not in row and "site" not in row and "latitude" not in row for row in bundle.trait_a_rows)
    provenance = next(row for row in bundle.provenance_rows if row["plant_id"] == "P01")
    assert provenance["flower_ids"] == "F01;F02"
    assert provenance["island_id"] == "Oshima"


def test_manifest_validation_rejects_duplicate_photo_ids_and_cross_island_plant(tmp_path: Path) -> None:
    duplicate = tmp_path / "duplicate.csv"
    _write_manifest(duplicate, [_row(photo="IMG001"), _row(plant="P02", photo="IMG001")])
    with pytest.raises(ValueError, match="duplicate photo_id"):
        read_field_manifest(duplicate)

    rows = [_row(island="Oshima"), _row(island="Hachijo", photo="IMG002")]
    with pytest.raises(ValueError, match="spans multiple island IDs"):
        build_field_review_bundle(rows)


def test_field_bundle_round_trips_to_existing_reader_and_field_reconcile(tmp_path: Path) -> None:
    rows = [_row(plant=f"P{index:02d}", photo=f"IMG{index:03d}") for index in range(1, 4)]
    bundle = build_field_review_bundle(rows, FieldReviewBundleConfig(seed=7))
    output = tmp_path / "field_bundle"
    write_field_review_bundle(output, bundle)

    geographic, a, b, key = read_completed_reviews(
        output / "field_geographic_taxonomic_review.csv",
        output / "field_blind_trait_review_A.csv",
        output / "field_blind_trait_review_B.csv",
        output / "field_blind_review_key_DO_NOT_SHARE_WITH_TRAIT_REVIEWERS.csv",
    )
    for row in geographic:
        row.update({"geographic_review_status": "accepted", "verified_island_id": "Oshima", "taxon_review_status": "accepted"})
    _accepted_trait(a, "reviewer_A", [1, 1, 2])
    _accepted_trait(b, "reviewer_B", [1, 2, 2])

    eligible, summaries, drafts = reconcile_field_reviews(geographic, a, b, key, min_units_per_island=3)

    assert len(eligible) == 3
    assert eligible[0]["source_note"].startswith("Double-blind ordinal review; first-party field photo")
    assert summaries[0]["source_boundary"].startswith("Ordinal first-party field-photo")
    assert drafts == []


def test_field_reconcile_refuses_mixed_public_and_field_sources() -> None:
    geographic = [{"source_type": "field_photo"}]
    key = [{"source_type": "iNaturalist"}]
    with pytest.raises(ValueError, match="field blind key"):
        reconcile_field_reviews(geographic, [], [], key)
