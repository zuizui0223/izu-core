from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import openpyxl


STRUCTURAL_TOKENS = (
    "site",
    "community",
    "plot",
    "date",
    "day",
    "time",
    "plant",
    "pollinator",
    "visitor",
    "interaction",
    "visit",
    "abundance",
    "frequency",
    "effort",
    "minute",
    "hour",
)


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def inspect_workbook(path: Path) -> dict[str, object]:
    workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
    sheets = []
    for worksheet in workbook.worksheets:
        preview_rows = []
        structural_hits: set[str] = set()
        for row_index, row in enumerate(worksheet.iter_rows(values_only=True)):
            values = [clean(value) for value in row]
            if row_index < 12:
                preview_rows.append(values[:40])
            for value in values:
                lower = value.casefold()
                for token in STRUCTURAL_TOKENS:
                    if token in lower:
                        structural_hits.add(token)
            if row_index >= 2000:
                break
        sheets.append(
            {
                "sheet": worksheet.title,
                "max_row": worksheet.max_row,
                "max_column": worksheet.max_column,
                "structural_token_hits": sorted(structural_hits),
                "preview": preview_rows,
            }
        )
    workbook.close()
    return {"filename": path.name, "sheets": sheets}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-root", type=Path, default=Path("artifacts/mallorca_stability"))
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("artifacts/mallorca_stability/natural_regime_source_inspection.json"),
    )
    args = parser.parse_args()
    files = sorted((args.artifact_root / "files").glob("*.xlsx"))
    if len(files) < 2:
        raise RuntimeError(f"expected Dryad_dataStability.xlsx and README.xlsx, found {files}")
    result = {
        "analysis": "mallorca_natural_regime_source_inspection",
        "files": [inspect_workbook(path) for path in files],
        "gate_evidence": {
            "coordinate_values_opened": False,
            "inspection_role": "source-structure only; no D1, phi, rho_eq, synchrony ranking or journal route is computed",
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result["gate_evidence"], indent=2))


if __name__ == "__main__":
    main()
