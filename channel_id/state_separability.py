"""Reusable diagnostics for state-to-mechanism separability in simulation models.

The functions in this module deliberately separate two questions:

1. Forward coverage: can a mechanism-present intervention generate an observable state?
2. Inverse separability: how often does the same state also appear when that
   mechanism is absent or replaced by a declared alternative intervention?

The rates are conditional on the supplied simulation interventions. They are
not empirical diagnostic accuracies for natural populations unless the caller
has separately justified that interpretation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import inf
from typing import Iterable


@dataclass(frozen=True)
class StateDiagnostic:
    """Diagnostic performance of one observable state for one mechanism contrast."""

    state: str
    mechanism_present: str
    mechanism_absent_or_alternative: str
    present_state_events: int
    present_total: int
    absent_state_events: int
    absent_total: int

    def __post_init__(self) -> None:
        for name in (
            "present_state_events",
            "present_total",
            "absent_state_events",
            "absent_total",
        ):
            value = getattr(self, name)
            if not isinstance(value, int) or isinstance(value, bool):
                raise TypeError(f"{name} must be an integer")
            if value < 0:
                raise ValueError(f"{name} must be non-negative")
        if self.present_total <= 0 or self.absent_total <= 0:
            raise ValueError("intervention totals must be positive")
        if self.present_state_events > self.present_total:
            raise ValueError("present_state_events cannot exceed present_total")
        if self.absent_state_events > self.absent_total:
            raise ValueError("absent_state_events cannot exceed absent_total")

    @property
    def sensitivity(self) -> float:
        return self.present_state_events / self.present_total

    @property
    def false_negative_rate(self) -> float:
        return 1.0 - self.sensitivity

    @property
    def false_positive_rate(self) -> float:
        return self.absent_state_events / self.absent_total

    @property
    def specificity(self) -> float:
        return 1.0 - self.false_positive_rate

    @property
    def youden_j(self) -> float:
        """Sensitivity + specificity - 1; zero means no separation by this state."""
        return self.sensitivity + self.specificity - 1.0

    @property
    def positive_likelihood_ratio(self) -> float:
        """P(state|present) / P(state|absent); infinity if FPR is zero."""
        if self.false_positive_rate == 0.0:
            return inf if self.sensitivity > 0.0 else 0.0
        return self.sensitivity / self.false_positive_rate

    def as_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload.update(
            sensitivity=self.sensitivity,
            false_negative_rate=self.false_negative_rate,
            false_positive_rate=self.false_positive_rate,
            specificity=self.specificity,
            youden_j=self.youden_j,
            positive_likelihood_ratio=self.positive_likelihood_ratio,
        )
        return payload


def diagnostic_from_frequencies(
    *,
    state: str,
    mechanism_present: str,
    mechanism_absent_or_alternative: str,
    present_frequency: float,
    absent_frequency: float,
) -> dict[str, float | str]:
    """Compute separability when only intervention frequencies are available.

    Frequencies must lie in [0, 1]. This helper is useful for previously
    aggregated frozen simulation outputs where raw event counts are not part of
    the retained artifact.
    """

    for name, value in (
        ("present_frequency", present_frequency),
        ("absent_frequency", absent_frequency),
    ):
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} must lie in [0, 1]")

    sensitivity = present_frequency
    false_positive_rate = absent_frequency
    specificity = 1.0 - false_positive_rate
    return {
        "state": state,
        "mechanism_present": mechanism_present,
        "mechanism_absent_or_alternative": mechanism_absent_or_alternative,
        "sensitivity": sensitivity,
        "false_negative_rate": 1.0 - sensitivity,
        "false_positive_rate": false_positive_rate,
        "specificity": specificity,
        "youden_j": sensitivity + specificity - 1.0,
        "positive_likelihood_ratio": (
            inf if false_positive_rate == 0.0 and sensitivity > 0.0
            else 0.0 if false_positive_rate == 0.0
            else sensitivity / false_positive_rate
        ),
    }


def rank_diagnostics(diagnostics: Iterable[StateDiagnostic]) -> list[StateDiagnostic]:
    """Rank states by intervention separability, then sensitivity.

    This is a descriptive ordering, not a model-selection criterion. It is
    intentionally prevalence-free because empirical prevalence is not implied
    by synthetic intervention frequencies.
    """

    return sorted(
        diagnostics,
        key=lambda row: (row.youden_j, row.sensitivity, row.specificity),
        reverse=True,
    )
