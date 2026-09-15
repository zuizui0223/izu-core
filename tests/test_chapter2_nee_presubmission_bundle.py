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
        assert {
            "manuscript.md",
            "cover_letter.md",
            "reference_provenance.md",
            "author_intake.json",
            "PRESUBMISSION_MANIFEST.json",
        } <= names
        figure_pdfs = sorted(name for name in names if name.startswith("figures/") and name.endswith(".pdf"))
        figure_svgs = sorted(name for name in names if name.startswith("figures/") and name.endswith(".svg"))
        assert len(figure_pdfs) == 4
        assert len(figure_svgs) == 4
        manifest = json.loads(zf.read("PRESUBMISSION_MANIFEST.json"))
        intake = json.loads(zf.read("author_intake.json"))

    assert manifest["schema_version"] == "1.2"
    assert manifest["status"] == "PRESUBMISSION_NOT_FINAL"
    assert manifest["author_intake"] == "data/design/chapter2_nee_initial_submission_metadata.json"
    assert intake["status"] == "AUTHOR_INPUT_REQUIRED"

    blockers = "\n".join(manifest["initial_submission_blockers"])
    assert "peer-review model selection" in blockers
    assert "final author list, order, affiliations" in blockers
    assert "related-manuscript disclosure" in blockers
    assert "competing interests" in blockers
    assert "ethics statement" in blockers
    assert "LLM-use statement" in blockers

    prepublication = manifest["prepublication_pending_not_initial_submission_blockers"]
    assert "corresponding-author ORCID linkage before final acceptance" in prepublication
    assert "permanent archived code/data release DOI before publication" in prepublication
    assert "initial-submission-ready journal bundle" in manifest["finalization_rule"]
    assert "do not block initial editorial submission" in manifest["finalization_rule"]
