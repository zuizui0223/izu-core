from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "scripts/acquire_audit_mahe_2017_iwdb.py"
DESIGN = ROOT / "data/design/abm_v9_mahe_iwdb_source_gate_v1.json"
AMENDMENT = ROOT / "data/design/abm_v9_mahe_iwdb_transport_amendment_v1.json"
OUT = ROOT / "data/results/mahe_2017_iwdb_source_audit.json"
RAW_DIR = ROOT / "data/external/mahe_2017_iwdb"


def load_base():
    spec = importlib.util.spec_from_file_location("mahe_iwdb_source_base", BASE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def same_path_on_entry_host(data_url: str, entry_url: str) -> str:
    data = urllib.parse.urlsplit(data_url)
    entry = urllib.parse.urlsplit(entry_url)
    if not data.path:
        raise ValueError("data URL has no path")
    return urllib.parse.urlunsplit((entry.scheme, entry.netloc, data.path, data.query, data.fragment))


def write(payload: dict) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def main() -> None:
    base = load_base()
    design = json.loads(DESIGN.read_text())
    amendment = json.loads(AMENDMENT.read_text())
    assert amendment["target_metrics_calculated_before_amendment"] is False
    assert amendment["workbook_bytes_recovered_before_amendment"] is False
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    page_attempts = []
    page_payload = None
    resolved_page_url = None
    for url in design["candidate_system"]["database_entry_paths"]:
        status, payload, error, resolved = base.fetch_bytes(url)
        page_attempts.append({"url": url, "http_status": status, "error": error, "resolved_url": resolved})
        if status == 200 and payload:
            page_payload = payload
            resolved_page_url = resolved or url
            break
    if page_payload is None or resolved_page_url is None:
        write({
            "schema_version": "1.1",
            "analysis": "mahe_2017_iwdb_source_audit",
            "status": "blocked_mahe_iwdb_entry_not_recovered",
            "page_attempts": page_attempts,
            "source_admission_succeeds": False,
            "target_metrics_calculated": False,
            "transport_amendment_used": True,
        })
        return

    parser = base.LinkParser()
    parser.feed(page_payload.decode("utf-8", errors="replace"))
    candidate_links = []
    seen = set()
    for href, anchor in parser.links:
        absolute = urllib.parse.urljoin(resolved_page_url, href)
        path = urllib.parse.urlparse(absolute).path.lower()
        if path.endswith((".xlsx", ".xls")) and absolute not in seen:
            seen.add(absolute)
            candidate_links.append({"href": href, "anchor": anchor, "url": absolute})

    file_records = []
    blocked_files = []
    for link in candidate_links:
        direct_url = link["url"]
        retry_url = same_path_on_entry_host(direct_url, resolved_page_url)
        attempts = []
        payload = None
        resolved = None
        for label, url in (("direct_href", direct_url), ("exact_path_entry_host", retry_url)):
            # If the hosts are already identical, do not duplicate the same request.
            if attempts and url == attempts[0]["url"]:
                continue
            status, candidate_payload, error, candidate_resolved = base.fetch_bytes(url)
            attempts.append({
                "mode": label,
                "url": url,
                "http_status": status,
                "error": error,
                "resolved_url": candidate_resolved,
            })
            if status == 200 and candidate_payload is not None:
                payload = candidate_payload
                resolved = candidate_resolved or url
                break

        name = Path(urllib.parse.urlparse(direct_url).path).name
        record = {
            **link,
            "name": urllib.parse.unquote(name),
            "transport_attempts": attempts,
            "resolved_url": resolved,
        }
        if payload is None:
            blocked_files.append(record["name"] or direct_url)
            file_records.append(record)
            continue

        record.update({
            "bytes": len(payload),
            "md5": hashlib.md5(payload).hexdigest(),
            "sha256": hashlib.sha256(payload).hexdigest(),
        })
        safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", record["name"] or f"iwdb_{len(file_records)}.xlsx")
        (RAW_DIR / safe_name).write_bytes(payload)
        suffix = Path(record["name"]).suffix.lower()
        try:
            if suffix == ".xlsx":
                record["workbook_inventory"] = base.inventory_xlsx(payload)
            elif suffix == ".xls":
                record["workbook_inventory"] = base.inventory_xls(payload)
        except Exception as exc:
            record["inventory_error"] = f"{type(exc).__name__}: {exc}"
        file_records.append(record)

    source_bytes_ok = bool(candidate_links) and not blocked_files and all(row.get("bytes") for row in file_records)
    matrix_64_visible = any(
        base.workbook_has_64_network_matrix(row.get("workbook_inventory") or {})
        for row in file_records
    )
    representations = base.representation_labels(file_records)
    admission = source_bytes_ok and matrix_64_visible
    write({
        "schema_version": "1.1",
        "analysis": "mahe_2017_iwdb_source_audit",
        "status": (
            "source_admitted_mahe_iwdb_64_raw_monthly_matrices"
            if admission
            else "blocked_mahe_iwdb_raw_matrix_bytes_or_64_network_schema_incomplete"
        ),
        "database_entry_resolved": resolved_page_url,
        "database_entry_bytes": len(page_payload),
        "database_entry_sha256": hashlib.sha256(page_payload).hexdigest(),
        "page_attempts": page_attempts,
        "excel_link_count": len(candidate_links),
        "excel_links": candidate_links,
        "files": file_records,
        "blocked_files": blocked_files,
        "source_bytes_ok": source_bytes_ok,
        "raw_64_network_matrix_structure_visible": matrix_64_visible,
        "representation_labels": representations,
        "source_admission_succeeds": admission,
        "target_metrics_calculated": False,
        "transport_amendment_used": True,
        "transport_amendment": amendment,
        "prior_block_boundary": design["prior_block_boundary"],
        "observation_boundary": design["source_only_gate"]["observation_boundary"],
        "claim_boundary": (
            "Source transport/schema audit only. The only transport amendment is an exact-path retry on the IWDB entry host. "
            "No network target or v9 predictive statistic is calculated."
        ),
    })


if __name__ == "__main__":
    main()
