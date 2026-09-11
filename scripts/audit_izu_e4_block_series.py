#!/usr/bin/env python3
"""Audit prespecified repeated Izu blocks for the Chapter 2 E4 confrontation.

This is an exposure-only structural audit.  It does not inspect dependency or
mature-seed outcomes and therefore cannot choose a crossover after seeing the
response.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Mapping, Sequence


BLOCK_REQUIRED = (
    "block_id",
    "population_id",
    "island_id",
    "site_id",
    "taxon",
    "season_id",
    "predeclared_before_outcomes",
    "realization_series_id",
    "block_sequence",
    "planned_duration_min",
    "e4_scale_role",
)
SCALE_REQUIRED = (
    "block_id",
    "effective_service_scale_ready",
    "complete_effectiveness_coverage",
    "effective_service_hill_q2",
)
E4_ROLES = frozenset({"rank_confrontation", "context_only", "exclude", ""})
TRUE_VALUES = frozenset({"true", "1", "yes"})


def _require_columns(fieldnames: Iterable[str], required: Sequence[str], label: str) -> None:
    missing = set(required) - set(fieldnames)
    if missing:
        raise ValueError(f"{label} missing columns: " + ", ".join(sorted(missing)))


def _read_csv(path: Path, required: Sequence[str], label: str) -> tuple[dict[str, str], ...]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _require_columns(reader.fieldnames or (), required, label)
        return tuple(reader)


def _text(row: Mapping[str, object], key: str) -> str:
    return str(row.get(key, "") or "").strip()


def _as_bool(value: object) -> bool:
    return str(value or "").strip().lower() in TRUE_VALUES


def audit_e4_series(
    blocks: Sequence[Mapping[str, object]],
    scales: Sequence[Mapping[str, object]],
) -> dict[str, object]:
    scale_by_block: dict[str, Mapping[str, object]] = {}
    for row in scales:
        block_id = _text(row, "block_id")
        if not block_id:
            raise ValueError("blank block_id in service-scale file")
        if block_id in scale_by_block:
            raise ValueError(f"duplicate service-scale row for block_id={block_id!r}")
        scale_by_block[block_id] = row

    series: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    block_rows: list[dict[str, object]] = []
    for row in blocks:
        block_id = _text(row, "block_id")
        role = _text(row, "e4_scale_role")
        if role not in E4_ROLES:
            raise ValueError(f"invalid e4_scale_role={role!r} for block_id={block_id!r}")

        if role == "rank_confrontation":
            if _text(row, "predeclared_before_outcomes") != "yes":
                raise ValueError(f"E4 block must be predeclared: block_id={block_id!r}")
            series_id = _text(row, "realization_series_id")
            if not series_id:
                raise ValueError(f"E4 block missing realization_series_id: block_id={block_id!r}")
            try:
                sequence = int(_text(row, "block_sequence"))
            except ValueError as exc:
                raise ValueError(f"invalid block_sequence for block_id={block_id!r}") from exc
            if sequence < 1:
                raise ValueError(f"block_sequence must be positive for block_id={block_id!r}")
            try:
                duration = float(_text(row, "planned_duration_min"))
            except ValueError as exc:
                raise ValueError(f"invalid planned_duration_min for block_id={block_id!r}") from exc
            if duration <= 0:
                raise ValueError(f"planned_duration_min must be positive for block_id={block_id!r}")
            series[series_id].append(row)
        else:
            series_id = _text(row, "realization_series_id")
            sequence = None
            duration = None

        scale = scale_by_block.get(block_id)
        scale_ready = bool(scale and _as_bool(scale.get("effective_service_scale_ready")))
        complete_coverage = bool(scale and _as_bool(scale.get("complete_effectiveness_coverage")))
        hill_q2 = _text(scale or {}, "effective_service_hill_q2") or None
        block_rows.append({
            "block_id": block_id,
            "e4_scale_role": role or "unassigned",
            "realization_series_id": series_id or None,
            "block_sequence": sequence,
            "planned_duration_min": duration,
            "effective_service_scale_ready": scale_ready,
            "complete_effectiveness_coverage": complete_coverage,
            "effective_service_hill_q2": hill_q2,
        })

    series_rows: list[dict[str, object]] = []
    for series_id, members in sorted(series.items()):
        sequences = [int(_text(row, "block_sequence")) for row in members]
        if len(sequences) != len(set(sequences)):
            raise ValueError(f"duplicate block_sequence in realization_series_id={series_id!r}")

        for field in ("population_id", "island_id", "site_id", "taxon", "season_id", "planned_duration_min"):
            values = {_text(row, field) for row in members}
            if len(values) != 1:
                raise ValueError(f"E4 series {series_id!r} mixes {field}: {sorted(values)!r}")

        member_ids = {_text(row, "block_id") for row in members}
        scale_ready_count = sum(
            bool(scale_by_block.get(block_id))
            and _as_bool(scale_by_block[block_id].get("effective_service_scale_ready"))
            and _as_bool(scale_by_block[block_id].get("complete_effectiveness_coverage"))
            for block_id in member_ids
        )
        series_rows.append({
            "realization_series_id": series_id,
            "population_id": _text(members[0], "population_id"),
            "island_id": _text(members[0], "island_id"),
            "site_id": _text(members[0], "site_id"),
            "taxon": _text(members[0], "taxon"),
            "season_id": _text(members[0], "season_id"),
            "planned_duration_min": float(_text(members[0], "planned_duration_min")),
            "rank_confrontation_blocks": len(members),
            "scale_ready_blocks": scale_ready_count,
            "descriptive_stability_ready": len(members) >= 2 and scale_ready_count >= 2,
            "confirmatory_boundary": (
                "two blocks open descriptive dispersion only; confirmatory replication/precision "
                "remain governed by the frozen planning gate"
            ),
        })

    summary = {
        "schema_version": "1.0",
        "analysis": "izu_e4_prespecified_block_series",
        "rank_confrontation_blocks": sum(row["e4_scale_role"] == "rank_confrontation" for row in block_rows),
        "rank_confrontation_series": len(series_rows),
        "descriptive_stability_ready_series": sum(bool(row["descriptive_stability_ready"]) for row in series_rows),
        "outcomes_inspected": false if False else False,
        "boundary": (
            "This audit establishes only exposure-side repeated-block structure. It does not establish "
            "a determinant-rank crossover or transfer the synthetic k threshold to field data."
        ),
    }
    return {"block_rows": block_rows, "series_rows": series_rows, "summary": summary}


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
    parser.add_argument("--service-scale", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    try:
        payload = audit_e4_series(
            _read_csv(args.blocks, BLOCK_REQUIRED, "transition block manifest"),
            _read_csv(args.service_scale, SCALE_REQUIRED, "effective-service scale file"),
        )
        _write_csv(args.output_dir / "e4_block_readiness.csv", payload["block_rows"])
        _write_csv(args.output_dir / "e4_series_readiness.csv", payload["series_rows"])
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "summary.json").write_text(
            json.dumps(payload["summary"], indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    except (OSError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
