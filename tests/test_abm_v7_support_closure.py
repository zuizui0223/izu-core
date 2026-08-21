from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

from channel_id.external_archipelago_network import WeightedNetwork

ROOT = Path(__file__).resolve().parents[1]
V7 = ROOT / "scripts/run_constraint_mechanism_abm_v7_support_closure.py"
V6 = ROOT / "scripts/run_constraint_mechanism_abm_v6_local_support.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def toy():
    return WeightedNetwork.from_rows(
        ["shared", "apis_only"],
        ["Apis", "Anthophora", "Bombus"],
        [[1.0, 1.0, 1.0], [2.0, 0.0, 0.0]],
    )


def test_joint_closure_resolves_partnerless_plant_without_manufacturing_service():
    v7 = load(V7, "v7_test_core")
    network, audit = v7.apply_joint_support_closure(toy(), (1, 2))
    assert network is not None
    assert network.plant_names == ("shared",)
    assert network.pollinator_names == ("Anthophora", "Bombus")
    assert audit["dropped_partnerless_positive_plants"] == ["apis_only"]
    assert math.isclose(sum(network.matrix[0]), 3.0, rel_tol=1e-12)


def test_same_mask_is_v6_failure_but_v7_closes_support():
    v7 = load(V7, "v7_test_compare")
    v6 = load(V6, "v7_test_v6")
    source = toy()
    try:
        v6.apply_active_pollinator_indices(source, (1, 2))
    except RuntimeError:
        pass
    else:
        raise AssertionError("toy mask must reproduce v6 failure class")
    closed, _ = v7.apply_joint_support_closure(source, (1, 2))
    assert closed is not None


def test_v6_admissible_mask_is_unchanged():
    v7 = load(V7, "v7_test_identity")
    v6 = load(V6, "v7_test_v6_identity")
    source = WeightedNetwork.from_rows(
        ["p1", "p2"], ["a", "b", "c"], [[1, 2, 3], [2, 2, 2]]
    )
    expected = v6.apply_active_pollinator_indices(source, (1, 2))
    actual, audit = v7.apply_joint_support_closure(source, (1, 2))
    assert actual == expected
    assert audit["dropped_partnerless_positive_plant_count"] == 0


def test_two_partial_support_masks_branch_joint_plant_support_when_reducible():
    v7 = load(V7, "v7_test_joint_branch")
    source = toy()
    retains_apis_only, audit_keep = v7.apply_joint_support_closure(source, (0, 1))
    drops_apis_only, audit_drop = v7.apply_joint_support_closure(source, (1, 2))
    assert retains_apis_only is not None
    assert drops_apis_only is not None
    assert retains_apis_only.plant_names == ("shared", "apis_only")
    assert drops_apis_only.plant_names == ("shared",)
    assert audit_keep["dropped_partnerless_positive_plant_count"] == 0
    assert audit_drop["dropped_partnerless_positive_plants"] == ["apis_only"]


def test_contract_adds_no_plant_dropout_parameter_or_giannutri_fit():
    v7 = load(V7, "v7_test_contract")
    contract = v7.build_contract()
    assert contract["new_parameter_count"] == 0
    assert contract["joint_support_rule"]["independent_plant_dropout_probability"] is None
    assert "No Giannutri target amplitude" in contract["failure_source"]["use_of_failure"]
    assert "cannot confirm v7" in contract["next_empirical_gate"]
