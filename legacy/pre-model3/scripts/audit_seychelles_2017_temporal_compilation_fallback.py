from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import urllib.parse
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data/design/seychelles_kaiser_bunbury2017_temporal_compilation_fallback.json"
RAW_DIR = ROOT / "data/external/seychelles_temporal_compilation"
OUT = ROOT / "data/results/seychelles_2017_temporal_compilation_fallback_audit.json"
DRYAD_PACKAGE_URL = "https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.qz612jmbp/download"


def get_bytes(url: str, timeout: int = 120) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "izu-core-source-audit/1.0", "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def candidate_urls(spec: dict[str, object]) -> list[str]:
    """Return byte-identical transport candidates without changing source identity."""
    original = str(spec["url"])
    filename = str(spec["filename"])
    candidates: list[str] = []
    match = re.search(r"zenodo\.org/records/(\d+)/files/", original)
    if match:
        record_id = match.group(1)
        key = urllib.parse.quote(filename, safe="")
        candidates.append(f"https://zenodo.org/api/records/{record_id}/files/{key}/content")
    candidates.append(original)
    return candidates


def md5_bytes(data: bytes) -> str:
    h = hashlib.md5(); h.update(data); return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    h = hashlib.sha256(); h.update(data); return h.hexdigest()


def normalize(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip()).lower()


def recover_missing_from_dryad_package(
    specs: list[dict[str, object]],
    recovered: dict[str, Path],
    file_states: dict[str, dict],
) -> dict:
    """Try the official Dryad full-dataset package only for still-missing frozen files.

    This is transport redundancy for the same published compilation, not a new
    scientific source. Files are accepted only when their frozen published MD5
    matches, so a package-layout or version change cannot silently alter evidence.
    """
    missing_specs = [spec for spec in specs if str(spec["filename"]) not in recovered]
    state: dict[str, object] = {
        "url": DRYAD_PACKAGE_URL,
        "attempted": bool(missing_specs),
        "status": "not_needed" if not missing_specs else "pending",
        "accepted_files": [],
    }
    if not missing_specs:
        return state
    try:
        package = get_bytes(DRYAD_PACKAGE_URL, timeout=180)
        state["bytes"] = len(package)
        state["sha256"] = sha256_bytes(package)
        with zipfile.ZipFile(io.BytesIO(package)) as archive:
            members_by_basename: dict[str, list[str]] = {}
            for member in archive.namelist():
                members_by_basename.setdefault(Path(member).name, []).append(member)
            state["member_count"] = len(archive.namelist())
            for spec in missing_specs:
                filename = str(spec["filename"])
                expected_md5 = str(spec["published_md5"]).lower()
                matches = members_by_basename.get(filename, [])
                record = file_states[filename]
                record.setdefault("attempts", []).append({
                    "url": DRYAD_PACKAGE_URL,
                    "status": "package_member_missing" if not matches else "package_member_found",
                    "members": matches,
                })
                if len(matches) != 1:
                    continue
                data = archive.read(matches[0])
                actual = md5_bytes(data)
                if actual.lower() != expected_md5:
                    record["attempts"].append({
                        "url": f"{DRYAD_PACKAGE_URL}#{matches[0]}",
                        "status": "md5_mismatch",
                        "observed_md5": actual,
                    })
                    continue
                path = RAW_DIR / filename
                path.write_bytes(data)
                recovered[filename] = path
                record.update({
                    "status": "recovered_md5_verified",
                    "transport_url": f"{DRYAD_PACKAGE_URL}#{matches[0]}",
                    "bytes": len(data),
                    "md5": actual,
                    "sha256": sha256_bytes(data),
                })
                cast_list = state["accepted_files"]
                assert isinstance(cast_list, list)
                cast_list.append(filename)
        state["status"] = "package_recovered_and_checked"
    except Exception as exc:
        state["status"] = "transport_failed"
        state["error"] = repr(exc)
    return state


