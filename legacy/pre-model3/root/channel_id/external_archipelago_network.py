"""Transparent weighted-network summaries for external island validation.

The functions in this module intentionally avoid package-specific indices whose
exact implementation cannot be reconstructed from source workbooks alone.  The
focus is on auditable quantities: richness, positive links, total interaction
weight, Shannon interaction diversity, binary connectance, partner diversity,
and shared-plant pollinator turnover.

A visit-frequency matrix is not pollinator effectiveness, effective dependency,
trait matching, pollen deposition, or reproductive success.  Those biological
channels must remain separate in downstream interpretation.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from statistics import median
from typing import Iterable, Mapping, Sequence


def canonical_label(value: object) -> str:
    """Collapse whitespace and case for source-label alignment."""
    return " ".join(str(value or "").split()).casefold()


def _finite_nonnegative(value: object, *, label: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{label} must be numeric") from error
    if not math.isfinite(number):
        raise ValueError(f"{label} must be finite")
    if number < 0:
        raise ValueError(f"{label} must be non-negative")
    return number


@dataclass(frozen=True)
class WeightedNetwork:
    plant_names: tuple[str, ...]
    pollinator_names: tuple[str, ...]
    matrix: tuple[tuple[float, ...], ...]

    @classmethod
    def from_rows(
        cls,
        plant_names: Sequence[object],
        pollinator_names: Sequence[object],
        matrix: Sequence[Sequence[object]],
    ) -> "WeightedNetwork":
        plants = tuple(" ".join(str(value).split()) for value in plant_names)
        pollinators = tuple(" ".join(str(value).split()) for value in pollinator_names)
        if not plants:
            raise ValueError("network requires at least one plant")
        if not pollinators:
            raise ValueError("network requires at least one pollinator")
        if len(set(map(canonical_label, plants))) != len(plants):
            raise ValueError("plant labels must be unique after canonicalisation")
        if len(set(map(canonical_label, pollinators))) != len(pollinators):
            raise ValueError("pollinator labels must be unique after canonicalisation")
        if len(matrix) != len(plants):
            raise ValueError("matrix row count does not match plant count")
        values: list[tuple[float, ...]] = []
        for row_index, row in enumerate(matrix):
            if len(row) != len(pollinators):
                raise ValueError(f"matrix row {row_index} does not match pollinator count")
            values.append(
                tuple(
                    _finite_nonnegative(value, label=f"matrix[{row_index},{column_index}]")
                    for column_index, value in enumerate(row)
                )
            )
        return cls(plants, pollinators, tuple(values))

    def positive_only(self) -> "WeightedNetwork":
        """Drop all-zero plant rows and pollinator columns."""
        row_keep = [index for index, row in enumerate(self.matrix) if sum(row) > 0]
        column_keep = [
            column
            for column in range(len(self.pollinator_names))
            if sum(self.matrix[row][column] for row in range(len(self.plant_names))) > 0
        ]
        if not row_keep or not column_keep:
            raise ValueError("network contains no positive interactions")
        return WeightedNetwork.from_rows(
            [self.plant_names[index] for index in row_keep],
            [self.pollinator_names[index] for index in column_keep],
            [
                [self.matrix[row][column] for column in column_keep]
                for row in row_keep
            ],
        )

    def plant_vector(self, plant_name: str, pollinator_union: Sequence[str] | None = None) -> tuple[float, ...]:
        plant_index = {canonical_label(name): index for index, name in enumerate(self.plant_names)}
        key = canonical_label(plant_name)
        if key not in plant_index:
            raise KeyError(plant_name)
        row = self.matrix[plant_index[key]]
        if pollinator_union is None:
            return row
        source = {canonical_label(name): row[index] for index, name in enumerate(self.pollinator_names)}
        return tuple(source.get(canonical_label(name), 0.0) for name in pollinator_union)


def _shannon(weights: Iterable[float]) -> float:
    positive = [float(value) for value in weights if value > 0]
    total = sum(positive)
    if total <= 0:
        return 0.0
    return -sum((value / total) * math.log(value / total) for value in positive)


def effective_number(weights: Iterable[float]) -> float:
    positive = [float(value) for value in weights if value > 0]
    if not positive:
        return 0.0
    return math.exp(_shannon(positive))


def morisita_horn_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    """Morisita-Horn similarity using relative interaction weights."""
    if len(left) != len(right):
        raise ValueError("vectors must have equal length")
    left_total = sum(left)
    right_total = sum(right)
    if left_total <= 0 or right_total <= 0:
        return 0.0
    p = [value / left_total for value in left]
    q = [value / right_total for value in right]
    denominator = sum(value * value for value in p) + sum(value * value for value in q)
    if denominator <= 0:
        return 0.0
    similarity = 2.0 * sum(a * b for a, b in zip(p, q)) / denominator
    return min(1.0, max(0.0, similarity))


def _mean_pairwise_similarity(vectors: Sequence[Sequence[float]]) -> float | None:
    similarities: list[float] = []
    for left_index in range(len(vectors)):
        for right_index in range(left_index + 1, len(vectors)):
            similarities.append(morisita_horn_similarity(vectors[left_index], vectors[right_index]))
    return None if not similarities else sum(similarities) / len(similarities)


def network_metrics(network: WeightedNetwork) -> dict[str, float | int | None]:
    network = network.positive_only()
    flattened = [value for row in network.matrix for value in row]
    positive = [value for value in flattened if value > 0]
    total = sum(positive)
    links = len(positive)
    plants = len(network.plant_names)
    pollinators = len(network.pollinator_names)
    interaction_shannon = _shannon(positive)
    plant_vectors = [list(row) for row in network.matrix]
    pollinator_vectors = [
        [network.matrix[row][column] for row in range(plants)]
        for column in range(pollinators)
    ]
    plant_richness = [sum(value > 0 for value in row) for row in plant_vectors]
    plant_effective = [effective_number(row) for row in plant_vectors]
    return {
        "n_plants": plants,
        "n_pollinators": pollinators,
        "n_positive_links": links,
        "total_visitation_rate": total,
        "binary_connectance": links / (plants * pollinators),
        "interaction_shannon": interaction_shannon,
        "interaction_evenness": interaction_shannon / math.log(links) if links > 1 else 0.0,
        "effective_number_interactions": math.exp(interaction_shannon) if links else 0.0,
        "mean_pollinator_richness_per_plant": sum(plant_richness) / plants,
        "median_pollinator_richness_per_plant": median(plant_richness),
        "mean_effective_pollinator_number_per_plant": sum(plant_effective) / plants,
        "mean_plant_niche_overlap_morisita_horn": _mean_pairwise_similarity(plant_vectors),
        "mean_pollinator_niche_overlap_morisita_horn": _mean_pairwise_similarity(pollinator_vectors),
    }


def _binary_jaccard(left: Sequence[float], right: Sequence[float]) -> float:
    left_set = {index for index, value in enumerate(left) if value > 0}
    right_set = {index for index, value in enumerate(right) if value > 0}
    union = left_set | right_set
    return 1.0 if not union else len(left_set & right_set) / len(union)


def shared_plant_contrasts(
    continental: WeightedNetwork,
    oceanic: WeightedNetwork,
) -> tuple[dict[str, object], ...]:
    continental_plants = {canonical_label(name): name for name in continental.plant_names}
    oceanic_plants = {canonical_label(name): name for name in oceanic.plant_names}
    shared_keys = sorted(set(continental_plants) & set(oceanic_plants))
    if not shared_keys:
        raise ValueError("no shared plant labels between networks")
    pollinator_union_map: dict[str, str] = {}
    for name in (*continental.pollinator_names, *oceanic.pollinator_names):
        pollinator_union_map.setdefault(canonical_label(name), name)
    pollinator_union = tuple(pollinator_union_map[key] for key in sorted(pollinator_union_map))

    rows: list[dict[str, object]] = []
    for key in shared_keys:
        source_name = continental_plants[key]
        left = continental.plant_vector(source_name, pollinator_union)
        right = oceanic.plant_vector(oceanic_plants[key], pollinator_union)
        left_total = sum(left)
        right_total = sum(right)
        left_richness = sum(value > 0 for value in left)
        right_richness = sum(value > 0 for value in right)
        similarity = morisita_horn_similarity(left, right)
        rows.append({
            "plant_name": source_name,
            "continental_total_visitation_rate": left_total,
            "oceanic_total_visitation_rate": right_total,
            "visitation_log_response_ratio": (
                math.log(right_total / left_total) if left_total > 0 and right_total > 0 else None
            ),
            "continental_pollinator_richness": left_richness,
            "oceanic_pollinator_richness": right_richness,
            "pollinator_richness_difference_oceanic_minus_continental": right_richness - left_richness,
            "pollinator_richness_log_response_ratio": (
                math.log(right_richness / left_richness)
                if left_richness > 0 and right_richness > 0
                else None
            ),
            "continental_effective_pollinator_number": effective_number(left),
            "oceanic_effective_pollinator_number": effective_number(right),
            "shared_pollinator_count": sum(a > 0 and b > 0 for a, b in zip(left, right)),
            "pollinator_binary_jaccard": _binary_jaccard(left, right),
            "pollinator_morisita_horn_similarity": similarity,
            "pollinator_morisita_horn_turnover": 1.0 - similarity,
        })
    return tuple(rows)


def exact_two_sided_sign_test(negative: int, positive: int) -> float | None:
    """Exact two-sided binomial sign test; ties are excluded."""
    if negative < 0 or positive < 0:
        raise ValueError("sign counts must be non-negative")
    n = negative + positive
    if n == 0:
        return None
    smaller = min(negative, positive)
    probability = 2.0 * sum(math.comb(n, index) for index in range(smaller + 1)) / (2**n)
    return min(1.0, probability)


def _direction_counts(values: Sequence[float], *, tolerance: float = 1e-12) -> dict[str, int]:
    lower = sum(value < -tolerance for value in values)
    higher = sum(value > tolerance for value in values)
    equal = len(values) - lower - higher
    return {"oceanic_lower": lower, "oceanic_higher": higher, "equal": equal}


def _leave_one_median(values: Sequence[float]) -> tuple[float | None, float | None]:
    if len(values) < 2:
        return None, None
    estimates = [median(values[:index] + values[index + 1 :]) for index in range(len(values))]
    return min(estimates), max(estimates)


def summarize_shared_plant_contrasts(rows: Sequence[Mapping[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("shared-plant summary requires rows")
    visitation_differences = [
        float(row["oceanic_total_visitation_rate"]) - float(row["continental_total_visitation_rate"])
        for row in rows
    ]
    richness_differences = [
        float(row["pollinator_richness_difference_oceanic_minus_continental"])
        for row in rows
    ]
    visitation_lrr = [
        float(row["visitation_log_response_ratio"])
        for row in rows
        if row.get("visitation_log_response_ratio") is not None
    ]
    richness_lrr = [
        float(row["pollinator_richness_log_response_ratio"])
        for row in rows
        if row.get("pollinator_richness_log_response_ratio") is not None
    ]
    turnover = [float(row["pollinator_morisita_horn_turnover"]) for row in rows]
    visitation_direction = _direction_counts(visitation_differences)
    richness_direction = _direction_counts(richness_differences)
    visitation_loo = _leave_one_median(visitation_lrr)
    richness_loo = _leave_one_median(richness_lrr)
    return {
        "n_shared_plants": len(rows),
        "visitation_direction_counts": visitation_direction,
        "visitation_exact_sign_test_two_sided": exact_two_sided_sign_test(
            visitation_direction["oceanic_lower"], visitation_direction["oceanic_higher"]
        ),
        "median_visitation_log_response_ratio": median(visitation_lrr) if visitation_lrr else None,
        "leave_one_plant_median_visitation_lrr_range": list(visitation_loo),
        "pollinator_richness_direction_counts": richness_direction,
        "pollinator_richness_exact_sign_test_two_sided": exact_two_sided_sign_test(
            richness_direction["oceanic_lower"], richness_direction["oceanic_higher"]
        ),
        "median_pollinator_richness_log_response_ratio": median(richness_lrr) if richness_lrr else None,
        "leave_one_plant_median_richness_lrr_range": list(richness_loo),
        "median_pollinator_morisita_horn_turnover": median(turnover),
        "minimum_pollinator_morisita_horn_turnover": min(turnover),
        "maximum_pollinator_morisita_horn_turnover": max(turnover),
        "claim_boundary": (
            "Shared plant identity reduces whole-flora composition confounding, but this remains one continental "
            "island versus one oceanic island sampled in different years. Visitation matrices do not measure "
            "FDQ, trait matching, pollen deposition, reproductive success, or effective dependency."
        ),
    }
