"""Declared flower-length comparability and leverage sets.

This module does not estimate an unreported experiment effect. It only prevents a
singleton experimental context from silently entering a cross-island comparison
as if it were calibrated against the other rows.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Iterable

from channel_id.island_source_level import FlowerLengthObservation, SourceLevelEvidence


COMPARABLE = "within_context_comparable"
SINGLETON = "singleton_context_not_comparable"


@dataclass(frozen=True)
class FlowerLengthMetadata:
    source_id: str
    source_locator: str
    island_id: str
    experiment_id: str
    comparability_status: str
    n: int

    def __post_init__(self) -> None:
        if not all((self.source_id, self.source_locator, self.island_id, self.experiment_id, self.comparability_status)):
            raise ValueError("flower metadata fields cannot be empty")
        if self.n <= 0:
            raise ValueError("flower metadata n must be positive")


@dataclass(frozen=True)
class FlowerLengthSet:
    set_id: str
    description: str
    retained_islands: tuple[str, ...]
    excluded_islands: tuple[str, ...]
    evidence: SourceLevelEvidence


def _map_island(value: str) -> str:
    return {"Kiyosumi": "Honshu", "Nikko": "Honshu"}.get(value.strip(), value.strip())


def load_flower_length_metadata(path: Path) -> tuple[FlowerLengthMetadata, ...]:
    rows: list[FlowerLengthMetadata] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"source_id", "source_locator", "island", "n", "experiment_id", "comparability_status"}
        missing = required - set(reader.fieldnames or ())
        if missing:
            raise ValueError("flower file missing comparability columns: " + ", ".join(sorted(missing)))
        for row in reader:
            rows.append(FlowerLengthMetadata(
                source_id=row["source_id"].strip(),
                source_locator=row["source_locator"].strip(),
                island_id=_map_island(row["island"]),
                experiment_id=row["experiment_id"].strip(),
                comparability_status=row["comparability_status"].strip(),
                n=int(row["n"]),
            ))
    if not rows:
        raise ValueError("flower metadata is empty")
    return tuple(rows)


def _metadata_index(rows: Iterable[FlowerLengthMetadata]) -> dict[tuple[str, str, str], FlowerLengthMetadata]:
    index: dict[tuple[str, str, str], FlowerLengthMetadata] = {}
    for row in rows:
        key = (row.source_id, row.source_locator, row.island_id)
        if key in index:
            raise ValueError(f"duplicate flower metadata key: {key}")
        index[key] = row
    return index


def _select(
    evidence: SourceLevelEvidence,
    metadata: dict[tuple[str, str, str], FlowerLengthMetadata],
    *,
    set_id: str,
    description: str,
    include: callable,
) -> FlowerLengthSet:
    retained: list[FlowerLengthObservation] = []
    excluded: list[str] = []
    for observation in evidence.flower:
        key = (observation.source_id, observation.source_locator, observation.island_id)
        row = metadata.get(key)
        if row is None:
            raise ValueError(f"flower observation lacks comparability metadata: {key}")
        if include(row):
            retained.append(observation)
        else:
            excluded.append(observation.island_id)
    if not retained:
        raise ValueError(f"flower set {set_id!r} retained no rows")
    return FlowerLengthSet(
        set_id=set_id,
        description=description,
        retained_islands=tuple(row.island_id for row in retained),
        excluded_islands=tuple(excluded),
        evidence=replace(evidence, flower=tuple(retained)),
    )


def build_flower_length_sets(evidence: SourceLevelEvidence, flower_path: Path) -> tuple[FlowerLengthSet, ...]:
    """Build preregistered comparability and row-leverage sets.

    The original all-row input is retained for reproducibility. The comparison
    set excludes only rows that cannot be anchored within their stated context.
    """
    metadata = _metadata_index(load_flower_length_metadata(flower_path))
    all_rows = _select(
        evidence, metadata,
        set_id="legacy_all_rows",
        description="Original six-row input; retained for reproducibility only.",
        include=lambda _: True,
    )
    comparable = _select(
        evidence, metadata,
        set_id="within_experiment_comparable",
        description="Rows with an explicit within-context retained comparison; excludes singleton Nikko context.",
        include=lambda row: row.comparability_status == COMPARABLE,
    )
    n_ge_10 = _select(
        evidence, metadata,
        set_id="within_experiment_n_ge_10",
        description="Comparable rows with n >= 10; tests leverage of the Niijima n=2 summary.",
        include=lambda row: row.comparability_status == COMPARABLE and row.n >= 10,
    )
    leave_one: list[FlowerLengthSet] = []
    comparable_rows = [row for row in metadata.values() if row.comparability_status == COMPARABLE]
    for excluded in sorted(comparable_rows, key=lambda row: row.island_id):
        leave_one.append(_select(
            evidence, metadata,
            set_id=f"leave_one_comparable_row_out:{excluded.island_id}",
            description=f"Comparable-context set excluding {excluded.island_id}.",
            include=lambda row, excluded=excluded: row.comparability_status == COMPARABLE and row.island_id != excluded.island_id,
        ))
    return (all_rows, comparable, n_ge_10, *leave_one)
