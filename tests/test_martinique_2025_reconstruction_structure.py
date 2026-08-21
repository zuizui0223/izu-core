from __future__ import annotations

import importlib.util
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/audit_martinique_2025_reconstruction_structure.py"


def load_script():
    scripts_dir = str(ROOT / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    spec = importlib.util.spec_from_file_location("martinique_reconstruction_structure_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_structure_audit_is_target_free():
    text = SCRIPT.read_text().lower()
    assert "from channel_id.external_archipelago_network" not in text
    assert "network_metrics(" not in text
    assert "interaction_shannon" not in text
    assert "morisita" not in text
    assert "pair_support_fraction" not in text
    assert "predictive_envelope" not in text


def test_month_is_derived_from_source_date_not_period():
    module = load_script()
    assert module.canonical_month(datetime(2022, 10, 15, 9, 0)) == "2022-10"
    assert module.canonical_month("2023-04-21") == "2023-04"


def test_joint_identity_audit_distinguishes_placeholder_patterns():
    module = load_script()
    rows = [
        {"Plant_Best_ID": "P1", "Insect_Best_ID": "I1", "Site": "S", "Period": "P1"},
        {"Plant_Best_ID": "", "Insect_Best_ID": "", "Site": "S", "Period": "P1", "Num_sp": 0},
        {"Plant_Best_ID": "P2", "Insect_Best_ID": "", "Site": "S", "Period": "P1"},
        {"Plant_Best_ID": "", "Insect_Best_ID": "I2", "Site": "S", "Period": "P1"},
    ]
    result = module.joint_interaction_identity_structure(rows)
    assert result["both_best_ids_nonblank_rows"] == 1
    assert result["both_best_ids_blank_rows"] == 1
    assert result["plant_only_best_id_rows"] == 1
    assert result["insect_only_best_id_rows"] == 1


def test_timing_fields_are_not_summed_as_sampling_effort():
    module = load_script()
    rows = [
        {"Site": "S1", "Period": "P1", "H_start": "09:00", "H_end": "09:30"},
        {"Site": "S1", "Period": "P1", "H_start": "09:30", "H_end": "10:00"},
    ]
    result = module.timing_field_structure(rows)
    assert result["published_protocol_minutes_per_site_period"] == 60
    assert result["event_rows_with_end_after_start"] == 2
    assert "never summed" in result["effort_rule_boundary"]
    assert "total_unique_window_minutes" not in result


def test_floral_measure_audit_preserves_missing_rows_for_later_binary_rule():
    module = load_script()
    rows = [
        {"Site": "S1", "Period": "P1", "Transect": "T", "Quadrat": "Q1", "Plant_Best_ID": "P1", "Name_Floral_unit": "flower", "Nb_Floral_unit": None},
        {"Site": "S1", "Period": "P1", "Transect": "T", "Quadrat": "Q2", "Plant_Best_ID": "P2", "Name_Floral_unit": "flower", "Nb_Floral_unit": 12},
    ]
    result = module.floral_structure(rows)
    assert result["nb_floral_unit_missing_or_nonnumeric_rows"] == 1
    assert result["missing_floral_unit_rows_with_nonblank_plant_best_id"] == 1
    assert result["nb_floral_unit_positive_rows"] == 1
    assert "does not yet decide" in result["binary_opportunity_boundary"]


def test_period_month_mapping_requires_source_one_to_one_mapping():
    module = load_script()
    rows = [
        {"Period": "P1", "Date": datetime(2022, 10, 1)},
        {"Period": "P1", "Date": datetime(2022, 10, 15)},
        {"Period": "P2", "Date": datetime(2022, 11, 1)},
    ]
    assert module.period_month_map(rows) == {"P1": ["2022-10"], "P2": ["2022-11"]}
