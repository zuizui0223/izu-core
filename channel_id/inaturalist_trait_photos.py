"""Review-gated extraction of iNaturalist flower-photo candidate rows.

The input is the raw `observation_pages.json` retained by
`fetch_izu_inaturalist_snapshots.py`. Every output row is one photograph, not
one observation. The module deliberately does not assign islands, score floral
traits, infer trait frequency, or infer pollination interaction.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


COLUMNS = (
    "candidate_id",
    "record_id",
    "target_id",
    "query_taxon_name",
    "observed_taxon_name",
    "observed_on",
    "latitude",
    "longitude",
    "positional_accuracy_m",
    "quality_grade",
    "photo_index",
    "photo_id",
    "photo_url",
    "photo_original_url",
    "photo_license_code",
    "photo_attribution",
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
        "Photo candidate extracted from an iNaturalist raw snapshot. It is not "
        "an island assignment, random trait sample, pollination interaction, or "
        "guide/spot observation until manually reviewed."
    ),
}


def _as_string(value: object) -> str:
    return "" if value is None else str(value)


def _coordinates(record: dict[str, Any]) -> tuple[str, str]:
    geojson = record.get("geojson")
    if not isinstance(geojson, dict):
        return "", ""
    coordinates = geojson.get("coordinates")
    if not isinstance(coordinates, list) or len(coordinates) < 2:
        return "", ""
    return _as_string(coordinates[1]), _as_string(coordinates[0])


def _taxon_name(record: dict[str, Any]) -> str:
    taxon = record.get("taxon")
    return _as_string(taxon.get("name")) if isinstance(taxon, dict) else ""


def _photo_rows(record: dict[str, Any], target_id: str, query_taxon_name: str) -> list[dict[str, str]]:
    photos = record.get("photos")
    if not isinstance(photos, list):
        return []
    record_id = _as_string(record.get("id")).strip()
    if not record_id:
        return []
    latitude, longitude = _coordinates(record)
    observation_url = _as_string(record.get("uri"))
    rows: list[dict[str, str]] = []
    for index, photo in enumerate(photos, start=1):
        if not isinstance(photo, dict):
            continue
        photo_id = _as_string(photo.get("id")).strip()
        rows.append(
            {
                "candidate_id": f"inat:{record_id}:photo:{photo_id or index}",
                "record_id": record_id,
                "target_id": target_id,
                "query_taxon_name": query_taxon_name,
                "observed_taxon_name": _taxon_name(record),
                "observed_on": _as_string(record.get("observed_on")),
                "latitude": latitude,
                "longitude": longitude,
                "positional_accuracy_m": _as_string(record.get("positional_accuracy")),
                "quality_grade": _as_string(record.get("quality_grade")),
                "photo_index": str(index),
                "photo_id": photo_id,
                "photo_url": _as_string(photo.get("url")),
                "photo_original_url": _as_string(photo.get("original_url")),
                "photo_license_code": _as_string(photo.get("license_code")),
                "photo_attribution": _as_string(photo.get("attribution")),
                "observation_source_url": observation_url,
                **REVIEW_TEMPLATE,
            }
        )
    return rows


def extract_snapshot(snapshot_root: Path) -> list[dict[str, str]]:
    """Extract candidate rows from all target directories in a snapshot root."""
    if not snapshot_root.is_dir():
        raise ValueError(f"snapshot root does not exist: {snapshot_root}")
    candidates: list[dict[str, str]] = []
    for target_dir in sorted(path for path in snapshot_root.iterdir() if path.is_dir()):
        pages_path = target_dir / "observation_pages.json"
        manifest_path = target_dir / "manifest.json"
        if not pages_path.is_file() or not manifest_path.is_file():
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        target = manifest.get("target")
        if not isinstance(target, dict):
            raise ValueError(f"{manifest_path}: missing target object")
        target_id = _as_string(target.get("target_id")).strip()
        query_taxon_name = _as_string(target.get("taxon_name")).strip()
        if not target_id or not query_taxon_name:
            raise ValueError(f"{manifest_path}: target needs target_id and taxon_name")
        pages = json.loads(pages_path.read_text(encoding="utf-8"))
        if not isinstance(pages, list):
            raise ValueError(f"{pages_path}: expected list of API pages")
        for page in pages:
            if not isinstance(page, dict):
                raise ValueError(f"{pages_path}: API page is not an object")
            records = page.get("results", [])
            if not isinstance(records, list):
                raise ValueError(f"{pages_path}: API page lacks results list")
            for record in records:
                if isinstance(record, dict):
                    candidates.extend(_photo_rows(record, target_id, query_taxon_name))
    return sorted(candidates, key=lambda row: (row["target_id"], row["record_id"], int(row["photo_index"])))


def write_candidates(rows: list[dict[str, str]], output_csv: Path, output_md: Path) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    by_target: dict[str, int] = {}
    for row in rows:
        by_target[row["target_id"]] = by_target.get(row["target_id"], 0) + 1
    lines = [
        "# iNaturalist trait-photo candidate inventory",
        "",
        "Each row is a public photograph candidate linked to its original observation metadata. No image has been scored for guide/spot traits, assigned to an island, or used as a population sample.",
        "",
        f"Total photo candidates: {len(rows)}",
        "",
        "| target | photo candidates |",
        "|---|---:|",
    ]
    for target_id, count in sorted(by_target.items()):
        lines.append(f"| {target_id} | {count} |")
    lines.extend(
        [
            "",
            "## Review gates",
            "",
            "Before a candidate can enter `guide_direction_constraints.csv`, a reviewer must record: taxon confidence; site/island assignment from geometry; whether the inner corolla is visible; flower stage and photographic comparability; license/attribution; and the exact directional claim supported. A photo that only shows the exterior remains ineligible for guide/spot inference.",
        ]
    )
    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
