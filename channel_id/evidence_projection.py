"""Audit which current ``izu-core`` evidence layers may invoke W=F*E theorems.

The purpose is to prevent category errors.  A response pattern, a network metric,
or a pollinator proxy is not silently promoted into a direct channel measurement.
The current Izu evidence is recorded at its actual layer and paired with explicit
permitted/prohibited conclusions.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ProjectionStatus(str, Enum):
    EXACT = "exact"
    REQUIRES_FACTORIZATION_EXTENSION = "requires_factorization_extension"
    NOT_APPLICABLE = "not_applicable"


@dataclass(frozen=True)
class EvidenceProjection:
    key: str
    target: str
    status: ProjectionStatus
    theorem_ids: tuple[str, ...]
    current_output: str
    permitted_conclusion: str
    prohibited_conclusion: str
    missing_requirements: tuple[str, ...]


_PROJECTIONS: tuple[EvidenceProjection, ...] = (
    EvidenceProjection(
        key="abstract_positive_wfe_model",
        target="Declared positive two-factor W=F*E model",
        status=ProjectionStatus.EXACT,
        theorem_ids=("N1", "N2", "N3", "N4"),
        current_output="Trait-specific positive W plus declared local F and establishment E factors.",
        permitted_conclusion=(
            "Net-only data are non-identifying; W plus one exact factor, or a stable/calibrated "
            "proxy for one factor, identifies the corresponding relative channel changes."
        ),
        prohibited_conclusion="Claims outside the declared factorisation, trait domain, or positive interior.",
        missing_requirements=(),
    ),
    EvidenceProjection(
        key="historical_campanula_three_channel_record",
        target="Source-locked historical Campanula response shapes",
        status=ProjectionStatus.NOT_APPLICABLE,
        theorem_ids=(),
        current_output=(
            "Floral size: continuous erosion; multilocus outcrossing: continuous erosion; "
            "autonomous reproductive capacity: second-transition step. Nectar-guide change is excluded."
        ),
        permitted_conclusion=(
            "The three response channels have non-identical shapes and can constrain competing historical explanations."
        ),
        prohibited_conclusion=(
            "The response shapes identify Bombus-loss causation, a local-reproduction F channel, "
            "or an establishment E channel."
        ),
        missing_requirements=(
            "trait-specific total performance W on a shared census scale",
            "one direct F/E factor or stable/calibrated factor proxy",
            "a biologically justified observation map from the historical record to W, F, and E",
        ),
    ),
    EvidenceProjection(
        key="hiraiwa_ushimaru_fdq_matching",
        target="Contemporary FDQ -> corrected trait-matching association",
        status=ProjectionStatus.NOT_APPLICABLE,
        theorem_ids=(),
        current_output=(
            "An observational association between pollinator functional diversity and corrected "
            "flower-pollinator trait matching, with weaker downstream matching-to-pollen evidence."
        ),
        permitted_conclusion=(
            "The functional pollinator environment is associated with trait matching in the observed system."
        ),
        prohibited_conclusion=(
            "FDQ, visitor richness, visitation, or trait matching is automatically a calibrated F factor, "
            "direct reproductive dependency, or historical causal exposure."
        ),
        missing_requirements=(
            "same-unit rate-weighted effective pollen service or another direct/calibrated local reproductive factor",
            "proxy calibration/stability evidence if a proxy is used as F",
            "trait-specific total performance W if an F-versus-E claim is attempted",
        ),
    ),
    EvidenceProjection(
        key="issue91_linked_dependency_field_chain",
        target="Prospective linked Izu effective-service and reproductive-dependency field bundle",
        status=ProjectionStatus.REQUIRES_FACTORIZATION_EXTENSION,
        theorem_ids=(),
        current_output=(
            "Planned linked effort -> visitor bout -> single-visit pollen deposition -> rate-weighted "
            "effective pollen service -> open/bagged/supplemental reproduction -> fruit/seed outcomes."
        ),
        permitted_conclusion=(
            "Once collected and admitted, the bundle can directly constrain pollination function and "
            "reproductive dependency on matched plants/populations."
        ),
        prohibited_conclusion=(
            "Completion alone identifies historical selection, an Oshima-Toshima causal boundary, or "
            "the full F-versus-E decomposition of lifetime recruitment."
        ),
        missing_requirements=(
            "real linked field observations rather than templates",
            "declared common trait domain and census scale for any W=F*E application",
            "an establishment/reachability observation or defensible reconstruction target",
            "proxy calibration/stability where any measured quantity stands in for a factor",
        ),
    ),
    EvidenceProjection(
        key="external_morphology_response_shapes",
        target="Cross-archipelago island/mainland floral morphology response shapes",
        status=ProjectionStatus.NOT_APPLICABLE,
        theorem_ids=(),
        current_output=(
            "Independent-system directional recurrence in response shape, with measurement-error and "
            "effect-family admission gates retained."
        ),
        permitted_conclusion=(
            "Morphological response directions may recur across independent systems under the declared analyses."
        ),
        prohibited_conclusion=(
            "Morphology alone identifies the local reproductive channel, establishment filtering, or a universal pollination mechanism."
        ),
        missing_requirements=(
            "mechanistically matched W/F/E observations within the same transition units",
        ),
    ),
)


def evidence_projections() -> tuple[EvidenceProjection, ...]:
    return _PROJECTIONS


def projection_for(key: str) -> EvidenceProjection:
    for entry in _PROJECTIONS:
        if entry.key == key:
            return entry
    available = ", ".join(entry.key for entry in _PROJECTIONS)
    raise KeyError(f"unknown evidence projection {key!r}; available: {available}")


def validate_projection_ledger() -> None:
    """Reject silent upgrades of incomplete evidence to theorem-exact status."""

    keys = [entry.key for entry in _PROJECTIONS]
    if len(keys) != len(set(keys)):
        raise ValueError("projection keys must be unique")
    for entry in _PROJECTIONS:
        if entry.status is ProjectionStatus.EXACT:
            if not entry.theorem_ids:
                raise ValueError(f"exact projection {entry.key} must name theorem ids")
            if entry.missing_requirements:
                raise ValueError(f"exact projection {entry.key} cannot have missing requirements")
        else:
            if entry.theorem_ids:
                raise ValueError(f"non-exact projection {entry.key} cannot claim theorem ids")
            if not entry.missing_requirements:
                raise ValueError(f"non-exact projection {entry.key} must state blocking requirements")


def keys_by_status() -> dict[ProjectionStatus, tuple[str, ...]]:
    return {
        status: tuple(entry.key for entry in _PROJECTIONS if entry.status is status)
        for status in ProjectionStatus
    }
