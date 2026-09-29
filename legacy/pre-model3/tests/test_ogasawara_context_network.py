from pathlib import Path

import pytest

from channel_id.ogasawara_context_network import (
    analyze_anijima_anole_contrast,
    context_season_metrics,
    validate_rows,
)


def source_row(
    *,
    context: str,
    anole: str,
    plant: str,
    pollinator: str,
    count: float,
    season: str = "MAY",
) -> dict[str, object]:
    return {
        "island": "Anijima",
        "context": context,
        "season": season,
        "forest_status": "Natural",
        "anole": anole,
        "plant": plant,
        "pollinator": pollinator,
        "interaction_count": count,
    }


def toy_rows() -> list[dict[str, object]]:
    rows = [
        source_row(
            context="ANI_A",
            anole="Absence",
            plant="P1",
            pollinator="bee_a",
            count=10,
        ),
        source_row(
            context="ANI_P",
            anole="Presence",
            plant="P1",
            pollinator="fly_a",
            count=5,
        ),
        source_row(
            context="ANI_A",
            anole="Absence",
            plant="P2",
            pollinator="bee_b",
            count=8,
        ),
        source_row(
            context="ANI_P",
            anole="Presence",
            plant="P2",
            pollinator="bee_b",
            count=4,
        ),
        source_row(
            context="ANI_A",
            anole="Absence",
            plant="P3",
            pollinator="bee_a",
            count=4,
        ),
        source_row(
            context="ANI_A",
            anole="Absence",
            plant="P3",
            pollinator="bee_b",
            count=4,
        ),
        source_row(
            context="ANI_P",
            anole="Presence",
            plant="P3",
            pollinator="moth_a",
            count=2,
        ),
        source_row(
            context="ANI_A",
            anole="Absence",
            plant="P0",
            pollinator="No_pollinator",
            count=0,
        ),
    ]
    return rows


def test_source_zero_marker_is_retained_but_not_a_partner():
    rows = validate_rows(toy_rows())
    metrics = context_season_metrics(rows)
    absence = next(row for row in metrics if row["context"] == "ANI_A")
    assert absence["n_zero_marker_rows"] == 1
    assert absence["n_sampled_plants_including_zero_markers"] == 4
    assert absence["n_plants_with_positive_interactions"] == 3
    assert absence["n_pollinators"] == 2


def test_zero_count_requires_source_no_pollinator_label():
    bad = toy_rows()
    bad[-1]["pollinator"] = "bee_a"
    with pytest.raises(ValueError, match="No_pollinator"):
        validate_rows(bad)


def test_anijima_effects_are_numeric_but_context_specific():
    rows = validate_rows(toy_rows())
    result = analyze_anijima_anole_contrast(rows, source_sha256="abc")
    assert result["n_plant_season_contrasts"] == 3
    assert result["n_unique_shared_plants"] == 3
    effects = result["effect_level_uncertainty"]["effects"]
    assert len(effects) == 3
    assert all(effect["n_effect_units"] == 3 for effect in effects)
    assert all(effect["cross_system_model_eligible"] is False for effect in effects)
    assert all(effect["causal_claim_allowed"] is False for effect in effects)
    turnover = next(
        effect
        for effect in effects
        if effect["effect_id"] == "ogasawara_anijima_partner_turnover"
    )
    assert turnover["estimate"] > 0
    assert result["effect_level_uncertainty"]["formal_cross_system_fit_ready"] is False


def test_context_metadata_cannot_change_within_source_label():
    bad = toy_rows()
    bad.append(
        {
            **bad[0],
            "island": "Chichijima",
        }
    )
    with pytest.raises(ValueError, match="inconsistent"):
        validate_rows(bad)
