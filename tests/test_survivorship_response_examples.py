import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "predictive_meta" / "survivorship_response_examples.csv"


def rows():
    with DATA.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_survivorship_examples_include_failure_rewiring_and_generalist_survival():
    records = rows()
    modes = {row["response_mode"] for row in records}
    assert "hybrid_replacement_plus_interaction_rewiring" in modes
    assert "interaction_rewiring_to_small_bee" in modes
    assert "within_lineage_morphology_plus_reproductive_assurance" in modes
    assert "generalist_survival_plus_morphological_change" in modes


def test_goodyera_is_not_forced_into_same_pure_lineage_survivor_analysis():
    row = next(row for row in rows() if row["example_id"] == "SV01")
    assert row["same_pure_lineage_survives"] == "no"
    assert "pure G. henryi was not recovered" in row["island_comparison"]
    assert "does not isolate pollinator causation" in row["claim_boundary"]


def test_calanthe_aristulifera_represents_rewiring_not_disappearance():
    row = next(row for row in rows() if row["example_id"] == "SV02")
    assert row["same_pure_lineage_survives"] == "yes"
    assert row["response_mode"] == "interaction_rewiring_to_small_bee"
    assert "Lasioglossum occidens" in row["island_comparison"]
    assert "does not prove" in row["claim_boundary"]


def test_broader_dependency_survivor_is_not_assumed_morphologically_static():
    row = next(row for row in rows() if row["example_id"] == "SV05")
    assert row["response_mode"] == "generalist_survival_plus_morphological_change"
    assert "does not imply morphological stasis" in row["claim_boundary"]
