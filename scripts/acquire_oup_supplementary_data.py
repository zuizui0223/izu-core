#!/usr/bin/env python3
"""Discover and acquire supplementary data from an Oxford Academic article.

The script follows only public article/supplement links, records provenance and
checksums, and preserves a diagnostic when publisher delivery blocks automated
retrieval. It does not reconstruct numeric results from an abstract or plot.
"""
from __future__ import annotations

import argparse
import hashlib
import html.parser
import io
import json
import re
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path
from typing import Iterable, Mapping


USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 "
    "izu-core-source-audit/1.0"
)
DATA_EXTENSIONS = {".csv", ".tsv", ".xlsx", ".xls", ".xlsm", ".zip", ".doc", ".docx", ".txt"}
LINK_HINTS = ("supp", "supporting", "additional", "data", "media", "appendix", "table_s", "figshare")


class LinkParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.casefold() != "a":
            return
        values = {key.casefold(): value for key, value in attrs}
        self._href = values.get("href")
        self._text = []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() == "a" and self._href is not None:
            self.links.append((self._href, " ".join(self._text).strip()))
            self._href = None
            self._text = []


def request(
    opener: urllib.request.OpenerDirector,
    url: str,
    *,
    accept: str,
    referer: str | None = None,
) -> tuple[bytes, str, Mapping[str, str]]:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": accept,
        "Accept-Language": "en-US,en;q=0.8",
        "Cache-Control": "no-cache",
    }
    if referer:
        headers["Referer"] = referer
    req = urllib.request.Request(url, headers=headers)
    try:
        with opener.open(req, timeout=120) as response:
            return response.read(), response.geturl(), dict(response.headers.items())
    except urllib.error.HTTPError as error:
        try:
            body = error.read(500).decode("utf-8", errors="replace")
        except Exception:
            body = ""
        body = re.sub(r"\s+", " ", body).strip()
        raise RuntimeError(f"HTTP {error.code} {error.reason}; body={body!r}") from error


def parse_links(base_url: str, payload: bytes) -> list[dict[str, str]]:
    parser = LinkParser()
    parser.feed(payload.decode("utf-8", errors="replace"))
    output = []
    for href, text in parser.links:
        absolute = urllib.parse.urljoin(base_url, href)
        output.append({"url": absolute, "text": re.sub(r"\s+", " ", text).strip()})
    return output


def is_candidate_link(url: str, text: str = "") -> bool:
    path = urllib.parse.urlsplit(url).path.casefold()
    suffix = Path(path).suffix
    haystack = f"{url} {text}".casefold()
    if suffix in DATA_EXTENSIONS:
        return True
    return any(hint in haystack for hint in LINK_HINTS)


def content_type(headers: Mapping[str, str]) -> str:
    for key, value in headers.items():
        if key.casefold() == "content-type":
            return value.split(";", 1)[0].strip().casefold()
    return ""


def looks_html(payload: bytes, headers: Mapping[str, str]) -> bool:
    if content_type(headers) in {"text/html", "application/xhtml+xml"}:
        return True
    prefix = payload[:500].lstrip().casefold()
    return prefix.startswith(b"<!doctype html") or prefix.startswith(b"<html")


def content_disposition_filename(headers: Mapping[str, str]) -> str | None:
    value = next((value for key, value in headers.items() if key.casefold() == "content-disposition"), "")
    extended = re.search(r"filename\*=UTF-8''([^;]+)", value, flags=re.IGNORECASE)
    if extended:
        return urllib.parse.unquote(extended.group(1)).strip('"')
    simple = re.search(r"filename=\"?([^\";]+)", value, flags=re.IGNORECASE)
    return simple.group(1).strip() if simple else None


def safe_filename(url: str, headers: Mapping[str, str], index: int) -> str:
    candidate = content_disposition_filename(headers) or Path(urllib.parse.urlsplit(url).path).name
    candidate = urllib.parse.unquote(candidate)
    candidate = re.sub(r"[^A-Za-z0-9._+() -]+", "_", candidate).strip(" ._")
    if not candidate or Path(candidate).suffix.casefold() not in DATA_EXTENSIONS:
        extension_by_type = {
            "application/zip": ".zip",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
            "text/csv": ".csv",
            "text/tab-separated-values": ".tsv",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
        }
        candidate = f"supplement_{index}{extension_by_type.get(content_type(headers), '')}"
    return candidate


def valid_data_payload(filename: str, payload: bytes, headers: Mapping[str, str]) -> tuple[bool, str]:
    if not payload:
        return False, "empty"
    if looks_html(payload, headers):
        return False, "html"
    suffix = Path(filename).suffix.casefold()
    if suffix in {".xlsx", ".xlsm", ".docx"}:
        if not zipfile.is_zipfile(io.BytesIO(payload)):
            return False, "invalid_office_zip"
    elif suffix == ".zip" and not zipfile.is_zipfile(io.BytesIO(payload)):
        return False, "invalid_zip"
    return True, "accepted"


def safe_extract_zip(path: Path, destination: Path) -> list[str]:
    destination.mkdir(parents=True, exist_ok=True)
    members = []
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


