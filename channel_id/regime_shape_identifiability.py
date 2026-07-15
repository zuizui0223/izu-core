"""Design-power audit for cline, threshold, and no-response hypotheses.

This module is deliberately a simulation and design diagnostic.  It does not fit
field data and it does not infer a historical Bombus transition.  It asks whether
the declared Izu sampling geometry can distinguish predeclared response shapes
under controlled virtual truths.

The scaffold separates two boundaries:

    mainland large Bombus -> Izu Oshima B. ardens -> no effective Bombus islands

Candidate shapes are ``none``, ``cline``, ``first_step``, ``second_step``,
``two_step``, and a latitude-based ``environment_history`` adversary.  The latter
is only an order-correlated design surrogate; it is not the final environmental
likelihood, which still requires measured climate, area, isolation, and history.
"""
from __future__ import annotations

import csv
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence


MODEL_SPECS: dict[str, tuple[str, ...]] = {
    "none": (),
    "cline": ("order_scaled",),
    "first_step": ("first_boundary_state",),
    "second_step": ("second_boundary_state",),
    "two_step": ("first_boundary_state", "second_boundary_state"),
    "environment_history": ("latitude_scaled",),
}

DESIGN_SCENARIOS = (
    "current_six_plus_mainland",
    "current_six_island_only",
    "add_toshima",
    "full_nine_plus_mainland",
    "full_nine_island_only",
)

RESPONSE_DOMAINS = ("continuous", "binary", "occupancy")
TRUTH_MODELS = tuple(MODEL_SPECS)


@dataclass(frozen=True)
class ScaffoldRow:
    unit_id: str
    unit_name: str
    unit_type: str
    sequence_order: int
    latitude_seed: float
    longitude_seed: float
    pollinator_regime: str
    first_boundary_state: int
    second_boundary_state: int
    occurrence_data_status: str
    regime_evidence_status: str
    analysis_role: str
    notes: str
    order_scaled: float = 0.0
    latitude_scaled: float = 0.0


@dataclass(frozen=True)
class PowerCell:
    design_id: str
    response_domain: str
    truth_model: str
    replicates: int
    selected_truth: int
    recovery_rate: float
    most_common_selected_model: str
    most_common_selected_count: int
    selection_counts: dict[str, int]


@dataclass(frozen=True)
class IdentifiabilityReport:
    schema_version: str
    replicates: int
    lineages_per_replicate: int
    seed: int
    cells: tuple[PowerCell, ...]
    focus: dict[str, object]
    interpretation_limits: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "replicates": self.replicates,
            "lineages_per_replicate": self.lineages_per_replicate,
            "seed": self.seed,
            "cells": [asdict(cell) for cell in self.cells],
            "focus": self.focus,
            "interpretation_limits": list(self.interpretation_limits),
        }


def _mean(values: Sequence[float]) -> float:
    return sum(values) / len(values)


def _sample_sd(values: Sequence[float]) -> float:
    if len(values) < 2:
        raise ValueError("at least two values are required")
    centre = _mean(values)
    value = math.sqrt(sum((item - centre) ** 2 for item in values) / (len(values) - 1))
    if value == 0.0:
        raise ValueError("cannot standardise a constant column")
    return value


def _standardise(values: Sequence[float]) -> list[float]:
    centre = _mean(values)
    scale = _sample_sd(values)
    return [(value - centre) / scale for value in values]


