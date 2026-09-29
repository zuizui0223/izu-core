"""Convert the locked Inoue trait transcription into prediction-calibration rows.

The resulting table keeps the three channels distinct:

* flower length (morphology);
* multilocus outcrossing (realized mating-system estimate); and
* bagged capsule set (autonomous reproductive capacity, not realized selfing).

No row is fabricated for missing flower-length measurements, and no public
occurrence is used to assign a pollinator regime.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path


REGIME = {
    "Honshu": "large_bombus",
    "Oshima": "ardens",
    "Toshima": "no_bombus",
    "Niijima": "no_bombus",
    "Kozushima": "no_bombus",
    "Miyake": "no_bombus",
    "Hachijo": "no_bombus",
}
FIELDS = (
    "observation_id", "analysis_partition", "lineage_id", "taxon", "analysis_group",
    "group_confidence", "trait_id", "trait_family", "pollinator_regime", "value",
    "value_unit", "evidence_tier", "source_locator", "review_status", "weight", "notes",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("data/inoue_literature_island_traits.csv"))
    parser.add_argument("--out", type=Path, required=True)
    return parser.parse_args()


def as_float(value: str) -> float | None:
    text = (value or "").strip()
    return None if not text else float(text)


def main() -> None:
    args = parse_args()
    with args.source.open(encoding="utf-8", newline="") as handle:
        source_rows = list(csv.DictReader(handle))
    output: list[dict[str, str]] = []
    for row in source_rows:
        island = row["island_id"]
        if island not in REGIME:
            raise SystemExit(f"unmapped island_id: {island}")
        common = {
            "analysis_partition": "calibration",
            "lineage_id": "campanula_microdonta",
            "taxon": "Campanula microdonta",
            "analysis_group": "specialist",
            "group_confidence": "source_locked_focal",
            "pollinator_regime": REGIME[island],
            "evidence_tier": "source_locked",
            "source_locator": f"data/inoue_literature_island_traits.csv:{island}",
            "review_status": "source_verified",
            "weight": "1",
        }
        minimum = as_float(row["outcrossing_rate_min"])
        maximum = as_float(row["outcrossing_rate_max"])
        if minimum is not None and maximum is not None:
            output.append({
                **common,
                "observation_id": f"campanula-outcrossing-{island.lower()}",
                "trait_id": "multilocus_outcrossing_rate",
                "trait_family": "outcrossing",
                "value": f"{(minimum + maximum) / 2:.9g}",
                "value_unit": "proportion",
                "notes": "Midpoint of locked min/max transcription; a direct outcrossing estimate, not self-compatibility.",
            })
        flower = as_float(row["flower_length_mm"])
        if flower is not None:
            output.append({
                **common,
                "observation_id": f"campanula-flower-{island.lower()}",
                "trait_id": "flower_length_mm",
                "trait_family": "floral_size",
                "value": f"{flower:.9g}",
                "value_unit": "mm",
                "notes": "Locked literature transcription; measurement context remains in source table.",
            })
        bagged = as_float(row["bagged_capsule_set_pct"])
        if bagged is not None:
            output.append({
                **common,
                "observation_id": f"campanula-autonomous-capacity-{island.lower()}",
                "trait_id": "bagged_capsule_set",
                "trait_family": "autonomous_assurance",
                "value": f"{bagged / 100:.9g}",
                "value_unit": "proportion",
                "notes": "Bagged capsule set is autonomous reproductive capacity; it is not a realized selfing-rate estimate.",
            })
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(output)
    print(f"wrote {len(output)} calibration observations to {args.out}")


if __name__ == "__main__":
    main()
