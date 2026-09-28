#!/usr/bin/env python3
"""Audit the Izu visitor -> SVD -> dependency -> seed chain on same plants/blocks.

This is a structural bridge from the Chapter 2 synthetic hierarchy to prospective
Izu field data.  It does not estimate historical causation or confirmatory effect
sizes.  Existing field validators are reused, then a stricter block x plant gate
is applied on top.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from statistics import mean
from typing import Iterable, Mapping, Sequence

from channel_id.effective_pollinator_dependency import (
    CORE_TREATMENTS,
    audit_effective_pollinator_dependency,
    read_dependency_plant_registry,
    read_pollination_treatments,
    read_svd_manifest,
)
from channel_id.field_legitimate_contact import audit_field_contacts, read_effort_manifest, read_visit_manifest
from scripts.audit_effective_pollinator_dependency import read_fruits


BLOCK_COLUMNS = (
    "block_id", "population_id", "field_event_id", "island_id", "site_id", "taxon",
    "block_start", "block_end", "season_id", "block_role", "predeclared_before_outcomes", "notes",
)
GEOMETRY_REQUIRED = (
    "field_event_id", "island_id", "site_id", "plant_id", "flower_id", "measurement_id",
    "corolla_length_mm", "corolla_mouth_diameter_mm", "corolla_inner_depth_mm", "measurement_date",
)
BLOCK_ROLES = frozenset({"pilot", "confirmatory", "calibration", "exploratory"})
YES_NO = frozenset({"yes", "no"})
TERMINAL_ANALYZABLE = frozenset({"mature_fruit", "aborted"})
NO_VISIT_TYPES = frozenset({"bagged_unvisited_control", "exposed_no_visit_control"})

BOUNDARY = (
    "A structurally complete block x plant chain is not a power claim or historical causal transition. "
    "It only establishes that richness/composition exposure, SVD/effective service, dependency and seed "
    "outcomes can be linked without changing tagged plant or prespecified block."
)


def _text(row: Mapping[str, object], field: str) -> str:
    return str(row.get(field, "") or "").strip()


def _parse_dt(value: str, *, label: str) -> datetime:
    try:
        out = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"invalid ISO-8601 datetime for {label}: {value!r}") from exc
    if out.tzinfo is None:
        raise ValueError(f"timezone offset required for {label}")
    return out


def _require_columns(fieldnames: Iterable[str], required: Sequence[str], label: str) -> None:
    missing = set(required) - set(fieldnames)
    if missing:
        raise ValueError(f"{label} missing columns: " + ", ".join(sorted(missing)))


def read_blocks(path: Path) -> tuple[dict[str, str], ...]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _require_columns(reader.fieldnames or (), BLOCK_COLUMNS, "transition block manifest")
        rows = tuple(reader)
    seen: set[str] = set()
    for row in rows:
        block_id = _text(row, "block_id")
        if not block_id:
            raise ValueError("blank block_id")
        if block_id in seen:
            raise ValueError(f"duplicate block_id={block_id!r}")
        seen.add(block_id)
        for field in (
            "population_id", "field_event_id", "island_id", "site_id", "taxon", "block_start",
            "block_end", "season_id", "block_role", "predeclared_before_outcomes",
        ):
            if not _text(row, field):
                raise ValueError(f"blank {field} for block_id={block_id!r}")
        if _text(row, "block_role") not in BLOCK_ROLES:
            raise ValueError(f"invalid block_role for block_id={block_id!r}")
        if _text(row, "predeclared_before_outcomes") not in YES_NO:
            raise ValueError(f"invalid predeclared_before_outcomes for block_id={block_id!r}")
        start = _parse_dt(_text(row, "block_start"), label=f"block_id={block_id!r} block_start")
        end = _parse_dt(_text(row, "block_end"), label=f"block_id={block_id!r} block_end")
        if end <= start:
            raise ValueError(f"block_end must be after block_start for block_id={block_id!r}")
    return rows


def read_geometry(path: Path) -> tuple[dict[str, str], ...]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _require_columns(reader.fieldnames or (), GEOMETRY_REQUIRED, "flower geometry manifest")
        rows = tuple(reader)
    for row in rows:
        measurement_id = _text(row, "measurement_id")
        if not measurement_id or not _text(row, "plant_id"):
            raise ValueError("geometry rows require measurement_id and plant_id")
        for field in ("corolla_length_mm", "corolla_mouth_diameter_mm", "corolla_inner_depth_mm"):
            try:
                value = float(_text(row, field))
            except ValueError as exc:
                raise ValueError(f"{field} must be numeric for measurement_id={measurement_id!r}") from exc
            if value <= 0:
                raise ValueError(f"{field} must be positive for measurement_id={measurement_id!r}")
        try:
            date.fromisoformat(_text(row, "measurement_date"))
        except ValueError as exc:
            raise ValueError(f"invalid measurement_date for measurement_id={measurement_id!r}") from exc
    return rows


def _row_signature(row: Mapping[str, object]) -> tuple[str, str, str]:
    return (_text(row, "field_event_id"), _text(row, "island_id"), _text(row, "site_id"))


def _block_signature(block: Mapping[str, object]) -> tuple[str, str, str]:
    return (_text(block, "field_event_id"), _text(block, "island_id"), _text(block, "site_id"))


def _block_window(block: Mapping[str, object]) -> tuple[datetime, datetime]:
    return (
        _parse_dt(_text(block, "block_start"), label=f"block_id={_text(block, 'block_id')!r} block_start"),
        _parse_dt(_text(block, "block_end"), label=f"block_id={_text(block, 'block_id')!r} block_end"),
    )


def _match_block_at_time(
    row: Mapping[str, object],
    when: datetime,
    blocks: Sequence[Mapping[str, object]],
    *,
    label: str,
) -> str:
    candidates: list[str] = []
    signature = _row_signature(row)
    for block in blocks:
        if _block_signature(block) != signature:
            continue
        start, end = _block_window(block)
        if start <= when <= end:
            candidates.append(_text(block, "block_id"))
    if len(candidates) != 1:
        raise ValueError(f"{label} must map to exactly one transition block; found {candidates!r}")
    return candidates[0]


def _effort_block_map(
    effort_rows: Sequence[Mapping[str, object]], blocks: Sequence[Mapping[str, object]]
) -> dict[str, str]:
    out: dict[str, str] = {}
    for row in effort_rows:
        start = _parse_dt(_text(row, "start_time"), label=f"effort_id={_text(row, 'effort_id')!r} start_time")
        end = _parse_dt(_text(row, "end_time"), label=f"effort_id={_text(row, 'effort_id')!r} end_time")
        block_id = _match_block_at_time(row, start, blocks, label=f"effort_id={_text(row, 'effort_id')!r}")
        block = next(block for block in blocks if _text(block, "block_id") == block_id)
        _, block_end = _block_window(block)
        if end > block_end:
            raise ValueError(f"effort_id={_text(row, 'effort_id')!r} crosses transition-block boundary")
        out[_text(row, "effort_id")] = block_id
    return out


def _svd_block_map(svd_rows: Sequence[Mapping[str, object]], blocks: Sequence[Mapping[str, object]]) -> dict[str, str]:
    out: dict[str, str] = {}
    for row in svd_rows:
        when = _parse_dt(_text(row, "bag_off_time"), label=f"svd_id={_text(row, 'svd_id')!r} bag_off_time")
        out[_text(row, "svd_id")] = _match_block_at_time(row, when, blocks, label=f"svd_id={_text(row, 'svd_id')!r}")
    return out


def _treatment_block_map(
    treatment_rows: Sequence[Mapping[str, object]], blocks: Sequence[Mapping[str, object]]
) -> dict[str, str]:
    out: dict[str, str] = {}
    for row in treatment_rows:
        when = _parse_dt(_text(row, "assigned_at"), label=f"treatment_id={_text(row, 'treatment_id')!r} assigned_at")
        out[_text(row, "treatment_id")] = _match_block_at_time(
            row, when, blocks, label=f"treatment_id={_text(row, 'treatment_id')!r}"
        )
    return out


def _geometry_by_plant(
    geometry_rows: Sequence[Mapping[str, object]], blocks: Sequence[Mapping[str, object]]
) -> dict[tuple[str, str], list[Mapping[str, object]]]:
    out: dict[tuple[str, str], list[Mapping[str, object]]] = defaultdict(list)
    for row in geometry_rows:
        signature = _row_signature(row)
        matching = [block for block in blocks if _block_signature(block) == signature]
        if not matching:
            continue
        measurement_date = date.fromisoformat(_text(row, "measurement_date"))
        for block in matching:
            start, end = _block_window(block)
            if measurement_date <= end.date():
                out[(_text(block, "block_id"), _text(row, "plant_id"))].append(row)
    return out


def _duration_flower_hours(row: Mapping[str, object]) -> float:
    start = _parse_dt(_text(row, "start_time"), label="effort start")
    end = _parse_dt(_text(row, "end_time"), label="effort end")
    return (end - start).total_seconds() / 3600.0 * float(_text(row, "monitored_open_flower_count"))


def _visitor_key(row: Mapping[str, object]) -> str:
    taxon = _text(row, "visitor_taxon_id")
    return f"taxon:{taxon}" if taxon else f"group:{_text(row, 'visitor_group')}"


def _block_exposure_rows(
    blocks: Sequence[Mapping[str, object]],
    effort_rows: Sequence[Mapping[str, object]],
    visit_rows: Sequence[Mapping[str, object]],
    svd_rows: Sequence[Mapping[str, object]],
    effort_block: Mapping[str, str],
    svd_block: Mapping[str, str],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    visits_by_block: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    for visit in visit_rows:
        block_id = effort_block.get(_text(visit, "effort_id"))
        if block_id:
            visits_by_block[block_id].append(visit)
    efforts_by_block: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    for effort in effort_rows:
        if _text(effort, "usable_observation") == "yes":
            efforts_by_block[effort_block[_text(effort, "effort_id")]].append(effort)
    svd_by_block: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    for row in svd_rows:
        svd_by_block[svd_block[_text(row, "svd_id")]].append(row)

    long_rows: list[dict[str, object]] = []
    summaries: list[dict[str, object]] = []
    for block in blocks:
        block_id = _text(block, "block_id")
        efforts = efforts_by_block.get(block_id, [])
        visits = visits_by_block.get(block_id, [])
        svds = svd_by_block.get(block_id, [])
        flower_hours = sum(_duration_flower_hours(row) for row in efforts)
        group_counts = Counter(_text(row, "visitor_group") for row in visits if _text(row, "visitor_group"))
        visitor_keys = {_visitor_key(row) for row in visits if _text(row, "visitor_group")}
        taxon_keys = {_text(row, "visitor_taxon_id") for row in visits if _text(row, "visitor_taxon_id")}
        controls = [
            int(_text(row, "conspecific_pollen_grains"))
            for row in svds
            if _text(row, "record_type") in NO_VISIT_TYPES
        ]
        background = mean(controls) if controls else None
        singles_by_group: dict[str, list[int]] = defaultdict(list)
        for row in svds:
            if _text(row, "record_type") == "single_visit":
                singles_by_group[_text(row, "visitor_group")].append(int(_text(row, "conspecific_pollen_grains")))

        effective_values: dict[str, float] = {}
        for group in sorted(set(group_counts) | set(singles_by_group)):
            visit_count = group_counts.get(group, 0)
            visit_rate = visit_count / flower_hours if flower_hours > 0 else None
            raw_svd = mean(singles_by_group[group]) if singles_by_group.get(group) else None
            adjusted = raw_svd - background if raw_svd is not None and background is not None else None
            effective = visit_rate * adjusted if visit_rate is not None and adjusted is not None else None
            if effective is not None:
                effective_values[group] = effective
            long_rows.append({
                "block_id": block_id,
                "visitor_group": group,
                "monitored_flower_hours": flower_hours,
                "visit_bouts": visit_count,
                "visit_rate_per_flower_hour": visit_rate,
                "mean_raw_svd": raw_svd,
                "mean_no_visit_background": background,
                "background_adjusted_svd": adjusted,
                "effective_pollen_delivery_per_flower_hour": effective,
                "effective_service_share": None,
            })
        total_effective = sum(effective_values.values()) if effective_values else None
        shares_allowed = bool(effective_values) and total_effective is not None and total_effective > 0 and all(
            value >= 0 for value in effective_values.values()
        )
        if shares_allowed:
            for row in long_rows:
                if row["block_id"] == block_id and row["visitor_group"] in effective_values:
                    row["effective_service_share"] = effective_values[str(row["visitor_group"])] / total_effective
        summaries.append({
            "block_id": block_id,
            "population_id": _text(block, "population_id"),
            "island_id": _text(block, "island_id"),
            "site_id": _text(block, "site_id"),
            "usable_effort_windows": len(efforts),
            "monitored_flower_hours": flower_hours,
            "visit_bouts": len(visits),
            "observed_visitor_key_richness": len(visitor_keys),
            "taxon_resolved_richness": len(taxon_keys),
            "visitor_group_richness": len(group_counts),
            "controlled_effective_group_count": sum(
                1 for group in group_counts if group in singles_by_group and background is not None
            ),
            "zero_visit_block": len(visits) == 0,
            "effective_service_composition_ready": shares_allowed,
        })
    return long_rows, summaries


def build_audit(
    blocks: Sequence[Mapping[str, object]],
    plants: Sequence[Mapping[str, object]],
    geometry: Sequence[Mapping[str, object]],
    effort: Sequence[Mapping[str, object]],
    visits: Sequence[Mapping[str, object]],
    svd: Sequence[Mapping[str, object]],
    treatments: Sequence[Mapping[str, object]],
    fruits: Sequence[Mapping[str, object]],
) -> dict[str, object]:
    # Reuse the existing validators before applying stricter same-block rules.
    audit_field_contacts(effort, visits)
    audit_effective_pollinator_dependency(plants, effort, visits, svd, treatments, fruit_rows=fruits)

    plant_registry = {_text(row, "plant_id"): row for row in plants}
    block_by_id = {_text(row, "block_id"): row for row in blocks}
    effort_block = _effort_block_map(effort, blocks)
    svd_block = _svd_block_map(svd, blocks)
    treatment_block = _treatment_block_map(treatments, blocks)
    geometry_map = _geometry_by_plant(geometry, blocks)
    fruit_by_id = {_text(row, "fruit_id"): row for row in fruits}

    # Every block must match the registered population/site/taxon signature of plants used in it.
    for block in blocks:
        if _text(block, "predeclared_before_outcomes") != "yes":
            continue
        for plant in plants:
            if _text(plant, "population_id") != _text(block, "population_id"):
                continue
            for field in ("field_event_id", "island_id", "site_id", "taxon"):
                if _text(plant, field) != _text(block, field):
                    raise ValueError(f"block_id={_text(block, 'block_id')!r} and plant_id={_text(plant, 'plant_id')!r} disagree on {field}")

    efforts_by_key: dict[tuple[str, str], list[Mapping[str, object]]] = defaultdict(list)
    for row in effort:
        plant_id = _text(row, "plant_id")
        if plant_id and _text(row, "usable_observation") == "yes":
            efforts_by_key[(effort_block[_text(row, "effort_id")], plant_id)].append(row)
    svd_by_key: dict[tuple[str, str], list[Mapping[str, object]]] = defaultdict(list)
    for row in svd:
        svd_by_key[(svd_block[_text(row, "svd_id")], _text(row, "plant_id"))].append(row)
    treatments_by_key: dict[tuple[str, str], list[Mapping[str, object]]] = defaultdict(list)
    for row in treatments:
        treatments_by_key[(treatment_block[_text(row, "treatment_id")], _text(row, "plant_id"))].append(row)

    plant_rows: list[dict[str, object]] = []
    for block in blocks:
        block_id = _text(block, "block_id")
        for plant_id, plant in plant_registry.items():
            if _text(plant, "population_id") != _text(block, "population_id"):
                continue
            key = (block_id, plant_id)
            effort_rows = efforts_by_key.get(key, [])
            svd_rows = svd_by_key.get(key, [])
            treatment_rows = treatments_by_key.get(key, [])
            single_visits = [row for row in svd_rows if _text(row, "record_type") == "single_visit"]
            controls = [row for row in svd_rows if _text(row, "record_type") in NO_VISIT_TYPES]
            treatment_types = {_text(row, "treatment_type") for row in treatment_rows}
            core_present = set(CORE_TREATMENTS).issubset(treatment_types)
            core_rows = [row for row in treatment_rows if _text(row, "treatment_type") in CORE_TREATMENTS]
            terminal = core_present and all(_text(row, "outcome_status") in TERMINAL_ANALYZABLE for row in core_rows)
            seed_link_ok = True
            mature_seed_values: list[int] = []
            for row in core_rows:
                status = _text(row, "outcome_status")
                if status == "aborted":
                    mature_seed_values.append(0)
                    continue
                if status == "mature_fruit":
                    fruit = fruit_by_id.get(_text(row, "fruit_id"))
                    if fruit is None or _text(fruit, "maternal_id") != plant_id:
                        seed_link_ok = False
                        continue
                    try:
                        seeds = int(_text(fruit, "mature_seed_count"))
                    except ValueError:
                        seed_link_ok = False
                        continue
                    if seeds < 0:
                        seed_link_ok = False
                        continue
                    mature_seed_values.append(seeds)
            geometry_ready = bool(geometry_map.get(key))
            predeclared = _text(block, "predeclared_before_outcomes") == "yes"
            full_chain = all((
                predeclared,
                bool(effort_rows),
                bool(single_visits),
                bool(controls),
                core_present,
                terminal,
                seed_link_ok,
                geometry_ready,
            ))
            plant_rows.append({
                "block_id": block_id,
                "plant_id": plant_id,
                "population_id": _text(block, "population_id"),
                "predeclared_block": predeclared,
                "geometry_ready": geometry_ready,
                "usable_effort_windows": len(effort_rows),
                "single_visit_svd_rows": len(single_visits),
                "no_visit_svd_controls": len(controls),
                "core_treatments_present": core_present,
                "core_treatments_terminal": terminal,
                "seed_link_complete": seed_link_ok and terminal,
                "core_treatment_seed_sum": sum(mature_seed_values) if terminal and seed_link_ok else None,
                "full_chain_plant": full_chain,
                "boundary": BOUNDARY,
            })

    exposure_long, block_exposure = _block_exposure_rows(blocks, effort, visits, svd, effort_block, svd_block)
    exposure_by_id = {str(row["block_id"]): row for row in block_exposure}
    block_rows: list[dict[str, object]] = []
    for block_id, block in block_by_id.items():
        plant_subset = [row for row in plant_rows if row["block_id"] == block_id]
        full_count = sum(bool(row["full_chain_plant"]) for row in plant_subset)
        exposure = exposure_by_id[block_id]
        block_rows.append({
            **exposure,
            "block_role": _text(block, "block_role"),
            "predeclared_before_outcomes": _text(block, "predeclared_before_outcomes"),
            "registered_plants": len(plant_subset),
            "full_chain_plants": full_count,
            "full_chain_block": full_count > 0 and _text(block, "predeclared_before_outcomes") == "yes",
            "synthetic_richness_bridge_ready": exposure["usable_effort_windows"] > 0,
            "synthetic_composition_bridge_ready": bool(exposure["effective_service_composition_ready"]),
            "synthetic_starting_state_bridge_ready": any(bool(row["geometry_ready"]) for row in plant_subset),
            "transition_linked_chain_ready": full_count > 0 and bool(exposure["effective_service_composition_ready"]),
            "boundary": BOUNDARY,
        })

    summary = {
        "schema_version": "1.0",
        "analysis": "izu_same_block_transition_linked_chain",
        "status": "field_data_required" if not any(row["transition_linked_chain_ready"] for row in block_rows) else "structurally_observed",
        "strict_unit": "block_id x plant_id",
        "blocks": len(block_rows),
        "plants": len({row["plant_id"] for row in plant_rows}),
        "full_chain_plants": sum(bool(row["full_chain_plant"]) for row in plant_rows),
        "full_chain_blocks": sum(bool(row["full_chain_block"]) for row in block_rows),
        "transition_linked_blocks": sum(bool(row["transition_linked_chain_ready"]) for row in block_rows),
        "synthetic_to_empirical_bridge": {
            "richness": "block observed visitor richness with effort denominator",
            "composition": "block visitor composition and controlled SVD-weighted effective-service composition",
            "starting_state": "same-plant pre-outcome floral geometry",
            "downstream_branch": "same-plant dependency and mature-seed response",
        },
        "boundary": BOUNDARY,
    }
    return {
        "plant_chain_rows": plant_rows,
        "block_chain_rows": block_rows,
        "block_exposure_rows": exposure_long,
        "summary": summary,
    }


def _write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blocks", type=Path, required=True)
    parser.add_argument("--plants", type=Path, required=True)
    parser.add_argument("--geometry", type=Path, required=True)
    parser.add_argument("--effort", type=Path, required=True)
    parser.add_argument("--visits", type=Path, required=True)
    parser.add_argument("--svd", type=Path, required=True)
    parser.add_argument("--treatments", type=Path, required=True)
    parser.add_argument("--fruits", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    try:
        payload = build_audit(
            read_blocks(args.blocks),
            read_dependency_plant_registry(args.plants),
            read_geometry(args.geometry),
            read_effort_manifest(args.effort),
            read_visit_manifest(args.visits),
            read_svd_manifest(args.svd),
            read_pollination_treatments(args.treatments),
            read_fruits(args.fruits),
        )
        args.output_dir.mkdir(parents=True, exist_ok=True)
        _write_csv(args.output_dir / "plant_chain_readiness.csv", payload["plant_chain_rows"])
        _write_csv(args.output_dir / "block_chain_readiness.csv", payload["block_chain_rows"])
        _write_csv(args.output_dir / "block_exposure_by_visitor_group.csv", payload["block_exposure_rows"])
        (args.output_dir / "summary.json").write_text(
            json.dumps(payload["summary"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    except (OSError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
