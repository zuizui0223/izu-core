from __future__ import annotations

import json
from pathlib import Path

from channel_id.external_archipelago_network import WeightedNetwork, network_metrics

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/external/mauritius_kaiser_bunbury2009/kaiser-bunbury_2009.xls"
ROLES = ROOT / "data/design/mauritius_kaiser_bunbury2009_sheet_roles.json"
OUT = ROOT / "data/results/mauritius_kaiser_bunbury2009_weighted_tierb.json"


def clean(value: object) -> str:
    return " ".join(str(value or "").split())


def as_weight(value: object, *, cell: str) -> float:
    if value in (None, ""):
        return 0.0
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"nonnumeric weight {cell}: {value!r}") from exc
    if out < 0:
        raise ValueError(f"negative weight {cell}: {out}")
    return out


def read_network(sheet, layout: dict) -> WeightedNetwork:
    plant_row = int(layout["plant_names_row_1_based"]) - 1
    plant_first = int(layout["plant_first_column_1_based"]) - 1
    animal_first = int(layout["animal_first_data_row_1_based"]) - 1
    animal_col = int(layout["animal_name_column_1_based"]) - 1

    plant_columns = []
    for column in range(plant_first, sheet.ncols):
        name = clean(sheet.cell_value(plant_row, column))
        if name:
            plant_columns.append((column, name))
    if not plant_columns:
        raise ValueError(f"{sheet.name}: no plant columns")

    pollinators = []
    source_rows = []
    for row in range(animal_first, sheet.nrows):
        animal = clean(sheet.cell_value(row, animal_col))
        if not animal:
            continue
        values = []
        numeric_seen = False
        for column, _ in plant_columns:
            raw = sheet.cell_value(row, column)
            if isinstance(raw, (int, float)):
                numeric_seen = True
            values.append(as_weight(raw, cell=f"{sheet.name}!R{row+1}C{column+1}"))
        if not numeric_seen:
            continue
        pollinators.append(animal)
        source_rows.append(values)
    if not pollinators:
        raise ValueError(f"{sheet.name}: no animal rows")

    # Source layout is pollinator x plant; WeightedNetwork is plant x pollinator.
    plant_rows = [
        [source_rows[p][plant_index] for p in range(len(pollinators))]
        for plant_index in range(len(plant_columns))
    ]
    return WeightedNetwork.from_rows(
        [name for _, name in plant_columns],
        pollinators,
        plant_rows,
    )


def main() -> None:
    try:
        import xlrd
    except ImportError as exc:
        raise RuntimeError("xlrd is required") from exc

    roles = json.loads(ROLES.read_text())
    if not RAW.exists():
        raise FileNotFoundError(RAW)
    book = xlrd.open_workbook(str(RAW))
    available = set(book.sheet_names())
    rows = []
    for spec in roles["sheet_roles"]:
        sheet_name = spec["sheet"]
        if sheet_name not in available:
            raise ValueError(f"missing frozen sheet {sheet_name!r}")
        network = read_network(book.sheet_by_name(sheet_name), roles["matrix_layout"])
        rows.append({
            **spec,
            "metrics": network_metrics(network),
        })
    book.release_resources()

    primary = [x for x in rows if x["analysis_role"] == "primary"]
    secondary = [x for x in rows if x["analysis_role"] == "secondary_sensitivity"]
    if {x["treatment"] for x in primary} != {"control", "restored"}:
        raise ValueError("primary sheets do not cover both treatments")
    if {x["treatment"] for x in secondary} != {"control", "restored"}:
        raise ValueError("secondary sheets do not cover both treatments")

    payload = {
        "schema_version": "1.0",
        "analysis": "mauritius_kaiser_bunbury2009_source_native_weighted_tierb",
        "source_sha256": roles["source_sha256"],
        "independent_system": "Mauritius",
        "nested_network_count": 2,
        "primary_weight_family": "visitation_rate",
        "secondary_weight_family": "interaction_strength",
        "rows": rows,
        "primary_rows": primary,
        "secondary_rows": secondary,
        "decision": "mauritius_source_native_weighted_tierb_ready",
        "cross_system_rule": roles["cross_system_unit_rule"],
        "claim_boundary": roles["claim_boundary"],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
