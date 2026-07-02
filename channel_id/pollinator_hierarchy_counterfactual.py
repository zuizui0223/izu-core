"""Core scoring for the transparent Izu pollinator-hierarchy pattern check.

This is a pattern-compatibility calculation over already locked literature and
proxy-environment inputs. It is not a fitted causal or demographic model.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from math import isfinite
from pathlib import Path
from statistics import mean
from typing import Iterable


@dataclass(frozen=True)
class IslandRecord:
    island_id: str
    region_order: float
    bombus_diversus: float
    bombus_ardens: float
    halictid_pollinator: float
    megachilid_pollinator: float
    bagged_capsule_set_pct: float | None
    bagged_seed_mean: float | None
    outcrossing_mid: float | None
    flower_length_mm: float | None
    mean_temp_c: float | None
    annual_precip_mm: float | None
    precip_cv: float | None


def _float(value: str) -> float | None:
    value = value.strip()
    if value == "":
        return None
    parsed = float(value)
    return parsed if isfinite(parsed) else None


def load_records(path: Path) -> list[IslandRecord]:
    records: list[IslandRecord] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            lo = _float(row["outcrossing_rate_min"])
            hi = _float(row["outcrossing_rate_max"])
            outcrossing_mid = None if lo is None or hi is None else (lo + hi) / 2.0
            records.append(IslandRecord(
                island_id=row["island_id"],
                region_order=float(row["region_order"]),
                bombus_diversus=float(row["bombus_diversus"]),
                bombus_ardens=float(row["bombus_ardens"]),
                halictid_pollinator=float(row["halictid_pollinator"]),
                megachilid_pollinator=float(row["megachilid_pollinator"]),
                bagged_capsule_set_pct=_float(row["bagged_capsule_set_pct"]),
                bagged_seed_mean=_float(row["bagged_seed_mean"]),
                outcrossing_mid=outcrossing_mid,
                flower_length_mm=_float(row["flower_length_mm"]),
                mean_temp_c=_float(row["mean_temp_c"]),
                annual_precip_mm=_float(row["annual_precip_mm"]),
                precip_cv=_float(row["precip_cv"]),
            ))
    return records


def minmax(values: Iterable[float | None]) -> tuple[float, float] | None:
    clean = [value for value in values if value is not None]
    if len(clean) < 2:
        return None
    lower, upper = min(clean), max(clean)
    return None if upper == lower else (lower, upper)


def scale(value: float | None, limits: tuple[float, float] | None, invert: bool = False) -> float | None:
    if value is None or limits is None:
        return None
    lower, upper = limits
    scaled = (value - lower) / (upper - lower)
    return 1.0 - scaled if invert else scaled


def hierarchy_stage(record: IslandRecord) -> float:
    """0 = mainland large Bombus, 1 = B. ardens bridge, 2 = non-Bombus bee regime."""
    if record.bombus_diversus:
        return 0.0
    if record.bombus_ardens:
        return 1.0
    return 2.0


def score(records: list[IslandRecord]) -> dict[str, object]:
    flower_limits = minmax(record.flower_length_mm for record in records)
    outcross_limits = minmax(record.outcrossing_mid for record in records)
    bag_limits = minmax(record.bagged_capsule_set_pct for record in records)
    temp_limits = minmax(record.mean_temp_c for record in records if record.island_id != "Honshu")
    precip_limits = minmax(record.annual_precip_mm for record in records if record.island_id != "Honshu")
    order_limits = minmax(record.region_order for record in records)

    rows: list[dict[str, object]] = []
    errors = {"pollinator_hierarchy": [], "environment_only": [], "isolation_order": []}
    for record in records:
        observed_selfing = scale(record.outcrossing_mid, outcross_limits, invert=True)
        observed_flower_smallness = scale(record.flower_length_mm, flower_limits, invert=True)
        observed_bagging = scale(record.bagged_capsule_set_pct, bag_limits)
        observed = [value for value in (observed_selfing, observed_flower_smallness, observed_bagging) if value is not None]
        if not observed:
            continue
        observed_stage_signal = mean(observed)
        pollinator_pred = hierarchy_stage(record) / 2.0
        env_parts = [scale(record.mean_temp_c, temp_limits), scale(record.annual_precip_mm, precip_limits)]
        env_clean = [value for value in env_parts if value is not None]
        environment_pred = mean(env_clean) if env_clean else None
        isolation_pred = scale(record.region_order, order_limits)
        model_predictions = {
            "pollinator_hierarchy": pollinator_pred,
            "environment_only": environment_pred,
            "isolation_order": isolation_pred,
        }
        row: dict[str, object] = {
            "island_id": record.island_id,
            "observed_stage_signal": round(observed_stage_signal, 4),
            "pollinator_stage_prediction": round(pollinator_pred, 4),
            "environment_prediction": None if environment_pred is None else round(environment_pred, 4),
            "isolation_prediction": None if isolation_pred is None else round(isolation_pred, 4),
        }
        for model, prediction in model_predictions.items():
            if prediction is None:
                continue
            absolute_error = abs(observed_stage_signal - prediction)
            errors[model].append(absolute_error)
            row[f"{model}_abs_error"] = round(absolute_error, 4)
        rows.append(row)

    model_scores = [
        {"model": model, "mean_absolute_error": round(mean(values), 4), "n": len(values)}
        for model, values in errors.items() if values
    ]
    model_scores.sort(key=lambda row: row["mean_absolute_error"])
    return {
        "schema_version": 1,
        "boundary": "Counterfactual pattern compatibility only; not causal proof and not a fitted demographic model.",
        "observed_channels": ["outcrossing_rate", "bagged_seed_or_capsule_set", "flower_length"],
        "candidate_models": ["pollinator_hierarchy", "environment_only", "isolation_order"],
        "model_scores": model_scores,
        "island_rows": rows,
    }


def write_markdown(result: dict[str, object], path: Path) -> None:
    lines = [
        "# Pollinator-hierarchy counterfactual pattern check", "", str(result["boundary"]), "",
        "## Model ranking", "", "| model | mean absolute error | n |", "|---|---:|---:|",
    ]
    for row in result["model_scores"]:  # type: ignore[index]
        lines.append(f"| {row['model']} | {row['mean_absolute_error']} | {row['n']} |")
    lines.extend(("", "## Island rows", "", "| island | observed signal | hierarchy pred | environment pred | isolation pred |", "|---|---:|---:|---:|---:|"))
    for row in result["island_rows"]:  # type: ignore[index]
        lines.append(f"| {row['island_id']} | {row['observed_stage_signal']} | {row['pollinator_stage_prediction']} | {row['environment_prediction']} | {row['isolation_prediction']} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
