import importlib.util
import io
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "acquire_dryad_external_dataset.py"
SPEC = importlib.util.spec_from_file_location("dryad_external", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def xlsx_payload() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("[Content_Types].xml", "<Types/>")
        archive.writestr("xl/workbook.xml", "<workbook/>")
    return buffer.getvalue()


def test_version_sort_uses_source_version_then_resource_id():
    older = {"id": 20, "version": 1}
    newer = {"_links": {"self": {"href": "/api/v2/versions/30"}}, "version": 2}
    assert sorted([older, newer], key=MODULE.version_sort_key, reverse=True)[0] == newer
    assert MODULE.id_from_links(newer, "versions") == 30


def test_source_filename_and_file_id_are_hateoas_tolerant():
    row = {
        "path": "network data.xlsx",
        "_links": {"self": {"href": "/api/v2/files/501"}},
    }
    assert MODULE.source_filename(row) == "network data.xlsx"
    assert MODULE.id_from_links(row, "files") == 501


def test_payload_guard_rejects_html_and_accepts_structural_xlsx():
    assert MODULE.valid_payload("table.xlsx", b"<html>blocked</html>")[0] is False
    accepted, reason = MODULE.valid_payload("table.xlsx", xlsx_payload())
    assert accepted is True
    assert reason == "accepted"


def test_zip_info_matches_exact_source_filename():
    info = [
        {"filename": "a.csv", "url": "https://example/a"},
        {"filename": "b.csv", "url": "https://example/b"},
    ]
    assert MODULE.zip_info_urls(info, "b.csv") == ["https://example/b"]
