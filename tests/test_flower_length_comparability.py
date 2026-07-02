from pathlib import Path

from channel_id.flower_length_comparability import build_flower_length_sets, load_flower_length_metadata
from channel_id.island_source_level import load_source_level_evidence

ROOT = Path(__file__).parents[1]
FLOWER = ROOT / "data" / "two_breakpoint_evidence" / "inoue1995_flower_length.csv"


def _evidence():
    return load_source_level_evidence(
        island_summary_path=ROOT / "data" / "inoue_literature_island_traits.csv",
        outcrossing_path=ROOT / "data" / "two_breakpoint_evidence" / "inoue1990_outcrossing.csv",
        bagging_path=ROOT / "data" / "two_breakpoint_evidence" / "inoue1988_bagging.csv",
        flower_path=FLOWER,
    )


def test_metadata_retains_distinct_kiyosumi_and_nikko_rows_after_mainland_mapping() -> None:
    metadata = load_flower_length_metadata(FLOWER)
    honshu = [row for row in metadata if row.island_id == "Honshu"]

    assert len(honshu) == 2
    assert {row.experiment_id for row in honshu} == {"tokyo_experiment", "nikko_experiment"}
    assert {row.mean_mm for row in honshu} == {46.66, 49.91}


def test_declared_sets_remove_only_noncomparable_or_low_n_rows() -> None:
    sets = {row.set_id: row for row in build_flower_length_sets(_evidence(), FLOWER)}

    assert len(sets["legacy_all_rows"].evidence.flower) == 6
    assert len(sets["within_experiment_comparable"].evidence.flower) == 5
    assert "Honshu:49.91" in sets["within_experiment_comparable"].excluded_labels
    assert len(sets["within_experiment_n_ge_10"].evidence.flower) == 4
    assert "Niijima:28.62" in sets["within_experiment_n_ge_10"].excluded_labels
    assert len([name for name in sets if name.startswith("leave_one_comparable_row_out:")]) == 5


def test_leave_one_sets_each_drop_exactly_one_comparable_row() -> None:
    sets = [row for row in build_flower_length_sets(_evidence(), FLOWER) if row.set_id.startswith("leave_one_comparable_row_out:")]

    assert all(len(row.evidence.flower) == 4 for row in sets)
    assert all(row.excluded_labels[-1] == "Honshu:49.91" for row in sets)
    assert len({row.set_id for row in sets}) == 5
