from scripts.acquire_dryad_external_dataset import looks_html, valid_payload


def test_html_guard_is_case_insensitive_for_bytes() -> None:
    assert looks_html(b"   <!DOCTYPE HTML><html>") is True
    assert looks_html(b"\n<HTML><body>") is True


def test_html_guard_accepts_non_html_binary_and_json_payloads() -> None:
    assert looks_html(b"PK\x03\x04binary") is False
    assert looks_html(b'{"data": 1}') is False


def test_valid_payload_rejects_html_without_bytes_attribute_error() -> None:
    assert valid_payload("source.csv", b"  <HTML><body>blocked</body>") == (
        False,
        "html_response",
    )
