"""Intake guards use synthetic ZIPs, never historical biological evidence."""
import hashlib
import importlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import warnings
from zipfile import ZipFile, ZIP_STORED

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
MODULE = "scripts.audit_chapter2_discovery_archive_intake_20261011"
intake = importlib.import_module(MODULE)
DESIGN = "data/design/model3_replenishment_evolution_20261005.json"
RECEIPT = "data/results/model3_replenishment_archive_20261005.json"
NEAR = "outputs/model3_full_mutation_20261004/core_assurance_cost_u0.01_h76001_r7101_near"
FAR = "outputs/model3_persistent_isolation_20261005/persistent_core_assurance_cost_u0.01_h76001_r7101_far"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(data):
    return (json.dumps(data, indent=2) + "\n").encode()


def synthetic_arrays():
    """Hand-checked constant genomes: N48, means .5, variance0, one allele."""
    trace = np.zeros((1001, 10))
    trace[:, 0] = 48
    trace[:, 1:4] = .5
    trace[:, 7:] = 1
    return {"trace": trace, **{
        f"state_{year}": np.full((48, 3, 2), .5)
        for year in (0, 200, 400, 1000)
    }}


def npz_bytes(arrays):
    handle = io.BytesIO()
    np.savez_compressed(handle, **arrays)
    return handle.getvalue()


@pytest.fixture
def synthetic_archive(tmp_path, monkeypatch):
    """Only this test utility replaces the unavailable historical byte contract.

    The ZIP reader, manifest hashes, source hashes, receipts and array checks
    remain real. No synthetic pass is historical admission evidence.
    """
    plan = json.loads((ROOT / DESIGN).read_text())
    plan.update(history_seeds=[76001], demographic_repeats=[7101],
                distance_coordinates=[0.0, .25, 3.0], new_coordinates=[.25], new_cases=2)
    members = {
        path: b"# synthetic frozen embedded source\r\n" + path.encode()
        for path in plan["source_sha256"]
    }
    plan["source_sha256"] = {path: digest(data) for path, data in members.items()}
    members[DESIGN] = json_bytes(plan).replace(b"\n", b"\r\n")
    for setting in ("assurance_cost", "prior_selfing"):
        for arm in ("near", "far"):
            stem = (NEAR if arm == "near" else FAR).replace("assurance_cost", setting)
            members[stem + ".npz"] = npz_bytes(synthetic_arrays())
            members[stem + ".json"] = json_bytes({
                "task": ["abm", setting, .01, 76001, 7101, arm, 0, "jump", False],
                "sha256": digest(members[stem + ".npz"]),
            })
        # The historical intermediate writer stores trace only and four task
        # fields. Requiring endpoint checkpoints here would reject the archive.
        stem = f"outputs/model3_replenishment_evolution_20261005/{setting}_d0.25_h76001_r7101"
        members[stem + ".npz"] = npz_bytes({"trace": synthetic_arrays()["trace"]})
        members[stem + ".json"] = json_bytes({
            "task": [setting, .25, 76001, 7101],
            "sha256": digest(members[stem + ".npz"]),
        })

    def write(*, change_members=None, change_manifest=None, extra_entries=()):
        data = dict(members)
        if change_members:
            change_members(data)
        manifest = {"cases": 6, "files": [
            {"path": path, "sha256": digest(content), "bytes": len(content)}
            for path, content in sorted(data.items())
        ]}
        if change_manifest:
            change_manifest(manifest)
        path = tmp_path / "synthetic.zip"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with ZipFile(path, "w", compression=ZIP_STORED) as archive:
                for name, content in data.items():
                    archive.writestr(name, content)
                archive.writestr("ARCHIVE_MANIFEST.json", json_bytes(manifest))
                archive.writestr("RESTORE.txt", b"Synthetic test fixture, no historical evidence.\n")
                for name, content in extra_entries:
                    archive.writestr(name, content)
        receipt = {
            "status": "all_archive_members_read_back_and_hash_verified",
            "cases": 6, "members": len(members),
            "archive": "outputs/archives/model3_replenishment_evolution_20261005.zip",
            "bytes": path.stat().st_size, "sha256": digest(path.read_bytes()),
            "scope": "Synthetic engineering fixture only.",
        }
        monkeypatch.setattr(intake, "_load_contract", lambda: (plan, receipt), raising=False)
        return path

    return write


