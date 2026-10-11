"""Negative controls for the portable original-archive verification command.

Only the pinned metadata read is supplied locally so these failure checks work
in shallow CI checkouts. Archive inspection and failure-receipt writing are the
real production paths. No synthetic fixture can claim a positive cohort audit.
"""
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import subprocess

import pytest


ROOT = Path(__file__).resolve().parents[1]
AUDITOR = ROOT / "scripts/audit_chapter2_recovered_evolution_archives_20261011.py"
MANIFEST = ROOT / "data/design/chapter2_public_archive_manifest_20261006.json"


def load_auditor(monkeypatch):
    assert AUDITOR.is_file(), "portable audit command has not been implemented"
    spec = spec_from_file_location("recovered_evolution_audit", AUDITOR)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    def local_frozen_metadata(repo, ref, path):
        assert ref == module.BASE
        assert path in {module.MANIFEST_PATH, module.IDENTITY_PATH}
        return (ROOT / path).read_bytes()

    monkeypatch.setattr(module, "git_bytes", local_frozen_metadata)
    return module


def source_snapshot(path):
    stat = path.stat()
    return path.read_bytes(), stat.st_ino, stat.st_size, stat.st_mtime_ns


def disposable_repo(path):
    path.mkdir()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    return path


@pytest.mark.parametrize(
    ("damage", "expected_failure"),
    [
        ("missing", "actual complete ZIP set differs"),
        ("truncated", "ZIP size mismatch"),
        ("changed_same_size", "ZIP hash mismatch"),
    ],
)
def test_damaged_inputs_return_nonzero_and_write_fail_receipt(
    tmp_path, monkeypatch, damage, expected_failure
):
    # Removing any of the three artifact admission gates must break its control.
    module = load_auditor(monkeypatch)
    artifact_dir = tmp_path / "originals"
    artifact_dir.mkdir()
    original_input = None
    if damage != "missing":
        manifest = json.loads(MANIFEST.read_text())
        records = []
        for campaign, block in manifest["campaigns"].items():
            for record in block["artifacts"]:
                path = artifact_dir / campaign / (record["name"] + ".zip")
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"")
                records.append((path, record))
        original_input, record = records[0]
        if damage == "truncated":
            original_input.write_bytes(b"PK\x03\x04")
        else:
            with original_input.open("wb") as handle:
                handle.write(b"changed archived bytes")
                handle.truncate(record["size_in_bytes"])
        original_stat = original_input.stat()

    output = tmp_path / "new-parent" / "nested" / "audit.json"
    exit_code = module.main(
        ["--repo", str(ROOT), "--artifact-dir", str(artifact_dir), "--out", str(output)]
    )

    assert exit_code != 0
    assert output.is_file()
    receipt = json.loads(output.read_text())
    assert receipt["status"] == "FAIL_OR_INCOMPLETE"
    assert len(receipt["failures"]) == 1
    assert expected_failure in receipt["failures"][0]["message"]
    assert "totals" not in receipt
    assert not any(str(c.get("status", "")).startswith("PASS") for c in receipt["campaigns"].values())
    if original_input is not None:
        current = original_input.stat()
        assert (current.st_size, current.st_mtime_ns) == (original_stat.st_size, original_stat.st_mtime_ns)


@pytest.mark.parametrize("alias", [False, True], ids=["original-zip", "symlink-alias"])
def test_output_cannot_overwrite_an_original_zip(tmp_path, monkeypatch, capsys, alias):
    module = load_auditor(monkeypatch)
    artifact_dir = tmp_path / "originals"
    artifact_dir.mkdir()
    original = artifact_dir / "original.zip"
    original.write_bytes(b"disposable original ZIP sentinel")
    before = source_snapshot(original)
    output = original
    if alias:
        output = tmp_path / "alias.json"
        output.symlink_to(original)

    code = module.main(["--repo", str(ROOT), "--artifact-dir", str(artifact_dir), "--out", str(output)])

    assert source_snapshot(original) == before
    assert code != 0
    captured = capsys.readouterr()
    assert "unsafe audit output" in captured.err.lower()
    assert "PASS" not in captured.out
    assert not list(artifact_dir.glob("*.part"))
    if alias:
        assert output.is_symlink()


