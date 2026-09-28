"""Two-stage ranking of marginal Issue #91 field effort.

Mandatory structural/pilot-dispersion gates always outrank optional marginal
replication.  Only after those gates are satisfied do we use the RACH-style
expected resolvability gain from :mod:`channel_id.causal_admissibility`.

The ranking is design-relative. Outcome probabilities are prespecified planning
assumptions, not empirical probabilities of mechanisms or outcomes.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from .causal_admissibility import CandidateObservation, expected_observation_value


MANDATORY_GATES = (
    "linked_ids_and_effort",
    "no_visit_svd_control",
    "svd_two_independent_plants",
    "open_two_independent_plants",
    "bagged_two_independent_plants",
    "supplemental_two_independent_plants",
    "terminal_fruit_seed_linkage",
)


@dataclass(frozen=True)
class PilotGateState:
    linked_ids_and_effort: bool
    no_visit_svd_control: bool
    svd_two_independent_plants: bool
    open_two_independent_plants: bool
    bagged_two_independent_plants: bool
    supplemental_two_independent_plants: bool
    terminal_fruit_seed_linkage: bool

    def missing(self) -> tuple[str, ...]:
        return tuple(name for name in MANDATORY_GATES if not bool(getattr(self, name)))


@dataclass(frozen=True)
class FieldEffortOption:
    name: str
    gate_target: str | None
    candidate: CandidateObservation | None = None
    note: str = ""


@dataclass(frozen=True)
class RankedFieldEffort:
    name: str
    tier: int
    reason: str
    expected_resolvability_gain: float | None
    expected_gain_per_cost: float | None


def rank_issue91_field_effort(
    gate_state: PilotGateState,
    accepted_rows: Sequence[dict],
    switches: Sequence[str],
    options: Iterable[FieldEffortOption],
) -> tuple[RankedFieldEffort, ...]:
    """Rank field actions without allowing optional work to bypass a missing gate.

    Tier 1 contains options that repair currently missing mandatory gates.  Their
    order follows ``MANDATORY_GATES``.  Tier 2 contains optional/marginal actions
    ranked by expected resolvability gain per declared cost.  Options aimed at an
    already-satisfied mandatory gate are treated as marginal and therefore tier 2.
    """
    missing = gate_state.missing()
    missing_rank = {name: i for i, name in enumerate(missing)}
    mandatory: list[tuple[int, RankedFieldEffort]] = []
    marginal: list[RankedFieldEffort] = []

    for option in options:
        if option.gate_target in missing_rank:
            mandatory.append((
                missing_rank[option.gate_target],
                RankedFieldEffort(
                    name=option.name,
                    tier=1,
                    reason=f"repairs missing mandatory gate: {option.gate_target}",
                    expected_resolvability_gain=None,
                    expected_gain_per_cost=None,
                ),
            ))
            continue

        if option.candidate is None:
            value_gain = None
            value_eff = None
            reason = "optional effort with no declared outcome model"
        else:
            value = expected_observation_value(accepted_rows, switches, option.candidate)
            value_gain = value.expected_resolvability_gain
            value_eff = value.expected_gain_per_cost
            reason = "marginal effort ranked by declared expected resolvability gain per cost"
        marginal.append(RankedFieldEffort(
            name=option.name,
            tier=2,
            reason=reason,
            expected_resolvability_gain=value_gain,
            expected_gain_per_cost=value_eff,
        ))

    mandatory.sort(key=lambda item: item[0])
    marginal.sort(
        key=lambda item: (
            item.expected_gain_per_cost is not None,
            item.expected_gain_per_cost if item.expected_gain_per_cost is not None else float("-inf"),
            item.expected_resolvability_gain if item.expected_resolvability_gain is not None else float("-inf"),
        ),
        reverse=True,
    )
    return tuple(item for _, item in mandatory) + tuple(marginal)
