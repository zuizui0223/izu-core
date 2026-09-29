from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from channel_id.external_archipelago_network import WeightedNetwork

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/run_abm_v8_cabrera_validation.py"
DESIGN = ROOT / "data/design/abm_v8_cabrera_validation_v1.json"
V8 = ROOT / "scripts/run_constraint_mechanism_abm_v8_pair_support.py"
V6 = ROOT / "scripts/run_constraint_mechanism_abm_v6_local_support.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def toy_network() -> WeightedNetwork:
    return WeightedNetwork.from_rows(
        ["p1", "p2"],
        ["a", "b", "c"],
        [[3.0, 2.0, 1.0], [1.0, 4.0, 2.0]],
    )


def test_fast_pair_mask_is_exactly_the_frozen_v8_draw():
    module = load(SCRIPT, "cabrera_validation_fast_mask_test")
    v8 = load(V8, "cabrera_validation_fast_mask_v8")
    v6 = load(V6, "cabrera_validation_fast_mask_v6")
    network = toy_network()
    for strength in (0.25, 0.5, 0.75):
        for seed in (20260821, 20260822, 20260823, 20260824):
            expected_mask, expected_active = v8.draw_hierarchical_pair_support_mask(
                network,
                support_seed=seed,
                support_strength=strength,
            )
            actual_mask, actual_active = module.fast_v8_pair_mask(
                v8,
                v6,
                network,
                support_seed=seed,
                support_strength=strength,
            )
            assert actual_mask == expected_mask
            assert actual_active == expected_active


def test_frozen_pair_support_statistics_have_expected_toy_values():
    module = load(SCRIPT, "cabrera_validation_stats_test")
    opportunity = {("p1", "a"), ("p1", "b"), ("p2", "b")}
    pair_sets = [
        {("p1", "a"), ("p1", "b")},
        {("p1", "b"), ("p2", "b")},
        set(),
    ]
    stats = module.context_stats(
        pair_sets,
        [1.0, 0.5, 0.0],
        opportunity_pairs=opportunity,
        pooled_shannon=2.0,
        pooled_plants={"p1", "p2"},
        pooled_pollinators={"a", "b"},
    )
    assert stats["median_pair_support_fraction"] == 2 / 3
    # Pairwise turnovers: 2/3, 1, 1 => 8/9.
    assert abs(stats["mean_pair_support_jaccard_turnover"] - 8 / 9) < 1e-12
    assert stats["interaction_shannon_relative_context_range"] == 0.5
    assert stats["secondary"]["empty_context_count"] == 1


def test_validation_script_is_bound_to_frozen_obs_n_ind_design():
    design = json.loads(DESIGN.read_text())
    rule = design["source_native_reconstruction"]
    assert rule["primary_method_label"] == "obs"
    assert rule["primary_interaction_weight"] == "N ind"
    assert len(rule["locked_context_keys"]) == 55
    text = SCRIPT.read_text()
    assert 'rule["primary_method_label"]' in text
    assert 'row.get("N ind")' in text
    assert "observed_keys != locked_set" in text
    assert "blank Pollinator row is not an explicit N ind=0 absence record" in text


def test_validation_contains_no_post_target_rescue_or_old_failure_fit():
    text = SCRIPT.read_text().lower()
    assert "menorca" not in text
    assert "giannutri" not in text
    assert "n visit flowers" not in text
    assert "argmin" not in text
    assert "best_setting" not in text
    assert "preferred_setting" not in text
    assert "redraw" not in text


def test_decision_requires_all_three_frozen_primary_estimands():
    design = json.loads(DESIGN.read_text())
    primary = list(design["primary_estimands"])
    assert primary == [
        "median_pair_support_fraction",
        "mean_pair_support_jaccard_turnover",
        "interaction_shannon_relative_context_range",
    ]
    text = SCRIPT.read_text()
    assert "for key, empirical_value in empirical[\"primary_estimands\"].items()" in text
    assert "all(value is True for value in tests.values())" in text
    assert "v8_survives_cabrera_conditional_pair_support_test" in text
    assert "v8_fails_cabrera_conditional_pair_support_predictive_adequacy" in text
