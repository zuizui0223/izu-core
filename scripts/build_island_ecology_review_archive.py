from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from scripts.generate_chapter2_manuscript_figures import build_figures

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "dist/island_ecology_anonymous_review_archive.zip"
MANUSCRIPT = "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_20260827.md"

CORE_REVIEW_FILES = (
    "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_20260827.md",
    "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_SUPPORTING_INFORMATION_20260827.md",
    "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_REFERENCE_LEDGER_20260827.md",
    "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_TABLES_20260827.md",
    "docs/CHAPTER2_MODEL_SPEC_FOR_MANUSCRIPT_20260827.md",
    "docs/CHAPTER2_SCIENTIFIC_GATE_RUN_20260827.md",
    "docs/CHAPTER2_CONDITIONAL_WHY_DIAGNOSTICS_20260827.md",
    "docs/CHAPTER2_MANUSCRIPT_REASSEMBLY_DECISION_20260827.md",
    "data/design/chapter2_active_manuscript_mainline_20260827.json",
    "data/design/chapter2_conditional_why_diagnostics_freeze_20260827.json",
    "data/design/manuscript_reassessment_gate_20260826.json",
    "data/design/island_syndrome_literature_claim_matrix_20260824.json",
    "data/results/chapter2_phase12_fixed_gate_summary_20260827.json",
    "data/results/context_assurance_threshold_maps_gate_frozen_20260827.json",
    "data/results/chapter2_scientific_gate_decision_frozen_20260827.json",
    "data/results/chapter2_conditional_why_diagnostics_frozen_20260827.json",
    "scripts/generate_chapter2_manuscript_figures.py",
    "scripts/generate_chapter2_manuscript_tables.py",
    "scripts/run_response_geometry_realization_stability.py",
    "scripts/run_joint_response_transition_surface.py",
    "scripts/run_chapter2_conditional_why_diagnostics.py",
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
    core_records = validate_files(CORE_REVIEW_FILES, deny_tokens)
    figure_payload = build_figures()
    figure_files = tuple(figure_payload["figure_outputs"])
    generated_files = figure_files + ("data/results/chapter2_manuscript_figure_inputs_20260827.json",)
    files = CORE_REVIEW_FILES + generated_files
    records = core_records + validate_files(generated_files, deny_tokens)

    manifest = {
        "archive_role": "double_anonymous_peer_review",
        "journal_target": "Journal of Ecology",
        "author_identity_included": False,
        "title_page_included": False,
        "manuscript_source": MANUSCRIPT,
        "scientific_state": "conditional_response_geometry_model_gate_closed",
        "figures_regenerated_fail_closed": True,
        "deny_tokens_checked": list(deny_tokens),
        "files": records,
        "claim_boundary": (
            "The archive reproduces the frozen synthetic response-geometry, joint-regime, "
            "local-context, assurance and conditional-WHY diagnostics. External island evidence is comparative "
            "grounding only and does not constitute cross-system mechanism validation."
        ),
    }
    readme = """# Anonymous review archive\n\nThis archive supports double-anonymous peer review of the active Chapter 2 Research Article candidate.\n\nThe active manuscript is regenerated from the completed scientific reassessment rather than from the retired Journal of Ecology V2/V3 drafts. The primary quantitative claim is conditional response geometry. The archive contains the complete manuscript companion specification, canonical active reference ledger, manuscript tables, frozen gate summaries, deterministic figure regeneration inputs and analysis scripts.\n\nThe figure builder recomputes the response geometry and joint parameter surface and refuses to continue if the regenerated regime counts differ from the frozen scientific gate. The conditional-WHY diagnostics reuse the same fixed points, seeds, realization counts and filtering strengths and fail closed against the frozen counts. Synthetic coefficients, variance shares, frequencies and thresholds are design diagnostics, not causal field effects, ecological prevalence or empirically calibrated thresholds.\n"""

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for record in records:
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
