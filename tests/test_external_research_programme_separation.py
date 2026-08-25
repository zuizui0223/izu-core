import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CURRENT_PAPER_FILES = (
    ROOT / "README.md",
    ROOT / "docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md",
    ROOT / "docs/ISLAND_ECOLOGY_JECOLOGY_SUPPLEMENT_20260824.md",
    ROOT / "docs/ISLAND_ECOLOGY_DATA_CODE_AVAILABILITY_20260824.md",
    ROOT / "docs/ISLAND_ECOLOGY_JECOLOGY_COVER_LETTER_20260824.md",
    ROOT / "data/design/island_ecology_jecology_submission_manifest.json",
    ROOT / "data/design/simulation_study_mainline_20260824.json",
)

FORBIDDEN_ACTIVE_COUPLING = (
    "microdonta",
    "issue #91",
    "real_signed_functional_starting_position",
    "matched_real_network_context_effective_service_mapping",
    "complete_external_service_dependency_response_bridge",
    "future empirical translation",
    "three empirical questions now follow directly from the paper",
)


def test_current_paper_package_has_no_external_programme_coupling():
    for path in CURRENT_PAPER_FILES:
        text = path.read_text(encoding="utf-8").lower()
        for token in FORBIDDEN_ACTIVE_COUPLING:
            assert token not in text, f"active external-programme coupling in {path.name}: {token}"


def test_machine_readable_boundaries_declare_independence():
    state = json.loads((ROOT / "data/design/simulation_study_mainline_20260824.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "data/design/island_ecology_jecology_submission_manifest.json").read_text(encoding="utf-8"))

    assert state["paper_scope_independent_of_external_research_programmes"] is True
    assert state["submission_logic"]["external_research_programmes_part_of_paper"] is False
    assert state["protected_boundaries"]["external_research_programmes"] == "out_of_scope_and_not_part_of_submission"
    assert manifest["paper_scope_independent_of_external_research_programmes"] is True
    assert manifest["review_archive"]["external_research_programmes_included"] is False


def test_historical_drafts_are_not_submission_files():
    manifest = json.loads((ROOT / "data/design/island_ecology_jecology_submission_manifest.json").read_text(encoding="utf-8"))
    current_paths = set(manifest["main_files"].values())
    archived = set(manifest["archived_provenance"].values())
    assert "docs/ISLAND_ECOLOGY_MANUSCRIPT_DRAFT_20260824.md" in archived
    assert "docs/ISLAND_ECOLOGY_MANUSCRIPT_DRAFT_20260824.md" not in current_paths
    assert "docs/SIMULATION_MANUSCRIPT_DRAFT_20260824.md" in archived
