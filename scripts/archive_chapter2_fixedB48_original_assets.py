"""Preserve original fixed-B48 independent raw artifacts as a versioned draft release.

Executed only by a one-time production workflow. Downloads the 130 original
source/future artifact ZIPs and the corrected final scientific readout.
It NEVER invokes any population model, and cannot change scientific estimates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tarfile
import zipfile

ORIGINAL_PRODUCTION_RUN = 37896872795
CORRECTED_READOUT_RUN = 37900150213
EXPECTED_RUN_SHAS = {
    ORIGINAL_PRODUCTION_RUN: "2737736f1dca36c8b43e9ac6a9fbd862ca21165b",
    CORRECTED_READOUT_RUN: "592cdad7fa0442a26fd5e79a2fd94812d4515c5d",
}
READOUT_SHA256 = "a6f3aad995b561ef4613301857a4e92e24d2d2138d2c66d59a7a28e1bd902023"
EXPECTED_SOURCES = {f"chapter2-k48-t400-shard-{i}" for i in range(64)}
EXPECTED_FUTURES = {f"chapter2-k48-future-shard-{i}" for i in range(64)}
EXPECTED_OTHER = {
    "chapter2-k48-new64-t400-full-admission",
    "chapter2-fixedB48-64-history-114688-full-readout",
    "chapter2-fixedB48-64-history-114688-confirmatory-readout-corrected",
}
RELEASE_TAG = "chapter2-fixedB48-raw-20261009-v1"


def github_api(path: str):
    result = subprocess.run(
        ["gh", "api", path], check=True, capture_output=True, text=True,
    )
    return json.loads(result.stdout)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def check_runs_and_list():
    artifacts = []
    for run, expected_sha in EXPECTED_RUN_SHAS.items():
        r = github_api(f"repos/zuizui0223/izu-core/actions/runs/{run}")
        if r["head_sha"] != expected_sha or r["conclusion"] != "success":
            raise AssertionError(f"Source run SHA or success changed: {run}")
        page = 1
        while True:
            result = github_api(
                f"repos/zuizui0223/izu-core/actions/runs/{run}/artifacts?per_page=100&page={page}"
            )
            found = result["artifacts"]
            if page == 1:
                expected_total = 130 if run == ORIGINAL_PRODUCTION_RUN else 1
                if result["total_count"] != expected_total:
                    raise AssertionError(f"Original run artifact count changed: {run}")
            for a in found:
                if a["expired"] or a["workflow_run"]["id"] != run:
                    raise AssertionError(f"Expired or mismatched source artifact {a['id']}")
                name = a["name"]
                if not re.fullmatch(r"[a-zA-Z0-9_.-]+", name):
                    raise AssertionError("Unexpected artifact name")
                artifacts.append({
                    "name": name,
                    "artifact_id": a["id"],
                    "run_id": run,
                    "original_github_artifact_bytes": a["size_in_bytes"],
                    "created_at": a["created_at"],
                    "expires_at": a["expires_at"],
                })
            if len(found) < 100:
                break
            page += 1
    by_name = {r["name"] for r in artifacts}
    if (len(artifacts) != 131 or len(by_name) != 131
            or by_name != EXPECTED_SOURCES | EXPECTED_FUTURES | EXPECTED_OTHER):
        raise AssertionError("Missing, duplicate or extraneous source/future artifacts")
    return sorted(artifacts, key=lambda x: x["name"])


def archive_originals(root: Path):
    if not os.getenv("GH_TOKEN"):
        raise PermissionError("GitHub token missing")
    artifacts = check_runs_and_list()
    raw = root / "original-zips"
    raw.mkdir(parents=True, exist_ok=True)
    for i, r in enumerate(artifacts, 1):
        src = f"https://api.github.com/repos/zuizui0223/izu-core/actions/artifacts/{r['artifact_id']}/zip"
        file = raw / (r["name"] + ".zip")
        if not file.exists():
            subprocess.run([
                "curl", "--fail", "--silent", "--show-error", "--location",
                "--retry", "4", "-H", f"Authorization: Bearer {os.environ['GH_TOKEN']}",
                "-H", "Accept: application/vnd.github+json", src,
                "--output", str(file),
            ], check=True)
        with zipfile.ZipFile(file) as z:
            if z.testzip() is not None:
                raise AssertionError(f"Damaged original ZIP member: {r['name']}")
            if "chapter2-fixedB48-64-history-114688-confirmatory" in r["name"]:
                readouts = [n for n in z.namelist() if n.endswith(".json")]
                if len(readouts) != 1:
                    raise AssertionError("Original readout ZIP missing its single JSON")
                if hashlib.sha256(z.read(readouts[0])).hexdigest() != READOUT_SHA256:
                    raise AssertionError("Original scientific JSON checksum mismatch")
        r["downloaded_zip_bytes"] = file.stat().st_size
        r["downloaded_zip_sha256"] = sha256(file)
        r["release_asset_name"] = file.name
        if i % 16 == 0:
            print(f"Authenticated {i}/{len(artifacts)} original immutable artifact ZIPs", flush=True)

    manifest = {
        "archive_type": "PRESERVED_ORIGINAL_RAW_ARTIFACT_BYTES_NO_NEW_SIMULATION",
        "release_tag": RELEASE_TAG,
        "is_draft_release": True,
        "original_run_head_shas": EXPECTED_RUN_SHAS,
        "scientific_json_sha256": READOUT_SHA256,
        "independent_history_clusters": 64,
        "complete_diploid_sources": 2048,
        "full_future_trajectories": 114688,
        "total_artifacts": len(artifacts),
        "raw_original_sources": 64,
        "raw_original_future_shards": 64,
        "original_artifacts": artifacts,
        "scientific_verdict": "supported_controlled_demographic_K_moderation_at_fixed_B48",
        "scope": "Finite synthetic population model; does not establish natural island extinction or genetic mutation-order causality.",
        "note": "An unpublished draft release is a temporary durable GitHub copy, NOT a DOI-bearing research deposit.",
    }
    root.mkdir(parents=True, exist_ok=True)
    path = root / "fixedB48-original-artifacts-manifest.json"
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    tarpath = root / "chapter2-fixedB48-all-original-131-artifacts.tar"
    with tarfile.open(tarpath, "w") as tar:
        tar.add(path, arcname=path.name)
        for r in artifacts:
            file = raw / r["release_asset_name"]
            tar.add(file, arcname="raw-artifact-zips/" + file.name)
    receipt = {
        "tag": RELEASE_TAG,
        "manifest_sha256": sha256(path),
        "archive_sha256": sha256(tarpath),
        "archive_bytes": tarpath.stat().st_size,
        "source_artifacts": len(artifacts),
        "status": "READY_FOR_DRAFT_RELEASE_UPLOAD_VERIFIED_SOURCE_ARCHIVES",
    }
    (root / "fixedB48-archive-receipt.json").write_text(json.dumps(receipt, indent=2)+"\n")
    print(json.dumps(receipt), flush=True)
    return receipt


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--execute-archive", action="store_true")
    args = p.parse_args()
    if not args.execute_archive:
        raise PermissionError("Run only for explicit original full-archive preservation")
    archive_originals(args.out)


if __name__ == "__main__":
    main()
