from __future__ import annotations

import hashlib
import io
import json
import re
import urllib.request
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/results/chapter2_sicily_bombus_natural_regime_source_audit_20260914.json"
ARTICLE_DOI = "10.1007/s13592-025-01153-4"
ARTICLE_URL = "https://link.springer.com/article/10.1007/s13592-025-01153-4"
FILENAME = "13592_2025_1153_MOESM1_ESM.xlsx"
SOURCE_URLS = [
    "https://media.springernature.com/original/springer-static/esm/art%3A10.1007%2Fs13592-025-01153-4/MediaObjects/" + FILENAME,
    "https://media.springernature.com/original/springer-static/esm/art:10.1007/s13592-025-01153-4/MediaObjects/" + FILENAME,
    "https://static-content.springer.com/esm/art%3A10.1007%2Fs13592-025-01153-4/MediaObjects/" + FILENAME,
]


def fetch(url: str, timeout: int = 120) -> tuple[bytes, dict[str, str], str]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/140 Safari/537.36",
            "Accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/octet-stream,*/*;q=0.8",
            "Referer": ARTICLE_URL,
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read(), {k.lower(): v for k, v in response.headers.items()}, response.geturl()


def norm(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value or "").strip().casefold()).strip("_")


def first_header(rows: list[tuple]) -> tuple[int | None, list[str], list[tuple]]:
    for i, row in enumerate(rows):
        vals = [str(v or "").strip() for v in row]
        if len([v for v in vals if v]) >= 3:
            return i + 1, vals, rows[i + 1 :]
    return None, [], []


def role_columns(headers: list[str]) -> dict[str, list[str]]:
    roles = {"site": [], "date": [], "plant": [], "bombus": [], "count": [], "effort": []}
    for raw in headers:
        n = norm(raw)
        if not n:
            continue
        if any(token in n for token in ("site", "locality", "location", "place")):
            roles["site"].append(raw)
        if any(token in n for token in ("date", "day", "sampling_round", "round")):
            roles["date"].append(raw)
        if "plant" in n or "flower" in n:
            roles["plant"].append(raw)
        if any(token in n for token in ("bombus", "bumble", "bee_species", "species_bee")):
            roles["bombus"].append(raw)
        if any(token in n for token in ("count", "number", "abundance", "frequency", "n_ind")):
            roles["count"].append(raw)
        if any(token in n for token in ("effort", "duration", "hour", "minute", "transect")):
            roles["effort"].append(raw)
    return roles


def unique_values(headers: list[str], rows: list[tuple], column: str) -> list[str]:
    try:
        j = headers.index(column)
    except ValueError:
        return []
    return sorted({
        str(row[j]).strip()
        for row in rows
        if j < len(row) and row[j] not in (None, "") and str(row[j]).strip()
    })


def inspect_workbook(payload: bytes) -> dict[str, object]:
    wb = openpyxl.load_workbook(io.BytesIO(payload), read_only=True, data_only=True)
    sheets = []
    raw_candidates = []
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        header_row, headers, body = first_header(rows)
        roles = role_columns(headers)
        record: dict[str, object] = {
            "sheet": ws.title,
            "nrows": ws.max_row,
            "ncols": ws.max_column,
            "header_row_1_based": header_row,
            "headers": headers,
            "roles": roles,
            "preview": [[str(v) if v is not None else None for v in row[:12]] for row in rows[:6]],
        }
        if roles["site"] and roles["date"] and roles["plant"] and roles["bombus"]:
            site_col, date_col = roles["site"][0], roles["date"][0]
            bee_col, plant_col = roles["bombus"][0], roles["plant"][0]
            record["source_structure"] = {
                "site_column": site_col,
                "date_column": date_col,
                "bombus_column": bee_col,
                "plant_column": plant_col,
                "site_values": unique_values(headers, body, site_col),
                "site_count": len(unique_values(headers, body, site_col)),
                "date_count": len(unique_values(headers, body, date_col)),
                "bombus_label_count": len(unique_values(headers, body, bee_col)),
                "plant_label_count": len(unique_values(headers, body, plant_col)),
            }
            raw_candidates.append(ws.title)
        sheets.append(record)
    wb.close()
    return {"sheet_count": len(sheets), "sheets": sheets, "raw_candidate_sheets": raw_candidates}


def main() -> None:
    state: dict[str, object] = {
        "schema_version": "1.1",
        "analysis": "chapter2_sicily_bombus_natural_regime_source_audit",
        "status": "source_structure_only_coordinates_not_opened",
        "source": {
            "article_doi": ARTICLE_DOI,
            "article_year": 2025,
            "island": "Sicily",
            "archipelago_id": "sicily",
            "official_supplement_urls": SOURCE_URLS,
            "published_design": {
                "fixed_sites": 2,
                "years": [2018, 2019],
                "sampling_window": "April-July",
                "sampling_rounds_per_site_per_year": "13-14",
                "transect_length_km": 1.0,
                "transect_duration_hours": 2.0,
                "same_collector": True,
                "source_note": "Each captured Bombus tube was marked with location and collection date, with associated plant identity; raw transect data are reported in DATAset.xlsx."
            }
        },
        "coordinates_opened": False,
    }

    attempts: list[dict[str, object]] = []
    accepted: bytes | None = None
    for url in SOURCE_URLS:
        try:
            payload, headers, resolved = fetch(url)
            attempt = {
                "url": url,
                "resolved_url": resolved,
                "bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "content_type": headers.get("content-type"),
                "content_length_header": headers.get("content-length"),
                "content_disposition": headers.get("content-disposition"),
                "prefix_hex": payload[:32].hex(),
                "prefix_text": payload[:300].decode("utf-8", errors="replace"),
                "xlsx_signature": payload.startswith(b"PK\x03\x04"),
            }
            if payload.startswith(b"PK\x03\x04"):
                attempt["status"] = "accepted_xlsx_payload"
                attempts.append(attempt)
                accepted = payload
                break
            attempt["status"] = "non_xlsx_payload"
            attempts.append(attempt)
        except Exception as exc:
            attempts.append({"url": url, "status": "request_failed", "error": repr(exc)})
    state["transport_attempts"] = attempts

    if accepted is None:
        state["decision"] = "TRANSPORT_BLOCKED_OFFICIAL_SPRINGER_PATHS_RETURN_NO_XLSX"
    else:
        state["download"] = {
            "status": "recovered_valid_xlsx",
            "bytes": len(accepted),
            "sha256": hashlib.sha256(accepted).hexdigest(),
        }
        workbook = inspect_workbook(accepted)
        state["workbook"] = workbook
        state["decision"] = (
            "RAW_SITE_DATE_PARTNER_PLANT_SCHEMA_RECOVERED_NEXT_FREEZE_ADAPTER"
            if workbook["raw_candidate_sheets"]
            else "RAW_WORKBOOK_RECOVERED_BUT_SITE_DATE_PARTNER_SCHEMA_NOT_IDENTIFIED"
        )

    state["biological_negative"] = False
    state["claim_boundary"] = (
        "This audit inspects only lawful source-equivalent Springer supplement transport, workbook schema, identifier cardinalities, and the published sampling design. "
        "No interaction matrix, D1, phi, response, determinant, or route value is calculated. A non-XLSX transport response is unavailable evidence, not a biological negative."
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "decision": state["decision"],
        "transport_attempts": attempts,
        "raw_candidate_sheets": (state.get("workbook") or {}).get("raw_candidate_sheets", []),
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
