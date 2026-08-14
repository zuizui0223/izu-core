import json
from pathlib import Path


def load_audit():
    return json.loads(
        Path("data/design/external_bridge_cordia_subcordata_source_audit.json")
        .read_text(encoding="utf-8")
    )


def test_cordia_is_near_complete_but_not_complete_or_formal():
    audit = load_audit()
    assert audit["admission_state"] == "bridge_system_partial"
    assert audit["bridge_strength"] == "near_complete_within_archipelago"
    assert audit["bridge_complete"] is False
    assert audit["formal_cross_system_model_eligible"] is False


def test_cordia_preserves_two_island_morph_state_without_causal_promotion():
    audit = load_audit()
    assert audit["response_channel"]["yongxing_morph_ratio"]["long_morph_n"] == 34
    assert audit["response_channel"]["dong_morph_ratio"]["long_morph_n"] == 0
    blocked = " ".join(audit["bridge_assessment"]["blocked_claims"])
    assert "pollinator-caused" in blocked


def test_cordia_dependency_is_yongxing_only_and_self_compatibility_is_not_assurance():
    audit = load_audit()
    assert audit["dependency_channel"]["population"] == "Yongxing Island"
    bagged = audit["dependency_channel"]["pollination_treatments"]["bagged_without_hand_pollination"]
    assert bagged["long_morph_seed_set"] == 0.0
    assert bagged["short_morph_seed_set"] == 0.0
    blocked = " ".join(audit["bridge_assessment"]["blocked_claims"])
    assert "self-compatibility with autonomous reproductive assurance" in blocked


def test_cordia_direct_effectiveness_is_not_transported_to_dong():
    audit = load_audit()
    assert audit["effective_service_channel"]["population"] == "Yongxing Island"
    assert audit["bridge_assessment"]["all_channels_matched_on_both_sides_of_response_transition"] is False
    blocked = " ".join(audit["bridge_assessment"]["blocked_claims"])
    assert "Yongxing single-visit effectiveness numerically to Dong" in blocked


def test_cordia_zosterops_has_higher_conspecific_single_visit_deposition_than_apis():
    audit = load_audit()
    long_morph = audit["effective_service_channel"]["single_visit_pollen_deposition"]["long_morph"]
    assert long_morph["zosterops_japonicus"]["conspecific_mean"] == 153.7
    assert long_morph["apis_cerana"]["conspecific_mean"] == 13.0
    assert long_morph["conspecific_test"]["p"] == 0.008


def test_cordia_byte_level_provenance_stays_open():
    audit = load_audit()
    assert audit["source"]["source_routes"]["checksum_locked"] is False
