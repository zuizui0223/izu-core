from channel_id.guide_review_audit import audit_completed_reviews


def _geo(unit: str, island: str = "Oshima", *, geographic: str = "accepted", taxon: str = "accepted") -> dict[str, str]:
    return {
        "observation_unit_id": unit,
        "source_type": "iNaturalist",
        "record_id": unit,
        "verified_island_id": island,
        "geographic_review_status": geographic,
        "taxon_review_status": taxon,
    }


def _trait(blind: str, reviewer: str, score: int | None, *, accepted: bool = True) -> dict[str, str]:
    return {
        "blind_unit_id": blind,
        "trait_reviewer_id": reviewer,
        "focal_taxon_consistent": "yes",
        "inner_corolla_visibility": "adequate",
        "flower_open_stage": "open",
        "image_comparable": "yes",
        "guide_ordinal_0_to_3": "" if score is None else str(score),
        "trait_review_status": "accepted" if accepted else "rejected",
    }


def _key(blind: str, unit: str) -> dict[str, str]:
    return {
        "blind_unit_id": blind,
        "observation_unit_id": unit,
        "source_type": "iNaturalist",
        "record_id": unit,
        "target_id": "campanula_microdonta",
    }


def test_audit_writes_per_unit_exclusion_codes_and_only_all_gates_pass() -> None:
    geographic = [
        _geo("u1"),
        _geo("u2", geographic="rejected"),
        _geo("u3"),
        _geo("u4"),
        _geo("u5"),
    ]
    key = [_key(f"b{index}", f"u{index}") for index in range(1, 6)]
    review_a = [
        _trait("b1", "reviewer_a", 2),
        _trait("b2", "reviewer_a", 2),
        _trait("b3", "reviewer_a", 2),
        _trait("b4", "reviewer_a", 2),
        _trait("b5", "", 2),
    ]
    review_b = [
        _trait("b1", "reviewer_b", 3),
        _trait("b2", "reviewer_b", 2),
        _trait("b3", "reviewer_a", 2),
        _trait("b4", "reviewer_b", 0),
        _trait("b5", "reviewer_b", 2),
    ]

    audit = audit_completed_reviews(geographic, review_a, review_b, key, maximum_reviewer_score_difference=1)
    rows = {row["blind_unit_id"]: row for row in audit.unit_rows}

    assert rows["b1"]["unit_disposition"] == "eligible_for_manual_constraint_review"
    assert rows["b1"]["trait_score_difference"] == "1"
    assert rows["b2"]["exclusion_code"] == "geographic_review_not_accepted"
    assert rows["b3"]["exclusion_code"] == "same_reviewer_identity"
    assert rows["b4"]["exclusion_code"] == "reviewer_score_difference_exceeds_threshold"
    assert rows["b5"]["exclusion_code"] == "missing_reviewer_identity"
    assert audit.eligible_observation_unit_ids == ("u1",)


def test_audit_reports_descriptive_agreement_only_for_scorable_pairs() -> None:
    geographic = [_geo("u1"), _geo("u2"), _geo("u3")]
    key = [_key("b1", "u1"), _key("b2", "u2"), _key("b3", "u3")]
    review_a = [_trait("b1", "a", 0), _trait("b2", "a", 1), _trait("b3", "a", None, accepted=False)]
    review_b = [_trait("b1", "b", 0), _trait("b2", "b", 3), _trait("b3", "b", 1)]

    audit = audit_completed_reviews(geographic, review_a, review_b, key, maximum_reviewer_score_difference=1)
    metrics = {row["metric"]: row["value"] for row in audit.agreement_rows}

    assert metrics["scorable_trait_pairs"] == "2"
    assert metrics["exact_score_agreement_fraction"] == "0.500000"
    assert metrics["within_1_ordinal_step_fraction"] == "0.500000"
    assert metrics["mean_absolute_score_difference"] == "1.000000"
    assert metrics["excluded:trait_review_a_not_accepted_or_unscorable"] == "1"


def test_audit_requires_keyed_rows_but_does_not_silently_convert_missing_review_to_eligible() -> None:
    geographic = [_geo("u1")]
    key = [_key("b1", "u1")]
    review_a = [_trait("b1", "a", 2)]

    audit = audit_completed_reviews(geographic, review_a, [], key)

    assert audit.unit_rows[0]["exclusion_code"] == "missing_trait_review_row"
    assert audit.eligible_observation_unit_ids == ()
