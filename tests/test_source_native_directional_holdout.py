import csv
from pathlib import Path

from channel_id.source_native_directional_holdout import (
    load_directional_evidence,
    run_audit,
)

ROOT = Path(__file__).resolve().parents[1]
DIRECTIONAL = ROOT / "data" / "predictive_meta" / "source_native_directional_holdout.csv"
NATIVE = ROOT / "data" / "predictive_meta" / "primary_source_native_evidence.csv"

FIELDS = [
    "directional_id", "source_id", "doi", "taxon", "lineage_id", "analysis_group",
    "dependency_status", "evidence_grade", "response_domain", "source_reported_pattern",
    "boundary_localization", "shared_second_step_evidence", "generalist_change_observed",
    "eligible_for_numeric_holdout", "source_locator", "claim_boundary", "next_required_evidence",
]


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(rows)


def base_row(**updates: str) -> dict[str, str]:
    row = {
        "directional_id": "D", "source_id": "source", "doi": "10.1/example",
        "taxon": "Example", "lineage_id": "example", "analysis_group": "specialist",
        "dependency_status": "resolved", "evidence_grade": "B", "response_domain": "floral_size",
        "source_reported_pattern": "decrease", "boundary_localization": "exact_island_sequence_missing",
        "shared_second_step_evidence": "does_not_demonstrate", "generalist_change_observed": "false",
        "eligible_for_numeric_holdout": "false", "source_locator": "abstract",
        "claim_boundary": "Directional only.", "next_required_evidence": "table",
    }
    row.update(updates)
    return row


def test_current_directional_layer_has_no_independent_shared_step_support():
    report = run_audit(DIRECTIONAL, NATIVE)
    summary = report["summary"]
    assert summary["n_lineages"] == 3
    assert summary["shared_second_step_support_lineages"] == []
    assert summary["universal_shared_second_step_status"] == "not_supported_by_current_directional_layer"
    assert summary["generalist_change_observed_lineages"] == ["ligustrum_ovalifolium"]
    assert summary["unresolved_dependency_lineages"] == ["hosta_longipes"]
    assert summary["numeric_holdout_rows"] == 0


def test_support_requires_explicit_oshima_postboundary_localization(tmp_path: Path):
    registry = tmp_path / "directional.csv"
    write_rows(registry, [base_row(shared_second_step_evidence="supports")])
    try:
        load_directional_evidence(registry)
    except ValueError as error:
        assert "requires explicit Oshima/post-boundary localization" in str(error)
    else:
        raise AssertionError("broad geography must not be promoted to second-step support")


def test_grade_b_can_never_be_numeric_holdout(tmp_path: Path):
    registry = tmp_path / "directional.csv"
    write_rows(registry, [base_row(eligible_for_numeric_holdout="true")])
    try:
        load_directional_evidence(registry)
    except ValueError as error:
        assert "cannot enter numeric holdout" in str(error)
    else:
        raise AssertionError("B-grade directional evidence must remain separate from numeric holdout")


def test_generalist_change_is_allowed_but_only_for_generalists(tmp_path: Path):
    registry = tmp_path / "directional.csv"
    write_rows(registry, [base_row(generalist_change_observed="true")])
    try:
        load_directional_evidence(registry)
    except ValueError as error:
        assert "requires generalist group" in str(error)
    else:
        raise AssertionError("generalist-change flag must not be applied to specialist records")
