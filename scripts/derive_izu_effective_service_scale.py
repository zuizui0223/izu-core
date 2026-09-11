#!/usr/bin/env python3
"""Derive field effective-service scale coordinates for the Chapter 2 E4 bridge.

This consumes ``block_exposure_by_visitor_group.csv`` from
``audit_izu_transition_linked_chain.py``.  It deliberately does not equate raw
visitor richness, or the derived effective number of service groups, with the
synthetic system-size parameter k.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Mapping, Sequence


REQUIRED_COLUMNS = (
    "block_id",
    "visitor_group",
    "effective_pollen_delivery_per_flower_hour",
)


def _require_columns(fieldnames: Iterable[str], required: Sequence[str]) -> None:
    missing = set(required) - set(fieldnames)
    if missing:
        raise ValueError("block exposure file missing columns: " + ", ".join(sorted(missing)))


def read_exposure(path: Path) -> tuple[dict[str, str], ...]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _require_columns(reader.fieldnames or (), REQUIRED_COLUMNS)
        return tuple(reader)


def _parse_optional_float(value: object) -> float | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError as exc:
        raise ValueError(f"expected numeric effective service, got {text!r}") from exc


def derive_block_scales(rows: Sequence[Mapping[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        block_id = str(row.get("block_id", "") or "").strip()
        if not block_id:
            raise ValueError("blank block_id in block exposure file")
        grouped[block_id].append(row)

    outputs: list[dict[str, object]] = []
    for block_id in sorted(grouped):
        block_rows = grouped[block_id]
        parsed = [
            _parse_optional_float(row.get("effective_pollen_delivery_per_flower_hour"))
            for row in block_rows
        ]
        complete = bool(parsed) and all(value is not None for value in parsed)
        values = [float(value) for value in parsed if value is not None]
        nonnegative = complete and all(value >= 0 for value in values)
        total = sum(values) if complete else None
        ready = bool(nonnegative and total is not None and total > 0)

        if ready:
            shares = [value / total for value in values]
            hill_q2 = 1.0 / sum(share * share for share in shares)
            group_count = len(values)
            evenness_q2 = hill_q2 / group_count if group_count > 0 else None
            max_share = max(shares)
        else:
            group_count = len(values) if complete else 0
            hill_q2 = None
            evenness_q2 = None
            max_share = None

        outputs.append({
            "block_id": block_id,
            "effective_service_scale_ready": ready,
            "controlled_effective_group_count": group_count,
            "total_effective_pollen_delivery_per_flower_hour": total if ready else None,
            "effective_service_hill_q2": hill_q2,
            "effective_service_evenness_q2": evenness_q2,
            "max_effective_service_share": max_share,
            "mapping_boundary": (
                "service Hill q2 is a field service-breadth coordinate, not synthetic k; "
                "no numerical k crossover is transferred to field data"
            ),
        })
    return outputs


def write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
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
    parser.add_argument("--block-exposure", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    try:
        write_csv(args.output, derive_block_scales(read_exposure(args.block_exposure)))
    except (OSError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
