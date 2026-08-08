#!/usr/bin/env python3
"""Acquire the frozen Hiraiwa-Ushimaru 2024 Figshare data and inventory it."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import urllib.request
import zipfile
from pathlib import Path


def request_bytes(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "izu-core-source-audit/1.0 (+https://github.com/zuizui0223/izu-core)",
            "Accept": "application/json, application/octet-stream;q=0.9, */*;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def safe_name(name: str) -> str:
    return "".join(ch if ch.isalnum() or ch in ".-_" else "_" for ch in name).strip("_") or "file"


def preview_csv(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8-sig", newline="", errors="replace") as handle:
        reader = csv.reader(handle)
        rows = []
        for index, row in enumerate(reader):
            rows.append(row)
            if index >= 4:
                break
    return {"preview": rows}


def preview_xlsx(path: Path) -> dict[str, object]:
    try:
        import openpyxl
    except ImportError:
        return {"preview_error": "openpyxl_not_installed"}
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    sheets = []
    for ws in wb.worksheets:
        rows = []
        for index, row in enumerate(ws.iter_rows(values_only=True)):
            rows.append(list(row))
            if index >= 4:
                break
        sheets.append({"sheet": ws.title, "preview": rows})
    wb.close()
    return {"sheet_previews": sheets}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("config/hiraiwa_ushimaru_figshare_source.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/hiraiwa_ushimaru_figshare"))
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = args.output_dir / "files"
    raw_dir.mkdir(parents=True, exist_ok=True)

    metadata = json.loads(request_bytes(str(config["api_url"])).decode("utf-8"))
    files = metadata.get("files") or []
    if not files:
        raise ValueError("Figshare article exposes no files")

    inventory = []
    for item in files:
        name = str(item.get("name") or f"file_{item.get('id')}")
        download_url = str(item.get("download_url") or "")
        if not download_url:
            raise ValueError(f"Figshare file lacks download_url: {name}")
        payload = request_bytes(download_url)
        destination = raw_dir / safe_name(name)
        destination.write_bytes(payload)
        row: dict[str, object] = {
            "id": item.get("id"),
            "name": name,
            "size_reported": item.get("size"),
            "size_downloaded": len(payload),
            "download_url": download_url,
            "sha256": hashlib.sha256(payload).hexdigest(),
            "supplied_md5": item.get("supplied_md5"),
        }
        suffix = destination.suffix.lower()
        if suffix in {".csv", ".tsv", ".txt"}:
            row.update(preview_csv(destination))
        elif suffix in {".xlsx", ".xlsm"}:
            row.update(preview_xlsx(destination))
        elif suffix == ".zip" or zipfile.is_zipfile(destination):
            extract_dir = args.output_dir / "extracted" / safe_name(destination.stem)
            extract_dir.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(destination) as archive:
                archive.extractall(extract_dir)
                row["archive_members"] = archive.namelist()
        inventory.append(row)

    summary = {
        "source_id": config["source_id"],
        "article_doi": config["article_doi"],
        "dataset_doi": config["dataset_doi"],
        "figshare_article_id": config["figshare_article_id"],
        "figshare_title": metadata.get("title"),
        "figshare_version": metadata.get("version"),
        "n_files": len(inventory),
        "files": inventory,
        "claim_boundary": (
            "Downloaded files are source-native network/pollination data. Interaction identity alone is not "
            "pollinator effectiveness, missing links are not biological absence, and contemporary network "
            "structure is not historical causal evidence."
        ),
    }
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8"
    )
    print(f"files: {len(inventory)}")
    for row in inventory:
        print(f"- {row['name']} ({row['size_downloaded']} bytes)")
    print(args.output_dir / "summary.json")


if __name__ == "__main__":
    main()
