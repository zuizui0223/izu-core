import csv
from pathlib import Path

import pytest

from channel_id.izu_comparative_taxon_screen import (
    TAXON_SCREEN_COLUMNS,
    build_izu_comparative_taxon_screen,
    read_izu_comparative_taxon_screen,
    write_izu_comparative_taxon_screen,
)

ROOT = Path(__file__).parents[1]
SCREEN = ROOT / "data" / "izu_comparative_taxon_screen.csv"


def test_initial_screen_keeps_only_campanula_as_ready_independent_contrast(tmp_path: Path) -> None:
    rows = read_izu_comparative_taxon_screen(SCREEN)
    result = build_izu_comparative_taxon_screen(rows)

    assert len(rows) == 5
    assert result.independent_mainland_to_island_ready == 1
    assert result.meta_analysis_status == "not_ready_requires_at_least_three_independent_ready_mainland_to_island_lineages"
    outcomes = {row["taxon_id"]: row["screen_outcome"] for row in rows}
    assert outcomes["campanula_microdonta"] == "core_focal_ready"
    assert outcomes["lilium_platyphyllum"] == "auxiliary_after_distribution_audit"
    assert outcomes["dianthus_japonicus"] == "discovery_only"

    output = tmp_path / "screen"
    write_izu_comparative_taxon_screen(output, result)
    assert (output / "izu_comparative_taxon_screen_summary.csv").exists()
    text = (output / "README.md").read_text(encoding="utf-8")
    assert "Meta-analysis status" in text
    assert "not_ready_requires_at_least_three" in text


def test_discovery_taxon_cannot_claim_island_or_mainland_coverage(tmp_path: Path) -> None:
    rows = read_izu_comparative_taxon_screen(SCREEN)
    changed = [dict(row) for row in rows]
    discovery = next(row for row in changed if row["taxon_id"] == "dianthus_japonicus")
    discovery["mainland_reference_status"] = "documented_external_source"
    path = tmp_path / "bad.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=TAXON_SCREEN_COLUMNS)
        writer.writeheader()
        writer.writerows(changed)

    with pytest.raises(ValueError, match="discovery-only cannot claim mainland or Izu coverage"):
        read_izu_comparative_taxon_screen(path)


def test_izu_only_taxon_is_not_allowed_to_masquerade_as_mainland_contrast(tmp_path: Path) -> None:
    rows = read_izu_comparative_taxon_screen(SCREEN)
    changed = [dict(row) for row in rows]
    auxiliary = next(row for row in changed if row["taxon_id"] == "lilium_platyphyllum")
    auxiliary["comparison_role"] = "prospective_mainland_to_island"
    path = tmp_path / "bad.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=TAXON_SCREEN_COLUMNS)
        writer.writeheader()
        writer.writerows(changed)

    with pytest.raises(ValueError, match="mainland-to-island role cannot be Izu endemic"):
        read_izu_comparative_taxon_screen(path)


def test_exactly_one_pre_field_core_is_required(tmp_path: Path) -> None:
    rows = read_izu_comparative_taxon_screen(SCREEN)
    changed = [dict(row) for row in rows]
    changed[0]["screen_outcome"] = "discovery_only"
    changed[0]["comparison_role"] = "prospective_mainland_to_island"
    changed[0]["taxonomy_status"] = "unreviewed_discovery"
    changed[0]["mainland_reference_status"] = "unverified"
    changed[0]["izu_coverage_status"] = "unverified"
    changed[0]["shared_channel_status"] = "needs_field_reconnaissance"
    changed[0]["pollination_evidence_status"] = "none_verified"
    changed[0]["source_status"] = "discovery_only"
    path = tmp_path / "no_core.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=TAXON_SCREEN_COLUMNS)
        writer.writeheader()
        writer.writerows(changed)

    with pytest.raises(ValueError, match="exactly one core focal taxon"):
        read_izu_comparative_taxon_screen(path)
