#!/usr/bin/env python3
"""Recover open PLOS supporting files for the Canary–Balearic communities.

This is a cross-source recovery probe. The 2016 PLOS article reuses the same
four named communities as the 2014 Canary–Balearic network comparison, but its
supporting files are not admitted as the complete 2014 network source until the
file contents pass an explicit identity and scope audit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


USER_AGENT = "izu-core-source-audit/1.0 (+https://github.com/zuizui0223/izu-core)"
OLE_MAGIC = bytes.fromhex("d0cf11e0a1b11ae1")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def load_config(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "source_id",
        "article_doi",
        "pmcid",
        "europe_pmc_supplementary_url",
        "expected_files",
        "claim_boundary",
    }
    missing = sorted(required - set(data))
    if missing:
        raise ValueError(f"config missing required keys: {missing}")
    return data


def request_bytes(url: str, *, timeout: float = 60.0) -> tuple[bytes, dict[str, str], str]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/zip, application/octet-stream, application/msword, */*",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = response.read()
        headers = {key.casefold(): value for key, value in response.headers.items()}
        return payload, headers, response.geturl()


def payload_kind(payload: bytes) -> str:
    prefix = payload[:256].lstrip().lower()
    if payload.startswith(b"PK\x03\x04"):
        return "zip"
    if payload.startswith(OLE_MAGIC):
        return "ole_doc"
    if prefix.startswith(b"{\\rtf"):
        return "rtf"
    if prefix.startswith(b"<!doctype html") or prefix.startswith(b"<html"):
        return "html"
    return "unknown"


def logical_id_from_name(name: str) -> str | None:
    match = re.search(r"(?:^|[._-])(s00[1-9])(?:[._-]|$)", name.casefold())
    return match.group(1) if match else None


def safe_archive_member(name: str) -> Path:
    pure = PurePosixPath(name)
    if pure.is_absolute() or ".." in pure.parts:
        raise ValueError(f"unsafe archive member: {name!r}")
    clean_parts = [part for part in pure.parts if part not in {"", "."}]
    if not clean_parts:
        raise ValueError(f"empty archive member: {name!r}")
    return Path(*clean_parts)


def extract_zip(zip_path: Path, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    extracted: list[Path] = []
    with zipfile.ZipFile(zip_path) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            relative = safe_archive_member(info.filename)
            target = output_dir / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(info) as source, target.open("wb") as destination:
                shutil.copyfileobj(source, destination)
            extracted.append(target)
    return extracted


def direct_candidates(article_doi: str, pmcid: str, logical_id: str) -> tuple[str, ...]:
    suffix_doi = f"{article_doi}.{logical_id}"
    pmc_number = pmcid.removeprefix("PMC")
    encoded_info = urllib.parse.urlencode(
        {"type": "supplementary", "id": f"info:doi/{suffix_doi}"}
    )
    encoded_plain = urllib.parse.urlencode(
        {"id": suffix_doi, "type": "supplementary"}
    )
    return (
        f"https://journals.plos.org/plosone/article/file?{encoded_info}",
        f"https://journals.plos.org/plosone/article/file?{encoded_plain}",
        f"https://pmc.ncbi.nlm.nih.gov/articles/instance/{pmc_number}/bin/pone.0150824.{logical_id}.doc",
    )


def file_record(
    path: Path,
    *,
    root: Path,
    logical_id: str | None,
    source_url: str | None,
) -> dict[str, object]:
    payload = path.read_bytes()
    return {
        "logical_id": logical_id,
        "path": str(path.relative_to(root)),
        "filename": path.name,
        "size_bytes": len(payload),
        "sha256": sha256_bytes(payload),
        "payload_kind": payload_kind(payload),
        "source_url_without_query": (
            urllib.parse.urlunsplit((*urllib.parse.urlsplit(source_url)[:3], "", ""))
            if source_url
            else None
        ),
    }


def inventory_expected_files(paths: Iterable[Path]) -> dict[str, Path]:
    output: dict[str, Path] = {}
    for path in paths:
        logical_id = logical_id_from_name(path.name)
        if logical_id is not None and logical_id not in output:
            output[logical_id] = path
    return output


def reconcile_package_record(
    package_record: dict[str, object] | None,
    config: dict[str, Any],
) -> dict[str, object] | None:
    """Retain the repository-locked package checksum across transport failures.

    A failed ZIP transport must not erase a checksum established by an earlier
    successful lawful recovery. If the package is observed again, checksum drift
    is a provenance gate rather than an automatic source update.
    """
    locked = str(config.get("locked_package_sha256") or "").strip().casefold()
    if locked and not re.fullmatch(r"[0-9a-f]{64}", locked):
        raise ValueError("locked_package_sha256 must be a 64-character hex digest")
    if package_record is None:
        if not locked:
            return None
        return {
            "status": "not_recovered_this_run_locked_checksum_retained",
            "sha256": locked,
            "provenance": "repository_locked_prior_successful_package",
        }
    observed = str(package_record.get("sha256") or "").strip().casefold()
    if locked and observed != locked:
        raise ValueError(
            f"Europe PMC supplementary package checksum drift: observed={observed!r} locked={locked!r}"
        )
    return package_record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/canary_balearic_plos_source.json"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/canary_balearic_plos"),
    )
    args = parser.parse_args()

    config = load_config(args.config)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    files_dir = args.output_dir / "files"
    files_dir.mkdir(parents=True, exist_ok=True)
    errors: list[dict[str, str]] = []
    package_record: dict[str, object] | None = None
    extracted: list[Path] = []

    package_url = str(config["europe_pmc_supplementary_url"])
    try:
        payload, headers, resolved_url = request_bytes(package_url)
        kind = payload_kind(payload)
        if kind != "zip":
            raise ValueError(
                f"Europe PMC supplementary endpoint did not return a ZIP: kind={kind}, "
                f"content_type={headers.get('content-type')!r}, prefix={payload[:80]!r}"
            )
        package_path = args.output_dir / "supplementary_files.zip"
        package_path.write_bytes(payload)
        package_record = {
            "status": "downloaded",
            "requested_url": package_url,
            "resolved_url_without_query": urllib.parse.urlunsplit(
                (*urllib.parse.urlsplit(resolved_url)[:3], "", "")
            ),
            "size_bytes": len(payload),
            "sha256": sha256_bytes(payload),
            "content_type": headers.get("content-type"),
        }
        extracted.extend(extract_zip(package_path, files_dir))
    except Exception as error:
        errors.append(
            {
                "stage": "europe_pmc_supplementary_package",
                "url": package_url,
                "error": repr(error),
            }
        )

    package_record = reconcile_package_record(package_record, config)

    expected = {str(row["logical_id"]): row for row in config["expected_files"]}
    discovered = inventory_expected_files(extracted)
    source_urls: dict[str, str] = {}

    for logical_id in expected:
        if logical_id in discovered:
            continue
        for url in direct_candidates(
            str(config["article_doi"]), str(config["pmcid"]), logical_id
        ):
            try:
                payload, headers, resolved_url = request_bytes(url)
                kind = payload_kind(payload)
                if kind in {"html", "unknown"}:
                    raise ValueError(
                        f"unexpected payload kind={kind}, content_type={headers.get('content-type')!r}, "
                        f"prefix={payload[:80]!r}"
                    )
                suffix = ".docx" if kind == "zip" else ".doc"
                target = files_dir / f"pone.0150824.{logical_id}{suffix}"
                target.write_bytes(payload)
                discovered[logical_id] = target
                source_urls[logical_id] = resolved_url
                break
            except Exception as error:
                errors.append(
                    {
                        "stage": f"direct_{logical_id}",
                        "url": url,
                        "error": repr(error),
                    }
                )

    records: list[dict[str, object]] = []
    for logical_id in sorted(discovered):
        record = file_record(
            discovered[logical_id],
            root=args.output_dir,
            logical_id=logical_id,
            source_url=source_urls.get(logical_id),
        )
        record["declared_scope"] = expected.get(logical_id, {}).get("declared_scope")
        record["declared_title"] = expected.get(logical_id, {}).get("title")
        records.append(record)

    recovered = sorted(set(discovered) & set(expected))
    missing = sorted(set(expected) - set(discovered))
    status = "complete" if not missing else "partial" if recovered else "blocked"
    inventory = {
        "schema_version": "1.0",
        "status": status,
        "source_id": config["source_id"],
        "article_doi": config["article_doi"],
        "pmcid": config["pmcid"],
        "source_role": config.get("source_role"),
        "target_source_id": config.get("target_source_id"),
        "target_article_doi": config.get("target_article_doi"),
        "package": package_record,
        "expected_logical_ids": sorted(expected),
        "recovered_logical_ids": recovered,
        "missing_logical_ids": missing,
        "n_expected": len(expected),
        "n_recovered": len(recovered),
        "files": records,
        "errors": errors,
        "community_map_to_verify": config.get("community_map_to_verify"),
        "cross_source_identity_gate": config.get("cross_source_identity_gate"),
        "claim_boundary": config["claim_boundary"],
    }
    inventory_path = args.output_dir / "source_inventory.json"
    inventory_path.write_text(
        json.dumps(inventory, indent=2, ensure_ascii=False, default=str) + "\n",
        encoding="utf-8",
    )
    print(f"supporting files recovered: {len(recovered)}/{len(expected)}")
    print(f"status: {status}")
    print(inventory_path)
    if not recovered:
        raise RuntimeError(
            "PLOS/Europe PMC supporting-file recovery blocked; see source_inventory.json"
        )


if __name__ == "__main__":
    main()
