import importlib.util
import io
import urllib.parse
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "acquire_galapagos_dataone.py"
SPEC = importlib.util.spec_from_file_location("galapagos_dataone", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def make_zip() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("network.csv", "plant,pollinator,weight\nA,B,1\n")
    return buffer.getvalue()


def test_doi_normalization_and_variants_are_exact():
    assert MODULE.canonical_doi("https://doi.org/10.5061/DRYAD.0C3CN5F/") == (
        "10.5061/dryad.0c3cn5f"
    )
    assert MODULE.doi_variants("doi:10.5061/dryad.0c3cn5f") == (
        "10.5061/dryad.0c3cn5f",
        "doi:10.5061/dryad.0c3cn5f",
        "https://doi.org/10.5061/dryad.0c3cn5f",
    )


def test_query_urls_request_json_and_include_doi_locked_fields():
    urls = MODULE.query_urls(
        "https://cn.dataone.org/cn/v2", "10.5061/dryad.0c3cn5f"
    )
    assert len(urls) == 2
    parsed = urllib.parse.urlsplit(urls[0])
    params = urllib.parse.parse_qs(parsed.query)
    assert parsed.path.endswith("/query/solr/")
    assert params["wt"] == ["json"]
    assert "id:" in params["q"][0]
    assert "seriesId:" in params["q"][0]
    assert "10.5061/dryad.0c3cn5f" in params["q"][0]


def test_solr_docs_and_document_doi_lock():
    payload = {
        "response": {
            "docs": [
                {
                    "id": "urn:uuid:metadata",
                    "seriesId": "doi:10.5061/dryad.0c3cn5f",
                    "title": "Galapagos metadata",
                },
                {"id": "unrelated", "title": "Other data"},
            ]
        }
    }
    docs = MODULE.solr_docs(payload)
    assert len(docs) == 2
    assert MODULE.document_matches_doi(docs[0], "10.5061/dryad.0c3cn5f")
    assert not MODULE.document_matches_doi(
        docs[1], "10.5061/dryad.0c3cn5f"
    )


def test_metadata_objects_are_not_relabelled_as_data():
    metadata = {
        "id": "urn:uuid:metadata",
        "formatType": "METADATA",
        "formatId": "eml://ecoinformatics.org/eml-2.2.0",
        "size": 1200,
    }
    resource_map = {
        "id": "urn:uuid:ore",
        "formatType": "RESOURCE",
        "formatId": "http://www.openarchives.org/ore/terms",
        "size": 900,
    }
    data = {
        "id": "urn:uuid:data",
        "formatType": "DATA",
        "formatId": "application/zip",
        "fileName": "data_galapagos_islands.zip",
        "size": 14001,
    }
    assert not MODULE.likely_data_document(metadata)
    assert not MODULE.likely_data_document(resource_map)
    assert MODULE.likely_data_document(data)


def test_filename_and_payload_guards_reject_html_and_invalid_zip():
    assert MODULE.safe_name("https://example.org/path/data galápagos.zip") == (
        "data gal_pagos.zip"
    )
    assert MODULE.valid_payload("data.zip", b"<html>blocked</html>") == (
        False,
        "html_or_error_xml_response",
    )
    assert MODULE.valid_payload("data.zip", b"not a zip") == (
        False,
        "invalid_zip",
    )
    assert MODULE.valid_payload("data.zip", make_zip()) == (True, "accepted")


def test_related_identifiers_and_deduplication_preserve_package_links():
    document = {
        "id": "metadata-id",
        "seriesId": "doi:10.5061/dryad.0c3cn5f",
        "resourceMap": ["resource-map-id"],
        "documents": ["data-id"],
    }
    identifiers = MODULE.related_identifiers(document)
    assert identifiers == {
        "metadata-id",
        "doi:10.5061/dryad.0c3cn5f",
        "resource-map-id",
        "data-id",
    }
    deduplicated = MODULE.deduplicate_documents(
        [document, dict(document), {"id": "data-id", "formatType": "DATA"}]
    )
    assert len(deduplicated) == 2
