from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "data/design/abm_v13_hawaii_lobelioid_source_gate.json"
SCRIPT = ROOT / "scripts/recover_abm_v13_hawaii_lobelioid_dryad.py"


def load_recovery():
    spec = importlib.util.spec_from_file_location("abm_v13_hawaii_recovery_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_gate_freezes_source_native_signed_position_without_target_reanalysis():
    gate = json.loads(GATE.read_text(encoding="utf-8"))
    assert gate["v12_mapping"]["signed_position"] == "bill_minus_flower = bird culmen length mm - plant flower length mm"
    assert gate["target_metrics_calculated"] is False
    assert gate["admission_boundary"]["literature_blind_validation"] is False
    assert gate["admission_boundary"]["direct_signed_position_to_service_propagation_test"] is True
    assert gate["v12_mapping"]["reproductive_endpoint_present"] is False


def test_exact_three_dryad_files_and_required_columns_are_frozen():
    recovery = load_recovery()
    assert [row["file_stream_id"] for row in recovery.FILES] == [4858933, 4858934, 4858939]
    assert recovery.FILES[0]["required_columns"][-1] == "bill_minus_flower"
    assert {"N", "pollen_contact", "nectar_robbing", "bill_minus_flower"}.issubset(
        recovery.FILES[1]["required_columns"]
    )


def test_recovery_urls_are_dryad_file_streams():
    recovery = load_recovery()
    assert recovery.source_url(4858933) == "https://datadryad.org/downloads/file_stream/4858933"


def test_csv_schema_rejects_missing_signed_position_column():
    recovery = load_recovery()
    text = "bird_species,culmen,island,assemblage,plant_species,flower_length\na,10,H,historic,p,20\n"
    schema = recovery.csv_schema(text, recovery.FILES[0]["required_columns"])
    assert schema["required_columns_present"] is False
    assert "bill_minus_flower" in schema["missing_required_columns"]
