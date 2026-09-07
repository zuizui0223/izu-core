from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
import zipfile
from pathlib import Path

from scripts.generate_chapter2_manuscript_figures_realized_richness import build_figures
from scripts.render_chapter2_realized_richness_reframe import render_submission_manuscript
from scripts.render_oikos_submission_rtf import render_supporting_information_markdown

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "dist/chapter2_oikos_anonymous_review_archive.zip"
SOURCE_MANUSCRIPT = "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
ANONYMOUS_MANUSCRIPT_NAME = "MANUSCRIPT.md"
ANONYMOUS_SI_NAME = "SUPPORTING_INFORMATION.md"

CORE_REVIEW_FILES = (
    "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_IZU_EMPIRICAL_APPENDIX_20260827.md",
    "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_REFERENCE_LEDGER_20260827.md",
    "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_TABLES_20260827.md",
    "docs/CHAPTER2_MODEL_SPEC_FOR_MANUSCRIPT_20260827.md",
    "docs/CHAPTER2_INTERACTION_KERNEL_DERIVATION_20260828.md",
    "docs/CHAPTER2_RELATIONAL_ROBUSTNESS_CORRECTION_20260831.md",
    "docs/CHAPTER2_SUPPORTING_INFORMATION_S19_REALIZED_RICHNESS_20260907.md",
    "docs/CHAPTER2_SUPPORTING_TABLE_S9_REALIZED_RICHNESS_20260907.md",
    "docs/CHAPTER2_SCIENTIFIC_GATE_RUN_20260827.md",
    "docs/CHAPTER2_CONDITIONAL_WHY_DIAGNOSTICS_20260827.md",
    "docs/CHAPTER2_EXTERNAL_PREDICTION_SOURCE_AUDIT_20260828.md",
    "docs/CHAPTER2_EXTERNAL_PREDICTION_UPGRADE_AUDIT_20260828.md",
    "docs/IZU_POLLINATOR_PROBOSCIS_RECOVERY.md",
    "docs/IZU_SIGNED_POSITION_TRIANGULATION_20260827.md",
    "docs/IZU_SIGNED_POSITION_STRUCTURAL_AUDIT_20260827.md",
    "data/design/chapter2_oikos_submission_manifest_20260831.json",
    "data/design/chapter2_active_manuscript_mainline_20260827.json",
    "data/design/chapter2_conditional_why_diagnostics_freeze_20260827.json",
    "data/design/chapter2_external_prediction_challenge_freeze_20260828.json",
    "data/design/chapter2_external_prediction_admission_ledger_20260828.csv",
    "data/design/chapter2_relational_robustness_audit_freeze_20260831.json",
    "data/design/chapter2_realized_richness_matching_freeze_20260907.json",
    "data/design/manuscript_reassessment_gate_20260826.json",
    "data/design/island_syndrome_literature_claim_matrix_20260824.json",
    "data/design/izu_pollinator_proboscis_recovery_status.json",
    "data/design/izu_signed_position_source_gate_20260827.json",
    "data/results/izu_signed_position_structural_audit_frozen_20260827.json",
    "data/results/chapter2_phase12_fixed_gate_summary_20260827.json",
    "data/results/context_assurance_threshold_maps_gate_frozen_20260827.json",
    "data/results/chapter2_scientific_gate_decision_frozen_20260827.json",
    "data/results/chapter2_conditional_why_diagnostics_frozen_20260827.json",
    "data/results/chapter2_external_prediction_readiness_frozen_20260828.json",
    "data/results/chapter2_interaction_kernel_audit_frozen_20260828.json",
    "data/results/chapter2_relational_robustness_audit_frozen_20260831.json",
    "data/results/chapter2_realized_richness_matching_decision_20260907.json",
    "scripts/audit_chapter2_interaction_kernel.py",
    "scripts/audit_chapter2_relational_robustness.py",
    "scripts/audit_chapter2_realized_richness_matching.py",
    "scripts/generate_chapter2_manuscript_figures.py",
    "scripts/generate_chapter2_manuscript_figures_relational.py",
    "scripts/generate_chapter2_manuscript_figures_realized_richness.py",
    "scripts/generate_chapter2_manuscript_tables.py",
    "scripts/run_response_geometry_realization_stability.py",
    "scripts/run_joint_response_transition_surface.py",
    "scripts/run_chapter2_conditional_why_diagnostics.py",
    "scripts/run_chapter2_external_prediction_readiness.py",
    "scripts/analyze_izu_signed_position_triangulation.py",
    "scripts/audit_izu_signed_position_table_s4_sensitivity.py",
    "scripts/audit_izu_signed_position_structural_independence.py",
)

