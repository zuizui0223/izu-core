import importlib.util
import io
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "acquire_oup_supplementary_data_v2.py"
SPEC = importlib.util.spec_from_file_location("oup_supplement_v2", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def office_zip() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("[Content_Types].xml", "<Types/>")
        archive.writestr("xl/workbook.xml", "<workbook/>")
    return buffer.getvalue()


def test_html_link_discovery_resolves_relative_supplement_paths():
    html = b'''<html><body>
      <a href="/aob/article-supplement/123/file.xlsx">Supplementary data</a>
      <a href="article.pdf">PDF</a>
    </body></html>'''
    links = MODULE.parse_links("https://academic.oup.com/aob/article/1", html)
    supplement = next(row for row in links if "file.xlsx" in row["url"])
    assert supplement["url"] == "https://academic.oup.com/aob/article-supplement/123/file.xlsx"
    assert MODULE.is_candidate_link(supplement["url"], supplement["text"]) is True
    assert MODULE.is_candidate_link("https://example.org/article.pdf", "PDF") is False


def test_payload_guard_rejects_html_and_accepts_office_zip():
    assert MODULE.valid_data_payload("data.xlsx", b"<html>blocked</html>", {"Content-Type": "text/html"})[0] is False
    accepted, reason = MODULE.valid_data_payload(
        "data.xlsx",
        office_zip(),
        {"Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"},
    )
    assert accepted is True
    assert reason == "accepted"


def test_content_disposition_filename_and_sanitisation():
    headers = {"Content-Disposition": "attachment; filename*=UTF-8''pair%20data.xlsx"}
    assert MODULE.content_disposition_filename(headers) == "pair data.xlsx"
    assert MODULE.safe_filename("https://example.org/download", headers, 1) == "pair data.xlsx"


def test_data_candidate_hints_admit_supplement_page_without_promoting_pdf():
    assert MODULE.is_candidate_link("https://example.org/supplementary-data", "Supplementary data") is True
    assert MODULE.is_candidate_link("https://example.org/main/article", "Main article") is False
