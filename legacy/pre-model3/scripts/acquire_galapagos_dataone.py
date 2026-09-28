#!/usr/bin/env python3
"""Attempt DOI-locked Galápagos source recovery through DataONE.

Dryad's public metadata API exposes the Galápagos package, but file transport
can return HTTP 403 in GitHub Actions. This script uses DataONE only as an
alternate transport/index route for objects whose metadata explicitly contains
the same Dryad DOI. It never searches by title alone and never treats an empty
or failed result as a biological zero.

The output directory mirrors the generic Dryad acquisition layout so the
existing Galápagos schema and network-analysis scripts can consume a recovered
ZIP without source-specific branching.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import re
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


USER_AGENT = "izu-core-source-audit/1.1 (+https://github.com/zuizui0223/izu-core)"
DEFAULT_CN_BASES = (
    "https://cn.dataone.org/cn/v2",
    "https://cn-secondary.dataone.org/cn/v2",
)
QUERY_FIELDS = (
    "id,seriesId,title,fileName,formatId,formatType,size,checksum,"
    "checksumAlgorithm,resourceMap,documents,isDocumentedBy,obsoletes,"
    "obsoletedBy,dateUploaded,datePublished,memberNode,datasource"
)
METADATA_HINTS = (
    "eml",
    "metadata",
    "datacite",
    "iso191",
    "fgdc",
    "resource-map",
    "resource_map",
    "ore",
    "rdf",
    "science-metadata",
    "text/xml",
    "application/xml",
)
DATA_SUFFIXES = (
    ".zip",
    ".csv",
    ".tsv",
    ".txt",
    ".xlsx",
    ".xlsm",
    ".xls",
    ".json",
    ".rdata",
    ".rds",
)


def canonical_doi(value: object) -> str:
    text = str(value or "").strip().casefold()
    text = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", text)
    text = re.sub(r"^doi:\s*", "", text)
    return text.rstrip("/ ")


def doi_variants(value: object) -> tuple[str, ...]:
    doi = canonical_doi(value)
    if not doi:
        return ()
    return doi, f"doi:{doi}", f"https://doi.org/{doi}"


def solr_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def query_urls(base: str, doi: str, *, rows: int = 250) -> tuple[str, ...]:
    bare, prefixed, url_form = doi_variants(doi)
    exact = " OR ".join(
        (
            f'id:"{solr_escape(bare)}"',
            f'id:"{solr_escape(prefixed)}"',
            f'seriesId:"{solr_escape(bare)}"',
            f'seriesId:"{solr_escape(prefixed)}"',
            f'resourceMap:"{solr_escape(bare)}"',
            f'"{solr_escape(url_form)}"',
        )
    )
    broad = f'"{solr_escape(bare)}" OR "{solr_escape(prefixed)}"'
    urls = []
    for query in (exact, broad):
        params = urllib.parse.urlencode(
            {"q": query, "fl": QUERY_FIELDS, "rows": rows, "wt": "json"}
        )
        urls.append(f"{base.rstrip('/')}/query/solr/?{params}")
    return tuple(urls)


def related_query_urls(base: str, identifier: str, *, rows: int = 500) -> tuple[str, ...]:
    escaped = solr_escape(identifier)
    exact = " OR ".join(
        (
            f'id:"{escaped}"',
            f'seriesId:"{escaped}"',
            f'resourceMap:"{escaped}"',
            f'documents:"{escaped}"',
            f'isDocumentedBy:"{escaped}"',
            f'obsoletes:"{escaped}"',
            f'obsoletedBy:"{escaped}"',
        )
    )
    broad = f'"{escaped}"'
    urls = []
    for query in (exact, broad):
        params = urllib.parse.urlencode(
            {"q": query, "fl": QUERY_FIELDS, "rows": rows, "wt": "json"}
        )
        urls.append(f"{base.rstrip('/')}/query/solr/?{params}")
    return tuple(urls)


def make_opener() -> urllib.request.OpenerDirector:
    return urllib.request.build_opener(urllib.request.HTTPRedirectHandler())


def request_bytes(
    opener: urllib.request.OpenerDirector,
    url: str,
    *,
    accept: str = "application/octet-stream, */*;q=0.8",
    timeout: float = 120.0,
) -> tuple[bytes, dict[str, str], str]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": accept,
            "Cache-Control": "no-cache",
        },
    )
    try:
        with opener.open(request, timeout=timeout) as response:
            payload = response.read()
            headers = {key.casefold(): value for key, value in response.headers.items()}
            return payload, headers, response.geturl()
    except urllib.error.HTTPError as error:
        try:
            body = error.read(500).decode("utf-8", errors="replace")
        except Exception:
            body = ""
        body = re.sub(r"\s+", " ", body).strip()
        raise RuntimeError(
            f"HTTP {error.code} {error.reason}; body={body!r}"
        ) from error


def request_json(opener: urllib.request.OpenerDirector, url: str) -> Any:
    payload, _, _ = request_bytes(opener, url, accept="application/json")
    return json.loads(payload.decode("utf-8"))


def solr_docs(payload: object) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        return []
    response = payload.get("response")
    if not isinstance(response, dict):
        return []
    docs = response.get("docs")
    if not isinstance(docs, list):
        return []
    return [doc for doc in docs if isinstance(doc, dict)]


def walk_strings(value: object) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, Mapping):
        for child in value.values():
            yield from walk_strings(child)
    elif isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray, str)):
        for child in value:
            yield from walk_strings(child)


def document_matches_doi(document: Mapping[str, object], doi: str) -> bool:
    target = canonical_doi(doi)
    for value in walk_strings(document):
        normalized = canonical_doi(value)
        if normalized == target or target in value.casefold():
            return True
    return False


def first_string(value: object) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray, str)):
        for item in value:
            if isinstance(item, str) and item.strip():
                return item.strip()
    return ""


def document_id(document: Mapping[str, object]) -> str:
    return first_string(document.get("id"))


def related_identifiers(document: Mapping[str, object]) -> set[str]:
    output: set[str] = set()
    for key in (
        "id",
        "seriesId",
        "resourceMap",
        "documents",
        "isDocumentedBy",
        "obsoletes",
        "obsoletedBy",
    ):
        value = document.get(key)
        if isinstance(value, str) and value.strip():
            output.add(value.strip())
        elif isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray, str)):
            output.update(str(item).strip() for item in value if str(item).strip())
    return output


def deduplicate_documents(documents: Iterable[Mapping[str, object]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    seen: set[str] = set()
    for document in documents:
        identifier = document_id(document)
        key = identifier or json.dumps(document, sort_keys=True, default=str)
        if key in seen:
            continue
        seen.add(key)
        output.append(dict(document))
    return output


def format_type(document: Mapping[str, object]) -> str:
    return first_string(document.get("formatType")).strip().casefold()


def format_id(document: Mapping[str, object]) -> str:
    return first_string(document.get("formatId")).strip().casefold()


def document_size(document: Mapping[str, object]) -> int | None:
    raw = document.get("size")
    if isinstance(raw, Sequence) and not isinstance(raw, (bytes, bytearray, str)):
        raw = next(iter(raw), None)
    try:
        number = int(float(raw))
    except (TypeError, ValueError):
        return None
    return number if number >= 0 else None


def document_filename(document: Mapping[str, object]) -> str:
    for key in ("fileName", "title", "id"):
        value = first_string(document.get(key))
        if not value:
            continue
        name = Path(urllib.parse.unquote(value)).name
        if name:
            return name
    return "dataone_object"


def likely_data_document(document: Mapping[str, object]) -> bool:
    identifier = document_id(document)
    if not identifier:
        return False
    kind = format_type(document)
    fmt = format_id(document)
    filename = document_filename(document).casefold()
    if kind == "data":
        return True
    if kind in {"metadata", "resource"}:
        return False
    if any(hint in fmt for hint in METADATA_HINTS):
        return False
    if any(filename.endswith(suffix) for suffix in DATA_SUFFIXES):
        return True
    size = document_size(document)
    return bool(size and size > 0 and fmt and not any(hint in fmt for hint in METADATA_HINTS))


def safe_name(value: object) -> str:
    name = Path(urllib.parse.unquote(str(value or ""))).name
    name = re.sub(r"[^A-Za-z0-9._+() -]+", "_", name).strip(" ._")
    return name or "dataone_object"


def looks_html_or_error_xml(payload: bytes) -> bool:
    prefix = payload[:1000].lstrip().lower()
    if prefix.startswith(b"<!doctype html") or prefix.startswith(b"<html"):
        return True
    return (
        prefix.startswith(b"<?xml")
        and any(marker in prefix for marker in (b"<error", b"<exception", b"notfound"))
    )


def valid_payload(filename: str, payload: bytes) -> tuple[bool, str]:
    if not payload:
        return False, "empty_response"
    if looks_html_or_error_xml(payload):
        return False, "html_or_error_xml_response"
    suffix = Path(filename).suffix.casefold()
    if suffix == ".zip":
        if not zipfile.is_zipfile(io.BytesIO(payload)):
            return False, "invalid_zip"
    elif suffix in {".xlsx", ".xlsm"}:
        try:
            with zipfile.ZipFile(io.BytesIO(payload)) as archive:
                names = archive.namelist()
        except zipfile.BadZipFile:
            return False, "invalid_xlsx_zip"
        if "[Content_Types].xml" not in names or not any(name.startswith("xl/") for name in names):
            return False, "missing_xlsx_structure"
    return True, "accepted"


def safe_extract_zip(path: Path, destination: Path) -> list[str]:
    destination.mkdir(parents=True, exist_ok=True)
    members: list[str] = []
    with zipfile.ZipFile(path) as archive:
        for member in archive.infolist():
            member_path = Path(member.filename)
            if member_path.is_absolute() or ".." in member_path.parts:
                continue
            members.append(member.filename)
            if member.is_dir():
                continue
            target = destination / member_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(member))
    return members


def preview_delimited(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    delimiter = "\t" if path.suffix.casefold() == ".tsv" else ","
    try:
        delimiter = csv.Sniffer().sniff(text[:8192], delimiters=",\t;").delimiter
    except csv.Error:
        pass
    preview: list[list[str]] = []
    reader = csv.reader(io.StringIO(text), delimiter=delimiter)
    for index, row in enumerate(reader):
        preview.append(row[:30])
        if index >= 5:
            break
    return {"kind": "delimited", "delimiter": delimiter, "preview": preview}


def preview_file(path: Path, extraction_root: Path) -> dict[str, object]:
    suffix = path.suffix.casefold()
    if suffix == ".zip" or zipfile.is_zipfile(path):
        return {
            "kind": "zip",
            "archive_members": safe_extract_zip(path, extraction_root / path.stem),
        }
    if suffix in {".csv", ".tsv", ".txt"}:
        return preview_delimited(path)
    return {"kind": "other"}


def query_documents(
    opener: urllib.request.OpenerDirector,
    urls: Iterable[str],
    errors: list[dict[str, str]],
    stage: str,
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for url in urls:
        try:
            output.extend(solr_docs(request_json(opener, url)))
        except Exception as error:
            errors.append({"stage": stage, "url": url, "error": repr(error)})
    return deduplicate_documents(output)


def acquire(
    *,
    config: Mapping[str, object],
    output_dir: Path,
    cn_bases: Sequence[str] = DEFAULT_CN_BASES,
) -> dict[str, object]:
    doi = canonical_doi(config.get("dataset_doi"))
    if not doi:
        raise ValueError("config must provide dataset_doi")
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = output_dir / "files"
    extraction_root = output_dir / "extracted"
    raw_dir.mkdir(parents=True, exist_ok=True)
    opener = make_opener()
    errors: list[dict[str, str]] = []

    initial: list[dict[str, Any]] = []
    for base in cn_bases:
        initial.extend(query_documents(opener, query_urls(base, doi), errors, "doi_query"))
    initial = deduplicate_documents(initial)
    doi_locked = [document for document in initial if document_matches_doi(document, doi)]

    related_ids: set[str] = set()
    for document in doi_locked:
        related_ids.update(related_identifiers(document))
    expanded: list[dict[str, Any]] = list(doi_locked)
    for identifier in sorted(related_ids):
        for base in cn_bases:
            expanded.extend(
                query_documents(
                    opener,
                    related_query_urls(base, identifier),
                    errors,
                    "related_object_query",
                )
            )
    expanded = deduplicate_documents(expanded)

    candidates = [document for document in expanded if likely_data_document(document)]
    candidates.sort(
        key=lambda document: (
            not document_filename(document).casefold().endswith(".zip"),
            -(document_size(document) or 0),
            document_filename(document).casefold(),
        )
    )

    inventory: list[dict[str, object]] = []
    used_names: set[str] = set()
    for document in candidates:
        identifier = document_id(document)
        filename = safe_name(document_filename(document))
        stem = Path(filename).stem
        suffix = Path(filename).suffix
        counter = 2
        while filename in used_names:
            filename = f"{stem}_{counter}{suffix}"
            counter += 1
        used_names.add(filename)
        attempts: list[dict[str, object]] = []
        payload: bytes | None = None
        successful_url: str | None = None
        successful_headers: dict[str, str] = {}
        for base in cn_bases:
            url = f"{base.rstrip('/')}/object/{urllib.parse.quote(identifier, safe='')}"
            try:
                candidate, headers, resolved_url = request_bytes(opener, url)
                accepted, reason = valid_payload(filename, candidate)
                attempts.append(
                    {
                        "url": url,
                        "resolved_url_without_query": urllib.parse.urlunsplit(
                            (*urllib.parse.urlsplit(resolved_url)[:3], "", "")
                        ),
                        "status": reason,
                        "size": len(candidate),
                        "content_type": headers.get("content-type"),
                    }
                )
                if accepted:
                    payload = candidate
                    successful_url = resolved_url
                    successful_headers = headers
                    break
            except Exception as error:
                attempts.append({"url": url, "status": "request_failed", "error": repr(error)})
        record: dict[str, object] = {
            "dataone_id": identifier,
            "source_filename": document_filename(document),
            "source_size": document_size(document),
            "source_checksum": document.get("checksum"),
            "source_checksum_algorithm": document.get("checksumAlgorithm"),
            "format_id": document.get("formatId"),
            "format_type": document.get("formatType"),
            "download_attempts": attempts,
        }
        if payload is None or successful_url is None:
            record["status"] = "download_failed"
            inventory.append(record)
            continue
        destination = raw_dir / filename
        destination.write_bytes(payload)
        record.update(
            {
                "status": "downloaded",
                "local_name": filename,
                "size_downloaded": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "successful_download_url_without_query": urllib.parse.urlunsplit(
                    (*urllib.parse.urlsplit(successful_url)[:3], "", "")
                ),
                "content_type": successful_headers.get("content-type"),
                "preview": preview_file(destination, extraction_root),
            }
        )
        inventory.append(record)

    downloaded = sum(record.get("status") == "downloaded" for record in inventory)
    if downloaded:
        status = "acquired_via_dataone"
    elif doi_locked and candidates:
        status = "dataone_objects_found_but_download_failed"
    elif doi_locked:
        status = "dataone_doi_record_found_metadata_only"
    elif initial:
        status = "dataone_search_returned_unlocked_records"
    else:
        status = "dataone_doi_not_indexed_or_unreachable"

    summary: dict[str, object] = {
        "schema_version": "1.0",
        "status": status,
        "acquisition_route": "dataone_cn_v2_doi_locked",
        "source_id": config.get("source_id"),
        "dataset_doi": doi,
        "cn_bases": list(cn_bases),
        "n_initial_documents": len(initial),
        "n_doi_locked_documents": len(doi_locked),
        "n_expanded_documents": len(expanded),
        "n_data_candidates": len(candidates),
        "n_source_files": len(candidates),
        "n_downloaded": downloaded,
        "doi_locked_documents": doi_locked,
        "expanded_documents": expanded,
        "files": inventory,
        "errors": errors,
        "expected_source_components": config.get("expected_source_components"),
        "next_gate": (
            "If no valid object is recovered, obtain the same Dryad package through a lawful repository, author, institutional or user-supplied route. Do not reconstruct raw networks from article summaries."
        ),
        "claim_boundary": config.get("claim_boundary"),
    }
    (output_dir / "source_inventory.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, default=str) + "\n",
        encoding="utf-8",
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/galapagos_dryad_source.json"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/galapagos_dryad"),
    )
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    summary = acquire(config=config, output_dir=args.output_dir)
    print(f"DataONE status: {summary['status']}")
    print(f"files downloaded: {summary['n_downloaded']}/{summary['n_source_files']}")
    if not summary["n_downloaded"]:
        raise RuntimeError("DataONE recovery did not yield a valid data object; see source_inventory.json")


if __name__ == "__main__":
    main()
