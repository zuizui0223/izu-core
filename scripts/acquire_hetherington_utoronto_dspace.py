#!/usr/bin/env python3
"""Recover the Hetherington-Rauth 2019 thesis through the public UofT DSpace API.

This script discovers the exact thesis item from source-registry metadata,
resolves its ORIGINAL bundle and PDF bitstream, downloads exact bytes, and writes
a source-lock record. Acquisition never creates a third-system numeric effect;
the source-native 136-pair table, trait definition, grouping and uncertainty must
still be verified separately.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "data/design/cross_archipelago_morphology_source_recovery.json"
DEFAULT_OUTPUT_DIR = ROOT / "artifacts/hetherington_2019/source_lock"
BASE = "https://utoronto.scholaris.ca/server/api"
USER_AGENT = "izu-core-hetherington-source-recovery/1.0 (+research reproducibility audit)"


def get_bytes(url: str, *, accept: str = "application/json", timeout: float = 30.0) -> tuple[bytes, str, str]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read(), response.geturl(), response.headers.get("Content-Type", "")


def get_json(url: str, timeout: float = 30.0) -> dict[str, Any]:
    data, _, _ = get_bytes(url, timeout=timeout)
    return json.loads(data.decode("utf-8"))


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def source_record(registry: dict[str, Any]) -> dict[str, Any]:
    matches = [
        source for source in registry.get("sources", [])
        if source.get("source_id") == "hetherington_rauth_johnson_2020_136_pairs"
    ]
    if len(matches) != 1:
        raise ValueError("expected exactly one 136-pair source-registry entry")
    return dict(matches[0])


def recursive_dicts(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from recursive_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from recursive_dicts(child)


def discover_item_candidates(payload: dict[str, Any]) -> list[dict[str, Any]]:
    candidates: dict[str, dict[str, Any]] = {}
    for item in recursive_dicts(payload):
        uuid = item.get("uuid") or item.get("id")
        name = item.get("name") or item.get("title")
        handle = item.get("handle")
        if isinstance(uuid, str) and re.fullmatch(r"[0-9a-fA-F-]{36}", uuid) and isinstance(name, str):
            candidates[uuid] = {"uuid": uuid, "name": name, "handle": handle}
    return list(candidates.values())


def select_exact_item(candidates: list[dict[str, Any]], expected_title: str) -> dict[str, Any]:
    expected = normalize(expected_title)
    exact = [item for item in candidates if normalize(str(item.get("name") or "")) == expected]
    if len(exact) == 1:
        return exact[0]
    # A narrowly normalized containment fallback tolerates repository-added thesis punctuation/subtitles.
    close = [
        item for item in candidates
        if expected in normalize(str(item.get("name") or ""))
        or normalize(str(item.get("name") or "")) in expected
    ]
    if len(close) == 1:
        return close[0]
    raise ValueError(f"could not uniquely resolve thesis item from {len(candidates)} candidates")


def discover_exact_item(source: dict[str, Any], timeout: float = 30.0) -> tuple[dict[str, Any], list[str]]:
    title = str(source["thesis_title"])
    author = str(source["thesis_author"])
    queries = [title, author, "Hetherington-Rauth floral traits island angiosperms"]
    attempted: list[str] = []
    pooled: dict[str, dict[str, Any]] = {}
    for query in queries:
        url = (
            BASE
            + "/discover/search/objects?dsoType=item&size=50&query="
            + urllib.parse.quote(query, safe="")
        )
        attempted.append(url)
        payload = get_json(url, timeout=timeout)
        for candidate in discover_item_candidates(payload):
            pooled[candidate["uuid"]] = candidate
    selected = select_exact_item(list(pooled.values()), title)
    item_url = BASE + "/core/items/" + selected["uuid"]
    attempted.append(item_url)
    details = get_json(item_url, timeout=timeout)
    observed_name = str(details.get("name") or selected.get("name") or "")
    if normalize(observed_name) != normalize(title):
        if normalize(title) not in normalize(observed_name) and normalize(observed_name) not in normalize(title):
            raise ValueError(f"resolved item title mismatch: {observed_name!r}")
    selected.update({"name": observed_name, "handle": details.get("handle") or selected.get("handle")})
    return selected, attempted


def object_candidates(payload: dict[str, Any], *, kind: str) -> list[dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for item in recursive_dicts(payload):
        uuid = item.get("uuid") or item.get("id")
        name = item.get("name")
        if not (isinstance(uuid, str) and re.fullmatch(r"[0-9a-fA-F-]{36}", uuid)):
            continue
        if not isinstance(name, str):
            continue
        if kind == "bundle" and item.get("bundleName") and not name:
            name = item.get("bundleName")
        output[uuid] = dict(item)
    return list(output.values())


def resolve_original_bundle(item_uuid: str, timeout: float = 30.0) -> tuple[dict[str, Any], str]:
    url = BASE + f"/core/items/{item_uuid}/bundles?size=100"
    payload = get_json(url, timeout=timeout)
    candidates = object_candidates(payload, kind="bundle")
    original = [bundle for bundle in candidates if str(bundle.get("name") or "").casefold() == "original"]
    if len(original) != 1:
        raise ValueError(f"expected one ORIGINAL bundle, found {len(original)}")
    return original[0], url


def resolve_pdf_bitstream(bundle_uuid: str, timeout: float = 30.0) -> tuple[dict[str, Any], str]:
    url = BASE + f"/core/bundles/{bundle_uuid}/bitstreams?size=100"
    payload = get_json(url, timeout=timeout)
    candidates = object_candidates(payload, kind="bitstream")
    pdfs = []
    for item in candidates:
        name = str(item.get("name") or "")
        mime = str(item.get("mimeType") or item.get("metadata", {}).get("dc.format") or "")
        if name.casefold().endswith(".pdf") or "pdf" in mime.casefold():
            pdfs.append(item)
    if len(pdfs) != 1:
        raise ValueError(f"expected one thesis PDF bitstream, found {len(pdfs)}")
    return pdfs[0], url


def download_bitstream(bitstream_uuid: str, timeout: float = 60.0) -> tuple[bytes, str]:
    candidates = [
        BASE + f"/core/bitstreams/{bitstream_uuid}/content",
        "https://utoronto.scholaris.ca/server/api/core/bitstreams/" + bitstream_uuid + "/content",
    ]
    error: Exception | None = None
    for url in dict.fromkeys(candidates):
        try:
            data, final_url, _ = get_bytes(url, accept="application/pdf,*/*;q=0.8", timeout=timeout)
            return data, final_url
        except Exception as caught:  # preserve final error only after lawful public routes are exhausted
            error = caught
    assert error is not None
    raise error


def build_lock(source: dict[str, Any], item: dict[str, Any], bundle: dict[str, Any], bitstream: dict[str, Any], data: bytes, final_url: str, attempted: list[str]) -> dict[str, Any]:
    if not data.startswith(b"%PDF-"):
        raise ValueError("recovered UofT bitstream is not PDF bytes")
    handle = str(item.get("handle") or "")
    return {
        "schema_version": "1.0",
        "status": "utoronto_thesis_pdf_bytes_recovered_and_checksum_locked",
        "source_id": source.get("source_id"),
        "thesis_title": source.get("thesis_title"),
        "item_uuid": item["uuid"],
        "item_handle": handle or None,
        "handle_url": ("https://hdl.handle.net/" + handle) if handle else None,
        "original_bundle_uuid": bundle["uuid"],
        "pdf_bitstream_uuid": bitstream["uuid"],
        "pdf_name": bitstream.get("name"),
        "final_download_url": final_url,
        "n_bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "md5": hashlib.md5(data).hexdigest(),  # nosec B324 - integrity only
        "attempted_public_api_routes": attempted,
        "source_native_136_pair_table_verified": False,
        "third_response_shape_admitted": False,
        "formal_cross_system_fit_opened": False,
        "claim_boundary": (
            "Exact thesis bytes establish provenance only. The 136-pair source table, trait definitions, "
            "pair/island grouping and usable uncertainty must still be verified before any third-system effect is created."
        ),
    }


def write_failure(path: Path, error: Exception) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "1.0",
        "status": "utoronto_thesis_acquisition_blocked_this_run",
        "error_type": type(error).__name__,
        "error": str(error),
        "biological_result_changed": False,
        "third_response_shape_admitted": False,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()

    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    source = source_record(registry)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    attempted: list[str] = []
    try:
        item, attempted = discover_exact_item(source, timeout=args.timeout)
        bundle, bundle_url = resolve_original_bundle(item["uuid"], timeout=args.timeout)
        attempted.append(bundle_url)
        bitstream, bitstream_url = resolve_pdf_bitstream(bundle["uuid"], timeout=args.timeout)
        attempted.append(bitstream_url)
        data, final_url = download_bitstream(bitstream["uuid"], timeout=max(args.timeout, 60.0))
        attempted.append(final_url)
        lock = build_lock(source, item, bundle, bitstream, data, final_url, attempted)
        pdf_path = args.output_dir / "hetherington_rauth_2019_thesis.pdf"
        lock_path = args.output_dir / "source_lock.json"
        pdf_path.write_bytes(data)
        lock_path.write_text(json.dumps(lock, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(lock_path)
    except Exception as error:
        write_failure(args.output_dir / "acquisition_state.json", error)
        raise


if __name__ == "__main__":
    main()
