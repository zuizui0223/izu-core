import json
from pathlib import Path

from scripts.build_frozen_abm_state_atlas import build

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "data/results/frozen_abm_state_atlas_frozen.json"


def test_state_atlas_regenerates_exactly():
    assert build() == json.loads(FROZEN.read_text(encoding="utf-8"))


def test_branching_minimal_generator_and_nonidentifying_same_direction():
    atlas = build()
    branching = atlas["synthetic_state_regions"]["branches_downstream"]
    same = atlas["synthetic_state_regions"]["same_direction_response"]
    assert branching["mixed_sign_run_fraction"] > 0
    assert branching["initial_trait_off_mixed_sign_run_fraction"] == 0
    assert branching["minimal_generator_status"] == "initial_trait_position_heterogeneity_necessary_within_declared_v12_residual_gate"
    assert same["trait_off_nonmixed_run_fraction"] == 1.0
    assert same["also_occurs_with_trait_heterogeneity_on_fraction"] > 0
    assert atlas["state_identifiability"]["same_direction_response"]["synthetic_mechanism_identified_within_tested_gate"] is False


def test_network_context_and_assurance_are_not_collapsed():
    atlas = build()
    network = atlas["synthetic_state_regions"]["strong_buffering_via_network_context"]
    assurance = atlas["synthetic_state_regions"]["assurance_attenuation_without_robust_sign_rescue"]
    assert network["sign_rescues"] == 16
    assert network["worsenings"] == 11
    assert assurance["sign_rescues"] == 0
    assert assurance["magnitude_rescues"] == 207
    assert assurance["broadened_support_envelope_sign_rescues"] == 0
    assert atlas["falsification_readout"]["universal_network_buffer_claim_already_rejected"] is True
    assert atlas["falsification_readout"]["robust_assurance_strong_sign_buffer_claim_already_rejected"] is True


def test_external_systems_are_challenges_not_calibration_targets():
    atlas = build()
    external = atlas["external_13_system_challenge"]
    assert external["systems"] == 13
    assert external["generative_state_challenges"] == 11
    assert external["generative_state_covered_or_sign_compatible"] == 11
    assert external["retained_falsifications"] == 1
    assert atlas["field_raw_bundle_required"] is False
    assert atlas["parameters_retuned_to_external_systems"] is False
    assert atlas["new_mechanism_added"] is False
    assert atlas["falsification_readout"]["dominica_frozen_mapping_failure_retained"] is True
