import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "predictive_meta" / "goodyera_suetsugu_2024_source_extraction.csv"


def rows():
    with SOURCE.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_source_extraction_locks_numeric_viscidium_contrast_without_holdout_promotion():
    indexed = {row["evidence_id"]: row for row in rows()}
    assert indexed["G01"]["value"] == "3.1"
    assert indexed["G01"]["sd"] == "0.3"
    assert indexed["G01"]["n"] == "60"
    assert indexed["G02"]["value"] == "2.2"
    assert indexed["G02"]["sd"] == "0.2"
    assert indexed["G02"]["n"] == "56"
    assert indexed["G01"]["holdout_eligibility"] == "excluded_context"
    assert indexed["G02"]["holdout_eligibility"] == "excluded_context"


def test_matched_similis_control_stays_qualitative_not_equivalence():
    indexed = {row["evidence_id"]: row for row in rows()}
    control = indexed["G05"]
    assert control["comparison_role"] == "dependency_control"
    assert control["holdout_eligibility"] == "qualitative_control"
    assert control["value"] == ""
    assert "not statistical equivalence" in control["reason"]


def test_hybrid_replacement_and_rewiring_are_kept_separate():
    indexed = {row["evidence_id"]: row for row in rows()}
    assert indexed["G04"]["comparison_role"] == "interaction_rewiring"
    assert indexed["G06"]["trait_id"] == "hybrid_classification"
    assert indexed["G06"]["n"] == "42"
    assert indexed["G07"]["trait_id"] == "migration_rate"
    assert indexed["G07"]["value"] == "0.091"
