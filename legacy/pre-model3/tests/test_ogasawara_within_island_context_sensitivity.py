from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/diagnose_ogasawara_within_island_context_sensitivity.py"


def load_module():
    spec = importlib.util.spec_from_file_location("ogasawara_context_diag_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_context_pair_design_has_nine_within_island_pairs():
    module = load_module()
    pairs = module.make_pairs(module.read_csv(module.CONTEXT))
    assert len(pairs) == 9
    assert sum(p["contrast_type"] == "forest_disturbed_minus_natural" for p in pairs) == 6
    assert sum(p["contrast_type"] == "anole_presence_minus_absence" for p in pairs) == 3
    assert all(p["season"] in module.SEASONS for p in pairs)


def test_four_island_ranges_use_only_same_raw_metrics():
    module = load_module()
    ranges = module.four_island_ranges(module.read_csv(module.ISLAND))
    assert set(ranges) == {"interaction_shannon", "plant_niche_overlap"}
    assert ranges["interaction_shannon"]["range"] > 0
    assert ranges["plant_niche_overlap"]["range"] > 0
    assert len(ranges["interaction_shannon"]["island_values"]) == 4


def test_sign_summary_is_two_sided_and_direction_neutral():
    module = load_module()
    mixed = module.sign_summary([-1.0, 1.0, -2.0, 2.0])
    assert mixed["positive"] == 2
    assert mixed["negative"] == 2
    assert mixed["exact_two_sided_sign_test"] == 1.0


def test_build_is_postresult_diagnostic_not_confirmatory_selection():
    module = load_module()
    result = module.build()
    assert result["status"] == "post_result_diagnosis_after_pr189_not_confirmatory_model_selection"
    assert result["fixed_starting_result"]["decision"] == "ogasawara_raw_weighted_falsifies_both_capacity_directions"
    assert result["design"]["n_pairs"] == 9
    assert result["design"]["outcome_fit_used_to_define_contexts"] is False
    assert "causal" in result["claim_boundary"].lower()
