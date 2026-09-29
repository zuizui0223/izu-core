import csv
from pathlib import Path

from channel_id.source_native_dependency import load_dependency_evidence, summarize

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "predictive_meta" / "source_native_dependency_registry.csv"

FIELDS = [
    "dependency_id", "source_id", "doi", "taxon", "lineage_id", "geographic_scope",
    "dependency_class", "evidence_basis", "evidence_strength", "within_lineage_regime_test_eligible",
    "analysis_role", "pollinator_evidence", "source_locator", "claim_boundary",
]


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(rows)


def base_row(**updates: str) -> dict[str, str]:
    row = {
        "dependency_id": "P", "source_id": "source", "doi": "10.1/example", "taxon": "Example",
        "lineage_id": "example", "geographic_scope": "mainland and island",
        "dependency_class": "unresolved", "evidence_basis": "visitor_list",
        "evidence_strength": "medium", "within_lineage_regime_test_eligible": "false",
        "analysis_role": "directional_candidate", "pollinator_evidence": "Visitors reported.",
        "source_locator": "Results", "claim_boundary": "Dependency unresolved.",
    }
    row.update(updates)
    return row


def test_current_registry_keeps_bombus_holdout_blocked():
    summary = summarize(load_dependency_evidence(REGISTRY))
    assert summary["source_classified_generalist_lineages"] == ["ligustrum_ovalifolium"]
    assert summary["unresolved_dependency_lineages"] == ["hosta_longipes", "weigela_coraeensis"]
    assert summary["source_classified_bombus_dependent_lineages"] == ["goodyera_henryi_mainland"]
    assert summary["eligible_bombus_dependent_lineages"] == []
    assert summary["independent_bombus_holdout_status"] == "blocked_no_clean_source_resolved_bombus_lineage"
    assert summary["dependency_control_lineages"] == ["goodyera_similis"]


def test_unresolved_dependency_cannot_be_regime_test_eligible(tmp_path: Path):
    path = tmp_path / "dependency.csv"
    write_rows(path, [base_row(within_lineage_regime_test_eligible="true")])
    try:
        load_dependency_evidence(path)
    except ValueError as error:
        assert "unresolved dependency cannot be regime-test eligible" in str(error)
    else:
        raise AssertionError("unresolved dependency must remain blocked")


def test_negative_control_requires_generalist_source_classification(tmp_path: Path):
    path = tmp_path / "dependency.csv"
    write_rows(path, [base_row(analysis_role="negative_control_candidate")])
    try:
        load_dependency_evidence(path)
    except ValueError as error:
        assert "must be source-classified generalist" in str(error)
    else:
        raise AssertionError("negative-control label must not be inferred from unresolved evidence")
