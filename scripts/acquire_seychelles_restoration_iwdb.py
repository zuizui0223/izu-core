#!/usr/bin/env python3
"""Acquire the source-native Kaiser-Bunbury et al. 2017 IWDB Excel files."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "a":
            self._href = dict(attrs).get("href")
            self._text = []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._href is not None:
            self.links.append((self._href, " ".join(self._text).strip()))
            self._href = None
            self._text = []


def request_bytes(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "izu-core-source-audit/1.0 (+https://github.com/zuizui0223/izu-core)",
            "Accept": "text/html,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-excel,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        return response.read()


def safe_name(url: str, fallback: str) -> str:
    path = urllib.parse.urlparse(url).path
    name = Path(urllib.parse.unquote(path)).name or fallback
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name)


def workbook_inventory(path: Path) -> dict[str, object]:
    suffix = path.suffix.lower()
    if suffix == ".xlsx":
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        sheets = []
        for ws in wb.worksheets:
            first_rows = []
            for index, row in enumerate(ws.iter_rows(values_only=True)):
                first_rows.append([value for value in row])
                if index >= 2:
                    break
            sheets.append({
                "sheet": ws.title,
                "max_row": ws.max_row,
                "max_column": ws.max_column,
                "preview": first_rows,
            })
        wb.close()
        return {"format": "xlsx", "sheets": sheets}
    if suffix == ".xls":
        import xlrd
        book = xlrd.open_workbook(path)
        sheets = []
        for sheet in book.sheets():
            preview = [sheet.row_values(index) for index in range(min(sheet.nrows, 3))]
            sheets.append({"sheet": sheet.name, "max_row": sheet.nrows, "max_column": sheet.ncols, "preview": preview})
        return {"format": "xls", "sheets": sheets}
    return {"format": suffix.lstrip(".") or "unknown"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("config/seychelles_restoration_network_iwdb_source.json"))
    parser.add_argument("--outdir", type=Path, default=Path("artifacts/seychelles_restoration_iwdb"))
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    page_url = str(config["source_page"])
    args.outdir.mkdir(parents=True, exist_ok=True)
    raw_dir = args.outdir / "files"
    raw_dir.mkdir(parents=True, exist_ok=True)

    page = request_bytes(page_url)
    page_sha = hashlib.sha256(page).hexdigest()
    text = page.decode("utf-8", errors="replace")
    parser_html = LinkParser(); parser_html.feed(text)

    links = []
    for href, label in parser_html.links:
        absolute = urllib.parse.urljoin(page_url, href)
        combined = f"{href} {label}".lower()
        if any(token in combined for token in (".xlsx", ".xls", "64 network", "visits", "visitfreq")):
            links.append({"href": href, "label": label, "url": absolute})

    # Prefer actual spreadsheet hrefs; keep all candidate links in the manifest for auditability.
    spreadsheet_links = [row for row in links if re.search(r"\.xlsx?(?:$|[?#])", row["url"], re.I)]
    if not spreadsheet_links:
        raise ValueError(f"no spreadsheet links found on IWDB page; candidates={links}")

    files = []
    for index, row in enumerate(spreadsheet_links, start=1):
        payload = request_bytes(row["url"])
        name = safe_name(row["url"], f"iwdb_{index}.xlsx")
        destination = raw_dir / name
        destination.write_bytes(payload)
        if len(payload) < 1024:
            raise ValueError(f"implausibly small spreadsheet payload: {name} ({len(payload)} bytes)")
        files.append({
            "name": name,
            "label": row["label"],
            "url": row["url"],
            "bytes": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
            "workbook": workbook_inventory(destination),
        })

    summary = {
        "schema_version": "1.0",
        "source_id": config["source_id"],
        "article_doi": config["article_doi"],
        "source_page": page_url,
        "source_page_bytes": len(page),
        "source_page_sha256": page_sha,
        "candidate_links": links,
        "downloaded_spreadsheets": files,
        "expected_scale": {
            key: config[key]
            for key in ("expected_networks", "expected_sites", "expected_months", "expected_observation_hours", "expected_unique_links", "expected_pollinator_visits")
        },
        "claim_boundary": config["claim_boundary"],
    }
    (args.outdir / "source_inventory.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    print(json.dumps({"candidate_links": links, "downloaded": [{"name": f["name"], "bytes": f["bytes"], "sha256": f["sha256"], "sheets": [s["sheet"] for s in f["workbook"].get("sheets", [])]} for f in files]}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
