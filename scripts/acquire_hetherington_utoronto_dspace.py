#!/usr/bin/env python3
"""Recover the Hetherington-Rauth 2019 thesis through the public UofT DSpace API.

Discover the exact thesis item, resolve its ORIGINAL bundle, select the full
thesis PDF while explicitly excluding an expanded-abstract PDF, download exact
bytes, and write a source-lock record. Acquisition alone never creates a
third-system effect.
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
    matches = [s for s in registry.get("sources", []) if s.get("source_id") == "hetherington_rauth_johnson_2020_136_pairs"]
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
        if isinstance(uuid, str) and re.fullmatch(r"[0-9a-fA-F-]{36}", uuid) and isinstance(name, str):
            candidates[uuid] = {"uuid": uuid, "name": name, "handle": item.get("handle")}
    return list(candidates.values())


def select_exact_item(candidates: list[dict[str, Any]], expected_title: str) -> dict[str, Any]:
    expected = normalize(expected_title)
    exact = [item for item in candidates if normalize(str(item.get("name") or "")) == expected]
    if len(exact) == 1:
        return exact[0]
    close = [item for item in candidates if expected in normalize(str(item.get("name") or "")) or normalize(str(item.get("name") or "")) in expected]
    if len(close) == 1:
        return close[0]
    raise ValueError(f"could not uniquely resolve thesis item from {len(candidates)} candidates")


def discover_exact_item(source: dict[str, Any], timeout: float = 30.0) -> tuple[dict[str, Any], list[str]]:
    title = str(source["thesis_title"])
    queries = [title, str(source["thesis_author"]), "Hetherington-Rauth floral traits island angiosperms"]
    attempted: list[str] = []
    pooled: dict[str, dict[str, Any]] = {}
    for query in queries:
        url = BASE + "/discover/search/objects?dsoType=item&size=50&query=" + urllib.parse.quote(query, safe="")
        attempted.append(url)
        for candidate in discover_item_candidates(get_json(url, timeout=timeout)):
            pooled[candidate["uuid"]] = candidate
    selected = select_exact_item(list(pooled.values()), title)
    item_url = BASE + "/core/items/" + selected["uuid"]
    attempted.append(item_url)
    details = get_json(item_url, timeout=timeout)
    observed = str(details.get("name") or selected.get("name") or "")
    if normalize(observed) != normalize(title) and normalize(title) not in normalize(observed) and normalize(observed) not in normalize(title):
        raise ValueError(f"resolved item title mismatch: {observed!r}")
    selected.update({"name": observed, "handle": details.get("handle") or selected.get("handle")})
    return selected, attempted


def object_candidates(payload: dict[str, Any]) -> list[dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for item in recursive_dicts(payload):
        uuid = item.get("uuid") or item.get("id")
        name = item.get("name")
        if isinstance(uuid, str) and re.fullmatch(r"[0-9a-fA-F-]{36}", uuid) and isinstance(name, str):
            output[uuid] = dict(item)
    return list(output.values())


def resolve_original_bundle(item_uuid: str, timeout: float = 30.0) -> tuple[dict[str, Any], str]:
    url = BASE + f"/core/items/{item_uuid}/bundles?size=100"
    original = [b for b in object_candidates(get_json(url, timeout=timeout)) if str(b.get("name") or "").casefold() == "original"]
    if len(original) != 1:
        raise ValueError(f"expected one ORIGINAL bundle, found {len(original)}")
    return original[0], url


def pdf_candidate_summary(item: dict[str, Any]) -> dict[str, Any]:
    return {key: item.get(key) for key in ("uuid", "name", "mimeType", "sizeBytes", "sequenceId", "description")}


def select_full_thesis_pdf(pdfs: list[dict[str, Any]]) -> dict[str, Any]:
    """Select only an explicit full-thesis filename; never infer from size alone."""
    non_abstract = [item for item in pdfs if "expandedabstract" not in normalize(str(item.get("name") or "")).replace(" ", "")]
    exact = [
        item for item in non_abstract
        if re.search(r"_msc_thesis\.pdf$", str(item.get("name") or ""), flags=re.IGNORECASE)
    ]
    if len(exact) == 1:
        return exact[0]
    if len(non_abstract) == 1 and str(non_abstract[0].get("name") or "").casefold().endswith(".pdf"):
        return non_abstract[0]
    raise ValueError("could not uniquely distinguish full thesis PDF; candidates=" + json.dumps([pdf_candidate_summary(i) for i in pdfs], sort_keys=True))


def resolve_pdf_bitstream(bundle_uuid: str, timeout: float = 30.0) -> tuple[dict[str, Any], str]:
    url = BASE + f"/core/bundles/{bundle_uuid}/bitstreams?size=100"
    candidates = object_candidates(get_json(url, timeout=timeout))
    pdfs = []
    for item in candidates:
        name = str(item.get("name") or "")
        mime = str(item.get("mimeType") or item.get("metadata", {}).get("dc.format") or "")
        if name.casefold().endswith(".pdf") or "pdf" in mime.casefold():
            pdfs.append(item)
    if not pdfs:
        raise ValueError("no PDF bitstream found in ORIGINAL bundle")
    return select_full_thesis_pdf(pdfs), url


def download_bitstream(bitstream_uuid: str, timeout: float = 60.0) -> tuple[bytes, str]:
    urls = [BASE + f"/core/bitstreams/{bitstream_uuid}/content"]
    error: Exception | None = None
    for url in urls:
        try:
            data, final_url, _ = get_bytes(url, accept="application/pdf,*/*;q=0.8", timeout=timeout)
            return data, final_url
        except Exception as caught:
            error = caught
    assert error is not None
    raise error


def build_lock(source: dict[str, Any], item: dict[str, Any], bundle: dict[str, Any], bitstream: dict[str, Any], data: bytes, final_url: str, attempted: list[str]) -> dict[str, Any]:
    if not data.startswith(b"%PDF-"):
        raise ValueError("recovered UofT bitstream is not PDF bytes")
    handle = str(item.get("handle") or "")
    return {
        "schema_version": "1.1",
        "status": "utoronto_thesis_pdf_bytes_recovered_and_checksum_locked",
        "source_id": source.get("source_id"),
        "thesis_title": source.get("thesis_title"),
        "item_uuid": item["uuid"],
        "item_handle": handle or None,
        "handle_url": ("https://hdl.handle.net/" + handle) if handle else None,
        "original_bundle_uuid": bundle["uuid"],
        "pdf_bitstream_uuid": bitstream["uuid"],
        "pdf_name": bitstream.get("name"),
        "pdf_sequence_id": bitstream.get("sequenceId"),
        "repository_reported_size_bytes": bitstream.get("sizeBytes"),
        "final_download_url": final_url,
        "n_bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "md5": hashlib.md5(data).hexdigest(),
        "attempted_public_api_routes": attempted,
        "source_native_136_pair_table_verified": False,
        "third_response_shape_admitted": False,
        "formal_cross_system_fit_opened": False,
        "claim_boundary": "Exact thesis bytes establish provenance only. The source-native 136-pair table, trait definitions, grouping and usable uncertainty must still be verified before any third-system effect is created."
    }


def write_failure(path: Path, error: Exception) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"schema_version": "1.1", "status": "utoronto_thesis_acquisition_blocked_this_run", "error_type": type(error).__name__, "error": str(error), "biological_result_changed": False, "third_response_shape_admitted": False}, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()
    source = source_record(json.loads(args.registry.read_text(encoding="utf-8")))
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
        (args.output_dir / "hetherington_rauth_2019_thesis.pdf").write_bytes(data)
        lock_path = args.output_dir / "source_lock.json"
        lock_path.write_text(json.dumps(lock, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(lock_path)
    except Exception as error:
        write_failure(args.output_dir / "acquisition_state.json", error)
        raise


if __name__ == "__main__":
    main()
