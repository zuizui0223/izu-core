"""Audit how historical visitor-rate tables support pollinator-regime inputs.

The island scenario model uses bounded pollinator-regime indicators as
availability/context inputs. This module prevents a common overstatement: a
zero indicator is not automatically a demonstrated biological absence.

It joins the direct Inoue 1986 positive-rate table to declared observation
hours and to the current island trait indicator table. The audit reports three
different states separately:

* a positive rate was reported;
* effort was recorded but the group was not reported in the rate table;
* the island/unit has no Inoue 1986 effort row.

Only the first is direct positive rate evidence. The second is a non-report
under a named table and effort context, not a proof of absence. The third says
nothing about 1986 detection and must not be backfilled as a zero.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


MODEL_GROUPS = {
    "Bombus diversus": "bombus_diversus",
    "Bombus ardens": "bombus_ardens",
    "Lasioglossum spp.": "halictid_pollinator",
    "Megachilid spp.": "megachilid_pollinator",
}
MODEL_INDICATORS = tuple(dict.fromkeys(MODEL_GROUPS.values()))
ISLAND_ORDER = ("Honshu", "Oshima", "Toshima", "Niijima", "Kozushima", "Miyake", "Hachijo")

AUDIT_COLUMNS = (
    "island_id",
    "model_indicator",
    "model_value",
    "inoue1986_effort_hours",
    "positive_rate_rows",
    "reported_rate_min_per_hour",
    "reported_rate_max_per_hour",
    "source_status",
    "model_indicator_interpretation",
    "source_ids",
    "source_locators",
    "boundary",
)


@dataclass(frozen=True)
class PollinatorRateRow:
    source_id: str
    source_locator: str
    region: str
    locality_or_island: str
    pollinator_group: str
    rate_per_hour: float


@dataclass(frozen=True)
class EffortRow:
    source_id: str
    source_locator: str
    region: str
    island_or_mainland: str
    locality: str
    observation_hours: float


@dataclass(frozen=True)
class AuditRow:
    island_id: str
    model_indicator: str
    model_value: int
    effort_hours: float
    positive_rates: tuple[PollinatorRateRow, ...]
    source_status: str
    interpretation: str


def _text(row: dict[str, str], field: str) -> str:
    return str(row.get(field, "")).strip()


def _parse_float(row: dict[str, str], field: str, path: Path) -> float:
    value = _text(row, field)
    try:
        parsed = float(value)
    except ValueError as error:
        raise ValueError(f"{path}: {field} is not numeric: {value!r}") from error
    if parsed < 0.0:
        raise ValueError(f"{path}: {field} cannot be negative")
    return parsed


def _require_fields(path: Path, fields: Sequence[str], required: Iterable[str]) -> None:
    missing = set(required) - set(fields)
    if missing:
        raise ValueError(f"{path}: missing columns: " + ", ".join(sorted(missing)))


def load_rate_rows(path: Path) -> tuple[PollinatorRateRow, ...]:
    required = {"source_id", "source_locator", "region", "locality_or_island", "pollinator_taxon_or_group", "mean_captured_per_observation_hour"}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _require_fields(path, tuple(reader.fieldnames or ()), required)
        rows: list[PollinatorRateRow] = []
        for raw in reader:
            rate = _parse_float(raw, "mean_captured_per_observation_hour", path)
            if rate <= 0.0:
                continue
            rows.append(PollinatorRateRow(
                source_id=_text(raw, "source_id"),
                source_locator=_text(raw, "source_locator"),
                region=_text(raw, "region"),
                locality_or_island=_text(raw, "locality_or_island"),
                pollinator_group=_text(raw, "pollinator_taxon_or_group"),
                rate_per_hour=rate,
            ))
    return tuple(rows)


def load_effort_rows(path: Path) -> tuple[EffortRow, ...]:
    required = {"source_id", "source_locator", "region", "island_or_mainland", "locality", "observation_hours"}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _require_fields(path, tuple(reader.fieldnames or ()), required)
        rows: list[EffortRow] = []
        for raw in reader:
            hours = _parse_float(raw, "observation_hours", path)
            if hours <= 0.0:
                continue
            rows.append(EffortRow(
                source_id=_text(raw, "source_id"),
                source_locator=_text(raw, "source_locator"),
                region=_text(raw, "region"),
                island_or_mainland=_text(raw, "island_or_mainland"),
                locality=_text(raw, "locality"),
                observation_hours=hours,
            ))
    return tuple(rows)


def load_model_indicators(path: Path) -> dict[str, dict[str, int]]:
    required = {"island_id", *MODEL_INDICATORS}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _require_fields(path, tuple(reader.fieldnames or ()), required)
        result: dict[str, dict[str, int]] = {}
        for raw in reader:
            island_id = _text(raw, "island_id")
            if not island_id:
                raise ValueError(f"{path}: blank island_id")
            if island_id in result:
                raise ValueError(f"{path}: duplicate island_id {island_id!r}")
            values: dict[str, int] = {}
            for indicator in MODEL_INDICATORS:
                value = _text(raw, indicator)
                if value not in {"0", "1"}:
                    raise ValueError(f"{path}: {island_id} {indicator} must be 0 or 1")
                values[indicator] = int(value)
            result[island_id] = values
    return result


def _canonical_rate_unit(row: PollinatorRateRow) -> str | None:
    if row.region == "Mainland":
        return "Honshu"
    if row.region == "Izu" and row.locality_or_island in ISLAND_ORDER:
        return row.locality_or_island
    return None


def _canonical_effort_unit(row: EffortRow) -> str | None:
    if row.region == "Mainland":
        return "Honshu"
    if row.region == "Izu" and row.island_or_mainland in ISLAND_ORDER:
        return row.island_or_mainland
    return None


def build_audit(
    model_indicators: dict[str, dict[str, int]],
    rate_rows: Sequence[PollinatorRateRow],
    effort_rows: Sequence[EffortRow],
) -> tuple[AuditRow, ...]:
    """Compare positive direct rate records with each model indicator.

    The function deliberately never treats an absent rate-row as a captured
    zero. `source_status` records the limited evidence state instead.
    """
    positive: dict[tuple[str, str], list[PollinatorRateRow]] = {}
    for row in rate_rows:
        island = _canonical_rate_unit(row)
        indicator = MODEL_GROUPS.get(row.pollinator_group)
        if island is None or indicator is None:
            continue
        positive.setdefault((island, indicator), []).append(row)

    effort: dict[str, float] = {}
    for row in effort_rows:
        island = _canonical_effort_unit(row)
        if island is not None:
            effort[island] = effort.get(island, 0.0) + row.observation_hours

    audit: list[AuditRow] = []
    for island_id in ISLAND_ORDER:
        if island_id not in model_indicators:
            continue
        for indicator in MODEL_INDICATORS:
            rates = tuple(positive.get((island_id, indicator), ()))
            hours = effort.get(island_id, 0.0)
            model_value = model_indicators[island_id][indicator]
            if rates:
                status = "positive_rate_reported"
                interpretation = (
                    "Direct positive rate evidence supports a presence/context coding. "
                    "It does not measure effective pollination."
                    if model_value == 1
                    else "Direct positive rate evidence conflicts with the current zero model indicator."
                )
            elif hours > 0.0:
                status = "not_reported_in_rate_table_after_recorded_effort"
                interpretation = (
                    "Current zero indicator is a non-report under named observation effort, not a confirmed zero capture or biological absence."
                    if model_value == 0
                    else "Current positive indicator is not supported by a specific positive Inoue 1986 rate row; inspect other declared sources."
                )
            else:
                status = "no_inoue1986_effort_row_for_unit"
                interpretation = (
                    "The current indicator is outside direct Inoue 1986 rate coverage; do not interpret it as an Inoue 1986 non-detection."
                )
            audit.append(AuditRow(
                island_id=island_id,
                model_indicator=indicator,
                model_value=model_value,
                effort_hours=hours,
                positive_rates=rates,
                source_status=status,
                interpretation=interpretation,
            ))
    return tuple(audit)


def audit_as_dicts(rows: Sequence[AuditRow]) -> list[dict[str, str]]:
    boundary = (
        "Positive rate rows are direct availability/context evidence only. Missing rows are not treated as proven absence, zero capture, or pollination ineffectiveness."
    )
    rendered: list[dict[str, str]] = []
    for row in rows:
        rates = [item.rate_per_hour for item in row.positive_rates]
        rendered.append({
            "island_id": row.island_id,
            "model_indicator": row.model_indicator,
            "model_value": str(row.model_value),
            "inoue1986_effort_hours": f"{row.effort_hours:g}",
            "positive_rate_rows": str(len(rates)),
            "reported_rate_min_per_hour": "" if not rates else f"{min(rates):g}",
            "reported_rate_max_per_hour": "" if not rates else f"{max(rates):g}",
            "source_status": row.source_status,
            "model_indicator_interpretation": row.interpretation,
            "source_ids": ";".join(sorted({item.source_id for item in row.positive_rates})),
            "source_locators": ";".join(sorted({item.source_locator for item in row.positive_rates})),
            "boundary": boundary,
        })
    return rendered


def write_audit(output_csv: Path, output_md: Path, rows: Sequence[AuditRow]) -> None:
    rendered = audit_as_dicts(rows)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=AUDIT_COLUMNS)
        writer.writeheader()
        writer.writerows(rendered)

    direct = [row for row in rendered if row["source_status"] == "positive_rate_reported"]
    nonreports = [row for row in rendered if row["source_status"] == "not_reported_in_rate_table_after_recorded_effort"]
    uncovered = [row for row in rendered if row["source_status"] == "no_inoue1986_effort_row_for_unit"]
    lines = [
        "# Pollinator regime evidence audit",
        "",
        "This audit checks the semantics of the model's pollinator-regime indicators against direct Inoue 1986 positive visitor-rate rows and declared observation effort.",
        "",
        f"Direct positive rate rows supporting an indicator: {len(direct)}",
        f"No positive row reported despite named effort: {len(nonreports)}",
        f"No Inoue 1986 effort coverage for the unit: {len(uncovered)}",
        "",
        "## Interpretation rule",
        "",
        "A positive rate is direct availability/context evidence. A group missing from the positive-rate table after recorded effort is a non-report, not proof of zero capture, local absence, or ineffective pollination. A unit with no effort row has no Inoue 1986 non-detection information at all.",
        "",
        "## Current input audit",
        "",
        "| island | model indicator | model value | effort h | positive rates | source status |",
        "|---|---|---:|---:|---:|---|",
    ]
    for row in rendered:
        lines.append(
            f"| {row['island_id']} | {row['model_indicator']} | {row['model_value']} | "
            f"{row['inoue1986_effort_hours']} | {row['positive_rate_rows']} | {row['source_status']} |"
        )
    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
