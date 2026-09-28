#!/usr/bin/env python3
"""Recover the Tribulus Dryad dataset from its Zenodo mirror with MD5 locks."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


USER_AGENT = "izu-core-source-audit/1.0 (+https://github.com/zuizui0223/izu-core)"


def request_bytes(url: str, *, accept: str = "application/octet-stream,*/*;q=0.8") -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return response.read()
    except urllib.error.HTTPError as error:
        body = error.read(400).decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {error.code} {error.reason}: {body!r}") from error


def request_json(url: str) -> Any:
    return json.loads(request_bytes(url, accept="application/json").decode("utf-8"))


def safe_name(value: str) -> str:
    name = Path(str(value)).name
    name = re.sub(r"[^A-Za-z0-9._+() -]+", "_", name).strip(" ._")
    return name or "zenodo_file"


def checksum_md5(payload: bytes) -> str:
    return hashlib.md5(payload).hexdigest()  # noqa: S324 - source checksum verification only


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("config/tribulus_dryad_source.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/tribulus_dryad"))
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    expected = {str(key): str(value).casefold() for key, value in config["expected_zenodo_md5"].items()}
    record = request_json(str(config["zenodo_api_url"]))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    files_dir = args.output_dir / "files"
    files_dir.mkdir(parents=True, exist_ok=True)
    inventory = []
    errors = []
    seen = set()
    for item in record.get("files") or []:
        key = str(item.get("key") or item.get("filename") or "")
        if not key:
            continue
        links = item.get("links") or {}
        url = str(links.get("content") or links.get("self") or "")
        row = {"source_filename": key, "status": "not_expected"}
        if key not in expected:
            inventory.append(row)
            continue
        seen.add(key)
        try:
            payload = request_bytes(url)
            observed_md5 = checksum_md5(payload)
            if observed_md5 != expected[key]:
                raise RuntimeError(
                    f"MD5 mismatch for {key}: expected {expected[key]}, observed {observed_md5}"
                )
            target = files_dir / safe_name(key)
            target.write_bytes(payload)
            row.update(
                {
                    "status": "downloaded_checksum_verified",
                    "local_name": target.name,
                    "size_downloaded": len(payload),
                    "md5": observed_md5,
                    "sha256": hashlib.sha256(payload).hexdigest(),
                }
            )
        except Exception as error:
            row.update({"status": "download_failed", "error": repr(error)})
            errors.append({"source_filename": key, "error": repr(error)})
        inventory.append(row)
    missing = sorted(set(expected) - seen)
    verified = [
        row for row in inventory if row.get("status") == "downloaded_checksum_verified"
    ]
    status = (
        "zenodo_mirror_checksum_verified"
        if len(verified) == len(expected) and not missing
        else "zenodo_mirror_incomplete"
    )
    summary = {
        "schema_version": "1.0",
        "status": status,
        "acquisition_route": "zenodo_record_7551873_mirror_of_dryad_doi",
        "source_id": config["source_id"],
        "dataset_doi": config["dataset_doi"],
        "zenodo_record_id": record.get("id"),
        "n_source_files": len(expected),
        "n_downloaded": len(verified),
        "missing_expected_files": missing,
        "files": inventory,
        "errors": errors,
        "claim_boundary": config["claim_boundary"],
    }
    (args.output_dir / "source_inventory.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"verified: {len(verified)}/{len(expected)}")
    if status != "zenodo_mirror_checksum_verified":
        raise RuntimeError("Tribulus Zenodo mirror recovery incomplete")


if __name__ == "__main__":
    main()
