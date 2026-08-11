import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "southwest_pacific_pmc",
    ROOT / "scripts" / "acquire_southwest_pacific_pmc_support.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_safe_member_rejects_archive_traversal():
    assert MODULE.safe_member("nested/file.xlsx") == Path("nested/file.xlsx")
    with pytest.raises(ValueError, match="unsafe archive"):
        MODULE.safe_member("../escape.xlsx")


def test_expected_filename_mapping_is_case_insensitive_and_does_not_guess(tmp_path: Path):
    a = tmp_path / "MCAF005_SUPPL_SUPPLEMENTARY_DATA_S1.XLSX"
    b = tmp_path / "mcaf005_suppl_supplementary_data_s2.xlsx"
    c = tmp_path / "unrelated.xlsx"
    for path in (a, b, c):
        path.write_bytes(b"x")
    expected = [
        "mcaf005_suppl_supplementary_data_s1.xlsx",
        "mcaf005_suppl_supplementary_data_s2.xlsx",
        "mcaf005_suppl_supplementary_materials.docx",
    ]
    matched, unexpected = MODULE.map_expected([a, b, c], expected)
    assert set(matched) == set(expected[:2])
    assert unexpected == [c]


def test_repository_config_locks_same_article_and_three_files():
    config = MODULE.load_config(ROOT / "config" / "southwest_pacific_aob_source.json")
    assert config["article_doi"] == "10.1093/aob/mcaf005"
    assert config["pmcid"] == "PMC12445859"
    assert config["europe_pmc_supplementary_url"].endswith(
        "/PMC12445859/supplementaryFiles"
    )
    assert config["analysis_source"]["filename"] == (
        "mcaf005_suppl_supplementary_data_s2.xlsx"
    )
    assert config["analysis_source"]["sheet"] == "Flower dataframe"
    assert len(config["expected_supplementary_files"]) == 3
