"""Register literature, figure, public-photo, herbarium, and field leads for guides.

Discovery is intentionally separated from trait evidence. A source can be
useful for finding island-resolved flowers yet remain ineligible for any guide
constraint until location, taxonomy, visibility, duplicate handling, and an
appropriate review route are completed.
"""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from channel_id.guide_photo_review import VALID_ISLANDS

REGISTRY_COLUMNS = (
    "evidence_id", "source_type", "source_record_id", "source_url_or_citation",
    "source_locator", "source_date_or_year", "taxon_label", "taxon_status",
    "island_claim", "island_assignment_status", "island_id_verified", "site_or_locality",
    "evidence_mode", "guide_region_claim", "inner_corolla_visibility",
    "duplicate_group", "discovery_status", "trait_review_status", "model_route",
    "review_basis", "reviewer_id", "notes",
)
SUMMARY_COLUMNS = ("dimension", "value", "records", "boundary")

SOURCE_TYPES = frozenset({"literature_text", "literature_figure", "public_photo", "herbarium_media", "field_photo"})
EVIDENCE_MODES = frozenset({"text_description", "figure_or_plate", "image", "mixed"})
TAXON_STATUS = frozenset({"unreviewed", "accepted", "rejected", "uncertain"})
ISLAND_STATUS = frozenset({"unreviewed", "accepted", "rejected", "not_island_resolved"})
VISIBILITY = frozenset({"unreviewed", "adequate", "inadequate", "not_applicable_text"})
DISCOVERY_STATUS = frozenset({"discovered", "source_located", "screened", "excluded"})
TRAIT_STATUS = frozenset({"unreviewed", "pending_blind_review", "reviewed_ordinal", "excluded", "text_only_not_scored"})
MODEL_ROUTES = frozenset({"not_eligible", "blind_review_queue", "manual_constraint_candidate", "field_bundle"})


@dataclass(frozen=True)
class GuideEvidenceRegistrySummary:
    rows: tuple[dict[str, str], ...]
    summary_rows: tuple[dict[str, str], ...]


def _text(row: dict[str, str], field: str) -> str:
    return str(row.get(field, "")).strip()


def _require_columns(fieldnames: Iterable[str]) -> None:
    missing = set(REGISTRY_COLUMNS) - set(fieldnames)
    if missing:
        raise ValueError("guide evidence registry missing columns: " + ", ".join(sorted(missing)))


def _choice(row: dict[str, str], field: str, choices: frozenset[str]) -> None:
    value = _text(row, field)
    if value not in choices:
        raise ValueError(f"invalid {field} for evidence_id={_text(row, 'evidence_id')!r}: {value!r}")


def read_guide_evidence_registry(path: Path) -> tuple[dict[str, str], ...]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _require_columns(reader.fieldnames or ())
        rows = tuple(reader)
    seen: set[str] = set()
    for row in rows:
        evidence_id = _text(row, "evidence_id")
        if not evidence_id:
            raise ValueError("blank evidence_id")
        if evidence_id in seen:
            raise ValueError(f"duplicate evidence_id {evidence_id!r}")
        seen.add(evidence_id)
        for field in ("source_type", "source_record_id", "source_url_or_citation", "taxon_label", "evidence_mode", "discovery_status", "trait_review_status", "model_route"):
            if not _text(row, field):
                raise ValueError(f"blank {field} for evidence_id={evidence_id!r}")
        _choice(row, "source_type", SOURCE_TYPES)
        _choice(row, "evidence_mode", EVIDENCE_MODES)
        _choice(row, "taxon_status", TAXON_STATUS)
        _choice(row, "island_assignment_status", ISLAND_STATUS)
        _choice(row, "inner_corolla_visibility", VISIBILITY)
        _choice(row, "discovery_status", DISCOVERY_STATUS)
        _choice(row, "trait_review_status", TRAIT_STATUS)
        _choice(row, "model_route", MODEL_ROUTES)
        island = _text(row, "island_id_verified")
        if island and island not in VALID_ISLANDS:
            raise ValueError(f"invalid island_id_verified for evidence_id={evidence_id!r}")
        _validate_route(row)
    return rows


def _validate_route(row: dict[str, str]) -> None:
    evidence_id = _text(row, "evidence_id")
    route = _text(row, "model_route")
    source_type = _text(row, "source_type")
    taxon_ok = _text(row, "taxon_status") == "accepted"
    island_ok = _text(row, "island_assignment_status") == "accepted" and bool(_text(row, "island_id_verified"))
    visibility_ok = _text(row, "inner_corolla_visibility") == "adequate"
    if route == "blind_review_queue":
        if source_type not in {"public_photo", "herbarium_media", "field_photo", "literature_figure"}:
            raise ValueError(f"{evidence_id}: text-only source cannot enter blind photo queue")
        if not taxon_ok or not island_ok:
            raise ValueError(f"{evidence_id}: blind queue requires accepted taxon and island")
    elif route == "field_bundle":
        if source_type != "field_photo" or not taxon_ok or not island_ok:
            raise ValueError(f"{evidence_id}: field bundle requires accepted field_photo taxon and island")
    elif route == "manual_constraint_candidate":
        if not (taxon_ok and island_ok and visibility_ok and _text(row, "trait_review_status") == "reviewed_ordinal"):
            raise ValueError(f"{evidence_id}: manual constraint candidate requires accepted taxon/island, adequate visibility, and reviewed ordinal trait")
    if _text(row, "trait_review_status") == "reviewed_ordinal" and _text(row, "source_type") == "literature_text":
        raise ValueError(f"{evidence_id}: text-only record cannot carry an ordinal image review")


def summarize_guide_evidence_registry(rows: Sequence[dict[str, str]]) -> GuideEvidenceRegistrySummary:
    boundary = (
        "Registry counts are discovery and review workflow counts, not island trait prevalence. "
        "No record becomes a model constraint without a separate explicit manual decision."
    )
    summary: list[dict[str, str]] = []
    dimensions = {
        "source_type": "source_type",
        "discovery_status": "discovery_status",
        "trait_review_status": "trait_review_status",
        "model_route": "model_route",
        "verified_island": "island_id_verified",
    }
    for label, field in dimensions.items():
        counts = Counter(_text(row, field) or "blank_or_unresolved" for row in rows)
        for value, count in sorted(counts.items()):
            summary.append({"dimension": label, "value": value, "records": str(count), "boundary": boundary})
    by_island_route: dict[tuple[str, str], int] = defaultdict(int)
    for row in rows:
        island = _text(row, "island_id_verified")
        if island:
            by_island_route[(island, _text(row, "model_route"))] += 1
    for (island, route), count in sorted(by_island_route.items()):
        summary.append({"dimension": "verified_island_by_route", "value": f"{island}:{route}", "records": str(count), "boundary": boundary})
    return GuideEvidenceRegistrySummary(tuple(rows), tuple(summary))


def write_guide_evidence_registry_summary(output_dir: Path, summary: GuideEvidenceRegistrySummary) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "guide_evidence_registry_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=SUMMARY_COLUMNS)
        writer.writeheader()
        writer.writerows(summary.summary_rows)
    lines = [
        "# Guide evidence registry summary", "",
        f"Registered records: {len(summary.rows)}", "",
        "The registry deliberately includes unresolved text, figure, photo, herbarium, and field leads. It is not a trait dataset and does not update guide-direction constraints.",
    ]
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
