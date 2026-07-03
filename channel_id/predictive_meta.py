"""Prediction-locked threshold tests for the Izu cross-lineage synthesis.

This module does not infer a historical pollinator regime from photographs, nor
does it fit a causal model.  It performs the intentionally narrower next step:

1. lock each competing scenario's *directional* predictions before reading
   cross-lineage photo scores;
2. aggregate observations within a lineage and pollinator regime;
3. score the observed first and second regime transitions against those locked
   predictions; and
4. keep the Campanula calibration partition separate from the other-lineage
   holdout partition.

The design prevents a common failure mode: counting multiple images or traits
from the same taxon as independent evolutionary replications.  One lineage ×
trait-family × transition is one comparison unit.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Iterable, Sequence


class PollinatorRegime(str, Enum):
    LARGE_BOMBUS = "large_bombus"
    ARDENS = "ardens"
    NO_BOMBUS = "no_bombus"


class Direction(str, Enum):
    DECREASE = "decrease"
    FLAT = "flat"
    INCREASE = "increase"


class Transition(str, Enum):
    LARGE_TO_ARDENS = "large_to_ardens"
    ARDENS_TO_NO_BOMBUS = "ardens_to_no_bombus"


class Scenario(str, Enum):
    ENVIRONMENT_ONLY = "environment_only"
    BODY_SIZE_ONLY = "body_size_only"
    SMALL_BEE_SUBSTITUTION = "small_bee_substitution"
    ARDENS_REPLACEMENT_LOSS = "ardens_replacement_loss"


TRANSITION_REGIMES: dict[Transition, tuple[PollinatorRegime, PollinatorRegime]] = {
    Transition.LARGE_TO_ARDENS: (PollinatorRegime.LARGE_BOMBUS, PollinatorRegime.ARDENS),
    Transition.ARDENS_TO_NO_BOMBUS: (PollinatorRegime.ARDENS, PollinatorRegime.NO_BOMBUS),
}

OBSERVATION_FIELDS = (
    "observation_id", "analysis_partition", "lineage_id", "taxon", "analysis_group",
    "group_confidence", "trait_id", "trait_family", "pollinator_regime", "value",
    "value_unit", "evidence_tier", "source_locator", "review_status", "weight", "notes",
)
CONTRACT_FIELDS = (
    "scenario", "analysis_group", "trait_family", "transition", "allowed_directions",
    "minimum_abs_delta", "rule_status", "interpretation", "boundary",
)


@dataclass(frozen=True)
class Observation:
    observation_id: str
    analysis_partition: str
    lineage_id: str
    taxon: str
    analysis_group: str
    group_confidence: str
    trait_id: str
    trait_family: str
    pollinator_regime: PollinatorRegime
    value: float
    value_unit: str
    evidence_tier: str
    source_locator: str
    review_status: str
    weight: float
    notes: str

    def __post_init__(self) -> None:
        if not self.observation_id:
            raise ValueError("observation_id is required")
        if not self.analysis_partition:
            raise ValueError(f"{self.observation_id}: analysis_partition is required")
        if self.analysis_group not in {"specialist", "generalist", "excluded"}:
            raise ValueError(f"{self.observation_id}: analysis_group must be specialist, generalist, or excluded")
        if self.weight <= 0:
            raise ValueError(f"{self.observation_id}: weight must be positive")


@dataclass(frozen=True)
class PredictionRule:
    scenario: Scenario
    analysis_group: str
    trait_family: str
    transition: Transition
    allowed_directions: frozenset[Direction]
    minimum_abs_delta: float
    rule_status: str
    interpretation: str
    boundary: str

    def __post_init__(self) -> None:
        if self.analysis_group not in {"specialist", "generalist"}:
            raise ValueError("prediction rules must target specialist or generalist")
        if self.minimum_abs_delta < 0:
            raise ValueError("minimum_abs_delta must be nonnegative")
        if self.rule_status not in {"active", "not_identified"}:
            raise ValueError("rule_status must be active or not_identified")
        if self.rule_status == "active" and not self.allowed_directions:
            raise ValueError("active rule requires one or more allowed directions")


@dataclass(frozen=True)
class AggregatedObservation:
    analysis_partition: str
    lineage_id: str
    taxon: str
    analysis_group: str
    trait_family: str
    pollinator_regime: PollinatorRegime
    value: float
    n_observations: int
    evidence_tiers: tuple[str, ...]


@dataclass(frozen=True)
class Contrast:
    analysis_partition: str
    lineage_id: str
    taxon: str
    analysis_group: str
    trait_family: str
    transition: Transition
    reference_regime: PollinatorRegime
    focal_regime: PollinatorRegime
    reference_value: float
    focal_value: float
    delta: float
    n_reference_observations: int
    n_focal_observations: int


@dataclass(frozen=True)
class ContrastAssessment:
    scenario: Scenario
    contrast: Contrast
    observed_direction: Direction
    allowed_directions: tuple[Direction, ...]
    assessment: str
    reason: str


@dataclass(frozen=True)
class ScenarioScore:
    scenario: Scenario
    analysis_partition: str
    supported_units: int
    contradicted_units: int
    total_tested_units: int
    alignment_rate: float | None
    net_score: float | None
    untestable_rules: int


def _require_columns(rows: list[dict[str, str]], required: Sequence[str], label: str) -> None:
    if not rows:
        raise ValueError(f"{label} is empty")
    missing = sorted(set(required).difference(rows[0]))
    if missing:
        raise ValueError(f"{label} missing required columns: {', '.join(missing)}")


def _clean(value: object) -> str:
    return str(value or "").strip()


def _parse_direction_set(value: str) -> frozenset[Direction]:
    items = [item.strip() for item in value.split("|") if item.strip()]
    try:
        return frozenset(Direction(item) for item in items)
    except ValueError as error:
        raise ValueError(f"invalid allowed_directions {value!r}") from error


def load_observations(path: str | Path) -> tuple[Observation, ...]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    _require_columns(rows, OBSERVATION_FIELDS, "predictive observation table")
    observations: list[Observation] = []
    seen: set[str] = set()
    for row in rows:
        observation_id = _clean(row["observation_id"])
        if observation_id in seen:
            raise ValueError(f"duplicate observation_id: {observation_id}")
        seen.add(observation_id)
        try:
            regime = PollinatorRegime(_clean(row["pollinator_regime"]))
            value = float(_clean(row["value"]))
            weight = float(_clean(row.get("weight", "1") or "1"))
        except ValueError as error:
            raise ValueError(f"{observation_id}: invalid regime/value/weight") from error
        observations.append(Observation(
            observation_id=observation_id,
            analysis_partition=_clean(row["analysis_partition"]),
            lineage_id=_clean(row["lineage_id"]),
            taxon=_clean(row["taxon"]),
            analysis_group=_clean(row["analysis_group"]),
            group_confidence=_clean(row["group_confidence"]),
            trait_id=_clean(row["trait_id"]),
            trait_family=_clean(row["trait_family"]),
            pollinator_regime=regime,
            value=value,
            value_unit=_clean(row["value_unit"]),
            evidence_tier=_clean(row["evidence_tier"]),
            source_locator=_clean(row["source_locator"]),
            review_status=_clean(row["review_status"]),
            weight=weight,
            notes=_clean(row["notes"]),
        ))
    return tuple(observations)


def load_prediction_rules(path: str | Path) -> tuple[PredictionRule, ...]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    _require_columns(rows, CONTRACT_FIELDS, "prediction contract")
    rules: list[PredictionRule] = []
    seen: set[tuple[Scenario, str, str, Transition]] = set()
    for row in rows:
        try:
            scenario = Scenario(_clean(row["scenario"]))
            transition = Transition(_clean(row["transition"]))
            delta = float(_clean(row["minimum_abs_delta"]))
        except ValueError as error:
            raise ValueError(f"invalid scenario/transition/minimum_abs_delta in contract row {row!r}") from error
        key = (scenario, _clean(row["analysis_group"]), _clean(row["trait_family"]), transition)
        if key in seen:
            raise ValueError(f"duplicate prediction rule: {key}")
        seen.add(key)
        rules.append(PredictionRule(
            scenario=scenario,
            analysis_group=key[1],
            trait_family=key[2],
            transition=transition,
            allowed_directions=_parse_direction_set(_clean(row["allowed_directions"])),
            minimum_abs_delta=delta,
            rule_status=_clean(row["rule_status"]),
            interpretation=_clean(row["interpretation"]),
            boundary=_clean(row["boundary"]),
        ))
    return tuple(rules)


def aggregate_observations(observations: Iterable[Observation]) -> tuple[AggregatedObservation, ...]:
    """Aggregate multiple cards/populations without promoting them to lineages.

    The aggregation unit deliberately drops ``trait_id``: a prespecified analysis
    must contribute at most one trait per lineage × trait family × regime.  The
    loader rejects mixed trait IDs in such a unit, which prevents silently
    averaging non-equivalent floral variables.
    """
    family_trait_ids: dict[tuple[str, str, str, str, str], set[str]] = {}
    source_rows = tuple(observations)
    for row in source_rows:
        if row.analysis_group == "excluded":
            continue
        family_key = (row.analysis_partition, row.lineage_id, row.taxon, row.analysis_group, row.trait_family)
        family_trait_ids.setdefault(family_key, set()).add(row.trait_id)
    mixed = [key for key, values in family_trait_ids.items() if len(values) > 1]
    if mixed:
        raise ValueError("a lineage × trait-family must use one predeclared trait_id across regimes")
    groups: dict[tuple[str, str, str, str, str, PollinatorRegime], list[Observation]] = {}
    for row in source_rows:
        if row.analysis_group == "excluded":
            continue
        key = (
            row.analysis_partition, row.lineage_id, row.taxon, row.analysis_group,
            row.trait_family, row.pollinator_regime,
        )
        groups.setdefault(key, []).append(row)
    output: list[AggregatedObservation] = []
    for key, rows in groups.items():
        trait_ids = {row.trait_id for row in rows}
        if len(trait_ids) != 1:
            raise ValueError(
                "mixed trait_id within one lineage × trait-family × regime aggregation unit: "
                + ", ".join(sorted(trait_ids))
            )
        weight_total = sum(row.weight for row in rows)
        weighted = sum(row.value * row.weight for row in rows) / weight_total
        output.append(AggregatedObservation(
            analysis_partition=key[0], lineage_id=key[1], taxon=key[2],
            analysis_group=key[3], trait_family=key[4], pollinator_regime=key[5],
            value=weighted, n_observations=len(rows),
            evidence_tiers=tuple(sorted({row.evidence_tier for row in rows})),
        ))
    return tuple(sorted(output, key=lambda item: (
        item.analysis_partition, item.lineage_id, item.trait_family, item.pollinator_regime.value,
    )))


def build_contrasts(aggregated: Iterable[AggregatedObservation]) -> tuple[Contrast, ...]:
    grouped: dict[tuple[str, str, str, str, str], dict[PollinatorRegime, AggregatedObservation]] = {}
    for row in aggregated:
        key = (row.analysis_partition, row.lineage_id, row.taxon, row.analysis_group, row.trait_family)
        bucket = grouped.setdefault(key, {})
        if row.pollinator_regime in bucket:
            raise ValueError(f"duplicate aggregated regime within {key}")
        bucket[row.pollinator_regime] = row
    output: list[Contrast] = []
    for key, bucket in grouped.items():
        for transition, (reference, focal) in TRANSITION_REGIMES.items():
            if reference not in bucket or focal not in bucket:
                continue
            reference_row = bucket[reference]
            focal_row = bucket[focal]
            output.append(Contrast(
                analysis_partition=key[0], lineage_id=key[1], taxon=key[2], analysis_group=key[3],
                trait_family=key[4], transition=transition, reference_regime=reference,
                focal_regime=focal, reference_value=reference_row.value, focal_value=focal_row.value,
                delta=focal_row.value - reference_row.value,
                n_reference_observations=reference_row.n_observations,
                n_focal_observations=focal_row.n_observations,
            ))
    return tuple(sorted(output, key=lambda item: (
        item.analysis_partition, item.lineage_id, item.trait_family, item.transition.value,
    )))


def classify_direction(delta: float, minimum_abs_delta: float) -> Direction:
    if abs(delta) <= minimum_abs_delta:
        return Direction.FLAT
    return Direction.INCREASE if delta > 0 else Direction.DECREASE


def _rule_index(rules: Iterable[PredictionRule]) -> dict[tuple[Scenario, str, str, Transition], PredictionRule]:
    return {(rule.scenario, rule.analysis_group, rule.trait_family, rule.transition): rule for rule in rules}


def assess_contrasts(
    contrasts: Iterable[Contrast],
    rules: Iterable[PredictionRule],
    scenario: Scenario,
    partition: str,
) -> tuple[ContrastAssessment, ...]:
    index = _rule_index(rules)
    assessments: list[ContrastAssessment] = []
    for contrast in contrasts:
        if contrast.analysis_partition != partition:
            continue
        rule = index.get((scenario, contrast.analysis_group, contrast.trait_family, contrast.transition))
        if rule is None:
            continue
        if rule.rule_status != "active":
            assessments.append(ContrastAssessment(
                scenario=scenario, contrast=contrast, observed_direction=Direction.FLAT,
                allowed_directions=tuple(), assessment="not_identified",
                reason="The contract declares no regime-specific prediction for this scenario/trait.",
            ))
            continue
        observed = classify_direction(contrast.delta, rule.minimum_abs_delta)
        supported = observed in rule.allowed_directions
        assessments.append(ContrastAssessment(
            scenario=scenario, contrast=contrast, observed_direction=observed,
            allowed_directions=tuple(sorted(rule.allowed_directions, key=lambda item: item.value)),
            assessment="supported" if supported else "contradicted",
            reason=rule.interpretation,
        ))
    return tuple(assessments)


def score_scenarios(
    observations: Iterable[Observation],
    rules: Iterable[PredictionRule],
    partition: str,
) -> tuple[ScenarioScore, ...]:
    aggregated = aggregate_observations(observations)
    contrasts = build_contrasts(aggregated)
    rule_tuple = tuple(rules)
    results: list[ScenarioScore] = []
    for scenario in Scenario:
        assessments = assess_contrasts(contrasts, rule_tuple, scenario, partition)
        supported = sum(item.assessment == "supported" for item in assessments)
        contradicted = sum(item.assessment == "contradicted" for item in assessments)
        tested = supported + contradicted
        not_identified = sum(item.assessment == "not_identified" for item in assessments)
        results.append(ScenarioScore(
            scenario=scenario,
            analysis_partition=partition,
            supported_units=supported,
            contradicted_units=contradicted,
            total_tested_units=tested,
            alignment_rate=(supported / tested) if tested else None,
            net_score=((supported - contradicted) / tested) if tested else None,
            untestable_rules=not_identified,
        ))
    return tuple(results)


def render_markdown(
    scores: Iterable[ScenarioScore],
    assessments: Iterable[ContrastAssessment],
    partition: str,
) -> str:
    ordered = sorted(
        scores,
        key=lambda row: (row.net_score is None, -(row.net_score if row.net_score is not None else -999.0), row.scenario.value),
    )
    lines = [
        "# Prediction-locked two-threshold comparison",
        "",
        f"Partition: `{partition}`.",
        "",
        "This report checks observed first/second regime contrasts against a prediction contract fixed before holdout photo scores are joined. It is not a causal estimator, does not infer pollinator presence from photos, and does not rank `environment_only` until its explicit environmental likelihood is supplied.",
        "",
        "| scenario | supported units | contradicted units | tested units | alignment rate | net score | not-identified units |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in ordered:
        alignment = "not ranked" if row.alignment_rate is None else f"{row.alignment_rate:.3f}"
        net = "not ranked" if row.net_score is None else f"{row.net_score:.3f}"
        lines.append(
            f"| {row.scenario.value} | {row.supported_units} | {row.contradicted_units} | {row.total_tested_units} | {alignment} | {net} | {row.untestable_rules} |"
        )
    material = [row for row in assessments if row.assessment in {"supported", "contradicted"}]
    if material:
        lines.extend(("", "## Auditable contrast decisions", "", "| scenario | lineage | trait family | transition | delta | observed direction | contract result |", "|---|---|---|---|---:|---|---|"))
        for row in material:
            contrast = row.contrast
            lines.append(
                f"| {row.scenario.value} | {contrast.taxon} | {contrast.trait_family} | {contrast.transition.value} | {contrast.delta:.4f} | {row.observed_direction.value} | {row.assessment} |"
            )
    lines.extend((
        "", "## Boundary", "",
        "Each unit is one lineage × trait family × regime transition, even when several images or populations contribute to a regime mean. Photo-derived scores are C-rank ordinal evidence only. Direct source-locked Campanula observations are calibration evidence and must not be relabelled as independent cross-lineage replications.",
    ))
    return "\n".join(lines) + "\n"


def write_assessments_csv(path: str | Path, assessments: Iterable[ContrastAssessment]) -> None:
    fieldnames = [
        "scenario", "analysis_partition", "lineage_id", "taxon", "analysis_group", "trait_family",
        "transition", "reference_regime", "focal_regime", "reference_value", "focal_value", "delta",
        "observed_direction", "allowed_directions", "assessment", "reason",
        "n_reference_observations", "n_focal_observations",
    ]
    rows = []
    for row in assessments:
        contrast = row.contrast
        rows.append({
            "scenario": row.scenario.value,
            "analysis_partition": contrast.analysis_partition,
            "lineage_id": contrast.lineage_id,
            "taxon": contrast.taxon,
            "analysis_group": contrast.analysis_group,
            "trait_family": contrast.trait_family,
            "transition": contrast.transition.value,
            "reference_regime": contrast.reference_regime.value,
            "focal_regime": contrast.focal_regime.value,
            "reference_value": f"{contrast.reference_value:.12g}",
            "focal_value": f"{contrast.focal_value:.12g}",
            "delta": f"{contrast.delta:.12g}",
            "observed_direction": row.observed_direction.value,
            "allowed_directions": "|".join(item.value for item in row.allowed_directions),
            "assessment": row.assessment,
            "reason": row.reason,
            "n_reference_observations": contrast.n_reference_observations,
            "n_focal_observations": contrast.n_focal_observations,
        })
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
