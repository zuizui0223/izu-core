"""Extract review-gated flower-photo candidates from raw GBIF occurrence pages.

The input is `occurrence_pages.json` retained by the GBIF snapshot workflow.
Each output row represents one media item linked to a GBIF occurrence. The module
never assigns an island, scores a floral trait, estimates trait frequency, or
infers a plant-pollinator interaction. It only retains source metadata needed
for later geographic, taxonomic, licensing, and blinded trait review.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


COLUMNS = (
    "candidate_id",
    "source_type",
    "record_id",
    "target_id",
    "query_taxon_name",
    "observed_taxon_name",
    "observed_on",
    "latitude",
    "longitude",
    "positional_accuracy_m",
    "quality_grade",
    "basis_of_record",
    "dataset_key",
    "media_index",
    "media_identifier",
    "media_type",
    "media_format",
    "media_license",
    "media_creator",
    "media_references",
    "photo_url",
    "photo_original_url",
    "observation_source_url",
    "corolla_inner_visibility",
    "island_assignment_status",
    "trait_eligibility",
    "review_status",
    "notes",
)

REVIEW_TEMPLATE = {
    "corolla_inner_visibility": "unreviewed",
    "island_assignment_status": "unreviewed",
    "trait_eligibility": "requires_independent_review",
    "review_status": "candidate",
    "notes": (
        "Photo candidate extracted from a raw GBIF occurrence snapshot. It is not "
        "an island assignment, random trait sample, pollination interaction, or "
        "guide/spot observation until manually reviewed."
    ),
}


def _text(value: object) -> str:
    return "" if value is None else str(value).strip()


def _coordinates(record: dict[str, Any]) -> tuple[str, str]:
    return _text(record.get("decimalLatitude")), _text(record.get("decimalLongitude"))


def _media_items(record: dict[str, Any]) -> list[dict[str, Any]]:
    """Return only image-like GBIF media entries with a usable identifier URL."""
    media = record.get("media")
    if not isinstance(media, list):
        return []
    output: list[dict[str, Any]] = []
    for item in media:
        if not isinstance(item, dict):
            continue
        identifier = _text(item.get("identifier"))
        media_type = _text(item.get("type"))
        media_format = _text(item.get("format"))
        image_like = (
            media_type.casefold() in {"stillimage", "image"}
            or media_format.casefold().startswith("image/")
            or identifier.casefold().split("?", 1)[0].endswith((".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"))
        )
        if identifier and image_like:
            output.append(item)
    return output


def _record_rows(record: dict[str, Any], target_id: str, query_taxon_name: str) -> list[dict[str, str]]:
    record_id = _text(record.get("key"))
    if not record_id:
        return []
    latitude, longitude = _coordinates(record)
    rows: list[dict[str, str]] = []
    for index, media in enumerate(_media_items(record), start=1):
        identifier = _text(media.get("identifier"))
        rows.append(
            {
                "candidate_id": f"gbif:{record_id}:media:{index}",
                "source_type": "GBIF",
                "record_id": record_id,
                "target_id": target_id,
                "query_taxon_name": query_taxon_name,
                "observed_taxon_name": _text(record.get("scientificName") or record.get("species")),
                "observed_on": _text(record.get("eventDate") or record.get("year")),
                "latitude": latitude,
                "longitude": longitude,
                "positional_accuracy_m": _text(record.get("coordinateUncertaintyInMeters")),
                "quality_grade": _text(record.get("basisOfRecord")),
                "basis_of_record": _text(record.get("basisOfRecord")),
                "dataset_key": _text(record.get("datasetKey")),
                "media_index": str(index),
                "media_identifier": identifier,
                "media_type": _text(media.get("type")),
                "media_format": _text(media.get("format")),
                "media_license": _text(media.get("license")),
                "media_creator": _text(media.get("creator")),
                "media_references": _text(media.get("references")),
                "photo_url": identifier,
                "photo_original_url": identifier,
                "observation_source_url": f"https://www.gbif.org/occurrence/{record_id}",
                **REVIEW_TEMPLATE,
            }
        )
    return rows


def extract_snapshot(snapshot_root: Path) -> list[dict[str, str]]:
    """Extract one candidate row per usable GBIF media item across all targets."""
    if not snapshot_root.is_dir():
        raise ValueError(f"snapshot root does not exist: {snapshot_root}")
    rows: list[dict[str, str]] = []
    for target_dir in sorted(path for path in snapshot_root.iterdir() if path.is_dir()):
        pages_path = target_dir / "occurrence_pages.json"
        manifest_path = target_dir / "manifest.json"
        if not pages_path.is_file() or not manifest_path.is_file():
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        target_id = _text(manifest.get("target_id"))
        query_taxon_name = _text(manifest.get("scientific_name_requested"))
        if not target_id or not query_taxon_name:
            raise ValueError(f"{manifest_path}: missing target_id or scientific_name_requested")
        pages = json.loads(pages_path.read_text(encoding="utf-8"))
        if not isinstance(pages, list):
            raise ValueError(f"{pages_path}: expected a list of API pages")
        for page in pages:
            if not isinstance(page, dict):
                raise ValueError(f"{pages_path}: API page is not an object")
            records = page.get("results", [])
            if not isinstance(records, list):
                raise ValueError(f"{pages_path}: API page lacks a results list")
            for record in records:
                if isinstance(record, dict):
                    rows.extend(_record_rows(record, target_id, query_taxon_name))
    return sorted(rows, key=lambda row: (row["target_id"], row["record_id"], int(row["media_index"])))


def write_candidates(rows: list[dict[str, str]], output_csv: Path, output_md: Path) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    by_target: dict[str, int] = {}
    by_record: dict[str, set[str]] = {}
    for row in rows:
        by_target[row["target_id"]] = by_target.get(row["target_id"], 0) + 1
        by_record.setdefault(row["target_id"], set()).add(row["record_id"])
    lines = [
        "# GBIF trait-photo candidate inventory",
        "",
        "Each row is a GBIF media candidate linked to its original occurrence. No image has been scored for guide/spot traits, assigned to an island, or used as a population sample.",
        "",
        f"Total photo candidates: {len(rows)}",
        "",
        "| target | media candidates | unique occurrence records |",
        "|---|---:|---:|",
    ]
    for target_id, count in sorted(by_target.items()):
        lines.append(f"| {target_id} | {count} | {len(by_record[target_id])} |")
    lines.extend((
        "",
        "## Review gates",
        "",
        "Before a candidate enters a guide-direction analysis, a reviewer must check the original GBIF occurrence, taxon, geometry and coordinate uncertainty, media provenance/license, open inner-corolla visibility, flower stage, and comparability. Multiple media items from one GBIF occurrence remain one review unit.",
    ))
    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
