"""Read-only byte and ZIP sidecar verification of fixed-B48 source shard 18.

This checks the exact original Actions artifact bytes, not the stopped private
backup transfer, an external DOI archive, or a biological outcome replay.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ARTIFACT_ID = 11600619779
SOURCE_RUN = 37896872795
EXPECTED_NAME = "chapter2-k48-future-shard-18.zip"
EXPECTED_SIZE = 118143
EXPECTED_SHA256 = "1b4c1450c387e24a844a97b25bcf01df20001ffe3afad64e2044e5d28cad3ff4"
EXPECTED_PROTOCOL_SHA256 = "64188a5c13a8681eb96c2237ab1c43c2f7b7f88910c230bcdb47bc81d3826672"
MANIFEST_NAME = "k48_future_shard_18.json"
EXPECTED_STATUS = "K_FIXEDB48_COMPLETE_32_SOURCES_1792_FUTURES_UNADJUDICATED"


def verify(path: Path, *, expected_sha256: str = EXPECTED_SHA256,
           expected_size: int = EXPECTED_SIZE) -> dict:
    raw = Path(path).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if len(raw) != expected_size or digest != expected_sha256:
        raise ValueError("original Actions ZIP size or SHA-256 differs")

    with zipfile.ZipFile(path) as archive:
        entries = archive.namelist()
        if len(entries) != 65 or len(set(entries)) != 65:
            raise ValueError("original Actions ZIP member count or uniqueness differs")
        if archive.testzip() is not None:
            raise ValueError("original Actions ZIP CRC failure")
        if MANIFEST_NAME not in entries:
            raise ValueError("original source manifest missing")
        manifest = json.loads(archive.read(MANIFEST_NAME))
        if (manifest.get("history") != 41110919 or manifest.get("shard") != 18
                or manifest.get("n_sources") != 32 or manifest.get("n_futures") != 1792
                or manifest.get("status") != EXPECTED_STATUS
                or manifest.get("protocol_sha256") != EXPECTED_PROTOCOL_SHA256):
            raise ValueError("original source manifest metadata differs")
        case_keys = manifest.get("case_keys")
        if not isinstance(case_keys, list) or len(case_keys) != 32 or len(set(case_keys)) != 32:
            raise ValueError("original source case-key set differs")
        expected_names = {MANIFEST_NAME}
        for case in case_keys:
            if not isinstance(case, str) or "/" in case or "\\" in case or case.startswith("."):
                raise ValueError("unsafe original source case key")
            expected_names.add("k48_" + case + ".json")
            expected_names.add("k48_" + case + ".sha256")
        if set(entries) != expected_names:
            raise ValueError("original Actions ZIP missing or extra case payloads")
        for case in case_keys:
            filename = "k48_" + case
            saved_hash = archive.read(filename + ".sha256").decode("ascii").strip()
            actual_hash = hashlib.sha256(archive.read(filename + ".json")).hexdigest()
            if saved_hash != actual_hash:
                raise ValueError("original JSON/sidecar SHA-256 mismatch: " + case)
        uncompressed_bytes = sum(i.file_size for i in archive.infolist())

    return {
        "status": "SOURCE_ACTIONS_SHARD18_BYTES_AND_32_CASE_SIDECARS_VERIFIED",
        "artifact_name": EXPECTED_NAME,
        "source_workflow_run": SOURCE_RUN,
        "source_artifact_id": ARTIFACT_ID,
        "actual_zip_bytes": len(raw),
        "actual_zip_sha256": digest,
        "zip_member_count": len(entries),
        "zip_unique_member_count": len(set(entries)),
        "zip_crc_failure_count": 0,
        "json_sha256_sidecars_checked": 32,
        "json_sha256_sidecar_mismatches": 0,
        "uncompressed_payload_bytes": uncompressed_bytes,
        "shard": manifest["shard"],
        "history": manifest["history"],
        "source_cases_declared": manifest["n_sources"],
        "future_conditions_declared": manifest["n_futures"],
        "protocol_sha256": manifest["protocol_sha256"],
        "source_manifest_status": manifest["status"],
        "scope": "Original GitHub Actions ZIP readback only; no private external transfer, independent biological replay, or DOI deposit.",
        "private_external_backup_restored": False,
        "original_results_or_decisions_changed": False,
        "doi_assigned": False,
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("archive", type=Path)
    p.add_argument("--receipt", type=Path, help="Optional local-only JSON receipt path")
    args = p.parse_args()
    result = verify(args.archive)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
