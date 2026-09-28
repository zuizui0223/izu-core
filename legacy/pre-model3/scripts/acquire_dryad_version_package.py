#!/usr/bin/env python3
"""Recover legacy Dryad source files from a version-package ZIP.

Some older Dryad records expose valid version/file metadata while their current
per-file streaming routes no longer deliver bytes. This fallback downloads the
version package, extracts only prespecified source components, and records
provenance on the extracted files. The assembled ZIP itself is treated only as
transport and is not assumed byte-stable.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

USER_AGENT = "izu-core-source-audit/1.0 (+https://github.com/zuizui0223/izu-core)"


def request_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/zip, application/octet-stream, */*;q=0.8"})
    with urllib.request.urlopen(req, timeout=120) as response:
        return response.read()


def safe_local_name(name: str) -> str:
    return "".join(ch if ch.isalnum() or ch in ".-_" else "_" for ch in name).strip("_") or "source_file"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", required=True, type=Path)
    ap.add_argument("--output-dir", required=True, type=Path)
    args = ap.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    url = str(config.get("version_package_url") or "")
    expected = [str(value) for value in config.get("expected_source_components") or []]
    if not url or not expected:
        raise ValueError("version_package_url and expected_source_components are required")

    payload = request_bytes(url)
    package_path = args.output_dir / "version_package.zip"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    package_path.write_bytes(payload)
    if not zipfile.is_zipfile(package_path):
        raise ValueError("Dryad version package is not a ZIP archive")

    raw_dir = args.output_dir / "files"
    raw_dir.mkdir(parents=True, exist_ok=True)
    expected_by_base = {PurePosixPath(name).name: name for name in expected}
    recovered: dict[str, dict[str, object]] = {}
    with zipfile.ZipFile(package_path) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            base = PurePosixPath(info.filename).name
            if base not in expected_by_base:
                continue
            data = archive.read(info)
            if not data:
                raise ValueError(f"empty source component in package: {base}")
            local_name = safe_local_name(base)
            destination = raw_dir / local_name
            destination.write_bytes(data)
            recovered[base] = {
                "source_filename": base,
                "archive_member": info.filename,
                "local_name": local_name,
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }

    missing = [name for name in expected if PurePosixPath(name).name not in recovered]
    if missing:
        raise ValueError(f"version package missing expected source components: {missing}")

    report = {
        "status": "acquired_via_version_package",
        "source_id": config["source_id"],
        "dataset_doi": config["dataset_doi"],
        "version_id": config.get("legacy_version_id"),
        "version_package_url": url,
        "package_transport": {
            "bytes": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
            "byte_stability": "not_assumed",
            "role": config.get("version_package_role", "transport_only"),
        },
        "n_expected": len(expected),
        "n_recovered": len(recovered),
        "files": [recovered[PurePosixPath(name).name] for name in expected],
        "claim_boundary": config["claim_boundary"],
    }
    (args.output_dir / "source_inventory.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
