from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data/results/abm_v13_hawaii_lobelioid_dryad_recovery.json"
DEFAULT_BYTES_DIR = ROOT / ".artifacts/abm_v13_hawaii_lobelioid_dryad"
USER_AGENT = "izu-core-v13-hawaii-lobelioid-source-recovery/1.0"

FILES = (
    {
        "role": "trait_assemblage_pairs",
        "file_stream_id": 4858933,
        "name": "Case_FE_2026_Analysis_1.csv",
        "reported_size_kb": 89.10,
        "kind": "csv",
        "required_columns": (
            "bird_species",
            "culmen",
            "island",
            "assemblage",
            "plant_species",
            "flower_length",
            "bill_minus_flower",
        ),
    },
    {
        "role": "interaction_quality_pairs",
        "file_stream_id": 4858934,
        "name": "Case_FE_2026_Analysis_2.csv",
        "reported_size_kb": 1.46,
        "kind": "csv",
        "required_columns": (
            "plant_species",
            "bird_species",
            "N",
            "pollen_contact",
            "nectar_robbing",
            "source",
            "culmen",
            "flower_length",
            "bill_minus_flower",
        ),
    },
    {
        "role": "readme",
        "file_stream_id": 4858939,
        "name": "README.md",
        "reported_size_kb": 7.51,
        "kind": "text",
        "required_columns": (),
    },
)


def source_url(file_stream_id: int) -> str:
    return f"https://datadryad.org/downloads/file_stream/{file_stream_id}"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def fetch_bytes(url: str, *, timeout: int = 120) -> tuple[bytes | None, dict[str, object]]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read()
            return payload, {
                "http_status": int(getattr(response, "status", 200)),
                "content_type": response.headers.get("Content-Type"),
                "final_url": response.geturl(),
                "transport_error": None,
            }
    except urllib.error.HTTPError as exc:
        return None, {
            "http_status": int(exc.code),
            "content_type": exc.headers.get("Content-Type") if exc.headers else None,
            "final_url": exc.geturl(),
            "transport_error": f"HTTPError: {exc.code} {exc.reason}",
        }
    except Exception as exc:  # transport state is provenance, not a CI exception
        return None, {
            "http_status": None,
            "content_type": None,
            "final_url": url,
            "transport_error": f"{type(exc).__name__}: {exc}",
        }


def decode_utf8(payload: bytes) -> str | None:
    try:
        return payload.decode("utf-8-sig")
    except UnicodeDecodeError:
        return None


def csv_schema(text: str, required_columns: tuple[str, ...]) -> dict[str, object]:
    reader = csv.DictReader(io.StringIO(text))
    fieldnames = tuple(reader.fieldnames or ())
    rows = list(reader)
    missing = [column for column in required_columns if column not in fieldnames]
    return {
        "columns": list(fieldnames),
        "row_count": len(rows),
        "required_columns_present": not missing,
        "missing_required_columns": missing,
    }


def audit_payload(payload: bytes, spec: dict[str, object]) -> dict[str, object]:
    reported_bytes = float(spec["reported_size_kb"]) * 1024.0
    ratio = len(payload) / reported_bytes if reported_bytes > 0 else None
    text = decode_utf8(payload)
    audit: dict[str, object] = {
        "byte_count": len(payload),
        "sha256": sha256_bytes(payload),
        "reported_size_kb": spec["reported_size_kb"],
        "byte_count_over_reported_kib": ratio,
        "plausible_size_vs_landing_metadata": ratio is not None and 0.80 <= ratio <= 1.20,
        "utf8_decodes": text is not None,
    }
    if spec["kind"] == "csv" and text is not None:
        audit["csv_schema"] = csv_schema(text, tuple(spec["required_columns"]))
    else:
        audit["csv_schema"] = None
    return audit


def source_gate_passes(spec: dict[str, object], audit: dict[str, object]) -> bool:
    if not audit["plausible_size_vs_landing_metadata"] or not audit["utf8_decodes"]:
        return False
    if spec["kind"] == "csv":
        schema = audit["csv_schema"]
        return bool(schema and schema["required_columns_present"] and int(schema["row_count"]) > 0)
    return True


def recover(*, bytes_dir: Path = DEFAULT_BYTES_DIR, timeout: int = 120) -> dict[str, object]:
    bytes_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    recovered = 0
    valid = 0

    for spec in FILES:
        url = source_url(int(spec["file_stream_id"]))
        payload, transport = fetch_bytes(url, timeout=timeout)
        row: dict[str, object] = {
            "role": spec["role"],
            "file_stream_id": spec["file_stream_id"],
            "name": spec["name"],
            "reported_size_kb": spec["reported_size_kb"],
            "url": url,
            **transport,
        }
        if payload is None:
            row.update({"recovered": False, "byte_audit": None, "saved_path": None, "source_byte_gate_passes": False})
        else:
            recovered += 1
            audit = audit_payload(payload, spec)
            passes = source_gate_passes(spec, audit)
            valid += int(passes)
            suffix = ".csv" if spec["kind"] == "csv" else ".md"
            path = bytes_dir / f"{spec['file_stream_id']}{suffix}"
            path.write_bytes(payload)
            row.update({
                "recovered": True,
                "byte_audit": audit,
                "saved_path": str(path),
                "source_byte_gate_passes": passes,
            })
        rows.append(row)

    all_recovered = recovered == len(FILES)
    all_valid = valid == len(FILES)
    if all_recovered and all_valid:
        decision = "hawaii_lobelioid_dryad_bytes_recovered_ready_for_schema_freeze"
    elif all_recovered:
        decision = "hawaii_lobelioid_bytes_recovered_but_source_gate_failed"
    else:
        decision = "blocked_hawaii_lobelioid_dryad_transport"

    return {
        "analysis": "abm_v13_hawaii_lobelioid_dryad_recovery",
        "dataset_doi": "10.5061/dryad.sj3tx96kr",
        "article_doi": "10.1111/1365-2435.70415",
        "signed_position_construct": "bill_minus_flower = culmen_mm - flower_length_mm",
        "target_metrics_calculated": False,
        "file_count_expected": len(FILES),
        "file_count_recovered": recovered,
        "file_count_structurally_valid": valid,
        "all_recovered": all_recovered,
        "all_structurally_valid": all_valid,
        "decision": decision,
        "files": rows,
        "next_gate": (
            "freeze exact row identities and source-native signed-position arithmetic before any repo quantitative outcome reanalysis"
            if decision == "hawaii_lobelioid_dryad_bytes_recovered_ready_for_schema_freeze"
            else "retain target closed; switch source route rather than reconstructing rows from the publication"
        ),
        "claim_boundary": (
            "This step audits public source transport, byte identity and declared schema only. It does not re-estimate the published trait-matching or interaction-quality results."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--bytes-dir", type=Path, default=DEFAULT_BYTES_DIR)
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()
    payload = recover(bytes_dir=args.bytes_dir, timeout=args.timeout)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "decision": payload["decision"],
        "file_count_recovered": payload["file_count_recovered"],
        "file_count_structurally_valid": payload["file_count_structurally_valid"],
    }, indent=2))


if __name__ == "__main__":
    main()
