#!/usr/bin/env python3
"""Recover the Southwest Pacific supplementary package via Europe PMC.

The Annals of Botany article is indexed in PMC as PMC12445859 and exposes the
same three supplementary files described by the publisher page. This route is
used only as a transport fallback when Oxford Academic delivery is blocked.

Admission is strict: filenames must match the configured supplements, OOXML
files must be structurally valid, and—when the checked source lock is present—
all recovered SHA-256 values must reproduce the already locked source bytes.
The emitted inventory mirrors the OUP lane so downstream schema and analysis
steps do not need a transport-specific branch.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import shutil
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping


USER_AGENT = "izu-core-source-audit/1.1 (+https://github.com/zuizui0223/izu-core)"


def load_config(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "source_id",
        "article_doi",
        "pmcid",
        "europe_pmc_supplementary_url",
        "expected_supplementary_files",
        "claim_boundary",
    }
    missing = sorted(required - set(data))
    if missing:
        raise ValueError(f"config missing required keys: {missing}")
    return data


def request_bytes(
    url: str, *, timeout: float = 90.0
) -> tuple[bytes, dict[str, str], str]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/zip,application/octet-stream,*/*;q=0.8",
            "Cache-Control": "no-cache",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return (
            response.read(),
            {key.casefold(): value for key, value in response.headers.items()},
            response.geturl(),
        )


def safe_member(name: str) -> Path:
    pure = PurePosixPath(name)
    if pure.is_absolute() or ".." in pure.parts:
        raise ValueError(f"unsafe archive member: {name!r}")
    parts = [part for part in pure.parts if part not in {"", "."}]
    if not parts:
        raise ValueError(f"empty archive member: {name!r}")
    return Path(*parts)


def extract_zip(payload: bytes, output_dir: Path) -> list[Path]:
    package = output_dir / "europe_pmc_supplementary_files.zip"
    package.write_bytes(payload)
    extracted_dir = output_dir / "pmc_extracted"
    if extracted_dir.exists():
        shutil.rmtree(extracted_dir)
    extracted_dir.mkdir(parents=True, exist_ok=True)
    extracted: list[Path] = []
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            relative = safe_member(info.filename)
            target = extracted_dir / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(info) as source, target.open("wb") as destination:
                shutil.copyfileobj(source, destination)
            extracted.append(target)
    return extracted


def normalize_filename(name: str) -> str:
    return Path(name).name.casefold()


def validate_office_file(path: Path) -> tuple[bool, str]:
    suffix = path.suffix.casefold()
    if suffix not in {".xlsx", ".docx"}:
        return False, "unsupported_extension"
    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
    except zipfile.BadZipFile:
        return False, "invalid_ooxml_zip"
    if "[Content_Types].xml" not in names:
        return False, "missing_content_types"
    if suffix == ".xlsx" and not any(name.startswith("xl/") for name in names):
        return False, "missing_xlsx_structure"
    if suffix == ".docx" and not any(name.startswith("word/") for name in names):
        return False, "missing_docx_structure"
    return True, "accepted"


def map_expected(
    extracted: Iterable[Path], expected_names: Iterable[str]
) -> tuple[dict[str, Path], list[Path]]:
    expected_names = list(expected_names)
    by_name = {normalize_filename(path.name): path for path in extracted}
    matched: dict[str, Path] = {}
    for expected in expected_names:
        candidate = by_name.get(normalize_filename(expected))
        if candidate is not None:
            matched[expected] = candidate
    expected_keys = {normalize_filename(name) for name in expected_names}
    unexpected = [
        path
        for path in extracted
        if normalize_filename(path.name) not in expected_keys
    ]
    return matched, unexpected


def load_checked_hashes(path: Path | None) -> dict[str, str]:
    if path is None or not path.exists():
        return {}
    document = json.loads(path.read_text(encoding="utf-8"))
    files = document.get("files") or {}
    if not isinstance(files, dict):
        return {}
    return {
        normalize_filename(filename): str(record["sha256"])
        for filename, record in files.items()
        if isinstance(record, Mapping) and record.get("sha256")
    }


def materialize_expected_files(
    matched: dict[str, Path],
    *,
    output_dir: Path,
    source_url: str,
    checked_hashes: Mapping[str, str],
) -> tuple[list[dict[str, object]], list[dict[str, str]]]:
    files_dir = output_dir / "files"
    if files_dir.exists():
        shutil.rmtree(files_dir)
    files_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    mismatches: list[dict[str, str]] = []
    for expected_name, source in sorted(matched.items()):
        target = files_dir / expected_name
        shutil.copy2(source, target)
        accepted, reason = validate_office_file(target)
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        expected_digest = checked_hashes.get(normalize_filename(expected_name))
        if expected_digest and digest != expected_digest:
            mismatches.append(
                {
                    "filename": expected_name,
                    "expected_sha256": expected_digest,
                    "observed_sha256": digest,
                }
            )
        with zipfile.ZipFile(target) as archive:
            members = archive.namelist()
        verified = accepted and (not expected_digest or digest == expected_digest)
        records.append(
            {
                "text": expected_name,
                "status": "downloaded_checksum_verified" if verified else reason,
                "url": source_url,
                "final_url": source_url,
                "content_type": None,
                "local_name": expected_name,
                "size": target.stat().st_size,
                "sha256": digest,
                "archive_members": members,
                "error": None if verified else reason,
            }
        )
        # The current analysis searches the source root for the configured file.
        shutil.copy2(target, output_dir / expected_name)
    return records, mismatches


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/southwest_pacific_aob_source.json"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/southwest_pacific_aob"),
    )
    parser.add_argument(
        "--source-lock",
        type=Path,
        default=Path("data/results/southwest_pacific_pairs/source_lock.json"),
    )
    args = parser.parse_args()

    config = load_config(args.config)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    errors: list[dict[str, str]] = []
    package: dict[str, object] | None = None
    extracted: list[Path] = []

    url = str(config["europe_pmc_supplementary_url"])
    final_url = url
    try:
        payload, headers, final_url = request_bytes(url)
        if not zipfile.is_zipfile(io.BytesIO(payload)):
            raise ValueError(
                "Europe PMC supplementary endpoint did not return a ZIP; "
                f"content_type={headers.get('content-type')!r}, prefix={payload[:80]!r}"
            )
        extracted = extract_zip(payload, args.output_dir)
        package = {
            "status": "downloaded",
            "requested_url": url,
            "resolved_url_without_query": urllib.parse.urlunsplit(
                (*urllib.parse.urlsplit(final_url)[:3], "", "")
            ),
            "content_type": headers.get("content-type"),
            "size_bytes": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        }
    except Exception as error:
        errors.append(
            {
                "stage": "europe_pmc_supplementary_package",
                "url": url,
                "error": repr(error),
            }
        )

    expected = [str(name) for name in config["expected_supplementary_files"]]
    matched, unexpected = map_expected(extracted, expected)
    checked_hashes = load_checked_hashes(args.source_lock)
    records, mismatches = materialize_expected_files(
        matched,
        output_dir=args.output_dir,
        source_url=final_url,
        checked_hashes=checked_hashes,
    )
    missing = [name for name in expected if name not in matched]
    complete = not missing and not mismatches and len(records) == len(expected)
    status = (
        "supplementary_files_acquired_checksum_verified"
        if complete
        else "supplementary_acquisition_partial"
        if matched
        else "supplementary_acquisition_blocked"
    )
    inventory = {
        "schema_version": "1.1",
        "status": status,
        "acquisition_route": "europe_pmc_supplementary_files",
        "source_id": config["source_id"],
        "article_doi": config["article_doi"],
        "pmcid": config["pmcid"],
        "crossref_message": {
            "title": ["Flower size evolution in the Southwest Pacific"]
        },
        "package": package,
        "n_candidates": len(expected),
        "n_downloaded": len(records),
        "expected_supplementary_files": expected,
        "recovered_supplementary_files": sorted(matched),
        "missing_supplementary_files": missing,
        "checksum_lock_path": str(args.source_lock) if checked_hashes else None,
        "checksum_mismatches": mismatches,
        "discovery_pages": [],
        "files": records,
        "unexpected_package_files": [
            {
                "filename": path.name,
                "relative_path": str(path.relative_to(args.output_dir)),
                "size_bytes": path.stat().st_size,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
            for path in unexpected
        ],
        "errors": errors,
        "analysis_source": config.get("analysis_source"),
        "expected_context_to_verify_from_source": config.get(
            "expected_context_to_verify_from_source"
        ),
        "claim_boundary": config["claim_boundary"],
    }
    path = args.output_dir / "source_inventory.json"
    path.write_text(
        json.dumps(inventory, indent=2, ensure_ascii=False, default=str) + "\n",
        encoding="utf-8",
    )
    print(f"Europe PMC supporting files recovered: {len(matched)}/{len(expected)}")
    print(f"checksum mismatches: {len(mismatches)}")
    print(f"status: {status}")
    if not complete:
        raise RuntimeError(
            "Europe PMC supplementary recovery did not reproduce the checked "
            "source; see source_inventory.json"
        )


if __name__ == "__main__":
    main()
