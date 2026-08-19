from __future__ import annotations

import hashlib
import json
import urllib.parse
import urllib.request
from pathlib import Path

RECORD_ID = 4300427
API = f"https://zenodo.org/api/records/{RECORD_ID}"
TARGET_KEY = "network interaction data.txt"
# Published on the Zenodo v1 record page; used as a byte-integrity gate even if the API is rate-limited.
PUBLISHED_MD5 = "077f7a7f8648c54a25e637c7f8eaa09c"
PUBLISHED_SIZE_APPROX_MB = 18.5
OUT_DIR = Path("data/external/dore2021_zenodo_v1")
OUT_FILE = OUT_DIR / TARGET_KEY
INVENTORY = Path("data/results/dore2021_zenodo_v1_raw_interaction_source_gate.json")


def get_bytes(url: str, timeout: int = 75) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "izu-core-source-audit/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    INVENTORY.parent.mkdir(parents=True, exist_ok=True)
    direct = f"https://zenodo.org/records/{RECORD_ID}/files/{urllib.parse.quote(TARGET_KEY)}?download=1"
    legacy_direct = f"https://zenodo.org/record/{RECORD_ID}/files/{urllib.parse.quote(TARGET_KEY)}?download=1"
    state: dict[str, object] = {
        "schema_version": "1.1",
        "source": "Zenodo: A database of plant-pollinator networks",
        "record_id": RECORD_ID,
        "doi": "10.5281/zenodo.4300427",
        "version_role": "version_1_source_contemporaneous_with_dore2021_compilation",
        "target_file": TARGET_KEY,
        "published_record_md5": PUBLISHED_MD5,
        "published_record_size_approx_mb": PUBLISHED_SIZE_APPROX_MB,
        "status": "not_recovered",
        "download_attempts": [],
        "metadata_attempt": None,
        "claim_boundary": "Byte recovery and checksum lock only. Source rows are flower-visitor interactions; they are not pollinator-effectiveness observations or reproductive outcomes.",
    }

    # Primary: direct public file route. Do not make byte recovery depend on the rate-limited metadata API.
    urls = [direct, legacy_direct]
    for url in urls:
        try:
            payload = get_bytes(url)
            if len(payload) < 1024 * 1024:
                raise RuntimeError(f"payload too small for the published 18.5 MB source: {len(payload)} bytes")
            OUT_FILE.write_bytes(payload)
            actual_md5 = md5(OUT_FILE)
            if actual_md5.lower() != PUBLISHED_MD5.lower():
                OUT_FILE.unlink(missing_ok=True)
                raise RuntimeError(
                    f"md5 mismatch against published record: expected {PUBLISHED_MD5}, got {actual_md5}"
                )
            state["download_attempts"].append(
                {"url": url, "status": "success", "bytes": len(payload)}
            )
            state.update(
                {
                    "status": "raw_interaction_bytes_recovered",
                    "admission": "byte_and_published_checksum_locked_for_schema_audit",
                    "bytes": len(payload),
                    "md5": actual_md5,
                    "sha256": sha256(OUT_FILE),
                }
            )
            break
        except Exception as exc:
            state["download_attempts"].append(
                {"url": url, "status": "failed", "error": repr(exc)}
            )

    # Supplementary metadata audit only; failure here must not invalidate a checksum-locked public file.
    try:
        record = json.loads(get_bytes(API, timeout=25).decode("utf-8"))
        files = record.get("files", [])
        selected = next((f for f in files if f.get("key") == TARGET_KEY), None)
        state["metadata_attempt"] = {
            "status": "success",
            "record_title": record.get("metadata", {}).get("title") or record.get("title"),
            "record_file_count": len(files),
            "selected_file": None
            if selected is None
            else {
                "key": selected.get("key"),
                "size": selected.get("size"),
                "checksum": selected.get("checksum"),
                "links": selected.get("links", {}),
            },
        }
    except Exception as exc:
        state["metadata_attempt"] = {"status": "failed_nonblocking", "error": repr(exc)}

    if state["status"] != "raw_interaction_bytes_recovered":
        state["admission"] = "blocked_raw_interaction_byte_retrieval"
    INVENTORY.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(state, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
