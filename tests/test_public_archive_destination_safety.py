"""Archive packaging must never delete or overwrite the source artifacts."""
import hashlib
import json
from pathlib import Path
import zipfile

import pytest

from scripts import build_chapter2_public_archive as builder


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture
def archive_inputs(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    root.mkdir()
    inputs = tmp_path / "package-staging"
    inputs.mkdir()
    manifest = {"source_main_sha": "fixture-source", "campaigns": {},
                "derived_committed_results": ["derived.json"], "manuscript": "paper.md"}
    for campaign in ("confirmatory", "assurance_generality"):
        folder = inputs / campaign
        folder.mkdir()
        raw = folder / "original-shard-0.zip"
        with zipfile.ZipFile(raw, "w") as z:
            z.writestr("original.txt", campaign + " immutable source")
        manifest["campaigns"][campaign] = {
            "artifacts": [{"name": "original-shard-0", "digest": "sha256:" + digest(raw)}],
            "expected_shards": 1, "declared_cases": 1,
            "design_file": campaign + "-design.json",
            "committed_result_file": campaign + "-result.json",
        }
        for suffix in ("design", "result"):
            (root / (campaign + "-" + suffix + ".json")).write_text('{"source": true}', encoding="utf-8")
    (root / "derived.json").write_text('{"derived": true}', encoding="utf-8")
    (root / "paper.md").write_text("# Original paper\n", encoding="utf-8")
    manifest_path = root / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    monkeypatch.setattr(builder, "ROOT", root)
    monkeypatch.setattr(builder, "MANIFEST", manifest_path)
    original = {p: p.read_bytes() for folder in (root, inputs) for p in folder.rglob("*") if p.is_file()}
    return root, inputs, manifest, original


def assert_originals(original):
    assert {p: p.read_bytes() for p in original} == original


def test_build_keeps_originals_even_in_preexisting_guessed_staging(tmp_path, archive_inputs):
    root, inputs, manifest, original = archive_inputs
    # This exact source folder used to be recursively deleted by build().
    out = tmp_path / "package.zip"
    receipt = builder.build(inputs, out)
    assert_originals(original)
    assert receipt["artifact_count"] == 2
    assert receipt["doi_assigned"] is False
    assert receipt["bundle_sha256"] == digest(out)
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None
        assert len(z.namelist()) == 10  # manifest + six supporting files + two ZIPs + receipt
        assert z.read("PUBLIC_ARCHIVE_MANIFEST.json") == builder.MANIFEST.read_bytes()
        for campaign in manifest["campaigns"]:
            rel = campaign + "/original-shard-0.zip"
            assert z.read("raw-artifacts/" + rel) == (inputs / rel).read_bytes()
        for name in ("paper.md", "derived.json"):
            assert z.read(name) == (root / name).read_bytes()
    assert list(tmp_path.glob("package-staging-*")) == []


@pytest.mark.parametrize("target", ["inside", "dotdot", "source", "manifest"])
def test_reject_source_destination_overlap(tmp_path, archive_inputs, target):
    root, inputs, _, original = archive_inputs
    outputs = {
        "inside": inputs / "new.zip",
        "dotdot": inputs / "subdir" / ".." / "new.zip",
        "source": root / "paper.md",
        "manifest": builder.MANIFEST,
    }
    with pytest.raises(ValueError, match="overlaps"):
        builder.build(inputs, outputs[target])
    assert_originals(original)
    assert not (inputs / "subdir").exists()
    assert not (inputs / "new.zip").exists()


@pytest.mark.parametrize("existing_receipt", [False, True])
def test_preserve_existing_output_or_receipt(tmp_path, archive_inputs, existing_receipt):
    _, inputs, _, original = archive_inputs
    out = tmp_path / "existing.zip"
    protected = out.with_suffix(".zip.receipt.json") if existing_receipt else out
    protected.write_bytes(b"preserve previous archive")
    with pytest.raises(FileExistsError):
        builder.build(inputs, out)
    assert protected.read_bytes() == b"preserve previous archive"
    assert_originals(original)
    if existing_receipt:
        assert not out.exists()


def test_hash_failure_creates_no_output_or_staging(tmp_path, archive_inputs):
    _, inputs, _, _ = archive_inputs
    (inputs / "confirmatory/original-shard-0.zip").write_bytes(b"corrupted")
    out = tmp_path / "output" / "archive.zip"
    with pytest.raises(ValueError, match="digest mismatch"):
        builder.build(inputs, out)
    assert not out.parent.exists()


def test_copy_failure_cleans_only_owned_temporary_directory(tmp_path, archive_inputs, monkeypatch):
    _, inputs, _, original = archive_inputs
    out = tmp_path / "package.zip"
    def fail_copy(*args, **kwargs):
        raise OSError("fixture copy failure")
    monkeypatch.setattr(builder.shutil, "copy2", fail_copy)
    with pytest.raises(OSError, match="fixture copy failure"):
        builder.build(inputs, out)
    assert_originals(original)
    assert inputs.exists()
    assert list(tmp_path.glob("package-staging-*")) == []
    assert not out.exists()
