#!/usr/bin/env python3
"""Recover the public Hiraiwa-Ushimaru 2017 Dryad workbook by individual file.

The legacy dataset bulk-download endpoint may require API authentication. This utility
uses anonymous public metadata (dataset versions -> version files) to locate the exact
published file, then tries the file's own public download routes. No biological matching,
imputation, or downstream outcome selection occurs here.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

DOI = "10.5061/dryad.pm29d"
EXPECTED_FILE = "primary_data.xlsx"
BASE = "https://datadryad.org"
API = f"{BASE}/api/v2"


def request(url: str, *, accept: str = "application/json, */*;q=0.8", timeout: int = 90) -> tuple[bytes, dict[str, str], str]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "izu-core-source-audit/1.0 (+https://github.com/zuizui0223/izu-core)",
            "Accept": accept,
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return (
            response.read(),
            {str(k).lower(): str(v) for k, v in response.headers.items()},
            str(response.geturl()),
        )


def absolute(href: str) -> str:
    return urllib.parse.urljoin(BASE, href)


def get_json(url: str, audit: list[dict[str, Any]], route: str) -> dict[str, Any]:
    row: dict[str, Any] = {"route": route, "url": url}
    try:
        payload, headers, final_url = request(url, accept="application/json")
        data = json.loads(payload.decode("utf-8"))
        row.update(
            {
                "status": "success",
                "final_url": final_url,
                "content_type": headers.get("content-type", ""),
                "size_bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
        )
        audit.append(row)
        return data
    except Exception as exc:
        row.update({"status": "failed", "error": f"{type(exc).__name__}: {exc}"})
        audit.append(row)
        raise


def is_xlsx(payload: bytes) -> bool:
    if not zipfile.is_zipfile(io.BytesIO(payload)):
        return False
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        names = set(archive.namelist())
    return "[Content_Types].xml" in names and "xl/workbook.xml" in names


def extract_workbook(path: Path, outdir: Path) -> dict[str, Any]:
    import openpyxl

    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    sheet_dir = outdir / "sheets"
    sheet_dir.mkdir(parents=True, exist_ok=True)
    sheets: list[dict[str, Any]] = []
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in ws.title).strip("_") or "sheet"
        csv_path = sheet_dir / f"{safe}.csv"
        with csv_path.open("w", encoding="utf-8", newline="") as handle:
            csv.writer(handle).writerows(rows)
        sheets.append(
            {
                "sheet": ws.title,
                "n_rows": len(rows),
                "n_columns_max": max((len(row) for row in rows), default=0),
                "csv": str(csv_path.relative_to(outdir)),
                "preview": [list(row) for row in rows[:6]],
            }
        )
    wb.close()
    return {"sheets": sheets}


def embedded(data: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = data.get("_embedded", {}).get(key, [])
    return value if isinstance(value, list) else []


def link_href(row: dict[str, Any], key: str) -> str:
    return str(row.get("_links", {}).get(key, {}).get("href") or "")


def id_from_row_or_links(row: dict[str, Any], kind: str) -> int | None:
    value = row.get("id")
    if value is not None:
        try:
            return int(value)
        except (TypeError, ValueError):
            pass
    patterns = {
        "version": r"/(?:api/v2/)?versions/(\d+)(?:/|$)",
        "file": r"/(?:api/v2/)?files/(\d+)(?:/|$)|/(?:stash/)?downloads/file_stream/(\d+)(?:/|$)",
    }
    hrefs = [str(v.get("href") or "") for v in row.get("_links", {}).values() if isinstance(v, dict)]
    for href in hrefs:
        match = re.search(patterns[kind], href)
        if match:
            for group in match.groups():
                if group is not None:
                    return int(group)
    return None


def write_blocked(outdir: Path, *, status: str, audit: list[dict[str, Any]], extra: dict[str, Any]) -> None:
    result = {
        "contract": "hiraiwa_ushimaru_2017_dryad_individual_file_recovery_v2",
        "dataset_doi": DOI,
        "target_file": EXPECTED_FILE,
        "status": status,
        **extra,
        "audit": audit,
        "claim_boundary": (
            "Source acquisition only. No biological mapping or downstream outcome is used. "
            "A blocked transport route is not evidence that the published data are absent."
        ),
    }
    (outdir / "dryad_recovery_audit.json").write_text(json.dumps(result, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    (outdir / "dryad_recovery_summary.md").write_text(
        "# Hiraiwa-Ushimaru 2017 Dryad individual-file recovery\n\n"
        f"Status: **{status}**\n\n"
        + "\n".join(f"- `{row.get('route')}` — `{row.get('status')}` — {row.get('url', '')}" for row in audit)
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    outdir = args.output_dir
    outdir.mkdir(parents=True, exist_ok=True)
    audit: list[dict[str, Any]] = []

    encoded = urllib.parse.quote(f"doi:{DOI}", safe="")
    versions_url = f"{API}/datasets/{encoded}/versions?per_page=100"
    versions = get_json(versions_url, audit, "dryad_versions_metadata")
    version_rows = embedded(versions, "stash:versions")
    if not version_rows:
        write_blocked(outdir, status="blocked_no_public_version_metadata", audit=audit, extra={})
        return

    version = version_rows[-1]
    files_href = link_href(version, "stash:files")
    version_id = id_from_row_or_links(version, "version")
    if not files_href:
        write_blocked(
            outdir,
            status="blocked_legacy_version_missing_files_link",
            audit=audit,
            extra={"selected_version_id": version_id, "selected_version_metadata": version},
        )
        return

    files_url = absolute(files_href)
    files = get_json(files_url, audit, "dryad_version_files_metadata")
    file_rows = embedded(files, "stash:files")
    (outdir / "dryad_versions.json").write_text(json.dumps(versions, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (outdir / "dryad_files.json").write_text(json.dumps(files, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if not file_rows:
        write_blocked(
            outdir,
            status="blocked_no_public_file_metadata",
            audit=audit,
            extra={"selected_version_id": version_id, "files_url": files_url},
        )
        return

    targets = [row for row in file_rows if Path(str(row.get("path") or row.get("name") or "")).name == EXPECTED_FILE]
    if len(targets) != 1:
        write_blocked(
            outdir,
            status="blocked_target_file_not_unique",
            audit=audit,
            extra={
                "selected_version_id": version_id,
                "n_target_file_matches": len(targets),
                "public_file_paths": [str(row.get("path") or row.get("name") or "") for row in file_rows],
            },
        )
        return

    target = targets[0]
    file_id = id_from_row_or_links(target, "file")
    link_download = link_href(target, "stash:download")
    candidates: list[tuple[str, str]] = []
    if link_download:
        candidates.append(("metadata_stash_download", absolute(link_download)))
    if file_id is not None:
        candidates.extend(
            [
                ("api_file_download", f"{API}/files/{file_id}/download"),
                ("stash_file_stream", f"{BASE}/stash/downloads/file_stream/{file_id}"),
                ("public_file_stream", f"{BASE}/downloads/file_stream/{file_id}"),
            ]
        )

    workbook_path: Path | None = None
    accepted: dict[str, Any] | None = None
    seen: set[str] = set()
    for route, url in candidates:
        if url in seen:
            continue
        seen.add(url)
        row: dict[str, Any] = {"route": route, "url": url, "file_id": file_id}
        try:
            payload, headers, final_url = request(
                url,
                accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/octet-stream, */*;q=0.5",
            )
            row.update(
                {
                    "status": "fetched",
                    "final_url": final_url,
                    "content_type": headers.get("content-type", ""),
                    "size_bytes": len(payload),
                    "sha256": hashlib.sha256(payload).hexdigest(),
                    "is_xlsx": is_xlsx(payload),
                }
            )
            if is_xlsx(payload):
                workbook_path = outdir / EXPECTED_FILE
                workbook_path.write_bytes(payload)
                row["status"] = "accepted_xlsx"
                accepted = row.copy()
                audit.append(row)
                break
            row["prefix_preview"] = payload[:160].decode("utf-8", errors="replace")
        except Exception as exc:
            row.update({"status": "failed", "error": f"{type(exc).__name__}: {exc}"})
        audit.append(row)

    extraction: dict[str, Any] = {}
    if workbook_path is not None:
        extraction = extract_workbook(workbook_path, outdir)

    status = "source_workbook_recovered" if workbook_path is not None else "blocked_public_metadata_only_download_not_recovered"
    result = {
        "contract": "hiraiwa_ushimaru_2017_dryad_individual_file_recovery_v2",
        "dataset_doi": DOI,
        "selected_version_id": version_id,
        "files_url": files_url,
        "target_file": EXPECTED_FILE,
        "target_file_id": file_id,
        "target_file_metadata": target,
        "status": status,
        "accepted_source": accepted,
        "extraction": extraction,
        "audit": audit,
        "claim_boundary": (
            "Source acquisition only. The workbook may contain interaction and reproductive variables, but no downstream outcome is used to choose or redefine the signed functional-position mapping. "
            "Plant-specific pollinator centers remain closed until the exact interaction-count columns and compatible site/plant units are audited."
        ),
    }
    (outdir / "dryad_recovery_audit.json").write_text(json.dumps(result, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")

    lines = [
        "# Hiraiwa-Ushimaru 2017 Dryad individual-file recovery",
        "",
        f"Status: **{status}**",
        f"Version ID: `{version_id}`",
        f"File ID: `{file_id}`",
        f"Target: `{EXPECTED_FILE}`",
        "",
    ]
    if accepted:
        lines += [
            f"Accepted route: `{accepted['route']}`",
            f"SHA256: `{accepted['sha256']}`",
            f"Bytes: `{accepted['size_bytes']}`",
            f"Sheets: `{len(extraction.get('sheets', []))}`",
            "",
        ]
    lines += ["## Route audit", ""]
    for row in audit:
        lines.append(f"- `{row.get('route')}` — `{row.get('status')}` — {row.get('url', '')}")
    (outdir / "dryad_recovery_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "version_id": version_id, "file_id": file_id, "accepted": accepted, "sheets": extraction.get("sheets", [])}, indent=2, default=str))


if __name__ == "__main__":
    main()
