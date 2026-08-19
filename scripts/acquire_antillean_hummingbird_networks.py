from __future__ import annotations

import hashlib
import json
import re
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

DOI = "10.5061/dryad.5770gm7"
API = "https://datadryad.org/api/v2"
ENCODED = urllib.parse.quote(f"doi:{DOI}", safe="")
DATASET_URL = f"{API}/datasets/{ENCODED}"


def get_json(url: str, timeout: int = 45) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "izu-core-source-audit/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def abs_api(href: str) -> str:
    if href.startswith("http"):
        return href
    return "https://datadryad.org" + href


def file_download_url(file_obj: dict) -> tuple[str | None, int | None]:
    links = file_obj.get("_links") or {}
    for key in ("stash:download", "download"):
        link = links.get(key)
        href = link.get("href") if isinstance(link, dict) else link
        if href:
            m = re.search(r"/files/(\d+)(?:/download)?", str(href))
            return abs_api(str(href)), (int(m.group(1)) if m else None)
    link = links.get("self")
    self_href = link.get("href") if isinstance(link, dict) else link
    if self_href:
        m = re.search(r"/files/(\d+)", str(self_href))
        if m:
            fid = int(m.group(1))
            return f"{API}/files/{fid}/download", fid
    fid = file_obj.get("id")
    if fid is not None:
        return f"{API}/files/{int(fid)}/download", int(fid)
    return None, None


def try_download(url: str, out: Path, timeout: int = 90) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/octet-stream", "User-Agent": "izu-core-source-audit/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
            final_url = r.geturl()
            ctype = r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as exc:
        return {"status": "blocked_download", "http_status": exc.code, "error": repr(exc), "url": url}
    except Exception as exc:
        return {"status": "blocked_download", "error": repr(exc), "url": url}
    if not data.startswith(b"PK"):
        return {"status": "invalid_payload", "bytes": len(data), "content_type": ctype, "url": url, "final_url": final_url}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    return {
        "status": "retrieved",
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "content_type": ctype,
        "url": url,
        "final_url": final_url,
        "path": str(out),
    }


def main() -> None:
    out_json = Path("data/results/antillean_hummingbird_network_source_gate.json")
    raw_zip = Path("data/external/antillean_hummingbird/Data_and_code.zip")
    payload: dict = {
        "source": "Dalsgaard et al. 2018 Antillean hummingbird networks",
        "doi": DOI,
        "dryad_dataset_url": "https://datadryad.org/dataset/doi%3A10.5061/dryad.5770gm7",
        "purpose": "Recover the eight raw weighted Antillean hummingbird-plant matrices for the preregistered fourth geographic stratum without inspecting ABM fit.",
        "selection_boundary": "Dominica/Grenada are considered because the Caribbean stratum was preregistered before this recovery and their volcanic-arc geology is independently supported; no network outcome is used for admission.",
    }
    try:
        ds = get_json(DATASET_URL)
        payload["dataset_metadata"] = {
            "identifier": ds.get("identifier"),
            "title": ds.get("title"),
            "versionNumber": ds.get("versionNumber"),
            "storageSize": ds.get("storageSize"),
        }
        version_href = ((ds.get("_links") or {}).get("stash:version") or {}).get("href")
        if not version_href:
            raise RuntimeError("Dryad dataset metadata lacks stash:version link")
        version_url = abs_api(version_href)
        version = get_json(version_url)
        version_id = version.get("id")
        if version_id is None:
            version_id = int(version_url.rstrip("/").split("/")[-1])
        files_url = f"{API}/versions/{version_id}/files"
        files_resp = get_json(files_url)
        files = files_resp.get("_embedded", {}).get("stash:files", files_resp.get("files", []))
        payload["version_id"] = version_id
        file_rows = []
        for f in files:
            dl_url, fid = file_download_url(f)
            file_rows.append({
                "id": fid,
                "path": f.get("path"),
                "size": f.get("size"),
                "mimeType": f.get("mimeType"),
                "digest": f.get("digest"),
                "api_download_url_resolved": dl_url,
                "public_stream_url": f"https://datadryad.org/downloads/file_stream/{fid}" if fid is not None else None,
            })
        payload["files"] = file_rows
        target = next((f for f in files if str(f.get("path", "")).lower() == "data_and_code.zip"), None)
        if target is None:
            payload["admission"] = {"status": "target_file_not_found", "raw_matrices_recovered": False}
        else:
            api_download_url, file_id = file_download_url(target)
            payload["resolved_target_file_id"] = file_id
            attempts = []
            dl = {"status": "download_link_not_resolved"}
            if api_download_url:
                dl = try_download(api_download_url, raw_zip)
                attempts.append({"route": "dryad_api_file_download", **dl})
            if dl.get("status") != "retrieved" and file_id is not None:
                public_url = f"https://datadryad.org/downloads/file_stream/{file_id}"
                dl = try_download(public_url, raw_zip)
                attempts.append({"route": "dryad_public_file_stream", **dl})
            payload["download_attempts"] = attempts
            payload["download"] = dl
            if dl.get("status") == "retrieved":
                with zipfile.ZipFile(raw_zip) as zf:
                    names = zf.namelist()
                    web_files = [n for n in names if "/webs/" in n.lower() and not n.endswith("/")]
                    manifest = []
                    for name in web_files:
                        data = zf.read(name)
                        manifest.append({
                            "path": name,
                            "bytes": len(data),
                            "sha256": hashlib.sha256(data).hexdigest(),
                        })
                payload["zip_manifest"] = names
                payload["web_matrix_files"] = manifest
                payload["admission"] = {
                    "status": "raw_webs_recovered_pending_island_mapping",
                    "raw_matrices_recovered": len(manifest) > 0,
                    "n_web_matrix_files": len(manifest),
                }
            else:
                payload["admission"] = {
                    "status": "download_blocked_pending_alternate_public_route",
                    "raw_matrices_recovered": False,
                }
    except Exception as exc:
        payload["admission"] = {"status": "source_gate_failed", "raw_matrices_recovered": False}
        payload["error"] = repr(exc)

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
