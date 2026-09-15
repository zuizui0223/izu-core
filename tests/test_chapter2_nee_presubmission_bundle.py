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
            "PRESUBMISSION_MANIFEST.json",
            "provenance/all_source_leave_one_out.json",
            "provenance/source_robustness_challenge_closure.json",
        } <= names
        figure_pdfs = sorted(name for name in names if name.startswith("figures/") and name.endswith(".pdf"))
        figure_svgs = sorted(name for name in names if name.startswith("figures/") and name.endswith(".svg"))
        assert len(figure_pdfs) == 4
        assert len(figure_svgs) == 4
        manifest = json.loads(zf.read("PRESUBMISSION_MANIFEST.json"))
        loo = json.loads(zf.read("provenance/all_source_leave_one_out.json"))
        challenge = json.loads(zf.read("provenance/source_robustness_challenge_closure.json"))

    assert manifest["status"] == "PRESUBMISSION_NOT_FINAL"
    assert manifest["schema_version"] == "1.2"
    assert manifest["analysis_provenance"]["all_source_leave_one_out"].endswith(
        "chapter2_natural_regime_six_source_all_loo_diagnostic_20260915.json"
    )
    assert manifest["analysis_provenance"]["source_robustness_challenge_closure"].endswith(
        "chapter2_natural_regime_source_robustness_challenge_closure_20260915.json"
    )
    assert loo["status"] == "post_promotion_diagnostic_not_route_redefinition"
    assert challenge["status"] == "challenge_closed_no_new_source_admitted"

    blockers = manifest["initial_submission_blockers"]
    assert "final author list and order" in blockers
    assert "corresponding-author designation" in blockers
    assert "all-author approval" in blockers

    prepublication = manifest["prepublication_pending_not_initial_submission_blockers"]
    assert "corresponding-author ORCID linkage before final acceptance" in prepublication
    assert "permanent archived code/data release DOI before publication" in prepublication
    assert "initial-submission-ready journal bundle" in manifest["finalization_rule"]
    assert "do not block initial editorial submission" in manifest["finalization_rule"]
