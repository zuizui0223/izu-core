from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/results/chapter2_mahe_visitfreq_known_mirror_audit_20260915.json"

SOURCE_PAGES = [
    {
        "url": "https://www.nceas.ucsb.edu/interactionweb/html/kaiser-bunbury_et_al_2017.html",
        "role": "source URL recorded by the verified Schwarz et al. temporal compilation",
    },
    {
        "url": "https://iwdb.nceas.ucsb.edu/html/kaiser-bunbury_et_al_2017.html",
        "role": "independently verified IWDB mirror predeclared in the weighted-source contract",
    },
]


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            self._href = dict(attrs).get("href")
            self._text = []

    def handle_data(self, data):
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "a" and self._href is not None:
            self.links.append((self._href, " ".join(self._text).strip()))
            self._href = None
            self._text = []


def get_bytes(url: str, timeout: int = 60) -> tuple[bytes, str, dict[str, str]]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "izu-core-source-audit/1.0",
            "Accept": "text/html,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-excel,application/octet-stream,*/*;q=0.5",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read(), response.geturl(), {k.lower(): v for k, v in response.headers.items()}


def main() -> None:
    state: dict[str, object] = {
        "schema_version": "1.0",
        "analysis": "chapter2_mahe_visitfreq_known_mirror_audit",
        "status": "source_transport_only_coordinates_not_opened",
        "target_doi": "10.1038/nature21071",
        "expected_labels": ["64 networks_no.visits", "64 networks_visitfreq"],
        "source_pages": [],
        "coordinates_opened": False,
    }
    recovered = []
    for spec in SOURCE_PAGES:
        page_state: dict[str, object] = {"url": spec["url"], "role": spec["role"]}
        try:
            payload, resolved, headers = get_bytes(spec["url"], timeout=60)
            page_state.update({
                "status": "page_recovered",
                "resolved_url": resolved,
                "bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "content_type": headers.get("content-type"),
            })
            parser = LinkParser()
            parser.feed(payload.decode("utf-8", errors="replace"))
            candidates = []
            for href, label in parser.links:
                absolute = urllib.parse.urljoin(resolved, href)
                joined = f"{href} {label}".casefold()
                if any(token in joined for token in (".xlsx", ".xls", "visitfreq", "no.visits", "no visits", "excel")):
                    candidates.append({"href": href, "label": label, "url": absolute})
            page_state["candidate_links"] = candidates
            downloads = []
            for item in candidates:
                url = item["url"]
                if not re.search(r"\.xlsx?(?:$|[?#])", url, re.I):
                    continue
                try:
                    data, resolved_file, file_headers = get_bytes(url, timeout=90)
                    downloads.append({
                        "label": item["label"],
                        "url": url,
                        "resolved_url": resolved_file,
                        "bytes": len(data),
                        "sha256": hashlib.sha256(data).hexdigest(),
                        "content_type": file_headers.get("content-type"),
                        "xlsx_signature": data.startswith(b"PK\x03\x04"),
                        "xls_signature": data.startswith(bytes.fromhex("D0CF11E0A1B11AE1")),
                    })
                    if data.startswith(b"PK\x03\x04") or data.startswith(bytes.fromhex("D0CF11E0A1B11AE1")):
                        recovered.append(downloads[-1])
                except Exception as exc:
                    downloads.append({"label": item["label"], "url": url, "status": "download_failed", "error": repr(exc)})
            page_state["spreadsheet_attempts"] = downloads
        except Exception as exc:
            page_state.update({"status": "page_transport_failed", "error": repr(exc)})
        state["source_pages"].append(page_state)

    state["recovered_spreadsheets"] = recovered
    has_visitfreq = any("visitfreq" in f"{row.get('label','')} {row.get('url','')}".casefold() for row in recovered)
    state["primary_visitfreq_transport_recovered"] = has_visitfreq
    state["decision"] = (
        "KNOWN_SOURCE_MIRROR_EXPOSES_VISITFREQ_SPREADSHEET_NEXT_INSPECT_SCHEMA"
        if has_visitfreq
        else "KNOWN_SOURCE_MIRRORS_DO_NOT_RECOVER_PRIMARY_VISITFREQ"
    )
    state["claim_boundary"] = (
        "Only source pages already named before this robustness challenge are attempted. "
        "Only spreadsheet links exposed by a successfully fetched page are followed; no workbook path is guessed. "
        "No D1, phi, determinant, response, or route metric is calculated."
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(state, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
