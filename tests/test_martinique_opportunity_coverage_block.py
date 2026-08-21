from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/diagnose_martinique_opportunity_coverage_block.py"


def load_script():
    spec = importlib.util.spec_from_file_location("martinique_coverage_diag_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_diagnosis_is_not_network_target_or_v9_fit():
    text = SCRIPT.read_text().lower()
    assert "network_metrics(" not in text
    assert "interaction_shannon" not in text
    assert "predictive_envelope" not in text
    assert "run_constraint_mechanism_abm_v9" not in text


def test_identity_missing_sentinels_are_not_taxa():
    module = load_script()
    assert module.identity("NA") == ""
    assert module.identity(None) == ""
    assert module.identity("Ocimum tenuiflorum") == "Ocimum tenuiflorum"


def test_structural_key_uses_sampling_provenance_not_taxon_identity():
    module = load_script()
    row = {
        "Period": "P1", "Date": "2022-10-01", "Site": "C1", "Transect": "T1",
        "H_start": "09:00", "H_end": "09:05", "Num_sp": 7,
        "Plant_Best_ID": "A", "Insect_Best_ID": "B",
    }
    key = module.structural_key(row)
    assert key == ("P1", "2022-10-01", "C1", "T1", "09:00", "09:05", "7")
    row["Plant_Best_ID"] = "renamed"
    assert module.structural_key(row) == key
