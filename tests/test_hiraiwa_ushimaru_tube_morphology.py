import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "predictive_meta" / "hiraiwa_ushimaru_tube_morphology.csv"


def rows():
    with DATA.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_pollen_target_tube_morphology_is_not_a_universal_second_step():
    target = [row for row in rows() if row["plant"] != "Campanula microdonta"]
    directions = [row["second_direction"] for row in target]
    assert directions.count("shorter_post") == 3
    assert directions.count("longer_post") == 4
    assert directions.count("equal") == 1


def test_farfugium_high_interaction_breadth_does_not_mean_morphological_stasis():
    row = next(row for row in rows() if row["plant"] == "Farfugium japonicum")
    assert float(row["oshima_tube_mm"]) == 11.276
    assert abs(float(row["post_mean_tube_mm"]) - 10.339) < 1e-6
    assert float(row["second_delta_mm"]) < -0.9
    assert float(row["second_percent_change_from_oshima"]) < -8.0
    assert row["within_site_uncertainty_available"] == "no"
    assert row["numeric_evidence_grade"] == "B_plus_site_mean_without_variance"
    assert "cannot support equivalence" in row["claim_boundary"]


def test_contemporary_campanula_morphology_reproduces_lower_post_direction_without_shape_identification():
    row = next(row for row in rows() if row["plant"] == "Campanula microdonta")
    assert float(row["oshima_tube_mm"]) > 26.9
    assert float(row["post_mean_tube_mm"]) < 19.5
    assert float(row["second_percent_change_from_oshima"]) < -27.0
    assert row["second_direction"] == "shorter_post"
    assert "lacks Toshima" in row["claim_boundary"]
    assert "cannot distinguish cline" in row["claim_boundary"]


def test_site_means_are_not_promoted_to_A_grade_effect_sizes():
    assert all(row["measurement_n_per_species_site"] == "5" for row in rows())
    assert all(row["within_site_uncertainty_available"] == "no" for row in rows())
    assert all(row["numeric_evidence_grade"] == "B_plus_site_mean_without_variance" for row in rows())
