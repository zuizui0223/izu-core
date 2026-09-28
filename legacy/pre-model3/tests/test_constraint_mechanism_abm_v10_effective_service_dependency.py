from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

import pytest

from channel_id.external_archipelago_network import WeightedNetwork

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_constraint_mechanism_abm_v10_effective_service_dependency.py"


def load_v10():
    spec = importlib.util.spec_from_file_location("abm_v10_test_module", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_quality_zero_is_exact_identity_and_full_probe_stays_in_v3_range():
    v10 = load_v10()
    names = ("p1", "p2", "p3")
    assert v10.quality_multipliers(names, seed=1, quality_strength=0.0) == (1.0, 1.0, 1.0)
    values = v10.quality_multipliers(names, seed=1, quality_strength=1.0)
    assert all(0.2 <= value <= 1.8 for value in values)


def test_quality_layer_changes_service_not_opportunity():
    v10 = load_v10()
    row = (0.2, 0.3)
    off_opportunity, off_service = v10.row_service(row, (1.0, 1.0), saturation=2.0)
    on_opportunity, on_service = v10.row_service(row, (0.5, 1.5), saturation=2.0)
    assert off_opportunity == pytest.approx(0.5)
    assert on_opportunity == pytest.approx(0.5)
    assert off_service == pytest.approx(1.0 - math.exp(-1.0))
    assert on_service != pytest.approx(off_service)


def test_missing_local_plant_has_zero_opportunity_and_service():
    v10 = load_v10()
    assert v10.row_service(None, (), saturation=2.0) == (0.0, 0.0)


def test_plant_rows_does_not_mutate_network():
    v10 = load_v10()
    network = WeightedNetwork.from_rows(["lineage_1"], ["pollinator_1"], [[0.25]])
    rows = v10.plant_rows(network)
    assert rows == {"lineage_1": (0.25,)}
    assert network.matrix == ((0.25,),)


def test_small_build_preserves_ablation_contract_and_loads_no_empirical_targets():
    v10 = load_v10()
    payload = v10.build(replicates=1, contexts=1, n_lineages=6, steps=5, seed=1234)
    assert payload["design"]["empirical_inputs_loaded"] == []
    assert payload["design"]["izu_target_frequencies_loaded"] is False
    assert payload["design"]["external_target_values_loaded"] is False
    assert payload["summary"]["configuration_count"] == 9
    assert payload["summary"]["lineage_contrast_count"] == 54
    assert payload["summary"]["upstream_identical_between_quality_ablations"] is True
    assert payload["summary"]["decision"] in {
        "v10_quality_layer_changes_magnitude_but_not_response_branch_identity",
        "v10_partner_effectiveness_interacts_with_v9_to_broaden_downstream_branching",
        "v10_partner_effectiveness_changes_branch_identity_without_broadening_positive_tail",
    }
