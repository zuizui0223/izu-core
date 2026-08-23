import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/audit_network_context_mapping_readiness.py"
REGISTRY = ROOT / "data/design/network_context_mapping_candidate_registry.json"
FROZEN = ROOT / "data/results/network_context_mapping_readiness_frozen.json"


def load_script():
    spec = importlib.util.spec_from_file_location("network_context_mapping_readiness_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_frozen_readiness_is_exactly_regenerated_from_registry():
    module = load_script()
    observed = module.audit(json.loads(REGISTRY.read_text(encoding="utf-8")))
    expected = json.loads(FROZEN.read_text(encoding="utf-8"))
    assert observed == expected


def test_no_current_system_is_mapping_ready_and_guaiacum_is_structurally_closest():
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    assert frozen["mapping_ready_count"] == 0
    assert frozen["closest_structural_candidate"] == "puerto_rico_mona_guaiacum"
    assert frozen["closest_missing_gate_count"] == 1
    guaiacum = next(row for row in frozen["rows"] if row["system_id"] == "puerto_rico_mona_guaiacum")
    assert guaiacum["missing_required_gates"] == ["visitor_specific_direct_effectiveness"]
    assert guaiacum["rate_weighted_effective_service_computable"] is False
    assert "search_exhausted" in guaiacum["source_state"]


def test_partial_or_protocol_only_links_never_pass_as_admitted():
    module = load_script()
    assert module.gate_is_admitted("admitted") is True
    for state in (
        "partial_cross_year_cross_paper",
        "admitted_yongxing_only_missing_dong",
        "protocol_ready_no_real_rows",
        "reported_but_primary_artifact_not_recovered",
    ):
        assert module.gate_is_admitted(state) is False


def test_campanula_remains_parallel_not_programme_blocker():
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    row = next(row for row in frozen["rows"] if row["system_id"] == "issue91_campanula_microdonta")
    assert row["network_context_mapping_ready"] is False
    assert row["programme_blocker"] is False
    assert row["n_missing_required_gates"] == 5
