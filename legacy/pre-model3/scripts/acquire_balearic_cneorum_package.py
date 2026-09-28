#!/usr/bin/env python3
"""Try public full-package Dryad routes for the legacy Cneorum dataset.

Dryad's current file API can require bearer auth even for a published legacy
record while the public landing page still exposes a full-dataset download.
This fallback tests only package routes and accepts bytes only when they form a
ZIP containing the seven source-native filenames declared in the config.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

USER_AGENT = "izu-core-source-audit/1.0 (+https://github.com/zuizui0223/izu-core)"


def fetch(url: str) -> tuple[bytes | None, dict[str, object]]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/zip, application/octet-stream;q=0.9, */*;q=0.5",
            "Cache-Control": "no-cache",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            payload = response.read()
            return payload, {
                "url": url,
                "status": getattr(response, "status", 200),
                "final_url": response.geturl(),
                "content_type": response.headers.get("Content-Type"),
                "bytes": len(payload),
            }
    except urllib.error.HTTPError as error:
        body = error.read(500).decode("utf-8", errors="replace")
        return None, {"url": url, "status": error.code, "error": body}
    except Exception as error:
        return None, {"url": url, "status": "request_failed", "error": repr(error)}


def zip_members(payload: bytes) -> list[str] | None:
    try:
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            return archive.namelist()
    except zipfile.BadZipFile:
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("config/balearic_cneorum_effectiveness_dryad_source.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/balearic_cneorum_effectiveness"))
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    files_dir = args.output_dir / "files"
    files_dir.mkdir(parents=True, exist_ok=True)
    expected = set(config["expected_source_components"])
    encoded = "doi%3A10.5061%2Fdryad.2ngf1vhj1"
    candidates = [
        f"https://datadryad.org/api/v2/datasets/{encoded}/download",
        "https://datadryad.org/api/v2/versions/36737/download",
        "https://datadryad.org/stash/downloads/download_dataset/36737",
    ]
    attempts = []
    success = None
    for url in candidates:
        payload, audit = fetch(url)
        if payload is None:
            attempts.append(audit)
            continue
        members = zip_members(payload)
        audit["sha256"] = hashlib.sha256(payload).hexdigest()
        audit["zip_members"] = members
        if members is None:
            audit["accepted"] = False
            audit["reason"] = "not_zip"
            attempts.append(audit)
            continue
        basenames = {Path(name).name for name in members if not name.endswith("/")}
        missing = sorted(expected - basenames)
        audit["missing_expected_files"] = missing
        if missing:
            audit["accepted"] = False
            audit["reason"] = "missing_expected_files"
            attempts.append(audit)
            continue
        audit["accepted"] = True
        attempts.append(audit)
        success = audit
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            for member in archive.infolist():
                if member.is_dir():
                    continue
                basename = Path(member.filename).name
                if basename in expected:
                    (files_dir / basename).write_bytes(archive.read(member))
        (args.output_dir / "cneorum_full_dataset.zip").write_bytes(payload)
        break

    report = {
        "source_id": config["source_id"],
        "dataset_doi": config["dataset_doi"],
        "expected_source_components": sorted(expected),
        "attempts": attempts,
        "status": "acquired" if success else "blocked_package_delivery",
        "successful_route": success,
        "claim_boundary": config["claim_boundary"],
    }
    (args.output_dir / "package_acquisition.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if success is None:
        raise RuntimeError("no public Dryad package route returned the seven expected files")


if __name__ == "__main__":
    main()