def load_scaffold(path: str | Path) -> tuple[ScaffoldRow, ...]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        raw_rows = list(csv.DictReader(handle))
    required = {
        "unit_id",
        "unit_name",
        "unit_type",
        "sequence_order",
        "latitude_seed",
        "longitude_seed",
        "pollinator_regime",
        "first_boundary_state",
        "second_boundary_state",
        "occurrence_data_status",
        "regime_evidence_status",
        "analysis_role",
        "notes",
    }
    if not raw_rows:
        raise ValueError("Izu regime scaffold is empty")
    missing = required.difference(raw_rows[0])
    if missing:
        raise ValueError("Izu regime scaffold missing columns: " + ", ".join(sorted(missing)))

    orders = [float(row["sequence_order"]) for row in raw_rows]
    latitudes = [float(row["latitude_seed"]) for row in raw_rows]
    order_scaled = _standardise(orders)
    latitude_scaled = _standardise(latitudes)

    output: list[ScaffoldRow] = []
    seen: set[str] = set()
    for index, row in enumerate(raw_rows):
        unit_id = row["unit_id"].strip()
        if not unit_id or unit_id in seen:
            raise ValueError("unit_id values must be non-empty and unique")
        seen.add(unit_id)
        first = int(row["first_boundary_state"])
        second = int(row["second_boundary_state"])
        if first not in {0, 1} or second not in {0, 1}:
            raise ValueError(f"{unit_id}: boundary states must be binary")
        if second > first:
            raise ValueError(f"{unit_id}: second boundary cannot precede the first boundary")
        output.append(
            ScaffoldRow(
                unit_id=unit_id,
                unit_name=row["unit_name"].strip(),
                unit_type=row["unit_type"].strip(),
                sequence_order=int(row["sequence_order"]),
                latitude_seed=float(row["latitude_seed"]),
                longitude_seed=float(row["longitude_seed"]),
                pollinator_regime=row["pollinator_regime"].strip(),
                first_boundary_state=first,
                second_boundary_state=second,
                occurrence_data_status=row["occurrence_data_status"].strip(),
                regime_evidence_status=row["regime_evidence_status"].strip(),
                analysis_role=row["analysis_role"].strip(),
                notes=row["notes"].strip(),
                order_scaled=order_scaled[index],
                latitude_scaled=latitude_scaled[index],
            )
        )
    output.sort(key=lambda item: item.sequence_order)
    if output[0].unit_type != "mainland_reference":
        raise ValueError("the first scaffold row must be the mainland reference")
    islands = [row for row in output if row.unit_type == "island"]
    if len(islands) != 9:
        raise ValueError(f"expected nine islands, found {len(islands)}")
    oshima = next((row for row in output if row.unit_id == "izu_oshima"), None)
    toshima = next((row for row in output if row.unit_id == "toshima"), None)
    if oshima is None or (oshima.first_boundary_state, oshima.second_boundary_state) != (1, 0):
        raise ValueError("Izu Oshima must define the B. ardens bridge state")
    if toshima is None or (toshima.first_boundary_state, toshima.second_boundary_state) != (1, 1):
        raise ValueError("Toshima must define the immediate second-boundary state")
    return tuple(output)


def load_effort(path: str | Path) -> dict[str, int]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("Izu effort table is empty")
    required = {"island_name", "n_records"}
    missing = required.difference(rows[0])
    if missing:
        raise ValueError("Izu effort table missing columns: " + ", ".join(sorted(missing)))
    return {row["island_name"].strip(): int(float(row["n_records"] or 0)) for row in rows}


def design_rows(
    scaffold: Sequence[ScaffoldRow],
    design_id: str,
    response_domain: str,
) -> tuple[ScaffoldRow, ...]:
    if design_id not in DESIGN_SCENARIOS:
        raise ValueError(f"unknown design scenario: {design_id}")
    if response_domain not in RESPONSE_DOMAINS:
        raise ValueError(f"unknown response domain: {response_domain}")

    acquired = [
        row
        for row in scaffold
        if row.unit_type == "mainland_reference"
        or row.occurrence_data_status == "acquired_exact_polygon"
    ]
    if design_id == "current_six_plus_mainland":
        rows = acquired
    elif design_id == "current_six_island_only":
        rows = [row for row in acquired if row.unit_type == "island"]
    elif design_id == "add_toshima":
        rows = [row for row in scaffold if row in acquired or row.unit_id == "toshima"]
    elif design_id == "full_nine_plus_mainland":
        rows = list(scaffold)
    else:
        rows = [row for row in scaffold if row.unit_type == "island"]

    if response_domain == "occupancy":
        rows = [row for row in rows if row.unit_type == "island"]
    return tuple(sorted(rows, key=lambda item: item.sequence_order))


def _solve(matrix: Sequence[Sequence[float]], vector: Sequence[float]) -> list[float] | None:
    n = len(vector)
    augmented = [list(map(float, matrix[index])) + [float(vector[index])] for index in range(n)]
    for column in range(n):
        pivot = max(range(column, n), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) < 1e-10:
            return None
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        divisor = augmented[column][column]
        augmented[column] = [value / divisor for value in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                augmented[row][index] - factor * augmented[column][index]
                for index in range(n + 1)
            ]
    return [augmented[index][-1] for index in range(n)]


def _feature(row: ScaffoldRow, name: str) -> float:
    if name == "order_scaled":
        return row.order_scaled
    if name == "latitude_scaled":
        return row.latitude_scaled
    if name == "first_boundary_state":
        return float(row.first_boundary_state)
    if name == "second_boundary_state":
        return float(row.second_boundary_state)
    raise ValueError(name)


def _design_matrix(rows: Sequence[ScaffoldRow], specification: Sequence[str]) -> list[list[float]]:
    return [[1.0, *(_feature(row, name) for name in specification)] for row in rows]


