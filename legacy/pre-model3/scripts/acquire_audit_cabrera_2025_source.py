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
DESIGN = ROOT / "data/design/abm_v8_cabrera_source_gate_v1.json"
OUT = ROOT / "data/results/cabrera_2025_source_audit.json"
RAW_DIR = ROOT / "data/external/cabrera_2025"
USER_AGENT = "izu-core-source-audit/1.0"


def fetch_bytes(url: str) -> tuple[int | None, bytes | None, str | None]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
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
    raise RuntimeError("source text could not be decoded")


def normalize(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value).lower()).strip("_")


def role_candidates(headers: list[str]) -> dict[str, list[str]]:
    normalized = [normalize(header) for header in headers]
    site_tokens = ("site", "community", "locality", "location", "habitat", "plot", "transect")
    time_tokens = ("campaign", "date", "day", "month", "year", "season", "round", "sampling", "visita", "censo", "census")
    method_tokens = ("method", "camera", "direct", "observation", "observer", "recording", "acs")
    plant_tokens = ("plant", "flower_species", "plant_species")
    pollinator_tokens = ("pollinator", "visitor", "insect", "animal_visitor", "pollinator_group", "visitor_group")

    result = {
        "site_context": [header for header, key in zip(headers, normalized) if any(token in key for token in site_tokens)],
        "time_context": [header for header, key in zip(headers, normalized) if any(token in key for token in time_tokens)],
        "method_context": [header for header, key in zip(headers, normalized) if any(token in key for token in method_tokens)],
        "plant": [header for header, key in zip(headers, normalized) if any(token in key for token in plant_tokens)],
        "pollinator": [header for header, key in zip(headers, normalized) if any(token in key for token in pollinator_tokens)],
        "interaction_amount": [],
    }
    # Source README defines `visita` as an identifier of the sampling visit, not
    # an interaction weight. Quantitative/event-amount candidates are therefore
    # deliberately narrower than generic substring matching on "visit".
    amount_keys = {
        "n_ind",
        "n_visit_flowers",
        "n_visits",
        "interaction_count",
        "interaction_frequency",
        "visit_count",
        "visit_frequency",
    }
    result["interaction_amount"] = [
        header for header, key in zip(headers, normalized)
        if key in amount_keys or key.startswith("n_visit_")
    ]
    return result


def sniff_rows(payload: bytes) -> tuple[list[list[str]], str, str]:
    text, encoding = decode_text(payload)
    lines = text.splitlines()
    sample = "\n".join(lines[:40])
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters="\t,;")
        delimiter = dialect.delimiter
    except csv.Error:
        first = lines[0] if lines else ""
        delimiter = ";" if first.count(";") > first.count(",") else ("\t" if "\t" in first else ",")
    rows = list(csv.reader(io.StringIO(text), delimiter=delimiter))
    return rows, encoding, delimiter


def structural_cardinalities(headers: list[str], rows: list[list[str]], roles: dict[str, list[str]]) -> dict[str, dict[str, int]]:
    index = {header: position for position, header in enumerate(headers)}
    result: dict[str, dict[str, int]] = {}
    for role in ("site_context", "time_context", "method_context", "plant", "pollinator"):
        result[role] = {}
        for header in roles.get(role, []):
            position = index.get(header)
            if position is None:
                continue
            values = {
                row[position].strip()
                for row in rows
                if position < len(row) and row[position].strip()
            }
            result[role][header] = len(values)
    return result


def composite_context_count(headers: list[str], rows: list[list[str]], fields: list[str]) -> int | None:
    index = {header: position for position, header in enumerate(headers)}
    if not fields or any(field not in index for field in fields):
        return None
    values = set()
    for row in rows:
        parts = []
        complete = True
        for field in fields:
            position = index[field]
            if position >= len(row) or not row[position].strip():
                complete = False
                break
            parts.append(row[position].strip())
        if complete:
            values.add(tuple(parts))
    return len(values)


def readme_event_semantics(text: str) -> bool:
    normalized = " ".join(text.lower().split())
    return (
        "each row" in normalized
        and ("sampling event" in normalized or "census" in normalized)
        and ("pollinator visit" in normalized or "plant-pollinator interaction" in normalized)
    )


