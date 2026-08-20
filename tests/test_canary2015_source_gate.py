from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v6_canary_site_source_gate_v1.json"
SCRIPT = ROOT / "scripts/acquire_audit_canary2015_dryad.py"


def load_script():
    spec = importlib.util.spec_from_file_location("canary_source_gate_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_canary_source_gate_freezes_fourteen_site_files_and_no_targets():
    design = json.loads(DESIGN.read_text())
    module = load_script()
    assert design["candidate_system"]["expected_site_network_count"] == 14
    assert len(module.EXPECTED_SITE_FILES) == 14
    assert len(set(module.EXPECTED_SITE_FILES)) == 14
    assert design["target_metrics_calculated"] is False
    prohibited = " ".join(design["prohibited_before_source_admission"]).lower()
    assert "shannon" in prohibited
    assert "niche overlap" in prohibited
    assert "merge the two replicate sites" in prohibited


def test_canary_source_gate_preserves_source_defined_replicates():
    module = load_script()
    expected = {
        "Site3_Fuerteventura1.csv",
        "Site4_Fuerteventura2.csv",
        "Site5_GranCanaria1.csv",
        "Site6_GranCanaria2.csv",
        "Site7_TenerifeSouth1.csv",
        "Site8_TenerifeSouth2.csv",
        "Site9_TenerifeTeno1.csv",
        "Site10_TenerifeTeno2.csv",
        "Site11_Gomera1.csv",
        "Site12_Gomera2.csv",
        "Site13_Hierro1.csv",
        "Site14_Hierro2.csv",
    }
    assert expected.issubset(set(module.EXPECTED_SITE_FILES))


def test_matrix_audit_is_schema_only_and_accepts_nonnegative_numeric_matrix():
    module = load_script()
    payload = b",plant_a,plant_b\npoll_1,1,0\npoll_2,2.5,3\n"
    audit = module.audit_matrix(payload, "toy.csv")
    assert audit["quantitative_nonnegative_schema"] is True
    assert audit["pollinator_rows"] == 2
    assert audit["plant_columns"] == 2
    assert audit["target_metrics_calculated"] is False


def test_source_script_does_not_import_network_metric_implementation():
    text = SCRIPT.read_text()
    assert "channel_id.external_archipelago_network" not in text
    assert "network_metrics(" not in text
