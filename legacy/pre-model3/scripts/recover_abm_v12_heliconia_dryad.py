from __future__ import annotations

import argparse
import hashlib
import json
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data" / "results" / "abm_v12_heliconia_dryad_recovery.json"
DEFAULT_BYTES_DIR = ROOT / ".artifacts" / "abm_v12_heliconia_dryad"
USER_AGENT = "izu-core-v12-heliconia-source-recovery/1.0"
OLE2_MAGIC = bytes.fromhex("D0CF11E0A1B11AE1")

FILES = (
    {
        "role": "bihai_plant_trait_seed_set",
        "file_stream_id": 37457,
        "name": "Temeles et al Heliconia Bihai Population Data.XLS",
        "reported_size_kb": 34.82,
    },
    {
        "role": "caribaea_red_plant_trait_seed_set",
        "file_stream_id": 37459,
        "name": "Temeles et al Heliconia caribaea red morph population data.XLS",
        "reported_size_kb": 32.77,
    },
    {
        "role": "caribaea_yellow_plant_trait_seed_set",
        "file_stream_id": 37461,
        "name": "Temeles et al Heliconia caribaea yellow morph population data.XLS",
        "reported_size_kb": 28.67,
    },
)


def source_url(file_stream_id: int) -> str:
    return f"https://datadryad.org/downloads/file_stream/{file_stream_id}"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def looks_like_legacy_xls(payload: bytes) -> bool:
    return len(payload) >= len(OLE2_MAGIC) and payload[: len(OLE2_MAGIC)] == OLE2_MAGIC


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
    except Exception as exc:  # transport state is scientific provenance, not a CI exception
        return None, {
            "http_status": None,
            "content_type": None,
            "final_url": url,
            "transport_error": f"{type(exc).__name__}: {exc}",
        }


def audit_payload(payload: bytes, spec: dict[str, object]) -> dict[str, object]:
    reported_bytes = float(spec["reported_size_kb"]) * 1024.0
    size_ratio = len(payload) / reported_bytes if reported_bytes > 0 else None
    return {
        "byte_count": len(payload),
        "sha256": sha256_bytes(payload),
        "legacy_xls_ole2_magic": looks_like_legacy_xls(payload),
        "reported_size_kb": spec["reported_size_kb"],
        "byte_count_over_reported_kib": size_ratio,
        "plausible_size_vs_landing_metadata": size_ratio is not None and 0.90 <= size_ratio <= 1.10,
    }


def recover(*, bytes_dir: Path = DEFAULT_BYTES_DIR, timeout: int = 120) -> dict[str, object]:
    bytes_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    recovered = 0
    structurally_valid = 0

    for spec in FILES:
        url = source_url(int(spec["file_stream_id"]))
        payload, transport = fetch_bytes(url, timeout=timeout)
        row: dict[str, object] = {**spec, "url": url, **transport}
        if payload is None:
            row.update({
                "recovered": False,
                "byte_audit": None,
                "saved_path": None,
            })
        else:
            recovered += 1
            audit = audit_payload(payload, spec)
            valid = bool(audit["legacy_xls_ole2_magic"] and audit["plausible_size_vs_landing_metadata"])
            structurally_valid += int(valid)
            safe_name = f"{spec['file_stream_id']}.xls"
            path = bytes_dir / safe_name
            path.write_bytes(payload)
            row.update({
                "recovered": True,
                "byte_audit": audit,
                "saved_path": str(path),
                "source_byte_gate_passes": valid,
            })
        rows.append(row)

    all_recovered = recovered == len(FILES)
    all_structurally_valid = structurally_valid == len(FILES)
    if all_recovered and all_structurally_valid:
        decision = "dryad_xls_bytes_recovered_ready_for_schema_freeze"
    elif all_recovered:
        decision = "dryad_xls_bytes_recovered_but_source_byte_gate_failed"
    else:
        decision = "blocked_dryad_xls_transport"

    return {
        "analysis": "abm_v12_heliconia_dryad_recovery",
        "dataset_doi": "10.5061/dryad.64835",
        "selection_article_doi": "10.1111/jeb.12053",
        "target_metrics_calculated": False,
        "file_count_expected": len(FILES),
        "file_count_recovered": recovered,
        "file_count_structurally_valid": structurally_valid,
        "all_recovered": all_recovered,
        "all_structurally_valid": all_structurally_valid,
        "decision": decision,
        "files": rows,
        "next_gate": (
            "freeze workbook sheet/column schema before any fitness target"
            if decision == "dryad_xls_bytes_recovered_ready_for_schema_freeze"
            else "retain target closed; do not infer missing raw values from article tables"
        ),
        "claim_boundary": (
            "This step audits public source transport and byte identity only. A successful download does not open the v12 target until workbook schema and population/year identity are separately frozen."
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
