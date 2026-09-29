"""Validate acquisition readiness for independent primary-source lineages.

The current comparison programme deliberately separates three states:

1. source-native directional evidence can be active from an abstract/full-text
   statement without inventing an effect size;
2. a population-level numeric morphology effect requires named localities,
   values, independent n, uncertainty/raw data, units and a source locator;
3. dependency-moderated synthesis additionally requires an independently
   justified effective-pollinator dependency class.

Publisher-listed supplementary filenames are useful acquisition routes, but
their existence is not evidence that any numeric gate has been satisfied.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence


NUMERIC_GATE_FIELDS = (
    "source_recovered",
    "named_population_localities",
    "trait_mean_or_raw_values",
    "independent_biological_n",
    "uncertainty_or_raw_values",
    "trait_definition_and_unit",
    "numeric_source_locator",
    "exact_geographic_mapping",
)
DEPENDENCY_GATE_FIELDS = (
    "effective_pollinator_dependency_resolved",
    "same_population_or_prespecified_transfer",
)
ALLOWED_DIRECTIONAL_STATUS = {"active_B_grade", "context_only", "not_active"}
ALLOWED_STEP_STATUS = {"supports", "does_not_demonstrate", "unresolved"}
ALLOWED_ADMISSION_STATUS = {"blocked", "ready"}
ALLOWED_ACCESS_STATUS = {
    "publisher_metadata_only",
    "publisher_supporting_files_identified_binary_delivery_blocked",
    "publisher_article_route_and_external_supplement_listing_binary_unrecovered",
    "full_text_recovered",
    "author_manuscript_recovered",
    "lawful_repository_copy_recovered",
}
ALLOWED_SUPPLEMENT_ROLE = {
    "locality_mapping",
    "trait_context",
    "pollinator_context",
    "pairwise_test_context",
    "photo_context",
}
REQUIRED_SOURCE_IDS = {
    "weigela_yamada_2010",
    "ligustrum_yamada_2014",
    "hosta_yamada_2014",
}


@dataclass(frozen=True)
class SourceAcquisition:
    source_id: str
    taxon: str
    doi: str
    directional_status: str
    directional_pattern: str
    shared_second_step_status: str
    access_status: str
    numeric_effect_status: str
    dependency_moderation_status: str
    numeric_gate: Mapping[str, bool]
    dependency_gate: Mapping[str, bool]
    supplements: tuple[Mapping[str, object], ...]
    issue_number: int
    next_action: str
    claim_boundary: str


def _require_bool_map(
    value: object,
    fields: Sequence[str],
    *,
    source_id: str,
    label: str,
) -> dict[str, bool]:
    if not isinstance(value, dict):
        raise ValueError(f"{source_id}: {label} must be an object")
    missing = sorted(set(fields) - set(value))
    extra = sorted(set(value) - set(fields))
    if missing or extra:
        details = []
        if missing:
            details.append("missing " + ", ".join(missing))
        if extra:
            details.append("unexpected " + ", ".join(extra))
        raise ValueError(f"{source_id}: invalid {label}: " + "; ".join(details))
    output: dict[str, bool] = {}
    for field in fields:
        item = value[field]
        if not isinstance(item, bool):
            raise ValueError(f"{source_id}: {label}.{field} must be boolean")
        output[field] = item
    return output


def numeric_effect_ready(source: SourceAcquisition) -> bool:
    return all(source.numeric_gate[field] for field in NUMERIC_GATE_FIELDS)


def dependency_moderation_ready(source: SourceAcquisition) -> bool:
    return numeric_effect_ready(source) and all(
        source.dependency_gate[field] for field in DEPENDENCY_GATE_FIELDS
    )


def load_manifest(path: str | Path) -> tuple[SourceAcquisition, ...]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("schema_version") != "1.0":
        raise ValueError("independent-source manifest requires schema_version=1.0")
    if payload.get("issue_number") != 92:
        raise ValueError("independent-source manifest must link acquisition issue #92")
    raw_sources = payload.get("sources")
    if not isinstance(raw_sources, list) or not raw_sources:
        raise ValueError("independent-source manifest requires a non-empty sources list")

    output: list[SourceAcquisition] = []
    seen_ids: set[str] = set()
    seen_dois: set[str] = set()
    for raw in raw_sources:
        if not isinstance(raw, dict):
            raise ValueError("each source acquisition record must be an object")
        source_id = str(raw.get("source_id") or "").strip()
        doi = str(raw.get("doi") or "").strip().lower()
        if not source_id or source_id in seen_ids:
            raise ValueError("source_id values must be non-empty and unique")
        if not doi or doi in seen_dois:
            raise ValueError("doi values must be non-empty and unique")
        seen_ids.add(source_id)
        seen_dois.add(doi)

        directional_status = str(raw.get("directional_status") or "").strip()
        shared_step = str(raw.get("shared_second_step_status") or "").strip()
        access_status = str(raw.get("access_status") or "").strip()
        numeric_status = str(raw.get("numeric_effect_status") or "").strip()
        dependency_status = str(raw.get("dependency_moderation_status") or "").strip()
        if directional_status not in ALLOWED_DIRECTIONAL_STATUS:
            raise ValueError(f"{source_id}: invalid directional_status")
        if shared_step not in ALLOWED_STEP_STATUS:
            raise ValueError(f"{source_id}: invalid shared_second_step_status")
        if access_status not in ALLOWED_ACCESS_STATUS:
            raise ValueError(f"{source_id}: invalid access_status")
        if numeric_status not in ALLOWED_ADMISSION_STATUS:
            raise ValueError(f"{source_id}: invalid numeric_effect_status")
        if dependency_status not in ALLOWED_ADMISSION_STATUS:
            raise ValueError(f"{source_id}: invalid dependency_moderation_status")

        numeric_gate = _require_bool_map(
            raw.get("numeric_gate"),
            NUMERIC_GATE_FIELDS,
            source_id=source_id,
            label="numeric_gate",
        )
        dependency_gate = _require_bool_map(
            raw.get("dependency_gate"),
            DEPENDENCY_GATE_FIELDS,
            source_id=source_id,
            label="dependency_gate",
        )
        supplements_raw = raw.get("supplements")
        if not isinstance(supplements_raw, list):
            raise ValueError(f"{source_id}: supplements must be a list")
        supplements: list[Mapping[str, object]] = []
        seen_files: set[str] = set()
        for supplement in supplements_raw:
            if not isinstance(supplement, dict):
                raise ValueError(f"{source_id}: supplement rows must be objects")
            filename = str(supplement.get("filename") or "").strip()
            role = str(supplement.get("role") or "").strip()
            sufficient = supplement.get("sufficient_for_numeric_gate")
            if not filename or filename in seen_files:
                raise ValueError(
                    f"{source_id}: supplement filenames must be non-empty and unique"
                )
            if role not in ALLOWED_SUPPLEMENT_ROLE:
                raise ValueError(f"{source_id}: invalid supplement role for {filename}")
            if not isinstance(sufficient, bool):
                raise ValueError(f"{source_id}: supplement sufficiency must be boolean")
            if sufficient:
                raise ValueError(
                    f"{source_id}: publisher-listed supplement metadata cannot by itself "
                    "satisfy the numeric gate"
                )
            seen_files.add(filename)
            supplements.append(
                {
                    "filename": filename,
                    "role": role,
                    "sufficient_for_numeric_gate": sufficient,
                }
            )

        source = SourceAcquisition(
            source_id=source_id,
            taxon=str(raw.get("taxon") or "").strip(),
            doi=doi,
            directional_status=directional_status,
            directional_pattern=str(raw.get("directional_pattern") or "").strip(),
            shared_second_step_status=shared_step,
            access_status=access_status,
            numeric_effect_status=numeric_status,
            dependency_moderation_status=dependency_status,
            numeric_gate=numeric_gate,
            dependency_gate=dependency_gate,
            supplements=tuple(supplements),
            issue_number=int(raw.get("issue_number") or 0),
            next_action=str(raw.get("next_action") or "").strip(),
            claim_boundary=str(raw.get("claim_boundary") or "").strip(),
        )
        if not source.taxon or not source.directional_pattern:
            raise ValueError(f"{source_id}: taxon and directional_pattern are required")
        if source.issue_number != 92:
            raise ValueError(f"{source_id}: issue_number must be 92")
        if not source.next_action or not source.claim_boundary:
            raise ValueError(f"{source_id}: next_action and claim_boundary are required")
        if (numeric_status == "ready") != numeric_effect_ready(source):
            raise ValueError(f"{source_id}: numeric_effect_status disagrees with numeric gate")
        if (dependency_status == "ready") != dependency_moderation_ready(source):
            raise ValueError(
                f"{source_id}: dependency_moderation_status disagrees with dependency gate"
            )
        if shared_step == "supports" and not numeric_gate["exact_geographic_mapping"]:
            raise ValueError(
                f"{source_id}: shared-step support requires exact geographic mapping"
            )
        output.append(source)

    if {row.source_id for row in output} != REQUIRED_SOURCE_IDS:
        found = {row.source_id for row in output}
        missing = sorted(REQUIRED_SOURCE_IDS - found)
        extra = sorted(found - REQUIRED_SOURCE_IDS)
        raise ValueError(
            f"priority independent sources mismatch; missing={missing}, extra={extra}"
        )
    return tuple(output)


def validate_source_native_links(
    sources: Sequence[SourceAcquisition],
    native_evidence_path: str | Path,
) -> None:
    import csv

    with Path(native_evidence_path).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or "source_id" not in rows[0]:
        raise ValueError("source-native evidence registry must contain source_id")
    native_ids = {str(row["source_id"]).strip() for row in rows}
    missing = sorted({row.source_id for row in sources} - native_ids)
    if missing:
        raise ValueError(
            "priority sources missing from source-native evidence: " + ", ".join(missing)
        )


def summarize(sources: Iterable[SourceAcquisition]) -> dict[str, object]:
    rows = tuple(sources)
    numeric_ready = sorted(row.source_id for row in rows if numeric_effect_ready(row))
    dependency_ready = sorted(
        row.source_id for row in rows if dependency_moderation_ready(row)
    )
    directional_active = sorted(
        row.source_id for row in rows if row.directional_status == "active_B_grade"
    )
    supplement_routes = sorted(row.source_id for row in rows if row.supplements)
    shared_step_support = sorted(
        row.source_id
        for row in rows
        if row.shared_second_step_status == "supports"
    )
    return {
        "n_priority_sources": len(rows),
        "directional_B_grade_active_sources": directional_active,
        "publisher_supplement_routes_confirmed_sources": supplement_routes,
        "numeric_effect_ready_sources": numeric_ready,
        "dependency_moderation_ready_sources": dependency_ready,
        "shared_second_step_support_sources": shared_step_support,
        "independent_numeric_test_status": (
            "ready" if numeric_ready else "blocked_no_population_level_numeric_source"
        ),
        "dependency_moderation_test_status": (
            "ready"
            if dependency_ready
            else "blocked_no_dependency_matched_numeric_source"
        ),
        "current_directional_reading": (
            "The three priority lineages retain B-grade response-shape information, "
            "but none currently demonstrates an explicitly localized Oshima-to-Toshima "
            "shared second step."
        ),
        "claim_boundary": (
            "Supplement filenames and publisher metadata are acquisition routes, not "
            "trait values. No effect size, equivalence result, dependency class or exact "
            "breakpoint is admitted until the corresponding source gates are satisfied."
        ),
    }


def run_audit(
    manifest_path: str | Path,
    native_evidence_path: str | Path,
) -> dict[str, object]:
    sources = load_manifest(manifest_path)
    validate_source_native_links(sources, native_evidence_path)
    return {
        "sources": [
            {
                "source_id": row.source_id,
                "taxon": row.taxon,
                "doi": row.doi,
                "directional_status": row.directional_status,
                "directional_pattern": row.directional_pattern,
                "shared_second_step_status": row.shared_second_step_status,
                "access_status": row.access_status,
                "numeric_effect_status": row.numeric_effect_status,
                "dependency_moderation_status": row.dependency_moderation_status,
                "numeric_gate": dict(row.numeric_gate),
                "dependency_gate": dict(row.dependency_gate),
                "supplements": [dict(item) for item in row.supplements],
                "issue_number": row.issue_number,
                "next_action": row.next_action,
                "claim_boundary": row.claim_boundary,
            }
            for row in sources
        ],
        "summary": summarize(sources),
    }


def write_report(path: str | Path, report: Mapping[str, object]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
