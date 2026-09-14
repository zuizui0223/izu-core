from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v6_giannutri_source_gate_v1.json"
OUT = ROOT / "data/results/giannutri2025_zenodo_source_audit.json"
RAW_DIR = ROOT / "data/external/giannutri2025"
API = "https://zenodo.org/api/records/14855496"
USER_AGENT = "izu-core-source-audit/1.0"


def fetch_bytes(url: str) -> tuple[int | None, bytes | None, str | None]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            return int(response.status), response.read(), None
    except urllib.error.HTTPError as exc:
        return int(exc.code), None, str(exc)
    except Exception as exc:
        return None, None, f"{type(exc).__name__}: {exc}"


def decode_text(payload: bytes) -> tuple[str, str]:
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return payload.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    raise RuntimeError("text source could not be decoded")


def tabular_inventory(payload: bytes) -> dict:
    text, encoding = decode_text(payload)
    sample = text[:10000]
    delimiter = "\t"
    try:
        delimiter = csv.Sniffer().sniff(sample, delimiters="\t,;").delimiter
    except csv.Error:
        if ";" in text.splitlines()[0]:
            delimiter = ";"
        elif "," in text.splitlines()[0]:
            delimiter = ","
    rows = list(csv.reader(io.StringIO(text), delimiter=delimiter))
    if not rows:
        raise RuntimeError("empty tabular source")
    headers = [str(value).strip() for value in rows[0]]
    normalized = [re.sub(r"[^a-z0-9]+", "_", h.lower()).strip("_") for h in headers]
    roles = {
        "time": [h for h, n in zip(headers, normalized) if any(k in n for k in ("date", "day", "year"))],
        "condition": [h for h, n in zip(headers, normalized) if any(k in n for k in ("condition", "hive", "hb", "treatment"))],
        "plant": [h for h, n in zip(headers, normalized) if any(k in n for k in ("plant", "flower"))],
        "visitor": [h for h, n in zip(headers, normalized) if any(k in n for k in ("bee", "visitor", "pollinator", "species"))],
        "count_or_visit": [h for h, n in zip(headers, normalized) if any(k in n for k in ("visit", "count", "frequency", "abundance", "number"))],
    }
    return {"encoding": encoding, "delimiter_repr": repr(delimiter), "row_count_excluding_header": max(0, len(rows)-1), "column_count": len(headers), "headers": headers, "field_role_candidates": roles, "target_metrics_calculated": False}


def code_inventory(payload: bytes) -> dict:
    text, encoding = decode_text(payload)
    indicators = []
    for index, line in enumerate(text.splitlines(), start=1):
        lower = line.lower()
        if any(pattern in lower for pattern in ("network", "bipartite", "transect_data_for_overlap", "date", "condition", "hive", "group_by")):
            indicators.append({"line": index, "text": line[:300]})
    return {"encoding": encoding, "line_count": len(text.splitlines()), "structural_indicator_lines": indicators[:120], "target_metrics_calculated": False}


def candidate_file_urls(record_id: int, name: str) -> list[str]:
    api_quoted = urllib.parse.quote(name, safe="")
    path_quoted = urllib.parse.quote(name, safe="")
    return [
        f"https://zenodo.org/api/records/{record_id}/files/{api_quoted}/content",
        f"https://zenodo.org/records/{record_id}/files/{path_quoted}?download=1",
    ]