def test_output_inside_artifact_tree_is_rejected_before_mkdir(tmp_path, monkeypatch, capsys):
    module = load_auditor(monkeypatch)
    artifact_dir = tmp_path / "originals"
    artifact_dir.mkdir()
    output = artifact_dir / "new" / "nested" / "audit.json"

    code = module.main(["--repo", str(ROOT), "--artifact-dir", str(artifact_dir), "--out", str(output)])

    assert code != 0
    assert not output.parent.exists()
    assert "unsafe audit output" in capsys.readouterr().err.lower()


def test_output_cannot_replace_external_target_of_input_zip_symlink(tmp_path, monkeypatch, capsys):
    module = load_auditor(monkeypatch)
    artifact_dir = tmp_path / "originals"
    artifact_dir.mkdir()
    original = tmp_path / "stored-original.zip"
    original.write_bytes(b"disposable original stored outside the artifact tree")
    before = source_snapshot(original)
    input_alias = artifact_dir / "original.zip"
    input_alias.symlink_to(original)

    code = module.main(["--repo", str(ROOT), "--artifact-dir", str(artifact_dir), "--out", str(original)])

    assert source_snapshot(original) == before
    assert input_alias.is_symlink()
    assert code != 0
    captured = capsys.readouterr()
    assert "unsafe audit output" in captured.err.lower()
    assert "original ZIP" in captured.err
    assert "PASS" not in captured.out


@pytest.mark.parametrize("source_kind", ["auditor", "tracked-source", "git-metadata"])
def test_output_cannot_replace_source_inputs(tmp_path, monkeypatch, capsys, source_kind):
    module = load_auditor(monkeypatch)
    repo = disposable_repo(tmp_path / "repo")
    artifact_dir = tmp_path / "originals"
    artifact_dir.mkdir()
    if source_kind == "auditor":
        source = tmp_path / "auditor.py"
        source.write_bytes(b"disposable auditor source sentinel")
        monkeypatch.setattr(module, "__file__", str(source))
    elif source_kind == "tracked-source":
        source = repo / "source.py"
        source.write_bytes(b"disposable tracked source sentinel")
        subprocess.run(["git", "add", "source.py"], cwd=repo, check=True)
    else:
        source = repo / ".git" / "config"
    before = source_snapshot(source)

    code = module.main(["--repo", str(repo), "--artifact-dir", str(artifact_dir), "--out", str(source)])

    assert source_snapshot(source) == before
    assert code != 0
    captured = capsys.readouterr()
    assert "unsafe audit output" in captured.err.lower()
    assert "PASS" not in captured.out


def test_unique_temporary_file_preserves_symlink_target_and_allows_repo_outputs(
    tmp_path, monkeypatch
):
    module = load_auditor(monkeypatch)
    repo = disposable_repo(tmp_path / "repo")
    artifact_dir = tmp_path / "originals"
    artifact_dir.mkdir()
    original = artifact_dir / "original.zip"
    original.write_bytes(b"disposable original behind a temporary-file symlink")
    before = source_snapshot(original)
    output = repo / "outputs" / "audit.json"
    output.parent.mkdir()
    legacy_temporary = output.with_suffix(".json.part")
    legacy_temporary.symlink_to(original)

    code = module.main(["--repo", str(repo), "--artifact-dir", str(artifact_dir), "--out", str(output)])

    assert source_snapshot(original) == before
    assert legacy_temporary.is_symlink()
    assert code != 0
    assert output.is_file() and not output.is_symlink()
    receipt = json.loads(output.read_text())
    assert receipt["status"] == "FAIL_OR_INCOMPLETE"
    assert "actual complete ZIP set differs" in receipt["failures"][0]["message"]
    assert "totals" not in receipt
    assert sorted(p.name for p in output.parent.iterdir()) == ["audit.json", "audit.json.part"]
