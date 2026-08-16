#!/usr/bin/env python3
"""Inventory the source-native Galapagos 2018 XLS before defining analysis."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import xlrd


def main() -> None:
    ap=argparse.ArgumentParser(); ap.add_argument("--xls",type=Path,default=Path("artifacts/galapagos_bird_insect_effectiveness/files/Hervias_Parejo_and_Traveset_-_ajb_-_2018.xls")); ap.add_argument("--out",type=Path,default=Path("artifacts/galapagos_bird_insect_effectiveness/schema_inventory.json")); args=ap.parse_args()
    book=xlrd.open_workbook(args.xls); sheets=[]
    for sheet in book.sheets():
        preview=[sheet.row_values(i) for i in range(min(sheet.nrows,12))]
        sheets.append({"sheet":sheet.name,"n_rows":sheet.nrows,"n_cols":sheet.ncols,"preview":preview})
    report={"workbook":args.xls.name,"n_sheets":len(sheets),"sheets":sheets}
    args.out.parent.mkdir(parents=True,exist_ok=True); args.out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"n_sheets":len(sheets),"sheets":[{"sheet":s["sheet"],"n_rows":s["n_rows"],"n_cols":s["n_cols"],"preview":s["preview"][:4]} for s in sheets]},indent=2,ensure_ascii=False))

if __name__=="__main__": main()
