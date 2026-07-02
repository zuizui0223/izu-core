import csv
import json
from pathlib import Path

from channel_id.gbif_trait_photos import extract_snapshot, origin_platform_hint, write_candidates


def _write_target(root: Path, target_id: str, scientific_name: str, pages: list[dict]) -> None:
    destination = root / target_id
    destination.mkdir(parents=True)
    (destination / "manifest.json").write_text(
        json.dumps({"target_id": target_id, "scientific_name_requested": scientific_name}),
        encoding="utf-8",
    )
    (destination / "occurrence_pages.json").write_text(json.dumps(pages), encoding="utf-8")


def test_extracts_image_media_only_and_preserves_gbif_source_metadata(tmp_path: Path) -> None:
    root = tmp_path / "snapshot"
    _write_target(
        root,
        "campanula_microdonta",
        "Campanula microdonta Koidz.",
        [{
            "results": [{
                "key": 123,
                "scientificName": "Campanula microdonta Koidz.",
                "eventDate": "2024-07-29",
                "decimalLatitude": 33.11,
                "decimalLongitude": 139.79,
                "coordinateUncertaintyInMeters": 50,
                "basisOfRecord": "HUMAN_OBSERVATION",
                "datasetKey": "dataset-1",
                "media": [
                    {
                        "identifier": "https://images.example/a.jpg",
                        "type": "StillImage",
                        "format": "image/jpeg",
                        "license": "CC_BY_4_0",
                        "creator": "observer",
                        "references": "https://source.example/record/123",
                    },
                    {"identifier": "https://images.example/sound.mp3", "type": "Sound", "format": "audio/mpeg"},
                ],
            }]
        }],
    )

    rows = extract_snapshot(root)

    assert len(rows) == 1
    row = rows[0]
    assert row["candidate_id"] == "gbif:123:media:1"
    assert row["source_type"] == "GBIF"
    assert row["quality_grade"] == "HUMAN_OBSERVATION"
    assert row["photo_url"] == "https://images.example/a.jpg"
    assert row["media_license"] == "CC_BY_4_0"
    assert row["origin_platform_hint"] == "not_flagged_as_iNaturalist"
    assert row["trait_eligibility"] == "requires_independent_review"


def test_origin_hint_flags_explicit_inaturalist_republication_only() -> None:
    assert origin_platform_hint("https://inaturalist-open-data.s3.amazonaws.com/photos/1/original.jpg", "") == "iNaturalist_republication"
    assert origin_platform_hint("https://images.example/flower.jpg", "https://www.inaturalist.org/photos/1") == "iNaturalist_republication"
    assert origin_platform_hint("https://collections.example/flower.jpg", "") == "not_flagged_as_iNaturalist"


def test_write_inventory_reports_media_and_unique_record_counts(tmp_path: Path) -> None:
    rows = [{
        "candidate_id": "gbif:1:media:1",
        "source_type": "GBIF",
        "record_id": "1",
        "target_id": "campanula_microdonta",
        "query_taxon_name": "Campanula microdonta Koidz.",
        "observed_taxon_name": "Campanula microdonta Koidz.",
        "observed_on": "",
        "latitude": "",
        "longitude": "",
        "positional_accuracy_m": "",
        "quality_grade": "HUMAN_OBSERVATION",
        "basis_of_record": "HUMAN_OBSERVATION",
        "dataset_key": "dataset",
        "origin_platform_hint": "iNaturalist_republication",
        "media_index": "1",
        "media_identifier": "https://images.example/a.jpg",
        "media_type": "StillImage",
        "media_format": "image/jpeg",
        "media_license": "",
        "media_creator": "",
        "media_references": "",
        "photo_url": "https://images.example/a.jpg",
        "photo_original_url": "https://images.example/a.jpg",
        "observation_source_url": "https://www.gbif.org/occurrence/1",
        "corolla_inner_visibility": "unreviewed",
        "island_assignment_status": "unreviewed",
        "trait_eligibility": "requires_independent_review",
        "review_status": "candidate",
        "notes": "candidate",
    }]
    csv_path = tmp_path / "gbif_candidates.csv"
    markdown_path = tmp_path / "inventory.md"

    write_candidates(rows, csv_path, markdown_path)

    with csv_path.open(newline="", encoding="utf-8") as handle:
        assert list(csv.DictReader(handle))[0]["source_type"] == "GBIF"
    text = markdown_path.read_text(encoding="utf-8")
    assert "Total photo candidates: 1" in text
    assert "Clearly flagged iNaturalist republications: 1" in text
    assert "| campanula_microdonta | 1 | 1 |" in text
