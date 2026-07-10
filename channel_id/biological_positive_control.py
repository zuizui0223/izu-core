"""Pre-key eligibility gate for a biological image positive control.

A regional key must not be joined when the blind cards cannot support the
predeclared floral trait.  Exclusion is never converted to a zero trait score.
"""
from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class PositiveControlGate:
    cards_reviewed: int
    stage0_eligible_cards: int
    scored_cards: int
    distinct_score_levels: int
    pre_key_status: str
    regional_key_join_permitted: str
    eligible_for_roi_selection: str
    eligible_for_broad_specialist_holdout: str
    reason: str


def _clean(value: object) -> str:
    return str(value or "").strip().lower()


def evaluate_pre_key_gate(path: str | Path) -> PositiveControlGate:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {
        "card_id", "flowering_state", "focal_flower_visible",
        "interior_visible", "comparable_for_guide_score", "guide_score_0_3",
    }
    if not rows or not required.issubset(rows[0]):
        raise ValueError("positive-control blind table is empty or incomplete")
    ids = [str(row["card_id"]).strip() for row in rows]
    if any(not value for value in ids) or len(ids) != len(set(ids)):
        raise ValueError("card_id must be nonempty and unique")

    eligible = [
        row for row in rows
        if _clean(row["flowering_state"]) == "open"
        and _clean(row["focal_flower_visible"]) == "yes"
        and _clean(row["interior_visible"]) == "yes"
        and _clean(row["comparable_for_guide_score"]) == "yes"
    ]
    scores: list[int] = []
    for row in eligible:
        text = str(row.get("guide_score_0_3", "")).strip()
        if not text:
            continue
        score = int(text)
        if score not in range(4):
            raise ValueError("guide_score_0_3 must be 0, 1, 2 or 3")
        scores.append(score)

    levels = len(set(scores))
    sufficient = len(eligible) >= 3 and len(scores) >= 3 and levels >= 2
    if sufficient:
        status = "ready_for_key_join"
        key_join = "yes"
        reason = "Blind stage 0 retained at least three scored cards across at least two score levels."
    elif len(eligible) < 3:
        status = "insufficient_stage0"
        key_join = "no"
        reason = "Fewer than three cards show a comparable inner corolla surface; excluded cards are not zero scores."
    elif len(scores) < 3:
        status = "insufficient_scoring"
        key_join = "no"
        reason = "Fewer than three eligible cards have frozen guide scores."
    else:
        status = "insufficient_score_range"
        key_join = "no"
        reason = "Blind scores contain fewer than two distinct guide levels."

    return PositiveControlGate(
        cards_reviewed=len(rows),
        stage0_eligible_cards=len(eligible),
        scored_cards=len(scores),
        distinct_score_levels=levels,
        pre_key_status=status,
        regional_key_join_permitted=key_join,
        eligible_for_roi_selection="no",
        eligible_for_broad_specialist_holdout="no",
        reason=reason,
    )


def gate_dict(gate: PositiveControlGate) -> dict[str, object]:
    return asdict(gate)
