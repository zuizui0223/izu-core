import csv
from pathlib import Path

from paper.compile_blind_photo_scores import compile_sheet


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)


def test_compile_joins_only_eligible_blind_score(tmp_path: Path):
    manifest = tmp_path / "manifest.csv"
    blind = tmp_path / "blind.csv"
    key = tmp_path / "key.csv"
    write_csv(manifest, [
        "taxon", "analysis_group", "group_confidence", "trait_id", "trait_family",
        "trait_definition_id", "trait_definition", "requires_interior_visible", "minimum_score",
        "maximum_score", "analysis_partition",
    ], [{
        "taxon": "Example", "analysis_group": "generalist", "group_confidence": "high",
        "trait_id": "signal", "trait_family": "visible_signal", "trait_definition_id": "signal_0_3",
        "trait_definition": "test", "requires_interior_visible": "no", "minimum_score": "0",
        "maximum_score": "3", "analysis_partition": "holdout",
    }])
    write_csv(blind, [
        "card_id", "image_url", "flowering_state_open_closed_fruit_vegetative_unclear",
        "focal_flower_visible_yes_no_unclear", "interior_visible_yes_no_na",
        "comparable_for_predeclared_trait_yes_no", "trait_definition_id", "trait_score_if_eligible", "reviewer_notes",
    ], [
        {"card_id": "one", "image_url": "x", "flowering_state_open_closed_fruit_vegetative_unclear": "open", "focal_flower_visible_yes_no_unclear": "yes", "interior_visible_yes_no_na": "na", "comparable_for_predeclared_trait_yes_no": "yes", "trait_definition_id": "signal_0_3", "trait_score_if_eligible": "2", "reviewer_notes": "ok"},
        {"card_id": "two", "image_url": "x", "flowering_state_open_closed_fruit_vegetative_unclear": "fruit", "focal_flower_visible_yes_no_unclear": "yes", "interior_visible_yes_no_na": "na", "comparable_for_predeclared_trait_yes_no": "no", "trait_definition_id": "", "trait_score_if_eligible": "", "reviewer_notes": "exclude"},
    ])
    write_csv(key, ["card_id", "region", "obs_id"], [
        {"card_id": "one", "region": "Oshima", "obs_id": "11"},
        {"card_id": "two", "region": "Hachijo", "obs_id": "12"},
    ])
    rows, counts = compile_sheet(blind, key, manifest, "Example")
    assert counts == {"cards_total": 2, "eligible": 1, "scored": 1, "excluded": 1}
    assert rows[0]["pollinator_regime"] == "ardens"
    assert rows[0]["value"] == "2"
