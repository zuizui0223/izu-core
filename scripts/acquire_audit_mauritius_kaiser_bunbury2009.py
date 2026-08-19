from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data/design/mauritius_kaiser_bunbury2009_weighted_source.json"
RAW_DIR = ROOT / "data/external/mauritius_kaiser_bunbury2009"
RAW = RAW_DIR / "kaiser-bunbury_2009.xls"
OUT = ROOT / "data/results/mauritius_kaiser_bunbury2009_weighted_source_audit.json"


def get_bytes(url: str, timeout: int = 90) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "izu-core-source-audit/1.0", "Accept": "application/vnd.ms-excel,*/*"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def sha256(data: bytes) -> str:
    h = hashlib.sha256(); h.update(data); return h.hexdigest()


def preview_sheet(sheet, max_rows=14, max_cols=14):
    rows = []
    for i in range(min(sheet.nrows, max_rows)):
        row = []
        for j in range(min(sheet.ncols, max_cols)):
            value = sheet.cell_value(i, j)
            if isinstance(value, float) and value.is_integer():
                value = int(value)
            row.append(value)
        rows.append(row)
    return rows


def main() -> None:
    try:
        import xlrd
    except ImportError as exc:
        raise RuntimeError("xlrd is required for .xls audit") from exc
    config = json.loads(CONFIG.read_text())
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "1.0",
        "analysis": "mauritius_kaiser_bunbury2009_weighted_source_audit",
        "source": config["source"],
        "article_doi": config["article_doi"],
        "primary_tierb_weight_family": config["primary_tierb_weight_family"],
        "status": "not_recovered",
    }
    try:
        data = get_bytes(config["iwdb_excel"])
        if len(data) < 4096:
            raise RuntimeError(f"workbook payload too small: {len(data)}")
        RAW.write_bytes(data)
        book = xlrd.open_workbook(file_contents=data)
        sheets = []
        for sheet in book.sheets():
            numeric_cells = 0
            positive_numeric_cells = 0
            text_cells = 0
            for i in range(sheet.nrows):
                for j in range(sheet.ncols):
                    v = sheet.cell_value(i, j)
                    if isinstance(v, (int, float)) and not isinstance(v, bool):
                        numeric_cells += 1
                        if float(v) > 0:
                            positive_numeric_cells += 1
                    elif str(v).strip():
                        text_cells += 1
            sheets.append({
                "name": sheet.name,
                "nrows": sheet.nrows,
                "ncols": sheet.ncols,
                "numeric_cells": numeric_cells,
                "positive_numeric_cells": positive_numeric_cells,
                "text_cells": text_cells,
                "preview": preview_sheet(sheet),
            })
        payload.update({
            "status": "workbook_bytes_recovered_and_structure_audited",
            "source_bytes": len(data),
            "source_sha256": sha256(data),
            "sheet_count": len(sheets),
            "sheets": sheets,
            "next_gate": "Identify control/restored and visitation-rate/fully-quantitative matrix sheets from workbook labels/layout only. Freeze sheet roles before calculating network metrics; do not choose sheets by Doré reconciliation or Tier-B fit.",
            "claim_boundary": config["claim_boundary"],
        })
    except Exception as exc:
        payload.update({
            "status": "source_recovery_or_workbook_audit_failed",
            "error": repr(exc),
            "next_gate": "Use an independently verified public mirror or original source; do not infer workbook contents.",
        })
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
