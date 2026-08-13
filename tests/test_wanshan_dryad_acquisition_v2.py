import importlib.util
import io
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "acquire_wanshan_yongxing_dryad_v2.py"
SPEC = importlib.util.spec_from_file_location("wanshan_acquire_v2", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def fake_xlsx() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_STORED) as archive:
        archive.writestr("[Content_Types].xml", "<Types/>" + " " * 1200)
        archive.writestr("xl/workbook.xml", "<workbook/>" + " " * 1200)
    return buffer.getvalue()


def test_version_ids_resolve_from_hateoas_links():
    metadata = {
        "_embedded": {
            "stash:versions": [
                {"_links": {"self": {"href": "/api/v2/versions/41872"}}},
                {"_links": {"self": {"href": "/api/v2/versions/42101"}}},
            ]
        }
    }
    assert MODULE.version_ids(metadata) == [42101, 41872]


def test_file_ids_resolve_from_file_links():
    listing = {
        "_embedded": {
            "stash:files": [
                {
                    "path": "network.xlsx",
                    "_links": {"self": {"href": "/api/v2/files/444/download"}},
                }
            ]
        }
    }
    assert MODULE.file_ids(listing, "target.xlsx") == [444]


def test_extract_workbook_accepts_direct_xlsx_and_dataset_zip():
    workbook = fake_xlsx()
    direct = MODULE.extract_workbook(workbook, "target.xlsx")
    assert direct is not None
    assert direct[0] == workbook
    assert direct[1] == "direct_xlsx"

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("nested/target.xlsx", workbook)
        archive.writestr("README.txt", "source archive")
    nested = MODULE.extract_workbook(buffer.getvalue(), "target.xlsx")
    assert nested is not None
    assert nested[0] == workbook
    assert nested[1] == "dataset_zip"
    assert nested[2] == ["nested/target.xlsx"]
