from __future__ import annotations

import hashlib
import io
import json
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data/design/canary_trojelsgaard2015_weighted_source_map.json"
OUT_DIR = ROOT / "data/external/canary_trojelsgaard2015"
GATE = ROOT / "data/results/canary_trojelsgaard2015_weighted_source_gate.json"
ZENODO_RECORD = 4998598
ZENODO_API = f"https://zenodo.org/api/records/{ZENODO_RECORD}"


def get_bytes(url: str, timeout: int = 75) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "izu-core-source-audit/1.0", "Accept": "application/json,text/csv,application/zip,*/*"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def digest(data: bytes, algorithm: str = "sha256") -> str:
    h = hashlib.new(algorithm)
    h.update(data)
    return h.hexdigest()


def store_if_expected(name: str, data: bytes, expected: set[str], recovered: dict[str, dict]) -> bool:
    base = Path(name).name
    if base not in expected or len(data) < 20:
        return False
    path = OUT_DIR / base
    path.write_bytes(data)
    recovered[base] = {
        "bytes": len(data),
        "sha256": digest(data),
        "source_member": name,
    }
    return True


def unpack_archive(data: bytes, expected: set[str], recovered: dict[str, dict], label: str) -> None:
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            for member in archive.namelist():
                if Path(member).name in expected:
                    store_if_expected(member, archive.read(member), expected, recovered)
    except zipfile.BadZipFile:
        return


def main() -> None:
    config = json.loads(CONFIG.read_text())
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    GATE.parent.mkdir(parents=True, exist_ok=True)
    expected = {x["filename"] for x in config["site_files"]}
    recovered: dict[str, dict] = {}
    attempts: list[dict] = []
    zenodo_metadata: dict[str, object] = {"record_id": ZENODO_RECORD, "status": "not_checked"}

    # Primary: institutional Zenodo mirror explicitly linked from the dataset record.
    try:
        record = json.loads(get_bytes(ZENODO_API, timeout=30).decode("utf-8"))
        files = record.get("files", [])
        zenodo_metadata = {
            "record_id": ZENODO_RECORD,
            "status": "metadata_recovered",
            "title": record.get("metadata", {}).get("title") or record.get("title"),
            "n_files": len(files),
            "files": [
                {"key": f.get("key"), "size": f.get("size"), "checksum": f.get("checksum")}
                for f in files
            ],
        }
        for file_info in files:
            key = str(file_info.get("key") or "")
            links = file_info.get("links", {}) or {}
            urls = [links.get("content"), links.get("download"), links.get("self")]
            urls.append(
                f"https://zenodo.org/records/{ZENODO_RECORD}/files/{urllib.parse.quote(key)}?download=1"
            )
            for url in [u for u in urls if u]:
                try:
                    data = get_bytes(url)
                    attempts.append({"route": "zenodo_mirror", "key": key, "url": url, "status": "success", "bytes": len(data)})
                    if key in expected:
                        store_if_expected(key, data, expected, recovered)
                    else:
                        unpack_archive(data, expected, recovered, key)
                    break
                except Exception as exc:
                    attempts.append({"route": "zenodo_mirror", "key": key, "url": url, "status": "failed", "error": repr(exc)})
    except Exception as exc:
        zenodo_metadata = {"record_id": ZENODO_RECORD, "status": "metadata_failed_nonfatal", "error": repr(exc)}

    # Secondary: exact Dryad file IDs fixed from the official dataset page before metric inspection.
    for item in config["site_files"]:
        name = item["filename"]
        if name in recovered:
            continue
        file_id = int(item["dryad_file_id"])
        urls = [
            f"https://datadryad.org/downloads/file_stream/{file_id}",
            f"https://datadryad.org/stash/downloads/file_stream/{file_id}",
            f"https://datadryad.org/api/v2/files/{file_id}/download",
        ]
        for url in urls:
            try:
                data = get_bytes(url)
                if len(data) < 20:
                    raise RuntimeError(f"payload too small: {len(data)}")
                store_if_expected(name, data, expected, recovered)
                attempts.append({"route": "dryad_file_id", "file": name, "file_id": file_id, "url": url, "status": "success", "bytes": len(data)})
                break
            except Exception as exc:
                attempts.append({"route": "dryad_file_id", "file": name, "file_id": file_id, "url": url, "status": "failed", "error": repr(exc)})

    missing = sorted(expected - set(recovered))
    payload = {
        "schema_version": "1.0",
        "analysis": "canary_trojelsgaard2015_weighted_source_gate",
        "source_doi": config["source_doi"],
        "source_semantics": config["source_semantics"],
        "zenodo_mirror": zenodo_metadata,
        "expected_site_files": len(expected),
        "recovered_site_files": len(recovered),
        "recovered": recovered,
        "missing": missing,
        "download_attempts": attempts,
        "status": "all_preregistered_canary_weighted_site_files_recovered" if not missing else "partial_or_blocked_canary_weighted_source_recovery",
        "admission": "ready_for_preregistered_island_aggregation" if not missing else "weighted_tier_b_not_ready_for_all_canary_rows",
        "claim_boundary": "Source-byte gate only. No network is admitted by outcome fit. Missing file delivery is not biological absence; only recovered matrices may proceed to source-native aggregation.",
    }
    GATE.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
