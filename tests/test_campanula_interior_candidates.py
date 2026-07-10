from channel_id.campanula_interior_candidates import (
    KNOWN_INELIGIBLE_PHOTO_IDS,
    flatten_observations,
    select_and_blind,
)


def test_all_attached_photos_are_retained_and_known_failures_excluded():
    observations = [{
        "id": 10,
        "photos": [
            {"id": 111, "url": "https://example.org/111/square.jpg"},
            {"id": 232356741, "url": "https://example.org/old/square.jpg"},
            {"id": 112, "url": "https://example.org/112/square.jpg"},
        ],
    }]
    rows = flatten_observations(observations, "Oshima", "ardens")
    assert [row["photo_id"] for row in rows] == ["111", "112"]
    assert all("medium" in row["image_url"] for row in rows)
    assert "232356741" in KNOWN_INELIGIBLE_PHOTO_IDS


def test_blind_output_contains_no_geography_and_key_is_separate():
    rows = [
        {"obs_id": "1", "photo_id": "11", "photo_index": "0", "image_url": "https://x/11.jpg", "region": "Oshima", "pollinator_regime": "ardens"},
        {"obs_id": "2", "photo_id": "22", "photo_index": "0", "image_url": "https://x/22.jpg", "region": "Toshima", "pollinator_regime": "no_bombus"},
    ]
    blind, key = select_and_blind(rows, per_region=2, seed=7)
    assert len(blind) == len(key) == 2
    assert all("region" not in row and "pollinator_regime" not in row for row in blind)
    assert {row["pollinator_regime"] for row in key} == {"ardens", "no_bombus"}
    assert {row["card_id"] for row in blind} == {row["card_id"] for row in key}
