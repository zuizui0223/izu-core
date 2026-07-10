import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read_rows(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_lilium_full_text_is_extracted_but_not_primary_holdout():
    queue = read_rows(ROOT / "data/predictive_meta/primary_source_extraction_queue.csv")
    row = next(item for item in queue if item["source_id"] == "lilium_nakajima_2018")
    assert "full text extracted" in row["current_status"]
    assert "non-Bombus" in row["blocking_item"]
    assert "do not pool" in row["do_not_infer"].lower()


def test_lilium_extraction_keeps_all_rows_out_of_primary_holdout():
    rows = read_rows(ROOT / "data/predictive_meta/lilium_nakajima_2018_source_extraction.csv")
    assert rows
    assert {row["primary_holdout_eligible"] for row in rows} == {"no"}
    assert any(row["trait_id"] == "seed_set_by_daypart" for row in rows)
    assert any(row["trait_id"] == "floral_scent_timing" for row in rows)
    assert any(row["trait_id"] == "effective_pollinator_guild" for row in rows)
    assert any(row["trait_id"] == "primary_holdout_eligibility" for row in rows)


def test_lilium_registry_is_contextual_and_excluded_from_scorer():
    rows = [
        row for row in read_rows(ROOT / "data/predictive_meta/primary_source_native_evidence.csv")
        if row["source_id"] == "lilium_nakajima_2018"
    ]
    assert rows
    assert {row["analysis_group"] for row in rows} == {"excluded"}
    assert {row["scoring_status"] for row in rows} == {"contextual_alternative_mechanism"}
    assert all("Bombus" not in row["claim"] for row in rows)


def test_descriptive_flower_ranges_are_not_promoted_to_effect_sizes():
    rows = read_rows(ROOT / "data/predictive_meta/lilium_nakajima_2018_source_extraction.csv")
    size_rows = [row for row in rows if row["trait_family"] == "floral_size"]
    assert size_rows
    assert all(row["project_role"] == "context_only" for row in size_rows)
    assert all("not" in row["boundary"].lower() for row in size_rows)
