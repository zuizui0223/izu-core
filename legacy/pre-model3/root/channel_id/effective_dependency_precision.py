"""Pilot dispersion summaries and precision-driven replication for dependency data.

The direct effective-pollinator field panel deliberately does not hard-code a
flower or plant sample size.  This module turns pilot data into plant-level
dispersion summaries and, only when an absolute CI half-width has been locked in
advance, an approximate number of *independent plants* required for a mean.

Flowers and SVD events within a plant contribute to that plant's pilot mean; they
do not inflate the independent-unit count.  The recommendation uses a simple
normal-approximation formula and is a planning diagnostic, not a substitute for
final hierarchical simulation/power analysis.
"""

from __future__ import annotations

import csv
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import NormalDist, mean, stdev
from typing import Iterable, Mapping, Sequence


GOAL_COLUMNS = (
    "goal_id", "metric", "population_id", "group_label", "absolute_half_width",
    "confidence", "status", "notes",
)
VALID_METRICS = frozenset({"background_adjusted_svd", "capsule_set_proportion"})
VALID_GOAL_STATUS = frozenset({"draft", "locked"})


@dataclass(frozen=True)
class PilotPrecisionAudit:
    svd_plant_rows: tuple[dict[str, str], ...]
    svd_summary_rows: tuple[dict[str, str], ...]
    treatment_plant_rows: tuple[dict[str, str], ...]
    treatment_summary_rows: tuple[dict[str, str], ...]
    precision_rows: tuple[dict[str, str], ...]


def _text(row: Mapping[str, object], field: str) -> str:
    return str(row.get(field, "") or "").strip()


def _require_columns(fieldnames: Iterable[str], required: Sequence[str], label: str) -> None:
    missing = set(required) - set(fieldnames)
    if missing:
        raise ValueError(f"{label} missing columns: " + ", ".join(sorted(missing)))


def _as_nonnegative_int(row: Mapping[str, object], field: str, label: str) -> int:
    try:
        value = int(_text(row, field))
    except ValueError as error:
        raise ValueError(f"{field} must be an integer for {label}") from error
    if value < 0:
        raise ValueError(f"{field} must be non-negative for {label}")
    return value


def _between_unit_summary(values: Sequence[float]) -> tuple[str, str, str]:
    if not values:
        return "", "", ""
    avg = mean(values)
    if len(values) < 2:
        return f"{avg:.8f}", "", ""
    sd = stdev(values)
    cv = "" if abs(avg) < 1e-12 else f"{sd / abs(avg):.8f}"
    return f"{avg:.8f}", f"{sd:.8f}", cv


def summarize_svd_pilot(svd_rows: Sequence[Mapping[str, object]]) -> tuple[tuple[dict[str, str], ...], tuple[dict[str, str], ...]]:
    """Summarize background-adjusted SVD first within plant, then among plants."""
    controls: dict[tuple[str, str], list[int]] = defaultdict(list)
    singles: dict[tuple[str, str, str], list[int]] = defaultdict(list)
    for row in svd_rows:
        pop = _text(row, "population_id")
        record_type = _text(row, "record_type")
        count = _as_nonnegative_int(row, "conspecific_pollen_grains", f"svd_id={_text(row, 'svd_id')!r}")
        if record_type == "single_visit":
            singles[(pop, _text(row, "visitor_group"), _text(row, "plant_id"))].append(count)
        elif record_type in {"exposed_no_visit_control", "bagged_unvisited_control"}:
            controls[(pop, record_type)].append(count)

    plant_rows: list[dict[str, str]] = []
    by_group: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for (pop, group, plant), values in sorted(singles.items()):
        exposed = controls.get((pop, "exposed_no_visit_control"), [])
        bagged = controls.get((pop, "bagged_unvisited_control"), [])
        if exposed:
            background = mean(exposed)
            basis = "exposed_no_visit_control"
            control_n = len(exposed)
        elif bagged:
            background = mean(bagged)
            basis = "bagged_unvisited_control"
            control_n = len(bagged)
        else:
            background = None
            basis = "missing_no_visit_control"
            control_n = 0
        raw = mean(values)
        adjusted = None if background is None else max(0.0, raw - background)
        row = {
            "population_id": pop,
            "visitor_group": group,
            "plant_id": plant,
            "svd_events": str(len(values)),
            "mean_raw_conspecific_pollen": f"{raw:.8f}",
            "background_control_basis": basis,
            "background_control_n": str(control_n),
            "background_adjusted_plant_mean_svd": "" if adjusted is None else f"{adjusted:.8f}",
            "boundary": "Independent-unit planning uses plant means; repeated flowers/visits do not count as independent plants.",
        }
        plant_rows.append(row)
        by_group[(pop, group)].append(row)

    summaries: list[dict[str, str]] = []
    for (pop, group), rows in sorted(by_group.items()):
        controlled = [
            float(row["background_adjusted_plant_mean_svd"])
            for row in rows
            if row["background_adjusted_plant_mean_svd"]
        ]
        avg, sd, cv = _between_unit_summary(controlled)
        summaries.append({
            "metric": "background_adjusted_svd",
            "population_id": pop,
            "group_label": group,
            "independent_plants_with_controlled_svd": str(len(controlled)),
            "total_single_visit_events": str(sum(int(row["svd_events"]) for row in rows)),
            "mean_of_plant_means": avg,
            "between_plant_sd": sd,
            "between_plant_cv": cv,
            "pilot_status": "dispersion_estimable" if len(controlled) >= 2 else "needs_more_independent_plants",
        })
    return tuple(plant_rows), tuple(summaries)


