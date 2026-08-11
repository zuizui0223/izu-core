#!/usr/bin/env python3
"""Run Tribulus flower divergence with source-hierarchy-aware ID aggregation.

The source README defines ``ID`` as a herbarium voucher when applicable or a
field site for field-collected material.  Therefore broad geographic labels
must be stable within an ID, but environmental rows can legitimately differ
within field-site IDs.  This entry point keeps strict guards on the broad model
strata, averages repeated climate values within ID, and records ambiguous
island-group labels instead of silently choosing one.
"""
from __future__ import annotations

from typing import Any

import pandas as pd

from scripts import analyze_tribulus_flower_divergence as base


STABLE_ID_COLUMNS = (
    "mainland_island_clean",
    "is_island",
    "continent_clean",
    "galapagos_binary",
    "year_collected",
)


def _clean_labels(series: pd.Series) -> list[str]:
    labels: set[str] = set()
    for value in series:
        if pd.isna(value):
            continue
        text = str(value).strip()
        if not text or text.casefold() in {"na", "nan", "null", "none"}:
            continue
        labels.add(text)
    return sorted(labels)


def _island_group_value(series: pd.Series) -> str:
    labels = _clean_labels(series)
    if not labels:
        return ""
    if len(labels) == 1:
        return labels[0]
    return "<mixed:" + "|".join(labels) + ">"


def id_level_frame(frame: pd.DataFrame) -> pd.DataFrame:
    for column in STABLE_ID_COLUMNS:
        conflicts = frame.groupby("ID")[column].nunique(dropna=False)
        bad = conflicts[conflicts > 1]
        if not bad.empty:
            raise ValueError(
                f"ID has conflicting model-defining {column} values: "
                + ", ".join(map(str, bad.index[:10]))
            )

    aggregations: dict[str, Any] = {
        "petal_length": ("petal_length", "mean"),
        "n_flower_rows": ("petal_length", "size"),
        **{column: (column, "first") for column in STABLE_ID_COLUMNS},
        "island_group": ("island_group", _island_group_value),
    }
    for column in base.CLIMATE_COLUMNS:
        aggregations[column] = (column, "mean")

    return (
        frame.groupby("ID", as_index=False)
        .agg(**aggregations)
        .reset_index(drop=True)
    )


_original_id_level_sensitivities = base.id_level_sensitivities


def id_level_sensitivities(frame: pd.DataFrame) -> dict[str, Any]:
    ambiguous_island_groups = {
        str(identifier): _clean_labels(group["island_group"])
        for identifier, group in frame.groupby("ID")
        if len(_clean_labels(group["island_group"])) > 1
    }
    climate_variable_ids = {
        column: [
            str(identifier)
            for identifier, count in frame.groupby("ID")[column].nunique(dropna=True).items()
            if count > 1
        ]
        for column in base.CLIMATE_COLUMNS
    }
    result = _original_id_level_sensitivities(frame)
    result["source_id_aggregation"] = {
        "id_definition": "source ID may denote a herbarium voucher or a field site",
        "strict_model_defining_columns": list(STABLE_ID_COLUMNS),
        "climate_aggregation": "mean within source ID",
        "island_group_aggregation": "single source label when unique; mixed labels retained explicitly and not coerced",
        "ambiguous_island_group_ids": ambiguous_island_groups,
        "ids_with_within_id_climate_variation": climate_variable_ids,
        "claim_boundary": "Within-ID environmental variation is averaged only for the ID-level sensitivity analysis. It is not evidence that the source locations are exchangeable or that mixed island-group labels can be collapsed to a single island group.",
    }
    return result


base.id_level_frame = id_level_frame
base.id_level_sensitivities = id_level_sensitivities


if __name__ == "__main__":
    base.main()
