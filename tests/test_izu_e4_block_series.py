from __future__ import annotations

import pytest

from scripts.audit_izu_e4_block_series import audit_e4_series


def block(block_id: str, sequence: int, *, site_id: str = "SITE1", duration: str = "60") -> dict[str, str]:
    return {
        "block_id": block_id,
        "population_id": "POP1",
        "island_id": "Oshima",
        "site_id": site_id,
        "taxon": "Campanula microdonta",
        "season_id": "2026_main",
        "predeclared_before_outcomes": "yes",
        "realization_series_id": "SER1",
        "block_sequence": str(sequence),
        "planned_duration_min": duration,
        "e4_scale_role": "rank_confrontation",
    }


def scale(block_id: str, *, ready: str = "true", complete: str = "true", q2: str = "1.5") -> dict[str, str]:
    return {
        "block_id": block_id,
        "effective_service_scale_ready": ready,
        "complete_effectiveness_coverage": complete,
        "effective_service_hill_q2": q2,
    }


def test_two_prespecified_scale_ready_blocks_open_descriptive_stability_only():
    payload = audit_e4_series(
        [block("B1", 1), block("B2", 2)],
        [scale("B1"), scale("B2", q2="2.1")],
    )
    assert payload["summary"]["rank_confrontation_series"] == 1
    assert payload["summary"]["descriptive_stability_ready_series"] == 1
    assert payload["summary"]["outcomes_inspected"] is False
    series = payload["series_rows"][0]
    assert series["rank_confrontation_blocks"] == 2
    assert series["scale_ready_blocks"] == 2
    assert series["descriptive_stability_ready"] is True


def test_incomplete_effectiveness_coverage_does_not_count_as_scale_ready():
    payload = audit_e4_series(
        [block("B1", 1), block("B2", 2)],
        [scale("B1"), scale("B2", complete="false", q2="")],
    )
    series = payload["series_rows"][0]
    assert series["scale_ready_blocks"] == 1
    assert series["descriptive_stability_ready"] is False


def test_series_cannot_mix_sites_after_outcome_blind_assignment():
    with pytest.raises(ValueError, match="mixes site_id"):
        audit_e4_series(
            [block("B1", 1), block("B2", 2, site_id="SITE2")],
            [scale("B1"), scale("B2")],
        )


def test_series_cannot_reuse_block_sequence():
    with pytest.raises(ValueError, match="duplicate block_sequence"):
        audit_e4_series(
            [block("B1", 1), block("B2", 1)],
            [scale("B1"), scale("B2")],
        )


def test_rank_confrontation_block_must_be_predeclared():
    bad = block("B1", 1)
    bad["predeclared_before_outcomes"] = "no"
    with pytest.raises(ValueError, match="must be predeclared"):
        audit_e4_series([bad], [scale("B1")])
