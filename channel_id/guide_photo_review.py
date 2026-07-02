"""Build blinded, review-gated floral-guide photo review bundles.

Input rows are public-photo candidates after a proxy-only geographic triage.
They are not trait data. The workflow separates geographic/taxonomic review from
trait scoring, keeps one source record as one review unit even when it has
multiple images, and creates only non-binding constraint drafts after review.
"""

from __future__ import annotations

import csv
import hashlib
import random
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import median
from typing import Iterable, Sequence


VALID_ISLANDS = frozenset({"Oshima", "Toshima", "Niijima", "Kozushima", "Miyake", "Hachijo"})
VALID_ORDINAL_SCORES = frozenset({0, 1, 2, 3})

GEOGRAPHIC_COLUMNS = (
    "observation_unit_id", "source_type", "record_id", "target_id", "query_taxon_name", "observed_taxon_name",
    "observed_on", "latitude", "longitude", "positional_accuracy_m", "quality_grade",
    "candidate_ids", "photo_urls", "observation_source_url", "nearest_declared_proxy",
    "nearest_proxy_distance_km", "second_nearest_declared_proxy", "second_nearest_proxy_distance_km",
    "nearest_proxy_gap_km", "geographic_review_status", "verified_island_id", "taxon_review_status",
    "review_basis", "geographic_reviewer_id", "geographic_review_date", "notes",
)
BLIND_TRAIT_COLUMNS = (
    "blind_unit_id", "photo_urls", "photo_count", "trait_reviewer_id", "trait_review_date",
    "focal_taxon_consistent", "inner_corolla_visibility", "flower_open_stage", "image_comparable",
    "guide_ordinal_0_to_3", "trait_review_status", "exclusion_reason", "notes",
)
KEY_COLUMNS = ("blind_unit_id", "observation_unit_id", "source_type", "record_id", "target_id")
ELIGIBLE_COLUMNS = (
    "observation_unit_id", "source_type", "record_id", "verified_island_id", "trait_score_reviewer_a",
    "trait_score_reviewer_b", "consensus_guide_ordinal", "trait_score_difference", "source_note",
)
ISLAND_SUMMARY_COLUMNS = (
    "island_id", "eligible_observation_units", "median_consensus_guide_ordinal",
    "minimum_consensus_guide_ordinal", "maximum_consensus_guide_ordinal", "source_boundary",
)
DRAFT_CONSTRAINT_COLUMNS = (
    "draft_id", "left_island", "right_island", "suggested_relation", "left_n", "right_n",
    "left_median_ordinal", "right_median_ordinal", "strict_pairwise_direction_fraction",
    "draft_status", "source_boundary",
)


@dataclass(frozen=True)
class ReviewBundleConfig:
    target_id: str = "campanula_microdonta"
    max_positional_accuracy_m: float = 100.0
    min_proxy_gap_km: float = 20.0
    allowed_quality_grades: tuple[str, ...] = ("research",)
    seed: int = 20260702

    def __post_init__(self) -> None:
        if self.max_positional_accuracy_m <= 0.0:
            raise ValueError("max_positional_accuracy_m must be positive")
        if self.min_proxy_gap_km < 0.0:
            raise ValueError("min_proxy_gap_km cannot be negative")
        if not self.allowed_quality_grades or not all(value.strip() for value in self.allowed_quality_grades):
            raise ValueError("allowed_quality_grades must contain at least one nonblank value")


def _text(row: dict[str, str], field: str) -> str:
    return str(row.get(field, "")).strip()


def _parse_float(row: dict[str, str], field: str) -> float | None:
    value = _text(row, field)
    if not value:
        return None
    try:
        return float(value)
    except ValueError as error:
        raise ValueError(f"{field} is not numeric for {row.get('candidate_id', '<unknown>')!r}") from error


def _source_type(row: dict[str, str]) -> str:
    return _text(row, "source_type") or "iNaturalist"


def _source_slug(source_type: str) -> str:
    return "".join(character if character.isalnum() else "_" for character in source_type.casefold()).strip("_") or "source"


def _require_columns(fieldnames: Sequence[str], required: Iterable[str]) -> None:
    missing = set(required) - set(fieldnames)
    if missing:
        raise ValueError("candidate queue missing columns: " + ", ".join(sorted(missing)))


