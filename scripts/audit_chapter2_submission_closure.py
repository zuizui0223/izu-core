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
from scripts.render_oikos_submission_rtf import (
    render_manuscript_rtf,
    render_supporting_information_rtf,
)

DEFAULT_METADATA = ROOT / "data/design/island_ecology_submission_metadata_template.json"
DEFAULT_OUTPUT = ROOT / "data/results/chapter2_submission_closure_audit_20260906.json"

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
    return errors


def build_audit(metadata_path: Path = DEFAULT_METADATA) -> dict:
    metadata = load_metadata(metadata_path)
    metadata_errors = validate_metadata(metadata)

    nonmetadata_errors: list[str] = []
    try:
        gate = validate_scientific_gate()
    except Exception as exc:  # fail-closed audit surface
        gate = {}
        nonmetadata_errors.append(f"scientific gate: {exc}")

    required_paths = [SOURCE_MANUSCRIPT, *STATIC_SUBMISSION_FILES]
    missing_paths = [rel for rel in required_paths if not (ROOT / rel).exists()]
    nonmetadata_errors.extend(f"missing required submission surface: {rel}" for rel in missing_paths)

    manifest_path = ROOT / ACTIVE_SUBMISSION_MANIFEST
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:  # fail-closed audit surface
        manifest = {}
        nonmetadata_errors.append(f"active submission manifest: {exc}")

    if manifest:
        if manifest.get("active_manuscript") != SOURCE_MANUSCRIPT:
            nonmetadata_errors.append("active manifest manuscript does not match bundle source manuscript")
        if manifest.get("submission_ready") is not False:
            nonmetadata_errors.append("active manifest must remain submission_ready=false before author metadata is supplied")
        if manifest.get("claim_ceiling", {}).get("external_full_contracts") != "0_of_25":
            nonmetadata_errors.append("active manifest lost the frozen 0/25 full-contract claim boundary")
        if manifest.get("world_saturation_and_izu_continuity", {}).get("izu_focal_selection_rule") != (
            "measurement_continuity_after_world_saturation_not_proximity_representativeness_or_positive_model_fit"
        ):
            nonmetadata_errors.append("active manifest lost the Izu measurement-continuity selection rule")

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
        error for error in metadata_errors if not error.startswith(ALLOWED_METADATA_ERROR_PREFIXES)
    ]
    only_human_blockers = bool(metadata_errors) and not nonmetadata_errors and not unexpected_metadata_errors

    return {
        "schema_version": "1.0",
        "audited_on": "2026-09-06",
        "journal": metadata.get("journal"),
        "article_type": metadata.get("article_type"),
        "scientific_gate_complete": gate.get("scientific_model_gate_complete") is True,
        "nonmetadata_submission_preflight_ready": not nonmetadata_errors,
        "nonmetadata_submission_errors": nonmetadata_errors,
        "metadata_template_validation_errors": metadata_errors,
        "metadata_template_validation_error_count": len(metadata_errors),
        "unexpected_metadata_errors": unexpected_metadata_errors,
        "only_author_supplied_metadata_and_confirmations_remain": only_human_blockers,
        "required_human_input_categories": REQUIRED_HUMAN_INPUT_CATEGORIES,
        "optional_not_initial_submission_blockers": [
            "coauthor_orcids",
            "author_contributions_credit_roles",
        ],
        "planned_public_repository_already_fixed": metadata.get("planned_public_repository"),
        "ethics_statement_prefilled": bool(str(metadata.get("ethics_statement") or "").strip()),
        "ethics_statement_author_confirmation_required": True,
        "submission_ready": not metadata_errors and not nonmetadata_errors,
        "next_transition": (
            "author supplies the nine required metadata/confirmation categories; then run the fail-closed metadata and bundle builders"
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
        if not audit["nonmetadata_submission_preflight_ready"]:
            raise SystemExit("non-metadata submission preflight is not ready")
        if not audit["only_author_supplied_metadata_and_confirmations_remain"]:
            raise SystemExit("submission closure is not restricted to author-supplied metadata/confirmations")
        print("chapter2 submission closure preflight: author metadata/confirmations only")
        return

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
