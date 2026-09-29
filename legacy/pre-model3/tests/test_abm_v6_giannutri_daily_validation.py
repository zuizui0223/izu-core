from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from channel_id.external_archipelago_network import WeightedNetwork

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/run_abm_v6_giannutri_daily_validation.py"
V6 = ROOT / "scripts/run_constraint_mechanism_abm_v6_local_support.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def toy_three_bee_network():
    return WeightedNetwork.from_rows(
        ["shared_plant", "apis_only"],
        ["Apis_mellifera", "Anthophora_dispar", "Bombus_terrestris"],
        [
            [2.0, 3.0, 4.0],
            [5.0, 0.0, 0.0],
        ],
    )


def test_conditioned_support_always_keeps_two_source_ascertained_wild_bees():
    module = load(SCRIPT, "giannutri_validation_test_support")
    network = toy_three_bee_network()
    for strength in (0.25, 0.5, 0.75):
        for seed in range(20):
            active = module.conditioned_active_indices(network, strength, seed)
            names = {network.pollinator_names[index] for index in active}
            assert "Anthophora_dispar" in names
            assert "Bombus_terrestris" in names
            assert names.issubset(set(module.POLLINATORS))


def test_apis_can_be_inactive_without_posthoc_redraw():
    module = load(SCRIPT, "giannutri_validation_test_apis")
    network = toy_three_bee_network()
    active = module.conditioned_active_indices(network, 0.75, 2)
    names = {network.pollinator_names[index] for index in active}
    assert names == {"Anthophora_dispar", "Bombus_terrestris"}


def test_same_v6_mask_application_rejects_apis_only_plant_when_apis_is_inactive():
    module = load(SCRIPT, "giannutri_validation_test_mask")
    v6 = load(V6, "giannutri_validation_test_v6")
    network = toy_three_bee_network()
    active = module.conditioned_active_indices(network, 0.75, 2)
    try:
        v6.apply_active_pollinator_indices(network, active)
    except RuntimeError as exc:
        assert "removed every positive partner" in str(exc)
    else:
        raise AssertionError("v6 must retain the structural row-budget failure")


def test_target_script_contains_no_menorca_fit_or_strength_selection_and_retains_failure():
    text = SCRIPT.read_text().lower()
    assert "menorca" not in text
    assert "preferred_setting" not in text
    assert "argmin" not in text
    assert "best_setting" not in text
    assert "predictive_draws_completed_before_failure" in text
    assert "the context was not skipped, redrawn, repaired, or replaced" in text
    assert "apply_active_pollinator_indices" in text


def test_target_script_asserts_locked_dates_before_empirical_metrics():
    text = SCRIPT.read_text()
    assert "final_dates != locked_dates" in text
    assert "exact_locked_date_match_before_target_calculation" in text
    assert "network_metrics" in text
