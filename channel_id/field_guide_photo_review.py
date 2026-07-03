"""Create blinded guide-photo review bundles from first-party field records.

A review unit is one tagged plant. Multiple images or flowers from that plant
are alternative views, never independent trait replicates. Field provenance is
kept outside the blinded trait sheets and is not pooled with public-photo data.
"""

from __future__ import annotations

import csv
import hashlib
import random
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from channel_id.guide_photo_review import BLIND_TRAIT_COLUMNS, GEOGRAPHIC_COLUMNS, KEY_COLUMNS, VALID_ISLANDS

FIELD_MANIFEST_COLUMNS = (
    "field_event_id", "island_id", "site_id", "plant_id", "flower_id", "photo_id",
    "photo_uri", "captured_at", "latitude", "longitude", "field_taxon_label",
    "field_taxon_confidence", "open_flower_field", "inner_corolla_view_field",
    "image_standardization_status", "photographer_id", "voucher_or_sample_id", "notes",
)
FIELD_PROVENANCE_COLUMNS = (
    "observation_unit_id", "field_event_id", "island_id", "site_id", "plant_id",
    "flower_ids", "photo_ids", "photo_uris", "captured_at_values", "latitude_values",
    "longitude_values", "field_taxon_label_values", "field_taxon_confidence_values",
    "open_flower_field_values", "inner_corolla_view_field_values",
    "image_standardization_status_values", "photographer_ids", "voucher_or_sample_ids", "notes",
)


@dataclass(frozen=True)
class FieldReviewBundleConfig:
    target_id: str = "campanula_microdonta"
    seed: int = 20260703


@dataclass(frozen=True)
class FieldReviewBundle:
    geographic_rows: tuple[dict[str, str], ...]
    trait_a_rows: tuple[dict[str, str], ...]
    trait_b_rows: tuple[dict[str, str], ...]
    key_rows: tuple[dict[str, str], ...]
    provenance_rows: tuple[dict[str, str], ...]


def _text(row: dict[str, str], field: str) -> str:
    return str(row.get(field, "")).strip()


def _unit_id(event: str, site: str, plant: str) -> str:
    return f"field_plant:{event}:{site}:{plant}"


def _blind_id(unit_id: str, ordinal: int, seed: int) -> str:
    digest = hashlib.sha256(f"field|{seed}|{ordinal}|{unit_id}".encode("utf-8")).hexdigest()[:12]
    return f"field_blind_{ordinal:03d}_{digest}"


