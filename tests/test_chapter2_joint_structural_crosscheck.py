from scripts.audit_chapter2_joint_structural_crosscheck import build


def test_joint_existing_harness_crosscheck_retains_branching_without_new_parameter_values():
    payload = build()
    assert payload["configuration"]["replace_arguments"] == {"steps": 240, "trait_adjustment": 0.0}
    assert payload["configuration"]["new_parameter_values_introduced"] is False
    result = payload["result"]
    assert result["realization_class_counts"] == {
        "all_positive": 12,
        "all_negative": 9,
        "mixed_sign": 75,
    }
    assert result["largest_component"] != "starting_position"
    assert result["sum_of_squares_fraction"]["starting_position_by_community_nonadditivity"] > 0.0
