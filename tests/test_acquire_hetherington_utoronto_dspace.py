from scripts.acquire_hetherington_utoronto_dspace import (
    build_lock,
    discover_item_candidates,
    select_exact_item,
)


def test_dspace_search_candidates_and_exact_title_selection():
    payload = {
        "_embedded": {
            "searchResult": {
                "_embedded": {
                    "objects": [
                        {
                            "_embedded": {
                                "indexableObject": {
                                    "uuid": "12345678-1234-1234-1234-123456789abc",
                                    "name": "The Comparative Evolution of the Floral Traits of Island Angiosperms",
                                    "handle": "1807/123456",
                                }
                            }
                        },
                        {
                            "_embedded": {
                                "indexableObject": {
                                    "uuid": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                                    "name": "Unrelated thesis",
                                }
                            }
                        },
                    ]
                }
            }
        }
    }
    candidates = discover_item_candidates(payload)
    assert len(candidates) == 2
    selected = select_exact_item(
        candidates,
        "The Comparative Evolution of the Floral Traits of Island Angiosperms",
    )
    assert selected["uuid"] == "12345678-1234-1234-1234-123456789abc"
    assert selected["handle"] == "1807/123456"


def test_locked_thesis_bytes_do_not_create_a_third_effect():
    source = {
        "source_id": "hetherington_rauth_johnson_2020_136_pairs",
        "thesis_title": "The Comparative Evolution of the Floral Traits of Island Angiosperms",
    }
    item = {
        "uuid": "12345678-1234-1234-1234-123456789abc",
        "name": source["thesis_title"],
        "handle": "1807/123456",
    }
    bundle = {"uuid": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb", "name": "ORIGINAL"}
    bitstream = {"uuid": "cccccccc-cccc-cccc-cccc-cccccccccccc", "name": "thesis.pdf"}
    data = b"%PDF-1.7\nsynthetic fixture\n"
    lock = build_lock(
        source,
        item,
        bundle,
        bitstream,
        data,
        "https://utoronto.scholaris.ca/server/api/core/bitstreams/cccccccc-cccc-cccc-cccc-cccccccccccc/content",
        ["https://utoronto.scholaris.ca/server/api/discover/search/objects"],
    )
    assert lock["sha256"]
    assert lock["source_native_136_pair_table_verified"] is False
    assert lock["third_response_shape_admitted"] is False
    assert lock["formal_cross_system_fit_opened"] is False
