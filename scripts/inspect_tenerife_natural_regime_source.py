from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

import openpyxl


TOKENS = (
    "site", "plot", "locality", "date", "day", "year", "time", "plant", "pollinator",
    "visitor", "interaction", "visit", "frequency", "abundance", "count", "effort", "minute", "hour"
)


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def inspect_delimited(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    delimiter = "\t" if path.suffix.casefold() == ".tsv" else ","
    try:
        delimiter = csv.Sniffer().sniff(text[:8192], delimiters=",\t;").delimiter
    except csv.Error:
        pass
    rows = list(csv.reader(text.splitlines(), delimiter=delimiter))
    preview = rows[:12]
    hits = sorted({token for row in preview for value in row for token in TOKENS if token in clean(value).casefold()})
    return {
        "path": str(path),
        "kind": "delimited",
        "rows": len(rows),
        "columns_max": max((len(row) for row in rows), default=0),
        "structural_token_hits": hits,
        "preview": preview,
    }


def inspect_xlsx(path: Path) -> dict[str, object]:
    workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
    sheets = []
    for worksheet in workbook.worksheets:
        preview = []
        hits: set[str] = set()
        for i, row in enumerate(worksheet.iter_rows(values_only=True)):
            values = [clean(value) for value in row]
            if i < 12:
                preview.append(values[:40])
            for value in values[:40]:
                lower = value.casefold()
                hits.update(token for token in TOKENS if token in lower)
            if i >= 100:
                break
        sheets.append({
            "sheet": worksheet.title,
            "max_row": worksheet.max_row,
            "max_column": worksheet.max_column,
            "structural_token_hits": sorted(hits),
            "preview": preview,
        })
    workbook.close()
    return {"path": str(path), "kind": "xlsx", "sheets": sheets}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-root", type=Path, default=Path("artifacts/tenerife_pollination"))
    parser.add_argument("--out", type=Path, default=Path("artifacts/tenerife_pollination/natural_regime_source_inspection.json"))
    args = parser.parse_args()
    extracted = args.artifact_root / "extracted"
    files = sorted(path for path in extracted.rglob("*") if path.is_file())
    inspected = []
    for path in files:
        suffix = path.suffix.casefold()
        if suffix in {".csv", ".tsv", ".txt"}:
            inspected.append(inspect_delimited(path))
        elif suffix in {".xlsx", ".xlsm"}:
            inspected.append(inspect_xlsx(path))
        else:
            inspected.append({"path": str(path), "kind": "other", "bytes": path.stat().st_size})
    result = {
        "analysis": "tenerife_natural_regime_source_inspection",
        "files": inspected,
        "gate_evidence": {
            "coordinate_values_opened": False,
            "inspection_role": "raw archive granularity only; aggregated networks do not automatically pass"
        }
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result["gate_evidence"], indent=2))


if __name__ == "__main__":
    main()