def summarize_treatment_pilot(treatment_rows: Sequence[Mapping[str, object]]) -> tuple[tuple[dict[str, str], ...], tuple[dict[str, str], ...]]:
    """Summarize capsule set within plant for each treatment, then among plants."""
    buckets: dict[tuple[str, str, str], list[Mapping[str, object]]] = defaultdict(list)
    for row in treatment_rows:
        buckets[(_text(row, "population_id"), _text(row, "treatment_type"), _text(row, "plant_id"))].append(row)

    plant_rows: list[dict[str, str]] = []
    by_group: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for (pop, treatment, plant), rows in sorted(buckets.items()):
        analyzable = [row for row in rows if _text(row, "outcome_status") in {"mature_fruit", "aborted"}]
        mature = [row for row in analyzable if _text(row, "outcome_status") == "mature_fruit"]
        proportion = None if not analyzable else len(mature) / len(analyzable)
        row = {
            "population_id": pop,
            "treatment_type": treatment,
            "plant_id": plant,
            "assigned_flowers": str(len(rows)),
            "analyzable_flowers": str(len(analyzable)),
            "mature_fruits": str(len(mature)),
            "plant_capsule_set_proportion": "" if proportion is None else f"{proportion:.8f}",
            "boundary": "Independent-unit planning uses plant-level treatment proportions; flowers within a plant are subsamples.",
        }
        plant_rows.append(row)
        by_group[(pop, treatment)].append(row)

    summaries: list[dict[str, str]] = []
    for (pop, treatment), rows in sorted(by_group.items()):
        values = [float(row["plant_capsule_set_proportion"]) for row in rows if row["plant_capsule_set_proportion"]]
        avg, sd, cv = _between_unit_summary(values)
        summaries.append({
            "metric": "capsule_set_proportion",
            "population_id": pop,
            "group_label": treatment,
            "independent_plants_with_analyzable_outcomes": str(len(values)),
            "total_analyzable_flowers": str(sum(int(row["analyzable_flowers"]) for row in rows)),
            "mean_of_plant_proportions": avg,
            "between_plant_sd": sd,
            "between_plant_cv": cv,
            "pilot_status": "dispersion_estimable" if len(values) >= 2 else "needs_more_independent_plants",
        })
    return tuple(plant_rows), tuple(summaries)


def read_precision_goals(path: Path) -> tuple[dict[str, str], ...]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _require_columns(reader.fieldnames or (), GOAL_COLUMNS, "precision-goal file")
        rows = tuple(reader)
    seen: set[str] = set()
    for row in rows:
        goal_id = _text(row, "goal_id")
        if not goal_id:
            raise ValueError("blank goal_id")
        if goal_id in seen:
            raise ValueError(f"duplicate goal_id={goal_id!r}")
        seen.add(goal_id)
        if _text(row, "metric") not in VALID_METRICS:
            raise ValueError(f"invalid metric for goal_id={goal_id!r}")
        if _text(row, "status") not in VALID_GOAL_STATUS:
            raise ValueError(f"invalid status for goal_id={goal_id!r}")
        if _text(row, "status") == "locked":
            for field in ("population_id", "group_label", "absolute_half_width", "confidence"):
                if not _text(row, field):
                    raise ValueError(f"locked goal requires {field} for goal_id={goal_id!r}")
            try:
                half_width = float(_text(row, "absolute_half_width"))
                confidence = float(_text(row, "confidence"))
            except ValueError as error:
                raise ValueError(f"locked goal has nonnumeric precision for goal_id={goal_id!r}") from error
            if half_width <= 0:
                raise ValueError(f"absolute_half_width must be positive for goal_id={goal_id!r}")
            if not 0 < confidence < 1:
                raise ValueError(f"confidence must be between 0 and 1 for goal_id={goal_id!r}")
    return rows


