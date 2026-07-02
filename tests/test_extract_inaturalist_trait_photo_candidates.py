import csv
import json
from pathlib import Path

from scripts.extract_inaturalist_trait_photo_candidates import extract_snapshot, write_candidates


def _write_target(root: Path, target_id: str, taxon_name: str, pages: list[dict]) -> None:
    destination = root / target_id
    destination.mkdir(parents=True)
    (destination / "manifest.json").write_text(
        json.dumps({"target": {"target_id": target_id, "taxon_name": taxon_name}}),
        encoding="utf-8",
    )
    (destination / "observation_pages.json").write_text(json.dumps(pages), encoding="utf-8")


def test_extracts_one_row_per_photo_and_preserves_review_gate(tmp_path: Path) -> None:
    root = tmp_path / "snapshot"
    _write_target(
        root,
        "campanula_microdonta",
        "Campanula microdonta",
        [
            {
                "results": [
                    {
                        "id": 11,
                        "uri": "https://www.inaturalist.org/observations/11",
                        "observed_on": "2020-06-01",
                        "quality_grade": "research",
                        "positional_accuracy": 25,
                        "geojson": {"coordinates": [139.2, 34.2]},
                        "taxon": {"name": "Campanula microdonta"},
                        "photos": [
                            {
                                "id": 101,
                                "url": "https://static.inat.example/square.jpg",
                                "original_url": "https://static.inat.example/original.jpg",
                                "license_code": "cc-by",
                                "attribution": "observer",
                            },
                            {"id": 102, "url": "https://static.inat.example/second.jpg"},
                        ],
                    },
                    {"id": 12, "photos": []},
                ]
            }
        ],
    )

    rows = extract_snapshot(root)

    assert len(rows) == 2
    assert rows[0]["candidate_id"] == "inat:11:photo:101"
    assert rows[0]["latitude"] == "34.2"
    assert rows[0]["longitude"] == "139.2"
    assert rows[0]["corolla_inner_visibility"] == "unreviewed"
    assert rows[0]["trait_eligibility"] == "requires_independent_review"
    assert rows[1]["candidate_id"] == "inat:11:photo:102"


def test_writes_candidate_csv_and_inventory(tmp_path: Path) -> None:
    rows = [
        {
            "candidate_id": "inat:1:photo:1",
            "record_id": "1",
            "target_id": "campanula_microdonta",
            "query_taxon_name": "Campanula microdonta",
            "observed_taxon_name": "Campanula microdonta",
            "observed_on": "",
            "latitude": "",
            "longitude": "",
            "positional_accuracy_m": "",
            "quality_grade": "",
            "photo_index": "1",
            "photo_id": "1",
            "photo_url": "",
            "photo_original_url": "",
            "photo_license_code": "",
            "photo_attribution": "",
            "observation_source_url": "",
            "corolla_inner_visibility": "unreviewed",
            "island_assignment_status": "unreviewed",
            "trait_eligibility": "requires_independent_review",
            "review_status": "candidate",
            "notes": "candidate",
        }
    ]
    csv_path = tmp_path / "candidates.csv"
    markdown_path = tmp_path / "inventory.md"

    write_candidates(rows, csv_path, markdown_path)

    with csv_path.open(newline="", encoding="utf-8") as handle:
        assert list(csv.DictReader(handle))[0]["candidate_id"] == "inat:1:photo:1"
    assert "Total photo candidates: 1" in markdown_path.read_text(encoding="utf-8")
