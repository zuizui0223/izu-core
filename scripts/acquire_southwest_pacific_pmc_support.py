#!/usr/bin/env python3
"""Recover the open Southwest Pacific supplementary package via Europe PMC.

The Annals of Botany article is indexed in PMC as PMC12445859 and exposes the
same three supplementary files described by the publisher page. This route is
used only as a transport fallback when Oxford Academic delivery is blocked.
Expected filenames are taken from the source config; unexpected files are kept
in the audit but cannot silently replace the configured analysis source.

On complete recovery the script writes the same ``source_inventory.json`` path
used by the Oxford acquirer so downstream schema and analysis steps do not need
a transport-specific branch. A previous Oxford inventory may be preserved by
the workflow as ``oup_source_inventory.json`` before this fallback runs.
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
from typing import Any, Iterable


USER_AGENT = "izu-core-source-audit/1.0 (+https://github.com/zuizui0223/izu-core)"


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


def request_bytes(url: str, *, timeout: float = 90.0) -> tuple[bytes, dict[str, str], str]:
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
    extracted_dir.mkdir(parents=True, exist_ok=True)
    extracted: list[Path] = []
    with zipfile.ZipFile(package) as archive:
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


def file_record(path: Path, *, root: Path) -> dict[str, object]:
    payload = path.read_bytes()
    return {
        "status": "downloaded",
        "source_filename": path.name,
        "local_name": path.name,
        "relative_path": str(path.relative_to(root)),
        "size": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "content_type": None,
        "archive_members": [],
    }


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
        path for path in extracted if normalize_filename(path.name) not in expected_keys
    ]
    return matched, unexpected


def materialize_expected_files(
    matched: dict[str, Path], *, output_dir: Path
) -> list[dict[str, object]]:
    files_dir = output_dir / "files"
    files_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for expected_name, source in sorted(matched.items()):
        target = files_dir / expected_name
        shutil.copy2(source, target)
        records.append(file_record(target, root=output_dir))
    return records


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
    args = parser.parse_args()

    config = load_config(args.config)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    errors: list[dict[str, str]] = []
    package: dict[str, object] | None = None
    extracted: list[Path] = []

    url = str(config["europe_pmc_supplementary_url"])
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
    materialized = materialize_expected_files(matched, output_dir=args.output_dir)
    missing = [name for name in expected if name not in matched]
    complete = not missing
    status = (
        "supplementary_files_acquired"
        if complete
        else "supplementary_acquisition_partial"
        if matched
        else "supplementary_acquisition_blocked"
    )
    inventory = {
        "schema_version": "1.0",
        "status": status,
        "acquisition_route": "europe_pmc_supplementary_files",
        "source_id": config["source_id"],
        "article_doi": config["article_doi"],
        "pmcid": config["pmcid"],
        "package": package,
        "n_candidates": len(extracted),
        "n_downloaded": len(materialized),
        "expected_supplementary_files": expected,
        "recovered_supplementary_files": sorted(matched),
        "missing_supplementary_files": missing,
        "files": materialized,
        "unexpected_package_files": [
            file_record(path, root=args.output_dir) for path in unexpected
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
    print(f"status: {status}")
    if not complete:
        raise RuntimeError(
            "Europe PMC supplementary recovery incomplete; see source_inventory.json"
        )


if __name__ == "__main__":
    main()
