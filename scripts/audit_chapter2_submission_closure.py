from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.build_island_ecology_submission_bundle import (
    ACTIVE_SUBMISSION_MANIFEST,
    ROOT,
    SOURCE_MANUSCRIPT,
    STATIC_SUBMISSION_FILES,
    validate_scientific_gate,
)
from scripts.build_island_ecology_submission_metadata import load_metadata, validate_metadata
from scripts.render_oikos_submission_rtf import render_manuscript_rtf, render_supporting_information_rtf

DEFAULT_METADATA = ROOT / "data/design/island_ecology_submission_metadata_template.json"
DEFAULT_OUTPUT = ROOT / "data/results/chapter2_submission_closure_audit_20260927.json"
UNIFIED_LOCK = ROOT / "data/design/chapter2_unified_model3_lock_20260927.json"

REQUIRED_HUMAN_INPUT_CATEGORIES = [
    "final_ordered_author_list_and_affiliations",
    "corresponding_author_selection_email_postal_address_and_orcid",
    "significance_prior_work_context",
    "acknowledgements",
    "funding",
    "inclusion_statement",
    "conflict_of_interest",
    "ethics_statement_author_confirmation",
    "explicit_submission_declarations",
]

ALLOWED_METADATA_ERROR_PREFIXES = (
    "authors",
    "corresponding_author_index",
    "corresponding author ",
    "significance_prior_work_context",
    "acknowledgements",
    "funding",
    "inclusion_statement",
    "conflict_of_interest",
    "ethics_statement_confirmed",
    "submission_declarations.",
)


def _rtf_preflight(text: str, *, main_text: bool) -> list[str]:
    errors: list[str] = []
    if not text.startswith("{\\rtf1"):
        errors.append("rendered output is not RTF")
    if main_text:
        for control in ("\\sl480\\slmult1", "\\linemod1", "\\linecont", "fldinst PAGE", "\\page"):
            if control not in text:
                errors.append(f"main-text RTF formatting control missing: {control}")
        lower = text.lower()
        for token in (
            "fixed-state reproductive assay",
            "deterministic genotype-density counterpart",
            "finite-population abm",
            "annual response-blind richness matching",
            "pooling eight independent visitor histories",
            "increasing plant capacity",
            "real islands occupy different stages of the same response architecture",
            "all eight shared oshima-to-post targets",
            "the main natural-data gap",
            "21/25",
            "2/25",
            "0/25",
        ):
            if token not in lower:
                errors.append(f"main-text unified-Model-3 token missing: {token}")
        for stale in (
            "figure 1. three-result inference chain",
            "result 1—mechanistic prediction",
            "result 2—real-world exposure",
            "result 3—biological consequence",
        ):
            if stale in lower:
                errors.append(f"historical three-result token leaked into main text: {stale}")
    return errors