def rejected(report, code):
    assert report["status"] == "ARCHIVE_INTAKE_REJECTED"
    assert report["verification"]["discovery_endpoints_complete"] is False
    assert report["verification"]["original_discovery_full_replay_completed"] is False
    assert report["verification"]["runtime_identity_verified"] is False
    assert code in {failure["code"] for failure in report["failures"]}


def test_missing_archive_cli_writes_failure_receipt_and_returns_nonzero(tmp_path):
    # Removing missing-input handling must lose its machine-readable receipt.
    out = tmp_path / "reports" / "intake.json"
    result = subprocess.run(
        [sys.executable, "-m", MODULE, "--archive", str(tmp_path / "absent.zip"),
         "--out", str(out)], cwd=ROOT, capture_output=True, text=True,
    )
    assert out.exists(), "missing archive must still produce an intake report"
    report = json.loads(out.read_text())
    assert result.returncode == 2
    assert report["status"] == "ARCHIVE_UNAVAILABLE"
    assert report["verification"]["discovery_endpoints_complete"] is False
    assert report["verification"]["original_discovery_full_replay_completed"] is False
    assert report["counts"]["discovery_cases_verified"] == 0
    assert report == json.loads(result.stdout)


def test_wrong_outer_archive_identity_is_rejected_before_zip_use(tmp_path):
    # Trusting a self-consistent internal manifest cannot authenticate a bundle.
    archive = tmp_path / "untrusted.zip"
    archive.write_bytes(b"not a ZIP or the named historical archive")
    report = intake.audit_archive(archive)
    rejected(report, "archive_identity_mismatch")
    assert report["archive_identity"]["expected_bytes"] == 763914318
    assert report["archive_identity"]["expected_sha256"] == "37bd0bd312734715392add19f424696121fbe88517dfa784d8e702173ec71b6c"
    assert report["archive_identity"]["observed_sha256"] == digest(archive.read_bytes())
    assert report["counts"]["zip_members_verified"] == 0


@pytest.mark.parametrize("changed", [DESIGN, RECEIPT])
def test_modified_local_frozen_contract_cannot_redefine_admission(tmp_path, monkeypatch, changed):
    # A caller-edited plan/receipt must fail even if it remains valid JSON.
    for path in (DESIGN, RECEIPT):
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / path).read_bytes() + (b" " if path == changed else b""))
    monkeypatch.setattr(intake, "ROOT", tmp_path, raising=False)
    rejected(intake.audit_archive(tmp_path / "absent.zip"), "frozen_contract_mismatch")


@pytest.mark.parametrize("alias", ["same_path", "symlink", "hardlink"])
def test_cli_cannot_replace_archive_through_output_alias(tmp_path, capsys, alias):
    # Report writing must never overwrite its input, even through another name.
    archive = tmp_path / "archive.zip"
    original = b"preserve the supplied archive bytes"
    archive.write_bytes(original)
    out = archive if alias == "same_path" else tmp_path / "alias.json"
    if alias == "symlink":
        out.symlink_to(archive)
    elif alias == "hardlink":
        os.link(archive, out)
    assert intake.main(["--archive", str(archive), "--out", str(out)]) == 2
    report = json.loads(capsys.readouterr().out)
    rejected(report, "output_aliases_archive")
    assert archive.read_bytes() == original
    assert out.read_bytes() == original


@pytest.mark.parametrize("protected", [DESIGN, RECEIPT])
@pytest.mark.parametrize("alias", ["same_path", "symlink", "hardlink"])
def test_cli_cannot_replace_a_frozen_trust_anchor(tmp_path, monkeypatch, capsys, protected, alias):
    # An explicit report path must not destroy either trusted verifier input.
    local_root = tmp_path / "repository"
    for name in (DESIGN, RECEIPT):
        target = local_root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / name).read_bytes())
    anchor = local_root / protected
    original = anchor.read_bytes()
    out = anchor if alias == "same_path" else tmp_path / "alias.json"
    if alias == "symlink":
        out.symlink_to(anchor)
    elif alias == "hardlink":
        os.link(anchor, out)
    monkeypatch.setattr(intake, "ROOT", local_root)
    result = intake.main(["--archive", str(tmp_path / "absent.zip"), "--out", str(out)])
    assert out.read_bytes() == original, "report output replaced a protected trust-anchor alias"
    assert anchor.read_bytes() == original
    assert result == 2
    rejected(json.loads(capsys.readouterr().out), "output_aliases_trust_anchor")


