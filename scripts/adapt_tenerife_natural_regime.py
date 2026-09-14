from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path

SOURCE_STUDY_ID = "lara_romero_etal_2019_tenerife_pollination"
ARCHIPELAGO_ID = "canary_islands"

SYSTEM_FILES = {
    "blanca_2700": "blanca_2730.txt",
    "rajada_2400": "rajada_2350.txt",
    "refugio_3200": "refugio_3300.txt",
    "torre_3500": "torre_3520.txt",
}

OUTPUT_FIELDS = [
    "source_study_id",
    "archipelago_id",
    "system_id",
    "time_bin",
    "partner_id",
    "value",
    "effort",
]


def clean(value: object) -> str:
    return str(value or "").strip()


def partner_id(row: dict[str, str]) -> str:
    genus = clean(row.get("genus"))
    species = clean(row.get("species"))
    family = clean(row.get("family"))
    taxon = " ".join(part for part in (genus, species) if part).strip()
    return taxon or family


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig", errors="replace") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def adapt_system(path: Path, system_id: str) -> list[dict[str, object]]:
    rows = read_rows(path)
    dates = sorted({clean(row.get("date")) for row in rows if clean(row.get("date"))})
    censuses = {
        (
            clean(row.get("locality")),
            clean(row.get("date")),
            clean(row.get("time")),
            clean(row.get("plant")),
        )
        for row in rows
        if clean(row.get("date")) and clean(row.get("time")) and clean(row.get("plant"))
    }
    effort_by_date = Counter(date for _, date, _, _ in censuses)

    values: dict[tuple[str, str], float] = defaultdict(float)
    observed_partners: set[str] = set()
    for row in rows:
        date = clean(row.get("date"))
        if not date:
            continue
        partner = partner_id(row)
        raw_value = clean(row.get("flower_visits"))
        value = float(raw_value) if raw_value else 0.0
        if value < 0:
            raise ValueError(f"negative flower_visits in {path}: {row}")
        if partner:
            observed_partners.add(partner)
            values[(date, partner)] += value

    if not observed_partners:
        raise ValueError(f"{system_id}: no identified partners")
    anchor_partner = sorted(observed_partners)[0]

    output: list[dict[str, object]] = []
    for date in dates:
        effort = int(effort_by_date[date])
        if effort <= 0:
            raise ValueError(f"{system_id} {date}: no reconstructible census effort")
        emitted = False
        for partner in sorted(observed_partners):
            value = float(values.get((date, partner), 0.0))
            if value <= 0:
                continue
            output.append(
                {
                    "source_study_id": SOURCE_STUDY_ID,
                    "archipelago_id": ARCHIPELAGO_ID,
                    "system_id": system_id,
                    "time_bin": date,
                    "partner_id": partner,
                    "value": value,
                    "effort": effort,
                }
            )
            emitted = True
        if not emitted:
            output.append(
                {
                    "source_study_id": SOURCE_STUDY_ID,
                    "archipelago_id": ARCHIPELAGO_ID,
                    "system_id": system_id,
                    "time_bin": date,
                    "partner_id": anchor_partner,
                    "value": 0.0,
                    "effort": effort,
                }
            )
    return output


def adapt(root: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for system_id, filename in SYSTEM_FILES.items():
        path = root / filename
        if not path.is_file():
            raise FileNotFoundError(path)
        rows.extend(adapt_system(path, system_id))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True, help="Directory containing the four source-native Tenerife txt files")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    rows = adapt(args.root)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
