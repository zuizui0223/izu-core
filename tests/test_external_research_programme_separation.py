import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CURRENT_PAPER_FILES = (
    ROOT / "README.md",
    ROOT / "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_V2_20260827.md",
    ROOT / "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_IZU_EMPIRICAL_APPENDIX_20260827.md",
    ROOT / "data/design/island_ecology_jecology_submission_manifest.json",
    ROOT / "data/design/manuscript_reassessment_gate_20260826.json",
)

FORBIDDEN_ACTIVE_COUPLING = (
    "microdonta",
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
    gate = json.loads((ROOT / "data/design/manuscript_reassessment_gate_20260826.json").read_text(encoding="utf-8"))

    assert state["paper_scope_independent_of_external_research_programmes"] is True
    assert state["submission_logic"]["external_research_programmes_part_of_paper"] is False
    assert manifest["paper_scope_independent_of_external_research_programmes"] is True
    assert gate["current_research_article_submission_ready"] is False


def test_manifest_routes_v2_without_promoting_historical_drafts():
    manifest = json.loads((ROOT / "data/design/island_ecology_jecology_submission_manifest.json").read_text(encoding="utf-8"))
    current = manifest["current_manuscript_artifacts"]
    assert current["status"] == "active_v2_synthetic_primary_plus_izu_triangulation_reproducible"
    assert current["active_manuscript"] == "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_V2_20260827.md"
    assert current["retired_pre_v2_manuscript"] == "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_20260827.md"
    assert current["supporting_information"] == "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_SUPPORTING_INFORMATION_20260827.md"
    assert current["izu_source_gate"] == "data/design/izu_signed_position_source_gate_20260827.json"
    assert manifest["focal_izu_triangulation"]["null_corrected_matching_supported"] is False
    assert manifest["submission_ready"] is False
