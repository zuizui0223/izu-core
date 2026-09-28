import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/check_nicotiana_source_artifacts.py"
GATE = ROOT / "data/design/nicotiana_source_artifact_recovery_gate.json"
FROZEN = ROOT / "data/results/nicotiana_source_artifact_recovery_frozen.json"


def load_module():
    spec = importlib.util.spec_from_file_location("nicotiana_source_recovery_test_module", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_gate_keeps_indexed_2007_values_unadmitted_until_source_lock():
    gate = json.loads(GATE.read_text(encoding="utf-8"))
    pending = gate["numeric_values_pending_source_lock"]
    assert pending["status"] == "indexed_full_text_values_known_but_not_formally_admitted"
    assert pending["allens_visits_n"] == 65
    assert pending["annas_visits_n"] == 31
    assert pending["pollen_deposited_percent_stigma_covered"]["allens_mean"] == 8.2
    assert pending["pollen_deposited_percent_stigma_covered"]["annas_mean"] == 24.0
    assert "must not enter" in pending["admission_rule"]


def test_payload_classification_requires_pdf_magic_or_reports_mismatch():
    module = load_module()
    assert module.classify_payload(b"%PDF-1.7\nbody", "application/pdf") == "recovered_pdf"
    assert module.classify_payload(b"<html>paywall</html>", "application/pdf") == "claimed_pdf_but_missing_pdf_magic"
    assert module.classify_payload(b"<html>paywall</html>", "text/html") == "recovered_non_pdf"


def test_gate_does_not_treat_restricted_dissertation_as_recovered_source():
    gate = json.loads(GATE.read_text(encoding="utf-8"))
    backup = gate["backup_context"]
    assert backup["access"] == "restricted_to_current_um_users"
    assert "Do not treat" in backup["rule"]
    assert "restricted dissertation" in backup["rule"]


def test_both_declared_routes_are_frozen_after_non_pdf_results():
    gate = json.loads(GATE.read_text(encoding="utf-8"))
    assert gate["transport_state"] == "all_declared_automated_routes_frozen_no_pdf_bytes_recovered"
    sources = {row["source_id"]: row for row in gate["sources"]}
    source_2004 = sources["schueller_2004_self_pollination"]
    source_2007 = sources["schueller_2007_corolla_selection"]
    assert source_2004["frozen_transport_result"]["state"] == "recovered_non_pdf"
    assert source_2004["frozen_transport_result"]["workflow_run"] == 32629804487
    assert source_2007["frozen_transport_result"]["state"] == "recovered_non_pdf"
    assert source_2007["frozen_transport_result"]["workflow_run"] == 32629642261
    assert source_2004["frozen_transport_result"]["sha256"] == source_2004["previous_transport_attempt"]["sha256"]


def test_fetch_source_reuses_both_frozen_results_without_network(monkeypatch):
    module = load_module()
    gate = json.loads(GATE.read_text(encoding="utf-8"))

    def forbidden_urlopen(*args, **kwargs):
        raise AssertionError("frozen route must not be fetched again")

    monkeypatch.setattr(module.urllib.request, "urlopen", forbidden_urlopen)
    for source in gate["sources"]:
        result = module.fetch_source(source)
        assert result["state"] == "recovered_non_pdf"
        assert result["reused_frozen_result"] is True


def test_frozen_result_records_zero_pdf_recovery_and_no_mapping_admission():
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    summary = frozen["source_recovery_summary"]
    assert frozen["workflow_run"] == 32629804487
    assert frozen["artifact_id"] == 9490703155
    assert summary["stable_pdf_sources_recovered"] == 0
    assert summary["declared_primary_sources"] == 2
    assert summary["formal_2007_effectiveness_values_admitted"] is False
    assert summary["network_context_mapping_ready"] is False
    assert summary["all_declared_automated_routes_frozen"] is True