def discover_candidates(
    opener: urllib.request.OpenerDirector,
    landing_url: str,
    errors: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, object]]]:
    seeds = [
        landing_url,
        f"{landing_url.rstrip('/')}/supplementary-data",
        f"{landing_url}?login=false",
    ]
    candidates: list[dict[str, str]] = []
    pages: list[dict[str, object]] = []
    visited: set[str] = set()
    queue = list(seeds)
    while queue and len(visited) < 12:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)
        try:
            payload, final_url, headers = request(
                opener,
                url,
                accept="text/html,application/xhtml+xml,application/json;q=0.8,*/*;q=0.5",
                referer=landing_url,
            )
        except Exception as error:
            errors.append({"stage": "discovery_page", "url": url, "error": repr(error)})
            continue
        page_links = parse_links(final_url, payload) if looks_html(payload, headers) else []
        pages.append(
            {
                "requested_url": url,
                "final_url": final_url,
                "content_type": content_type(headers),
                "size": len(payload),
                "n_links": len(page_links),
            }
        )
        for link in page_links:
            if not is_candidate_link(link["url"], link["text"]):
                continue
            if link not in candidates:
                candidates.append(link)
            suffix = Path(urllib.parse.urlsplit(link["url"]).path).suffix.casefold()
            if suffix not in DATA_EXTENSIONS and link["url"] not in visited and len(queue) < 20:
                queue.append(link["url"])
    return candidates, pages


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = args.output_dir / "files"
    extract_dir = args.output_dir / "extracted"
    raw_dir.mkdir(parents=True, exist_ok=True)
    opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler())
    errors: list[dict[str, str]] = []

    crossref = {}
    try:
        payload, _, _ = request(opener, str(config["crossref_url"]), accept="application/json")
        crossref = json.loads(payload.decode("utf-8"))
    except Exception as error:
        errors.append({"stage": "crossref", "url": str(config["crossref_url"]), "error": repr(error)})

    candidates, discovery_pages = discover_candidates(opener, str(config["landing_page_url"]), errors)
    inventory = []
    seen_sha: set[str] = set()
    used_names: set[str] = set()
    for index, candidate in enumerate(candidates, start=1):
        url = candidate["url"]
        try:
            payload, final_url, headers = request(
                opener,
                url,
                accept=(
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,"
                    "application/zip,text/csv,application/octet-stream;q=0.9,*/*;q=0.5"
                ),
                referer=str(config["landing_page_url"]),
            )
        except Exception as error:
            inventory.append({**candidate, "status": "download_failed", "error": repr(error)})
            continue
        if looks_html(payload, headers):
            child_links = parse_links(final_url, payload)
            inventory.append(
                {
                    **candidate,
                    "status": "supplement_landing_page",
                    "final_url": final_url,
                    "content_type": content_type(headers),
                    "n_child_links": len(child_links),
                }
            )
            for child in child_links:
                if is_candidate_link(child["url"], child["text"]) and child not in candidates:
                    candidates.append(child)
            continue
        filename = safe_filename(final_url, headers, index)
        accepted, reason = valid_data_payload(filename, payload, headers)
        if not accepted:
            inventory.append(
                {
                    **candidate,
                    "status": reason,
                    "final_url": final_url,
                    "content_type": content_type(headers),
                    "size": len(payload),
                }
            )
            continue
        sha256 = hashlib.sha256(payload).hexdigest()
        if sha256 in seen_sha:
            inventory.append({**candidate, "status": "duplicate_payload", "sha256": sha256})
            continue
        seen_sha.add(sha256)
        stem = Path(filename).stem
        suffix = Path(filename).suffix
        local_name = filename
        counter = 2
        while local_name in used_names:
            local_name = f"{stem}_{counter}{suffix}"
            counter += 1
        used_names.add(local_name)
        destination = raw_dir / local_name
        destination.write_bytes(payload)
        archive_members = safe_extract_zip(destination, extract_dir / destination.stem) if zipfile.is_zipfile(destination) else []
        inventory.append(
            {
                **candidate,
                "status": "downloaded",
                "final_url": final_url,
                "content_type": content_type(headers),
                "local_name": local_name,
                "size": len(payload),
                "sha256": sha256,
                "archive_members": archive_members,
            }
        )

    summary = {
        "status": "supplementary_files_acquired" if any(row.get("status") == "downloaded" for row in inventory) else "supplementary_acquisition_blocked",
        "source_id": config["source_id"],
        "article_doi": config["article_doi"],
        "crossref_message": crossref.get("message") if isinstance(crossref, dict) else None,
        "discovery_pages": discovery_pages,
        "n_candidates": len(candidates),
        "n_downloaded": sum(row.get("status") == "downloaded" for row in inventory),
        "files": inventory,
        "errors": errors,
        "expected_context_to_verify_from_source": config["expected_context_to_verify_from_source"],
        "claim_boundary": config["claim_boundary"],
    }
    (args.output_dir / "source_inventory.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, default=str) + "\n",
        encoding="utf-8",
    )
    print(f"supplement candidates: {summary['n_candidates']}")
    print(f"downloaded: {summary['n_downloaded']}")
    if summary["n_downloaded"] == 0:
        raise RuntimeError("supplementary acquisition blocked; see source_inventory.json")


if __name__ == "__main__":
    main()
