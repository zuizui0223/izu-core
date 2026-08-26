from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
import zipfile
from pathlib import Path

from scripts.build_island_ecology_manuscript_v3 import build_manuscript

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "dist/island_ecology_anonymous_review_archive.zip"
MANUSCRIPT_ARCNAME = "docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V3_20260826.md"

REVIEW_FILES = (
    "docs/ISLAND_ECOLOGY_JECOLOGY_SUPPLEMENT_20260824.md",
    "docs/ISLAND_ECOLOGY_H2_SIGN_DECOMPOSITION_20260825.md",
    "docs/ISLAND_ECOLOGY_DATA_CODE_AVAILABILITY_20260824.md",
    "docs/ISLAND_ECOLOGY_FIGURE_CAPTIONS_20260824.md",
    "docs/SIMULATION_MANUSCRIPT_EXTERNAL_SYSTEM_REFERENCES_20260824.md",
    "data/design/island_ecology_jecology_submission_manifest.json",
    "data/design/simulation_manuscript_external_system_reference_matrix.json",
    "data/design/abm_v12_branch_generator_independent_robustness_freeze.json",
    "data/results/constraint_mechanism_abm_v11_factorial_summary_frozen.json",
    "data/results/constraint_mechanism_abm_v12_residual_trait_causes_frozen.json",
    "data/results/abm_v12_branch_generator_independent_robustness_frozen.json",
    "data/results/network_context_buffering_capability_robustness_frozen.json",
    "data/results/constraint_mechanism_abm_v14_assurance_buffering_robustness_frozen.json",
    "data/results/frozen_abm_state_atlas_frozen.json",
    "data/results/frozen_abm_state_separability_frozen.json",
    "data/results/simulation_manuscript_figure_data_frozen.json",
    "data/results/simulation_manuscript_falsification_table_frozen.json",
    "channel_id/state_separability.py",
    "scripts/run_constraint_mechanism_abm_v12_residual_trait_causes.py",
    "scripts/render_simulation_manuscript_fig1_svg.py",
    "scripts/render_island_ecology_mechanism_figures_svg.py",
    "scripts/render_island_ecology_external_figures_svg.py",
    "tests/test_island_ecology_figure_routing.py",
    "tests/test_island_ecology_paper_completion.py",
    "tests/test_h2_sign_decomposition.py",
    "tests/test_island_ecology_manuscript_v3.py",
)

DEFAULT_DENY_TOKENS = (
    "zuizui0223",
    "github.com/zuizui0223",
)

TEXT_SUFFIXES = {".md", ".py", ".json", ".txt", ".csv", ".toml", ".yaml", ".yml"}


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


def validate_review_files(deny_tokens: tuple[str, ...]) -> list[dict]:
    records: list[dict] = []
    for rel in REVIEW_FILES:
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
    records = validate_review_files(deny_tokens)

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp_name:
        generated_manuscript = Path(tmp_name) / "ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V3_20260826.md"
        build_manuscript(generated_manuscript)
        denied = find_denied_tokens(generated_manuscript, deny_tokens)
        if denied:
            raise ValueError(f"author-identifying token(s) {denied!r} found in generated V3 manuscript")
        manuscript_record = {
            "path": MANUSCRIPT_ARCNAME,
            "sha256": sha256(generated_manuscript),
            "size_bytes": generated_manuscript.stat().st_size,
        }
        manifest = {
            "archive_role": "double_anonymous_peer_review",
            "journal_target": "Journal of Ecology",
            "author_identity_included": False,
            "title_page_included": False,
            "external_research_programmes_included": False,
            "manuscript_source": "V2 source rendered deterministically to editorial V3",
            "deny_tokens_checked": list(deny_tokens),
            "files": [manuscript_record, *records],
            "claim_boundary": (
                "The archive reproduces the frozen island-ecology simulation results, "
                "the algebraic H2 endpoint sign decomposition, and the source-audited "
                "external response-state challenge. Editorial V3 integrates the already-frozen "
                "H2 algebra into the manuscript without changing scientific results."
            ),
        }
        readme = """# Anonymous review archive\n\nThis archive supports double-anonymous peer review of the island-ecology manuscript.\n\nThe reviewer-facing manuscript is editorial V3, rendered deterministically from the frozen V2 source. V3 sharpens the Introduction gap statement and integrates the already-frozen H2 endpoint sign decomposition into the Abstract, Methods, Results, Discussion and Conclusion. It does not rerun or alter any scientific analysis.\n\nThe archive also contains Supporting Information, frozen analysis summaries, the source-audited external-system matrix, figure inputs/renderers and paper-specific regression guards. It intentionally excludes title-page material, author-identifying links, historical pre-submission drafts, and unrelated research programmes.\n\nNo external research programme is required to define, reproduce, or validate the submitted paper.\n"""

        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.write(generated_manuscript, arcname=MANUSCRIPT_ARCNAME)
            for record in records:
                archive.write(ROOT / record["path"], arcname=record["path"])
            archive.writestr("REVIEW_ARCHIVE_MANIFEST.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
            archive.writestr("README_REVIEW_ARCHIVE.md", readme)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--deny-token",
        action="append",
        default=[],
        help="additional author-identifying token to reject; may be supplied repeatedly",
    )
    args = parser.parse_args()
    path = build_archive(args.output, extra_deny_tokens=tuple(args.deny_token))
    print(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


if __name__ == "__main__":
    main()
