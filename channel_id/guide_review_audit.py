"""Audit completed blinded guide-photo reviews before any manual constraint use.

This module is deliberately downstream of the blind sheets.  It writes a
unit-level decision ledger that records why a source record is eligible or
excluded, and it reports descriptive reviewer agreement only among scorable
pairs.  It does not create or edit model constraints.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Sequence

from channel_id.guide_photo_review import (
    VALID_ISLANDS,
    _accepted_trait_score,
    _index_unique,
    _text,
)


UNIT_AUDIT_COLUMNS = (
    "blind_unit_id", "observation_unit_id", "source_type", "record_id",
    "verified_island_id", "geographic_review_status", "taxon_review_status",
    "trait_reviewer_a_id", "trait_reviewer_b_id", "reviewer_identity_status",
    "trait_score_reviewer_a", "trait_score_reviewer_b", "trait_score_difference",
    "unit_disposition", "exclusion_code", "audit_note",
)
AGREEMENT_COLUMNS = (
    "metric", "value", "boundary",
)


@dataclass(frozen=True)
class GuideReviewAudit:
    unit_rows: tuple[dict[str, str], ...]
    agreement_rows: tuple[dict[str, str], ...]
    eligible_observation_unit_ids: tuple[str, ...]


def _identity_status(review_a: dict[str, str], review_b: dict[str, str]) -> str:
    a = _text(review_a, "trait_reviewer_id")
    b = _text(review_b, "trait_reviewer_id")
    if not a or not b:
        return "missing_reviewer_identity"
    if a.casefold() == b.casefold():
        return "same_reviewer_identity"
    return "distinct_reviewer_ids"


def _reviewer_sheet_ids(rows: Sequence[dict[str, str]]) -> tuple[str, ...]:
    return tuple(sorted({_text(row, "trait_reviewer_id") for row in rows if _text(row, "trait_reviewer_id")}))


def _accepted_geography(geo: dict[str, str]) -> tuple[bool, str]:
    if _text(geo, "geographic_review_status").casefold() != "accepted":
        return False, "geographic_review_not_accepted"
    if _text(geo, "taxon_review_status").casefold() != "accepted":
        return False, "taxon_review_not_accepted"
    if _text(geo, "verified_island_id") not in VALID_ISLANDS:
        return False, "verified_island_invalid_or_blank"
    return True, ""


def audit_completed_reviews(
    geographic_rows: Sequence[dict[str, str]],
    review_a_rows: Sequence[dict[str, str]],
    review_b_rows: Sequence[dict[str, str]],
    key_rows: Sequence[dict[str, str]],
    *,
    maximum_reviewer_score_difference: int = 1,
) -> GuideReviewAudit:
    """Return an unblinded decision ledger and descriptive agreement summary.

    `eligible_for_manual_constraint_review` means only that all administrative
    and double-blind gates passed.  It remains non-binding biological evidence
    until a human inspects the source unit and approves a draft constraint.
    """
    if maximum_reviewer_score_difference < 0:
        raise ValueError("maximum_reviewer_score_difference cannot be negative")
    geographic = _index_unique(geographic_rows, "observation_unit_id", "geographic review")
    review_a = _index_unique(review_a_rows, "blind_unit_id", "trait review A")
    review_b = _index_unique(review_b_rows, "blind_unit_id", "trait review B")
    key = _index_unique(key_rows, "blind_unit_id", "blind key")

    a_sheet_ids = _reviewer_sheet_ids(review_a_rows)
    b_sheet_ids = _reviewer_sheet_ids(review_b_rows)
    unit_rows: list[dict[str, str]] = []
    scorable_pairs: list[tuple[int, int]] = []
    eligible_ids: list[str] = []
    exclusions: Counter[str] = Counter()

    for blind_id, key_row in sorted(key.items()):
        geo = geographic.get(_text(key_row, "observation_unit_id"))
        left = review_a.get(blind_id)
        right = review_b.get(blind_id)
        row = {
            "blind_unit_id": blind_id,
            "observation_unit_id": _text(key_row, "observation_unit_id"),
            "source_type": _text(key_row, "source_type") or _text(geo or {}, "source_type") or "unknown",
            "record_id": _text(key_row, "record_id") or _text(geo or {}, "record_id"),
            "verified_island_id": _text(geo or {}, "verified_island_id"),
            "geographic_review_status": _text(geo or {}, "geographic_review_status"),
            "taxon_review_status": _text(geo or {}, "taxon_review_status"),
            "trait_reviewer_a_id": _text(left or {}, "trait_reviewer_id"),
            "trait_reviewer_b_id": _text(right or {}, "trait_reviewer_id"),
            "reviewer_identity_status": "",
            "trait_score_reviewer_a": "",
            "trait_score_reviewer_b": "",
            "trait_score_difference": "",
            "unit_disposition": "excluded",
            "exclusion_code": "",
            "audit_note": "",
        }
        if geo is None:
            row["exclusion_code"] = "missing_geographic_review_row"
        elif left is None or right is None:
            row["exclusion_code"] = "missing_trait_review_row"
        else:
            geo_ok, geo_code = _accepted_geography(geo)
            identity = _identity_status(left, right)
            row["reviewer_identity_status"] = identity
            score_a = _accepted_trait_score(left)
            score_b = _accepted_trait_score(right)
            if score_a is not None:
                row["trait_score_reviewer_a"] = str(score_a)
            if score_b is not None:
                row["trait_score_reviewer_b"] = str(score_b)
            if score_a is not None and score_b is not None:
                difference = abs(score_a - score_b)
                row["trait_score_difference"] = str(difference)
                scorable_pairs.append((score_a, score_b))
            if not geo_ok:
                row["exclusion_code"] = geo_code
            elif identity != "distinct_reviewer_ids":
                row["exclusion_code"] = identity
            elif score_a is None:
                row["exclusion_code"] = "trait_review_a_not_accepted_or_unscorable"
            elif score_b is None:
                row["exclusion_code"] = "trait_review_b_not_accepted_or_unscorable"
            elif abs(score_a - score_b) > maximum_reviewer_score_difference:
                row["exclusion_code"] = "reviewer_score_difference_exceeds_threshold"
            else:
                row["unit_disposition"] = "eligible_for_manual_constraint_review"
                row["audit_note"] = "All geographic, taxon, independent-reviewer, trait-gate, and score-difference checks passed; still non-binding."
                eligible_ids.append(row["observation_unit_id"])
        if row["unit_disposition"] == "excluded":
            exclusions[row["exclusion_code"] or "unclassified_exclusion"] += 1
        unit_rows.append(row)

    exact = sum(a == b for a, b in scorable_pairs)
    within = sum(abs(a - b) <= maximum_reviewer_score_difference for a, b in scorable_pairs)
    mean_abs = (sum(abs(a - b) for a, b in scorable_pairs) / len(scorable_pairs)) if scorable_pairs else None
    boundary = (
        "Descriptive agreement among scorable double-blind pairs only; no chance-corrected reliability estimate is reported because the expected sample is small and ordinal category prevalence can dominate such statistics."
    )
    agreement_rows = [
        {"metric": "key_units", "value": str(len(key)), "boundary": boundary},
        {"metric": "eligible_for_manual_constraint_review", "value": str(len(eligible_ids)), "boundary": boundary},
        {"metric": "scorable_trait_pairs", "value": str(len(scorable_pairs)), "boundary": boundary},
        {"metric": "exact_score_agreement_fraction", "value": "" if not scorable_pairs else f"{exact / len(scorable_pairs):.6f}", "boundary": boundary},
        {"metric": f"within_{maximum_reviewer_score_difference}_ordinal_step_fraction", "value": "" if not scorable_pairs else f"{within / len(scorable_pairs):.6f}", "boundary": boundary},
        {"metric": "mean_absolute_score_difference", "value": "" if mean_abs is None else f"{mean_abs:.6f}", "boundary": boundary},
        {"metric": "trait_review_A_distinct_ids", "value": ";".join(a_sheet_ids), "boundary": boundary},
        {"metric": "trait_review_B_distinct_ids", "value": ";".join(b_sheet_ids), "boundary": boundary},
    ]
    for code, count in sorted(exclusions.items()):
        agreement_rows.append({"metric": f"excluded:{code}", "value": str(count), "boundary": boundary})
    return GuideReviewAudit(tuple(unit_rows), tuple(agreement_rows), tuple(eligible_ids))
