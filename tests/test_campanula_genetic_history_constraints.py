import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONSTRAINTS = ROOT / "data" / "design" / "campanula_genetic_history_constraints.csv"


def load_rows():
    with CONSTRAINTS.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_genetic_history_constraints_are_source_locked_and_non_numeric():
    rows = load_rows()
    assert {row["source_id"] for row in rows} == {"inoue_kawahara_1990", "oiki_2001"}
    assert all(row["verification_status"] == "primary_abstract_verified" for row in rows)
    assert all(row["numeric_axis_status"] != "numeric_ready" for row in rows)
    assert all(row["source_locator"] == "primary abstract" for row in rows)


def test_marker_results_are_not_silently_reconciled():
    rows = {row["constraint_id"]: row for row in load_rows()}
    assert "decreased with distance" in rows["allozyme_distance"]["source_native_result"]
    assert "did not correlate" in rows["rapd_distance"]["source_native_result"]
    assert "progressively to southern islands" in rows["allozyme_colonisation"]["source_native_result"]
    assert "Miyake Island" in rows["rapd_colonisation"]["source_native_result"]


def test_order_cline_is_not_allowed_to_become_pollinator_specific_by_label():
    rows = {row["constraint_id"]: row for row in load_rows()}
    consequence = rows["allozyme_colonisation"]["analysis_consequence"]
    assert "Do not interpret a winning island-order cline as pollinator-specific evidence" in consequence
