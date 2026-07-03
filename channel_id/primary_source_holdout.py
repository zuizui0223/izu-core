"""Compile primary-source floral evidence into prediction-meta holdout rows.

The cross-lineage synthesis needs two evidence layers that must never be
confused:

* **source-native evidence**: a faithfully recorded claim or contrast from an
  original paper, including qualitative statements that cannot yet be scored;
* **prediction-meta observations**: numeric observations with an explicit
  locality-to-regime mapping, suitable for the locked holdout scorer.

This module enforces that separation.  A qualitative abstract statement, a
comparison whose localities cannot be mapped to the declared three-regime
scaffold, or a source with no n/variance extraction can remain valuable in the
source-native registry but cannot become a prediction-test data point.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


NATIVE_FIELDS = (
    "evidence_id", "source_id", "doi", "taxon", "lineage_id", "analysis_group",
    "group_confidence", "comparison_id", "comparison_units", "trait_id", "trait_family",
    "reported_direction", "numeric_status", "value", "value_unit", "n", "variance",
    "pollinator_regime", "geographic_mapping_status", "source_locator",
    "verification_status", "scoring_status", "claim", "notes",
)
OUTPUT_FIELDS = (
    "observation_id", "analysis_partition", "lineage_id", "taxon", "analysis_group",
    "group_confidence", "trait_id", "trait_family", "pollinator_regime", "value",
    "value_unit", "evidence_tier", "source_locator", "review_status", "weight", "notes",
)
VALID_NUMERIC_STATUS = {"not_extracted", "qualitative_only", "numeric_extracted"}
VALID_MAPPING = {"unmapped_source_native", "needs_locality_table", "mapped_explicit"}
VALID_SCORING = {"not_scoreable", "ready_for_holdout", "excluded_comparator"}
VALID_GROUPS = {"specialist", "generalist", "excluded"}


@dataclass(frozen=True)
class NativeEvidence:
    evidence_id: str
    source_id: str
    doi: str
    taxon: str
    lineage_id: str
    analysis_group: str
    group_confidence: str
    comparison_id: str
    comparison_units: str
    trait_id: str
    trait_family: str
    reported_direction: str
    numeric_status: str
    value: float | None
    value_unit: str
    n: float | None
    variance: float | None
    pollinator_regime: str
    geographic_mapping_status: str
    source_locator: str
    verification_status: str
    scoring_status: str
    claim: str
    notes: str


def _clean(value: object) -> str:
    return str(value or "").strip()


def _optional_float(value: object, field: str, evidence_id: str) -> float | None:
    text = _clean(value)
    if not text:
        return None
    try:
        return float(text)
    except ValueError as error:
        raise ValueError(f"{evidence_id}: {field} must be numeric or blank") from error


def _require_columns(rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError("primary-source evidence registry is empty")
    missing = sorted(set(NATIVE_FIELDS).difference(rows[0]))
    if missing:
        raise ValueError("primary-source evidence registry missing columns: " + ", ".join(missing))


def load_native_evidence(path: str | Path) -> tuple[NativeEvidence, ...]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    _require_columns(rows)
    out: list[NativeEvidence] = []
    seen: set[str] = set()
    for row in rows:
        evidence_id = _clean(row["evidence_id"])
        if not evidence_id:
            raise ValueError("evidence_id is required")
        if evidence_id in seen:
            raise ValueError(f"duplicate evidence_id: {evidence_id}")
        seen.add(evidence_id)
        numeric_status = _clean(row["numeric_status"])
        mapping = _clean(row["geographic_mapping_status"])
        scoring = _clean(row["scoring_status"])
        group = _clean(row["analysis_group"])
        if numeric_status not in VALID_NUMERIC_STATUS:
            raise ValueError(f"{evidence_id}: invalid numeric_status")
        if mapping not in VALID_MAPPING:
            raise ValueError(f"{evidence_id}: invalid geographic_mapping_status")
        if scoring not in VALID_SCORING:
            raise ValueError(f"{evidence_id}: invalid scoring_status")
        if group not in VALID_GROUPS:
            raise ValueError(f"{evidence_id}: invalid analysis_group")
        value = _optional_float(row["value"], "value", evidence_id)
        n = _optional_float(row["n"], "n", evidence_id)
        variance = _optional_float(row["variance"], "variance", evidence_id)
        if numeric_status == "numeric_extracted" and value is None:
            raise ValueError(f"{evidence_id}: numeric_extracted requires value")
        if numeric_status != "numeric_extracted" and value is not None:
            raise ValueError(f"{evidence_id}: only numeric_extracted may contain value")
        if scoring == "ready_for_holdout":
            if numeric_status != "numeric_extracted":
                raise ValueError(f"{evidence_id}: ready_for_holdout requires numeric_extracted")
            if mapping != "mapped_explicit":
                raise ValueError(f"{evidence_id}: ready_for_holdout requires mapped_explicit")
            if not _clean(row["pollinator_regime"]):
                raise ValueError(f"{evidence_id}: ready_for_holdout requires pollinator_regime")
            if not _clean(row["value_unit"]):
                raise ValueError(f"{evidence_id}: ready_for_holdout requires value_unit")
            if n is None or variance is None:
                raise ValueError(f"{evidence_id}: ready_for_holdout requires n and variance")
            if n <= 0 or variance < 0:
                raise ValueError(f"{evidence_id}: n must be > 0 and variance >= 0")
        out.append(NativeEvidence(
            evidence_id=evidence_id, source_id=_clean(row["source_id"]), doi=_clean(row["doi"]),
            taxon=_clean(row["taxon"]), lineage_id=_clean(row["lineage_id"]), analysis_group=group,
            group_confidence=_clean(row["group_confidence"]), comparison_id=_clean(row["comparison_id"]),
            comparison_units=_clean(row["comparison_units"]), trait_id=_clean(row["trait_id"]),
            trait_family=_clean(row["trait_family"]), reported_direction=_clean(row["reported_direction"]),
            numeric_status=numeric_status, value=value, value_unit=_clean(row["value_unit"]), n=n,
            variance=variance, pollinator_regime=_clean(row["pollinator_regime"]),
            geographic_mapping_status=mapping, source_locator=_clean(row["source_locator"]),
            verification_status=_clean(row["verification_status"]), scoring_status=scoring,
            claim=_clean(row["claim"]), notes=_clean(row["notes"]),
        ))
    return tuple(out)


def compile_holdout_observations(records: Iterable[NativeEvidence]) -> tuple[dict[str, str], ...]:
    """Emit only scored-eligible numeric evidence in the common holdout schema."""
    rows: list[dict[str, str]] = []
    for record in records:
        if record.scoring_status != "ready_for_holdout":
            continue
        assert record.value is not None and record.n is not None and record.variance is not None
        weight = record.n / (record.variance + 1e-12)
        rows.append({
            "observation_id": record.evidence_id,
            "analysis_partition": "holdout",
            "lineage_id": record.lineage_id,
            "taxon": record.taxon,
            "analysis_group": record.analysis_group,
            "group_confidence": record.group_confidence,
            "trait_id": record.trait_id,
            "trait_family": record.trait_family,
            "pollinator_regime": record.pollinator_regime,
            "value": f"{record.value:.12g}",
            "value_unit": record.value_unit,
            "evidence_tier": "primary_numeric",
            "source_locator": record.source_locator,
            "review_status": "primary_table_transcribed",
            "weight": f"{weight:.12g}",
            "notes": (
                f"source_id={record.source_id}; doi={record.doi}; comparison_id={record.comparison_id}; "
                f"n={record.n:.12g}; variance={record.variance:.12g}; {record.notes}"
            ).strip(),
        })
    return tuple(rows)


def write_holdout_observations(path: str | Path, rows: Iterable[dict[str, str]]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def summarize(records: Iterable[NativeEvidence]) -> dict[str, int]:
    rows = tuple(records)
    return {
        "native_evidence_rows": len(rows),
        "qualitative_rows": sum(row.numeric_status == "qualitative_only" for row in rows),
        "numeric_extracted_rows": sum(row.numeric_status == "numeric_extracted" for row in rows),
        "ready_for_holdout_rows": sum(row.scoring_status == "ready_for_holdout" for row in rows),
        "unmapped_or_incomplete_rows": sum(row.scoring_status == "not_scoreable" for row in rows),
        "excluded_comparator_rows": sum(row.scoring_status == "excluded_comparator" for row in rows),
    }
