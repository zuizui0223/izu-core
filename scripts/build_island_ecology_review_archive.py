from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
import zipfile
from pathlib import Path

from scripts.generate_chapter2_unified_model3_figures import build_figures
from scripts.render_chapter2_oikos_generality_overlay import render_submission_manuscript
from scripts.render_oikos_submission_rtf import render_supporting_information_markdown

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "dist/chapter2_oikos_anonymous_review_archive.zip"
SOURCE_MANUSCRIPT = "legacy/submission-history/model3_bridge_20261004/MANUSCRIPT.md"
ANONYMOUS_MANUSCRIPT_NAME = "MANUSCRIPT.md"
ANONYMOUS_SI_NAME = "SUPPORTING_INFORMATION.md"

CORE_REVIEW_FILES = (
    "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_IZU_EMPIRICAL_APPENDIX_20260827.md",
    "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_REFERENCE_LEDGER_20260827.md",
    "docs/CHAPTER2_CANONICAL_STORY_20260927.md",
    "docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md",
    "docs/CHAPTER2_MODEL_UNIFICATION_DECISION_20260927.md",
    "docs/MODEL3_CH2_BRIDGE_PROSPECTIVE_RESULTS_20260927.md",
    "data/results/model3_ch2_bridge_prospective_frozen_20260927.json",
    "docs/CHAPTER2_UNIFIED_MODEL3_REAL_ISLAND_PROJECTION_20260927.md",
    "docs/CHAPTER1_CHAPTER2_CANONICAL_BRIDGE_20260927.md",
    "docs/CHAPTER1_OPEN_PROBLEMS_TO_UNIFIED_MODEL3_20260927.md",
    "data/design/chapter2_oikos_submission_manifest_20260927.json",
    "data/design/chapter2_unified_model3_lock_20260927.json",
    "data/design/model3_unified_reduction_audit_20260927.json",
    "data/design/model3_ch2_bridge_20260927.json",
    "data/design/model3_ch2_bridge_execution_20260927.json",
    "scripts/model3_island_bridge_ops.py",
    "scripts/run_model3_ch2_bridge.py",
    "scripts/run_model3_ch2_bridge_shard.py",
    "scripts/export_model3_ch2_bridge_shard.py",
    "scripts/summarize_model3_ch2_bridge_shards.py",
    "scripts/summarize_model3_ch2_bridge_prospective.py",
    "scripts/generate_chapter2_unified_model3_figures.py",
    "data/results/model3_unified_reduction_audit_frozen_20260927.json",
    "data/results/chapter2_unified_model3_real_island_projection_20260927.json",
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
        "data/results/chapter2_unified_model3_figure_inputs_20260927.json",
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
        if "appendix s4. prospective model 3 isolation bridge" not in supporting_lower:
            raise ValueError("prospective Model 3 bridge missing from anonymous Supporting Information")
        for legacy in (
            "appendix s19",
            "finite-community system-size audit",
            "gaussian mean-field limit",
            "regime-dependent response hierarchy under active plant adjustment",
        ):
            if legacy in supporting_lower:
                raise ValueError(f"legacy Model 2 material leaked into anonymous Supporting Information: {legacy}")

        required_story = (
            "fixed-state reproductive assay",
            "deterministic genotype-density counterpart",
            "finite-population abm",
            "real islands occupy different stages of the same response architecture",
            "all eight shared oshima-to-post targets",
            "counterdirectional case",
            "principal natural-data gap",
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
            "source": "current Model 3 / natural-confrontation SI only; legacy Model 2 excluded",
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
            "prospective_model3_bridge_included_fail_closed": True,
            "legacy_realized_richness_reframe_included_fail_closed": False,
            "legacy_equal_turnover_generality_control_included_fail_closed": False,
            "mechanism_mainline_included_fail_closed": True,
            "three_result_reframe_active": False,
            "scientific_state": "unified_model3_bridge_complete_with_real_island_layer_confrontation",
            "relational_robustness_audit_included": False,
            "realized_richness_hard_control_included": False,
            "equal_turnover_control_included": False,
            "interaction_kernel_identity_audit_included": False,
            "izu_empirical_material_role": "A_layer_branching_confrontation_and_future_AC_falsification_context",
            "field_e3_e4_required_for_current_paper": False,
            "external_prediction_readiness_audit_included": False,
            "oikos_data_code_review_ready": True,
            "deny_tokens_checked": list(deny_tokens),
            "files": records,
            "claim_boundary": (
                "The archive presents Chapter 2 as one nested Model 3 mechanism paper with a completed prospective isolation bridge. Controlled compositions establish branch capacity; annual visitor-count matching shifts the coarse mean regime; finite visitor-environment pooling and plant-capacity controls separate ecological from demographic realization. "
                "Source-locked island systems are confronted by layer rather than fitted to synthetic parameter cells: A is partly observed, C has direct-history anchors, and the inherited longitudinal B layer remains the clearest empirical gap. "
                "Legacy Model 2 exact-richness, synthetic-k, response-rule and S/C/I analyses are repository legacy provenance under legacy/model2/ and are excluded from the anonymous review archive."
            ),        }
        readme = """# Anonymous review archive

This archive supports Oikos double-anonymous review of the Chapter 2 mechanism paper.

The active manuscript is organized around one nested Model 3: **controlled branch capacity -> isolation-driven deterministic response -> finite visitor and plant-population realization -> history/context-dependent outcome**. The prospective 24,576-case bridge shows that annual visitor-count matching reverses the coarse mean response, eight-history visitor pooling removes mixed branches, and fourfold larger plant capacity nearly removes finite-ABM mixed branches.

Natural systems are confronted by layer rather than assigned to synthetic model cells. The source-locked 14-system-layer matrix includes same-direction propagation, branching, buffering and a counterdirectional falsifier. Izu is the strongest current A-layer branching example; Surtsey, Tiritiri Matangi and direct partner-loss systems provide C-layer history anchors. The inherited longitudinal B layer remains the main empirical gap. The formal source audit remains 0/25 complete A -> B -> C contracts.

Legacy Model 2 exact realized-richness, synthetic-k, S/C/I and response-rule analyses remain only in the repository legacy archive and do not define a second mechanism, active control gate or current Supporting Information component.
"""

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
