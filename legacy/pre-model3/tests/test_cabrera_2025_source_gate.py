from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v8_cabrera_source_gate_v1.json"
SCRIPT = ROOT / "scripts/acquire_audit_cabrera_2025_source.py"


def load_source_gate():
    spec = importlib.util.spec_from_file_location("cabrera_source_gate_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_cabrera_source_gate_freezes_dataset_and_repeated_context_scope():
    design = json.loads(DESIGN.read_text())
    candidate = design["candidate_system"]
    assert candidate["article_doi"] == "10.1111/2041-210X.70165"
    assert candidate["zenodo_doi"] == "10.5281/zenodo.17130777"
    assert "six study sites" in candidate["published_scope"]
    assert "13 field campaigns" in candidate["published_scope"]
    assert design["target_metrics_calculated"] is False


def test_source_gate_prohibits_outcome_based_method_or_context_selection():
    design = json.loads(DESIGN.read_text())
    prohibited = " ".join(design["prohibited_before_source_admission"]).lower()
    assert "shannon" in prohibited
    assert "plant niche overlap" in prohibited
    assert "support estimands" in prohibited
    assert "select observation method" in prohibited
    assert "drop sites" in prohibited
    assert "pool repeated contexts" in prohibited
    assert "menorca" in prohibited and "giannutri" in prohibited


def test_source_audit_does_not_import_network_target_layer():
    text = SCRIPT.read_text().lower()
    assert "from channel_id.external_archipelago_network" not in text
    assert "network_metrics(" not in text
    assert "morisita_horn_similarity(" not in text
    assert "effective_number(" not in text


def test_generic_role_detection_requires_pair_entities_and_repeated_context():
    module = load_source_gate()
    roles = module.role_candidates([
        "site",
        "campaign",
        "method",
        "plant_species",
        "pollinator_group",
        "n_visits",
    ])
    assert roles["site_context"] == ["site"]
    assert roles["time_context"] == ["campaign"]
    assert roles["method_context"] == ["method"]
    assert roles["plant"] == ["plant_species"]
    assert roles["pollinator"] == ["pollinator_group"]
    assert roles["interaction_amount"] == ["n_visits"]


def test_source_native_cabrera_roles_follow_readme_definitions():
    module = load_source_gate()
    roles = module.role_candidates([
        "visita",
        "censo",
        "COMMUNITY",
        "habitat",
        "Plant sp",
        "Pollinator",
        "N ind",
        "N visit flowers",
        "Method",
    ])
    assert "COMMUNITY" in roles["site_context"]
    assert "habitat" in roles["site_context"]
    assert "visita" in roles["time_context"]
    assert "censo" in roles["time_context"]
    assert roles["plant"] == ["Plant sp"]
    assert roles["pollinator"] == ["Pollinator"]
    assert roles["interaction_amount"] == ["N ind", "N visit flowers"]
    assert "visita" not in roles["interaction_amount"]
    assert roles["method_context"] == ["Method"]


def test_readme_event_semantics_is_structural_not_target_calculation():
    module = load_source_gate()
    text = "Each row corresponds to a sampling event (census of pollinator visits to flowering plants)."
    assert module.readme_event_semantics(text) is True
