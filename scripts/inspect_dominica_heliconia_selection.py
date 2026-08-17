#!/usr/bin/env python3
"""Print the source-native Dominica Heliconia XLS schema for audit."""
from __future__ import annotations
import json
from pathlib import Path
import xlrd

PATH = Path("artifacts/dominica_heliconia_selection/files/Temeles_and_Bishop_data.xls")
book = xlrd.open_workbook(PATH)
report = {"workbook": PATH.name, "sheets": []}
for sheet in book.sheets():
    rows = [sheet.row_values(i) for i in range(min(sheet.nrows, 8))]
    report["sheets"].append({
        "name": sheet.name,
        "nrows": sheet.nrows,
        "ncols": sheet.ncols,
        "preview": rows,
    })
print(json.dumps(report, indent=2, ensure_ascii=False, default=str))
