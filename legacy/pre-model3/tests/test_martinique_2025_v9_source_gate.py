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
    assert "do not aggregate event rows" in boundary


def test_core_files_required_optional_metadata_not_required():
    design = json.loads(DESIGN.read_text())
    required = {row["name"] for row in design["author_deposited_files"] if row.get("required")}
    optional = {row["name"] for row in design["author_deposited_files"] if not row.get("required")}
    assert required == {
        "Plant_insect_interactions_former_names.xlsx",
        "Sampling_data.xlsx",
    }
    assert {"README.docx", "Plant_species.xlsx"}.issubset(optional)


def test_source_script_has_no_network_metric_or_v9_import():
    text = SCRIPT.read_text().lower()
    assert "from channel_id.external_archipelago_network" not in text
    assert "network_metrics(" not in text
    assert "interaction_shannon" not in text
    assert "morisita" not in text
    assert "run_constraint_mechanism_abm_v9" not in text


def test_role_detection_finds_explicit_amount_interaction_schema():
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


def test_event_row_interaction_representation_needs_no_amount_column(tmp_path):
    module = load_script()
    from openpyxl import Workbook

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Insects_Plants"
    sheet.append(["Period", "Date", "Site", "Plant_Best_ID", "Insect_Best_ID", "H_start", "H_end"])
    sheet.append(["P1", "2022-10-01", "S1", "PL1", "IN1", "09:00", "09:05"])
    path = tmp_path / "events.xlsx"
    workbook.save(path)
    inspection = module.inspect_workbook(path.read_bytes(), "events.xlsx")
    candidate = inspection["sheets"][0]
    assert candidate["repeated_interaction_candidate"] is True
    assert candidate["interaction_representation"] == "event_rows"


def test_optional_transport_failure_does_not_block_required_bytes():
    module = load_script()
    design_sources = [
        {"name": "core1.xlsx", "required": True},
        {"name": "core2.xlsx", "required": True},
        {"name": "readme.docx", "required": False},
    ]
    records = [
        {"name": "core1.xlsx", "http_status": 200, "bytes": 10},
        {"name": "core2.xlsx", "http_status": 200, "bytes": 11},
        {"name": "readme.docx", "http_status": 404},
    ]
    result = module.transport_summary(design_sources, records)
    assert result["required_source_bytes_ok"] is True
    assert result["all_source_bytes_ok"] is False
    assert result["blocked_required_files"] == []
    assert result["blocked_optional_files"] == ["readme.docx"]


def test_primary_download_endpoints_are_frozen():
    design = json.loads(DESIGN.read_text())
    rows = {row["name"]: row["url"] for row in design["author_deposited_files"]}
    assert rows["Plant_insect_interactions_former_names.xlsx"].endswith("file=597")
    assert rows["README.docx"].endswith("file=599")
    assert rows["Sampling_data.xlsx"].endswith("file=601")
