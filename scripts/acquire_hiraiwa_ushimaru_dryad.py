#!/usr/bin/env python3
"""Acquire and unpack the frozen Hiraiwa-Ushimaru Izu pollination dataset."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import urllib.request
import zipfile
from pathlib import Path


def load_config(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = {"source_id", "dataset_doi", "download_url", "expected_workbook"}
    missing = sorted(required - set(data))
    if missing:
        raise ValueError("source config missing: " + ", ".join(missing))
    return data


def download(url: str, destination: Path) -> str:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "izu-core-source-audit/1.0 (+https://github.com/zuizui0223/izu-core)"},
    )
    with urllib.request.urlopen(request, timeout=120) as response, destination.open("wb") as handle:
        shutil.copyfileobj(response, handle)
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    return digest


def locate_workbook(downloaded: Path, expected_name: str, workdir: Path) -> Path:
    if zipfile.is_zipfile(downloaded):
        extract_dir = workdir / "extracted"
        extract_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(downloaded) as archive:
            archive.extractall(extract_dir)
        matches = list(extract_dir.rglob(expected_name))
        if len(matches) != 1:
            raise ValueError(f"expected exactly one {expected_name}, found {len(matches)}")
        return matches[0]
    if downloaded.suffix.lower() == ".xlsx":
        return downloaded
    raise ValueError("Dryad download is neither a zip archive nor an xlsx workbook")


def workbook_to_csv(workbook: Path, output_dir: Path) -> dict[str, object]:
    try:
        import openpyxl
    except ImportError as error:
        raise RuntimeError("openpyxl is required for workbook extraction") from error

    wb = openpyxl.load_workbook(workbook, read_only=True, data_only=True)
    sheet_dir = output_dir / "sheets"
    sheet_dir.mkdir(parents=True, exist_ok=True)
    sheets = []
    for sheet in wb.worksheets:
        safe_name = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in sheet.title).strip("_") or "sheet"
        rows = list(sheet.iter_rows(values_only=True))
        width = max((len(row) for row in rows), default=0)
        csv_path = sheet_dir / f"{safe_name}.csv"
        with csv_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerows(rows)
        preview = [list(row) for row in rows[:5]]
        sheets.append({
            "sheet": sheet.title,
            "csv": str(csv_path.relative_to(output_dir)),
            "n_rows": len(rows),
            "n_columns_max": width,
            "preview": preview,
        })
    wb.close()
    return {"sheets": sheets}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("config/hiraiwa_ushimaru_dryad_source.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/hiraiwa_ushimaru_dryad"))
    args = parser.parse_args()

    config = load_config(args.config)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    workdir = args.output_dir / "work"
    workdir.mkdir(parents=True, exist_ok=True)
    downloaded = workdir / "dryad_download.bin"
    digest = download(str(config["download_url"]), downloaded)
    workbook = locate_workbook(downloaded, str(config["expected_workbook"]), workdir)
    workbook_digest = hashlib.sha256(workbook.read_bytes()).hexdigest()
    extracted = workbook_to_csv(workbook, args.output_dir)

    summary = {
        "source_id": config["source_id"],
        "dataset_doi": config["dataset_doi"],
        "download_url": config["download_url"],
        "download_sha256": digest,
        "workbook_name": workbook.name,
        "workbook_sha256": workbook_digest,
        **extracted,
        "claim_boundary": (
            "This artifact exposes archived interaction-data structure only. Flower visits are not pollinator "
            "effectiveness, missing links are not biological absence, and the network snapshot is not a historical cause."
        ),
    }
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8"
    )
    print(f"workbook: {workbook.name}")
    print(f"sheets: {len(extracted['sheets'])}")
    print(args.output_dir / "summary.json")


if __name__ == "__main__":
    main()
