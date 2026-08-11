import json
from pathlib import Path
import zipfile

import pytest

from scripts.acquire_southwest_pacific_pmc_support import (
    load_checked_hashes,
    load_config,
    map_expected,
    normalize_filename,
    safe_member,
    validate_office_file,
)


ROOT = Path(__file__).resolve().parents[1]


def make_minimal_ooxml(path: Path, root: str) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("[Content_Types].xml", "<Types/>")
        archive.writestr(f"{root}/placeholder.xml", "<x/>")


def test_current_config_locks_pmc_and_expected_three_files():
    config = load_config(ROOT / "config/southwest_pacific_aob_source.json")
    assert config["article_doi"] == "10.1093/aob/mcaf005"
    assert config["pmcid"] == "PMC12445859"
    assert config["europe_pmc_supplementary_url"].endswith(
        "/PMC12445859/supplementaryFiles"
    )
    assert config["expected_supplementary_files"] == [
        "mcaf005_suppl_supplementary_data_s1.xlsx",
        "mcaf005_suppl_supplementary_data_s2.xlsx",
        "mcaf005_suppl_supplementary_materials.docx",
    ]


def test_safe_member_rejects_archive_traversal():
    assert safe_member("nested/data.xlsx") == Path("nested/data.xlsx")
    with pytest.raises(ValueError, match="unsafe archive"):
        safe_member("../escape.xlsx")


def test_expected_mapping_is_case_insensitive_and_does_not_substitute(tmp_path: Path):
    a = tmp_path / "MCAF005_SUPPL_SUPPLEMENTARY_DATA_S2.XLSX"
    a.write_bytes(b"x")
    other = tmp_path / "other.xlsx"
    other.write_bytes(b"y")
    matched, unexpected = map_expected(
        [a, other], ["mcaf005_suppl_supplementary_data_s2.xlsx"]
    )
    assert matched["mcaf005_suppl_supplementary_data_s2.xlsx"] == a
    assert unexpected == [other]
    assert normalize_filename(a.name) == "mcaf005_suppl_supplementary_data_s2.xlsx"


def test_ooxml_structure_gate_distinguishes_xlsx_and_docx(tmp_path: Path):
    xlsx = tmp_path / "a.xlsx"
    docx = tmp_path / "b.docx"
    wrong = tmp_path / "wrong.xlsx"
    make_minimal_ooxml(xlsx, "xl")
    make_minimal_ooxml(docx, "word")
    make_minimal_ooxml(wrong, "word")
    assert validate_office_file(xlsx) == (True, "accepted")
    assert validate_office_file(docx) == (True, "accepted")
    assert validate_office_file(wrong) == (False, "missing_xlsx_structure")


def test_checked_source_hashes_are_loaded_without_relabeling(tmp_path: Path):
    lock = tmp_path / "source_lock.json"
    lock.write_text(
        json.dumps(
            {
                "files": {
                    "A.XLSX": {"sha256": "abc"},
                    "b.docx": {"sha256": "def"},
                }
            }
        ),
        encoding="utf-8",
    )
    assert load_checked_hashes(lock) == {"a.xlsx": "abc", "b.docx": "def"}


def test_repository_source_lock_contains_the_known_s2_checksum():
    hashes = load_checked_hashes(
        ROOT / "data/results/southwest_pacific_pairs/source_lock.json"
    )
    assert hashes["mcaf005_suppl_supplementary_data_s2.xlsx"] == (
        "452c6f83143eb17e8249faae9659386be7b162f93742c4e137921952a9b88677"
    )