def read_proxy_queue(path: Path) -> tuple[list[dict[str, str]], tuple[str, ...]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = tuple(reader.fieldnames or ())
        _require_columns(fieldnames, {
            "candidate_id", "record_id", "target_id", "quality_grade", "positional_accuracy_m",
            "photo_url", "observation_source_url", "nearest_declared_proxy", "nearest_proxy_gap_km",
        })
        return list(reader), fieldnames


def _is_candidate_for_bundle(row: dict[str, str], config: ReviewBundleConfig) -> bool:
    if _text(row, "target_id") != config.target_id:
        return False
    allowed = {value.casefold() for value in config.allowed_quality_grades}
    if _text(row, "quality_grade").casefold() not in allowed:
        return False
    if not _text(row, "photo_url") or not _text(row, "observation_source_url"):
        return False
    accuracy = _parse_float(row, "positional_accuracy_m")
    gap = _parse_float(row, "nearest_proxy_gap_km")
    return (
        accuracy is not None and gap is not None
        and accuracy <= config.max_positional_accuracy_m
        and gap >= config.min_proxy_gap_km
    )


def _unit_id(source_type: str, record_id: str) -> str:
    return f"{_source_slug(source_type)}_record:{record_id}"


def _stable_blind_id(observation_unit_id: str, ordinal: int, seed: int) -> str:
    digest = hashlib.sha256(f"{seed}|{ordinal}|{observation_unit_id}".encode("utf-8")).hexdigest()[:12]
    return f"blind_{ordinal:03d}_{digest}"


def build_review_bundle(
    rows: Sequence[dict[str, str]],
    config: ReviewBundleConfig = ReviewBundleConfig(),
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    """Make geographic rows, two identical blinded sheets, and a private key."""
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if _is_candidate_for_bundle(row, config):
            record_id = _text(row, "record_id")
            if record_id:
                grouped[(_source_type(row), record_id)].append(row)

    geographic: list[dict[str, str]] = []
    for (source_type, record_id), photo_rows in sorted(grouped.items()):
        ordered = sorted(photo_rows, key=lambda row: (_text(row, "photo_index") or _text(row, "media_index"), _text(row, "candidate_id")))
        first = ordered[0]
        geographic.append({
            "observation_unit_id": _unit_id(source_type, record_id),
            "source_type": source_type,
            "record_id": record_id,
            "target_id": _text(first, "target_id"),
            "query_taxon_name": _text(first, "query_taxon_name"),
            "observed_taxon_name": _text(first, "observed_taxon_name"),
            "observed_on": _text(first, "observed_on"),
            "latitude": _text(first, "latitude"),
            "longitude": _text(first, "longitude"),
            "positional_accuracy_m": _text(first, "positional_accuracy_m"),
            "quality_grade": _text(first, "quality_grade"),
            "candidate_ids": ";".join(_text(row, "candidate_id") for row in ordered),
            "photo_urls": ";".join(_text(row, "photo_url") for row in ordered),
            "observation_source_url": _text(first, "observation_source_url"),
            "nearest_declared_proxy": _text(first, "nearest_declared_proxy"),
            "nearest_proxy_distance_km": _text(first, "nearest_proxy_distance_km"),
            "second_nearest_declared_proxy": _text(first, "second_nearest_declared_proxy"),
            "second_nearest_proxy_distance_km": _text(first, "second_nearest_proxy_distance_km"),
            "nearest_proxy_gap_km": _text(first, "nearest_proxy_gap_km"),
            "geographic_review_status": "unreviewed",
            "verified_island_id": "",
            "taxon_review_status": "unreviewed",
            "review_basis": "",
            "geographic_reviewer_id": "",
            "geographic_review_date": "",
            "notes": "",
        })

    shuffled = list(geographic)
    random.Random(config.seed).shuffle(shuffled)
    trait_a: list[dict[str, str]] = []
    trait_b: list[dict[str, str]] = []
    key: list[dict[str, str]] = []
    for ordinal, unit in enumerate(shuffled, start=1):
        blind_id = _stable_blind_id(unit["observation_unit_id"], ordinal, config.seed)
        base = {
            "blind_unit_id": blind_id,
            "photo_urls": unit["photo_urls"],
            "photo_count": str(len(unit["photo_urls"].split(";"))),
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
        trait_a.append(dict(base))
        trait_b.append(dict(base))
        key.append({
            "blind_unit_id": blind_id,
            "observation_unit_id": unit["observation_unit_id"],
            "source_type": unit["source_type"],
            "record_id": unit["record_id"],
            "target_id": unit["target_id"],
        })
    return geographic, trait_a, trait_b, key


def _write_csv(path: Path, fieldnames: Sequence[str], rows: Sequence[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_review_bundle(
    output_dir: Path,
    geographic: Sequence[dict[str, str]],
    trait_a: Sequence[dict[str, str]],
    trait_b: Sequence[dict[str, str]],
    key: Sequence[dict[str, str]],
    config: ReviewBundleConfig = ReviewBundleConfig(),
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "geographic_taxonomic_review.csv", GEOGRAPHIC_COLUMNS, geographic)
    _write_csv(output_dir / "blind_trait_review_A.csv", BLIND_TRAIT_COLUMNS, trait_a)
    _write_csv(output_dir / "blind_trait_review_B.csv", BLIND_TRAIT_COLUMNS, trait_b)
    _write_csv(output_dir / "blind_review_key_DO_NOT_SHARE_WITH_TRAIT_REVIEWERS.csv", KEY_COLUMNS, key)
    source_counts: dict[str, int] = defaultdict(int)
    for row in geographic:
        source_counts[row["source_type"]] += 1
    lines = [
        "# Blinded guide-photo review bundle",
        "",
        "One row equals one source record, not one photo. Multiple linked photos are alternative views of the same unit.",
        "",
        f"Eligible focal observation units: {len(geographic)}",
        f"Sources: {', '.join(f'{name}={count}' for name, count in sorted(source_counts.items())) or 'none'}",
        f"Selection: target_id={config.target_id}; quality-grade values={', '.join(config.allowed_quality_grades)}; positional accuracy ≤ {config.max_positional_accuracy_m:g} m; nearest-versus-second-proxy gap ≥ {config.min_proxy_gap_km:g} km.",
        "",
        "## Workflow",
        "",
        "1. Complete geographic_taxonomic_review.csv from the source URL, coordinates, accuracy, and taxonomy. This file is not blinded.",
        "2. Two trait reviewers independently complete A and B. Do not share the geographic file or key with trait reviewers. Blind files hide coordinates, island/proxy names, source names, and source URLs.",
        "3. Enter an ordinal guide score only when inner corolla visibility is adequate, flower stage is open, and image comparability is yes: 0 = no/negligible guide, 1 = weak, 2 = moderate, 3 = strong.",
        "4. Reconcile completed sheets. The output is a review draft only; it never edits model constraints automatically.",
        "",
        "## Boundary",
        "",
        "Quality-grade filtering and a large proxy gap are triage gates, not proof of island membership, media reliability, or random sampling. Geographic/taxonomic acceptance remains mandatory, and one source record remains one unit in all summaries.",
    ]
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _read_required_csv(path: Path, required: Iterable[str]) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = tuple(reader.fieldnames or ())
        missing = set(required) - set(fields)
        if missing:
            raise ValueError(f"{path}: missing columns: " + ", ".join(sorted(missing)))
        return list(reader)


def read_completed_reviews(
    geographic_path: Path,
    review_a_path: Path,
    review_b_path: Path,
    key_path: Path,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    return (
        _read_required_csv(geographic_path, {"observation_unit_id", "record_id", "verified_island_id", "geographic_review_status", "taxon_review_status"}),
        _read_required_csv(review_a_path, {"blind_unit_id", "focal_taxon_consistent", "inner_corolla_visibility", "flower_open_stage", "image_comparable", "guide_ordinal_0_to_3", "trait_review_status"}),
        _read_required_csv(review_b_path, {"blind_unit_id", "focal_taxon_consistent", "inner_corolla_visibility", "flower_open_stage", "image_comparable", "guide_ordinal_0_to_3", "trait_review_status"}),
        _read_required_csv(key_path, {"blind_unit_id", "observation_unit_id", "record_id", "target_id"}),
    )


def _index_unique(rows: Sequence[dict[str, str]], field: str, label: str) -> dict[str, dict[str, str]]:
    indexed: dict[str, dict[str, str]] = {}
    for row in rows:
        key = _text(row, field)
        if not key:
            raise ValueError(f"{label}: blank {field}")
        if key in indexed:
            raise ValueError(f"{label}: duplicate {field} {key!r}")
        indexed[key] = row
    return indexed


def _accepted_trait_score(row: dict[str, str]) -> int | None:
    gates = {
        "focal_taxon_consistent": "yes",
        "inner_corolla_visibility": "adequate",
        "flower_open_stage": "open",
        "image_comparable": "yes",
        "trait_review_status": "accepted",
    }
    if any(_text(row, field).lower() != value for field, value in gates.items()):
        return None
    try:
        score = int(_text(row, "guide_ordinal_0_to_3"))
    except ValueError:
        return None
    return score if score in VALID_ORDINAL_SCORES else None


def reconcile_reviews(
    geographic_rows: Sequence[dict[str, str]],
    review_a_rows: Sequence[dict[str, str]],
    review_b_rows: Sequence[dict[str, str]],
    key_rows: Sequence[dict[str, str]],
    *,
    min_units_per_island: int = 3,
    maximum_reviewer_score_difference: int = 1,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    """Return eligible units, island ordinal summaries, and non-binding drafts."""
    if min_units_per_island < 1:
        raise ValueError("min_units_per_island must be positive")
    if maximum_reviewer_score_difference < 0:
        raise ValueError("maximum_reviewer_score_difference cannot be negative")
    geographic = _index_unique(geographic_rows, "observation_unit_id", "geographic review")
    review_a = _index_unique(review_a_rows, "blind_unit_id", "trait review A")
    review_b = _index_unique(review_b_rows, "blind_unit_id", "trait review B")
    key = _index_unique(key_rows, "blind_unit_id", "blind key")
    eligible: list[dict[str, str]] = []
    for blind_id, key_row in sorted(key.items()):
        geo = geographic.get(_text(key_row, "observation_unit_id"))
        left = review_a.get(blind_id)
        right = review_b.get(blind_id)
        if geo is None or left is None or right is None:
            continue
        island_id = _text(geo, "verified_island_id")
        if _text(geo, "geographic_review_status").lower() != "accepted":
            continue
        if _text(geo, "taxon_review_status").lower() != "accepted" or island_id not in VALID_ISLANDS:
            continue
        score_a = _accepted_trait_score(left)
        score_b = _accepted_trait_score(right)
        if score_a is None or score_b is None or abs(score_a - score_b) > maximum_reviewer_score_difference:
            continue
        eligible.append({
            "observation_unit_id": _text(key_row, "observation_unit_id"),
            "source_type": _text(key_row, "source_type") or _text(geo, "source_type") or "unknown",
            "record_id": _text(geo, "record_id"),
            "verified_island_id": island_id,
            "trait_score_reviewer_a": str(score_a),
            "trait_score_reviewer_b": str(score_b),
            "consensus_guide_ordinal": str(round((score_a + score_b) / 2)),
            "trait_score_difference": str(abs(score_a - score_b)),
            "source_note": "Double-blind ordinal review; public photo candidate; one row per source record.",
        })

    by_island: dict[str, list[int]] = defaultdict(list)
    for row in eligible:
        by_island[row["verified_island_id"]].append(int(row["consensus_guide_ordinal"]))
    boundary = (
        "Ordinal public-photo review summary, not a random-sample estimate. A directional model constraint requires independent biological confirmation after inspecting underlying units."
    )
    summary = [{
        "island_id": island_id,
        "eligible_observation_units": str(len(values)),
        "median_consensus_guide_ordinal": f"{median(values):g}",
        "minimum_consensus_guide_ordinal": str(min(values)),
        "maximum_consensus_guide_ordinal": str(max(values)),
        "source_boundary": boundary,
    } for island_id, values in sorted(by_island.items())]

    drafts: list[dict[str, str]] = []
    islands = sorted(by_island)
    for index, left_island in enumerate(islands):
        for right_island in islands[index + 1:]:
            left_values, right_values = by_island[left_island], by_island[right_island]
            if len(left_values) < min_units_per_island or len(right_values) < min_units_per_island:
                continue
            left_median, right_median = median(left_values), median(right_values)
            relation = "gt" if left_median > right_median else "lt" if left_median < right_median else ""
            if relation == "gt":
                strict = sum(left > right for left in left_values for right in right_values)
            elif relation == "lt":
                strict = sum(left < right for left in left_values for right in right_values)
            else:
                strict = 0
            drafts.append({
                "draft_id": f"public_photo_ordinal_{left_island.lower()}_{right_island.lower()}",
                "left_island": left_island,
                "right_island": right_island,
                "suggested_relation": relation,
                "left_n": str(len(left_values)),
                "right_n": str(len(right_values)),
                "left_median_ordinal": f"{left_median:g}",
                "right_median_ordinal": f"{right_median:g}",
                "strict_pairwise_direction_fraction": f"{strict / (len(left_values) * len(right_values)):.6f}",
                "draft_status": "requires_manual_biological_confirmation",
                "source_boundary": boundary,
            })
    return eligible, summary, drafts


def write_reconciliation(
    output_dir: Path,
    eligible: Sequence[dict[str, str]],
    summary: Sequence[dict[str, str]],
    drafts: Sequence[dict[str, str]],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "eligible_observation_units.csv", ELIGIBLE_COLUMNS, eligible)
    _write_csv(output_dir / "island_ordinal_summary.csv", ISLAND_SUMMARY_COLUMNS, summary)
    _write_csv(output_dir / "guide_direction_constraint_drafts.csv", DRAFT_CONSTRAINT_COLUMNS, drafts)
    lines = [
        "# Guide-photo review reconciliation",
        "",
        f"Eligible observation units after geographic, taxonomic, and double-blind trait gates: {len(eligible)}",
        f"Island summaries: {len(summary)}",
        f"Directional drafts requiring scientific confirmation: {len(drafts)}",
        "",
        "No output here modifies data/guide_direction_constraints.csv. Every draft needs source-unit, guide-region, reviewer-note, and public-photo-boundary checks before a manual model update.",
    ]
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
