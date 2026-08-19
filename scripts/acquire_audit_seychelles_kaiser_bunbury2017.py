from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
import urllib.request
import zipfile
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data/design/seychelles_kaiser_bunbury2017_weighted_source.json"
RAW_DIR = ROOT / "data/external/seychelles_kaiser_bunbury2017"
OUT = ROOT / "data/results/seychelles_kaiser_bunbury2017_weighted_source_audit.json"


def get_bytes(url: str, timeout: int = 90) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "izu-core-source-audit/1.0", "Accept": "text/html,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,*/*"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def sha256(data: bytes) -> str:
    h = hashlib.sha256(); h.update(data); return h.hexdigest()


def hrefs_from_html(page_url: str, html: bytes) -> list[str]:
    text = html.decode("latin-1", errors="replace")
    hrefs = re.findall(r'href\s*=\s*["\']([^"\']+)["\']', text, flags=re.I)
    out = []
    for href in hrefs:
        absolute = urllib.parse.urljoin(page_url, href)
        lower = absolute.lower()
        if any(token in lower for token in ("xls", "xlsx", "excel", "kaiser", "visit")):
            out.append(absolute)
    return list(dict.fromkeys(out))


def inspect_excel(name: str, data: bytes) -> dict:
    lower = name.lower()
    if data[:2] == b"PK" or lower.endswith(".xlsx"):
        import openpyxl
        book = openpyxl.load_workbook(BytesIO(data), read_only=True, data_only=True)
        sheets = []
        for ws in book.worksheets:
            preview = []
            for row in ws.iter_rows(min_row=1, max_row=min(ws.max_row or 0, 12), values_only=True):
                preview.append([x for x in row[:14]])
            sheets.append({"name": ws.title, "nrows": ws.max_row, "ncols": ws.max_column, "preview": preview})
        book.close()
        return {"format": "xlsx", "sheets": sheets}
    import xlrd
    book = xlrd.open_workbook(file_contents=data)
    sheets = []
    for ws in book.sheets():
        preview = []
        for i in range(min(ws.nrows, 12)):
            preview.append([ws.cell_value(i, j) for j in range(min(ws.ncols, 14))])
        sheets.append({"name": ws.name, "nrows": ws.nrows, "ncols": ws.ncols, "preview": preview})
    return {"format": "xls", "sheets": sheets}


def main() -> None:
    config = json.loads(CONFIG.read_text())
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    page = config["iwdb_page"]
    payload = {
        "schema_version": "1.0",
        "analysis": "seychelles_kaiser_bunbury2017_weighted_source_audit",
        "article_doi": config["article_doi"],
        "primary_tierb_weight_family": config["primary_tierb_weight_family"],
        "secondary_sensitivity_weight_family": config["secondary_sensitivity_weight_family"],
        "status": "not_recovered",
        "attempts": [],
    }
    try:
        html = get_bytes(page)
        (RAW_DIR / "source_page.html").write_bytes(html)
        hrefs = hrefs_from_html(page, html)
        payload["source_page_sha256"] = sha256(html)
        payload["candidate_data_links"] = hrefs
        recovered = []
        for index, url in enumerate(hrefs):
            try:
                data = get_bytes(url)
                content_hint = data[:8]
                if len(data) < 1024:
                    raise RuntimeError(f"payload too small: {len(data)}")
                # Accept OLE xls or ZIP-based xlsx only; reject HTML/error pages.
                if not (data[:8] == bytes.fromhex("D0CF11E0A1B11AE1") or data[:2] == b"PK"):
                    raise RuntimeError(f"not an Excel payload: magic={content_hint!r}")
                suffix = ".xlsx" if data[:2] == b"PK" else ".xls"
                filename = Path(urllib.parse.urlparse(url).path).name or f"source_{index}{suffix}"
                if not filename.lower().endswith((".xls", ".xlsx")):
                    filename += suffix
                path = RAW_DIR / filename
                path.write_bytes(data)
                inspection = inspect_excel(filename, data)
                recovered.append({
                    "url": url,
                    "filename": filename,
                    "bytes": len(data),
                    "sha256": sha256(data),
                    **inspection,
                })
                payload["attempts"].append({"url": url, "status": "success", "bytes": len(data)})
            except Exception as exc:
                payload["attempts"].append({"url": url, "status": "failed", "error": repr(exc)})
        payload.update({
            "status": "source_page_and_excel_candidates_audited",
            "recovered_excel_file_count": len(recovered),
            "recovered_excel_files": recovered,
            "next_gate": "Identify the no.visits and visitfreq workbooks/sheets from source filenames and labels only, verify the 64 source-defined site-month networks, then freeze parsing roles before calculating Tier-B metrics.",
            "claim_boundary": config["claim_boundary"],
        })
    except Exception as exc:
        payload.update({
            "status": "source_page_recovery_failed",
            "error": repr(exc),
            "next_gate": "Use an independently verified public mirror; do not infer file URLs or source values.",
        })
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