def recommend_independent_plants(*, between_plant_sd: float, absolute_half_width: float, confidence: float) -> int:
    """Normal-approximation n for a mean with a specified absolute half-width."""
    if between_plant_sd < 0:
        raise ValueError("between_plant_sd must be non-negative")
    if absolute_half_width <= 0:
        raise ValueError("absolute_half_width must be positive")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")
    z = NormalDist().inv_cdf(0.5 + confidence / 2.0)
    return max(1, math.ceil((z * between_plant_sd / absolute_half_width) ** 2))


def build_precision_recommendations(
    goals: Sequence[Mapping[str, object]],
    svd_summary_rows: Sequence[Mapping[str, object]],
    treatment_summary_rows: Sequence[Mapping[str, object]],
) -> tuple[dict[str, str], ...]:
    index: dict[tuple[str, str, str], Mapping[str, object]] = {}
    for row in (*svd_summary_rows, *treatment_summary_rows):
        index[(_text(row, "metric"), _text(row, "population_id"), _text(row, "group_label"))] = row

    output: list[dict[str, str]] = []
    for goal in goals:
        if _text(goal, "status") != "locked":
            continue
        goal_id = _text(goal, "goal_id")
        key = (_text(goal, "metric"), _text(goal, "population_id"), _text(goal, "group_label"))
        pilot = index.get(key)
        half_width = float(_text(goal, "absolute_half_width"))
        confidence = float(_text(goal, "confidence"))
        if pilot is None:
            status = "pilot_group_missing"
            pilot_n = mean_value = sd_text = recommended = ""
        else:
            n_field = (
                "independent_plants_with_controlled_svd"
                if key[0] == "background_adjusted_svd"
                else "independent_plants_with_analyzable_outcomes"
            )
            pilot_n = _text(pilot, n_field)
            mean_value = _text(pilot, "mean_of_plant_means" if key[0] == "background_adjusted_svd" else "mean_of_plant_proportions")
            sd_text = _text(pilot, "between_plant_sd")
            if not sd_text:
                status = "pilot_dispersion_not_estimable"
                recommended = ""
            else:
                status = "approximate_n_available"
                recommended = str(
                    recommend_independent_plants(
                        between_plant_sd=float(sd_text),
                        absolute_half_width=half_width,
                        confidence=confidence,
                    )
                )
        output.append({
            "goal_id": goal_id,
            "metric": key[0],
            "population_id": key[1],
            "group_label": key[2],
            "pilot_independent_plants": pilot_n,
            "pilot_mean": mean_value,
            "pilot_between_plant_sd": sd_text,
            "absolute_half_width": f"{half_width:.8f}",
            "confidence": f"{confidence:.8f}",
            "recommended_independent_plants_normal_approx": recommended,
            "status": status,
            "boundary": (
                "Planning approximation only. Confirmatory design should also preserve site/time replication, expected loss, "
                "visitor-group availability and hierarchical simulation; flowers within a plant are not independent n."
            ),
        })
    return tuple(output)


def _write_csv(path: Path, rows: Sequence[Mapping[str, object]], fallback_columns: Sequence[str]) -> None:
    columns = list(rows[0].keys()) if rows else list(fallback_columns)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def write_pilot_precision_audit(output_dir: Path, audit: PilotPrecisionAudit) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "svd_plant_pilot.csv", audit.svd_plant_rows, ("population_id", "visitor_group", "plant_id"))
    _write_csv(output_dir / "svd_pilot_dispersion.csv", audit.svd_summary_rows, ("metric", "population_id", "group_label"))
    _write_csv(output_dir / "treatment_plant_pilot.csv", audit.treatment_plant_rows, ("population_id", "treatment_type", "plant_id"))
    _write_csv(output_dir / "treatment_pilot_dispersion.csv", audit.treatment_summary_rows, ("metric", "population_id", "group_label"))
    _write_csv(output_dir / "precision_recommendations.csv", audit.precision_rows, ("goal_id", "metric", "population_id", "group_label"))
