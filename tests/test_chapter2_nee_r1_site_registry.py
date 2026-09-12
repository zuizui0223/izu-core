from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_chapter2_nee_r1_site_registry.py"
TEMPLATE = ROOT / "templates" / "chapter2_nee_r1_site_registry_template.csv"
CANDIDATES = ROOT / "data" / "design" / "chapter2_nee_r1_site_registry_candidates_20260913.csv"
PRIORITY = ROOT / "data" / "design" / "chapter2_nee_r1b_candidate_priority_lock_20260913.json"

spec = importlib.util.spec_from_file_location("r1audit", SCRIPT)
assert spec and spec.loader
r1audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r1audit)


def _base(context: str, block: int) -> dict[str, str]:
    taxon = "Campanula microdonta" if context == "focal" else "Farfugium japonicum"
    return {
        "context_id": context,
        "taxon": taxon,
        "geographic_unit": "test-region",
        "population_site_id": f"site-{context}",
        "site_name": f"Test {context}",
        "evidence_source": "https://example.org/source",
        "evidence_basis": "pre-outcome occurrence and feasibility source",
        "planned_block_id": f"{context}-b{block:02d}",
        "planned_start_date": "2027-06-01" if context == "focal" else "2027-11-01",
        "planned_end_date": "2027-06-02" if context == "focal" else "2027-11-02",
        "eligible_flowering_plants_screen": "20",
        "block_independence_basis": "predeclared non-overlapping site-time exposure opportunity",
        "independence_review_status": "pass",
        "svd_background_feasible": "true",
        "open_pollination_feasible": "true",
        "bagged_autonomous_feasible": "true",
        "supplemental_outcross_feasible": "true",
        "dependence_coordinate_feasible": "true",
        "access_status": "confirmed",
        "permit_status": "not_required",
        "phenology_status": "confirmed",
        "outcome_blind_exclusion_reason": "",
        "admission_status": "admitted",
    }


def _write(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=r1audit.REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def test_template_matches_audit_schema() -> None:
    with TEMPLATE.open(newline="", encoding="utf-8") as handle:
        columns = next(csv.reader(handle))
    assert columns == r1audit.REQUIRED_COLUMNS


def test_valid_structural_registry_passes_r1b_screen(tmp_path: Path) -> None:
    rows = [_base("focal", i) for i in range(1, 33)]
    rows.append(_base("transport", 1))
    path = tmp_path / "registry.csv"
    _write(path, rows)
    result = r1audit.audit(path)
    assert result["status"] == "R1B_READY_FOR_R2"
    assert result["admitted_focal_blocks"] == 32
    assert result["admitted_transport_blocks"] == 1
    assert result["h5_r1_screen_pass"] is True
    assert result["h5_r1_screen_is_empirical_power"] is False


def test_fewer_than_32_focal_blocks_is_not_ready_not_power_failure(tmp_path: Path) -> None:
    rows = [_base("focal", i) for i in range(1, 32)]
    rows.append(_base("transport", 1))
    path = tmp_path / "registry.csv"
    _write(path, rows)
    result = r1audit.audit(path)
    assert result["status"] == "NOT_READY"
    assert result["scope_complete"] is True
    assert result["h5_r1_screen_pass"] is False
    assert "not empirical power" in result["claim_boundary"]


def test_candidate_can_preserve_pending_field_feasibility_without_schema_error(tmp_path: Path) -> None:
    row = _base("focal", 1)
    row.update(
        {
            "planned_start_date": "pending",
            "planned_end_date": "pending",
            "eligible_flowering_plants_screen": "pending",
            "independence_review_status": "review",
            "svd_background_feasible": "pending",
            "open_pollination_feasible": "pending",
            "bagged_autonomous_feasible": "pending",
            "supplemental_outcross_feasible": "pending",
            "dependence_coordinate_feasible": "pending",
            "access_status": "pending",
            "permit_status": "pending",
            "phenology_status": "pending",
            "admission_status": "candidate",
        }
    )
    path = tmp_path / "registry.csv"
    _write(path, [row])
    result = r1audit.audit(path)
    assert result["status"] == "NOT_READY"
    assert result["registry_schema_valid"] is True
    assert result["candidate_counts"]["focal"] == 1
    assert result["errors"] == []


def test_source_backed_candidate_registry_is_valid_but_not_admitted() -> None:
    result = r1audit.audit(CANDIDATES)
    assert result["status"] == "NOT_READY"
    assert result["registry_schema_valid"] is True
    assert result["candidate_counts"] == {"focal": 5, "transport": 3}
    assert result["admitted_focal_blocks"] == 0
    assert result["admitted_transport_blocks"] == 0
    assert result["scope_complete"] is False
    assert result["errors"] == []


def test_candidate_priority_is_outcome_blind_and_prefers_kozu_transport() -> None:
    data = json.loads(PRIORITY.read_text(encoding="utf-8"))
    assert data["status"] == "candidate_priority_frozen_before_field_outcomes"
    assert data["focal_Campanula_priority"][0]["geographic_unit"] == "Oshima"
    assert data["transport_Farfugium_priority"][0]["geographic_unit"] == "Kozushima"
    assert "kozu-sainbara-lighthouse" in data["transport_Farfugium_priority"][0]["candidate_ids"]
    assert data["regulatory_triage"]["oshima_senzu_coastal"]["status"] == "high_friction_pending_confirmation"
    forbidden = "\n".join(data["ranking_inputs_forbidden"])
    assert "mature seed" in forbidden
    assert "expected crossover" in forbidden
    assert "not proof of current abundance" in data["claim_boundary"].lower()


def test_admitted_row_fails_closed_when_structural_gate_is_pending(tmp_path: Path) -> None:
    row = _base("focal", 1)
    row["permit_status"] = "pending"
    row["svd_background_feasible"] = "pending"
    path = tmp_path / "registry.csv"
    _write(path, [row])
    result = r1audit.audit(path)
    assert result["status"] == "NOT_READY"
    assert result["admitted_focal_blocks"] == 0
    assert any("admitted row fails" in error and "permit" in error for error in result["errors"])
    assert any("SVD/treatment/dependence feasibility" in error for error in result["errors"])


def test_excluded_row_requires_outcome_blind_reason(tmp_path: Path) -> None:
    row = _base("transport", 1)
    row["admission_status"] = "excluded"
    row["outcome_blind_exclusion_reason"] = ""
    path = tmp_path / "registry.csv"
    _write(path, [row])
    result = r1audit.audit(path)
    assert result["status"] == "NOT_READY"
    assert any("outcome-blind exclusion reason" in error for error in result["errors"])
