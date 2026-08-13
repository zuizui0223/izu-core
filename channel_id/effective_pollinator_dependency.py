"""Field audit for direct effective-pollinator dependency measurements.

This module fills the empirical gap between camera/contact observations and
fruit/parentage outcomes.  It keeps three quantities separate:

1. per-visit pollinator effectiveness: conspecific pollen deposited on a
   previously unvisited stigma after one observed visit (SVD);
2. realized visitor-group contribution: observed visit rate multiplied by SVD;
3. plant reproductive dependence: open, autonomously bagged, and supplemental
   outcross treatments on tagged flowers from the same population.

The resulting summaries are descriptive field quantities.  Structural
completion of the panel is not a sample-size or power claim, and none of the
indices identify historical selection or causal pollinator loss.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Iterable, Mapping, Sequence

from channel_id.guide_photo_review import VALID_ISLANDS


PLANT_COLUMNS = (
    "population_id", "field_event_id", "island_id", "site_id", "taxon", "plant_id",
    "analysis_role", "tagged_at", "notes",
)
SVD_COLUMNS = (
    "svd_id", "population_id", "field_event_id", "island_id", "site_id", "taxon",
    "plant_id", "flower_id", "record_type", "effort_id", "visit_id", "visitor_group",
    "identification_confidence", "first_visit_confirmed", "bag_on_time", "bag_off_time",
    "stigma_collected_time", "pollen_count_method", "total_pollen_grains",
    "conspecific_pollen_grains", "heterospecific_pollen_grains", "unclassified_pollen_grains",
    "counter_id", "notes",
)
TREATMENT_COLUMNS = (
    "treatment_id", "population_id", "field_event_id", "island_id", "site_id", "taxon",
    "plant_id", "flower_id", "treatment_type", "assigned_at", "bag_on_time", "bag_off_time",
    "hand_pollen_source_site_id", "hand_pollen_source_plant_id", "outcome_status", "fruit_id",
    "notes",
)

ANALYSIS_ROLES = frozenset({"focal_anchor", "functional_control", "comparator", "exploratory"})
SVD_RECORD_TYPES = frozenset({"single_visit", "bagged_unvisited_control", "exposed_no_visit_control"})
FIRST_VISIT_STATES = frozenset({"yes", "no", "not_applicable"})
IDENTIFICATION_CONFIDENCE = frozenset({"confirmed", "group_level", "uncertain", "not_applicable"})
POLLEN_COUNT_METHODS = frozenset({"fuchsin_gel", "fluorescence", "light_microscopy", "other"})
TREATMENT_TYPES = frozenset({
    "open_pollinated", "bagged_autonomous", "supplemental_outcross", "hand_self", "emasculated_open"
})
OUTCOME_STATES = frozenset({"pending", "mature_fruit", "aborted", "lost", "damaged"})
CORE_TREATMENTS = ("open_pollinated", "bagged_autonomous", "supplemental_outcross")

BOUNDARY = (
    "Structural completion means linked field channels exist; it is not evidence of adequate power, "
    "equivalence, historical causation, self-compatibility, realized selfing, or evolutionary selection."
)


@dataclass(frozen=True)
class EffectiveDependencyAudit:
    svd_group_rows: tuple[dict[str, str], ...]
    effective_service_rows: tuple[dict[str, str], ...]
    treatment_rows: tuple[dict[str, str], ...]
    population_readiness_rows: tuple[dict[str, str], ...]
    summary: Mapping[str, object]


def _text(row: Mapping[str, object], field: str) -> str:
    return str(row.get(field, "") or "").strip()


def _require_columns(fieldnames: Iterable[str], required: Sequence[str], label: str) -> None:
    missing = set(required) - set(fieldnames)
    if missing:
        raise ValueError(f"{label} missing columns: " + ", ".join(sorted(missing)))


def _parse_time(value: str, *, field: str, label: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as error:
        raise ValueError(f"invalid {field} for {label}: {value!r}") from error
    if parsed.tzinfo is None:
        raise ValueError(f"{field} requires an ISO-8601 timezone offset for {label}")
    return parsed


def _nonnegative_int(row: Mapping[str, object], field: str, label: str) -> int:
    try:
        value = int(_text(row, field))
    except ValueError as error:
        raise ValueError(f"{field} must be an integer for {label}") from error
    if value < 0:
        raise ValueError(f"{field} must be non-negative for {label}")
    return value


def _read_csv(path: Path, columns: Sequence[str], label: str) -> tuple[dict[str, str], ...]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _require_columns(reader.fieldnames or (), columns, label)
        return tuple(reader)


def read_dependency_plant_registry(path: Path) -> tuple[dict[str, str], ...]:
    rows = _read_csv(path, PLANT_COLUMNS, "dependency plant registry")
    seen: set[str] = set()
    for row in rows:
        plant_id = _text(row, "plant_id")
        if not plant_id:
            raise ValueError("blank plant_id in dependency plant registry")
        if plant_id in seen:
            raise ValueError(f"duplicate plant_id {plant_id!r} in dependency plant registry")
        seen.add(plant_id)
        for field in ("population_id", "field_event_id", "island_id", "site_id", "taxon", "analysis_role", "tagged_at"):
            if not _text(row, field):
                raise ValueError(f"blank {field} for plant_id={plant_id!r}")
        if _text(row, "island_id") not in VALID_ISLANDS:
            raise ValueError(f"invalid island_id for plant_id={plant_id!r}")
        if _text(row, "analysis_role") not in ANALYSIS_ROLES:
            raise ValueError(f"invalid analysis_role for plant_id={plant_id!r}")
        _parse_time(_text(row, "tagged_at"), field="tagged_at", label=f"plant_id={plant_id!r}")
    return rows


def read_svd_manifest(path: Path) -> tuple[dict[str, str], ...]:
    rows = _read_csv(path, SVD_COLUMNS, "SVD manifest")
    seen: set[str] = set()
    for row in rows:
        svd_id = _text(row, "svd_id")
        if not svd_id:
            raise ValueError("blank svd_id")
        if svd_id in seen:
            raise ValueError(f"duplicate svd_id {svd_id!r}")
        seen.add(svd_id)
        for field in (
            "population_id", "field_event_id", "island_id", "site_id", "taxon", "plant_id", "flower_id",
            "record_type", "first_visit_confirmed", "bag_on_time", "bag_off_time", "stigma_collected_time",
            "pollen_count_method", "counter_id",
        ):
            if not _text(row, field):
                raise ValueError(f"blank {field} for svd_id={svd_id!r}")
        if _text(row, "island_id") not in VALID_ISLANDS:
            raise ValueError(f"invalid island_id for svd_id={svd_id!r}")
        if _text(row, "record_type") not in SVD_RECORD_TYPES:
            raise ValueError(f"invalid record_type for svd_id={svd_id!r}")
        if _text(row, "first_visit_confirmed") not in FIRST_VISIT_STATES:
            raise ValueError(f"invalid first_visit_confirmed for svd_id={svd_id!r}")
        if _text(row, "identification_confidence") not in IDENTIFICATION_CONFIDENCE:
            raise ValueError(f"invalid identification_confidence for svd_id={svd_id!r}")
        if _text(row, "pollen_count_method") not in POLLEN_COUNT_METHODS:
            raise ValueError(f"invalid pollen_count_method for svd_id={svd_id!r}")
        bag_on = _parse_time(_text(row, "bag_on_time"), field="bag_on_time", label=f"svd_id={svd_id!r}")
        bag_off = _parse_time(_text(row, "bag_off_time"), field="bag_off_time", label=f"svd_id={svd_id!r}")
        collected = _parse_time(
            _text(row, "stigma_collected_time"), field="stigma_collected_time", label=f"svd_id={svd_id!r}"
        )
        if bag_off < bag_on or collected < bag_off:
            raise ValueError(f"invalid bag/collection time order for svd_id={svd_id!r}")
        counts = {
            field: _nonnegative_int(row, field, f"svd_id={svd_id!r}")
            for field in (
                "total_pollen_grains", "conspecific_pollen_grains", "heterospecific_pollen_grains",
                "unclassified_pollen_grains",
            )
        }
        if counts["total_pollen_grains"] != (
            counts["conspecific_pollen_grains"]
            + counts["heterospecific_pollen_grains"]
            + counts["unclassified_pollen_grains"]
        ):
            raise ValueError(f"pollen count partition does not sum for svd_id={svd_id!r}")
        record_type = _text(row, "record_type")
        if record_type == "single_visit":
            for field in ("effort_id", "visit_id", "visitor_group"):
                if not _text(row, field):
                    raise ValueError(f"single_visit requires {field} for svd_id={svd_id!r}")
            if _text(row, "identification_confidence") == "not_applicable":
                raise ValueError(f"single_visit requires visitor identification status for svd_id={svd_id!r}")
            if _text(row, "first_visit_confirmed") != "yes":
                raise ValueError(f"single_visit requires confirmed first visit for svd_id={svd_id!r}")
        else:
            if any(_text(row, field) for field in ("visit_id", "visitor_group")):
                raise ValueError(f"no-visit control cannot name a visitor for svd_id={svd_id!r}")
            if _text(row, "first_visit_confirmed") != "not_applicable":
                raise ValueError(f"no-visit control requires first_visit_confirmed=not_applicable for svd_id={svd_id!r}")
            if _text(row, "identification_confidence") != "not_applicable":
                raise ValueError(f"no-visit control requires identification_confidence=not_applicable for svd_id={svd_id!r}")
    return rows


def read_pollination_treatments(path: Path) -> tuple[dict[str, str], ...]:
    rows = _read_csv(path, TREATMENT_COLUMNS, "pollination treatment manifest")
    seen: set[str] = set()
    flower_seen: set[tuple[str, str]] = set()
    for row in rows:
        treatment_id = _text(row, "treatment_id")
        if not treatment_id:
            raise ValueError("blank treatment_id")
        if treatment_id in seen:
            raise ValueError(f"duplicate treatment_id {treatment_id!r}")
        seen.add(treatment_id)
        for field in (
            "population_id", "field_event_id", "island_id", "site_id", "taxon", "plant_id", "flower_id",
            "treatment_type", "assigned_at", "outcome_status",
        ):
            if not _text(row, field):
                raise ValueError(f"blank {field} for treatment_id={treatment_id!r}")
        if _text(row, "island_id") not in VALID_ISLANDS:
            raise ValueError(f"invalid island_id for treatment_id={treatment_id!r}")
        if _text(row, "treatment_type") not in TREATMENT_TYPES:
            raise ValueError(f"invalid treatment_type for treatment_id={treatment_id!r}")
        if _text(row, "outcome_status") not in OUTCOME_STATES:
            raise ValueError(f"invalid outcome_status for treatment_id={treatment_id!r}")
        _parse_time(_text(row, "assigned_at"), field="assigned_at", label=f"treatment_id={treatment_id!r}")
        key = (_text(row, "plant_id"), _text(row, "flower_id"))
        if key in flower_seen:
            raise ValueError(f"flower assigned to multiple pollination treatments: {key!r}")
        flower_seen.add(key)
        treatment = _text(row, "treatment_type")
        bag_on = _text(row, "bag_on_time")
        bag_off = _text(row, "bag_off_time")
        if treatment == "bagged_autonomous" and not bag_on:
            raise ValueError(f"bagged_autonomous requires bag_on_time for treatment_id={treatment_id!r}")
        if treatment in {"supplemental_outcross", "hand_self"}:
            if not _text(row, "hand_pollen_source_plant_id"):
                raise ValueError(f"{treatment} requires hand_pollen_source_plant_id for treatment_id={treatment_id!r}")
        if treatment == "supplemental_outcross" and _text(row, "hand_pollen_source_plant_id") == _text(row, "plant_id"):
            raise ValueError(f"supplemental_outcross donor must differ from maternal plant for treatment_id={treatment_id!r}")
        if treatment == "hand_self" and _text(row, "hand_pollen_source_plant_id") != _text(row, "plant_id"):
            raise ValueError(f"hand_self donor must equal maternal plant for treatment_id={treatment_id!r}")
        if bag_on:
            on = _parse_time(bag_on, field="bag_on_time", label=f"treatment_id={treatment_id!r}")
            if bag_off:
                off = _parse_time(bag_off, field="bag_off_time", label=f"treatment_id={treatment_id!r}")
                if off < on:
                    raise ValueError(f"bag_off_time before bag_on_time for treatment_id={treatment_id!r}")
        if _text(row, "outcome_status") == "mature_fruit" and not _text(row, "fruit_id"):
            raise ValueError(f"mature_fruit requires fruit_id for treatment_id={treatment_id!r}")
        if _text(row, "outcome_status") != "mature_fruit" and _text(row, "fruit_id"):
            raise ValueError(f"fruit_id is only allowed for mature_fruit outcome in treatment_id={treatment_id!r}")
    return rows


def _float(row: Mapping[str, object], field: str, label: str) -> float:
    try:
        return float(_text(row, field))
    except ValueError as error:
        raise ValueError(f"{field} must be numeric for {label}") from error


def _population_registry(plants: Sequence[Mapping[str, object]]) -> tuple[dict[str, Mapping[str, object]], dict[str, tuple[str, str, str]]]:
    by_plant: dict[str, Mapping[str, object]] = {}
    population_meta: dict[str, tuple[str, str, str]] = {}
    for row in plants:
        plant_id = _text(row, "plant_id")
        pop = _text(row, "population_id")
        by_plant[plant_id] = row
        signature = (_text(row, "island_id"), _text(row, "site_id"), _text(row, "taxon"))
        previous = population_meta.setdefault(pop, signature)
        if previous != signature:
            raise ValueError(f"population_id={pop!r} mixes island/site/taxon signatures")
    return by_plant, population_meta


def _validate_row_link(row: Mapping[str, object], registry: Mapping[str, Mapping[str, object]], row_id: str) -> str:
    plant_id = _text(row, "plant_id")
    plant = registry.get(plant_id)
    if plant is None:
        raise ValueError(f"{row_id} references unregistered plant_id={plant_id!r}")
    for field in ("population_id", "field_event_id", "island_id", "site_id", "taxon"):
        if _text(row, field) != _text(plant, field):
            raise ValueError(f"{row_id} does not match registered plant {field}")
    return _text(plant, "population_id")


def _effort_duration_seconds(row: Mapping[str, object]) -> float:
    start = _parse_time(_text(row, "start_time"), field="start_time", label=f"effort_id={_text(row, 'effort_id')!r}")
    end = _parse_time(_text(row, "end_time"), field="end_time", label=f"effort_id={_text(row, 'effort_id')!r}")
    return (end - start).total_seconds()


def _fruit_index(fruit_rows: Sequence[Mapping[str, object]] | None) -> dict[str, Mapping[str, object]]:
    index: dict[str, Mapping[str, object]] = {}
    for row in fruit_rows or ():
        fruit_id = _text(row, "fruit_id")
        if not fruit_id:
            raise ValueError("blank fruit_id in fruit manifest")
        if fruit_id in index:
            raise ValueError(f"duplicate fruit_id={fruit_id!r}")
        index[fruit_id] = row
    return index


def audit_effective_pollinator_dependency(
    plants: Sequence[Mapping[str, object]],
    effort_rows: Sequence[Mapping[str, object]],
    visit_rows: Sequence[Mapping[str, object]],
    svd_rows: Sequence[Mapping[str, object]],
    treatment_rows: Sequence[Mapping[str, object]],
    fruit_rows: Sequence[Mapping[str, object]] | None = None,
) -> EffectiveDependencyAudit:
    registry, population_meta = _population_registry(plants)
    fruits = _fruit_index(fruit_rows)

    # Link SVD/treatment rows to the same tagged plants/populations.
    for row in svd_rows:
        _validate_row_link(row, registry, f"svd_id={_text(row, 'svd_id')!r}")
    for row in treatment_rows:
        _validate_row_link(row, registry, f"treatment_id={_text(row, 'treatment_id')!r}")
        if fruits and _text(row, "outcome_status") == "mature_fruit":
            fruit = fruits.get(_text(row, "fruit_id"))
            if fruit is None:
                raise ValueError(f"treatment_id={_text(row, 'treatment_id')!r} references unknown fruit_id")
            if _text(fruit, "site_id") != _text(row, "site_id") or _text(fruit, "maternal_id") != _text(row, "plant_id"):
                raise ValueError(f"treatment_id={_text(row, 'treatment_id')!r} does not match linked fruit site/maternal_id")

    # Contact effort and visits must be attributable to tagged plants for this panel.
    exposure_by_population: dict[str, float] = defaultdict(float)
    effort_by_id: dict[str, Mapping[str, object]] = {}
    for effort in effort_rows:
        effort_id = _text(effort, "effort_id")
        if not effort_id:
            raise ValueError("blank effort_id in effective-dependency audit")
        effort_by_id[effort_id] = effort
        if _text(effort, "usable_observation") != "yes":
            continue
        plant_id = _text(effort, "plant_id")
        if not plant_id or plant_id not in registry:
            raise ValueError(f"usable effort_id={effort_id!r} lacks a registered plant_id")
        plant = registry[plant_id]
        for field in ("field_event_id", "island_id", "site_id"):
            if _text(effort, field) != _text(plant, field):
                raise ValueError(f"effort_id={effort_id!r} does not match registered plant {field}")
        duration_h = _effort_duration_seconds(effort) / 3600.0
        flowers = _float(effort, "monitored_open_flower_count", f"effort_id={effort_id!r}")
        if flowers <= 0:
            raise ValueError(f"monitored_open_flower_count must be positive for effort_id={effort_id!r}")
        exposure_by_population[_text(plant, "population_id")] += duration_h * flowers

    visit_counts: dict[tuple[str, str], int] = defaultdict(int)
    visit_by_id: dict[str, Mapping[str, object]] = {}
    for visit in visit_rows:
        visit_id = _text(visit, "visit_id")
        if not visit_id:
            raise ValueError("blank visit_id in effective-dependency audit")
        if visit_id in visit_by_id:
            raise ValueError(f"duplicate visit_id={visit_id!r}")
        visit_by_id[visit_id] = visit
        effort = effort_by_id.get(_text(visit, "effort_id"))
        if effort is None or _text(effort, "usable_observation") != "yes":
            raise ValueError(f"visit_id={visit_id!r} lacks usable effort")
        plant_id = _text(visit, "plant_id") or _text(effort, "plant_id")
        if not plant_id or plant_id not in registry:
            raise ValueError(f"visit_id={visit_id!r} lacks registered plant identity")
        pop = _text(registry[plant_id], "population_id")
        visit_counts[(pop, _text(visit, "visitor_group"))] += 1

    # Ensure each SVD single-visit row points back to the same observed visit.
    for row in svd_rows:
        if _text(row, "record_type") != "single_visit":
            continue
        visit = visit_by_id.get(_text(row, "visit_id"))
        if visit is None:
            raise ValueError(f"svd_id={_text(row, 'svd_id')!r} references unknown visit_id")
        if _text(visit, "effort_id") != _text(row, "effort_id"):
            raise ValueError(f"svd_id={_text(row, 'svd_id')!r} does not match visit effort_id")
        for field in ("plant_id", "flower_id", "visitor_group"):
            if _text(visit, field) and _text(row, field) != _text(visit, field):
                raise ValueError(f"svd_id={_text(row, 'svd_id')!r} does not match visit {field}")

    # Background pollen on no-visit controls.
    control_values: dict[tuple[str, str], list[int]] = defaultdict(list)
    single_values: dict[tuple[str, str], list[int]] = defaultdict(list)
    for row in svd_rows:
        pop = _text(row, "population_id")
        count = _nonnegative_int(row, "conspecific_pollen_grains", f"svd_id={_text(row, 'svd_id')!r}")
        record_type = _text(row, "record_type")
        if record_type == "single_visit":
            single_values[(pop, _text(row, "visitor_group"))].append(count)
        else:
            control_values[(pop, record_type)].append(count)

    svd_group_rows: list[dict[str, str]] = []
    net_svd: dict[tuple[str, str], float] = {}
    for (pop, visitor_group), values in sorted(single_values.items()):
        exposed_controls = control_values.get((pop, "exposed_no_visit_control"), [])
        bagged_controls = control_values.get((pop, "bagged_unvisited_control"), [])
        if exposed_controls:
            background = mean(exposed_controls)
            background_basis = "exposed_no_visit_control"
        elif bagged_controls:
            background = mean(bagged_controls)
            background_basis = "bagged_unvisited_control"
        else:
            background = 0.0
            background_basis = "missing_no_visit_control"
        raw = mean(values)
        adjusted = max(0.0, raw - background)
        net_svd[(pop, visitor_group)] = adjusted
        island, site, taxon = population_meta[pop]
        svd_group_rows.append({
            "population_id": pop,
            "island_id": island,
            "site_id": site,
            "taxon": taxon,
            "visitor_group": visitor_group,
            "single_visit_svd_n": str(len(values)),
            "mean_raw_conspecific_pollen": f"{raw:.8f}",
            "background_control_basis": background_basis,
            "background_control_n": str(len(exposed_controls) if exposed_controls else len(bagged_controls)),
            "mean_background_conspecific_pollen": f"{background:.8f}" if background_basis != "missing_no_visit_control" else "",
            "mean_background_adjusted_svd": f"{adjusted:.8f}" if background_basis != "missing_no_visit_control" else "",
            "boundary": "SVD is per-visit pollen deposition, not seed production or historical selection.",
        })

    effective_service_rows: list[dict[str, str]] = []
    service_by_population: dict[str, list[tuple[str, float]]] = defaultdict(list)
    observed_groups_by_population: dict[str, set[str]] = defaultdict(set)
    for (pop, visitor_group), visits in sorted(visit_counts.items()):
        observed_groups_by_population[pop].add(visitor_group)
        exposure = exposure_by_population.get(pop, 0.0)
        if exposure <= 0:
            continue
        rate = visits / exposure
        svd = net_svd.get((pop, visitor_group))
        service = None if svd is None else rate * svd
        if service is not None:
            service_by_population[pop].append((visitor_group, service))
        island, site, taxon = population_meta[pop]
        effective_service_rows.append({
            "population_id": pop,
            "island_id": island,
            "site_id": site,
            "taxon": taxon,
            "visitor_group": visitor_group,
            "usable_monitored_flower_hours": f"{exposure:.8f}",
            "visit_bouts": str(visits),
            "visit_bouts_per_flower_hour": f"{rate:.8f}",
            "mean_background_adjusted_svd": "" if svd is None else f"{svd:.8f}",
            "effective_pollen_delivery_per_flower_hour": "" if service is None else f"{service:.8f}",
            "effective_service_share": "",
            "boundary": "Rate-weighted SVD is a realized service estimate within sampled windows, not island-wide absence/presence.",
        })
    totals = {pop: sum(value for _, value in values) for pop, values in service_by_population.items()}
    for row in effective_service_rows:
        pop = row["population_id"]
        value = row["effective_pollen_delivery_per_flower_hour"]
        total = totals.get(pop, 0.0)
        if value and total > 0:
            row["effective_service_share"] = f"{float(value) / total:.8f}"

    # Treatment outcome summaries, with seed outcome linked to the existing fruits table when supplied.
    treatment_buckets: dict[tuple[str, str], list[Mapping[str, object]]] = defaultdict(list)
    for row in treatment_rows:
        treatment_buckets[(_text(row, "population_id"), _text(row, "treatment_type"))].append(row)
    treatment_summary_rows: list[dict[str, str]] = []
    treatment_analyzable_n: dict[tuple[str, str], int] = {}
    treatment_capsule_set: dict[tuple[str, str], float] = {}
    for (pop, treatment), rows in sorted(treatment_buckets.items()):
        analyzable = [row for row in rows if _text(row, "outcome_status") in {"mature_fruit", "aborted"}]
        mature = [row for row in analyzable if _text(row, "outcome_status") == "mature_fruit"]
        capsule_set = (len(mature) / len(analyzable)) if analyzable else None
        treatment_analyzable_n[(pop, treatment)] = len(analyzable)
        if capsule_set is not None:
            treatment_capsule_set[(pop, treatment)] = capsule_set
        seeds_per_assigned: list[int] = []
        if fruits and analyzable:
            for row in analyzable:
                if _text(row, "outcome_status") == "aborted":
                    seeds_per_assigned.append(0)
                else:
                    fruit = fruits[_text(row, "fruit_id")]
                    seeds_per_assigned.append(_nonnegative_int(fruit, "mature_seed_count", f"fruit_id={_text(fruit, 'fruit_id')!r}"))
        island, site, taxon = population_meta[pop]
        treatment_summary_rows.append({
            "population_id": pop,
            "island_id": island,
            "site_id": site,
            "taxon": taxon,
            "treatment_type": treatment,
            "assigned_flowers": str(len(rows)),
            "analyzable_flowers": str(len(analyzable)),
            "mature_fruits": str(len(mature)),
            "capsule_set_proportion": "" if capsule_set is None else f"{capsule_set:.8f}",
            "mean_mature_seeds_per_analyzable_flower": "" if not seeds_per_assigned else f"{mean(seeds_per_assigned):.8f}",
            "pending_or_lost_flowers": str(len(rows) - len(analyzable)),
            "boundary": "Treatment outcomes separate autonomous capacity, open service and supplemental pollen; they do not identify realized selfing.",
        })

    population_readiness_rows: list[dict[str, str]] = []
    for pop, (island, site, taxon) in sorted(population_meta.items()):
        svd_groups = {group for (p, group), _values in single_values.items() if p == pop}
        control_exposed_n = len(control_values.get((pop, "exposed_no_visit_control"), []))
        control_bagged_n = len(control_values.get((pop, "bagged_unvisited_control"), []))
        service_estimable_groups = {
            group for group, value in service_by_population.get(pop, []) if value >= 0
        }
        core_counts = {t: treatment_analyzable_n.get((pop, t), 0) for t in CORE_TREATMENTS}
        core_complete = all(value > 0 for value in core_counts.values())
        effect_complete = exposure_by_population.get(pop, 0.0) > 0 and bool(service_estimable_groups) and (
            control_exposed_n > 0 or control_bagged_n > 0
        )
        supplemental = treatment_capsule_set.get((pop, "supplemental_outcross"))
        bagged = treatment_capsule_set.get((pop, "bagged_autonomous"))
        opened = treatment_capsule_set.get((pop, "open_pollinated"))
        autonomous_ratio = None
        open_ratio = None
        if supplemental is not None and supplemental > 0:
            if bagged is not None:
                autonomous_ratio = bagged / supplemental
            if opened is not None:
                open_ratio = opened / supplemental
        population_readiness_rows.append({
            "population_id": pop,
            "island_id": island,
            "site_id": site,
            "taxon": taxon,
            "registered_plants": str(sum(1 for row in plants if _text(row, "population_id") == pop)),
            "usable_monitored_flower_hours": f"{exposure_by_population.get(pop, 0.0):.8f}",
            "visitor_groups_observed": str(len(observed_groups_by_population.get(pop, set()))),
            "visitor_groups_with_svd": str(len(svd_groups)),
            "visitor_groups_with_rate_weighted_svd": str(len(service_estimable_groups)),
            "exposed_no_visit_controls": str(control_exposed_n),
            "bagged_unvisited_controls": str(control_bagged_n),
            "open_pollinated_analyzable": str(core_counts["open_pollinated"]),
            "bagged_autonomous_analyzable": str(core_counts["bagged_autonomous"]),
            "supplemental_outcross_analyzable": str(core_counts["supplemental_outcross"]),
            "effective_service_structurally_estimable": "yes" if effect_complete else "no",
            "core_reproductive_panel_structurally_complete": "yes" if core_complete else "no",
            "dependency_panel_structurally_complete": "yes" if (effect_complete and core_complete) else "no",
            "autonomous_to_supplemental_capsule_ratio": "" if autonomous_ratio is None else f"{autonomous_ratio:.8f}",
            "open_to_supplemental_capsule_ratio": "" if open_ratio is None else f"{open_ratio:.8f}",
            "boundary": BOUNDARY,
        })

    summary = {
        "populations": len(population_meta),
        "registered_plants": len(plants),
        "svd_records": len(svd_rows),
        "single_visit_svd_records": sum(_text(row, "record_type") == "single_visit" for row in svd_rows),
        "treatment_assignments": len(treatment_rows),
        "structurally_complete_populations": sum(
            row["dependency_panel_structurally_complete"] == "yes" for row in population_readiness_rows
        ),
        "claim_boundary": BOUNDARY,
    }
    return EffectiveDependencyAudit(
        svd_group_rows=tuple(svd_group_rows),
        effective_service_rows=tuple(effective_service_rows),
        treatment_rows=tuple(treatment_summary_rows),
        population_readiness_rows=tuple(population_readiness_rows),
        summary=summary,
    )


def _write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_effective_dependency_audit(output_dir: Path, audit: EffectiveDependencyAudit) -> None:
    import json

    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "svd_by_visitor_group.csv", audit.svd_group_rows)
    _write_csv(output_dir / "rate_weighted_effective_service.csv", audit.effective_service_rows)
    _write_csv(output_dir / "pollination_treatment_summary.csv", audit.treatment_rows)
    _write_csv(output_dir / "population_dependency_readiness.csv", audit.population_readiness_rows)
    (output_dir / "summary.json").write_text(json.dumps(dict(audit.summary), indent=2) + "\n", encoding="utf-8")
