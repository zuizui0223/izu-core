#!/usr/bin/env python3
"""Audit PLOS supporting files from the four Canary–Balearic communities.

The audit asks two separate questions:

1. Do the files demonstrably refer to the same four named communities used by
   the 2014 Canary–Balearic comparison?
2. Do they contain complete plant-by-visitor interaction data, or only selected
   species and derived partner-trait summaries?

The first answer must never be used to assume the second.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Sequence


COMMUNITY_CODES = ("SB", "CM", "CB", "LC")
PAIR_TERMS = ("flower visitor", "flower-visitor", "pollinator", "visitor")
WEIGHT_TERMS = ("fvr", "flower visitation rate", "visit frequency", "interaction weight")
DERIVED_TERMS = (
    "linkage level",
    "selectiveness",
    "specificity",
    "partner",
    "functional richness",
    "evenness",
    "rank abundance",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_space(value: str) -> str:
    return " ".join(value.replace("\xa0", " ").split())


def extract_doc(path: Path) -> str:
    commands = (
        ["antiword", "-t", str(path)],
        ["antiword", str(path)],
    )
    errors: list[str] = []
    for command in commands:
        result = subprocess.run(command, capture_output=True, check=False)
        if result.returncode == 0 and result.stdout:
            for encoding in ("utf-8", "cp1252", "latin-1"):
                try:
                    return result.stdout.decode(encoding)
                except UnicodeDecodeError:
                    continue
            return result.stdout.decode("utf-8", errors="replace")
        errors.append(
            f"{' '.join(command)} -> returncode={result.returncode}, "
            f"stderr={result.stderr[:200]!r}"
        )
    raise RuntimeError("; ".join(errors))


def extract_docx(path: Path) -> str:
    from docx import Document

    document = Document(path)
    lines: list[str] = []
    lines.extend(paragraph.text for paragraph in document.paragraphs if paragraph.text.strip())
    for table_index, table in enumerate(document.tables, start=1):
        lines.append(f"[TABLE {table_index}]")
        for row in table.rows:
            lines.append("\t".join(cell.text for cell in row.cells))
    return "\n".join(lines)


def extract_text(path: Path) -> str:
    suffix = path.suffix.casefold()
    if suffix == ".doc":
        return extract_doc(path)
    if suffix == ".docx":
        return extract_docx(path)
    if suffix in {".txt", ".csv", ".tsv"}:
        return path.read_text(encoding="utf-8-sig", errors="replace")
    raise ValueError(f"unsupported supporting-file type: {path}")


def logical_id_from_name(name: str) -> str | None:
    match = re.search(r"(?:^|[._-])(s00[1-9])(?:[._-]|$)", name.casefold())
    return match.group(1) if match else None


def is_number(value: str) -> bool:
    cleaned = value.strip().replace(",", ".")
    if not cleaned:
        return False
    try:
        return math.isfinite(float(cleaned))
    except ValueError:
        return False


def split_fields(line: str) -> list[str]:
    if "\t" in line:
        fields = [normalize_space(value) for value in line.split("\t")]
    else:
        fields = [normalize_space(value) for value in re.split(r"\s{2,}", line.strip())]
    return [field for field in fields if field]


def table_like_lines(lines: Sequence[str]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    for index, line in enumerate(lines, start=1):
        fields = split_fields(line)
        if len(fields) < 3:
            continue
        numeric_after_first = sum(is_number(value) for value in fields[1:])
        output.append(
            {
                "line": index,
                "n_fields": len(fields),
                "numeric_fraction_after_first": (
                    numeric_after_first / max(1, len(fields) - 1)
                ),
                "preview": fields[:12],
            }
        )
    return output


def numeric_matrix_blocks(rows: Sequence[dict[str, object]]) -> list[dict[str, object]]:
    candidates = [
        row
        for row in rows
        if int(row["n_fields"]) >= 4
        and float(row["numeric_fraction_after_first"]) >= 0.7
        and row.get("preview")
        and not is_number(str(row["preview"][0]))
    ]
    blocks: list[list[dict[str, object]]] = []
    current: list[dict[str, object]] = []
    for row in candidates:
        if current and int(row["line"]) != int(current[-1]["line"]) + 1:
            if len(current) >= 3:
                blocks.append(current)
            current = []
        current.append(row)
    if len(current) >= 3:
        blocks.append(current)
    return [
        {
            "start_line": int(block[0]["line"]),
            "end_line": int(block[-1]["line"]),
            "n_rows": len(block),
            "typical_field_count": Counter(
                int(row["n_fields"]) for row in block
            ).most_common(1)[0][0],
            "preview": [row["preview"] for row in block[:3]],
        }
        for block in blocks
    ]


def count_codes(text: str) -> dict[str, int]:
    return {
        code: len(
            re.findall(
                rf"(?<![A-Za-z0-9]){re.escape(code)}(?![A-Za-z0-9])", text
            )
        )
        for code in COMMUNITY_CODES
    }


def candidate_lines(
    lines: Sequence[str], terms: Iterable[str]
) -> list[dict[str, object]]:
    lowered_terms = tuple(term.casefold() for term in terms)
    output = []
    for index, line in enumerate(lines, start=1):
        lowered = line.casefold()
        matched = [term for term in lowered_terms if term in lowered]
        if matched:
            output.append(
                {
                    "line": index,
                    "matched_terms": matched,
                    "text": normalize_space(line)[:500],
                }
            )
    return output[:30]


def has_pairwise_header(lines: Sequence[str]) -> bool:
    for line in lines:
        fields = split_fields(line)
        if len(fields) < 3:
            continue
        lowered = " | ".join(fields).casefold()
        has_plant = "plant" in lowered
        has_visitor = any(term in lowered for term in PAIR_TERMS)
        has_weight = any(term in lowered for term in WEIGHT_TERMS)
        if has_plant and has_visitor and has_weight:
            return True
    return False


def audit_file(
    path: Path,
    *,
    output_dir: Path,
    declared_scope: str | None,
) -> dict[str, object]:
    text = extract_text(path)
    text_dir = output_dir / "text"
    text_dir.mkdir(parents=True, exist_ok=True)
    text_path = text_dir / f"{path.name}.txt"
    text_path.write_text(text, encoding="utf-8")
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    rows = table_like_lines(lines)
    blocks = numeric_matrix_blocks(rows)
    pair_headers = has_pairwise_header(lines)
    code_counts = count_codes(text)
    lowered = text.casefold()
    return {
        "logical_id": logical_id_from_name(path.name),
        "filename": path.name,
        "declared_scope": declared_scope,
        "text_path": str(text_path.relative_to(output_dir)),
        "n_nonempty_text_lines": len(lines),
        "community_code_counts": code_counts,
        "community_codes_present": [
            code for code, count in code_counts.items() if count > 0
        ],
        "contains_fvr_term": any(term in lowered for term in WEIGHT_TERMS),
        "contains_derived_partner_terms": [
            term for term in DERIVED_TERMS if term in lowered
        ],
        "pairwise_interaction_header_candidate": pair_headers,
        "n_table_like_lines": len(rows),
        "numeric_matrix_blocks": blocks,
        "n_numeric_matrix_blocks": len(blocks),
        "content_term_lines": candidate_lines(
            lines,
            (*PAIR_TERMS, *WEIGHT_TERMS, *DERIVED_TERMS, "zone", "month"),
        ),
        "opening_preview": [normalize_space(line)[:500] for line in lines[:20]],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/canary_balearic_plos_source.json"),
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("artifacts/canary_balearic_plos"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/canary_balearic_plos/content_audit.json"),
    )
    args = parser.parse_args()

    config = load_json(args.config)
    source_inventory = load_json(args.input_dir / "source_inventory.json")
    expected_scope = {
        str(row["logical_id"]): str(row.get("declared_scope") or "")
        for row in config.get("expected_files", [])
    }
    audits: list[dict[str, object]] = []
    errors: list[dict[str, str]] = []
    file_paths = sorted(
        path
        for path in (args.input_dir / "files").rglob("*")
        if path.is_file()
        and path.suffix.casefold() in {".doc", ".docx", ".txt", ".csv", ".tsv"}
    )
    for path in file_paths:
        logical_id = logical_id_from_name(path.name)
        try:
            audits.append(
                audit_file(
                    path,
                    output_dir=args.input_dir,
                    declared_scope=expected_scope.get(logical_id or ""),
                )
            )
        except Exception as error:
            errors.append({"file": str(path), "error": repr(error)})

    aggregate_code_counts = {
        code: sum(
            int(row["community_code_counts"].get(code, 0)) for row in audits
        )
        for code in COMMUNITY_CODES
    }
    present_codes = [
        code for code, count in aggregate_code_counts.items() if count > 0
    ]
    raw_pair_candidates = [
        row for row in audits if bool(row["pairwise_interaction_header_candidate"])
    ]
    numeric_matrix_candidates = [
        row for row in audits if int(row["n_numeric_matrix_blocks"]) > 0
    ]
    same_four_communities_supported = set(present_codes) == set(COMMUNITY_CODES)

    if (
        same_four_communities_supported
        and not raw_pair_candidates
        and not numeric_matrix_candidates
    ):
        scope_status = "same_four_communities_supported_but_derived_subset_only"
    elif same_four_communities_supported and (
        raw_pair_candidates or numeric_matrix_candidates
    ):
        scope_status = (
            "same_four_communities_with_raw_network_candidate_manual_mapping_required"
        )
    elif audits:
        scope_status = "supporting_files_recovered_community_identity_incomplete"
    else:
        scope_status = "supporting_file_content_not_readable"

    summary = {
        "schema_version": "1.0",
        "status": scope_status,
        "source_id": config["source_id"],
        "article_doi": config["article_doi"],
        "pmcid": config["pmcid"],
        "target_source_id": config.get("target_source_id"),
        "target_article_doi": config.get("target_article_doi"),
        "source_inventory_status": source_inventory.get("status"),
        "n_supporting_files_audited": len(audits),
        "n_text_extraction_errors": len(errors),
        "aggregate_community_code_counts": aggregate_code_counts,
        "community_codes_present": present_codes,
        "same_four_communities_supported": same_four_communities_supported,
        "n_pairwise_interaction_header_candidates": len(raw_pair_candidates),
        "n_numeric_matrix_candidate_files": len(numeric_matrix_candidates),
        "full_network_source_admitted": False,
        "effect_registry_eligible": False,
        "audits": audits,
        "errors": errors,
        "reading": (
            "The supporting files can establish a lawful cross-source link to the four named communities. "
            "They are not admitted as complete 2014 network matrices unless plant, flower-visitor, interaction-weight, "
            "community and effort fields are jointly source-resolved."
        ),
        "next_gate": (
            "If a raw interaction candidate is present, write an explicit source-specific column and community mapping and compare full-season network totals against the 2014 article. Otherwise retain these files as a derived same-community subset and continue searching for the original matrices."
        ),
        "claim_boundary": config["claim_boundary"],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, default=str) + "\n",
        encoding="utf-8",
    )
    print(f"supporting files audited: {len(audits)}")
    print(f"community codes: {present_codes}")
    print(f"raw pair candidates: {len(raw_pair_candidates)}")
    print(f"numeric matrix candidates: {len(numeric_matrix_candidates)}")
    print(f"status: {scope_status}")


if __name__ == "__main__":
    main()