def write(payload: dict) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def main() -> None:
    design = json.loads(DESIGN.read_text())
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    file_records = []
    blocked_files: list[str] = []
    readme_text = ""
    csv_payload: bytes | None = None

    for source in design["source_files"]:
        name = source["name"]
        url = source["url"]
        status, payload, error = fetch_bytes(url)
        record = {
            "name": name,
            "url": url,
            "http_status": status,
            "error": error,
        }
        if status != 200 or payload is None:
            blocked_files.append(name)
            file_records.append(record)
            continue
        record.update({
            "bytes": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        })
        (RAW_DIR / name).write_bytes(payload)
        if name.lower().endswith("readme.txt"):
            readme_text, encoding = decode_text(payload)
            record["encoding"] = encoding
            record["line_count"] = len(readme_text.splitlines())
            keywords = ("site", "community", "habitat", "campaign", "plant", "pollinator", "visit", "camera", "direct", "census", "method", "n ind")
            record["structural_keyword_lines"] = [
                {"line": i, "text": line[:500]}
                for i, line in enumerate(readme_text.splitlines(), start=1)
                if any(token in line.lower() for token in keywords)
            ][:120]
        elif name.lower().endswith(".csv"):
            csv_payload = payload
        file_records.append(record)

    source_bytes_ok = len(file_records) == len(design["source_files"]) and not blocked_files
    if not source_bytes_ok or csv_payload is None:
        write({
            "schema_version": "1.1",
            "analysis": "cabrera_2025_source_audit",
            "status": "blocked_cabrera_source_bytes_not_recovered",
            "files": file_records,
            "blocked_files": blocked_files,
            "source_bytes_ok": False,
            "source_admission_succeeds": False,
            "target_metrics_calculated": False,
            "claim_boundary": "Source-byte admission only; no network target or ABM v8 prediction was calculated.",
        })
        return

    rows, encoding, delimiter = sniff_rows(csv_payload)
    headers = [str(value).strip() for value in (rows[0] if rows else [])]
    data_rows = rows[1:] if rows else []
    roles = role_candidates(headers)
    cardinalities = structural_cardinalities(headers, data_rows, roles)
    event_semantics = readme_event_semantics(readme_text)

    has_plant = bool(roles["plant"])
    has_pollinator = bool(roles["pollinator"])
    has_repeated_context = bool(roles["site_context"]) and bool(roles["time_context"])
    has_interaction_amount_or_event_rows = bool(roles["interaction_amount"]) or event_semantics
    raw_repeated_pair_records_visible = (
        has_plant and has_pollinator and has_repeated_context and has_interaction_amount_or_event_rows
    )

    source_context_counts = {
        "COMMUNITY_x_visita": composite_context_count(headers, data_rows, ["COMMUNITY", "visita"]),
        "COMMUNITY_x_visita_x_censo": composite_context_count(headers, data_rows, ["COMMUNITY", "visita", "censo"]),
        "COMMUNITY_x_visita_x_Method": composite_context_count(headers, data_rows, ["COMMUNITY", "visita", "Method"]),
    }

    status_name = (
        "source_admitted_cabrera_raw_repeated_pair_interaction_records"
        if raw_repeated_pair_records_visible
        else "blocked_cabrera_schema_missing_raw_pair_or_repeated_context"
    )

    write({
        "schema_version": "1.1",
        "analysis": "cabrera_2025_source_audit",
        "status": status_name,
        "source": design["candidate_system"],
        "files": file_records,
        "blocked_files": [],
        "source_bytes_ok": True,
        "csv_schema": {
            "encoding": encoding,
            "delimiter_repr": repr(delimiter),
            "row_count_including_header": len(rows),
            "data_row_count": len(data_rows),
            "column_count": len(headers),
            "headers": headers,
            "role_candidates": roles,
            "structural_cardinalities": cardinalities,
            "source_context_counts": source_context_counts,
            "readme_describes_rows_as_interaction_sampling_events": event_semantics,
            "source_native_role_correction_before_targets": {
                "COMMUNITY": "site/community identifier",
                "visita": "sampling visit identifier, not interaction weight",
                "censo": "census identifier within sampling visit",
                "N ind": "pollinator-individual amount candidate",
                "N visit flowers": "visited-flower amount candidate"
            },
        },
        "raw_repeated_pair_interaction_records_visible": raw_repeated_pair_records_visible,
        "source_admission_succeeds": raw_repeated_pair_records_visible,
        "target_metrics_calculated": False,
        "independence_boundary": design["independence_boundary"],
        "method_boundary": design["source_only_gate"]["method_boundary"],
        "claim_boundary": "Source bytes and schema only. No interaction diversity, niche overlap, pair/plant/pollinator support estimand, empirical range, or ABM v8 predictive fit is calculated here.",
    })


if __name__ == "__main__":
    main()
