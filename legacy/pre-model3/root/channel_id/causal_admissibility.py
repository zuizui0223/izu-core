"""Small RACH-style diagnostics for a predeclared causal-program grammar.

The module does not discover causes and does not turn simulator frequencies into
empirical posterior probabilities.  It summarises a caller-supplied admissible
region: rows that have already passed biological constraints and observation
compatibility checks.

The intended use in ``izu-core`` is structural: keep competing explanations
visible, measure how unresolved the declared switch space remains, and ask which
additional observation would reduce that ambiguity.  All conclusions are
conditional on the declared grammar, sampling design, acceptance rule, and priors.
"""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from typing import Callable, Iterable, Sequence


@dataclass(frozen=True)
class CausalAdmissibility:
    switch: str
    fraction_on: float
    n_on: int
    n_accepted: int


@dataclass(frozen=True)
class AdmissibilitySummary:
    n_accepted: int
    n_switches: int
    switch_admissibility: tuple[CausalAdmissibility, ...]
    degeneracy_bits: float
    max_degeneracy_bits: float
    resolvability: float
    explanation_mass: tuple[tuple[frozenset[str], float], ...]


@dataclass(frozen=True)
class ObservationOutcome:
    """One possible result of a candidate observation.

    ``predicate`` selects the subset of the current admissible region that would
    remain compatible if that outcome were observed.  ``probability`` is a
    predeclared design probability; it is not estimated from the filtered rows.
    """

    name: str
    probability: float
    predicate: Callable[[dict], bool]


@dataclass(frozen=True)
class CandidateObservation:
    name: str
    outcomes: tuple[ObservationOutcome, ...]
    cost: float = 1.0


@dataclass(frozen=True)
class ObservationValue:
    candidate: str
    expected_resolvability_gain: float
    expected_gain_per_cost: float
    baseline_resolvability: float


def _switch_vector(row: dict, switches: Sequence[str]) -> tuple[bool, ...]:
    missing = [name for name in switches if name not in row]
    if missing:
        raise KeyError(f"accepted row missing switch columns: {', '.join(missing)}")
    return tuple(bool(row[name]) for name in switches)


def _joint_entropy(vectors: Iterable[tuple[bool, ...]]) -> float:
    values = tuple(vectors)
    if not values:
        return 0.0
    counts = Counter(values)
    n = len(values)
    return -sum((count / n) * math.log2(count / n) for count in counts.values())


def causal_resolvability(accepted_rows: Sequence[dict], switches: Sequence[str]) -> float:
    """Return ``1 - H(S|A)/K`` for the declared binary switch vector."""

    if not switches:
        return 1.0
    if not accepted_rows:
        return float("nan")
    entropy = _joint_entropy(_switch_vector(row, switches) for row in accepted_rows)
    value = 1.0 - entropy / len(switches)
    return min(1.0, max(0.0, value))


def summarise_admissible_region(
    accepted_rows: Sequence[dict],
    switches: Sequence[str],
) -> AdmissibilitySummary:
    """Summarise a caller-defined admissible region without selecting one cause."""

    rows = tuple(accepted_rows)
    names = tuple(switches)
    if len(set(names)) != len(names):
        raise ValueError("switch names must be unique")

    vectors = tuple(_switch_vector(row, names) for row in rows)
    entropy = _joint_entropy(vectors)
    maximum = float(len(names))
    resolvability = float("nan") if not rows else (
        1.0 if not names else min(1.0, max(0.0, 1.0 - entropy / maximum))
    )

    per_switch = tuple(
        CausalAdmissibility(
            switch=name,
            fraction_on=(sum(bool(row[name]) for row in rows) / len(rows)) if rows else float("nan"),
            n_on=sum(bool(row[name]) for row in rows),
            n_accepted=len(rows),
        )
        for name in names
    )

    explanation_counts = Counter(
        frozenset(name for name, is_on in zip(names, vector) if is_on)
        for vector in vectors
    )
    explanation_mass = tuple(
        sorted(
            (
                (explanation, count / len(rows))
                for explanation, count in explanation_counts.items()
            ),
            key=lambda item: (-item[1], tuple(sorted(item[0]))),
        )
    ) if rows else ()

    return AdmissibilitySummary(
        n_accepted=len(rows),
        n_switches=len(names),
        switch_admissibility=per_switch,
        degeneracy_bits=entropy,
        max_degeneracy_bits=maximum,
        resolvability=resolvability,
        explanation_mass=explanation_mass,
    )


def causal_replaceability_cost(
    accepted_rows: Sequence[dict],
    switch: str,
) -> float:
    """Informational cost of removing one declared mechanism from A.

    ``CRC = -log2 P(switch=OFF | A)``.  ``inf`` means no currently admissible
    explanation survives with that mechanism removed.  This is a grammar-relative
    structural diagnostic, not a natural-cause probability.
    """

    rows = tuple(accepted_rows)
    if not rows:
        return float("nan")
    if any(switch not in row for row in rows):
        raise KeyError(f"accepted row missing switch column: {switch}")
    p_off = sum(not bool(row[switch]) for row in rows) / len(rows)
    if p_off == 0.0:
        return float("inf")
    return -math.log2(p_off)


def expected_observation_value(
    accepted_rows: Sequence[dict],
    switches: Sequence[str],
    candidate: CandidateObservation,
) -> ObservationValue:
    """Expected gain in switch-space resolvability from one candidate observation."""

    if candidate.cost <= 0:
        raise ValueError("candidate cost must be positive")
    if not candidate.outcomes:
        raise ValueError("candidate must declare at least one outcome")
    total_probability = sum(outcome.probability for outcome in candidate.outcomes)
    if any(outcome.probability < 0 for outcome in candidate.outcomes):
        raise ValueError("outcome probabilities must be non-negative")
    if not math.isclose(total_probability, 1.0, rel_tol=1e-9, abs_tol=1e-9):
        raise ValueError("outcome probabilities must sum to 1")

    baseline = causal_resolvability(accepted_rows, switches)
    if baseline != baseline:  # NaN
        return ObservationValue(candidate.name, float("nan"), float("nan"), baseline)

    expected_after = 0.0
    for outcome in candidate.outcomes:
        subset = [row for row in accepted_rows if outcome.predicate(row)]
        if subset:
            after = causal_resolvability(subset, switches)
        else:
            # An impossible outcome under the current admissible region should not
            # be interpreted as perfect resolution.  It contributes the baseline
            # until the model/grammar is revised.
            after = baseline
        expected_after += outcome.probability * after

    gain = expected_after - baseline
    return ObservationValue(
        candidate=candidate.name,
        expected_resolvability_gain=gain,
        expected_gain_per_cost=gain / candidate.cost,
        baseline_resolvability=baseline,
    )