def build_audit(metadata_path: Path = DEFAULT_METADATA) -> dict:
    metadata = load_metadata(metadata_path)
    metadata_errors = validate_metadata(metadata)

    nonmetadata_errors: list[str] = []
    try:
        gate = validate_scientific_gate()
    except Exception as exc:
        gate = {}
        nonmetadata_errors.append(f"scientific gate: {exc}")

    required_paths = [SOURCE_MANUSCRIPT, *STATIC_SUBMISSION_FILES]
    missing_paths = [rel for rel in required_paths if not (ROOT / rel).exists()]
    nonmetadata_errors.extend(f"missing required submission surface: {rel}" for rel in missing_paths)

    try:
        lock = json.loads(UNIFIED_LOCK.read_text(encoding="utf-8"))
    except Exception as exc:
        lock = {}
        nonmetadata_errors.append(f"unified Model 3 lock: {exc}")

    if lock:
        if lock.get("status") != "active_chapter2_unified_model3_bridge_complete":
            nonmetadata_errors.append("unified Model 3 bridge-complete lock is not active")
        if lock.get("submission_state", {}).get("new_field_data_required") is not False:
            nonmetadata_errors.append("unified lock incorrectly restores new focal field data as required")
        if lock.get("unification_audit", {}).get("decision") != "model2_not_required_as_active_scientific_model_or_control_gate":
            nonmetadata_errors.append("unified lock lost the final Model 2 disposition")
        if lock.get("prospective_bridge", {}).get("status") != "complete":
            nonmetadata_errors.append("unified lock lost the completed prospective bridge")

    manifest_path = ROOT / ACTIVE_SUBMISSION_MANIFEST
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        manifest = {}
        nonmetadata_errors.append(f"active submission manifest: {exc}")

    package_blockers: list[str] = []
    if manifest:
        if manifest.get("active_manuscript") != SOURCE_MANUSCRIPT:
            nonmetadata_errors.append("active manifest manuscript does not match bundle source manuscript")
        if manifest.get("submission_ready") is not False:
            nonmetadata_errors.append("active manifest must remain submission_ready=false before final QA and author metadata")
        if manifest.get("scientific_state") != "unified_model3_bridge_complete_with_real_island_layer_confrontation":
            nonmetadata_errors.append("active manifest lost the bridge-complete unified Model 3 scientific state")
        if manifest.get("narrative_lock") != "docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md":
            nonmetadata_errors.append("active manifest lost the mechanism-mainline narrative lock")
        if manifest.get("real_island_confrontation", {}).get("principal_gap") != "B_inherited_longitudinal_response_under_measured_visitor_regime":
            nonmetadata_errors.append("active manifest lost the inherited-longitudinal B-layer gap")
        boundary = manifest.get("formal_natural_evidence_boundary", {})
        if boundary.get("complete_A_to_B_to_C_contracts") != "0_of_25":
            nonmetadata_errors.append("active manifest lost the frozen 0/25 A-to-B-to-C boundary")
        state = manifest.get("current_submission_state", {})
        if state.get("scientific_question_closed") is not True:
            nonmetadata_errors.append("active manifest lost scientific closure")
        if state.get("original_chapter2_controls_closed") is not True:
            nonmetadata_errors.append("active manifest lost original-Chapter-2 control closure")
        if state.get("new_field_data_required") is not False:
            nonmetadata_errors.append("active manifest incorrectly restores new focal field data")
        if manifest.get("prospective_bridge", {}).get("status") != "complete":
            nonmetadata_errors.append("active manifest lost completed prospective bridge")
        if state.get("figures_need_regeneration") is True:
            package_blockers.append("regenerate unified Model 3 main figures")
        if state.get("supporting_information_rewrite_in_progress") is True:
            package_blockers.append("finish and validate unified Supporting Information")
        if state.get("renderers_and_fail_closed_audits_need_final_pass") is True:
            package_blockers.append("pass unified renderers and fail-closed submission audits")

    try:
        manuscript_rtf = render_manuscript_rtf()
        nonmetadata_errors.extend(_rtf_preflight(manuscript_rtf, main_text=True))
    except Exception as exc:
        nonmetadata_errors.append(f"main manuscript renderer: {exc}")

    try:
        supporting_rtf = render_supporting_information_rtf()
        nonmetadata_errors.extend(_rtf_preflight(supporting_rtf, main_text=False))
    except Exception as exc:
        nonmetadata_errors.append(f"supporting-information renderer: {exc}")

    unexpected_metadata_errors = [
        error for error in metadata_errors
        if not error.startswith(ALLOWED_METADATA_ERROR_PREFIXES)
    ]
    scientific_gate_complete = (
        gate.get("status") == "active_chapter2_unified_model3_bridge_complete"
        and gate.get("unification_audit", {}).get("conclusion") == "success"
        and gate.get("prospective_bridge", {}).get("status") == "complete"
    )
    nonmetadata_ready = not nonmetadata_errors and not package_blockers
    only_human_blockers = bool(metadata_errors) and nonmetadata_ready and not unexpected_metadata_errors

    return {
        "schema_version": "2.0",
        "audited_on": "2026-09-27",
        "journal": metadata.get("journal"),
        "article_type": metadata.get("article_type"),
        "scientific_state": manifest.get("scientific_state") if manifest else None,
        "scientific_question_closed": manifest.get("current_submission_state", {}).get("scientific_question_closed") if manifest else None,
        "scientific_gate_complete": scientific_gate_complete,
        "unified_model3_locked": lock.get("status") == "active_chapter2_unified_model3_bridge_complete" if lock else False,
        "real_island_abc_confrontation_locked": bool(manifest.get("real_island_confrontation")) if manifest else False,
        "field_e3_e4_required": False,
        "nonmetadata_submission_preflight_ready": nonmetadata_ready,
        "nonmetadata_submission_errors": nonmetadata_errors,
        "active_nonmetadata_package_blockers": package_blockers,
        "metadata_template_validation_errors": metadata_errors,
        "metadata_template_validation_error_count": len(metadata_errors),
        "unexpected_metadata_errors": unexpected_metadata_errors,
        "only_author_supplied_metadata_and_confirmations_remain": only_human_blockers,
        "required_human_input_categories": REQUIRED_HUMAN_INPUT_CATEGORIES,
        "optional_not_initial_submission_blockers": ["coauthor_orcids", "author_contributions_credit_roles"],
        "planned_public_repository_already_fixed": metadata.get("planned_public_repository"),
        "ethics_statement_prefilled": bool(str(metadata.get("ethics_statement") or "").strip()),
        "ethics_statement_author_confirmation_required": True,
        "submission_ready": not metadata_errors and nonmetadata_ready,
        "next_transition": (
            "regenerate unified bridge figures/SI and finish submission QA; then author metadata/confirmations"
            if package_blockers or nonmetadata_errors
            else "author supplies the required metadata/confirmation categories; then build the fail-closed bundle"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    audit = build_audit(args.metadata)
    if args.check:
        if not audit["scientific_gate_complete"]:
            raise SystemExit("unified Model 3 scientific gate is not complete")
        if audit["nonmetadata_submission_errors"]:
            raise SystemExit("non-metadata submission surface has errors")
        if audit["active_nonmetadata_package_blockers"]:
            raise SystemExit("unified submission package still has declared QA blockers")
        if not audit["only_author_supplied_metadata_and_confirmations_remain"]:
            raise SystemExit("submission closure is not restricted to author-supplied metadata/confirmations")
        print("chapter2 submission closure preflight: author metadata/confirmations only")
        return

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
