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


def test_identity_audit_keeps_best_id_and_fallback_completeness_separate():
    module = load_script()
    rows = [
        {"Best": "A", "Genus": "G", "Species": "s", "Family": "F"},
        {"Best": "", "Genus": "H", "Species": "t", "Family": "F2"},
        {"Best": "", "Genus": "J", "Species": "", "Family": "F3"},
        {"Best": "", "Genus": "", "Species": "", "Family": ""},
    ]
    result = module.identity_structure(rows, "Best", "Genus", "Species", "Family")
    assert result["blank_best_id_rows"] == 3
    assert result["blank_best_with_genus_species_rows"] == 1
    assert result["blank_best_with_genus_only_rows"] == 1
    assert result["fully_unresolved_rows"] == 1


def test_exposure_windows_are_deduplicated_across_event_rows():
    module = load_script()
    rows = [
        {"Site": "S1", "Date": datetime(2022, 10, 1), "Transect": "T1", "H_start": "09:00", "H_end": "09:30"},
        {"Site": "S1", "Date": datetime(2022, 10, 1), "Transect": "T1", "H_start": "09:00", "H_end": "09:30"},
        {"Site": "S1", "Date": datetime(2022, 10, 1), "Transect": "T1", "H_start": "09:30", "H_end": "10:00"},
    ]
    result = module.exposure_structure(rows)
    assert result["unique_observation_window_count"] == 2
    assert result["total_unique_window_minutes_distinct"] == [60.0]


def test_floral_measure_audit_checks_numeric_nonnegative_field_without_network_metrics():
    module = load_script()
    rows = [
        {"Site": "S1", "Date": datetime(2022, 10, 1), "Transect": "T", "Quadrat": "Q1", "Nb_Floral_unit": 0},
        {"Site": "S1", "Date": datetime(2022, 10, 1), "Transect": "T", "Quadrat": "Q2", "Nb_Floral_unit": 12},
    ]
    result = module.floral_structure(rows)
    assert result["nb_floral_unit_zero_rows"] == 1
    assert result["nb_floral_unit_positive_rows"] == 1
    assert result["nb_floral_unit_negative_rows"] == 0
