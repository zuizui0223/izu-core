#!/usr/bin/env python3
"""Audit whether direct dependency field data can move beyond structural completion.

This is deliberately stricter than the structural panel audit and deliberately
weaker than a power/precision claim.  It separates three states:

1. structural completion: linked channels exist;
2. plant-level dispersion estimability: at least two independent plants
   contribute to the relevant quantity; and
3. confirmatory adequacy: never inferred here; it requires a separately chosen
   precision target and pilot-derived variance/loss assumptions.

Flowers and repeated visits within one plant are subsamples.  Missing,
pending, lost, damaged, unresolved, or unscorable records never manufacture
independent plant replication.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Mapping

CORE_TREATMENTS = ("open_pollinated", "bagged_autonomous", "supplemental_outcross")
TERMINAL_ANALYZABLE_OUTCOMES = frozenset({"mature_fruit", "aborted"})
NO_VISIT_CONTROLS = frozenset({"exposed_no_visit_control", "bagged_unvisited_control"})


def _read(path: Path) -> tuple[dict[str, str], ...]:
    with path.open(newline="", encoding="utf-8") as handle:
        return tuple(csv.DictReader(handle))


def _text(row: Mapping[str, object], field: str) -> str:
    return str(row.get(field, "") or "").strip()


def _require(rows: Iterable[Mapping[str, object]], columns: set[str], label: str) -> None:
    rows = tuple(rows)
    if not rows:
        return
    missing = columns - set(rows[0])
    if missing:
        raise ValueError(f"{label} missing columns: " + ", ".join(sorted(missing)))


def build_admission(
    plants: tuple[dict[str, str], ...],
    svd: tuple[dict[str, str], ...],
    treatments: tuple[dict[str, str], ...],
) -> dict[str, object]:
    _require(plants, {"population_id", "plant_id"}, "plants")
    _require(svd, {"population_id", "plant_id", "record_type", "visitor_group"}, "svd")
    _require(
        treatments,
        {"population_id", "plant_id", "treatment_type", "outcome_status"},
        "treatments",
    )

    registered: dict[str, set[str]] = defaultdict(set)
    for row in plants:
        registered[_text(row, "population_id")].add(_text(row, "plant_id"))

    svd_plants: dict[tuple[str, str], set[str]] = defaultdict(set)
    controls: dict[str, int] = defaultdict(int)
    for row in svd:
        pop = _text(row, "population_id")
        record_type = _text(row, "record_type")
        if record_type == "single_visit":
            group = _text(row, "visitor_group")
            if group:
                svd_plants[(pop, group)].add(_text(row, "plant_id"))
        elif record_type in NO_VISIT_CONTROLS:
            controls[pop] += 1

    treatment_plants: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in treatments:
        treatment = _text(row, "treatment_type")
        if treatment not in CORE_TREATMENTS:
            continue
        if _text(row, "outcome_status") not in TERMINAL_ANALYZABLE_OUTCOMES:
            continue
        treatment_plants[(_text(row, "population_id"), treatment)].add(_text(row, "plant_id"))

    populations: list[dict[str, object]] = []
    for pop in sorted(registered):
        group_counts = {
            group: len(ids)
            for (p, group), ids in sorted(svd_plants.items())
            if p == pop
        }
        svd_dispersion_groups = sorted(group for group, n in group_counts.items() if n >= 2)
        treatment_counts = {
            treatment: len(treatment_plants.get((pop, treatment), set()))
            for treatment in CORE_TREATMENTS
        }
        treatment_dispersion_estimable = all(n >= 2 for n in treatment_counts.values())
        controlled_svd_dispersion_estimable = bool(svd_dispersion_groups) and controls.get(pop, 0) > 0
        dispersion_gate = controlled_svd_dispersion_estimable and treatment_dispersion_estimable
        populations.append({
            "population_id": pop,
            "registered_independent_plants": len(registered[pop]),
            "no_visit_control_records": controls.get(pop, 0),
            "single_visit_svd_distinct_plants_by_group": group_counts,
            "svd_groups_with_between_plant_dispersion_estimable": svd_dispersion_groups,
            "core_treatment_distinct_plants_with_terminal_outcome": treatment_counts,
            "controlled_svd_between_plant_dispersion_estimable": controlled_svd_dispersion_estimable,
            "core_treatment_between_plant_dispersion_estimable": treatment_dispersion_estimable,
            "pilot_dispersion_gate_pass": dispersion_gate,
            "confirmatory_adequacy": False,
            "boundary": (
                "Two plants is only the minimum needed for a between-plant variance to be defined. "
                "It is not a power, precision, equivalence, geographic-replication, or causal-identification threshold."
            ),
        })

    return {
        "schema_version": "effective_dependency_admission_v1",
        "populations": populations,
        "n_populations_passing_dispersion_gate": sum(bool(row["pilot_dispersion_gate_pass"]) for row in populations),
        "confirmatory_adequacy_inferred": False,
        "claim_boundary": (
            "Passing this audit only permits pilot variance/reliability estimation and precision planning. "
            "It does not permit historical Bombus causation, an Oshima-Toshima causal boundary claim, "
            "or a confirmatory sample-size claim."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plants", type=Path, required=True)
    parser.add_argument("--svd", type=Path, required=True)
    parser.add_argument("--treatments", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = build_admission(_read(args.plants), _read(args.svd), _read(args.treatments))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
