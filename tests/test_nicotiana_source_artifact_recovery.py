import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/check_nicotiana_source_artifacts.py"
GATE = ROOT / "data/design/nicotiana_source_artifact_recovery_gate.json"


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


def test_only_alternate_deepblue_route_is_live_and_springer_is_frozen():
    gate = json.loads(GATE.read_text(encoding="utf-8"))
    sources = {row["source_id"]: row for row in gate["sources"]}
    source_2004 = sources["schueller_2004_self_pollination"]
    source_2007 = sources["schueller_2007_corolla_selection"]
    assert source_2004["retrieval_url"].endswith("/bitstream/2027.42/142032/1/ajb20672.pdf")
    assert source_2004["previous_transport_attempt"]["state"] == "recovered_non_pdf"
    assert source_2007["frozen_transport_result"]["state"] == "recovered_non_pdf"
    assert source_2007["frozen_transport_result"]["reused_frozen_result"] is True


def test_fetch_source_reuses_frozen_result_without_network(monkeypatch):
    module = load_module()
    gate = json.loads(GATE.read_text(encoding="utf-8"))
    source = next(row for row in gate["sources"] if row["source_id"] == "schueller_2007_corolla_selection")

    def forbidden_urlopen(*args, **kwargs):
        raise AssertionError("frozen route must not be fetched again")

    monkeypatch.setattr(module.urllib.request, "urlopen", forbidden_urlopen)
    result = module.fetch_source(source)
    assert result["state"] == "recovered_non_pdf"
    assert result["reused_frozen_result"] is True
