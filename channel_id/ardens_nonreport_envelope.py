"""Logical uncertainty envelope for the *Bombus ardens* hierarchy input.

The direct Inoue 1986 audit distinguishes a positive rate from a non-report after
recorded effort and from a unit outside effort coverage. This module asks a
limited robustness question:

    Does the small pollinator-hierarchy pattern ranking depend on coding every
    non-positive *B. ardens* table state as zero availability/context?

For each island with a current zero coding but no direct positive-rate proof of
zero, the envelope enumerates 0/1 *model-context codings*. It does not estimate
occupancy, detection probability, pollination effectiveness, or a probability
that any configuration is true. All configurations are logical sensitivity cases,
not equally likely posterior states.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from itertools import product
from statistics import mean
from typing import Sequence

from channel_id.pollinator_hierarchy_counterfactual import IslandRecord, score
from channel_id.pollinator_regime_evidence_audit import AuditRow


UNCERTAIN_ZERO_STATUSES = frozenset({
    "not_reported_in_rate_table_after_recorded_effort",
    "no_inoue1986_effort_row_for_unit",
})
MODEL_NAMES = ("pollinator_hierarchy", "environment_only", "isolation_order")


@dataclass(frozen=True)
class EnvelopeConfiguration:
    configuration_id: str
    coded_one_islands: tuple[str, ...]
    coded_zero_islands: tuple[str, ...]
    pollinator_hierarchy_mae: float
    environment_only_mae: float
    isolation_order_mae: float
    pollinator_hierarchy_rank: int
    pollinator_hierarchy_is_co_winner: bool
    pollinator_hierarchy_is_unique_winner: bool


def derive_uncertain_ardens_islands(records: Sequence[IslandRecord], audit_rows: Sequence[AuditRow]) -> tuple[str, ...]:
    """Return zero-coded non-large-Bombus islands not proved absent by the audit.

    A direct positive rate remains fixed at one in the locked table. A large
    *B. diversus* mainland state is not varied because the hierarchy score assigns
    it stage zero regardless of the *B. ardens* indicator.
    """
    record_by_island = {record.island_id: record for record in records}
    uncertain: list[str] = []
    for row in audit_rows:
        if row.model_indicator != "bombus_ardens" or row.model_value != 0:
            continue
        record = record_by_island.get(row.island_id)
        if record is None or record.bombus_diversus:
            continue
        if row.source_status in UNCERTAIN_ZERO_STATUSES:
            uncertain.append(row.island_id)
    return tuple(sorted(set(uncertain)))


def _score_map(records: Sequence[IslandRecord]) -> dict[str, float]:
    result = score(list(records))
    rows = result["model_scores"]
    return {str(row["model"]): float(row["mean_absolute_error"]) for row in rows}  # type: ignore[index]


def _rank(score_map: dict[str, float], model: str) -> tuple[int, bool, bool]:
    if model not in score_map:
        raise ValueError(f"missing model score for {model}")
    value = score_map[model]
    minimum = min(score_map.values())
    winners = [name for name, candidate in score_map.items() if candidate == minimum]
    rank = 1 + sum(candidate < value for candidate in score_map.values())
    return rank, model in winners, winners == [model]


def enumerate_ardens_context_envelope(
    records: Sequence[IslandRecord],
    uncertain_islands: Sequence[str],
) -> tuple[EnvelopeConfiguration, ...]:
    """Enumerate all 0/1 context-coding cases for declared uncertain islands."""
    if len(set(uncertain_islands)) != len(tuple(uncertain_islands)):
        raise ValueError("uncertain_islands must be unique")
    by_island = {record.island_id: record for record in records}
    if set(uncertain_islands) - set(by_island):
        raise ValueError("uncertain_islands contain unknown record IDs")
    ordered = tuple(sorted(uncertain_islands))
    configurations: list[EnvelopeConfiguration] = []
    for bits in product((0, 1), repeat=len(ordered)):
        overrides = dict(zip(ordered, bits))
        modified = tuple(replace(record, bombus_ardens=float(overrides.get(record.island_id, record.bombus_ardens))) for record in records)
        scores = _score_map(modified)
        rank, co_winner, unique_winner = _rank(scores, "pollinator_hierarchy")
        configurations.append(EnvelopeConfiguration(
            configuration_id="ardens_context_" + "".join(str(bit) for bit in bits),
            coded_one_islands=tuple(island for island, bit in zip(ordered, bits) if bit == 1),
            coded_zero_islands=tuple(island for island, bit in zip(ordered, bits) if bit == 0),
            pollinator_hierarchy_mae=scores["pollinator_hierarchy"],
            environment_only_mae=scores["environment_only"],
            isolation_order_mae=scores["isolation_order"],
            pollinator_hierarchy_rank=rank,
            pollinator_hierarchy_is_co_winner=co_winner,
            pollinator_hierarchy_is_unique_winner=unique_winner,
        ))
    return tuple(configurations)


def summarize_envelope(configurations: Sequence[EnvelopeConfiguration], uncertain_islands: Sequence[str]) -> dict[str, object]:
    if not configurations:
        raise ValueError("configurations cannot be empty")
    count = len(configurations)
    co_winners = [row for row in configurations if row.pollinator_hierarchy_is_co_winner]
    unique_winners = [row for row in configurations if row.pollinator_hierarchy_is_unique_winner]
    ranks = [row.pollinator_hierarchy_rank for row in configurations]
    return {
        "schema_version": 1,
        "boundary": (
            "Logical sensitivity envelope over availability/context codings for islands whose Inoue 1986 *Bombus ardens* row is a non-report or lies outside table effort coverage. Configurations have no probability weights and do not estimate occupancy, detection, absence, or pollination effectiveness."
        ),
        "uncertain_ardens_context_islands": list(uncertain_islands),
        "configuration_count": count,
        "pollinator_hierarchy_co_winner_count": len(co_winners),
        "pollinator_hierarchy_co_winner_fraction": len(co_winners) / count,
        "pollinator_hierarchy_unique_winner_count": len(unique_winners),
        "pollinator_hierarchy_unique_winner_fraction": len(unique_winners) / count,
        "pollinator_hierarchy_best_rank": min(ranks),
        "pollinator_hierarchy_worst_rank": max(ranks),
        "mean_pollinator_hierarchy_mae": mean(row.pollinator_hierarchy_mae for row in configurations),
        "mean_environment_only_mae": mean(row.environment_only_mae for row in configurations),
        "mean_isolation_order_mae": mean(row.isolation_order_mae for row in configurations),
    }


def configuration_rows(configurations: Sequence[EnvelopeConfiguration]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in configurations:
        rows.append({
            "configuration_id": row.configuration_id,
            "ardens_context_coded_one_islands": ";".join(row.coded_one_islands),
            "ardens_context_coded_zero_islands": ";".join(row.coded_zero_islands),
            "pollinator_hierarchy_mae": f"{row.pollinator_hierarchy_mae:.4f}",
            "environment_only_mae": f"{row.environment_only_mae:.4f}",
            "isolation_order_mae": f"{row.isolation_order_mae:.4f}",
            "pollinator_hierarchy_rank": str(row.pollinator_hierarchy_rank),
            "pollinator_hierarchy_is_co_winner": str(row.pollinator_hierarchy_is_co_winner).lower(),
            "pollinator_hierarchy_is_unique_winner": str(row.pollinator_hierarchy_is_unique_winner).lower(),
        })
    return rows
