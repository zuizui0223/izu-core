from channel_id.inaturalist_photo_proxy_queue import haversine_km, queue_rows


def test_haversine_is_zero_for_same_point() -> None:
    assert haversine_km(34.0, 139.0, 34.0, 139.0) == 0.0


def test_queue_uses_nearest_proxy_without_making_island_assignment() -> None:
    candidates = [
        {
            "candidate_id": "inat:1:photo:1",
            "target_id": "campanula_microdonta",
            "latitude": "34.01",
            "longitude": "139.01",
        }
    ]
    proxies = (
        {"island_id": "near", "latitude": 34.0, "longitude": 139.0},
        {"island_id": "far", "latitude": 33.0, "longitude": 139.0},
    )

    rows = queue_rows(candidates, proxies)

    assert rows[0]["nearest_declared_proxy"] == "near"
    assert rows[0]["second_nearest_declared_proxy"] == "far"
    assert rows[0]["reviewer_island_decision"] == "unreviewed"
    assert "review aid only" in rows[0]["proxy_assignment_boundary"]


def test_queue_leaves_proxy_fields_blank_when_coordinates_missing() -> None:
    candidates = [{"candidate_id": "inat:2:photo:1", "target_id": "campanula_microdonta", "latitude": "", "longitude": ""}]
    proxies = (
        {"island_id": "a", "latitude": 34.0, "longitude": 139.0},
        {"island_id": "b", "latitude": 33.0, "longitude": 139.0},
    )

    row = queue_rows(candidates, proxies)[0]

    assert row["nearest_declared_proxy"] == ""
    assert row["reviewer_island_decision"] == "unreviewed"
