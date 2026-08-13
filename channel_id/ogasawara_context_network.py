"""Source-specific analysis for the 2026 Ogasawara interaction workbook.

The workbook records legitimate flower-contact counts by island, source-defined
invasion context, season, forest status, anole context, plant and pollinator.
These counts describe realized interactions; they are not pollen deposition,
pollinator effectiveness, effective dependency, or reproductive success.
"""
from __future__ import annotations

import math
from collections import defaultdict
from statistics import median
from typing import Mapping, Sequence

from channel_id.external_archipelago_network import (
    WeightedNetwork,
    exact_two_sided_sign_test,
    morisita_horn_similarity,
    network_metrics,
)
from channel_id.paired_effect_uncertainty import exact_bootstrap_median_interval


REQUIRED_FIELDS = (
    "island",
    "context",
    "season",
    "forest_status",
    "anole",
    "plant",
    "pollinator",
    "interaction_count",
)


def _text(row: Mapping[str, object], field: str) -> str:
    value = str(row.get(field, "") or "").strip()
    if not value:
        raise ValueError(f"blank {field}")
    return " ".join(value.split())


def _count(row: Mapping[str, object]) -> float:
    try:
        value = float(row.get("interaction_count", ""))
    except (TypeError, ValueError) as error:
        raise ValueError("interaction_count must be numeric") from error
    if not math.isfinite(value) or value < 0:
        raise ValueError("interaction_count must be finite and non-negative")
    return value


def validate_rows(rows: Sequence[Mapping[str, object]]) -> tuple[dict[str, object], ...]:
    if not rows:
        raise ValueError("Ogasawara analysis requires interaction rows")
    validated: list[dict[str, object]] = []
    context_meta: dict[str, tuple[str, str, str]] = {}
    for source in rows:
        row = {
            field: _text(source, field)
            for field in REQUIRED_FIELDS
            if field != "interaction_count"
        }
        row["interaction_count"] = _count(source)
        if (
            float(row["interaction_count"]) == 0
            and str(row["pollinator"]).casefold() != "no_pollinator"
        ):
            raise ValueError(
                "zero interaction rows must use the source label No_pollinator"
            )
        context = str(row["context"])
        metadata = (
            str(row["island"]),
            str(row["forest_status"]),
            str(row["anole"]),
        )
        previous = context_meta.setdefault(context, metadata)
        if previous != metadata:
            raise ValueError(
                f"context {context!r} maps to inconsistent island/forest/anole metadata"
            )
        validated.append(row)
    return tuple(validated)


def context_metadata(
    rows: Sequence[Mapping[str, object]],
) -> tuple[dict[str, str], ...]:
    metadata: dict[str, dict[str, str]] = {}
    for row in rows:
        context = str(row["context"])
        metadata[context] = {
            "context": context,
            "island": str(row["island"]),
            "forest_status": str(row["forest_status"]),
            "anole": str(row["anole"]),
        }
    return tuple(metadata[key] for key in sorted(metadata))


def _build_network(rows: Sequence[Mapping[str, object]]) -> WeightedNetwork:
    positive_rows = [
        row
        for row in rows
        if float(row["interaction_count"]) > 0
        and str(row["pollinator"]).casefold() != "no_pollinator"
    ]
    if not positive_rows:
        raise ValueError("context-season contains no positive legitimate interactions")
    plants = sorted({str(row["plant"]) for row in positive_rows})
    pollinators = sorted({str(row["pollinator"]) for row in positive_rows})
    weights: dict[tuple[str, str], float] = defaultdict(float)
    for row in positive_rows:
        weights[(str(row["plant"]), str(row["pollinator"]))] += float(
            row["interaction_count"]
        )
    return WeightedNetwork.from_rows(
        plants,
        pollinators,
        [
            [weights[(plant, pollinator)] for pollinator in pollinators]
            for plant in plants
        ],
    )