def _gaussian_bic(x: Sequence[Sequence[float]], y: Sequence[float]) -> float | None:
    n = len(y)
    k = len(x[0])
    xtx = [[sum(row[i] * row[j] for row in x) for j in range(k)] for i in range(k)]
    xty = [sum(row[i] * value for row, value in zip(x, y)) for i in range(k)]
    beta = _solve(xtx, xty)
    if beta is None:
        return None
    predictions = [sum(beta[index] * row[index] for index in range(k)) for row in x]
    rss = max(sum((value - prediction) ** 2 for value, prediction in zip(y, predictions)), 1e-12)
    return n * math.log(rss / n) + k * math.log(n)


def _logistic_bic(x: Sequence[Sequence[float]], y: Sequence[float]) -> float | None:
    n = len(y)
    k = len(x[0])
    beta = [0.0] * k
    for _ in range(60):
        eta = [max(-20.0, min(20.0, sum(beta[j] * row[j] for j in range(k)))) for row in x]
        probabilities = [1.0 / (1.0 + math.exp(-value)) for value in eta]
        weights = [max(1e-6, value * (1.0 - value)) for value in probabilities]
        adjusted = [eta[index] + (y[index] - probabilities[index]) / weights[index] for index in range(n)]
        xtwx = [
            [
                sum(weights[t] * x[t][i] * x[t][j] for t in range(n))
                + (1e-6 if i == j else 0.0)
                for j in range(k)
            ]
            for i in range(k)
        ]
        xtwz = [sum(weights[t] * x[t][i] * adjusted[t] for t in range(n)) for i in range(k)]
        candidate = _solve(xtwx, xtwz)
        if candidate is None:
            return None
        if max(abs(candidate[index] - beta[index]) for index in range(k)) < 1e-8:
            beta = candidate
            break
        beta = candidate

    eta = [max(-20.0, min(20.0, sum(beta[j] * row[j] for j in range(k)))) for row in x]
    log_likelihood = 0.0
    for outcome, linear in zip(y, eta):
        if outcome:
            log_likelihood -= math.log1p(math.exp(-linear))
        else:
            log_likelihood -= math.log1p(math.exp(linear))
    return -2.0 * log_likelihood + k * math.log(n)


def identifiable_models(rows: Sequence[ScaffoldRow]) -> tuple[str, ...]:
    output = []
    dummy = [float(index % 2) for index in range(len(rows))]
    for model_id, specification in MODEL_SPECS.items():
        matrix = _design_matrix(rows, specification)
        if _gaussian_bic(matrix, dummy) is not None:
            output.append(model_id)
    return tuple(output)


def _truth_value(row: ScaffoldRow, truth_model: str, effect_size: float) -> float:
    if truth_model == "none":
        return 0.0
    if truth_model == "cline":
        return effect_size * row.order_scaled
    if truth_model == "first_step":
        return effect_size * row.first_boundary_state
    if truth_model == "second_step":
        return effect_size * row.second_boundary_state
    if truth_model == "two_step":
        return effect_size * (0.6 * row.first_boundary_state + row.second_boundary_state)
    if truth_model == "environment_history":
        return effect_size * row.latitude_scaled
    raise ValueError(truth_model)


def _detection_probability(row: ScaffoldRow, effort: dict[str, int], target_effort: int) -> float:
    records = effort.get(row.unit_name, target_effort)
    return min(0.98, max(0.05, 1.0 - math.exp(-records / 500.0)))


def select_model_once(
    rng: random.Random,
    rows: Sequence[ScaffoldRow],
    response_domain: str,
    truth_model: str,
    effort: dict[str, int],
    lineages: int = 20,
    effect_size: float = 1.2,
    continuous_noise_sd: float = 1.0,
    target_effort: int = 500,
) -> str:
    if response_domain not in RESPONSE_DOMAINS:
        raise ValueError(response_domain)
    if truth_model not in TRUTH_MODELS:
        raise ValueError(truth_model)

    expanded_rows: list[ScaffoldRow] = []
    outcomes: list[float] = []
    for _ in range(lineages):
        lineage_offset = rng.gauss(0.0, 0.35 if response_domain != "occupancy" else 0.30)
        for row in rows:
            linear = _truth_value(row, truth_model, effect_size) + lineage_offset
            expanded_rows.append(row)
            if response_domain == "continuous":
                outcomes.append(linear + rng.gauss(0.0, continuous_noise_sd))
            elif response_domain == "binary":
                probability = 1.0 / (1.0 + math.exp(-linear))
                outcomes.append(float(rng.random() < probability))
            else:
                # Occupancy uses a decline-oriented scale so a positive step effect
                # means lower persistence beyond that boundary.
                occupancy_probability = 1.0 / (1.0 + math.exp(-(0.8 - linear)))
                occupied = rng.random() < occupancy_probability
                detected = rng.random() < _detection_probability(row, effort, target_effort)
                outcomes.append(float(occupied and detected))

    scores: dict[str, float] = {}
    for model_id, specification in MODEL_SPECS.items():
        matrix = _design_matrix(expanded_rows, specification)
        score = (
            _gaussian_bic(matrix, outcomes)
            if response_domain == "continuous"
            else _logistic_bic(matrix, outcomes)
        )
        if score is not None and math.isfinite(score):
            scores[model_id] = score
    return min(scores, key=scores.get) if scores else "unidentifiable"


