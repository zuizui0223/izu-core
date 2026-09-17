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
        # Keep both the readable supplement and its exact frozen analysis receipts in the submission archive.
        assert {
            "manuscript.md",
            "cover_letter.md",
            "reference_provenance.md",
            "supplementary_source_leverage.md",
            "author_intake.json",
            "provenance/all_source_leave_one_out.json",
            "provenance/source_robustness_challenge_closure.json",
            "PRESUBMISSION_MANIFEST.json",
        } <= names
        figure_pdfs = sorted(name for name in names if name.startswith("figures/") and name.endswith(".pdf"))
        figure_svgs = sorted(name for name in names if name.startswith("figures/") and name.endswith(".svg"))
        assert len(figure_pdfs) == 4
        assert len(figure_svgs) == 4
        manifest = json.loads(zf.read("PRESUBMISSION_MANIFEST.json"))
        intake = json.loads(zf.read("author_intake.json"))
        supplement = zf.read("supplementary_source_leverage.md").decode("utf-8")
        loo = json.loads(zf.read("provenance/all_source_leave_one_out.json"))
        challenge = json.loads(zf.read("provenance/source_robustness_challenge_closure.json"))

    assert manifest["schema_version"] == "1.4"
    assert manifest["status"] == "PRESUBMISSION_NOT_FINAL"
    assert manifest["author_intake"] == "data/design/chapter2_nee_initial_submission_metadata.json"
    assert manifest["source_leverage_supplement"] == "docs/CHAPTER2_NEE_SUPPLEMENTARY_SOURCE_LEVERAGE_20260915.md"
    assert manifest["analysis_provenance"]["all_source_leave_one_out"].endswith(
        "chapter2_natural_regime_six_source_all_loo_diagnostic_20260915.json"
    )
    assert manifest["analysis_provenance"]["source_robustness_challenge_closure"].endswith(
        "chapter2_natural_regime_source_robustness_challenge_closure_20260915.json"
    )
    assert loo["status"] == "post_promotion_diagnostic_not_route_redefinition"
    assert challenge["status"] == "CLOSED_UNSUCCESSFUL_NO_ADDITIONAL_SOURCE_COORDINATES_OPENED"
    assert challenge["coordinates_opened_for_reopened_candidates"] == 0
    assert challenge["england_dependence_removed"] is False
    assert intake["status"] == "AUTHOR_INPUT_REQUIRED"
    assert "england step reduces synchrony dispersion" in supplement.lower()
    assert "all four candidates closed before d1 or phi extraction" in supplement.lower()

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