def main() -> None:
    design = json.loads(DESIGN.read_text())
    record_id = int(design["candidate_system"]["zenodo_record_id"])
    required = design["required_zenodo_files"]
    status, metadata_bytes, metadata_error = fetch_bytes(API)
    metadata_available = status == 200 and metadata_bytes is not None
    metadata = json.loads(metadata_bytes) if metadata_available else {}
    files = {row.get("key"): row for row in metadata.get("files", [])} if metadata_available else {}

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    records = []
    blocked: list[str] = []
    for name, expected_md5 in required.items():
        row = files.get(name) or {}
        links = row.get("links") or {}
        urls: list[str] = []
        for url in (links.get("content"), links.get("self"), *candidate_file_urls(record_id, name)):
            if url and str(url) not in urls:
                urls.append(str(url))
        record = {"name": name, "expected_md5": expected_md5, "metadata_checksum": row.get("checksum"), "metadata_size": row.get("size"), "candidate_urls": urls, "download_attempts": []}
        payload = None
        successful_url = None
        for url in urls:
            file_status, candidate, error = fetch_bytes(url)
            attempt = {"url": url, "http_status": file_status, "error": error}
            if file_status == 200 and candidate is not None:
                md5 = hashlib.md5(candidate).hexdigest()
                attempt["md5"] = md5
                attempt["checksum_match_expected"] = md5 == expected_md5
                if md5 == expected_md5:
                    payload, successful_url = candidate, url
                    record["download_attempts"].append(attempt)
                    break
            record["download_attempts"].append(attempt)
        if payload is None:
            record["checksum_match"] = False
            blocked.append(name)
            records.append(record)
            continue
        actual_md5 = hashlib.md5(payload).hexdigest()
        metadata_md5 = str(row.get("checksum") or "").removeprefix("md5:")
        record.update({"successful_download_url": successful_url, "bytes": len(payload), "md5": actual_md5, "sha256": hashlib.sha256(payload).hexdigest(), "checksum_match": True, "metadata_checksum_match": None if not metadata_md5 else actual_md5 == metadata_md5})
        (RAW_DIR / name).write_bytes(payload)
        if name.endswith(".txt") and name != "README.txt":
            record["schema_inventory"] = tabular_inventory(payload)
        elif name.endswith(".R"):
            record["code_inventory"] = code_inventory(payload)
        else:
            text, encoding = decode_text(payload)
            record["text_inventory"] = {"encoding": encoding, "line_count": len(text.splitlines()), "target_metrics_calculated": False}
        records.append(record)

    raw_records = {row["name"]: row for row in records if row.get("checksum_match") is True}
    overlap = raw_records.get("transect_data_for_overlap_analysis.txt", {}).get("schema_inventory", {})
    walking = raw_records.get("walking_transects_dataset.txt", {}).get("schema_inventory", {})
    code = raw_records.get("Code for Resource use and overlap analysis.R", {}).get("code_inventory", {})
    def roles_present(inv: dict) -> bool:
        roles = inv.get("field_role_candidates", {})
        return bool(roles.get("time")) and bool(roles.get("plant")) and bool(roles.get("visitor"))
    source_bytes_ok = len(raw_records) == len(required) and not blocked
    daily_structure_visible = roles_present(overlap) or roles_present(walking)
    condition_structure_visible = bool(overlap.get("field_role_candidates", {}).get("condition")) or bool(walking.get("field_role_candidates", {}).get("condition"))
    code_structure_visible = bool(code.get("structural_indicator_lines"))
    admission = source_bytes_ok and daily_structure_visible and condition_structure_visible and code_structure_visible
    result = {
        "schema_version": "1.2", "analysis": "giannutri2025_zenodo_source_audit",
        "status": "source_admitted_raw_daily_network_reconstruction_inputs" if admission else "blocked_giannutri_source_or_grouping_structure_incomplete",
        "zenodo_record_id": record_id, "zenodo_doi": design["candidate_system"]["zenodo_doi"],
        "metadata_available": metadata_available, "metadata_http_status": status, "metadata_error": metadata_error,
        "public_record_page_file_list_verified_separately": True,
        "direct_file_fallback_requires_preexisting_expected_md5": True,
        "required_file_count": len(required), "recovered_checksum_locked_file_count": len(raw_records), "blocked_files": sorted(set(blocked)), "files": records,
        "source_bytes_ok": source_bytes_ok, "daily_structure_visible": daily_structure_visible, "condition_structure_visible": condition_structure_visible, "code_structure_visible": code_structure_visible,
        "source_admission_succeeds": admission, "target_metrics_calculated": False,
        "published_scope": design["candidate_system"]["published_network_scope"], "published_daily_network_count": design["candidate_system"]["published_daily_network_count"], "independence_boundary": design["independence_boundary"],
        "claim_boundary": "Acquisition only. Fallback bytes are accepted only if they match MD5 locks frozen before this audit. No natural D1/phi or route result is calculated."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
