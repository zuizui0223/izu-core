"""Track completion and island-level readiness of blinded guide-photo reviews.

This module consumes the audit ledger rather than proxy queues.  Island counts
begin only after geographic and taxonomic acceptance; a nearest-island proxy is
never counted as a verified unit.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Sequence

from channel_id.guide_photo_review import VALID_ISLANDS
from channel_id.guide_review_audit import GuideReviewAudit


UNIT_PROGRESS_COLUMNS = (
    "blind_unit_id", "observation_unit_id", "verified_island_id",
    "unit_disposition", "exclusion_code", "next_required_action",
    "counted_in_verified_island_pool", "boundary",
)
ISLAND_PROGRESS_COLUMNS = (
    "island_id", "verified_geographic_taxon_units", "awaiting_trait_review_units",
    "eligible_for_manual_constraint_review_units", "minimum_units_required",
    "eligible_shortfall", "potential_shortfall_if_all_pending_pass",
    "readiness_status", "boundary",
)


@dataclass(frozen=True)
class GuideReviewProgress:
    unit_rows: tuple[dict[str, str], ...]
    island_rows: tuple[dict[str, str], ...]


def _next_action(row: dict[str, str]) -> str:
    if row["unit_disposition"] == "eligible_for_manual_constraint_review":
        return "inspect_source_record_and_manual_biological_confirmation"
    code = row["exclusion_code"]
    actions = {
        "missing_geographic_review_row": "restore_or_complete_geographic_taxonomic_review",
        "geographic_review_not_accepted": "resolve_or_document_geographic_rejection",
        "taxon_review_not_accepted": "resolve_or_document_taxon_rejection",
        "verified_island_invalid_or_blank": "resolve_verified_island_from_source_record",
        "missing_trait_review_row": "complete_missing_blinded_trait_review",
        "missing_reviewer_identity": "record_reviewer_identity_or_repeat_blinded_review",
        "same_reviewer_identity": "obtain_independent_second_blinded_review",
        "trait_review_a_not_accepted_or_unscorable": "repeat_or_replace_trait_review_A",
        "trait_review_b_not_accepted_or_unscorable": "repeat_or_replace_trait_review_B",
        "reviewer_score_difference_exceeds_threshold": "third_independent_blinded_review_or_exclude",
    }
    return actions.get(code, "inspect_audit_ledger_and_resolve")


def _is_verified_geo_taxon(row: dict[str, str]) -> bool:
    return (
        row["geographic_review_status"].casefold() == "accepted"
        and row["taxon_review_status"].casefold() == "accepted"
        and row["verified_island_id"] in VALID_ISLANDS
    )


def _awaiting_trait(row: dict[str, str]) -> bool:
    return _is_verified_geo_taxon(row) and row["unit_disposition"] != "eligible_for_manual_constraint_review"


def build_guide_review_progress(
    audit: GuideReviewAudit,
    *,
    min_units_per_island: int = 3,
) -> GuideReviewProgress:
    """Return a task ledger and verified-island readiness counts.

    `awaiting_trait_review_units` includes every verified geography/taxon unit
    that has not passed all trait-review gates.  It is a potential count, not
    trait evidence and not a promise that the unit will be eligible.
    """
    if min_units_per_island < 1:
        raise ValueError("min_units_per_island must be positive")
    boundary = (
        "Counts begin only after accepted geographic and taxonomic review. Pending "
        "units are not guide evidence; proxy queue counts, unverified localities, "
        "and public-photo selection bias are intentionally excluded."
    )
    units: list[dict[str, str]] = []
    verified: dict[str, int] = defaultdict(int)
    pending: dict[str, int] = defaultdict(int)
    eligible: dict[str, int] = defaultdict(int)
    for row in audit.unit_rows:
        verified_ok = _is_verified_geo_taxon(row)
        island = row["verified_island_id"] if verified_ok else ""
        if verified_ok:
            verified[island] += 1
        if _awaiting_trait(row):
            pending[island] += 1
        if verified_ok and row["unit_disposition"] == "eligible_for_manual_constraint_review":
            eligible[island] += 1
        units.append({
            "blind_unit_id": row["blind_unit_id"],
            "observation_unit_id": row["observation_unit_id"],
            "verified_island_id": island,
            "unit_disposition": row["unit_disposition"],
            "exclusion_code": row["exclusion_code"],
            "next_required_action": _next_action(row),
            "counted_in_verified_island_pool": str(verified_ok).lower(),
            "boundary": boundary,
        })
    islands = sorted(set(verified) | set(pending) | set(eligible))
    summaries: list[dict[str, str]] = []
    for island in islands:
        eligible_n = eligible[island]
        pending_n = pending[island]
        eligible_shortfall = max(0, min_units_per_island - eligible_n)
        potential_shortfall = max(0, min_units_per_island - eligible_n - pending_n)
        readiness = (
            "ready_for_manual_pairwise_direction_check"
            if eligible_n >= min_units_per_island
            else "pending_existing_verified_units"
            if potential_shortfall == 0
            else "needs_additional_independent_verified_source_records"
        )
        summaries.append({
            "island_id": island,
            "verified_geographic_taxon_units": str(verified[island]),
            "awaiting_trait_review_units": str(pending_n),
            "eligible_for_manual_constraint_review_units": str(eligible_n),
            "minimum_units_required": str(min_units_per_island),
            "eligible_shortfall": str(eligible_shortfall),
            "potential_shortfall_if_all_pending_pass": str(potential_shortfall),
            "readiness_status": readiness,
            "boundary": boundary,
        })
    return GuideReviewProgress(tuple(units), tuple(summaries))
