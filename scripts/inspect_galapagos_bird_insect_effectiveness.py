#!/usr/bin/env python3
"""Inventory the source-native Galapagos 2018 XLS before defining analysis."""
from __future__ import annotations
import argparse, collections, json
from pathlib import Path
import xlrd


def normalized(value):
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def main() -> None:
    ap=argparse.ArgumentParser(); ap.add_argument("--xls",type=Path,default=Path("artifacts/galapagos_bird_insect_effectiveness/files/Hervias_Parejo_and_Traveset_-_ajb_-_2018.xls")); ap.add_argument("--out",type=Path,default=Path("artifacts/galapagos_bird_insect_effectiveness/schema_inventory.json")); args=ap.parse_args()
    book=xlrd.open_workbook(args.xls); sheets=[]
    for sheet in book.sheets():
        preview=[sheet.row_values(i) for i in range(min(sheet.nrows,12))]
        entry={"sheet":sheet.name,"n_rows":sheet.nrows,"n_cols":sheet.ncols,"preview":preview}
        if sheet.nrows:
            headers=[str(v).strip() for v in sheet.row_values(0)]
            entry["headers"]=headers
            if "treatment" in headers:
                j=headers.index("treatment")
                counts=collections.Counter(str(normalized(sheet.cell_value(i,j))).strip() for i in range(1,sheet.nrows))
                entry["treatment_row_counts"]=dict(sorted(counts.items()))
            if "ID" in headers:
                jid=headers.index("ID")
                entry["unique_individual_ids"]=len({normalized(sheet.cell_value(i,jid)) for i in range(1,sheet.nrows)})
                if "treatment" in headers:
                    jt=headers.index("treatment")
                    units={(normalized(sheet.cell_value(i,jid)),str(normalized(sheet.cell_value(i,jt))).strip()) for i in range(1,sheet.nrows)}
                    unit_counts=collections.Counter(t for _,t in units)
                    entry["unique_id_treatment_units"]=len(units)
                    entry["unique_id_treatment_counts"]=dict(sorted(unit_counts.items()))
            if "Species" in headers:
                js=headers.index("Species")
                entry["species_row_counts"]=dict(collections.Counter(str(sheet.cell_value(i,js)).strip() for i in range(1,sheet.nrows)))
            if sheet.name=="Census of flower visitors":
                for key in ("Class","Species","Flowers with bird exclusion treatment?"):
                    if key in headers:
                        j=headers.index(key)
                        entry[key+" counts"]=dict(collections.Counter(str(normalized(sheet.cell_value(i,j))).strip() for i in range(1,sheet.nrows)))
        sheets.append(entry)
    report={"workbook":args.xls.name,"n_sheets":len(sheets),"sheets":sheets}
    args.out.parent.mkdir(parents=True,exist_ok=True); args.out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"n_sheets":len(sheets),"sheets":[{k:s.get(k) for k in ("sheet","n_rows","n_cols","treatment_row_counts","unique_individual_ids","unique_id_treatment_units","unique_id_treatment_counts","species_row_counts","Class counts","Flowers with bird exclusion treatment? counts") if k in s} for s in sheets]},indent=2,ensure_ascii=False))

if __name__=="__main__": main()
