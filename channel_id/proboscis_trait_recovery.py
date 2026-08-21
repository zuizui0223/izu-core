"""Validation helpers for the Izu pollinator proboscis-length recovery gate."""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ALLOWED_TRAIT_STATUS = {
    "source_exact_site",
    "source_transfer_prespecified",
    "measured_new",
    "trait_missing",
}


def load_status(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_recovery_status(status: dict[str, object]) -> None:
    current = status["current_trait_coverage"]
    source = status["source_reference"]
    artifact = status["current_2024_reference_artifact"]

    if int(current["current_named_pollinator_taxa"]) != int(artifact["unique_named_pollinator_taxa"]):
        raise ValueError("current named-taxon count must match frozen 2024 artifact inventory")
    recovered = int(current["exact_source_native_numeric_proboscis_mm_recovered"])
    total = int(current["current_named_pollinator_taxa"])
    if not 0 <= recovered <= total:
        raise ValueError("recovered trait count must be inside [0,total]")
    expected_coverage = recovered / total if total else 0.0
    if not math.isclose(float(current["coverage_fraction"]), expected_coverage, abs_tol=1e-12):
        raise ValueError("coverage fraction does not match recovered/total")
    discrepancy = int(source["paper_reported_pollinator_species"]) - total
    if int(current["paper_species_count_minus_current_named_taxa"]) != discrepancy:
        raise ValueError("paper/current species-count discrepancy is inconsistent")
    if recovered == 0 and bool(current["fdq_reconstruction_from_current_repo_trait_values_ready"]):
        raise ValueError("FDQ cannot be trait-ready with zero recovered numeric traits")


def validate_trait_lookup(path: Path) -> dict[str, int]:
    """Validate an eventual visitor-trait lookup without filling missing traits.

    Numeric proboscis length is required only for admitted numeric statuses. Missing
    rows must remain explicitly missing and may not carry a hidden numeric value.
    """
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    counts = {status: 0 for status in sorted(ALLOWED_TRAIT_STATUS)}
    for index, row in enumerate(rows, start=2):
        status = (row.get("trait_status") or "").strip()
        if status not in ALLOWED_TRAIT_STATUS:
            raise ValueError(f"row {index}: unknown trait_status {status!r}")
        counts[status] += 1
        value = (row.get("proboscis_length_mm") or "").strip()
        n = (row.get("measurement_n") or "").strip()
        source = (row.get("measurement_source") or "").strip()
        locator = (row.get("source_locator") or "").strip()
        if status == "trait_missing":
            if value:
                raise ValueError(f"row {index}: trait_missing row cannot carry a numeric value")
            continue
        if not value:
            raise ValueError(f"row {index}: admitted numeric trait requires proboscis_length_mm")
        try:
            numeric = float(value)
        except ValueError as exc:
            raise ValueError(f"row {index}: invalid proboscis_length_mm") from exc
        if not numeric > 0:
            raise ValueError(f"row {index}: proboscis length must be positive")
        if not source or not locator:
            raise ValueError(f"row {index}: admitted numeric trait requires source and locator")
        if status in {"source_exact_site", "measured_new"} and not n:
            raise ValueError(f"row {index}: exact/measured trait requires measurement_n")
    return counts


def recovery_state(status: dict[str, object]) -> dict[str, object]:
    validate_recovery_status(status)
    current = status["current_trait_coverage"]
    retrieval = status["retrieval_state"]
    return {
        "current_named_pollinator_taxa": current["current_named_pollinator_taxa"],
        "recovered_numeric_proboscis_taxa": current["exact_source_native_numeric_proboscis_mm_recovered"],
        "coverage_fraction": current["coverage_fraction"],
        "paper_vs_current_count_discrepancy": current["paper_species_count_minus_current_named_taxa"],
        "table_s2_values_recovered": retrieval["supplementary_table_s2_numeric_values_recovered"],
        "fdq_trait_lookup_ready": current["fdq_reconstruction_from_current_repo_trait_values_ready"],
        "decision": (
            "ready_for_exact_trait_join"
            if current["fdq_reconstruction_from_current_repo_trait_values_ready"]
            else "blocked_until_source_native_proboscis_values_recovered"
        ),
    }
