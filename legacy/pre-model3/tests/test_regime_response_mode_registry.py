import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "predictive_meta" / "regime_response_mode_registry.csv"


def rows():
    with REGISTRY.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_response_modes_keep_quantitative_calibration_and_context_separate():
    records = rows()
    campanula = [row for row in records if row["source_id"] == "campanula_source_locked"]
    goodyera = [row for row in records if row["source_id"] == "goodyera_suetsugu_2024"]
    assert {row["response_mode"] for row in campanula} == {
        "within_lineage_cline", "second_transition_step"
    }
    assert {row["primary_synthesis_role"] for row in campanula} == {"calibration"}
    assert {row["response_mode"] for row in goodyera} == {
        "hybrid_replacement", "interaction_rewiring", "no_reported_regional_shift"
    }
    assert all(row["primary_synthesis_role"] in {"mechanism_context", "dependency_control"} for row in goodyera)


def test_hybrid_replacement_is_not_mislabeled_as_within_lineage_evolution():
    records = {row["response_id"]: row for row in rows()}
    boundary = records["R04"]["claim_boundary"]
    assert "hybrid" in boundary
    assert "same-lineage floral effect" in boundary
    assert any(token in boundary for token in ("cannot", "not"))
    assert "not an equivalence test" in records["R06"]["claim_boundary"]


def test_occupancy_is_not_silently_added_to_trait_modes():
    assert all(row["response_domain"] != "occupancy" for row in rows())
