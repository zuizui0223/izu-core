from __future__ import annotations

import importlib.util
import json
from datetime import datetime, timedelta
from pathlib import Path

import openpyxl
import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/adapt_hawaii_native_pollination_regime.py"
ADMISSION = ROOT / "data/design/chapter2_hawaii_natural_regime_admission_20260914.json"

spec = importlib.util.spec_from_file_location("hawaii_regime_adapter", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

HEADERS = [
    "Site",
    "Plant Species",
    "Date",
    "Start Time",
    "Observer",
    "Scan block time start",
    "Scan visitor spp",
    "Scan # Inds",
]


def _synthetic_workbook(path: Path) -> None:
    workbook = openpyxl.Workbook()
    workbook.remove(workbook.active)
    start = datetime(2026, 1, 1)
    for sheet in module.OBSERVATION_SHEETS:
        worksheet = workbook.create_sheet(sheet)
        worksheet.append(HEADERS)
        for day in range(6):
            date = start + timedelta(days=day)
            for block, partner, count in ((800, "bee a", 1 + day), (810, "bee b", 2 + day), (820, "bee c", 7 - day)):
                worksheet.append(["plot free text", sheet, date, 800, "obs", block, partner, count])
        if sheet == module.OBSERVATION_SHEETS[0]:
            worksheet.append(["plot free text", sheet, start, 800, "obs", 830, "bee missing", None])
    workbook.save(path)


def test_adapter_preserves_one_ecosystem_unit_and_source_native_dates(tmp_path: Path) -> None:
    workbook = tmp_path / "hawaii.xlsx"
    _synthetic_workbook(workbook)
    rows, diagnostics = module.adapt_workbook(workbook, expected_sha256=module._sha256(workbook))

    assert diagnostics["system_count"] == 1
    assert diagnostics["time_bins"] == 6
    assert diagnostics["raw_partner_labels"] == 3
    assert diagnostics["nonconstant_partner_series"] == 3
    assert diagnostics["coordinate_values_opened"] is False
    assert {row["system_id"] for row in rows} == {module.SYSTEM_ID}
    assert len({row["time_bin"] for row in rows}) == 6
    assert len(rows) == 18


def test_adapter_uses_scan_events_as_effort_and_does_not_impute_missing_count(tmp_path: Path) -> None:
    workbook = tmp_path / "hawaii.xlsx"
    _synthetic_workbook(workbook)
    rows, diagnostics = module.adapt_workbook(workbook, expected_sha256=module._sha256(workbook))

    first_date = diagnostics["first_time_bin"]
    first_rows = [row for row in rows if row["time_bin"] == first_date]
    assert {row["effort"] for row in first_rows} == {25}
    assert "BEE MISSING" not in {row["partner_id"] for row in rows}


def test_production_hash_lock_rejects_other_workbooks(tmp_path: Path) -> None:
    workbook = tmp_path / "hawaii.xlsx"
    _synthetic_workbook(workbook)
    with pytest.raises(ValueError, match="unexpected Hawaii workbook SHA256"):
        module.adapt_workbook(workbook)


def test_admission_record_precedes_coordinate_opening_and_counts_one_system() -> None:
    admission = json.loads(ADMISSION.read_text(encoding="utf-8"))
    assert admission["status"] == "admitted_for_coordinate_computation"
    assert admission["decision"]["counts_toward_NEE_systems"] == 1
    assert admission["system_unit_decision"]["focal_plant_sheets"] == 8
    assert admission["coordinate_values_opened"] is False
