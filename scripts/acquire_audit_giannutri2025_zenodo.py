from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v6_giannutri_source_gate_v1.json"
OUT = ROOT / "data/results/giannutri2025_zenodo_source_audit.json"
RAW_DIR = ROOT / "data/external/giannutri2025"
API = "https://zenodo.org/api/records/14855496"
USER_AGENT = "izu-core-source-audit/1.0"


def fetch_bytes(url: str) -> tuple[int | None, bytes | None, str | None]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
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
    reader = csv.reader(io.StringIO(text), delimiter=delimiter)
    rows = list(reader)
    if not rows:
        raise RuntimeError("empty tabular source")
    headers = [str(value).strip() for value in rows[0]]
    normalized = [re.sub(r"[^a-z0-9]+", "_", h.lower()).strip("_") for h in headers]
    field_roles = {
        "time": [h for h, n in zip(headers, normalized) if any(k in n for k in ("date", "day", "year"))],
        "condition": [h for h, n in zip(headers, normalized) if any(k in n for k in ("condition", "hive", "hb", "treatment"))],
        "plant": [h for h, n in zip(headers, normalized) if any(k in n for k in ("plant", "flower"))],
        "visitor": [h for h, n in zip(headers, normalized) if any(k in n for k in ("bee", "visitor", "pollinator", "species"))],
        "count_or_visit": [h for h, n in zip(headers, normalized) if any(k in n for k in ("visit", "count", "frequency", "abundance", "number"))],
    }
    return {
        "encoding": encoding,
        "delimiter_repr": repr(delimiter),
        "row_count_excluding_header": max(0, len(rows) - 1),
        "column_count": len(headers),
        "headers": headers,
        "field_role_candidates": field_roles,
        "target_metrics_calculated": False,
    }


def code_inventory(payload: bytes) -> dict:
    text, encoding = decode_text(payload)
    lines = text.splitlines()
    indicators = []
    patterns = ("network", "bipartite", "transect_data_for_overlap", "date", "condition", "hive", "group_by")
    for index, line in enumerate(lines, start=1):
        lower = line.lower()
        if any(pattern in lower for pattern in patterns):
            indicators.append({"line": index, "text": line[:300]})
    return {
        "encoding": encoding,
        "line_count": len(lines),
        "structural_indicator_lines": indicators[:120],
        "target_metrics_calculated": False,
    }


def main() -> None:
    design = json.loads(DESIGN.read_text())
    status, metadata_bytes, metadata_error = fetch_bytes(API)
    if status != 200 or metadata_bytes is None:
        result = {
            "schema_version": "1.0",
            "analysis": "giannutri2025_zenodo_source_audit",
            "status": "blocked_zenodo_metadata_not_recovered",
            "metadata_http_status": status,
            "metadata_error": metadata_error,
            "source_admission_succeeds": False,
            "target_metrics_calculated": False,
        }
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2))
        return

    metadata = json.loads(metadata_bytes)
    files = {row.get("key"): row for row in metadata.get("files", [])}
    required = design["required_zenodo_files"]
    missing = [name for name in required if name not in files]
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    records = []
    blocked = list(missing)

    for name, expected_md5 in required.items():
        row = files.get(name)
        if row is None:
            continue
        links = row.get("links") or {}
        download_url = links.get("content") or links.get("self")
        record = {
            "name": name,
            "expected_md5": expected_md5,
            "metadata_checksum": row.get("checksum"),
            "metadata_size": row.get("size"),
            "download_url": download_url,
        }
        if not download_url:
            record["error"] = "no download URL in Zenodo metadata"
            blocked.append(name)
            records.append(record)
            continue
        file_status, payload, error = fetch_bytes(download_url)
        record["http_status"] = file_status
        record["error"] = error
        if file_status != 200 or payload is None:
            blocked.append(name)
            records.append(record)
            continue
        actual_md5 = hashlib.md5(payload).hexdigest()
        actual_sha256 = hashlib.sha256(payload).hexdigest()
        record.update({"bytes": len(payload), "md5": actual_md5, "sha256": actual_sha256})
        metadata_md5 = str(row.get("checksum") or "").removeprefix("md5:")
        if actual_md5 != expected_md5 or (metadata_md5 and actual_md5 != metadata_md5):
            record["checksum_match"] = False
            blocked.append(name)
            records.append(record)
            continue
        record["checksum_match"] = True
        (RAW_DIR / name).write_bytes(payload)
        if name.endswith(".txt") and name != "README.txt":
            record["schema_inventory"] = tabular_inventory(payload)
        elif name.endswith(".R"):
            record["code_inventory"] = code_inventory(payload)
        else:
            text, encoding = decode_text(payload)
            record["text_inventory"] = {
                "encoding": encoding,
                "line_count": len(text.splitlines()),
                "target_metrics_calculated": False,
            }
        records.append(record)

    raw_records = {
        row["name"]: row for row in records if row.get("checksum_match") is True
    }
    overlap = raw_records.get("transect_data_for_overlap_analysis.txt", {}).get("schema_inventory", {})
    walking = raw_records.get("walking_transects_dataset.txt", {}).get("schema_inventory", {})
    code = raw_records.get("Code for Resource use and overlap analysis.R", {}).get("code_inventory", {})

    def roles_present(inventory: dict) -> bool:
        roles = inventory.get("field_role_candidates", {})
        return bool(roles.get("time")) and bool(roles.get("plant")) and bool(roles.get("visitor"))

    source_bytes_ok = len(raw_records) == len(required) and not blocked
    daily_structure_visible = roles_present(overlap) or roles_present(walking)
    condition_structure_visible = bool(overlap.get("field_role_candidates", {}).get("condition")) or bool(
        walking.get("field_role_candidates", {}).get("condition")
    )
    code_structure_visible = bool(code.get("structural_indicator_lines"))
    admission = source_bytes_ok and daily_structure_visible and condition_structure_visible and code_structure_visible

    result = {
        "schema_version": "1.0",
        "analysis": "giannutri2025_zenodo_source_audit",
        "status": (
            "source_admitted_raw_daily_network_reconstruction_inputs"
            if admission else "blocked_giannutri_source_or_grouping_structure_incomplete"
        ),
        "zenodo_record_id": design["candidate_system"]["zenodo_record_id"],
        "zenodo_doi": design["candidate_system"]["zenodo_doi"],
        "metadata_bytes": len(metadata_bytes),
        "metadata_sha256": hashlib.sha256(metadata_bytes).hexdigest(),
        "required_file_count": len(required),
        "recovered_checksum_locked_file_count": len(raw_records),
        "blocked_files": sorted(set(blocked)),
        "files": records,
        "source_bytes_ok": source_bytes_ok,
        "daily_structure_visible": daily_structure_visible,
        "condition_structure_visible": condition_structure_visible,
        "code_structure_visible": code_structure_visible,
        "source_admission_succeeds": admission,
        "target_metrics_calculated": False,
        "published_scope": design["candidate_system"]["published_network_scope"],
        "published_daily_network_count": design["candidate_system"]["published_daily_network_count"],
        "independence_boundary": design["independence_boundary"],
        "claim_boundary": "Source admission only. No Shannon, plant niche overlap, empirical network range, or v6 predictive fit was calculated.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
