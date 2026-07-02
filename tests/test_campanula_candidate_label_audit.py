import json
from pathlib import Path

import pytest

from channel_id.campanula_candidate_label_audit import (
    CandidateLabel,
    build_audit_rows,
    load_label_registry,
    load_snapshot_targets,
    validate_registry_against_snapshot,
)


ROOT = Path(__file__).parents[1]


def _photo(target_id: str, record_id: str, *, proxy: str = "Hachijo") -> dict[str, str]:
    return {
        "candidate_id": f"inat:{record_id}:photo:1",
        "record_id": record_id,
        "target_id": target_id,
        "query_taxon_name": "unused",
        "observed_taxon_name": "Campanula punctata",
        "observed_on": "2024-07-29",
        "latitude": "33.11",
        "longitude": "139.79",
        "positional_accuracy_m": "20",
        "quality_grade": "research",
        "photo_url": f"https://example.test/{record_id}.jpg",
        "observation_source_url": f"https://www.inaturalist.org/observations/{record_id}",
        "nearest_declared_proxy": proxy,
        "nearest_proxy_distance_km": "3",
        "second_nearest_declared_proxy": "Miyake",
        "second_nearest_proxy_distance_km": "40",
        "nearest_proxy_gap_km": "37",
    }


def test_declared_registry_matches_snapshot_config() -> None:
    registry = load_label_registry(ROOT / "data" / "campanula_candidate_label_registry.csv")
    targets = load_snapshot_targets(ROOT / "configs" / "izu_inaturalist_snapshot_targets.json")

    validate_registry_against_snapshot(registry, targets)


def test_overlapping_query_labels_are_deduplicated_at_source_record_level() -> None:
    registry = (
        CandidateLabel("campanula_microdonta", "Campanula microdonta", "focal_exact", "eligible_after_manual_taxon_review", True, "test", ""),
        CandidateLabel("campanula_punctata", "Campanula punctata", "broader_aggregate", "candidate_only_until_manual_focal_taxon_confirmation", True, "test", ""),
        CandidateLabel("campanula_punctata_var_microdonta", "Campanula punctata var. microdonta", "historical_record_label", "candidate_only_until_manual_focal_taxon_confirmation", True, "test", ""),
    )
    rows = [
        _photo("campanula_microdonta", "1"),
        _photo("campanula_punctata", "1"),
        _photo("campanula_punctata_var_microdonta", "2", proxy="Oshima"),
    ]

    records, summary = build_audit_rows(registry, rows)

    assert len(records) == 2
    shared = next(row for row in records if row["record_id"] == "1")
    assert shared["discovery_target_ids"] == "campanula_microdonta;campanula_punctata"
    assert shared["review_route"] == "existing_focal_review_path_after_manual_taxon_confirmation"
    historical = next(row for row in records if row["record_id"] == "2")
    assert historical["review_route"] == "candidate_only_do_not_send_to_focal_blind_review_without_explicit_taxon_promotion"
    by_target = {row["target_id"]: row for row in summary}
    assert by_target["campanula_microdonta"]["source_record_units_nearest_hachijo_proxy"] == "1"
    assert by_target["campanula_punctata"]["overlap_with_other_registry_target_ids"] == "campanula_microdonta"


def test_registry_validation_rejects_snapshot_name_mismatch(tmp_path: Path) -> None:
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"targets": [{"target_id": "campanula_microdonta", "taxon_name": "wrong label"}]}), encoding="utf-8")
    registry = (CandidateLabel("campanula_microdonta", "Campanula microdonta", "focal_exact", "eligible_after_manual_taxon_review", True, "test", ""),)

    with pytest.raises(ValueError, match="does not match"):
        validate_registry_against_snapshot(registry, load_snapshot_targets(config))
