from scripts.audit_hetherington_dspace_bitstreams import build_inventory
from scripts.screen_hetherington_thesis_source_table import audit_supplemental_a2


def test_supplemental_a2_identity_table_does_not_become_numeric_table():
    pages = [
        "Front matter",
        (
            "Supplemental Table A.2. Island-mainland pairs of taxa. "
            "Family Endemic Island Taxa Mainland Sister Taxa Data Source Reference "
            "Asteraceae Islandus example Mainlandus example Herbarium Smith 2001"
        ),
        "Literature cited in Table A.2 Smith 2001",
    ]
    result = audit_supplemental_a2(pages)
    assert result["found"] is True
    assert result["pair_identity_table_verified"] is True
    assert result["numeric_flower_size_columns_found"] is False


def test_bitstream_inventory_excludes_readme_and_finds_explicit_data_attachment():
    lock = {
        "item_handle": "1807/96116",
        "item_uuid": "4fe4945e-d284-4b0d-b306-97c2a02d51ad",
        "original_bundle_uuid": "e7584ca9-97fb-47bf-a6b1-e8aeee5e0ba9",
    }
    payload = {
        "_embedded": {
            "bitstreams": [
                {
                    "uuid": "61628fd5-25ed-4fa9-b869-593b4a71b8eb",
                    "name": "Hetherington-Rauth_Molly_C_201906_MSc_thesis_expandedabstract.pdf",
                    "sequenceId": 3,
                    "sizeBytes": 50571,
                },
                {
                    "uuid": "fa56a964-8e77-47bb-9d42-476b1e2ed97e",
                    "name": "Hetherington-Rauth_Molly_C_201906_MSc_thesis.pdf",
                    "sequenceId": 4,
                    "sizeBytes": 175645192,
                },
                {
                    "uuid": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                    "name": "README.txt",
                    "sequenceId": 5,
                    "sizeBytes": 100,
                },
                {
                    "uuid": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
                    "name": "floral_trait_data.csv",
                    "sequenceId": 6,
                    "sizeBytes": 5000,
                },
            ]
        }
    }
    result = build_inventory(lock, payload, "https://example.invalid/bitstreams")
    assert result["n_full_thesis_pdfs"] == 1
    assert result["n_expanded_abstract_pdfs"] == 1
    assert result["n_tabular_data_attachments"] == 1
    assert result["tabular_data_attachments"][0]["name"] == "floral_trait_data.csv"
    assert result["separate_numeric_136_pair_attachment_verified"] is False
