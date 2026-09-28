from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v9_mahe_iwdb_source_gate_v1.json"
SCRIPT = ROOT / "scripts/acquire_audit_mahe_2017_iwdb.py"


def load_script():
    spec = importlib.util.spec_from_file_location("mahe_source_gate_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_gate_is_bound_to_primary_iwdb_entry_and_64_network_scope():
    design = json.loads(DESIGN.read_text())
    candidate = design["candidate_system"]
    assert candidate["publication_doi"] == "10.1038/nature21071"
    assert "Interaction Web DataBase" in candidate["primary_data_database"]
    assert "64 monthly" in candidate["published_database_scope"]
    assert len(candidate["database_entry_paths"]) == 2
    assert design["target_metrics_calculated"] is False


def test_prior_block_can_only_be_reopened_by_raw_iwdb_matrix_bytes():
    design = json.loads(DESIGN.read_text())
    boundary = design["prior_block_boundary"].lower()
    assert "previous izu-core seychelles attempt was blocked" in boundary
    assert "raw matrix bytes linked by the iwdb entry" in boundary
    assert "third-party reanalyses" in boundary
    blocked = design["source_only_gate"]["blocked_rule"].lower()
    assert "later secondary analyses" in blocked
    assert "earlier blocked transport" in blocked


def test_source_audit_contains_no_network_target_layer():
    text = SCRIPT.read_text().lower()
    assert "from channel_id.external_archipelago_network" not in text
    assert "network_metrics(" not in text
    assert "interaction_shannon" not in text
    assert "morisita_horn_similarity(" not in text
    assert "pair_support_fraction" not in text


def test_workbook_admission_requires_64_ids_metadata_and_interaction_columns():
    module = load_script()
    inventory = {
        "sheets": [{
            "metadata_structure": {
                "unique_counts": {"network_id": 64},
                "metadata_column_indices_zero_based": {
                    "site": 1,
                    "month": 2,
                    "network_id": 3,
                    "plant_id": 4,
                    "floral_abundance": 5,
                },
                "interaction_column_count_excluding_recognized_metadata": 10,
            }
        }]
    }
    assert module.workbook_has_64_network_matrix(inventory) is True
    inventory["sheets"][0]["metadata_structure"]["unique_counts"]["network_id"] = 63
    assert module.workbook_has_64_network_matrix(inventory) is False


def test_gate_does_not_choose_no_visits_or_visitfreq_before_targets():
    design = json.loads(DESIGN.read_text())
    boundary = design["source_only_gate"]["observation_boundary"].lower()
    assert "does not select" in boundary
    assert "no.visits" in boundary
    assert "visitfreq" in boundary
    prohibited = " ".join(design["prohibited_before_source_admission"]).lower()
    assert "choose no.visits versus visitfreq based on fit" in prohibited
