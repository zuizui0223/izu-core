"""Cross-chapter island empirical bridge is a prospective test, not an observed result."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CONTRACT=ROOT/"data/design/chapter2_island_empirical_mechanism_contract_20261008.json"
CHAPTER2=ROOT/"data/results/chapter2_assurance_generality_20261006.json"
FAILED_DONOR=ROOT/"data/results/chapter2_island_genetic_state_transplant_independent16_20261008.json"
ABLATED=ROOT/"data/results/chapter2_island_assurance_dispersion_ablation_20261008.json"


def test_empirical_contract_is_unfitted_and_has_all_island_evidence_levels():
    c=json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert c["status"]=="prospective_empirical_measurement_contract_no_field_outcomes"
    assert c["current_decision"]=="NOT_READY_FOR_EMPIRICAL_SIGN_TEST"
    assert [x["repository"] for x in c["independent_empirical_resources"]]==[
        "zuizui0223/island","zuizui0223/shimahotarubukuro"]
    assert set(c["islands_with_existing_flower_phenotype"])=={
        "Oshima","Toshima","Niijima","Shikinejima","Kozushima"}
    need=c["new_data_requirements"]
    assert {"visit_effectiveness","mating_and_reproductive_assurance",
            "floral_investment","paternal_component","demography_and_history"}==set(need)
    assert any("paternal" in item.lower() for item in need["paternal_component"])
    assert len(c["minimum_analysis_gates"])>=9


def test_no_synthetic_result_promoted_as_island_field_confirmation():
    c=json.loads(CONTRACT.read_text(encoding="utf-8"))
    established=json.loads(CHAPTER2.read_text(encoding="utf-8"))
    donor=json.loads(FAILED_DONOR.read_text(encoding="utf-8"))
    ablation=json.loads(ABLATED.read_text(encoding="utf-8"))
    assert established["adjudication"]["status"]=="all_four_confirmed"
    assert donor["frozen_primary"]["passed"] is False
    assert ablation["status"].startswith("completed_exploratory")
    assert ablation["independent_visitor_histories"]==4
    assert any("null" in x.lower() or "opposite" in x.lower() 
               for x in c["minimum_analysis_gates"])
    assert "NOT_READY" in c["current_decision"]
