#!/usr/bin/env python3
"""Probe lawful morphology source routes without changing evidence admission state.

This audit is intentionally discovery-only. It checks known catalogue and
repository pages, records delivery state, and extracts candidate full-text links
for later checksum locking. Repository-specific title/author search URLs and
public repository APIs are generated from registry metadata so the audit does
not stop at repository home pages or client-side search shells. A successful
HTTP response never by itself opens a numeric or provenance gate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from html import unescape
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "data/design/cross_archipelago_morphology_source_recovery.json"
DEFAULT_OUTPUT = ROOT / "artifacts/cross_archipelago_morphology_source_routes/summary.json"
USER_AGENT = "izu-core-source-route-audit/1.2 (+research reproducibility audit)"


def _is_candidate_url(url: str) -> bool:
    lower = url.lower()
    static_suffixes = (".css", ".js", ".json", ".ico", ".png", ".svg", ".woff", ".woff2")
    if lower.endswith(static_suffixes) or "/assets/" in lower:
        return False
    return any(
        token in lower
        for token in (
            "hdl.handle.net/",
            "dam-oclc.bac-lac.gc.ca/",
            "openaccess.wgtn.ac.nz/articles/",
            "openaccess.wgtn.ac.nz/ndownloader/files/",
            "/server/api/core/items/",
            "/server/api/core/bitstreams/",
            ".pdf",
        )
    ) or (
        ("tspace.library.utoronto.ca/" in lower or "utoronto.scholaris.ca/" in lower)
        and lower.rstrip("/") not in {
            "https://tspace.library.utoronto.ca",
            "https://utoronto.scholaris.ca",
        }
    )


def candidate_links(text: str, base_url: str) -> list[str]:
    """Extract plausible source/repository URLs from HTML or JSON text."""
    raw: set[str] = set()
    for href in re.findall(r"(?i)href\s*=\s*[\"']([^\"']+)[\"']", text):
        raw.add(urllib.parse.urljoin(base_url, unescape(href.strip())))
    for value in re.findall(r'(?i)[\"\'](?:href|url)[\"\']\s*:\s*[\"\']([^\"\']+)[\"\']', text):
        raw.add(urllib.parse.urljoin(base_url, unescape(value.strip()).replace("\\/", "/")))
    for value in re.findall(r"https?://[^\s\"'<>]+", text):
        raw.add(unescape(value.rstrip(",]}")))
    return sorted(url for url in raw if _is_candidate_url(url))


def _json_discovery_candidates(text: str, base_url: str) -> list[str]:
    """Extract DSpace item/handle candidates from a REST discovery response."""
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return []

    output: set[str] = set()

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            handle = value.get("handle")
            if isinstance(handle, str) and "/" in handle:
                output.add("https://hdl.handle.net/" + handle.lstrip("/"))
            item_id = value.get("uuid") or value.get("id")
            if isinstance(item_id, str) and re.fullmatch(r"[0-9a-fA-F-]{36}", item_id):
                output.add("https://utoronto.scholaris.ca/server/api/core/items/" + item_id)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
        elif isinstance(value, str):
            absolute = urllib.parse.urljoin(base_url, value)
            if _is_candidate_url(absolute):
                output.add(absolute)

    walk(payload)
    return sorted(output)


def probe(url: str, timeout: float = 20.0) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json, text/html, application/pdf;q=0.9, */*;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = response.read()
            final_url = response.geturl()
            content_type = response.headers.get("Content-Type", "")
            record: dict[str, Any] = {
                "url": url,
                "status": "delivered",
                "http_status": int(getattr(response, "status", 200)),
                "final_url": final_url,
                "content_type": content_type,
                "n_bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
                "is_pdf_bytes": data.startswith(b"%PDF-"),
                "candidate_links": [],
            }
            if not record["is_pdf_bytes"]:
                text = data.decode("utf-8", errors="replace")
                candidates = set(candidate_links(text, final_url))
                if "json" in content_type.lower() or text.lstrip().startswith(("{", "[")):
                    candidates.update(_json_discovery_candidates(text, final_url))
                record["candidate_links"] = sorted(candidates)
            return record
    except urllib.error.HTTPError as error:
        return {
            "url": url,
            "status": "http_error",
            "http_status": int(error.code),
            "error": str(error),
            "candidate_links": [],
        }
    except Exception as error:
        return {
            "url": url,
            "status": "delivery_error",
            "error_type": type(error).__name__,
            "error": str(error),
            "candidate_links": [],
        }


def repository_search_urls(source: dict[str, Any]) -> list[str]:
    """Generate narrow repository search/API URLs from source metadata."""
    urls: list[str] = []
    source_id = str(source.get("source_id") or "")

    if source_id == "hendriks_2019_flower_area":
        title = str(source.get("title") or "").strip()
        author = str(source.get("author") or "").strip()
        for query in (title, author, "Hendriks island rule plant traits"):
            if query:
                urls.append("https://openaccess.wgtn.ac.nz/search?q=" + urllib.parse.quote_plus(query))

    if source_id == "hetherington_rauth_johnson_2020_136_pairs":
        title = str(source.get("thesis_title") or "").strip()
        author = str(source.get("thesis_author") or "").strip()
        for query in (title, author, "Hetherington-Rauth floral traits island angiosperms"):
            if query:
                encoded_plus = urllib.parse.quote_plus(query)
                encoded = urllib.parse.quote(query, safe="")
                urls.append("https://utoronto.scholaris.ca/search?query=" + encoded_plus)
                urls.append("https://tspace.library.utoronto.ca/simple-search?query=" + encoded_plus)
                urls.append(
                    "https://utoronto.scholaris.ca/server/api/discover/search/objects?"
                    + "dsoType=item&size=20&query=" + encoded
                )

    return urls


def route_urls(source: dict[str, Any]) -> list[str]:
    urls: list[str] = []
    for route in source.get("known_routes", []):
        url = str(route.get("url") or "").strip()
        if url:
            urls.append(url)
    repository = source.get("institutional_repository") or {}
    base_url = str(repository.get("base_url") or "").strip()
    if base_url:
        urls.append(base_url)
    urls.extend(repository_search_urls(source))
    return list(dict.fromkeys(urls))


def build_report(registry: dict[str, Any], timeout: float = 20.0) -> dict[str, Any]:
    sources = []
    all_candidates: set[str] = set()
    for source in registry.get("sources", []):
        urls = route_urls(source)
        probes = [probe(url, timeout=timeout) for url in urls]
        candidates = sorted({link for item in probes for link in item.get("candidate_links", [])})
        all_candidates.update(candidates)
        sources.append(
            {
                "source_id": source.get("source_id"),
                "route_count": len(urls),
                "probes": probes,
                "candidate_full_text_or_repository_links": candidates,
                "admission_changed": False,
            }
        )
    return {
        "schema_version": "1.2",
        "status": "route_probe_complete",
        "sources": sources,
        "all_candidate_links": sorted(all_candidates),
        "claim_boundary": (
            "Route delivery, repository API/search hits, and candidate links are acquisition evidence only. "
            "No source becomes checksum-locked, numerically admitted, or formally meta-analytic until exact "
            "source bytes and the predeclared gates are verified."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--timeout", type=float, default=20.0)
    args = parser.parse_args()

    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    report = build_report(registry, timeout=args.timeout)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
