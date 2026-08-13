#!/usr/bin/env python3
"""Run the Tribulus specimen-ID context audit without coercing mixed island groups.

The source ID can denote a herbarium voucher or a field site. Broad model strata
(mainland/island and Galapagos/other) must remain stable within ID. A few IDs span
more than one source ``island_group`` label; those labels are retained as an
explicit ambiguity record and excluded from island-group descriptive summaries,
while the predeclared broad contrasts remain usable.
"""
from __future__ import annotations

from collections import defaultdict
from statistics import fmean
from typing import Mapping, Sequence

import analyze_tribulus_flower_context as base


def _labels(group: Sequence[Mapping[str, object]], key: str) -> list[str]:
    values = {
        str(row.get(key) or "").strip()
        for row in group
        if base.norm(row.get(key)) not in base.MISSING
    }
    return sorted(value for value in values if value)


def aggregate_ids(rows: Sequence[Mapping[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["ID"])].append(row)

    output: list[dict[str, object]] = []
    for identifier, group in sorted(grouped.items()):
        mainland = base.norm(base.stable_category(group, "mainland_island"))
        galapagos = base.norm(base.stable_category(group, "galapagos_other"))
        island_groups = _labels(group, "island_group")
        record: dict[str, object] = {
            "ID": identifier,
            "n_flowers": len(group),
            "petal_length": fmean(float(row["petal_length"]) for row in group),
            "mainland_island": mainland,
            "galapagos_other": galapagos,
            # Do not invent a single island-group identity for mixed source IDs.
            "island_group": island_groups[0] if len(island_groups) == 1 else "",
            "island_group_source_values": island_groups,
            "island_group_ambiguous": len(island_groups) > 1,
        }
        for key in base.CONTINUOUS:
            values = [float(row[key]) for row in group if row.get(key) is not None]
            record[key] = fmean(values) if values else None
        output.append(record)
    return output


_original_analyse = base.analyse


def analyse(rows: Sequence[Mapping[str, object]], repetitions: int = 5000) -> dict[str, object]:
    result = _original_analyse(rows, repetitions=repetitions)
    ids = aggregate_ids(rows)
    ambiguous = {
        str(row["ID"]): row["island_group_source_values"]
        for row in ids
        if row["island_group_ambiguous"]
    }
    result["source_id_aggregation"] = {
        "id_definition": "source ID may denote a herbarium voucher or a field site",
        "broad_model_strata_required_stable_within_id": [
            "mainland_island",
            "galapagos_other",
        ],
        "continuous_covariates": "mean within source ID, matching the existing specimen-ID collapse",
        "ambiguous_island_group_ids": ambiguous,
        "island_group_summary_rule": "IDs with multiple source island_group labels are excluded from island-group descriptive summaries rather than coerced to one label",
        "claim_boundary": "Ambiguous island-group labels do not alter the predeclared mainland/island or Galapagos/other contrasts because those broad strata are stable within the affected IDs.",
    }
    return result


base.aggregate_ids = aggregate_ids
base.analyse = analyse


if __name__ == "__main__":
    base.main()