def _write(path: Path, fields: Sequence[str], rows: Sequence[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _require_manifest_columns(fieldnames: Iterable[str]) -> None:
    missing = set(FIELD_MANIFEST_COLUMNS) - set(fieldnames)
    if missing:
        raise ValueError("field manifest missing columns: " + ", ".join(sorted(missing)))


def _coordinate(row: dict[str, str], field: str, lower: float, upper: float) -> None:
    try:
        value = float(_text(row, field))
    except ValueError as error:
        raise ValueError(f"{field} must be numeric for photo_id={_text(row, 'photo_id')!r}") from error
    if not lower <= value <= upper:
        raise ValueError(f"{field} outside valid range for photo_id={_text(row, 'photo_id')!r}")


def read_field_manifest(path: Path) -> tuple[dict[str, str], ...]:
    """Validate a photo-level first-party manifest before plant-level grouping."""
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _require_manifest_columns(reader.fieldnames or ())
        rows = tuple(reader)
    if not rows:
        raise ValueError("field manifest has no rows")
    seen_photo_ids: set[str] = set()
    for row in rows:
        for field in ("field_event_id", "island_id", "site_id", "plant_id", "photo_id", "photo_uri", "field_taxon_label"):
            if not _text(row, field):
                raise ValueError(f"blank {field} for photo_id={_text(row, 'photo_id')!r}")
        if _text(row, "island_id") not in VALID_ISLANDS:
            raise ValueError(f"invalid island_id for photo_id={_text(row, 'photo_id')!r}")
        photo_id = _text(row, "photo_id")
        if photo_id in seen_photo_ids:
            raise ValueError(f"duplicate photo_id {photo_id!r}")
        seen_photo_ids.add(photo_id)
        _coordinate(row, "latitude", -90.0, 90.0)
        _coordinate(row, "longitude", -180.0, 180.0)
    return rows


def _join_unique(rows: Sequence[dict[str, str]], field: str) -> str:
    values: list[str] = []
    seen: set[str] = set()
    for row in rows:
        value = _text(row, field)
        if value and value not in seen:
            seen.add(value)
            values.append(value)
    return ";".join(values)


def build_field_review_bundle(
    rows: Sequence[dict[str, str]],
    config: FieldReviewBundleConfig = FieldReviewBundleConfig(),
) -> FieldReviewBundle:
    """Create geographic sheet, two blind sheets, a key, and provenance per plant."""
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(_text(row, "field_event_id"), _text(row, "site_id"), _text(row, "plant_id"))].append(row)
    geographic: list[dict[str, str]] = []
    provenance: list[dict[str, str]] = []
    for (event, site, plant), photo_rows in sorted(grouped.items()):
        islands = {_text(row, "island_id") for row in photo_rows}
        if len(islands) != 1:
            raise ValueError(f"field plant {event}/{site}/{plant} spans multiple island IDs")
        ordered = sorted(photo_rows, key=lambda row: (_text(row, "captured_at"), _text(row, "photo_id")))
        first = ordered[0]
        unit = _unit_id(event, site, plant)
        photo_uris = _join_unique(ordered, "photo_uri")
        geographic.append({
            "observation_unit_id": unit,
            "source_type": "field_photo",
            "record_id": unit,
            "target_id": config.target_id,
            "query_taxon_name": "",
            "observed_taxon_name": _join_unique(ordered, "field_taxon_label"),
            "observed_on": _text(first, "captured_at"),
            "latitude": _text(first, "latitude"),
            "longitude": _text(first, "longitude"),
            "positional_accuracy_m": "0",
            "quality_grade": "first_party_field_record",
            "candidate_ids": _join_unique(ordered, "photo_id"),
            "photo_urls": photo_uris,
            "observation_source_url": f"field_manifest:{event}",
            "nearest_declared_proxy": "not_applicable_direct_field_record",
            "nearest_proxy_distance_km": "",
            "second_nearest_declared_proxy": "",
            "second_nearest_proxy_distance_km": "",
            "nearest_proxy_gap_km": "",
            "geographic_review_status": "unreviewed",
            "verified_island_id": "",
            "taxon_review_status": "unreviewed",
            "review_basis": "first_party_field_manifest; inspect event, coordinate, plant ID, field taxon label, and image",
            "geographic_reviewer_id": "",
            "geographic_review_date": "",
            "notes": "",
        })
        provenance.append({
            "observation_unit_id": unit,
            "field_event_id": event,
            "island_id": next(iter(islands)),
            "site_id": site,
            "plant_id": plant,
            "flower_ids": _join_unique(ordered, "flower_id"),
            "photo_ids": _join_unique(ordered, "photo_id"),
            "photo_uris": photo_uris,
            "captured_at_values": _join_unique(ordered, "captured_at"),
            "latitude_values": _join_unique(ordered, "latitude"),
            "longitude_values": _join_unique(ordered, "longitude"),
            "field_taxon_label_values": _join_unique(ordered, "field_taxon_label"),
            "field_taxon_confidence_values": _join_unique(ordered, "field_taxon_confidence"),
            "open_flower_field_values": _join_unique(ordered, "open_flower_field"),
            "inner_corolla_view_field_values": _join_unique(ordered, "inner_corolla_view_field"),
            "image_standardization_status_values": _join_unique(ordered, "image_standardization_status"),
            "photographer_ids": _join_unique(ordered, "photographer_id"),
            "voucher_or_sample_ids": _join_unique(ordered, "voucher_or_sample_id"),
            "notes": _join_unique(ordered, "notes"),
        })
    shuffled = list(geographic)
    random.Random(config.seed).shuffle(shuffled)
    trait_a: list[dict[str, str]] = []
    trait_b: list[dict[str, str]] = []
    key: list[dict[str, str]] = []
    for ordinal, row in enumerate(shuffled, start=1):
        blind_id = _blind_id(row["observation_unit_id"], ordinal, config.seed)
        trait = {
            "blind_unit_id": blind_id,
            "photo_urls": row["photo_urls"],
            "photo_count": str(len(row["photo_urls"].split(";"))),
            "trait_reviewer_id": "",
            "trait_review_date": "",
            "focal_taxon_consistent": "unreviewed",
            "inner_corolla_visibility": "unreviewed",
            "flower_open_stage": "unreviewed",
            "image_comparable": "unreviewed",
            "guide_ordinal_0_to_3": "",
            "trait_review_status": "unreviewed",
            "exclusion_reason": "",
            "notes": "",
        }
        trait_a.append(dict(trait))
        trait_b.append(dict(trait))
        key.append({
            "blind_unit_id": blind_id,
            "observation_unit_id": row["observation_unit_id"],
            "source_type": "field_photo",
            "record_id": row["record_id"],
            "target_id": config.target_id,
        })
    return FieldReviewBundle(tuple(geographic), tuple(trait_a), tuple(trait_b), tuple(key), tuple(provenance))


def write_field_review_bundle(output_dir: Path, bundle: FieldReviewBundle) -> None:
    """Write a standalone first-party bundle; never concatenate with public-photo files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    _write(output_dir / "field_geographic_taxonomic_review.csv", GEOGRAPHIC_COLUMNS, bundle.geographic_rows)
    _write(output_dir / "field_blind_trait_review_A.csv", BLIND_TRAIT_COLUMNS, bundle.trait_a_rows)
    _write(output_dir / "field_blind_trait_review_B.csv", BLIND_TRAIT_COLUMNS, bundle.trait_b_rows)
    _write(output_dir / "field_blind_review_key_DO_NOT_SHARE_WITH_TRAIT_REVIEWERS.csv", KEY_COLUMNS, bundle.key_rows)
    _write(output_dir / "field_unit_provenance.csv", FIELD_PROVENANCE_COLUMNS, bundle.provenance_rows)
    lines = [
        "# First-party field guide-photo review bundle",
        "",
        f"Field plant review units: {len(bundle.geographic_rows)}",
        "One unit equals one field plant. Several photos or flowers from that plant are alternate views, not replicates.",
        "",
        "1. Complete field_geographic_taxonomic_review.csv using paired provenance and source images.",
        "2. Two trait reviewers complete the blind sheets independently; never share provenance, geographic sheet, or key with them.",
        "3. Run existing audit and reconciliation tools on this field bundle only; do not concatenate with public-photo files.",
        "",
        "The field island claim is not auto-accepted. First-party records improve provenance but do not establish guide mechanism, pollination effectiveness, or random island-wide estimates.",
    ]
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
