from __future__ import annotations

import argparse
import json
import tempfile
import zipfile
from pathlib import Path

from scripts.build_island_ecology_review_archive import build_archive as build_review_archive
from scripts.build_island_ecology_submission_metadata import (
    load_metadata,
    render_cover_letter,
    render_significance_statement,
    render_submission_statements,
    render_title_page,
    validate_metadata,
)
from scripts.generate_chapter2_unified_model3_figures import build_figures
from scripts.render_oikos_submission_rtf import (
    render_manuscript_rtf,
    render_plain_text_rtf,
    render_supporting_information_rtf,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_METADATA = ROOT / "data/design/island_ecology_submission_metadata_template.json"
DEFAULT_OUTPUT = ROOT / "dist/chapter2_oikos_submission_bundle.zip"
UNIFIED_MODEL3_LOCK = ROOT / "data/design/chapter2_unified_model3_lock_20260927.json"
UNIFICATION_RESULT = ROOT / "data/results/model3_unified_reduction_audit_frozen_20260927.json"
PROSPECTIVE_BRIDGE_RESULT = ROOT / "data/results/model3_ch2_bridge_prospective_frozen_20260927.json"
SOURCE_MANUSCRIPT = "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
SUBMISSION_MANUSCRIPT_NAME = "MANUSCRIPT.rtf"
SUBMISSION_SI_NAME = "SUPPORTING_INFORMATION.rtf"
TITLE_PAGE_NAME = "TITLE_PAGE.rtf"
COVER_LETTER_NAME = "COVER_LETTER.rtf"
SIGNIFICANCE_NAME = "SIGNIFICANCE_STATEMENT.rtf"
STATEMENTS_NAME = "SUBMISSION_STATEMENTS.rtf"
ACTIVE_SUBMISSION_MANIFEST = "data/design/chapter2_oikos_submission_manifest_20260927.json"
RELATIONAL_FIGURE_INPUTS_ARCNAME = "data/results/chapter2_unified_model3_figure_inputs_20260927.json"
RELATIONAL_FIGURE_INPUTS = ROOT / RELATIONAL_FIGURE_INPUTS_ARCNAME

STATIC_SUBMISSION_FILES = (
    "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_IZU_EMPIRICAL_APPENDIX_20260827.md",
    "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_REFERENCE_LEDGER_20260827.md",
    "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_TABLES_20260827.md",
    "docs/CHAPTER2_CANONICAL_STORY_20260927.md",
    "docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md",
    "docs/CHAPTER2_MODEL_UNIFICATION_DECISION_20260927.md",
    "docs/MODEL3_CH2_BRIDGE_PROSPECTIVE_RESULTS_20260927.md",
    "data/results/model3_ch2_bridge_prospective_frozen_20260927.json",
    "docs/CHAPTER2_UNIFIED_MODEL3_REAL_ISLAND_PROJECTION_20260927.md",
    "docs/CHAPTER1_CHAPTER2_CANONICAL_BRIDGE_20260927.md",
    "docs/CHAPTER2_THREE_RESULT_NARRATIVE_LOCK_20260908.md",
    "docs/CHAPTER2_RELATIONAL_ROBUSTNESS_CORRECTION_20260831.md",
    "data/design/chapter2_unified_model3_lock_20260927.json",
    "data/design/model3_unified_reduction_audit_20260927.json",
    "data/results/model3_unified_reduction_audit_frozen_20260927.json",
    "data/results/chapter2_unified_model3_real_island_projection_20260927.json",
    "docs/CHAPTER2_SUPPORTING_INFORMATION_S19_REALIZED_RICHNESS_20260907.md",
    "docs/CHAPTER2_SUPPORTING_TABLE_S9_REALIZED_RICHNESS_20260907.md",
    "data/design/chapter2_relational_robustness_audit_freeze_20260831.json",
    "data/design/chapter2_realized_richness_matching_freeze_20260907.json",
    "data/results/chapter2_relational_robustness_audit_frozen_20260831.json",
    "data/results/chapter2_realized_richness_matching_decision_20260907.json",
    ACTIVE_SUBMISSION_MANIFEST,
)


def validate_scientific_gate() -> dict:
    if not UNIFIED_MODEL3_LOCK.exists():
        raise ValueError("unified Model 3 scientific lock is missing; refuse to build a submission bundle")
    try:
        gate = json.loads(UNIFIED_MODEL3_LOCK.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("unified Model 3 scientific lock is unreadable; refuse to build a submission bundle") from exc

    if gate.get("status") != "active_chapter2_unified_model3_bridge_complete":
        raise ValueError("Chapter 2 unified Model 3 bridge-complete lock is not active")

    audit = gate.get("unification_audit", {})
    if audit.get("conclusion") != "success":
        raise ValueError("Model 3 unification audit is not successful")
    if audit.get("decision") != "model2_not_required_as_active_scientific_model_or_control_gate":
        raise ValueError("Chapter 2 final model-unification decision is not locked")
    if audit.get("scope", {}).get("not_answered"):
        raise ValueError("Chapter 2 unification audit still has unanswered internal control gates")

    if not UNIFICATION_RESULT.exists():
        raise ValueError("Model 3 unification result is missing")
    reduction = json.loads(UNIFICATION_RESULT.read_text(encoding="utf-8"))
    if reduction.get("decision") != "model2_not_required_as_independent_mechanistic_model":
        raise ValueError("Frozen controlled-composition reduction result changed")

    bridge = gate.get("prospective_bridge", {})
    if bridge.get("status") != "complete" or bridge.get("cases_verified") != 24576:
        raise ValueError("Model 3 prospective bridge is not complete")
    if not PROSPECTIVE_BRIDGE_RESULT.exists():
        raise ValueError("Model 3 prospective bridge result is missing")
    bridge_result = json.loads(PROSPECTIVE_BRIDGE_RESULT.read_text(encoding="utf-8"))
    if bridge_result.get("status") != "frozen_complete_prospective_model3_ch2_bridge":
        raise ValueError("Model 3 prospective bridge result is not frozen complete")
    if bridge_result.get("provenance", {}).get("cases_verified") != 24576:
        raise ValueError("Model 3 prospective bridge denominator changed")

    state = gate.get("submission_state", {})
    if state.get("original_chapter2_controls_closed") is not True:
        raise ValueError("original Chapter 2 controls are not closed")
    if state.get("new_field_data_required") is not False:
        raise ValueError("Chapter 2 field-data completion boundary changed")
    return gate

def _write_rtf(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")
    rendered = path.read_text(encoding="utf-8")
    if not rendered.startswith("{\\rtf1"):
        raise ValueError(f"Oikos upload file is not RTF: {path.name}")


def build_submission_bundle(metadata_path: Path, output: Path) -> Path:
    gate = validate_scientific_gate()

    metadata = load_metadata(metadata_path)
    errors = validate_metadata(metadata)
    if errors:
        raise ValueError("submission metadata incomplete:\n- " + "\n- ".join(errors))
    if metadata.get("journal") != "Oikos" or metadata.get("article_type") != "Research Paper":
        raise ValueError("active submission metadata must route to Oikos Research Paper")

    if not (ROOT / SOURCE_MANUSCRIPT).exists():
        raise FileNotFoundError(SOURCE_MANUSCRIPT)
    for rel in STATIC_SUBMISSION_FILES:
        if not (ROOT / rel).exists():
            raise FileNotFoundError(rel)

    figure_payload = build_figures()
    figure_files = tuple(figure_payload["figure_outputs"])
    for rel in figure_files:
        if not (ROOT / rel).exists():
            raise FileNotFoundError(rel)
    if not RELATIONAL_FIGURE_INPUTS.exists():
        raise FileNotFoundError(RELATIONAL_FIGURE_INPUTS)

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp_name:
        tmp = Path(tmp_name)
        manuscript = tmp / SUBMISSION_MANUSCRIPT_NAME
        supporting_information = tmp / SUBMISSION_SI_NAME
        title_page = tmp / TITLE_PAGE_NAME
        cover_letter = tmp / COVER_LETTER_NAME
        significance = tmp / SIGNIFICANCE_NAME
        statements = tmp / STATEMENTS_NAME
        review_archive = tmp / "anonymous_review_archive.zip"

        _write_rtf(manuscript, render_manuscript_rtf())
        _write_rtf(supporting_information, render_supporting_information_rtf())
        _write_rtf(title_page, render_plain_text_rtf(render_title_page(metadata)))
        _write_rtf(cover_letter, render_plain_text_rtf(render_cover_letter(metadata)))
        _write_rtf(significance, render_plain_text_rtf(render_significance_statement(metadata)))
        _write_rtf(statements, render_plain_text_rtf(render_submission_statements(metadata)))
        build_review_archive(review_archive)

        main_rtf = manuscript.read_text(encoding="utf-8")
        lower_main = main_rtf.lower()
        for control in ("\\sl480\\slmult1", "\\linemod1", "\\linecont", "fldinst PAGE", "\\page"):
            if control not in main_rtf:
                raise ValueError(f"Oikos manuscript formatting control missing: {control}")
        required_story = (
            "fixed-state reproductive assay",
            "deterministic genotype-density counterpart",
            "finite-population abm",
            "real islands occupy different stages of the same response architecture",
            "all eight shared oshima-to-post targets",
            "the main natural-data gap",
        )
        missing_story = [token for token in required_story if token not in lower_main]
        if missing_story:
            raise ValueError(f"Oikos manuscript lost the mechanism-mainline narrative: {missing_story}")
        stale_story = (
            "result 1—mechanistic prediction",
            "result 2—real-world exposure",
            "result 3—biological consequence",
            "figure 1. three-result inference chain",
        )
        leaked = [token for token in stale_story if token in lower_main]
        if leaked:
            raise ValueError(f"historical three-result narrative leaked into active manuscript: {leaked}")

        bundle_manifest = {
            "journal": metadata["journal"],
            "article_type": metadata["article_type"],
            "scientific_state": "unified_model3_nested_ecoevolutionary_response_with_real_island_layer_confrontation",
            "manuscript_state": "active_20260927_unified_model3_rendered_to_oikos_rtf_submission",
            "mechanism_mainline_narrative": True,
            "three_result_narrative": False,
            "identifiability_coequal_study_objective": False,
            "field_e3_e4_required_for_submission": False,
            "source_manuscript": SOURCE_MANUSCRIPT,
            "submission_manuscript": SUBMISSION_MANUSCRIPT_NAME,
            "submission_supporting_information": SUBMISSION_SI_NAME,
            "active_submission_manifest": ACTIVE_SUBMISSION_MANIFEST,
            "author_metadata_source": metadata_path.name,
            "review_archive_anonymous": True,
            "oikos_upload_format": "RTF",
            "main_text_single_column": True,
            "main_text_double_spaced": True,
            "main_text_continuous_line_numbers": True,
            "main_text_page_numbers": True,
            "introduction_forced_to_page_two": True,
            "main_text_reference_list_included": True,
            "main_text_reference_scope": "active_references_for_mechanism_mainline_and_empirical_claim_boundary",
            "main_text_reference_audit_metadata_excluded": True,
            "world_descriptive_research_entries": 42,
            "world_descriptive_exact_geographic_labels": 37,
            "formal_identifiability_research_entries": 25,
            "formal_full_contracts": "0_of_25",
            "unified_model3_reduction_audit_complete": True,
            "real_island_abc_projection_included": True,
            "legacy_realized_richness_reframe_retained_in_si": True,
            "realized_richness_mean_geometry": "all_positive_in_6_of_6_matching_seeds",
            "realized_richness_mixed_individual_realizations": "51_to_65_of_96",
            "realized_richness_nonadditivity_fraction": "0.4272_to_0.4851",
            "system_size_rank_crossover": {
                "k_values": [1, 2, 4, 8, 16],
                "median_starting_share_percent": [2.55, 10.33, 27.33, 42.52, 55.84],
                "median_community_share_percent": [72.98, 48.03, 23.52, 18.26, 12.72],
                "starting_exceeds_community_from_k4": "6_of_6_seeds",
                "mixed_at_k16": "28_to_42_of_96",
                "natural_threshold_claimed": False,
            },
            "izu_e3_e4_status": "future_optional_A_C_falsification_not_completion_gate",
            "chapter3_direct_phenotype_used_as_validation": False,
            "corresponding_author_orcid_required": True,
            "planned_public_repository_named": True,
            "significance_prior_work_context_included": True,
            "submission_manuscript_internal_thesis_language_removed_fail_closed": True,
            "supporting_information_superseded_nonadditivity_wording_removed_fail_closed": True,
            "oikos_significance_statement_included": True,
            "oikos_submission_statements_included": True,
            "oikos_data_code_ready_for_first_submission": True,
            "figures_regenerated_from_frozen_gate": True,
            "model_gate": gate.get("status"),
            "files": [
                SUBMISSION_MANUSCRIPT_NAME,
                SUBMISSION_SI_NAME,
                *STATIC_SUBMISSION_FILES,
                *figure_files,
                RELATIONAL_FIGURE_INPUTS_ARCNAME,
                TITLE_PAGE_NAME,
                COVER_LETTER_NAME,
                SIGNIFICANCE_NAME,
                STATEMENTS_NAME,
                "anonymous_review_archive.zip",
            ],
            "boundary": (
                "The submission is organized around one nested Model 3: fixed-state reproductive selection, deterministic genotype-density inheritance, finite-population ABM realization, and history/context interventions. "
                "The prospective reduction audit shows that composition x starting-state branch capacity precedes demographic stochasticity and can persist without demographic sampling under controlled compositions. "
                "Finite-history mixed labels in the isolation bridge are descriptive, repeat/threshold/numerical-representation sensitive, and are not estimates of stable latent branch prevalence. "
                "Real-island evidence is confronted by A/B/C layer rather than fitted to synthetic parameter cells; A and C have multiple source-locked examples, while inherited longitudinal B remains the main gap. "
                "Legacy exact-richness, synthetic-k and response-rule analyses are retained as Supporting Information robustness, and no synthetic coordinate is transferred to nature."
            ),        }

        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for generated in (manuscript, supporting_information, title_page, cover_letter, significance, statements, review_archive):
                archive.write(generated, arcname=generated.name)
            for rel in STATIC_SUBMISSION_FILES:
                archive.write(ROOT / rel, arcname=rel)
            for rel in figure_files:
                archive.write(ROOT / rel, arcname=rel)
            archive.write(RELATIONAL_FIGURE_INPUTS, arcname=RELATIONAL_FIGURE_INPUTS_ARCNAME)
            archive.writestr(
                "SUBMISSION_BUNDLE_MANIFEST.json",
                json.dumps(bundle_manifest, indent=2, ensure_ascii=False) + "\n",
            )
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    path = build_submission_bundle(args.metadata, args.output)
    print(path)


if __name__ == "__main__":
    main()
