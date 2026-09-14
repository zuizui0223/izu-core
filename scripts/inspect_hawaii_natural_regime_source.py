from __future__ import annotations

import argparse
import json
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

import openpyxl


HEADER_TOKENS = {
    "site": ("site",),
    "date": ("date",),
    "start_time": ("start time", "start_time"),
    "end_time": ("end time", "end_time"),
    "duration": ("duration", "minutes", "minute", "hours", "hour", "effort", "observation time", "observation_time"),
    "visitor": ("visitor spp", "visitor species", "visitor", "insect"),
}


def normalize(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip()).casefold()


def find_column(headers: list[object], tokens: tuple[str, ...]) -> int | None:
    normalized = [normalize(value) for value in headers]
    for i, header in enumerate(normalized):
        if any(token in header for token in tokens):
            return i
    return None


def docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        payload = archive.read("word/document.xml")
    root = ET.fromstring(payload)
    text = " ".join(node.text or "" for node in root.iter() if node.tag.endswith("}t"))
    return re.sub(r"\s+", " ", text).strip()


def source_files(root: Path) -> tuple[Path, Path]:
    candidates = list((root / "files").glob("*"))
    xlsx = [path for path in candidates if path.suffix.casefold() == ".xlsx"]
    docx = [path for path in candidates if path.suffix.casefold() == ".docx"]
    if len(xlsx) != 1 or len(docx) != 1:
        raise RuntimeError(f"expected one xlsx and one docx, got xlsx={xlsx}, docx={docx}")
    return xlsx[0], docx[0]


def inspect_workbook(path: Path) -> dict:
    workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
    sheets = []
    global_dates: set[str] = set()
    global_sessions: set[tuple[str, str, str, str]] = set()
    effort_like_headers: Counter[str] = Counter()
    for worksheet in workbook.worksheets:
        rows = worksheet.iter_rows(values_only=True)
        try:
            headers = list(next(rows))
        except StopIteration:
            continue
        indices = {name: find_column(headers, tokens) for name, tokens in HEADER_TOKENS.items()}
        for header in headers:
            h = normalize(header)
            if any(token in h for token in HEADER_TOKENS["duration"] + HEADER_TOKENS["end_time"]):
                effort_like_headers[str(header)] += 1
        date_values: set[str] = set()
        session_values: set[tuple[str, str, str, str]] = set()
        row_count = 0
        for row in rows:
            row_count += 1
            if indices["date"] is not None and indices["date"] < len(row):
                date = str(row[indices["date"]] or "").strip()
                if date:
                    date_values.add(date)
                    global_dates.add(date)
            parts = []
            for field in ("site", "date", "start_time"):
                idx = indices[field]
                parts.append(str(row[idx] or "").strip() if idx is not None and idx < len(row) else "")
            observer_idx = find_column(headers, ("observer",))
            observer = str(row[observer_idx] or "").strip() if observer_idx is not None and observer_idx < len(row) else ""
            session = (parts[0], parts[1], parts[2], observer)
            if any(session):
                session_values.add(session)
                global_sessions.add(session)
        sheets.append(
            {
                "sheet": worksheet.title,
                "rows_after_header": row_count,
                "headers": [str(value) if value is not None else "" for value in headers],
                "required_columns": indices,
                "unique_dates": len(date_values),
                "unique_sessions": len(session_values),
            }
        )
    workbook.close()
    return {
        "sheets": sheets,
        "global_unique_dates": len(global_dates),
        "global_unique_sessions": len(global_sessions),
        "effort_like_headers": dict(effort_like_headers),
    }


def inspect_readme(path: Path) -> dict:
    text = docx_text(path)
    sentences = re.split(r"(?<=[.!?])\s+", text)
    keywords = ("hour", "minute", "duration", "observation", "observe", "effort", "start time", "end time")
    snippets = [sentence for sentence in sentences if any(keyword in sentence.casefold() for keyword in keywords)]
    return {
        "characters": len(text),
        "effort_protocol_snippets": snippets[:40],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", type=Path, default=Path("artifacts/hawaii_native_pollination"))
    parser.add_argument("--out", type=Path, default=Path("artifacts/hawaii_native_pollination/natural_regime_source_inspection.json"))
    args = parser.parse_args()
    xlsx, docx = source_files(args.artifact_root)
    workbook = inspect_workbook(xlsx)
    readme = inspect_readme(docx)
    sheets = workbook["sheets"]
    temporal_schema = bool(sheets) and all(
        row["required_columns"]["site"] is not None
        and row["required_columns"]["date"] is not None
        and row["required_columns"]["start_time"] is not None
        and row["required_columns"]["visitor"] is not None
        for row in sheets
    )
    direct_effort_field = bool(workbook["effort_like_headers"])
    result = {
        "analysis": "hawaii_natural_regime_source_inspection",
        "artifact_root": str(args.artifact_root),
        "workbook": workbook,
        "readme": readme,
        "gate_evidence": {
            "raw_temporal_schema_confirmed": temporal_schema,
            "minimum_six_dates_possible": workbook["global_unique_dates"] >= 6,
            "direct_effort_or_endtime_header_present": direct_effort_field,
            "effort_protocol_text_present": bool(readme["effort_protocol_snippets"]),
            "coordinate_values_opened": False,
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    print(json.dumps(result["gate_evidence"], indent=2))


if __name__ == "__main__":
    main()