DEFAULT_DENY_TOKENS = (
    "zuizui0223",
    "github.com/zuizui0223",
)
TEXT_SUFFIXES = {".md", ".py", ".json", ".txt", ".csv", ".toml", ".yaml", ".yml", ".svg"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def find_denied_tokens(path: Path, deny_tokens: tuple[str, ...]) -> tuple[str, ...]:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return ()
    text = path.read_text(encoding="utf-8")
    lower = text.lower()
    return tuple(token for token in deny_tokens if token.lower() in lower)


def validate_files(files: tuple[str, ...], deny_tokens: tuple[str, ...]) -> list[dict]:
    records: list[dict] = []
    for rel in files:
        path = ROOT / rel
        if not path.exists():
            raise FileNotFoundError(f"missing review archive file: {rel}")
        denied = find_denied_tokens(path, deny_tokens)
        if denied:
            raise ValueError(f"author-identifying token(s) {denied!r} found in {rel}")
        records.append({"path": rel, "sha256": sha256(path), "size_bytes": path.stat().st_size})
    return records


def build_archive(output: Path, *, extra_deny_tokens: tuple[str, ...] = ()) -> Path:
    deny_tokens = tuple(dict.fromkeys(DEFAULT_DENY_TOKENS + extra_deny_tokens))
    if not (ROOT / SOURCE_MANUSCRIPT).exists():
        raise FileNotFoundError(SOURCE_MANUSCRIPT)
    core_records = validate_files(CORE_REVIEW_FILES, deny_tokens)
    figure_payload = build_figures()
    figure_files = tuple(figure_payload["figure_outputs"])
    generated_files = figure_files + (
        "data/results/chapter2_manuscript_figure_inputs_20260827.json",
        "data/results/chapter2_manuscript_figure_inputs_relational_20260831.json",
    )
    generated_records = validate_files(generated_files, deny_tokens)

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp_name:
        tmp = Path(tmp_name)
        manuscript = tmp / ANONYMOUS_MANUSCRIPT_NAME
        supporting_information = tmp / ANONYMOUS_SI_NAME
        manuscript.write_text(render_submission_manuscript(), encoding="utf-8")
        supporting_information.write_text(render_supporting_information_markdown(), encoding="utf-8")
        for generated in (manuscript, supporting_information):
            denied = find_denied_tokens(generated, deny_tokens)
            if denied:
                raise ValueError(f"author-identifying token(s) {denied!r} found in rendered anonymous file {generated.name}")
        supporting_lower = supporting_information.read_text(encoding="utf-8").lower()
        manuscript_lower = manuscript.read_text(encoding="utf-8").lower()
        if "cell-level simulation variation" in supporting_lower:
            raise ValueError("superseded nonadditivity wording survived anonymous Supporting Information")
        if "appendix s19. exact realized-richness matching hard control" not in supporting_lower:
            raise ValueError("realized-richness hard control missing from anonymous Supporting Information")
        if "mean regime placement is therefore richness-sensitive" not in manuscript_lower:
            raise ValueError("realized-richness reframe missing from anonymous manuscript")
        if "richness reduction is not necessary for mixed response geometry" in manuscript_lower:
            raise ValueError("stale richness-independent claim survived anonymous manuscript")

        manuscript_record = {
            "path": ANONYMOUS_MANUSCRIPT_NAME,
            "source": SOURCE_MANUSCRIPT,
            "sha256": sha256(manuscript),
            "size_bytes": manuscript.stat().st_size,
        }
        si_record = {
            "path": ANONYMOUS_SI_NAME,
            "source": "base SI + relational correction + realized-richness S19 + Supporting Tables S1-S9",
            "sha256": sha256(supporting_information),
            "size_bytes": supporting_information.stat().st_size,
        }
        records = [manuscript_record, si_record, *core_records, *generated_records]

        manifest = {
            "archive_role": "double_anonymous_peer_review",
            "journal_target": "Oikos",
            "article_type": "Research Paper",
            "author_identity_included": False,
            "title_page_included": False,
            "scientific_source_manuscript": SOURCE_MANUSCRIPT,
            "review_manuscript": ANONYMOUS_MANUSCRIPT_NAME,
            "review_supporting_information": ANONYMOUS_SI_NAME,
            "review_manuscript_internal_thesis_language_removed_fail_closed": True,
            "supporting_information_superseded_nonadditivity_wording_removed_fail_closed": True,
            "realized_richness_reframe_included_fail_closed": True,
            "scientific_state": "richness_sensitive_mean_regime_with_relational_branching_and_bounded_empirical_resolution",
            "frozen_figures_regenerated_then_realized_richness_overlay": True,
            "relational_robustness_audit_included": True,
            "realized_richness_hard_control_included": True,
            "interaction_kernel_identity_audit_included": True,
            "izu_source_gate_included": True,
            "izu_structural_audit_included": True,
            "izu_empirical_appendix_included": True,
            "external_prediction_readiness_audit_included": True,
            "oikos_data_code_review_ready": True,
            "deny_tokens_checked": list(deny_tokens),
            "files": records,
            "claim_boundary": (
                "The archive preserves the historical freeze chain and adds the prespecified exact realized-richness hard control. "
                "The hard control changes the ensemble mean geometry to all-positive in all six matching seeds, so realized richness cannot be declared irrelevant to mean-regime placement. "
                "At the same time, 51-65/96 individual communities remain mixed and state-by-community nonadditivity remains 42.72-48.51%, so response branching remains relational. "
                "World confrontation remains an outcome-rich/process-poor measurement audit and Izu remains a bounded continuity-system zoom rather than validation."
            ),
        }
        readme = """# Anonymous review archive\n\nThis archive supports Oikos double-anonymous review of the response-geometry Research Paper.\n\nThe historical Chapter 2 freeze chain is retained unchanged. A prespecified 2026-08-31 relational-robustness audit tests seed ensemble, model horizon, trait adjustment and equal initial pollinator richness. A second sensitivity was frozen on 2026-09-07 before execution and forces realized mainland-like and island-like pollinator richness to be exactly equal at every simulated step by response-blind subsampling.\n\nThat hard control changes the ensemble mean response geometry to all-positive in all six matching seeds. The submission therefore does not claim that richness differences are unnecessary for mean-regime placement. However, 51-65/96 individual community realizations remain mixed and state-by-community nonadditivity remains 42.72-48.51%, while the additive starting-position term remains 0.94-2.21%. The revised structural claim is that mean-regime placement is richness-sensitive whereas branch identity remains relational to starting state and realized community composition.\n\nThe world audit is presented as measurement availability rather than prediction success: response outcomes are directly measured in 21/25 entries but partner arrival/replacement in only 2/25, and no entry meets the full joint outcome-independent contract. The Izu analysis retains the historical raw-positive/null-corrected-negative boundary, a robust contemporary FDQ-to-matching association and weaker downstream matching-to-pollen propagation. No missing predictor is reconstructed from known outcomes and no downstream focal phenotype is used as validation.\n"""

        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.write(manuscript, arcname=ANONYMOUS_MANUSCRIPT_NAME)
            archive.write(supporting_information, arcname=ANONYMOUS_SI_NAME)
            for record in [*core_records, *generated_records]:
                archive.write(ROOT / record["path"], arcname=record["path"])
            archive.writestr("REVIEW_ARCHIVE_MANIFEST.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
            archive.writestr("README_REVIEW_ARCHIVE.md", readme)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--deny-token", action="append", default=[])
    args = parser.parse_args()
    path = build_archive(args.output, extra_deny_tokens=tuple(args.deny_token))
    print(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


if __name__ == "__main__":
    main()
