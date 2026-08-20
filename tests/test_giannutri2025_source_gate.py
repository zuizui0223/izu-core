from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v6_giannutri_source_gate_v1.json"
SCRIPT = ROOT / "scripts/acquire_audit_giannutri2025_zenodo.py"


def load_script():
    spec = importlib.util.spec_from_file_location("giannutri_source_gate_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_giannutri_gate_locks_zenodo_and_three_bee_scope_before_targets():
    design = json.loads(DESIGN.read_text())
    assert design["candidate_system"]["zenodo_record_id"] == 14855496
    assert design["candidate_system"]["published_daily_network_count"] == 29
    scope = design["candidate_system"]["published_network_scope"]
    assert "Apis mellifera" in scope
    assert "Anthophora dispar" in scope
    assert "Bombus terrestris" in scope
    assert design["target_metrics_calculated"] is False


def test_exact_required_source_files_and_md5s_are_frozen():
    design = json.loads(DESIGN.read_text())
    required = design["required_zenodo_files"]
    assert required == {
        "README.txt": "4e0085f3337078bc7f60bffc2dbfe80e",
        "Code for Resource use and overlap analysis.R": "b1eae37f3cada984dcbe439c75806c39",
        "transect_data_for_overlap_analysis.txt": "1c68690ac94ba90367b9cfb79ce55b38",
        "walking_transects_dataset.txt": "55a95d49383c65c6dd33d079e0478e55",
    }


def test_source_audit_does_not_import_network_metrics():
    text = SCRIPT.read_text()
    assert "network_metrics" not in text
    assert "external_archipelago_network" not in text
    assert "interaction_shannon" not in text
    assert "mean_plant_niche_overlap" not in text


def test_tabular_inventory_only_reports_structure():
    module = load_script()
    payload = b"date\tcondition\tplant\tbee\tvisits\n2025-01-01\tHB+\tp1\tb1\t3\n"
    audit = module.tabular_inventory(payload)
    assert audit["row_count_excluding_header"] == 1
    assert audit["field_role_candidates"]["time"] == ["date"]
    assert audit["field_role_candidates"]["condition"] == ["condition"]
    assert audit["field_role_candidates"]["plant"] == ["plant"]
    assert audit["field_role_candidates"]["visitor"] == ["bee"]
    assert audit["target_metrics_calculated"] is False


def test_post_admission_rules_prohibit_scope_expansion_and_posthoc_pooling():
    design = json.loads(DESIGN.read_text())
    prohibited = " ".join(design["prohibited_before_source_admission"]).lower()
    assert "three-focal-bee" in prohibited
    assert "pool days differently" in prohibited
    assert "predictive envelope" in prohibited
