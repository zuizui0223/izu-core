import json
import zipfile
from pathlib import Path

from scripts.build_chapter2_nee_presubmission_bundle import build


def test_nee_presubmission_bundle_is_complete_but_fail_closed(tmp_path: Path) -> None:
    out_dir = tmp_path / "bundle"
    zip_path = build(out_dir)
    assert zip_path.is_file()

    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
        assert {"manuscript.md", "cover_letter.md", "reference_provenance.md", "PRESUBMISSION_MANIFEST.json"} <= names
        figure_pdfs = sorted(name for name in names if name.startswith("figures/") and name.endswith(".pdf"))
        figure_svgs = sorted(name for name in names if name.startswith("figures/") and name.endswith(".svg"))
        assert len(figure_pdfs) == 4
        assert len(figure_svgs) == 4
        manifest = json.loads(zf.read("PRESUBMISSION_MANIFEST.json"))

    assert manifest["status"] == "PRESUBMISSION_NOT_FINAL"
    assert "final author list and order" in manifest["blocking_author_controlled_fields"]
    assert "corresponding-author designation" in manifest["blocking_author_controlled_fields"]
    assert "ORCID(s)" in manifest["blocking_author_controlled_fields"]
    assert manifest["blocking_archive_field"] == ["permanent archived code/data release DOI"]
    assert "final journal submission bundle" in manifest["finalization_rule"]
