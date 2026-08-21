from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v9_martinique_2025_source_gate_v1.json"
SCRIPT = ROOT / "scripts/acquire_audit_martinique_2025_v9_source.py"


def load_script():
    spec = importlib.util.spec_from_file_location("martinique_v9_source_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_design_is_insect_only_and_target_free():
    design = json.loads(DESIGN.read_text())
    assert "insect interactions only" in design["primary_biological_scope"].lower()
    assert design["target_metrics_calculated"] is False
    boundary = " ".join(design["hard_boundaries"]).lower()
    assert "independently recorded floral-offer" in boundary
    assert "pair-support fraction" in boundary


def test_source_script_has_no_network_metric_or_v9_import():
    text = SCRIPT.read_text().lower()
    assert "from channel_id.external_archipelago_network" not in text
    assert "network_metrics(" not in text
    assert "interaction_shannon" not in text
    assert "morisita" not in text
    assert "run_constraint_mechanism_abm_v9" not in text


def test_role_detection_finds_repeated_interaction_schema():
    module = load_script()
    roles = module.role_candidates(["Site", "Month", "Plant species", "Insect species", "N visits"])
    assert roles["site"] == ["Site"]
    assert roles["time"] == ["Month"]
    assert roles["plant"] == ["Plant species"]
    assert roles["pollinator"] == ["Insect species"]
    assert roles["interaction_amount"] == ["N visits"]


def test_role_detection_separates_independent_floral_offer():
    module = load_script()
    roles = module.role_candidates(["Garden", "Month", "Plant", "Open floral units"])
    assert roles["site"] == ["Garden"]
    assert roles["time"] == ["Month"]
    assert roles["plant"] == ["Plant"]
    assert roles["floral_offer"] == ["Open floral units"]
    assert roles["pollinator"] == []


def test_primary_download_endpoints_are_frozen():
    design = json.loads(DESIGN.read_text())
    rows = {row["name"]: row["url"] for row in design["author_deposited_files"]}
    assert rows["Plant_insect_interactions_former_names.xlsx"].endswith("file=597")
    assert rows["README.docx"].endswith("file=599")
    assert rows["Sampling_data.xlsx"].endswith("file=601")