def run_identifiability_audit(
    scaffold: Sequence[ScaffoldRow],
    effort: dict[str, int],
    replicates: int = 300,
    lineages: int = 20,
    seed: int = 20260715,
) -> IdentifiabilityReport:
    if replicates <= 0 or lineages <= 0:
        raise ValueError("replicates and lineages must be positive")
    cells: list[PowerCell] = []
    for design_index, design_id in enumerate(DESIGN_SCENARIOS):
        for domain_index, response_domain in enumerate(RESPONSE_DOMAINS):
            rows = design_rows(scaffold, design_id, response_domain)
            for truth_index, truth_model in enumerate(TRUTH_MODELS):
                rng = random.Random(
                    seed
                    + design_index * 100_000
                    + domain_index * 10_000
                    + truth_index * 1_000
                )
                counts = {model_id: 0 for model_id in (*MODEL_SPECS, "unidentifiable")}
                for _ in range(replicates):
                    selected = select_model_once(
                        rng,
                        rows,
                        response_domain,
                        truth_model,
                        effort,
                        lineages=lineages,
                    )
                    counts[selected] += 1
                selected_truth = counts[truth_model]
                most_common = max(counts, key=counts.get)
                cells.append(
                    PowerCell(
                        design_id=design_id,
                        response_domain=response_domain,
                        truth_model=truth_model,
                        replicates=replicates,
                        selected_truth=selected_truth,
                        recovery_rate=selected_truth / replicates,
                        most_common_selected_model=most_common,
                        most_common_selected_count=counts[most_common],
                        selection_counts=counts,
                    )
                )

    index = {
        (cell.design_id, cell.response_domain, cell.truth_model): cell
        for cell in cells
    }
    focus = {
        "continuous_second_step_recovery": {
            design: index[(design, "continuous", "second_step")].recovery_rate
            for design in (
                "current_six_plus_mainland",
                "add_toshima",
                "full_nine_plus_mainland",
            )
        },
        "binary_second_step_recovery": {
            design: index[(design, "binary", "second_step")].recovery_rate
            for design in (
                "current_six_plus_mainland",
                "add_toshima",
                "full_nine_plus_mainland",
            )
        },
        "occupancy_second_step_recovery": {
            design: index[(design, "occupancy", "second_step")].recovery_rate
            for design in (
                "current_six_island_only",
                "add_toshima",
                "full_nine_island_only",
            )
        },
        "first_step_identifiable": {
            design: "first_step" in identifiable_models(
                design_rows(scaffold, design, "continuous")
            )
            for design in DESIGN_SCENARIOS
        },
        "toshima_priority_reason": (
            "Toshima is the only immediate post-Oshima unit in the declared sequence; "
            "adding it directly tests whether an apparent trend is a smooth cline or "
            "a discontinuity at the second pollinator boundary."
        ),
    }
    return IdentifiabilityReport(
        schema_version="1.0",
        replicates=replicates,
        lineages_per_replicate=lineages,
        seed=seed,
        cells=tuple(cells),
        focus=focus,
        interpretation_limits=(
            "This is virtual design power, not evidence that any response shape generated the field pattern.",
            "The latitude adversary is only an order-correlated surrogate and cannot replace measured climate, area, isolation, or geological history.",
            "The working pollinator-regime assignments remain hypotheses until source-direct effectiveness evidence is locked.",
            "Occupancy simulations include effort-dependent non-detection but do not yet reproduce the full GBIF/S-Net observation process.",
            "Nectar-guide data are absent from both the scaffold and the simulation truth set.",
        ),
    )


def write_report(report: IdentifiabilityReport, output_dir: str | Path) -> None:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "izu_shape_identifiability.json").write_text(
        json.dumps(report.to_dict(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    with (output / "izu_shape_identifiability.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "design_id",
                "response_domain",
                "truth_model",
                "replicates",
                "selected_truth",
                "recovery_rate",
                "most_common_selected_model",
                "most_common_selected_count",
            ],
        )
        writer.writeheader()
        for cell in report.cells:
            writer.writerow(
                {
                    key: value
                    for key, value in asdict(cell).items()
                    if key != "selection_counts"
                }
            )
