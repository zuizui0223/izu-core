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


def test_missing_sentinels_are_not_taxon_identity():
    module = load_script()
    assert module.identity_value(None) == ""
    assert module.identity_value("NA") == ""
    assert module.identity_value("nan") == ""
    assert module.identity_value("PL1") == "PL1"


def test_month_is_derived_from_source_date_not_period():
    module = load_script()
    assert module.canonical_month(datetime(2022, 10, 15, 9, 0)) == "2022-10"
    assert module.canonical_month("2023-04-21") == "2023-04"


def test_joint_identity_audit_distinguishes_placeholder_patterns():
    module = load_script()
    rows = [
        {"Plant_Best_ID": "P1", "Insect_Best_ID": "I1", "Site": "S", "Period": "P1"},
        {"Plant_Best_ID": "NA", "Insect_Best_ID": "NA", "Site": "S", "Period": "P1", "Num_sp": "NA"},
        {"Plant_Best_ID": "P2", "Insect_Best_ID": "NA", "Site": "S", "Period": "P1"},
        {"Plant_Best_ID": "NA", "Insect_Best_ID": "I2", "Site": "S", "Period": "P1"},
    ]
    result = module.joint_interaction_identity_structure(rows)
    assert result["both_best_ids_nonblank_rows"] == 1
    assert result["both_best_ids_blank_rows"] == 1
    assert result["plant_only_best_id_rows"] == 1
    assert result["insect_only_best_id_rows"] == 1
    assert result["both_blank_num_sp_raw_values"] == {"NA": 1}


def test_num_sp_is_audited_before_selecting_event_weight():
    module = load_script()
    rows = [
        {"Plant_Best_ID": "P1", "Insect_Best_ID": "I1", "Num_sp": 1},
        {"Plant_Best_ID": "P1", "Insect_Best_ID": "I2", "Num_sp": 3},
        {"Plant_Best_ID": "NA", "Insect_Best_ID": "NA", "Num_sp": "NA"},
    ]
    result = module.interaction_amount_structure(rows)
    assert result["identified_interaction_rows"] == 2
    assert result["num_sp_numeric_rows"] == 2
    assert result["num_sp_min"] == 1
    assert result["num_sp_max"] == 3
    assert "no event-weight rule" in result["weight_rule_boundary"].lower()


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


def test_floral_na_placeholder_does_not_define_plant_identity():
    module = load_script()
    rows = [
        {"Site": "S1", "Period": "P1", "Transect": "T", "Quadrat": "Q1", "Plant_Best_ID": "NA", "Name_Floral_unit": "NA", "Nb_Floral_unit": "NA"},
        {"Site": "S1", "Period": "P1", "Transect": "T", "Quadrat": "Q2", "Plant_Best_ID": "P2", "Name_Floral_unit": "flower", "Nb_Floral_unit": 12},
    ]
    result = module.floral_structure(rows)
    assert result["nb_floral_unit_missing_or_nonnumeric_rows"] == 1
    assert result["missing_floral_unit_rows_with_identified_plant"] == 0
    assert result["missing_floral_unit_rows_with_raw_na_plant_id"] == 1
    assert result["nb_floral_unit_positive_rows"] == 1


def test_period_month_mapping_requires_source_one_to_one_mapping():
    module = load_script()
    rows = [
        {"Period": "P1", "Date": datetime(2022, 10, 1)},
        {"Period": "P1", "Date": datetime(2022, 10, 15)},
        {"Period": "P2", "Date": datetime(2022, 11, 1)},
    ]
    assert module.period_month_map(rows) == {"P1": ["2022-10"], "P2": ["2022-11"]}
