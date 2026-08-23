import json
from pathlib import Path

from scripts.audit_buffer_mechanism_abm_admission import assess_candidate


ROOT = Path(__file__).resolve().parents[1]
INTERFACE = ROOT / "data/design/buffer_mechanism_abm_admission_interface.json"
HAWAII = ROOT / "data/design/buffer_candidate_hawaii_autonomous_assurance.json"
FROZEN = ROOT / "data/results/hawaii_autonomous_assurance_abm_admission_frozen.json"
LEDGER = ROOT / "data/design/cross_system_buffer_prediction_ledger.json"


def test_hawaii_exact_taxon_assurance_is_candidate_only_under_common_interface():
    interface = json.loads(INTERFACE.read_text(encoding="utf-8"))
    candidate = json.loads(HAWAII.read_text(encoding="utf-8"))
    generated = assess_candidate(candidate, interface)
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    assert generated == frozen
    assert generated["state"] == "candidate_only_no_abm_admission"
    assert generated["mapping_ready"] is False
    assert generated["empirically_admitted"] is False


def test_prediction_ledger_keeps_mechanisms_nonuniversal_and_distinguishable():
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    rows = {row["mechanism"]: row for row in ledger["candidate_predictions"]}
    assert set(rows) == {
        "autonomous_reproductive_assurance",
        "service_redundancy_or_compensatory_abundance",
        "resource_or_demographic_compensation",
        "colonization_or_establishment_filtering",
        "network_context_or_rewiring",
    }
    assert all(row["universal_mechanism_prediction"] is False for row in rows.values())
    assurance = rows["autonomous_reproductive_assurance"]
    assert "argues_against_universal_assurance_buffer" in assurance["current_case_reading"]["guaiacum"]
    assert "candidate_supported" in assurance["current_case_reading"]["hawaii_lobelioids"]


def test_dominica_failure_is_a_falsification_control_not_rescue_target():
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    falsification = ledger["positive_and_negative_control_cases"]["falsification_reference"]
    assert falsification["system"] == "dominica_heliconia"
    assert falsification["model_rescue_allowed"] is False
