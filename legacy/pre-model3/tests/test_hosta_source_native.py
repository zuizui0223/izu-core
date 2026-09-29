import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "predictive_meta" / "hosta_yamada_2014_source_native.csv"


def rows():
    with SOURCE.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_hosta_keeps_late_corolla_decline_and_complex_other_traits_separate():
    indexed = {row["evidence_id"]: row for row in rows()}
    assert "southern Izu Islands" in indexed["HST01"]["reported_result"]
    assert "complicated" in indexed["HST02"]["reported_result"]
    assert indexed["HST01"]["numeric_status"] == "qualitative_only"
    assert indexed["HST02"]["current_use"] == "falsification_candidate"


def test_hosta_abstract_cannot_be_mapped_to_the_second_boundary():
    indexed = {row["evidence_id"]: row for row in rows()}
    assert "must not be converted" in indexed["HST01"]["blocking_reason"]
    assert indexed["HST04"]["current_use"] == "recovery_gate"


def test_hosta_dependency_class_stays_unresolved_until_pollinator_table_is_transcribed():
    indexed = {row["evidence_id"]: row for row in rows()}
    assert indexed["HST06"]["current_use"] == "dependency_audit"
    assert "remains unresolved" in indexed["HST06"]["blocking_reason"]