def test_complete_synthetic_archive_includes_trace_only_intermediates_without_replay(synthetic_archive):
    # A verified fixture must close only the byte/endpoint gate, never replay.
    report = intake.audit_archive(synthetic_archive())
    assert report["status"] == "ARCHIVE_BYTES_AND_DISCOVERY_ENDPOINTS_VERIFIED"
    assert report["failures"] == []
    assert report["verification"]["discovery_endpoints_complete"] is True
    assert report["verification"]["manifest_complete"] is True
    assert report["verification"]["embedded_sources_verified"] is True
    assert report["verification"]["original_discovery_full_replay_completed"] is False
    assert report["verification"]["runtime_identity_verified"] is False
    assert report["counts"] == {
        "zip_members_verified": 38, "manifest_records_verified": 36,
        "embedded_sources_verified": 23, "discovery_cases_verified": 4,
        "genome_checkpoints_verified": 16,
    }
    assert report["coverage"]["mutation_rates_verified"] == [.01]
    assert report["coverage"]["mutation_zero_covered"] is False
    assert report["coverage"]["discovery_cases_expected"] == 4
    assert report["coverage"]["archive_cases_expected"] == 6
    assert report["trust_anchor"]["contract_files_verified"] is True


@pytest.mark.parametrize("corruption,code", [
    ("hash", "manifest_member_mismatch"),
    ("size", "manifest_member_mismatch"),
    ("duplicate", "duplicate_manifest_path"),
    ("undeclared", "manifest_member_set_mismatch"),
    ("cases", "manifest_case_count_mismatch"),
])
def test_manifest_cannot_hide_changed_or_incomplete_content(synthetic_archive, corruption, code):
    def change(manifest):
        if corruption == "hash":
            manifest["files"][0]["sha256"] = "0" * 64
        elif corruption == "size":
            manifest["files"][0]["bytes"] += 1
        elif corruption == "duplicate":
            manifest["files"][-1] = dict(manifest["files"][0])
        elif corruption == "undeclared":
            manifest["files"].pop()
        else:
            manifest["cases"] = 13312
    report = intake.audit_archive(synthetic_archive(change_manifest=change))
    rejected(report, code)


@pytest.mark.parametrize("path,code", [
    ("RESTORE.txt", "duplicate_zip_path"),
    ("../escape", "noncanonical_zip_path"),
    ("a/./b", "noncanonical_zip_path"),
    ("a\\b", "noncanonical_zip_path"),
])
def test_zip_paths_must_be_unique_and_canonical(synthetic_archive, path, code):
    rejected(intake.audit_archive(synthetic_archive(extra_entries=[(path, b"x")])), code)


@pytest.mark.parametrize("corruption,code", [
    ("missing_npz", "missing_case_members"),
    ("missing_receipt", "missing_case_members"),
    ("wrong_cohort", "missing_case_members"),
    ("task", "case_task_mismatch"),
    ("task_types", "case_task_mismatch"),
    ("sha", "case_receipt_sha_mismatch"),
])
def test_endpoint_admission_requires_the_exact_original_pair(synthetic_archive, corruption, code):
    def change(members):
        if corruption.startswith("missing_"):
            suffix = ".npz" if corruption == "missing_npz" else ".json"
            del members[FAR + suffix]
        elif corruption == "wrong_cohort":
            for suffix in (".npz", ".json"):
                members[FAR.replace("76001", "26100601") + suffix] = members.pop(FAR + suffix)
        else:
            receipt = json.loads(members[FAR + ".json"])
            if corruption == "task":
                receipt["task"][5] = "near"
            elif corruption == "task_types":
                receipt["task"][8] = 0
            else:
                receipt["sha256"] = "0" * 64
            members[FAR + ".json"] = json_bytes(receipt)
    rejected(intake.audit_archive(synthetic_archive(change_members=change)), code)


