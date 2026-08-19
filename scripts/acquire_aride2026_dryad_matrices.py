from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v5_aride_seasonal_validation_v1.json"
RAW_DIR = ROOT / "data/external/aride_2026"
OUT = ROOT / "data/results/aride2026_dryad_source_lock.json"
LEGACY_BASE = "https://datadryad.org/downloads/file_stream/{}"
API_BASE = "https://datadryad.org/api/v2/files/{}/download"


def get_bytes(url: str, timeout: int = 120) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "izu-core-source-audit/1.0",
            "Accept": "application/octet-stream,text/csv,*/*",
            "X-API-Version": "2.1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_matrix_shape(data: bytes) -> dict:
    text = data.decode("utf-8-sig")
    rows = list(csv.reader(io.StringIO(text)))
    if len(rows) < 2 or len(rows[0]) < 2:
        raise RuntimeError("CSV does not contain a matrix with row and column labels")
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise RuntimeError("CSV matrix has ragged row widths")
    pollinators = [cell.strip() for cell in rows[0][1:]]
    plants = [row[0].strip() for row in rows[1:]]
    if any(not x for x in pollinators) or len(set(pollinators)) != len(pollinators):
        raise RuntimeError("pollinator labels must be unique and non-empty")
    if any(not x for x in plants) or len(set(plants)) != len(plants):
        raise RuntimeError("plant labels must be unique and non-empty")
    positive = 0
    total = 0.0
    for row in rows[1:]:
        for cell in row[1:]:
            try:
                value = float(cell)
            except (TypeError, ValueError):
                raise RuntimeError(f"non-numeric matrix cell {cell!r}")
            if not math.isfinite(value) or value < 0:
                raise RuntimeError("matrix weights must be finite and non-negative")
            total += value
            positive += value > 0
    return {
        "n_plants": len(plants),
        "n_pollinators": len(pollinators),
        "n_positive_links": positive,
        "total_weight": total,
        "first_header_cell": rows[0][0],
        "plant_label_preview": plants[:5],
        "pollinator_label_preview": pollinators[:5],
    }


def main() -> None:
    design = json.loads(DESIGN.read_text())
    streams = design["held_out_system"]["dryad_file_streams"]
    required = design["source_gate"]["required_files"]
    if set(streams) != set(required):
        raise RuntimeError("frozen Dryad stream set does not match required files")

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    files = []
    attempts = []
    for name in required:
        file_id = int(streams[name])
        api_url = API_BASE.format(file_id)
        legacy_url = LEGACY_BASE.format(file_id)
        attempt = {
            "filename": name,
            "dryad_file_id": file_id,
            "legacy_file_stream_url": legacy_url,
            "api_download_endpoint": api_url,
        }
        try:
            data = get_bytes(api_url)
        except urllib.error.HTTPError as exc:
            attempt.update({
                "status": "transport_blocked" if exc.code in (401, 403) else "transport_failed",
                "http_status": exc.code,
                "error": repr(exc),
            })
            attempts.append(attempt)
            if exc.code in (401, 403):
                continue
            raise

        if len(data) < 100:
            raise RuntimeError(f"Dryad payload too small for {name}: {len(data)} bytes")
        # Once bytes are available, schema defects remain hard failures rather than
        # being reclassified as source unavailability.
        shape = parse_matrix_shape(data)
        path = RAW_DIR / name
        path.write_bytes(data)
        digest = sha256(data)
        files.append({
            "filename": name,
            "dryad_file_id": file_id,
            "download_endpoint": api_url,
            "bytes": len(data),
            "sha256": digest,
            "schema_audit": shape,
        })
        attempt.update({"status": "recovered", "bytes": len(data), "sha256": digest})
        attempts.append(attempt)

    recovered_names = {row["filename"] for row in files}
    missing = [name for name in required if name not in recovered_names]
    auth_blocks = [row for row in attempts if row.get("status") == "transport_blocked"]
    all_recovered = not missing
    if all_recovered:
        status = "all_required_source_native_matrices_recovered"
        next_gate = "Proceed to outcome-blind GIFT opportunity lock and the already-frozen target analysis."
    elif len(auth_blocks) == len(missing) and auth_blocks:
        status = "blocked_dryad_authenticated_download_required"
        next_gate = "Keep Aride target estimands uninspected. Reopen only with lawful authorized Dryad file access or an independently verified public mirror of the exact frozen files."
    else:
        status = "blocked_required_aride_source_bytes_not_recovered"
        next_gate = "Do not calculate target metrics or substitute other seasonal networks."

    payload = {
        "schema_version": "1.2",
        "analysis": "aride2026_dryad_source_lock",
        "status": status,
        "dryad_doi": design["held_out_system"]["dryad_doi"],
        "dryad_api_version": "2.1.0",
        "required_weight_type": design["source_gate"]["required_weight_type"],
        "required_file_count": len(required),
        "recovered_file_count": len(files),
        "all_required_files_recovered": all_recovered,
        "missing_required_files": missing,
        "files": files,
        "attempts": attempts,
        "transport_history": "Legacy /downloads/file_stream/:id returned HTTP 403 to automated access; current /api/v2/files/:id/download returned HTTP 401 without an authenticated Dryad session on the inspected public runner.",
        "target_metrics_inspected": False,
        "next_gate": next_gate,
        "claim_boundary": "A source-access block is not biological evidence. Until all exact frozen source matrices are recovered, no Shannon diversity, niche overlap, v5 fit, or biological direction may be calculated from Aride.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
