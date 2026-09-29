import csv
from pathlib import Path

import pytest

from scripts.audit_effective_dependency_parentage import audit_parentage, read_parentage


def fruit(fruit_id="F1", site_id="S1", maternal_id="P1"):
    return {
        "fruit_id": fruit_id,
        "site_id": site_id,
        "maternal_id": maternal_id,
        "collection_date": "2026-08-01",
        "mature_seed_count": "10",
        "genotyped_seed_target": "3",
        "genotyped_seed_count": "3",
        "fruit_notes": "",
    }


def parentage(status, paternal_id="", posterior="", qc="pending", seed_id="seed1"):
    return {
        "parentage_id": "PA1",
        "fruit_id": "F1",
        "seed_id": seed_id,
        "site_id": "S1",
        "maternal_id": "P1",
        "paternal_id": paternal_id,
        "parentage_status": status,
        "posterior_probability": posterior,
        "genotype_qc_status": qc,
        "notes": "",
    }


def test_assigned_parentage_can_distinguish_explicit_self_and_outcross_assignments():
    rows = [parentage("assigned", paternal_id="P1", posterior="0.99", qc="pass")]
    report = audit_parentage([fruit()], rows)
    assert report["assigned_parent_identity"]["maternal_parent_assignment"] == 1
    assert report["assigned_parent_identity"]["different_parent_assignment"] == 0
    assert report["realized_selfing_estimable_from_all_seeds"] is False

    row = parentage("assigned", paternal_id="P2", posterior="0.95", qc="pass")
    report = audit_parentage([fruit()], [row])
    assert report["assigned_parent_identity"]["different_parent_assignment"] == 1


def test_unresolved_parentage_is_not_selfing():
    report = audit_parentage([fruit()], [parentage("unresolved", qc="pending")])
    assert report["parentage_status_counts"]["unresolved"] == 1
    assert report["assigned_parent_identity"]["maternal_parent_assignment"] == 0
    assert report["assigned_parent_identity"]["different_parent_assignment"] == 0
    assert "not selfing" in report["claim_boundary"].lower()


def test_parentage_must_link_to_same_fruit_site_and_maternal_identity():
    row = parentage("unresolved", qc="pending")
    row["site_id"] = "S2"
    with pytest.raises(ValueError, match="site_id mismatch"):
        audit_parentage([fruit()], [row])

    row = parentage("unresolved", qc="pending")
    row["maternal_id"] = "P2"
    with pytest.raises(ValueError, match="maternal_id mismatch"):
        audit_parentage([fruit()], [row])


def test_reader_rejects_paternal_assignment_on_unresolved_row(tmp_path: Path):
    path = tmp_path / "parentage.csv"
    fields = list(parentage("unresolved").keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow(parentage("unresolved", paternal_id="P2", qc="pending"))
    with pytest.raises(ValueError, match="cannot carry paternal_id"):
        read_parentage(path)
