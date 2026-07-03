"""Tests for the primary-source numeric extraction gate."""
from __future__ import annotations

import csv
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "paper" / "validate_quantitative_effects.py"
SCHEMA = ROOT / "paper" / "evidence_screening" / "quantitative_effects.schema.csv"


def load_module():
    spec = importlib.util.spec_from_file_location("validate_quantitative_effects", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def schema_fields() -> list[str]:
    with SCHEMA.open(encoding="utf-8", newline="") as handle:
        return next(csv.reader(handle))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def queue_row(status: str) -> dict[str, str]:
    return {
        "source_id": "doi:10.test/example", "taxon": "Example plant", "source_citation": "Example",
        "current_synthesis_role": "primary_geographic", "current_evidence_rank": "B",
        "access_state": "full_text", "full_text_state": "transcribed", "reported_comparison_scope": "mainland-island",
        "reported_direction": "reduction", "required_extraction_unit": "trait x population",
        "required_fields_before_numeric_promotion": "all", "promotion_rule": "all", "parent_observation_ids": "",
        "status": status, "next_action": "none", "notes": "",
    }


def effect_row() -> dict[str, str]:
    return {
        "effect_id": "example-001", "source_id": "doi:10.test/example", "synthesis_role": "primary_geographic",
        "taxon_as_reported": "Example plant", "accepted_taxon_concept": "Example plant", "trait_id": "corolla_length",
        "trait_definition": "mean corolla length", "comparison_id": "mainland_vs_island", "comparison_scope": "wild mainland-island populations",
        "mainland_or_reference_unit": "Mainland A", "island_or_focal_unit": "Island B", "island_order": "1",
        "mean_reference": "10", "mean_focal": "5", "variance_type": "sd", "variance_reference": "2", "variance_focal": "1",
        "n_reference": "20", "n_focal": "15", "effect_metric": "lnRR", "effect_value": "-0.693147", "effect_variance": "0.05",
        "page_table_figure": "Table 2, p. 5", "extraction_method": "direct_table_transcription", "unit_compatibility": "yes",
        "taxonomy_verified": "yes", "geography_verified": "yes", "wild_status_verified": "yes",
        "source_verification_status": "source_locked", "notes": "",
    }


def test_repository_gate_accepts_empty_effect_table():
    module = load_module()
    summary = module.validate()
    assert summary["sources"] >= 1
    assert summary["numeric_effects"] == 0


def test_signed_effect_is_accepted_when_source_is_locked(tmp_path: Path):
    module = load_module()
    fields = schema_fields()
    queue_fields = list(queue_row("numeric_extracted"))
    queue = tmp_path / "queue.csv"
    effects = tmp_path / "effects.csv"
    schema = tmp_path / "schema.csv"
    write_csv(queue, queue_fields, [queue_row("numeric_extracted")])
    write_csv(effects, fields, [effect_row()])
    write_csv(schema, fields, [])
    summary = module.validate(queue, schema, effects)
    assert summary == {"sources": 1, "numeric_effects": 1}


def test_effect_is_rejected_while_source_is_not_transcribed(tmp_path: Path):
    module = load_module()
    fields = schema_fields()
    queue_fields = list(queue_row("awaiting_full_text"))
    queue = tmp_path / "queue.csv"
    effects = tmp_path / "effects.csv"
    schema = tmp_path / "schema.csv"
    write_csv(queue, queue_fields, [queue_row("awaiting_full_text")])
    write_csv(effects, fields, [effect_row()])
    write_csv(schema, fields, [])
    with pytest.raises(ValueError, match="lock primary source"):
        module.validate(queue, schema, effects)


def test_effect_requires_page_locator_and_variance(tmp_path: Path):
    module = load_module()
    fields = schema_fields()
    broken = effect_row()
    broken["page_table_figure"] = ""
    broken["effect_variance"] = ""
    queue_fields = list(queue_row("source_locked"))
    queue = tmp_path / "queue.csv"
    effects = tmp_path / "effects.csv"
    schema = tmp_path / "schema.csv"
    write_csv(queue, queue_fields, [queue_row("source_locked")])
    write_csv(effects, fields, [broken])
    write_csv(schema, fields, [])
    with pytest.raises(ValueError, match="missing required fields"):
        module.validate(queue, schema, effects)
