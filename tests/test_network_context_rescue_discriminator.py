import importlib.util
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/run_network_context_rescue_discriminator.py"
FREEZE = ROOT / "data/design/network_context_rescue_discriminator_freeze.json"
PARENT_FREEZE = ROOT / "data/design/network_context_buffering_robustness_freeze.json"


def load_module():
    spec = importlib.util.spec_from_file_location("network_context_rescue_discriminator_test_module", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_discriminator_reuses_exact_parent_robustness_configuration():
    gate = json.loads(FREEZE.read_text(encoding="utf-8"))
    parent = json.loads(PARENT_FREEZE.read_text(encoding="utf-8"))["configuration"]
    config = gate["reuse_exact_parent_configuration"]
    assert config["saturations"] == parent["saturations"]
    assert config["replicates"] == parent["replicates"]
    assert config["contexts"] == parent["contexts"]
    assert config["lineages"] == parent["lineages"]
    assert config["steps"] == parent["steps"]
    assert config["support_off"] == parent["support_off"]
    assert config["support_on"] == parent["support_on"]
    assert config["seed_block"] == parent["independent_seed_block"]
    assert config["new_parameter_count"] == 0


def test_descriptor_list_is_frozen_before_outcome_inspection():
    module = load_module()
    gate = json.loads(FREEZE.read_text(encoding="utf-8"))
    assert tuple(gate["predeclared_descriptors"]) == module.DESCRIPTORS
    assert "add descriptor variables after outcome-class inspection" in gate["forbidden"]
    assert "drop worsening cases from the analysis" in gate["forbidden"]


def test_classification_uses_zero_direction_boundary_only():
    module = load_module()
    assert module.classify(-0.2, 0.01) == "sign_rescue"
    assert module.classify(-0.2, -0.1) == "attenuation_only"
    assert module.classify(-0.2, -0.3) == "worsening"
    assert module.classify(-0.2, -0.2) == "other_no_material_change"


def test_row_structure_reports_active_richness_entropy_and_dominance():
    module = load_module()
    active, richness, shannon, dominant = module.row_structure((1.0, 1.0, 0.0))
    assert active == 1.0
    assert richness == 2.0
    assert math.isclose(shannon, math.log(2.0))
    assert dominant == 0.5
    assert module.row_structure(None) == (0.0, 0.0, 0.0, 0.0)
