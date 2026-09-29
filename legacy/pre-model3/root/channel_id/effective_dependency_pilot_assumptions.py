"""Empirical pilot assumptions for direct effective-pollinator dependency work.

This module converts raw pilot structure into quantities that may legitimately
replace declared synthetic planning assumptions: observed panel coverage and
explicit treatment loss/pending fractions. It deliberately does not relabel
biological replicate variation as measurement reliability.

Repeated flowers or visits within one plant are biological subsamples. Without
an independent repeated-measurement/calibration design, those repeats do not
identify the reliability ratio of the eventual direct dependency estimand.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Mapping, Sequence

CORE_TREATMENTS = ("open_pollinated", "bagged_autonomous", "supplemental_outcross")
TERMINAL = frozenset({"mature_fruit", "aborted"})
LOSS = frozenset({"lost", "damaged"})
NO_VISIT_CONTROLS = frozenset({"exposed_no_visit_control", "bagged_unvisited_control"})


def _text(row: Mapping[str, object], field: str) -> str:
    return str(row.get(field, "") or "").strip()


def _fraction(numerator: int, denominator: int) -> float | None:
    if denominator <= 0:
        return None
    return numerator / denominator


def build_pilot_assumption_audit(
    plants: Sequence[Mapping[str, object]],
    svd: Sequence[Mapping[str, object]],
    treatments: Sequence[Mapping[str, object]],
) -> dict[str, object]:
    """Summarize empirical coverage/loss while keeping reliability unidentified."""
    registered: dict[str, set[str]] = defaultdict(set)
    for row in plants:
        pop = _text(row, "population_id")
        plant = _text(row, "plant_id")
        if pop and plant:
            registered[pop].add(plant)

    controls: dict[str, int] = defaultdict(int)
    svd_events: dict[tuple[str, str, str], int] = defaultdict(int)
    for row in svd:
        pop = _text(row, "population_id")
        record_type = _text(row, "record_type")
        if record_type == "single_visit":
            group = _text(row, "visitor_group")
            plant = _text(row, "plant_id")
            if pop and group and plant:
                svd_events[(pop, group, plant)] += 1
        elif record_type in NO_VISIT_CONTROLS and pop:
            controls[pop] += 1

    treatment_status: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    for row in treatments:
        pop = _text(row, "population_id")
        treatment = _text(row, "treatment_type")
        plant = _text(row, "plant_id")
        if pop and treatment in CORE_TREATMENTS and plant:
            treatment_status[(pop, treatment, plant)].append(_text(row, "outcome_status"))

    populations: list[dict[str, object]] = []
    for pop in sorted(registered):
        registered_plants = registered[pop]
        group_rows: list[dict[str, object]] = []
        groups = sorted({group for (p, group, _plant) in svd_events if p == pop})
        controlled_svd_plants: set[str] = set()
        for group in groups:
            counts = {
                plant: n
                for (p, g, plant), n in svd_events.items()
                if p == pop and g == group
            }
            group_plants = set(counts)
            if controls.get(pop, 0) > 0:
                controlled_svd_plants.update(group_plants)
            group_rows.append({
                "visitor_group": group,
                "single_visit_events": sum(counts.values()),
                "independent_plants": len(group_plants),
                "plants_with_two_or_more_svd_events": sum(n >= 2 for n in counts.values()),
                "no_visit_control_records_in_population": controls.get(pop, 0),
                "controlled_svd_available": bool(group_plants) and controls.get(pop, 0) > 0,
            })

        treatment_rows: list[dict[str, object]] = []
        plants_with_terminal_by_treatment: dict[str, set[str]] = {}
        for treatment in CORE_TREATMENTS:
            statuses_by_plant = {
                plant: statuses
                for (p, t, plant), statuses in treatment_status.items()
                if p == pop and t == treatment
            }
            assigned = sum(len(statuses) for statuses in statuses_by_plant.values())
            terminal = sum(status in TERMINAL for statuses in statuses_by_plant.values() for status in statuses)
            lost_damaged = sum(status in LOSS for statuses in statuses_by_plant.values() for status in statuses)
            pending = sum(status == "pending" for statuses in statuses_by_plant.values() for status in statuses)
            terminal_plants = {
                plant
                for plant, statuses in statuses_by_plant.items()
                if any(status in TERMINAL for status in statuses)
            }
            plants_with_terminal_by_treatment[treatment] = terminal_plants
            treatment_rows.append({
                "treatment_type": treatment,
                "assigned_flowers": assigned,
                "terminal_analyzable_flowers": terminal,
                "lost_or_damaged_flowers": lost_damaged,
                "pending_flowers": pending,
                "terminal_coverage_fraction": _fraction(terminal, assigned),
                "loss_damage_fraction": _fraction(lost_damaged, assigned),
                "pending_fraction": _fraction(pending, assigned),
                "independent_plants_with_terminal_outcome": len(terminal_plants),
                "registered_plant_coverage_fraction": _fraction(len(terminal_plants), len(registered_plants)),
            })

        core_terminal_joint = set(registered_plants)
        for treatment in CORE_TREATMENTS:
            core_terminal_joint &= plants_with_terminal_by_treatment[treatment]
        joint_with_svd = core_terminal_joint & controlled_svd_plants

        populations.append({
            "population_id": pop,
            "registered_independent_plants": len(registered_plants),
            "visitor_group_svd": group_rows,
            "treatments": treatment_rows,
            "plants_with_controlled_svd_any_group": len(controlled_svd_plants),
            "controlled_svd_registered_plant_coverage_fraction": _fraction(
                len(controlled_svd_plants), len(registered_plants)
            ),
            "plants_with_terminal_outcomes_all_core_treatments": len(core_terminal_joint),
            "core_treatment_registered_plant_coverage_fraction": _fraction(
                len(core_terminal_joint), len(registered_plants)
            ),
            "plants_with_controlled_svd_and_all_core_terminal_treatments": len(joint_with_svd),
            "joint_panel_registered_plant_coverage_fraction": _fraction(
                len(joint_with_svd), len(registered_plants)
            ),
        })

    return {
        "schema_version": "effective_dependency_pilot_assumptions_v1",
        "populations": populations,
        "synthetic_assumption_replacement": {
            "between_plant_variance": {
                "status": "handled_by_pilot_precision_dispersion_audit",
                "source": "svd_pilot_dispersion.csv and treatment_pilot_dispersion.csv",
            },
            "coverage": {
                "status": "empirically_summarized_when_pilot_rows_exist",
                "boundary": "These are observed pilot panel-coverage fractions, not automatically the taxon x site x season coverage fraction used by the dependency x FDQ design simulation.",
            },
            "loss": {
                "status": "empirically_summarized_when_treatment_rows_exist",
                "boundary": "Lost and damaged remain separate from reproductive failure; pending remains separate from both.",
            },
            "dependency_reliability": {
                "status": "not_identified_from_current_pilot_schema",
                "reason": "Repeated flowers/SVD events within a plant mix biological subsampling variation with measurement variation and therefore do not identify a measurement-error reliability ratio for the direct dependency estimand.",
                "required_next_evidence": "An independent repeat/calibration design or another identified measurement-error model for the final dependency estimand.",
            },
            "all_synthetic_assumptions_replaced": False,
        },
        "automatic_design_simulation_injection_allowed": False,
        "claim_boundary": (
            "This audit describes empirical pilot coverage, treatment attrition, and repeated-SVD structure. "
            "It does not identify direct-dependency reliability, empirical power, historical Bombus causation, "
            "or a dependency x FDQ effect."
        ),
    }
