from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/audit_cabrera_2025_reconstruction_structure.py"


def test_structure_audit_is_checksum_locked_and_target_free():
    text = SCRIPT.read_text().lower()
    assert "399ec11ae6ce18c8e9ebb050857ca7c1da4cb4a7858e24382750a92ae5e16a07" in text
    assert "from channel_id.external_archipelago_network" not in text
    assert "network_metrics(" not in text
    assert "interaction_shannon" not in text
    assert "morisita_horn_similarity(" not in text
    assert '"target_metrics_calculated": false' in text
    assert '"network_matrices_built": false' in text


def test_source_native_fields_are_audited_before_reconstruction_freeze():
    text = SCRIPT.read_text()
    for field in (
        '"visita"',
        '"censo"',
        '"COMMUNITY"',
        '"habitat"',
        '"Plant sp"',
        '"Pollinator"',
        '"N ind"',
        '"N visit flowers"',
        '"Method"',
    ):
        assert field in text


def test_audit_checks_method_coverage_zero_structure_and_identity_collisions():
    text = SCRIPT.read_text()
    assert "community_coverage_by_visit" in text
    assert "blank_pollinator_row_count" in text
    assert "nonblank_pollinator_labels_with_zero_n_ind" in text
    assert "variant_collision_count" in text
    assert "habitat_by_community" in text
