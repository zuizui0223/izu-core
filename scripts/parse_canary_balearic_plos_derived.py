#!/usr/bin/env python3
"""Parse source-locked Canary–Balearic PLOS derived partner-trait tables.

The source package does not contain full plant-by-visitor matrices. It contains
selected-species metadata (S1/S2) and monthly derived partner summaries (S3/S4).
The PLOS supporting-information labels for S3 and S4 are reversed relative to
the species-code domains in the files; this parser uses the audited code-domain
crosswalk and never infers interaction edges from the derived columns.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Iterable, Mapping, Sequence


SPECIFICITY_CLASSES = {
    "Generalized",
    "Specialized",
    "Opportunistic",
    "Selective",
}
ZONES = {"SB", "CM", "CB", "LC"}
ZONE_CONTEXT = {
    "SB": {
        "community_name": "Son Bosc",
        "island": "Mallorca",
        "archipelago": "Balearic Islands",
        "geological_origin": "continental_island_system",
    },
    "CM": {
        "community_name": "Cala Mesquida",
        "island": "Mallorca",
        "archipelago": "Balearic Islands",
        "geological_origin": "continental_island_system",
    },
    "CB": {
        "community_name": "Caleton Blanco",
        "island": "Lanzarote",
        "archipelago": "Canary Islands",
        "geological_origin": "oceanic_island_system",
    },
    "LC": {
        "community_name": "Las Conchas",
        "island": "Lanzarote",
        "archipelago": "Canary Islands",
        "geological_origin": "oceanic_island_system",
    },
}
SPECIES_CODE_PATTERN = re.compile(r"^[a-z]{3}\.[a-z0-9]{2,3}$")
MONTH_LABEL_PATTERN = re.compile(r"^\(([^)]+)\)$")
COLUMNS = (
    "source_logical_id",
    "resolved_domain",
    "specificity",
    "zone",
    "community_name",
    "island",
    "archipelago",
    "geological_origin",
    "species_code",
    "month_index",
    "month_label",
    "classification_metric",
    "classification_value",
    "partner_functional_richness",
    "partner_rank_abundance",
    "partner_abundance_evenness",
    "source_line",
)


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def as_number(token: str) -> float | None:
    if token.strip() in {"-", "–", "—", "NA", "na", ""}:
        return None
    try:
        value = float(token)
    except ValueError as error:
        raise ValueError(
            f"expected numeric or missing value, got {token!r}"
        ) from error
    if not math.isfinite(value):
        raise ValueError(f"value must be finite: {token!r}")
    return value


def parse_derived_lines(
    lines: Iterable[str],
    *,
    source_logical_id: str,
    resolved_domain: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    specificity: str | None = None
    zone: str | None = None
    for line_number, line in enumerate(lines, start=1):
        tokens = line.split()
        code_indices = [
            index
            for index, token in enumerate(tokens)
            if SPECIES_CODE_PATTERN.fullmatch(token.casefold())
        ]
        if not code_indices:
            continue
        code_index = code_indices[0]
        species_code = tokens[code_index].casefold()
        for token in tokens[:code_index]:
            if token in SPECIFICITY_CLASSES:
                specificity = token
            if token in ZONES:
                zone = token
        if specificity is None or zone is None:
            raise ValueError(
                f"row {line_number} lacks carried specificity/zone context: "
                f"{line!r}"
            )
        remainder = list(tokens[code_index + 1 :])
        if not remainder or not remainder[0].isdigit():
            raise ValueError(f"row {line_number} lacks integer month: {line!r}")
        month_index = int(remainder.pop(0))
        if month_index not in {1, 2, 3, 4}:
            raise ValueError(
                f"unexpected relative month {month_index} on row {line_number}"
            )
        month_label = ""
        if remainder:
            month_match = MONTH_LABEL_PATTERN.fullmatch(remainder[0])
            if month_match:
                month_label = month_match.group(1)
                remainder.pop(0)
        if len(remainder) != 4:
            raise ValueError(
                f"row {line_number} expected four derived values, got "
                f"{remainder!r}"
            )
        classification_value, functional_richness, rank_abundance, evenness = (
            as_number(token) for token in remainder
        )
        classification_metric = (
            "L"
            if specificity in {"Generalized", "Specialized"}
            else "d_prime"
        )
        context = ZONE_CONTEXT[zone]
        rows.append(
            {
                "source_logical_id": source_logical_id,
                "resolved_domain": resolved_domain,
                "specificity": specificity,
                "zone": zone,
                **context,
                "species_code": species_code,
                "month_index": month_index,
                "month_label": month_label,
                "classification_metric": classification_metric,
                "classification_value": classification_value,
                "partner_functional_richness": functional_richness,
                "partner_rank_abundance": rank_abundance,
                "partner_abundance_evenness": evenness,
                "source_line": line_number,
            }
        )
    return rows


def validate_rows(
    rows: Sequence[Mapping[str, object]],
) -> dict[str, object]:
    if not rows:
        raise ValueError("derived parser recovered no rows")
    domains = sorted({str(row["resolved_domain"]) for row in rows})
    zones = sorted({str(row["zone"]) for row in rows})
    specificities = sorted({str(row["specificity"]) for row in rows})
    if domains != ["flower_visitor", "plant"]:
        raise ValueError(f"unexpected domain set: {domains}")
    if set(zones) != ZONES:
        raise ValueError(f"not all four communities were recovered: {zones}")
    if set(specificities) != SPECIFICITY_CLASSES:
        raise ValueError(
            f"not all four specificity classes were recovered: {specificities}"
        )
    for row in rows:
        expected_metric = (
            "L"
            if row["specificity"] in {"Generalized", "Specialized"}
            else "d_prime"
        )
        if row["classification_metric"] != expected_metric:
            raise ValueError(f"classification metric mismatch: {row}")
    return {
        "n_rows": len(rows),
        "domains": domains,
        "zones": zones,
        "specificity_classes": specificities,
        "rows_by_domain": dict(
            Counter(str(row["resolved_domain"]) for row in rows)
        ),
        "rows_by_zone": dict(Counter(str(row["zone"]) for row in rows)),
        "rows_by_specificity": dict(
            Counter(str(row["specificity"]) for row in rows)
        ),
        "unique_species_codes_by_domain": {
            domain: len(
                {
                    str(row["species_code"])
                    for row in rows
                    if row["resolved_domain"] == domain
                }
            )
            for domain in domains
        },
    }


def write_csv(
    path: Path,
    rows: Sequence[Mapping[str, object]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("artifacts/canary_balearic_plos"),
    )
    parser.add_argument(
        "--audit",
        type=Path,
        default=Path("artifacts/canary_balearic_plos/content_audit.json"),
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path(
            "artifacts/canary_balearic_plos/derived_partner_traits.csv"
        ),
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=Path(
            "artifacts/canary_balearic_plos/"
            "derived_partner_traits_summary.json"
        ),
    )
    args = parser.parse_args()

    audit = load_json(args.audit)
    expected_status = (
        "same_four_communities_supported_"
        "derived_species_partner_summaries_only"
    )
    if audit.get("status") != expected_status:
        raise RuntimeError(
            "content audit has not locked the derived-only scope: "
            f"{audit.get('status')!r}"
        )
    if not audit.get("caption_content_role_mismatch_detected"):
        raise RuntimeError("S3/S4 code-domain crosswalk was not resolved")
    roles = audit.get("resolved_content_roles") or {}
    expected = {
        "s003": "flower_visitor_by_month_derived_partner_traits",
        "s004": "plant_by_month_derived_partner_traits",
    }
    if any(roles.get(key) != value for key, value in expected.items()):
        raise RuntimeError(f"unexpected resolved content roles: {roles}")

    rows: list[dict[str, object]] = []
    for logical_id, domain in (
        ("s003", "flower_visitor"),
        ("s004", "plant"),
    ):
        text_path = (
            args.input_dir
            / "text"
            / f"pone.0150824.{logical_id}.doc.txt"
        )
        if not text_path.exists():
            raise FileNotFoundError(text_path)
        rows.extend(
            parse_derived_lines(
                text_path.read_text(encoding="utf-8").splitlines(),
                source_logical_id=logical_id,
                resolved_domain=domain,
            )
        )
    validation = validate_rows(rows)
    write_csv(args.output_csv, rows)
    summary = {
        "schema_version": "1.0",
        "status": "parsed_selected_species_monthly_partner_traits",
        "source_id": audit.get("source_id"),
        "article_doi": audit.get("article_doi"),
        "target_source_id": audit.get("target_source_id"),
        "target_article_doi": audit.get("target_article_doi"),
        **validation,
        "source_role_mismatch_retained": True,
        "raw_interaction_edges_available": False,
        "full_network_matrix_available": False,
        "effect_registry_eligible": False,
        "independent_unit": (
            "selected species x community; monthly rows are repeated "
            "observations and two communities per island do not create "
            "independent geological-origin replicates"
        ),
        "selection_boundary": (
            "Species were deliberately selected from extreme linkage/"
            "selectiveness classes and were required to occur in at least two "
            "temporal networks. These rows do not represent the full plant or "
            "visitor assemblage."
        ),
        "reading": (
            "The recovered package supports selected-species seasonal "
            "partner-trait analyses and source-quality checks. It cannot "
            "reproduce the complete 2014 quantitative networks or supply a "
            "compatible Wanshan-Yongxing plant-level island effect."
        ),
        "claim_boundary": audit.get("claim_boundary"),
    }
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"derived rows: {validation['n_rows']}")
    print(f"rows by domain: {validation['rows_by_domain']}")
    print(args.output_csv)


if __name__ == "__main__":
    main()
