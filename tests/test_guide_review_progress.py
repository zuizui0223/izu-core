from channel_id.guide_review_audit import audit_completed_reviews
from channel_id.guide_review_progress import build_guide_review_progress


def _geo(unit: str, island: str, *, status: str = "accepted") -> dict[str, str]:
    return {
        "observation_unit_id": unit,
        "record_id": unit,
        "source_type": "iNaturalist",
        "verified_island_id": island,
        "geographic_review_status": status,
        "taxon_review_status": status,
    }


def _trait(blind: str, reviewer: str, score: int | None, *, status: str = "accepted") -> dict[str, str]:
    return {
        "blind_unit_id": blind,
        "trait_reviewer_id": reviewer,
        "focal_taxon_consistent": "yes",
        "inner_corolla_visibility": "adequate",
        "flower_open_stage": "open",
        "image_comparable": "yes",
        "guide_ordinal_0_to_3": "" if score is None else str(score),
        "trait_review_status": status,
    }


def _key(blind: str, unit: str) -> dict[str, str]:
    return {
        "blind_unit_id": blind,
        "observation_unit_id": unit,
        "record_id": unit,
        "source_type": "iNaturalist",
        "target_id": "campanula_microdonta",
    }


def test_progress_counts_only_geographically_and_taxonomically_verified_units() -> None:
    geographic = [
        _geo("o1", "Oshima"),
        _geo("o2", "Oshima"),
        _geo("o3", "Oshima"),
        _geo("h1", "Hachijo"),
        _geo("unassigned", "", status="unreviewed"),
    ]
    key = [_key("b1", "o1"), _key("b2", "o2"), _key("b3", "o3"), _key("b4", "h1"), _key("b5", "unassigned")]
    a = [
        _trait("b1", "a", 1),
        _trait("b2", "a", 1),
        _trait("b3", "a", None, status="unreviewed"),
        _trait("b4", "a", None, status="unreviewed"),
        _trait("b5", "a", None, status="unreviewed"),
    ]
    b = [
        _trait("b1", "b", 1),
        _trait("b2", "b", 1),
        _trait("b3", "b", None, status="unreviewed"),
        _trait("b4", "b", None, status="unreviewed"),
        _trait("b5", "b", None, status="unreviewed"),
    ]
    audit = audit_completed_reviews(geographic, a, b, key)
    progress = build_guide_review_progress(audit, min_units_per_island=3)
    islands = {row["island_id"]: row for row in progress.island_rows}

    assert set(islands) == {"Oshima", "Hachijo"}
    assert islands["Oshima"]["verified_geographic_taxon_units"] == "3"
    assert islands["Oshima"]["eligible_for_manual_constraint_review_units"] == "2"
    assert islands["Oshima"]["awaiting_trait_review_units"] == "1"
    assert islands["Oshima"]["potential_shortfall_if_all_pending_pass"] == "0"
    assert islands["Oshima"]["readiness_status"] == "pending_existing_verified_units"
    assert islands["Hachijo"]["verified_geographic_taxon_units"] == "1"
    assert islands["Hachijo"]["eligible_shortfall"] == "3"
    assert islands["Hachijo"]["potential_shortfall_if_all_pending_pass"] == "2"
    assert islands["Hachijo"]["readiness_status"] == "needs_additional_independent_verified_source_records"


def test_progress_assigns_single_next_action_per_audit_disposition() -> None:
    geographic = [_geo("u1", "Oshima"), _geo("u2", "Oshima"), _geo("u3", "Oshima")]
    key = [_key("b1", "u1"), _key("b2", "u2"), _key("b3", "u3")]
    a = [_trait("b1", "a", 1), _trait("b2", "", 1), _trait("b3", "a", 0)]
    b = [_trait("b1", "b", 3), _trait("b2", "b", 1), _trait("b3", "a", 0)]
    audit = audit_completed_reviews(geographic, a, b, key, maximum_reviewer_score_difference=1)
    progress = build_guide_review_progress(audit)
    rows = {row["blind_unit_id"]: row for row in progress.unit_rows}

    assert rows["b1"]["next_required_action"] == "third_independent_blinded_review_or_exclude"
    assert rows["b2"]["next_required_action"] == "record_reviewer_identity_or_repeat_blinded_review"
    assert rows["b3"]["next_required_action"] == "obtain_independent_second_blinded_review"


def test_progress_rejects_invalid_threshold() -> None:
    audit = audit_completed_reviews([], [], [], [])
    try:
        build_guide_review_progress(audit, min_units_per_island=0)
    except ValueError as error:
        assert "positive" in str(error)
    else:
        raise AssertionError("invalid threshold accepted")
