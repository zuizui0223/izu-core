from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
import zipfile
from pathlib import Path

from scripts.generate_chapter2_manuscript_figures_realized_richness import build_figures
from scripts.render_chapter2_oikos_generality_overlay import render_submission_manuscript
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
    "docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md",
    "docs/CHAPTER2_THREE_RESULT_NARRATIVE_LOCK_20260908.md",
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
    "data/results/chapter2_equal_turnover_control_20260908.json",
    "data/results/wanshan_yongxing/effect_rows.json",
    "data/results/ogasawara/context_analysis/effect_rows.json",
    "scripts/audit_chapter2_interaction_kernel.py",
    "scripts/audit_chapter2_relational_robustness.py",
    "scripts/audit_chapter2_realized_richness_matching.py",
    "scripts/audit_chapter2_equal_turnover_control.py",
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

DEFAULT_DENY_TOKENS = ("zuizui0223", "github.com/zuizui0223")
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

        required_story = (
            "conditional response geometry",
            "realized richness differences therefore help position the ensemble mean regime",
            "ordering of response determinants is itself regime dependent",
            "deterministic mean-field kernel contrast was all-positive",
            "70/96",
            "65.61%",
            "optional future validation programme",
        )
        missing_story = [token for token in required_story if token not in manuscript_lower]
        if missing_story:
            raise ValueError(f"mechanism-mainline narrative missing from anonymous manuscript: {missing_story}")
        stale_story = (
            "figure 1. three-result inference chain",
            "result 1—mechanistic prediction",
            "result 2—real-world exposure",
            "result 3—biological consequence",
        )
        leaked = [token for token in stale_story if token in manuscript_lower]
        if leaked:
            raise ValueError(f"historical three-result narrative leaked into anonymous manuscript: {leaked}")

        manuscript_record = {
            "path": ANONYMOUS_MANUSCRIPT_NAME,
            "source": SOURCE_MANUSCRIPT,
            "sha256": sha256(manuscript),
            "size_bytes": manuscript.stat().st_size,
        }
        si_record = {
            "path": ANONYMOUS_SI_NAME,
            "source": "base SI + relational correction + realized-richness S19 + Supporting Tables S1-S9 + equal-turnover/system-size generality material",
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
            "equal_turnover_generality_control_included_fail_closed": True,
            "mechanism_mainline_included_fail_closed": True,
            "three_result_reframe_active": False,
            "scientific_state": "synthetic_conditional_response_geometry_with_regime_dependent_determinant_ordering",
            "relational_robustness_audit_included": True,
            "realized_richness_hard_control_included": True,
            "equal_turnover_control_included": True,
            "interaction_kernel_identity_audit_included": True,
            "izu_empirical_material_role": "future_validation_context_and_claim_boundary",
            "field_e3_e4_required_for_current_paper": False,
            "external_prediction_readiness_audit_included": True,
            "oikos_data_code_review_ready": True,
            "deny_tokens_checked": list(deny_tokens),
            "files": records,
            "claim_boundary": (
                "The archive presents Chapter 2 as a synthetic mechanism paper. Exact realized-richness matching shifts the ensemble mean geometry while preserving individual branching and state-by-community nonadditivity. "
                "The prespecified system-size audit shows that the ordering of starting-state and community-realization contributions changes across the declared finite-community regime, with no natural threshold claim. "
                "World and Izu materials are retained for plausibility, falsification and reviewer audit, not as required validation or as a coequal three-result empirical cascade."
            ),
        }
        readme = """# Anonymous review archive\n\nThis archive supports Oikos double-anonymous review of the Chapter 2 mechanism paper.\n\nThe active manuscript is organized around **conditional response geometry -> exact realized-richness control -> scale-dependent determinant ordering -> downstream modifiers**. World and Izu materials remain available for reviewer inspection, but they define biological plausibility and the historical claim ceiling rather than a required empirical validation chain.\n\nExact realized-richness matching shifts the ensemble mean geometry to all-positive in all six matching seeds while 51-65/96 individual realizations remain mixed and state-by-community nonadditivity remains 42.72-48.51%. A separate equal-turnover control retains 70/96 mixed realizations and 65.61% nonadditivity. Under active plant adjustment, the additive determinant ordering reverses across the declared k sequence: median starting-position share rises from 2.55% to 55.84% while median community-realization share falls from 72.98% to 12.72%. The numerical crossover is model-specific and is not transferred to nature.\n\nThe formal source audit remains available for reviewer inspection: no entry meets the full joint outcome-independent historical transition contract. Izu same-block E3/E4 measurements remain an optional future validation programme, not a current manuscript completion gate.\n"""

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
