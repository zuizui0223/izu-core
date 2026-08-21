from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v9_thousand_island_lake_source_gate_v1.json"
SCRIPT = ROOT / "scripts/acquire_audit_thousand_island_lake_2022.py"


def load_script():
    spec = importlib.util.spec_from_file_location("til_source_gate_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_gate_is_bound_to_author_deposited_dryad_zenodo_dataset():
    design = json.loads(DESIGN.read_text())
    candidate = design["candidate_system"]
    assert candidate["dryad_doi"] == "10.5061/dryad.rv15dv484"
    assert candidate["zenodo_record"] == 6519751
    assert "42 plant-pollinator networks" in candidate["published_scope"]
    assert "three years" in candidate["published_scope"]
    assert design["target_metrics_calculated"] is False


def test_gate_does_not_assume_year_specific_networks_before_source_inspection():
    design = json.loads(DESIGN.read_text())
    boundary = design["source_only_gate"]["temporal_boundary"].lower()
    assert "does not assume" in boundary
    assert "source itself exposes year/time identifiers" in boundary
    prohibited = " ".join(design["prohibited_before_source_admission"]).lower()
    assert "treat 42 published networks as 42 repeated local contexts" in prohibited


def test_source_audit_is_target_metric_free():
    text = SCRIPT.read_text().lower()
    assert "from channel_id.external_archipelago_network" not in text
    assert "network_metrics(" not in text
    assert "interaction_shannon" not in text
    assert "morisita_horn_similarity(" not in text
    assert "pair_support_fraction" not in text


def test_long_table_role_detection_requires_pair_amount_and_context():
    module = load_script()
    roles = module.role_candidates([
        "island",
        "year",
        "plant",
        "pollinator",
        "visits",
    ])
    assert roles["network_or_site"] == ["island"]
    assert roles["time"] == ["year"]
    assert roles["plant"] == ["plant"]
    assert roles["pollinator"] == ["pollinator"]
    assert roles["interaction_amount"] == ["visits"]


def test_admission_signal_requires_raw_pair_structure_and_repeated_network_identifier():
    module = load_script()
    signals = module.inventory_signals([
        {
            "relative_path": "raw.csv",
            "inventory": {
                "format": "delimited_text",
                "raw_pair_long_table_visible": True,
                "candidate_headers": ["island", "year", "plant", "pollinator", "visits"],
            },
        }
    ])
    assert signals["raw_pair_structure_visible"] is True
    assert signals["repeated_network_identifier_signal_visible"] is True
    assert signals["temporal_identifier_signal_visible"] is True