def main() -> None:
    import openpyxl

    cfg = json.loads(CONFIG.read_text())
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    state = {
        "schema_version": "1.2",
        "analysis": "seychelles_2017_temporal_compilation_fallback_audit",
        "target_doi": cfg["target_doi"],
        "compilation_doi": cfg["compilation_doi"],
        "role": cfg["role"],
        "files": {},
        "status": "not_recovered",
    }

    recovered: dict[str, Path] = {}
    for spec in cfg["files"]:
        filename = str(spec["filename"])
        attempts = []
        data = None
        successful_url = None
        for url in candidate_urls(spec):
            try:
                candidate = get_bytes(url, timeout=90)
                actual = md5_bytes(candidate)
                if actual.lower() != str(spec["published_md5"]).lower():
                    attempts.append({"url": url, "status": "md5_mismatch", "observed_md5": actual})
                    continue
                data = candidate
                successful_url = url
                attempts.append({"url": url, "status": "recovered_md5_verified", "bytes": len(candidate)})
                break
            except Exception as exc:
                attempts.append({"url": url, "status": "failed", "error": repr(exc)})
        if data is None:
            state["files"][filename] = {"status": "failed", "attempts": attempts}
            continue
        path = RAW_DIR / filename
        path.write_bytes(data)
        recovered[filename] = path
        state["files"][filename] = {
            "status": "recovered_md5_verified",
            "transport_url": successful_url,
            "attempts": attempts,
            "bytes": len(data),
            "md5": md5_bytes(data),
            "sha256": sha256_bytes(data),
        }

    state["dryad_package_fallback"] = recover_missing_from_dryad_package(
        list(cfg["files"]), recovered, state["files"]
    )

    db_path = recovered.get("OIK-07303_database.csv")
    refs_path = recovered.get("OIK-07303_original_studies.xlsx")
    if db_path is None or refs_path is None:
        state.update({
            "status": "fallback_bytes_incomplete",
            "decision": "seychelles_compilation_fallback_not_ready",
            "claim_boundary": (
                cfg["claim_boundary"]
                + " Zenodo and official Dryad package transport are treated only as redundant byte routes; "
                  "failure of either route is unavailability, not a biological negative."
            ),
        })
        OUT.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
        print(json.dumps(state, indent=2, ensure_ascii=False))
        return

    # 1) Identify target study only from the references workbook.
    wb = openpyxl.load_workbook(refs_path, read_only=True, data_only=True)
    ref_matches = []
    sheet_audits = []
    target = normalize(cfg["target_doi"])
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        header = [str(v or "") for v in (rows[0] if rows else [])]
        matches = []
        for idx, row in enumerate(rows[1:], start=2):
            joined = " | ".join(str(v or "") for v in row)
            if target in normalize(joined) or "kaiser-bunbury_et_al_2017" in normalize(joined):
                record = {header[j] if j < len(header) and header[j] else f"col_{j+1}": value for j, value in enumerate(row)}
                matches.append({"row_1_based": idx, "record": record})
                ref_matches.append({"sheet": ws.title, "row_1_based": idx, "record": record})
        sheet_audits.append({"sheet": ws.title, "nrows": len(rows), "ncols": len(header), "header": header, "target_matches": len(matches)})
    wb.close()

    # 2) Audit interaction table schema before any metric calculation.
    with db_path.open("r", encoding="utf-8-sig", errors="replace", newline="") as handle:
        sample = handle.read(100000)
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
    except csv.Error:
        dialect = csv.excel
    with db_path.open("r", encoding="utf-8-sig", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle, dialect=dialect)
        fields = list(reader.fieldnames or [])
        total_rows = 0
        previews = []
        column_examples = {field: Counter() for field in fields}
        for row in reader:
            total_rows += 1
            if len(previews) < 5:
                previews.append({field: row.get(field) for field in fields})
            for field in fields:
                value = row.get(field)
                if value not in (None, "") and len(column_examples[field]) < 20:
                    column_examples[field][str(value)] += 1

    # Candidate identifier values from matched reference rows, without using interaction values.
    ref_values = sorted({str(v) for match in ref_matches for v in match["record"].values() if v not in (None, "")})
    identifier_candidates = []
    for field in fields:
        examples = set(column_examples[field])
        overlaps = [value for value in ref_values if value in examples]
        if overlaps:
            identifier_candidates.append({"field": field, "overlap_values": overlaps[:20]})

    state.update({
        "status": "fallback_bytes_and_schema_audited",
        "reference_workbook": {
            "sheets": sheet_audits,
            "target_matches": ref_matches,
            "target_match_count": len(ref_matches),
        },
        "interaction_database": {
            "delimiter": getattr(dialect, "delimiter", None),
            "n_rows": total_rows,
            "n_columns": len(fields),
            "columns": fields,
            "preview": previews,
            "identifier_candidates_from_reference_row": identifier_candidates,
        },
        "decision": (
            "target_study_identified_in_verified_compilation_next_resolve_interaction_rows"
            if ref_matches else "target_study_not_identified_in_reference_workbook"
        ),
        "next_gate": "Resolve the target study's interaction rows using only reference-workbook identifiers/explicit study columns. Then verify preservation of site/month/network identity and quantitative weight before calculating Seychelles Tier-B metrics.",
        "claim_boundary": cfg["claim_boundary"],
    })
    OUT.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(state, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
