"""Technical fixtures for read-only fixed-B48 original-archive admission."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import zipfile

import pytest

from scripts.verify_chapter2_k48_shard18_source_20261014 import (
    EXPECTED_PROTOCOL_SHA256, EXPECTED_STATUS, MANIFEST_NAME, verify,
)


def fixture_archive(tmp_path: Path, *, corrupt_sidecar=False, extra_member=False):
    p = tmp_path / "synthetic_original.zip"
    cases = [f"synthetic_case_{i:02d}" for i in range(32)]
    manifest = {
        "history": 41110919, "shard": 18, "n_sources": 32,
        "n_futures": 1792, "status": EXPECTED_STATUS,
        "protocol_sha256": EXPECTED_PROTOCOL_SHA256, "case_keys": cases,
    }
    with zipfile.ZipFile(p, "w", compression=zipfile.ZIP_STORED) as zipf:
        zipf.writestr(MANIFEST_NAME, json.dumps(manifest))
        for i, case in enumerate(cases):
            raw = json.dumps({"case": case, "value": i}).encode()
            name = "k48_" + case
            zipf.writestr(name + ".json", raw)
            digest = hashlib.sha256(raw).hexdigest()
            zipf.writestr(name + ".sha256", "0" * 64 if corrupt_sidecar and i == 0 else digest)
        if extra_member:
            zipf.writestr("unexpected.json", "{}")
    data = p.read_bytes()
    return p, hashlib.sha256(data).hexdigest(), len(data)


def test_verified_original_format(tmp_path):
    p, sha, nbytes = fixture_archive(tmp_path)
    result = verify(p, expected_sha256=sha, expected_size=nbytes)
    assert result["json_sha256_sidecars_checked"] == 32
    assert result["zip_member_count"] == 65
    assert result["source_cases_declared"] == 32
    assert result["private_external_backup_restored"] is False
    assert result["doi_assigned"] is False


def test_rejects_archive_byte_drift(tmp_path):
    p, sha, nbytes = fixture_archive(tmp_path)
    with pytest.raises(ValueError, match="size or SHA-256"):
        verify(p, expected_sha256="0" * 64, expected_size=nbytes)


def test_rejects_sidecar_mismatch_even_when_zip_hash_matches(tmp_path):
    p, sha, nbytes = fixture_archive(tmp_path, corrupt_sidecar=True)
    with pytest.raises(ValueError, match="sidecar"):
        verify(p, expected_sha256=sha, expected_size=nbytes)


def test_rejects_extra_payload_even_when_zip_hash_matches(tmp_path):
    p, sha, nbytes = fixture_archive(tmp_path, extra_member=True)
    with pytest.raises(ValueError, match="member count"):
        verify(p, expected_sha256=sha, expected_size=nbytes)
