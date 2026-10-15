"""Offline-only consistency check for the unpublished Chapter 2 Zenodo proposal.

No Zenodo calls, upload, DOI reservation, simulation or private-transfer action.
This verifies source-receipt metadata, not the actual bytes of each giant archive.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = "docs/deposit/chapter2_zenodo_unpublished_preflight_20261015.json"
HANDOFF = "data/submission/chapter2_private_external_backup_deposit_handoff_20261013.json"
SOURCE_MD = "docs/CHAPTER2_UNIFIED_DATA_DEPOSIT_READINESS_20261011.md"
EVOLUTION = "data/submission/chapter2_evolution_archive_recovery_20261011.json"
TEMPO = "data/results/chapter2_sequence_abrupt_gradual_functional_loss_receipt_20261011.json"
DISCOVERY = "docs/CHAPTER2_SOURCE_REPLAY_COHORT_IDENTITY_20261011.md"
SI = "docs/CHAPTER2_UNIFIED_EL_SUPPORTING_INFORMATION_20261010.md"


def read(root: Path, path: str) -> dict:
    return json.loads((root / path).read_text(encoding="utf-8"))


def validate_record(d: dict) -> None:
    if (d["preflight_only"] is not True or
            d["fixed_b48_private_provider_safety_stop_must_not_be_bypassed"] is not True):
        raise ValueError("Zenodo planning-only and safety boundary missing")
    for k in ("external_draft_created", "external_uploads_performed", "doi_reserved",
              "published", "ready_to_upload_or_publish", "paper_submitted"):
        if d.get(k) is not False:
            raise ValueError("unapproved Zenodo action or publication: " + k)
    if d.get("external_record_id") is not None or d.get("doi_assigned") is not None:
        raise ValueError("cannot invent unverified DOI/record ID")
    if d.get("demographic_external_private_copy_verified") != "520/521":
        raise ValueError("blocked private backup must stay 520/521")
    meta = d["record"]
    for k in ("ordered_creators", "affiliations_and_identifiers", "data_license",
              "code_license", "resource_version", "access_or_embargo_choice",
              "access_or_embargo_release_date"):
        if meta.get(k) is not None:
            raise ValueError("approval-required Zenodo metadata must remain unset")
    for k in ("disclosure_and_rights_review_approved",
              "depositor_account_authenticated", "metadata_ready_for_zenodo_save"):
        if meta.get(k) is not False:
            raise ValueError("unauthenticated Zenodo account/approval")
    if meta.get("type") != "dataset":
        raise ValueError("invalid resource type")
    limits = d["limits_confirmed_from_zenodo_help"]
    if (limits["maximum_files_per_record"] != 100 or
            limits["maximum_total_bytes_per_record"] != 50_000_000_000 or
            limits["creators_required"] is not True):
        raise ValueError("Zenodo limit/creator requirement needs fresh verification")
    files = d["six_core_packages"]
    if len(files) != 6 or len({x["filename"] for x in files}) != 6:
        raise ValueError("missing or duplicate core archive")
    total = sum(x["bytes"] for x in files)
    if total != 1_691_637_982 or d["six_core_bytes"] != total or d["six_core_file_count"] != 6:
        raise ValueError("six core archive size disagrees")
    if sum(x.get("inner_original_zip_count", 0) for x in files[:4]) != 521:
        raise ValueError("source ZIP denominators changed")
    for f in files:
        if (not isinstance(f["bytes"], int) or f["bytes"] < 1 or
                re.fullmatch(r"[0-9a-f]{64}", f["sha256"]) is None or
                f["fresh_container_byte_check_in_this_preflight"] is not False):
            raise ValueError("unverified original archive bytes/hashes")
    extra = d["additional_documented_archives_not_yet_admitted"]
    if (len(extra) != 2 or
            d["additional_candidate_bytes"] != sum(x["bytes"] for x in extra) or
            d["eight_known_archive_bytes_if_all_admitted"] != total + d["additional_candidate_bytes"]):
        raise ValueError("extra source candidates inconsistent")
    if (d["fixed_b48_missing_external_private_original"] !=
            "chapter2-k48-future-shard-18.zip" or not d["missing_manifest_scope"]):
        raise ValueError("known incomplete source/review gate suppressed")


def validate_repo(root: Path = ROOT, record: dict | None = None) -> dict:
    d = read(root, RECORD) if record is None else record
    validate_record(d)
    hand = read(root, HANDOFF)
    if (hand["original_actions_zip_total"] != 521 or
            hand["external_verified_unique_zip_total"] != 520 or
            "do_not_bypass" not in hand["cohorts"]["fixed_b48"]["missing_original"]["external_transfer_status"]):
        raise ValueError("frozen backup handoff changed")
    text = (root / SOURCE_MD).read_text(encoding="utf-8")
    expected = [
        ("orthogonal", 130), ("kb", 130), ("fixed_b48", 131), ("timed", 130)
    ]
    quote = chr(96)
    for f, (group, n) in zip(d["six_core_packages"][:4], expected):
        if (f["cohort"] != group or f["inner_original_zip_count"] != n or
                hand["cohorts"][group]["n_original"] != n):
            raise ValueError("wrong demographic source identity/count")
        needle = "| " + quote + f["filename"] + quote + " | " + quote + f["sha256"] + quote + " |"
        if needle not in text or f"{f['bytes']:,} bytes" not in text:
            raise ValueError("tar identity not present in historical source receipt")
    ev = read(root, EVOLUTION)["assembled_outer_archive"]
    evo = d["six_core_packages"][4]
    if (evo["filename"] != ev["filename"] or
            evo["bytes"] != ev["builder_receipt"]["bundle_bytes"] or
            evo["sha256"] != ev["builder_receipt"]["bundle_sha256"] or
            evo["inner_original_zip_count"] != ev["builder_receipt"]["artifact_count"]):
        raise ValueError("evolution source archive mismatch")
    tp = read(root, TEMPO)["raw_archive"]
    tempo = d["six_core_packages"][5]
    if (tempo["filename"] != tp["filename"] or tempo["bytes"] != tp["size_bytes"] or
            tempo["sha256"] != tp["sha256"] or
            tempo["inner_raw_member_count"] != tp["member_count_including_inventory"]):
        raise ValueError("tempo source archive mismatch")
    for extra, path in zip(d["additional_documented_archives_not_yet_admitted"], (DISCOVERY, SI)):
        source = (root / path).read_text(encoding="utf-8")
        if extra["sha256"] not in source or str(extra["bytes"]) not in source.replace(",", ""):
            raise ValueError("additional archive source receipt not matched")
    return {
        "status": "PASS_READONLY_PREPARED_METADATA_NO_REMOTE_DRAFT",
        "core_files": len(d["six_core_packages"]),
        "core_bytes": d["six_core_bytes"],
        "additional_source_candidates": len(d["additional_documented_archives_not_yet_admitted"]),
        "eight_known_bytes_if_included": d["eight_known_archive_bytes_if_all_admitted"],
        "private_backup_coverage": "520/521",
        "external_zenodo_draft_created": False,
        "doi_assigned": False,
        "complete_paper_source_inventory": False,
    }


if __name__ == "__main__":
    print(json.dumps(validate_repo(), indent=2))
