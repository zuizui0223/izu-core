#!/usr/bin/env python3
"""Acquire the exact Hendriks 2019 VUW thesis bytes through the public Figshare API.

This is a provenance acquisition step, not an evidence-admission step.  It
validates the institutional article identity, resolves the expected file through
public Figshare metadata, downloads exact PDF bytes, and records cryptographic
checksums.  Successful acquisition alone does not promote the reconstructed
35-pair effect into the formal cross-system registry; pair/island re-verification
and the separate EIV gate still apply.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "data/source_tables/hendriks_2019_flower_area_table_b9_source.json"
DEFAULT_OUTPUT_DIR = ROOT / "artifacts/hendriks_2019/source_lock"
API_BASE = "https://api.figshare.com/v2"
USER_AGENT = "izu-core-hendriks-provenance/1.0 (+research reproducibility audit)"


def get_json(url: str, timeout: float = 30.0) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def download_bytes(url: str, timeout: float = 60.0) -> tuple[bytes, str]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/pdf,*/*;q=0.8"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read(), response.geturl()


def article_id_from_source(source: dict[str, Any]) -> int:
    page = str(source.get("institutional_record_page") or "").rstrip("/")
    if not page:
        raise ValueError("institutional_record_page is missing")
    token = page.rsplit("/", 1)[-1]
    if not token.isdigit():
        raise ValueError(f"cannot resolve Figshare article id from {page!r}")
    return int(token)


def expected_file_id_from_source(source: dict[str, Any]) -> int:
    url = str(source.get("institutional_download_url") or "").rstrip("/")
    if not url:
        raise ValueError("institutional_download_url is missing")
    token = url.rsplit("/", 1)[-1]
    if not token.isdigit():
        raise ValueError(f"cannot resolve expected Figshare file id from {url!r}")
    return int(token)


def canonical_figshare_doi(value: str) -> str:
    """Compare Figshare record DOI identity while tolerating only a terminal .vN."""
    doi = value.casefold().strip()
    return re.sub(r"\.v\d+$", "", doi)


def validate_article_metadata(metadata: dict[str, Any], source: dict[str, Any]) -> None:
    expected_title = str(source["title"]).casefold().strip()
    observed_title = str(metadata.get("title") or "").casefold().strip()
    if expected_title != observed_title:
        raise ValueError(
            f"institutional article title mismatch: {observed_title!r} != {expected_title!r}"
        )

    expected_doi = str(source.get("institutional_identifier") or "").casefold().strip()
    observed_doi = str(metadata.get("doi") or "").casefold().strip()
    if (
        expected_doi
        and observed_doi
        and canonical_figshare_doi(expected_doi) != canonical_figshare_doi(observed_doi)
    ):
        raise ValueError(
            f"institutional DOI mismatch: {observed_doi!r} != {expected_doi!r}"
        )


def select_expected_file(metadata: dict[str, Any], expected_file_id: int) -> dict[str, Any]:
    files = metadata.get("files") or []
    matches = [item for item in files if int(item.get("id", -1)) == expected_file_id]
    if len(matches) != 1:
        raise ValueError(
            f"expected exactly one Figshare file id {expected_file_id}, found {len(matches)}"
        )
    selected = dict(matches[0])
    if not selected.get("download_url"):
        raise ValueError("expected Figshare file has no download_url")
    return selected


def checksum_record(data: bytes) -> dict[str, Any]:
    return {
        "n_bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "md5": hashlib.md5(data).hexdigest(),  # nosec B324 - integrity comparison only
        "pdf_magic_valid": data.startswith(b"%PDF-"),
    }


def build_lock(
    *,
    source: dict[str, Any],
    article_id: int,
    metadata: dict[str, Any],
    file_metadata: dict[str, Any],
    data: bytes,
    final_download_url: str,
) -> dict[str, Any]:
    checksums = checksum_record(data)
    if not checksums["pdf_magic_valid"]:
        raise ValueError("downloaded institutional artifact does not begin with PDF magic")

    supplied_md5 = str(file_metadata.get("supplied_md5") or "").lower().strip()
    computed_md5 = str(file_metadata.get("computed_md5") or "").lower().strip()
    if supplied_md5 and supplied_md5 != checksums["md5"]:
        raise ValueError("downloaded MD5 does not match Figshare supplied_md5")
    if computed_md5 and computed_md5 != checksums["md5"]:
        raise ValueError("downloaded MD5 does not match Figshare computed_md5")

    return {
        "schema_version": "1.0",
        "status": "institutional_pdf_bytes_recovered_and_checksum_locked",
        "source_id": source.get("source_id"),
        "institutional_identifier": source.get("institutional_identifier"),
        "figshare_article_id": article_id,
        "figshare_file_id": int(file_metadata["id"]),
        "article_title": metadata.get("title"),
        "article_doi": metadata.get("doi"),
        "file_name": file_metadata.get("name"),
        "figshare_download_url": file_metadata.get("download_url"),
        "final_download_url": final_download_url,
        "checksums": checksums,
        "figshare_supplied_md5": supplied_md5 or None,
        "figshare_computed_md5": computed_md5 or None,
        "provenance_gate_opened": False,
        "pair_verification_complete": False,
        "island_assignment_verification_complete": False,
        "eiv_gate_opened": False,
        "formal_cross_system_admission_opened": False,
        "claim_boundary": (
            "Exact institutional PDF bytes and cryptographic checksums are acquisition evidence. "
            "The Hendriks provenance gate remains closed until all 35 Table B9 pairs and Appendix-A "
            "island assignments are re-verified against these exact bytes. EIV remains separate."
        ),
    }


def write_failure(path: Path, *, article_id: int | None, error: Exception) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "1.0",
        "status": "institutional_byte_acquisition_blocked_this_run",
        "figshare_article_id": article_id,
        "error_type": type(error).__name__,
        "error": str(error),
        "biological_result_changed": False,
        "provenance_gate_opened": False,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()

    source = json.loads(args.source.read_text(encoding="utf-8"))
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    article_id: int | None = None
    try:
        article_id = article_id_from_source(source)
        expected_file_id = expected_file_id_from_source(source)
        metadata_url = f"{API_BASE}/articles/{article_id}"
        metadata = get_json(metadata_url, timeout=args.timeout)
        validate_article_metadata(metadata, source)
        file_metadata = select_expected_file(metadata, expected_file_id)
        data, final_url = download_bytes(
            str(file_metadata["download_url"]), timeout=max(args.timeout, 60.0)
        )
        lock = build_lock(
            source=source,
            article_id=article_id,
            metadata=metadata,
            file_metadata=file_metadata,
            data=data,
            final_download_url=final_url,
        )
        pdf_path = output_dir / "hendriks_2019_vuw_thesis.pdf"
        lock_path = output_dir / "source_lock.json"
        pdf_path.write_bytes(data)
        lock_path.write_text(json.dumps(lock, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(lock_path)
    except Exception as error:
        write_failure(output_dir / "acquisition_state.json", article_id=article_id, error=error)
        raise


if __name__ == "__main__":
    main()
