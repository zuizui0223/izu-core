#!/usr/bin/env python3
"""Acquire the Wanshan–Yongxing workbook across visible Dryad versions.

A DOI landing page can expose a stale file ID when a metadata-only latest
resource supersedes the resource that owns the public file. This resolver checks
all visible version/file links and accepts either a direct XLSX or a dataset ZIP
containing one unambiguous XLSX. Failure diagnostics are always written.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path
from typing import Any, Iterable

import acquire_wanshan_yongxing_dryad as legacy


def walk(value: object) -> Iterable[object]:
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def linked_ids(value: object, expression: str) -> list[int]:
    pattern = re.compile(expression)
    return sorted(
        {
            int(match.group(1))
            for item in walk(value)
            if isinstance(item, str)
            for match in pattern.finditer(item)
        },
        reverse=True,
    )


def version_ids(value: object) -> list[int]:
    ids = set(linked_ids(value, r"/versions/(\d+)(?:/|$)"))
    ids.update(
        int(item["id"])
        for item in walk(value)
        if isinstance(item, dict) and isinstance(item.get("id"), int)
    )
    return sorted(ids, reverse=True)


def file_ids(value: object, target_filename: str) -> list[int]:
    ids: set[int] = set()
    for item in walk(value):
        if not isinstance(item, dict):
            continue
        name = str(
            item.get("path")
            or item.get("name")
            or item.get("filename")
            or item.get("downloadFilename")
            or ""
        )
        if not (name == target_filename or name.casefold().endswith(".xlsx")):
            continue
        if isinstance(item.get("id"), int):
            ids.add(int(item["id"]))
        ids.update(linked_ids(item, r"/files/(\d+)(?:/|$)"))
    return sorted(ids, reverse=True)


def hrefs(value: object) -> list[str]:
    return list(
        dict.fromkeys(
            item
            for item in walk(value)
            if isinstance(item, str)
            and (
                "/downloads/file_stream/" in item
                or ("/api/v2/files/" in item and item.rstrip("/").endswith("download"))
            )
        )
    )


def zip_info_urls(value: object, target_filename: str) -> list[str]:
    """Extract target workbook URLs from an already-fetched zip-assembly response."""
    urls: list[str] = []
    rows = value if isinstance(value, list) else []
    for row in rows:
        if not isinstance(row, dict):
            continue
        filename = str(row.get("filename") or "")
        url = row.get("url")
        if isinstance(url, str) and (
            filename == target_filename or filename.casefold().endswith(".xlsx")
        ) and url not in urls:
            urls.append(url)
    return urls


def add_unique(target: list[str], values: Iterable[str]) -> None:
    for value in values:
        if value and value not in target:
            target.append(value)


def extract_workbook(payload: bytes, target_filename: str) -> tuple[bytes, str, list[str]] | None:
    if legacy.is_xlsx(payload):
        return payload, "direct_xlsx", []
    try:
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            members = [name for name in archive.namelist() if name.casefold().endswith(".xlsx")]
            exact = [name for name in members if Path(name).name == target_filename]
            selected = exact[0] if exact else (members[0] if len(members) == 1 else None)
            workbook = archive.read(selected) if selected else b""
    except zipfile.BadZipFile:
        return None
    return (workbook, "dataset_zip", members) if legacy.is_xlsx(workbook) else None


def get_json(opener: object, url: str, errors: list[dict[str, str]], stage: str) -> Any:
    try:
        return legacy.request_json(opener, url)
    except Exception as error:
        errors.append({"stage": stage, "url": url, "error": repr(error)})
        return {}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("config/wanshan_yongxing_dryad_source.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/wanshan_yongxing_dryad"))
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    opener = legacy.make_opener()
    errors: list[dict[str, str]] = []
    target = str(config["known_file"]["filename"])

    metadata = get_json(opener, str(config["api_dataset_url"]), errors, "metadata")
    versions = get_json(opener, str(config["api_versions_url"]), errors, "versions")
    linkset_url = str(config.get("linkset_json_url") or f"{str(config['landing_page_url']).rstrip('/')}/linkset.json")
    linkset = get_json(opener, linkset_url, errors, "linkset")

    resources = version_ids(versions)
    listings: dict[str, object] = {}
    zip_info: dict[str, object] = {}
    resolved_files: set[int] = set()
    candidates: list[str] = []

    for resource_id in resources:
        files_url = f"https://datadryad.org/api/v2/versions/{resource_id}/files"
        listing = get_json(opener, files_url, errors, "version_files")
        listings[str(resource_id)] = listing
        resolved_files.update(file_ids(listing, target))
        add_unique(candidates, hrefs(listing))

        info_url = f"https://datadryad.org/downloads/zip_assembly_info/{resource_id}.json"
        info = get_json(opener, info_url, errors, "zip_assembly_info")
        zip_info[str(resource_id)] = info
        add_unique(candidates, zip_info_urls(info, target))

    add_unique(candidates, legacy.extract_linkset_download_urls(linkset))
    for file_id in sorted(resolved_files, reverse=True):
        add_unique(candidates, (
            f"https://datadryad.org/downloads/file_stream/{file_id}",
            f"https://datadryad.org/stash/downloads/file_stream/{file_id}",
            f"https://datadryad.org/api/v2/files/{file_id}/download",
        ))
    for resource_id in resources:
        add_unique(candidates, (
            f"https://datadryad.org/downloads/download_resource/{resource_id}",
            f"https://datadryad.org/api/v2/versions/{resource_id}/download",
        ))
    add_unique(candidates, map(str, config.get("public_download_candidates", [])))

    workbook = None
    success_url = None
    container_kind = None
    container_members: list[str] = []
    container_sha = None
    for url in candidates:
        try:
            payload = legacy.request_bytes(
                opener,
                url,
                accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/zip,application/octet-stream;q=0.9,*/*;q=0.8",
                referer=str(config["landing_page_url"]),
            )
            extracted = extract_workbook(payload, target)
            if extracted is None:
                prefix = re.sub(r"\s+", " ", payload[:160].decode("utf-8", errors="replace"))
                raise ValueError(f"not an xlsx or unambiguous dataset zip; prefix={prefix!r}")
            workbook, container_kind, container_members = extracted
            success_url = url
            container_sha = hashlib.sha256(payload).hexdigest()
            break
        except Exception as error:
            errors.append({"stage": "download", "url": url, "error": repr(error)})

    diagnostic = {
        "source_id": config["source_id"],
        "article_doi": config["article_doi"],
        "dataset_doi": config["dataset_doi"],
        "resolved_version_ids": resources,
        "resolved_file_ids": sorted(resolved_files, reverse=True),
        "metadata": metadata,
        "versions": versions,
        "linkset": linkset,
        "file_listings": listings,
        "zip_assembly_info": zip_info,
        "download_candidates": candidates,
        "errors": errors,
        "claim_boundary": config["claim_boundary"],
    }
    (args.output_dir / "acquisition_diagnostics_v2.json").write_text(
        json.dumps(diagnostic, indent=2, ensure_ascii=False, default=str) + "\n",
        encoding="utf-8",
    )
    if workbook is None or success_url is None:
        raise RuntimeError("unable to acquire Dryad workbook; see acquisition_diagnostics_v2.json")

    destination = args.output_dir / target
    destination.write_bytes(workbook)
    inventory = {
        **diagnostic,
        "successful_download_url": success_url,
        "filename": target,
        "size_downloaded": len(workbook),
        "sha256": hashlib.sha256(workbook).hexdigest(),
        "source_container_kind": container_kind,
        "source_container_members": container_members,
        "source_container_sha256": container_sha,
        **legacy.workbook_preview(destination),
    }
    inventory_text = json.dumps(inventory, indent=2, ensure_ascii=False, default=str) + "\n"
    (args.output_dir / "source_inventory.json").write_text(inventory_text, encoding="utf-8")
    # Transitional compatibility for the materialization workflow; the canonical
    # consumer path is source_inventory.json.
    (args.output_dir / "source_inventory_v2.json").write_text(inventory_text, encoding="utf-8")
    print(f"downloaded: {destination}")
    print(f"sha256: {inventory['sha256']}")
    print(f"resource IDs: {resources}")
    print(f"file IDs: {sorted(resolved_files, reverse=True)}")


if __name__ == "__main__":
    main()
