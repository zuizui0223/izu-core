import csv
from pathlib import Path

from channel_id.primary_source_holdout import (
    compile_holdout_observations,
    load_native_evidence,
    summarize,
)

FIELDS = [
    "evidence_id", "source_id", "doi", "taxon", "lineage_id", "analysis_group",
    "group_confidence", "comparison_id", "comparison_units", "trait_id", "trait_family",
    "reported_direction", "numeric_status", "value", "value_unit", "n", "variance",
    "pollinator_regime", "geographic_mapping_status", "source_locator",
    "verification_status", "scoring_status", "claim", "notes",
]


def write_registry(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(rows)


def base_row(**updates: str) -> dict[str, str]:
    row = {
        "evidence_id": "x", "source_id": "source", "doi": "10.1/example", "taxon": "Example",
        "lineage_id": "example", "analysis_group": "specialist", "group_confidence": "high",
        "comparison_id": "comparison", "comparison_units": "two named populations", "trait_id": "tube_length",
        "trait_family": "floral_size", "reported_direction": "decrease", "numeric_status": "qualitative_only",
        "value": "", "value_unit": "", "n": "", "variance": "", "pollinator_regime": "",
        "geographic_mapping_status": "unmapped_source_native", "source_locator": "abstract",
        "verification_status": "publisher_abstract_verified", "scoring_status": "not_scoreable",
        "claim": "Qualitative source-native claim.", "notes": "No numeric table yet.",
    }
    row.update(updates)
    return row


def test_qualitative_registry_rows_are_retained_but_not_emitted(tmp_path: Path):
    registry = tmp_path / "registry.csv"
    write_registry(registry, [base_row()])
    records = load_native_evidence(registry)
    assert summarize(records)["qualitative_rows"] == 1
    assert compile_holdout_observations(records) == ()


def test_only_explicit_mapped_numeric_rows_enter_holdout(tmp_path: Path):
    registry = tmp_path / "registry.csv"
    row = base_row(
        evidence_id="numeric-mainland", numeric_status="numeric_extracted", value="12.5", value_unit="mm",
        n="20", variance="4", pollinator_regime="large_bombus", geographic_mapping_status="mapped_explicit",
        source_locator="Table 2; mainland locality A", verification_status="primary_table_verified",
        scoring_status="ready_for_holdout", notes="Exact source transcription.",
    )
    write_registry(registry, [row])
    records = load_native_evidence(registry)
    emitted = compile_holdout_observations(records)
    assert len(emitted) == 1
    assert emitted[0]["evidence_tier"] == "primary_numeric"
    assert emitted[0]["pollinator_regime"] == "large_bombus"
    assert float(emitted[0]["weight"]) == 5.0


def test_ready_row_rejects_missing_variance(tmp_path: Path):
    registry = tmp_path / "registry.csv"
    row = base_row(
        numeric_status="numeric_extracted", value="12.5", value_unit="mm", n="20",
        pollinator_regime="large_bombus", geographic_mapping_status="mapped_explicit",
        scoring_status="ready_for_holdout",
    )
    write_registry(registry, [row])
    try:
        load_native_evidence(registry)
    except ValueError as error:
        assert "requires n and variance" in str(error)
    else:
        raise AssertionError("missing variance must block holdout compilation")