def context_season_metrics(
    rows: Sequence[Mapping[str, object]],
) -> tuple[dict[str, object], ...]:
    groups: dict[tuple[str, str], list[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        groups[(str(row["context"]), str(row["season"]))].append(row)
    output: list[dict[str, object]] = []
    for (context, season), group in sorted(groups.items()):
        first = group[0]
        positive_rows = [
            row for row in group if float(row["interaction_count"]) > 0
        ]
        output.append(
            {
                "context": context,
                "season": season,
                "island": str(first["island"]),
                "forest_status": str(first["forest_status"]),
                "anole": str(first["anole"]),
                "n_source_rows": len(group),
                "n_zero_marker_rows": sum(
                    float(row["interaction_count"]) == 0 for row in group
                ),
                "n_sampled_plants_including_zero_markers": len(
                    {str(row["plant"]) for row in group}
                ),
                "n_plants_with_positive_interactions": len(
                    {str(row["plant"]) for row in positive_rows}
                ),
                **network_metrics(_build_network(group)),
            }
        )
    return tuple(output)


def _plant_vector(
    rows: Sequence[Mapping[str, object]], plant: str
) -> tuple[dict[str, float], float, int]:
    weights: dict[str, float] = defaultdict(float)
    for row in rows:
        if (
            str(row["plant"]) == plant
            and float(row["interaction_count"]) > 0
            and str(row["pollinator"]).casefold() != "no_pollinator"
        ):
            weights[str(row["pollinator"])] += float(row["interaction_count"])
    return (
        dict(weights),
        sum(weights.values()),
        sum(value > 0 for value in weights.values()),
    )


def _effect_row(
    *,
    effect_id: str,
    evidence_family: str,
    response: str,
    unit: str,
    values: Sequence[float],
    source_sha256: str,
) -> dict[str, object]:
    interval = exact_bootstrap_median_interval(values)
    return {
        "effect_id": effect_id,
        "system_id": "ogasawara_2026",
        "system_cluster": "ogasawara_oceanic_archipelago",
        "evidence_family": evidence_family,
        "response": response,
        "predictor_or_contrast": (
            "Anijima natural forest with green-anole presence versus natural forest "
            "without green anoles, matched plant species within shared seasons"
        ),
        "estimate": interval["estimate"],
        "uncertainty_type": interval["method"],
        "uncertainty_value": [interval["lower"], interval["upper"]],
        "confidence": interval["confidence"],
        "unit": unit,
        "independent_unit": (
            "plant species after taking the within-plant median across shared seasons; "
            "plants do not create independent invasion contexts or archipelagos"
        ),
        "n_effect_units": interval["resampling_unit_count"],
        "bootstrap_support_size": interval["weak_composition_support_size"],
        "row_role": "external_context_effect",
        "admission_status": (
            "empirical_numeric_effect_with_plant_level_uncertainty_context_specific"
        ),
        "cross_system_model_eligible": False,
        "causal_claim_allowed": False,
        "source_sha256": source_sha256,
        "notes": (
            "The contrast is source-defined and within Anijima, but invasion contexts "
            "are spatially distinct rather than randomized. Plant-level uncertainty "
            "does not supply geographic replication."
        ),
    }


def analyze_anijima_anole_contrast(
    rows: Sequence[Mapping[str, object]],
    *,
    source_sha256: str,
) -> dict[str, object]:
    metadata = context_metadata(rows)
    candidates = [
        item
        for item in metadata
        if "anijima" in item["island"].casefold()
        and item["forest_status"].casefold() == "natural"
    ]
    presence = [
        item for item in candidates if item["anole"].casefold() == "presence"
    ]
    absence = [
        item for item in candidates if item["anole"].casefold() == "absence"
    ]
    if len(presence) != 1 or len(absence) != 1:
        raise ValueError(
            "expected exactly one natural Anijima context for anole presence and absence"
        )
    presence_context = presence[0]["context"]
    absence_context = absence[0]["context"]

    by_context_season: dict[
        tuple[str, str], list[Mapping[str, object]]
    ] = defaultdict(list)
    for row in rows:
        by_context_season[(str(row["context"]), str(row["season"]))].append(row)
    presence_seasons = {
        season
        for context, season in by_context_season
        if context == presence_context
    }
    absence_seasons = {
        season
        for context, season in by_context_season
        if context == absence_context
    }
    shared_seasons = sorted(presence_seasons & absence_seasons)
    if not shared_seasons:
        raise ValueError("Anijima contexts share no seasons")

    contrasts: list[dict[str, object]] = []
    for season in shared_seasons:
        presence_rows = by_context_season[(presence_context, season)]
        absence_rows = by_context_season[(absence_context, season)]
        shared_plants = sorted(
            {str(row["plant"]) for row in presence_rows}
            & {str(row["plant"]) for row in absence_rows}
        )
        for plant in shared_plants:
            left, absence_total, absence_richness = _plant_vector(
                absence_rows, plant
            )
            right, presence_total, presence_richness = _plant_vector(
                presence_rows, plant
            )
            if (
                absence_total <= 0
                or presence_total <= 0
                or absence_richness <= 0
                or presence_richness <= 0
            ):
                continue
            pollinator_union = sorted(set(left) | set(right))
            similarity = morisita_horn_similarity(
                [left.get(name, 0.0) for name in pollinator_union],
                [right.get(name, 0.0) for name in pollinator_union],
            )
            contrasts.append(
                {
                    "season": season,
                    "plant_name": plant,
                    "absence_context": absence_context,
                    "presence_context": presence_context,
                    "absence_total_legitimate_interactions": absence_total,
                    "presence_total_legitimate_interactions": presence_total,
                    "visitation_log_response_ratio_presence_over_absence": math.log(
                        presence_total / absence_total
                    ),
                    "absence_pollinator_richness": absence_richness,
                    "presence_pollinator_richness": presence_richness,
                    "pollinator_richness_log_response_ratio_presence_over_absence": math.log(
                        presence_richness / absence_richness
                    ),
                    "shared_pollinator_count": sum(
                        left.get(name, 0.0) > 0 and right.get(name, 0.0) > 0
                        for name in pollinator_union
                    ),
                    "pollinator_morisita_horn_similarity": similarity,
                    "pollinator_morisita_horn_turnover": 1.0 - similarity,
                }
            )
    if not contrasts:
        raise ValueError("Anijima contexts share no positive plants within season")

    by_plant: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    for contrast in contrasts:
        by_plant[str(contrast["plant_name"])].append(contrast)
    plant_units: list[dict[str, object]] = []
    for plant, plant_rows in sorted(by_plant.items()):
        plant_units.append(
            {
                "plant_name": plant,
                "n_shared_seasons": len(plant_rows),
                "shared_seasons": sorted(
                    str(row["season"]) for row in plant_rows
                ),
                "median_visitation_lrr_presence_over_absence": median(
                    float(
                        row[
                            "visitation_log_response_ratio_presence_over_absence"
                        ]
                    )
                    for row in plant_rows
                ),
                "median_pollinator_richness_lrr_presence_over_absence": median(
                    float(
                        row[
                            "pollinator_richness_log_response_ratio_presence_over_absence"
                        ]
                    )
                    for row in plant_rows
                ),
                "median_pollinator_morisita_horn_turnover": median(
                    float(row["pollinator_morisita_horn_turnover"])
                    for row in plant_rows
                ),
            }
        )

    visitation_values = [
        float(row["median_visitation_lrr_presence_over_absence"])
        for row in plant_units
    ]
    richness_values = [
        float(row["median_pollinator_richness_lrr_presence_over_absence"])
        for row in plant_units
    ]
    turnover_values = [
        float(row["median_pollinator_morisita_horn_turnover"])
        for row in plant_units
    ]

    def direction(values: Sequence[float]) -> dict[str, object]:
        lower = sum(value < -1e-12 for value in values)
        higher = sum(value > 1e-12 for value in values)
        equal = len(values) - lower - higher
        return {
            "presence_lower": lower,
            "presence_higher": higher,
            "equal": equal,
            "exact_two_sided_sign_test": exact_two_sided_sign_test(
                lower, higher
            ),
        }

    effects = [
        _effect_row(
            effect_id="ogasawara_anijima_visitation_lrr",
            evidence_family="matched_shared_plant_visitation_log_response_ratio",
            response="visitation_log_response_ratio",
            unit=(
                "ln(anole-presence legitimate interactions / anole-absence "
                "legitimate interactions)"
            ),
            values=visitation_values,
            source_sha256=source_sha256,
        ),
        _effect_row(
            effect_id="ogasawara_anijima_pollinator_richness_lrr",
            evidence_family=(
                "matched_shared_plant_pollinator_richness_log_response_ratio"
            ),
            response="pollinator_richness_log_response_ratio",
            unit=(
                "ln(anole-presence pollinator richness / anole-absence pollinator "
                "richness)"
            ),
            values=richness_values,
            source_sha256=source_sha256,
        ),
        _effect_row(
            effect_id="ogasawara_anijima_partner_turnover",
            evidence_family="matched_shared_plant_pollinator_assemblage_turnover",
            response="pollinator_morisita_horn_turnover",
            unit="Morisita-Horn turnover (1 - similarity)",
            values=turnover_values,
            source_sha256=source_sha256,
        ),
    ]

    return {
        "absence_context": absence_context,
        "presence_context": presence_context,
        "shared_seasons": shared_seasons,
        "n_plant_season_contrasts": len(contrasts),
        "n_unique_shared_plants": len(plant_units),
        "plant_season_contrasts": contrasts,
        "plant_level_effect_units": plant_units,
        "visitation_direction": direction(visitation_values),
        "pollinator_richness_direction": direction(richness_values),
        "effect_level_uncertainty": {
            "schema_version": "1.0",
            "status": "effect_rows_ready_context_specific",
            "source_id": "ogasawara_pollination_network_2026",
            "dataset_doi": "10.5281/zenodo.19221853",
            "source_sha256": source_sha256,
            "effects": effects,
            "formal_cross_system_fit_ready": False,
            "claim_boundary": (
                "These effects quantify a spatially structured anole-presence/absence "
                "contrast within Anijima. They do not estimate a mainland-distance or "
                "island-origin effect, and legitimate interaction counts are not "
                "pollinator effectiveness, pollen deposition, reproductive success, "
                "or effective dependency."
            ),
        },
    }
