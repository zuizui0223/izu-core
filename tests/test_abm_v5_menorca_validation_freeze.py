from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v5_menorca_nine_local_validation_v1.json"
GEO = ROOT / "scripts/match_menorca2023_to_gift_opportunity.py"


def load_geo():
    spec = importlib.util.spec_from_file_location("menorca_geo_freeze_test", GEO)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_menorca_freeze_has_exact_nine_source_defined_local_sheets():
    design = json.loads(DESIGN.read_text())
    sheets = design["held_out_system"]["source_defined_local_sheets"]
    assert sheets == [
        "Favaritx",
        "Platja Es Grau",
        "Sa Bassa",
        "costa Son Bou",
        "Llucalari",
        "Sant Jaume de Dalt",
        "Cala Tirant",
        "Salinas",
        "Torre Fornells",
    ]
    assert len(set(sheets)) == 9
    assert design["network_reconstruction"]["three_by_three_regrouping"].startswith("prohibited")


def test_menorca_freeze_keeps_two_targets_and_fvr_weight():
    design = json.loads(DESIGN.read_text())
    assert design["outcomes_frozen_before_target_calculation"] == [
        "interaction_shannon",
        "mean_plant_niche_overlap_morisita_horn",
    ]
    assert design["source_recovery_gate"]["weight_column"] == "FVR"
    assert design["network_reconstruction"]["pair_weight"].startswith("sum FVR")


def test_menorca_predictive_mixture_is_equal_weight_and_not_selectable():
    design = json.loads(DESIGN.read_text())
    predictive = design["v5_predictive_distribution"]
    assert predictive["context_strengths"] == [0.25, 0.5, 0.75, 1.0]
    assert predictive["v4_saturations"] == [1.0, 1.5, 2.0, 2.5, 3.0]
    assert predictive["context_strength_weighting"] == "equal"
    assert predictive["saturation_weighting"] == "equal"
    assert predictive["replicates_per_setting"] == 100
    assert predictive["preferred_setting_selection"] == "prohibited"


def test_menorca_primary_statistic_and_decision_cannot_change_posthoc():
    design = json.loads(DESIGN.read_text())
    stats = design["empirical_primary_statistics"]
    assert "max interaction_shannon" in stats["interaction_shannon_relative_local_range"]
    assert "pooled-nine-sheet metaweb" in stats["interaction_shannon_relative_local_range"]
    assert "max mean_plant_niche_overlap" in stats["plant_niche_overlap_relative_local_range"]
    prohibited = " ".join(design["prohibited_after_target_calculation"]).lower()
    assert "relative local range" in prohibited
    assert "context strength or saturation" in prohibited
    assert "drop or merge" in prohibited


def test_frozen_ecdf_interpolation_preserves_reference_knots():
    geo = load_geo()
    reference = [10.0, 20.0, 40.0]
    assert geo.frozen_ecdf_interpolate(10.0, reference) == 0.0
    assert geo.frozen_ecdf_interpolate(20.0, reference) == 0.5
    assert geo.frozen_ecdf_interpolate(40.0, reference) == 1.0
    assert geo.frozen_ecdf_interpolate(30.0, reference) == 0.75
    assert geo.frozen_ecdf_interpolate(1.0, reference) == 0.0
    assert geo.frozen_ecdf_interpolate(100.0, reference) == 1.0
