from __future__ import annotations

import hashlib
import json
import urllib.parse
import urllib.request
from pathlib import Path

RECORD_ID = 4300427
API = f"https://zenodo.org/api/records/{RECORD_ID}"
TARGET_KEY = "network interaction data.txt"
OUT_DIR = Path("data/external/dore2021_zenodo_v1")
OUT_FILE = OUT_DIR / TARGET_KEY
INVENTORY = Path("data/results/dore2021_zenodo_v1_raw_interaction_source_gate.json")


def get_bytes(url: str, timeout: int = 180) -> bytes:
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
    state: dict[str, object] = {
        "schema_version": "1.0",
        "source": "Zenodo: A database of plant-pollinator networks",
        "record_id": RECORD_ID,
        "doi": "10.5281/zenodo.4300427",
        "version_role": "version_1_source_contemporaneous_with_dore2021_compilation",
        "target_file": TARGET_KEY,
        "status": "not_recovered",
        "download_attempts": [],
        "claim_boundary": "Byte recovery and checksum lock only. Source rows are flower-visitor interactions; they are not pollinator-effectiveness observations or reproductive outcomes.",
    }
    try:
        record = json.loads(get_bytes(API).decode("utf-8"))
        state["record_title"] = record.get("metadata", {}).get("title") or record.get("title")
        files = record.get("files", [])
        state["record_file_count"] = len(files)
        selected = next((f for f in files if f.get("key") == TARGET_KEY), None)
        if selected is None:
            raise RuntimeError(f"{TARGET_KEY!r} absent from Zenodo record")
        checksum = str(selected.get("checksum") or "")
        expected_md5 = checksum.split(":", 1)[1] if checksum.startswith("md5:") else None
        state["zenodo_file_metadata"] = {
            "key": selected.get("key"),
            "size": selected.get("size"),
            "checksum": checksum,
            "links": selected.get("links", {}),
        }
        urls = []
        links = selected.get("links", {}) or {}
        for key in ("content", "download", "self"):
            value = links.get(key)
            if value:
                urls.append(value)
        urls.append(
            f"https://zenodo.org/records/{RECORD_ID}/files/{urllib.parse.quote(TARGET_KEY)}?download=1"
        )
        seen = set()
        for url in urls:
            if url in seen:
                continue
            seen.add(url)
            try:
                payload = get_bytes(url)
                if len(payload) < 1024:
                    raise RuntimeError(f"payload too small: {len(payload)} bytes")
                OUT_FILE.write_bytes(payload)
                actual_md5 = md5(OUT_FILE)
                if expected_md5 and actual_md5.lower() != expected_md5.lower():
                    OUT_FILE.unlink(missing_ok=True)
                    raise RuntimeError(
                        f"md5 mismatch: expected {expected_md5}, got {actual_md5}"
                    )
                state["download_attempts"].append(
                    {"url": url, "status": "success", "bytes": len(payload)}
                )
                state.update(
                    {
                        "status": "raw_interaction_bytes_recovered",
                        "admission": "byte_and_checksum_locked_for_schema_audit",
                        "bytes": len(payload),
                        "md5": actual_md5,
                        "sha256": sha256(OUT_FILE),
                    }
                )
                break
            except Exception as exc:  # source gate must preserve route failures
                state["download_attempts"].append(
                    {"url": url, "status": "failed", "error": repr(exc)}
                )
        if state["status"] != "raw_interaction_bytes_recovered":
            state["admission"] = "blocked_raw_interaction_byte_retrieval"
    except Exception as exc:
        state["fatal_metadata_or_source_error"] = repr(exc)
        state["admission"] = "blocked_raw_interaction_source_resolution"
    INVENTORY.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(state, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
