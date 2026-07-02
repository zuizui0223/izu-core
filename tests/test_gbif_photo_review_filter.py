from channel_id.gbif_photo_review_filter import split_gbif_review_rows


def test_obvious_iNaturalist_republications_are_not_sent_to_parallel_gbif_review() -> None:
    rows = [
        {"record_id": "1", "origin_platform_hint": "iNaturalist_republication"},
        {"record_id": "2", "origin_platform_hint": "not_flagged_as_iNaturalist"},
        {"record_id": "2", "origin_platform_hint": "not_flagged_as_iNaturalist"},
    ]

    retained, excluded, counts = split_gbif_review_rows(rows)

    assert [row["record_id"] for row in retained] == ["2", "2"]
    assert [row["record_id"] for row in excluded] == ["1"]
    assert counts["input_unique_gbif_records"] == 2
    assert counts["excluded_unique_gbif_records"] == 1
    assert counts["retained_unique_gbif_records"] == 1
