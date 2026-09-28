from __future__ import annotations

import csv
import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

DOI = "10.5061/dryad.fv94v"
API = "https://datadryad.org/api/v2"
EXPECTED = "Weigelt_etal_2013_PNAS_islanddata.csv"
LEGACY_FILE_ID = 85841
OUT = Path("data/results/weigelt2013_global_island_attribute_source_gate.json")
RAW = Path("data/external/weigelt2013/Weigelt_etal_2013_PNAS_islanddata.csv")


def request_json(url: str, timeout: int = 45) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "izu-core-source-audit/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def fetch_bytes(url: str, timeout: int = 90) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "text/csv,*/*", "User-Agent": "izu-core-source-audit/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
            return {
                "status": "retrieved",
                "url": url,
                "final_url": r.geturl(),
                "content_type": r.headers.get("Content-Type", ""),
                "bytes": len(data),
                "data": data,
            }
    except urllib.error.HTTPError as exc:
        return {"status": "blocked", "url": url, "http_status": exc.code, "error": repr(exc)}
    except Exception as exc:
        return {"status": "blocked", "url": url, "error": repr(exc)}


def is_csv_payload(data: bytes) -> bool:
    if len(data) < 1000:
        return False
    head = data[:500].decode("utf-8", errors="replace").lower()
    return "<html" not in head and "," in head and "area" in head


def main() -> None:
    payload: dict = {
        "source": "Weigelt, Jetz & Kreft 2013 global island physical/bioclimatic data",
        "doi": DOI,
        "expected_file": EXPECTED,
        "purpose": "Provide one common definition of island distance-to-mainland, area and elevation for the frozen global oceanic-island validation sample before named-system ABM fit.",
        "selection_boundary": "This source is chosen for globally standardized island geography, not because of any ABM or network outcome.",
    }

    resolved_ids: list[int] = []
    metadata_errors = []
    try:
        encoded = urllib.parse.quote(f"doi:{DOI}", safe="")
        ds = request_json(f"{API}/datasets/{encoded}")
        payload["dataset_metadata"] = {
            "identifier": ds.get("identifier"),
            "title": ds.get("title"),
            "versionNumber": ds.get("versionNumber"),
            "storageSize": ds.get("storageSize"),
        }
        version_href = ((ds.get("_links") or {}).get("stash:version") or {}).get("href")
        if version_href:
            version_url = version_href if version_href.startswith("http") else "https://datadryad.org" + version_href
            version = request_json(version_url)
            version_id = version.get("id") or int(version_url.rstrip("/").split("/")[-1])
            files = request_json(f"{API}/versions/{version_id}/files").get("_embedded", {}).get("stash:files", [])
            payload["version_id"] = version_id
            payload["files"] = []
            for f in files:
                self_href = ((f.get("_links") or {}).get("self") or {}).get("href", "")
                fid = f.get("id")
                if fid is None and self_href:
                    try:
                        fid = int(self_href.rstrip("/").split("/")[-1])
                    except ValueError:
                        pass
                payload["files"].append({
                    "id": fid,
                    "path": f.get("path"),
                    "size": f.get("size"),
                    "mimeType": f.get("mimeType"),
                    "digest": f.get("digest"),
                })
                if str(f.get("path", "")).lower() == EXPECTED.lower() and isinstance(fid, int):
                    resolved_ids.append(fid)
    except Exception as exc:
        metadata_errors.append(repr(exc))

    if LEGACY_FILE_ID not in resolved_ids:
        resolved_ids.append(LEGACY_FILE_ID)

    urls = []
    for fid in resolved_ids:
        urls.extend([
            f"{API}/files/{fid}/download",
            f"https://datadryad.org/downloads/file_stream/{fid}",
            f"https://datadryad.org/stash/downloads/file_stream/{fid}",
        ])
    attempts = []
    selected = None
    for url in urls:
        result = fetch_bytes(url)
        attempts.append({k: v for k, v in result.items() if k != "data"})
        if result["status"] == "retrieved" and is_csv_payload(result["data"]):
            selected = result
            break
    payload["metadata_errors"] = metadata_errors
    payload["download_attempts"] = attempts

    if selected is None:
        payload["status"] = "global_island_attribute_bytes_not_recovered"
        payload["admission"] = "blocked_common_geography_source_retrieval"
    else:
        data = selected["data"]
        RAW.parent.mkdir(parents=True, exist_ok=True)
        RAW.write_bytes(data)
        text = data.decode("utf-8-sig", errors="replace")
        reader = csv.DictReader(text.splitlines())
        preview = []
        n_rows = 0
        for row in reader:
            n_rows += 1
            if len(preview) < 5:
                preview.append(row)
        payload["status"] = "global_island_attribute_bytes_recovered"
        payload["retrieved"] = {
            "path": str(RAW),
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "source_url": selected["url"],
            "columns": reader.fieldnames,
            "n_rows": n_rows,
            "preview": preview,
        }
        payload["admission"] = "ready_for_frozen_candidate_coordinate_name_matching"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
