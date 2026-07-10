import json

from channel_id.priority_source_access import flatten_locations, summarize_openalex


def test_openalex_locations_preserve_all_legal_routes():
    payload = {
        "id": "https://openalex.org/W1",
        "display_name": "Example floral paper",
        "publication_year": 2014,
        "open_access": {"is_oa": True, "oa_status": "green"},
        "best_oa_location": {
            "pdf_url": "https://repo.example/paper.pdf",
            "landing_page_url": "https://repo.example/item",
            "source": {"display_name": "Example Repository"},
        },
        "locations": [
            {
                "pdf_url": "https://repo.example/paper.pdf",
                "landing_page_url": "https://repo.example/item",
                "is_oa": True,
                "version": "acceptedVersion",
                "license": "cc-by",
                "source": {"display_name": "Example Repository", "type": "repository"},
            },
            {
                "pdf_url": None,
                "landing_page_url": "https://publisher.example/article",
                "is_oa": False,
                "version": "publishedVersion",
                "license": None,
                "source": {"display_name": "Publisher", "type": "journal"},
            },
        ],
    }
    locations = flatten_locations(payload)
    assert len(locations) == 2
    summary = summarize_openalex(payload)
    assert summary["access_class"] == "oa_pdf"
    assert summary["next_action"] == "download_and_inspect_legal_OA_PDF"
    assert summary["oa_pdf_location_count"] == "1"
    assert len(json.loads(summary["all_locations_json"])) == 2


def test_non_oa_source_routes_to_library_or_author():
    payload = {
        "display_name": "Closed paper",
        "publication_year": 2010,
        "open_access": {"is_oa": False, "oa_status": "closed"},
        "best_oa_location": None,
        "locations": [{
            "pdf_url": None,
            "landing_page_url": "https://publisher.example/closed",
            "is_oa": False,
            "source": {"display_name": "Publisher"},
        }],
    }
    summary = summarize_openalex(payload)
    assert summary["access_class"] == "library_or_author"
    assert summary["next_action"] == "institutional_library_or_author_request"
