from pathlib import Path

from scripts.recover_abm_v12_heliconia_dryad import (
    FILES,
    OLE2_MAGIC,
    audit_payload,
    looks_like_legacy_xls,
    source_url,
)


def test_frozen_file_stream_ids_and_urls():
    assert [row["file_stream_id"] for row in FILES] == [37457, 37459, 37461]
    assert source_url(37457) == "https://datadryad.org/downloads/file_stream/37457"


def test_legacy_xls_magic_is_required():
    assert looks_like_legacy_xls(OLE2_MAGIC + b"x" * 100)
    assert not looks_like_legacy_xls(b"PK\x03\x04" + b"x" * 100)
    assert not looks_like_legacy_xls(b"<html>blocked</html>")


def test_plausible_legacy_xls_payload_passes_byte_structure_gate():
    spec = FILES[0]
    size = round(float(spec["reported_size_kb"]) * 1024)
    payload = OLE2_MAGIC + b"\x00" * (size - len(OLE2_MAGIC))
    audit = audit_payload(payload, spec)
    assert audit["legacy_xls_ole2_magic"] is True
    assert audit["plausible_size_vs_landing_metadata"] is True
    assert len(audit["sha256"]) == 64


def test_html_error_page_cannot_masquerade_as_xls():
    spec = FILES[0]
    payload = b"<html><body>Forbidden</body></html>"
    audit = audit_payload(payload, spec)
    assert audit["legacy_xls_ole2_magic"] is False
    assert audit["plausible_size_vs_landing_metadata"] is False