@pytest.mark.parametrize("corruption,code", [
    ("missing_checkpoint", "invalid_case_arrays"),
    ("trace_shape", "invalid_case_arrays"),
    ("genome_shape", "invalid_case_arrays"),
    ("nan_genome", "invalid_case_arrays"),
    ("out_of_range", "invalid_case_arrays"),
    ("checkpoint_summary", "checkpoint_summary_mismatch"),
    ("occupied_nan", "invalid_case_arrays"),
    ("object_array", "invalid_case_arrays"),
])
def test_endpoint_arrays_require_original_shapes_and_consistent_checkpoints(synthetic_archive, corruption, code):
    def change(members):
        arrays = synthetic_arrays()
        if corruption == "missing_checkpoint":
            del arrays["state_400"]
        elif corruption == "trace_shape":
            arrays["trace"] = arrays["trace"][:1000]
        elif corruption == "genome_shape":
            arrays["state_400"] = np.full((48, 3), .5)
        elif corruption == "nan_genome":
            arrays["state_400"][0, 0, 0] = np.nan
        elif corruption == "out_of_range":
            arrays["state_400"][0, 0, 0] = 1.01
        elif corruption == "checkpoint_summary":
            arrays["state_400"][0, 0, 0] = .6
        elif corruption == "occupied_nan":
            arrays["trace"][201, 1] = np.nan
        else:
            arrays["state_400"] = arrays["state_400"].astype(object)
        members[FAR + ".npz"] = npz_bytes(arrays)
        receipt = json.loads(members[FAR + ".json"])
        receipt["sha256"] = digest(members[FAR + ".npz"])
        members[FAR + ".json"] = json_bytes(receipt)
    rejected(intake.audit_archive(synthetic_archive(change_members=change)), code)


@pytest.mark.parametrize("member", ["trace.npy", "state_400.npy"])
def test_non_npy_required_members_produce_machine_readable_cli_rejection(
    synthetic_archive, tmp_path, capsys, member,
):
    # np.load can return raw bytes for a non-NPY ZIP member; names alone do not
    # establish that each of the five required entries is an ndarray.
    def change(members):
        buffer = io.BytesIO()
        with ZipFile(io.BytesIO(members[FAR + ".npz"])) as original:
            with ZipFile(buffer, "w", compression=ZIP_STORED) as malformed:
                for info in original.infolist():
                    content = b"not a numpy array" if info.filename == member else original.read(info)
                    malformed.writestr(info.filename, content)
        members[FAR + ".npz"] = buffer.getvalue()
        receipt = json.loads(members[FAR + ".json"])
        receipt["sha256"] = digest(members[FAR + ".npz"])
        members[FAR + ".json"] = json_bytes(receipt)
    archive = synthetic_archive(change_members=change)
    out = tmp_path / "malformed-intake.json"
    try:
        result = intake.main(["--archive", str(archive), "--out", str(out)])
    except AttributeError as exc:
        pytest.fail(f"Malformed required member escaped the JSON failure boundary: {exc}")
    assert result == 2
    report = json.loads(out.read_text())
    rejected(report, "invalid_case_arrays")
    assert report["counts"]["discovery_cases_verified"] == 0
    assert report["counts"]["genome_checkpoints_verified"] == 0
    assert report == json.loads(capsys.readouterr().out)


def test_empty_population_preserves_original_nan_trace_convention(synthetic_archive):
    # Extinction is N0 plus NaN summaries and an empty diploid array, not zeros.
    def change(members):
        arrays = synthetic_arrays()
        arrays["trace"][200:, 0] = 0
        arrays["trace"][200:, 1:] = np.nan
        for year in (200, 400, 1000):
            arrays[f"state_{year}"] = np.empty((0, 3, 2))
        members[FAR + ".npz"] = npz_bytes(arrays)
        receipt = json.loads(members[FAR + ".json"])
        receipt["sha256"] = digest(members[FAR + ".npz"])
        members[FAR + ".json"] = json_bytes(receipt)
    report = intake.audit_archive(synthetic_archive(change_members=change))
    assert report["status"] == "ARCHIVE_BYTES_AND_DISCOVERY_ENDPOINTS_VERIFIED"
    assert report["counts"]["genome_checkpoints_verified"] == 16


@pytest.mark.parametrize("corruption,code", [
    ("source_bytes", "embedded_source_mismatch"),
    ("design_semantics", "embedded_design_mismatch"),
])
def test_updated_manifest_cannot_redefine_frozen_embedded_sources(synthetic_archive, corruption, code):
    def change(members):
        if corruption == "source_bytes":
            source = "scripts/model3_island/reproduction.py"
            members[source] = members[source].replace(b"\r\n", b"\n")
        else:
            plan = json.loads(members[DESIGN])
            plan["mutation_rate"] = 0.0
            members[DESIGN] = json_bytes(plan)
    rejected(intake.audit_archive(synthetic_archive(change_members=change)), code)
