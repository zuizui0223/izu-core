from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data/results/abm_v13_hawaii_lobelioid_dryad_package_recovery.json"
DEFAULT_BYTES_DIR = ROOT / ".artifacts/abm_v13_hawaii_lobelioid_package"
PACKAGE_URL = "https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.sj3tx96kr/download"
USER_AGENT = "izu-core-v13-hawaii-lobelioid-package-recovery/1.0"
EXPECTED = {
    "Case_FE_2026_Analysis_1.csv": (
        "bird_species", "culmen", "island", "assemblage", "plant_species", "flower_length", "bill_minus_flower"
    ),
    "Case_FE_2026_Analysis_2.csv": (
        "plant_species", "bird_species", "N", "pollen_contact", "nectar_robbing", "source", "culmen", "flower_length", "bill_minus_flower"
    ),
    "README.md": (),
}


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def fetch_package(*, timeout: int = 120) -> tuple[bytes | None, dict[str, object]]:
    request = urllib.request.Request(
        PACKAGE_URL,
        headers={"User-Agent": USER_AGENT, "Accept": "application/zip"},
    )
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
        body = exc.read(500).decode("utf-8", errors="replace")
        return None, {
            "http_status": int(exc.code),
            "content_type": exc.headers.get("Content-Type") if exc.headers else None,
            "final_url": exc.geturl(),
            "transport_error": f"HTTPError: {exc.code} {exc.reason}",
            "response_preview": body,
        }
    except Exception as exc:
        return None, {
            "http_status": None,
            "content_type": None,
            "final_url": PACKAGE_URL,
            "transport_error": f"{type(exc).__name__}: {exc}",
            "response_preview": None,
        }


def csv_audit(payload: bytes, required: tuple[str, ...]) -> dict[str, object]:
    text = payload.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    fields = tuple(reader.fieldnames or ())
    rows = list(reader)
    missing = [column for column in required if column not in fields]
    return {
        "columns": list(fields),
        "row_count": len(rows),
        "missing_required_columns": missing,
        "required_columns_present": not missing,
    }


def member_by_basename(archive: zipfile.ZipFile, basename: str) -> str | None:
    matches = [name for name in archive.namelist() if Path(name).name == basename and not name.endswith("/")]
    return matches[0] if len(matches) == 1 else None


def audit_package(payload: bytes, *, bytes_dir: Path) -> dict[str, object]:
    bytes_dir.mkdir(parents=True, exist_ok=True)
    package_path = bytes_dir / "dryad_dataset_package.zip"
    package_path.write_bytes(payload)
    try:
        archive = zipfile.ZipFile(io.BytesIO(payload))
    except zipfile.BadZipFile:
        return {
            "zip_valid": False,
            "package_sha256": sha256_bytes(payload),
            "package_byte_count": len(payload),
            "package_saved_path": str(package_path),
            "members": [],
            "expected_files": {},
            "all_expected_files_unique_and_valid": False,
        }

    members = archive.namelist()
    results: dict[str, object] = {}
    all_valid = True
    for basename, required in EXPECTED.items():
        member = member_by_basename(archive, basename)
        if member is None:
            results[basename] = {"found_unique": False}
            all_valid = False
            continue
        content = archive.read(member)
        target = bytes_dir / basename
        target.write_bytes(content)
        row: dict[str, object] = {
            "found_unique": True,
            "archive_member": member,
            "byte_count": len(content),
            "sha256": sha256_bytes(content),
            "saved_path": str(target),
        }
        if basename.endswith(".csv"):
            try:
                audit = csv_audit(content, required)
            except UnicodeDecodeError as exc:
                audit = {"decode_error": str(exc), "required_columns_present": False, "row_count": 0}
            row["csv_schema"] = audit
            valid = bool(audit.get("required_columns_present") and int(audit.get("row_count", 0)) > 0)
        else:
            try:
                content.decode("utf-8-sig")
                valid = len(content) > 0
            except UnicodeDecodeError:
                valid = False
            row["utf8_nonempty"] = valid
        row["source_member_gate_passes"] = valid
        all_valid = all_valid and valid
        results[basename] = row
    archive.close()
    return {
        "zip_valid": True,
        "package_sha256": sha256_bytes(payload),
        "package_byte_count": len(payload),
        "package_saved_path": str(package_path),
        "members": members,
        "expected_files": results,
        "all_expected_files_unique_and_valid": all_valid,
    }


def recover(*, bytes_dir: Path = DEFAULT_BYTES_DIR, timeout: int = 120) -> dict[str, object]:
    payload, transport = fetch_package(timeout=timeout)
    if payload is None:
        status = transport.get("http_status")
        if status == 401:
            decision = "blocked_dryad_package_api_requires_authentication"
        elif status == 403:
            decision = "blocked_dryad_package_api_forbidden"
        else:
            decision = "blocked_dryad_package_transport"
        package_audit = None
    else:
        package_audit = audit_package(payload, bytes_dir=bytes_dir)
        decision = (
            "hawaii_lobelioid_package_recovered_ready_for_row_schema_freeze"
            if package_audit["all_expected_files_unique_and_valid"]
            else "hawaii_lobelioid_package_recovered_but_source_gate_failed"
        )
    return {
        "analysis": "abm_v13_hawaii_lobelioid_dryad_package_recovery",
        "dataset_doi": "10.5061/dryad.sj3tx96kr",
        "package_url": PACKAGE_URL,
        "route": "Dryad REST API latest-visible-version ZIP package; distinct from /downloads/file_stream/{id}",
        "bearer_token_supplied": False,
        "target_metrics_calculated": False,
        "transport": transport,
        "package_audit": package_audit,
        "decision": decision,
        "next_gate": (
            "freeze exact recovered member checksums, row identities and signed-position arithmetic before target reanalysis"
            if decision == "hawaii_lobelioid_package_recovered_ready_for_row_schema_freeze"
            else "do not retry anonymously if API authentication is required; retain source target closed unless exact lawful mirror bytes are obtained"
        ),
        "claim_boundary": "This is a distinct source-transport test only. Failure due API authentication is not biological evidence and does not justify reconstructing raw rows from publication text.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--bytes-dir", type=Path, default=DEFAULT_BYTES_DIR)
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()
    result = recover(bytes_dir=args.bytes_dir, timeout=args.timeout)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "decision": result["decision"],
        "http_status": result["transport"].get("http_status"),
        "package_gate": None if result["package_audit"] is None else result["package_audit"]["all_expected_files_unique_and_valid"],
    }, indent=2))


if __name__ == "__main__":
    main()
