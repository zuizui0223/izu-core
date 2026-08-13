import pytest

from scripts.acquire_hetherington_utoronto_dspace import (
    build_lock,
    discover_item_candidates,
    select_exact_item,
    select_full_thesis_pdf,
)


def test_dspace_search_candidates_and_exact_title_selection():
    payload = {
        "_embedded": {"searchResult": {"_embedded": {"objects": [
            {"_embedded": {"indexableObject": {"uuid": "12345678-1234-1234-1234-123456789abc", "name": "The Comparative Evolution of the Floral Traits of Island Angiosperms", "handle": "1807/123456"}}},
            {"_embedded": {"indexableObject": {"uuid": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "name": "Unrelated thesis"}}},
        ]}}}
    }
    candidates = discover_item_candidates(payload)
    selected = select_exact_item(candidates, "The Comparative Evolution of the Floral Traits of Island Angiosperms")
    assert selected["uuid"] == "12345678-1234-1234-1234-123456789abc"
    assert selected["handle"] == "1807/123456"


def test_full_thesis_selected_by_explicit_filename_not_size():
    candidates = [
        {"uuid": "61628fd5-25ed-4fa9-b869-593b4a71b8eb", "name": "Hetherington-Rauth_Molly_C_201906_MSc_thesis_expandedabstract.pdf", "sizeBytes": 999999999, "sequenceId": 3},
        {"uuid": "fa56a964-8e77-47bb-9d42-476b1e2ed97e", "name": "Hetherington-Rauth_Molly_C_201906_MSc_thesis.pdf", "sizeBytes": 1, "sequenceId": 4},
    ]
    selected = select_full_thesis_pdf(candidates)
    assert selected["uuid"] == "fa56a964-8e77-47bb-9d42-476b1e2ed97e"


def test_full_thesis_selection_refuses_two_nonabstract_pdfs():
    candidates = [
        {"uuid": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "name": "one.pdf"},
        {"uuid": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb", "name": "two.pdf"},
    ]
    with pytest.raises(ValueError, match="could not uniquely distinguish"):
        select_full_thesis_pdf(candidates)


def test_locked_thesis_bytes_do_not_create_a_third_effect():
    source = {"source_id": "hetherington_rauth_johnson_2020_136_pairs", "thesis_title": "The Comparative Evolution of the Floral Traits of Island Angiosperms"}
    item = {"uuid": "12345678-1234-1234-1234-123456789abc", "name": source["thesis_title"], "handle": "1807/123456"}
    bundle = {"uuid": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb", "name": "ORIGINAL"}
    bitstream = {"uuid": "cccccccc-cccc-cccc-cccc-cccccccccccc", "name": "thesis.pdf"}
    data = b"%PDF-1.7\nsynthetic fixture\n"
    lock = build_lock(source, item, bundle, bitstream, data, "https://utoronto.scholaris.ca/server/api/core/bitstreams/cccccccc-cccc-cccc-cccc-cccccccccccc/content", ["https://utoronto.scholaris.ca/server/api/discover/search/objects"])
    assert lock["sha256"]
    assert lock["source_native_136_pair_table_verified"] is False
    assert lock["third_response_shape_admitted"] is False
    assert lock["formal_cross_system_fit_opened"] is False
