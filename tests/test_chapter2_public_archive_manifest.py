import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/design/chapter2_public_archive_manifest_20261006.json"
WORKFLOW = ROOT / ".github/workflows/chapter2-public-archive.yml"
BUILDER = ROOT / "scripts/build_chapter2_public_archive.py"


def test_public_archive_manifest_has_complete_campaign_artifact_sets():
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert m["status"] == "deposition_source_manifest"
    assert m["source_main_sha"] == "982e55e80e4ca1e880edf089c3a06ce6bebce61f"

    confirm = m["campaigns"]["confirmatory"]
    general = m["campaigns"]["assurance_generality"]

    assert confirm["declared_cases"] == 4096
    assert confirm["expected_shards"] == 16
    assert general["declared_cases"] == 8448
    assert general["expected_shards"] == 32

    confirm_shards = [a for a in confirm["artifacts"] if "-shard-" in a["name"]]
    general_shards = [a for a in general["artifacts"] if "-shard-" in a["name"]]
    assert len(confirm_shards) == 16
    assert len(general_shards) == 32
    assert len(confirm["artifacts"]) == 17
    assert len(general["artifacts"]) == 33

    for campaign in (confirm, general):
        assert all(a["digest"].startswith("sha256:") for a in campaign["artifacts"])
        assert all(len(a["digest"]) == 71 for a in campaign["artifacts"])
        assert all(a["size_in_bytes"] > 0 for a in campaign["artifacts"])
        assert all(a["expired"] is False for a in campaign["artifacts"])


def test_public_archive_builder_and_workflow_verify_before_packaging():
    builder = BUILDER.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "digest mismatch" in builder
    assert "expected_shards" in builder
    assert "ZIP_STORED" in builder
    assert "doi_assigned" in builder
    assert "digest mismatch" in workflow
    assert "actions/artifacts/{rec['id']}/zip" in workflow
    assert "chapter2_public_archive_20261006.zip" in workflow


def test_public_archive_includes_submission_relevant_committed_sources():
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert m["manuscript"] == "docs/CHAPTER2_MANUSCRIPT_ECOLOGY_LETTERS_20261006.md"
    assert "data/results/chapter2_assurance_attenuation_decomposition_20261006.json" in m["derived_committed_results"]
    assert "data/results/chapter2_assurance_gradient_components_20261006.json" in m["derived_committed_results"]
    for campaign in m["campaigns"].values():
        assert (ROOT / campaign["design_file"]).is_file()
        assert (ROOT / campaign["committed_result_file"]).is_file()
