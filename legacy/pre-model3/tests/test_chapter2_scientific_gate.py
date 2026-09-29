from scripts.evaluate_chapter2_scientific_gate import assess


def payloads(*, mean_boundary=True, realization_fraction=0.5, joint_fraction=0.5, context_changes=3, assurance_safe=True, assurance_rescues=2):
    phase1 = {
        "baseline": {
            "mean_geometry_mixed_sign": mean_boundary,
            "mixed_sign_realization_fraction": realization_fraction,
        }
    }
    joint = {"class_fractions": {"mixed_mean_geometry": joint_fraction}}
    thresholds = {
        "context_map": {
            "lineages_with_any_sign_change": context_changes,
            "median_first_sign_change_strength": 0.4,
        },
        "assurance_map": {
            "upstream_service_identical_across_assurance_multipliers": assurance_safe,
            "lineages_with_any_sign_rescue": assurance_rescues,
            "median_first_sign_rescue_multiplier": 2.0 if assurance_rescues else None,
        },
    }
    return phase1, joint, thresholds


def test_research_article_candidate_requires_broad_mean_geometry():
    result = assess(*payloads())
    assert result["route"] == "research_article_candidate"
    assert result["submission_ready"] is True


def test_realization_contingent_route_when_mean_boundary_is_weak():
    result = assess(*payloads(mean_boundary=False, realization_fraction=0.45, joint_fraction=0.1))
    assert result["route"] == "research_article_possible_but_branching_is_realization_contingent"
    assert result["headline"] == "starting_position_by_pollinator_realization_interaction"


def test_conceptual_route_when_branching_is_not_robust():
    result = assess(*payloads(mean_boundary=False, realization_fraction=0.1, joint_fraction=0.0))
    assert result["route"] == "conceptual_review_or_mini_review"
    assert result["submission_ready"] is False


def test_assurance_upstream_mismatch_blocks_submission():
    result = assess(*payloads(assurance_safe=False))
    assert "assurance_threshold_map_changes_upstream_service" in result["blocking_failures"]
    assert result["submission_ready"] is False


def test_context_sign_change_is_required_for_context_headline_support():
    result = assess(*payloads(context_changes=0))
    assert "no_local_context_sign_change_found" in result["blocking_failures"]
