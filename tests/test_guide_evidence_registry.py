import csv
from pathlib import Path

import pytest

from channel_id.guide_evidence_registry import (
    REGISTRY_COLUMNS,
    read_guide_evidence_registry,
    summarize_guide_evidence_registry,
)


def _row(**changes: str) -> dict[str, str]:
    row = {
        "evidence_id": "lead_001",
        "source_type": "literature_text",
        "source_record_id": "paper:table_or_page",
        "source_url_or_citation": "Author year, page 1",
        "source_locator": "p. 1",
        "source_date_or_year": "1995",
        "taxon_label": "Campanula microdonta",
        "taxon_status": "unreviewed",
        "island_claim": "",
        "island_assignment_status": "not_island_resolved",
        "island_id_verified": "",
        "site_or_locality": "",
        "evidence_mode": "text_description",
        "guide_region_claim": "",
        "inner_corolla_visibility": "not_applicable_text",
        "duplicate_group": "",
        "discovery_status": "source_located",
        "trait_review_status": "text_only_not_scored",
        "model_route": "not_eligible",
        "review_basis": "direct source inspection pending",
        "reviewer_id": "",
        "notes": "",
    }
    row.update(changes)
    return row


def _write(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=REGISTRY_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def test_text_and_photo_leads_can_coexist_without_becoming_trait_constraints(tmp_path: Path) -> None:
    path = tmp_path / "registry.csv"
    photo = _row(
        evidence_id="photo_001",
        source_type="public_photo",
        source_record_id="inat:123",
        source_url_or_citation="https://www.inaturalist.org/observations/123",
        evidence_mode="image",
        taxon_status="accepted",
        island_claim="Oshima",
        island_assignment_status="accepted",
        island_id_verified="Oshima",
        inner_corolla_visibility="adequate",
        discovery_status="screened",
        trait_review_status="pending_blind_review",
        model_route="blind_review_queue",
    )
    _write(path, [_row(), photo])

    rows = read_guide_evidence_registry(path)
    summary = summarize_guide_evidence_registry(rows)
    counts = {(row["dimension"], row["value"]): row["records"] for row in summary.summary_rows}

    assert len(rows) == 2
    assert counts[("source_type", "literature_text")] == "1"
    assert counts[("source_type", "public_photo")] == "1"
    assert counts[("verified_island_by_route", "Oshima:blind_review_queue")] == "1"


def test_manual_constraint_route_requires_all_review_gates(tmp_path: Path) -> None:
    path = tmp_path / "registry.csv"
    bad = _row(
        source_type="public_photo",
        evidence_mode="image",
        taxon_status="accepted",
        island_assignment_status="accepted",
        island_id_verified="Hachijo",
        inner_corolla_visibility="inadequate",
        trait_review_status="reviewed_ordinal",
        model_route="manual_constraint_candidate",
    )
    _write(path, [bad])

    with pytest.raises(ValueError, match="manual constraint candidate"):
        read_guide_evidence_registry(path)


def test_text_only_record_cannot_fake_an_ordinal_image_review(tmp_path: Path) -> None:
    path = tmp_path / "registry.csv"
    bad = _row(trait_review_status="reviewed_ordinal")
    _write(path, [bad])

    with pytest.raises(ValueError, match="text-only"):
        read_guide_evidence_registry(path)


def test_duplicate_evidence_ids_are_rejected(tmp_path: Path) -> None:
    path = tmp_path / "registry.csv"
    _write(path, [_row(), _row()])

    with pytest.raises(ValueError, match="duplicate evidence_id"):
        read_guide_evidence_registry(path)
