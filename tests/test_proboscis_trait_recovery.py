import csv
import json
import subprocess
import sys
from pathlib import Path

import pytest

from channel_id.proboscis_trait_recovery import (
    load_status,
    recovery_state,
    validate_recovery_status,
    validate_trait_lookup,
)

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "data/design/izu_pollinator_proboscis_recovery_status.json"
TEMPLATE = ROOT / "templates/field_pollinator_trait_lookup_template.csv"


def test_current_source_state_stays_blocked_without_numeric_table_s2() -> None:
    status = load_status(STATUS)
    validate_recovery_status(status)
    state = recovery_state(status)
    assert state == {
        "current_named_pollinator_taxa": 209,
        "recovered_numeric_proboscis_taxa": 0,
        "coverage_fraction": 0.0,
        "paper_vs_current_count_discrepancy": 2,
        "table_s2_values_recovered": False,
        "fdq_trait_lookup_ready": False,
        "decision": "blocked_until_source_native_proboscis_values_recovered",
    }


def test_blank_field_template_is_valid_and_contains_no_fake_traits() -> None:
    counts = validate_trait_lookup(TEMPLATE)
    assert sum(counts.values()) == 0


def write_lookup(path: Path, rows: list[dict[str, str]]) -> None:
    fields = [
        "visitor_taxon_id",
        "source_taxon_name",
        "site_id",
        "proboscis_length_mm",
        "measurement_n",
        "measurement_source",
        "source_locator",
        "trait_status",
        "source_bundle_sha256",
        "notes",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def test_trait_missing_must_not_hide_numeric_value(tmp_path: Path) -> None:
    path = tmp_path / "lookup.csv"
    write_lookup(path, [{
        "visitor_taxon_id": "x",
        "source_taxon_name": "x",
        "site_id": "oshima",
        "proboscis_length_mm": "8.2",
        "measurement_n": "",
        "measurement_source": "",
        "source_locator": "",
        "trait_status": "trait_missing",
        "source_bundle_sha256": "",
        "notes": "",
    }])
    with pytest.raises(ValueError, match="trait_missing row cannot carry a numeric value"):
        validate_trait_lookup(path)


def test_exact_source_trait_requires_value_n_source_and_locator(tmp_path: Path) -> None:
    path = tmp_path / "lookup.csv"
    write_lookup(path, [{
        "visitor_taxon_id": "Bombus ardens ardens",
        "source_taxon_name": "Bombus ardens ardens",
        "site_id": "oshima",
        "proboscis_length_mm": "",
        "measurement_n": "",
        "measurement_source": "",
        "source_locator": "",
        "trait_status": "source_exact_site",
        "source_bundle_sha256": "",
        "notes": "",
    }])
    with pytest.raises(ValueError, match="requires proboscis_length_mm"):
        validate_trait_lookup(path)


def test_audit_cli_matches_committed_result() -> None:
    subprocess.run([sys.executable, "scripts/audit_izu_proboscis_trait_recovery.py"], cwd=ROOT, check=True)
    result = json.loads((ROOT / "data/results/izu_pollinator_proboscis_recovery_audit.json").read_text())
    assert result["state"] == recovery_state(load_status(STATUS))
