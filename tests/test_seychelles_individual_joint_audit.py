import json
from pathlib import Path

import pytest

from channel_id.seychelles_joint_linkage import build_report, load_joint_rows

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/predictive_meta/seychelles_thespesia_joint_plant.csv"
RESULT = ROOT / "data/results/seychelles_individual_joint_audit.json"
ROWS = load_joint_rows(LEDGER)
REPORT = build_report(ROWS)


def test_exact_id_prefix_linkage_and_joint_coverage() -> None:
    assert len(ROWS) == 8
    assert REPORT["raw_linkage"]["normalized_census_breeding_overlap"] == 12
    assert REPORT["raw_linkage"]["plants_with_census_and_both_auto_xenogamy"] == 8
    assert REPORT["raw_linkage"]["raw_joint_measurement_exact"] is True


def test_species_dependency_is_direct_but_source_scale_only() -> None:
    dependency = REPORT["species_level_direct_dependency"]
    assert dependency["full_species_auto_fruit"] == {
        "successes": 3,
        "n": 39,
        "proportion": pytest.approx(3 / 39),
    }
    assert dependency["full_species_xenogamy_fruit"] == {
        "successes": 15,
        "n": 30,
        "proportion": pytest.approx(0.5),
    }
    assert dependency["dependency_shortfall_one_minus_ratio"] == pytest.approx(0.8461538461538461)


def test_exploratory_joint_diagnostics_do_not_promote_fdq_or_moderation() -> None:
    diagnostics = REPORT["linked_eight_plant_scope"]["association_diagnostics"]
    assert diagnostics["functional_group_shannon"]["spearman_rho"] == pytest.approx(0.05231552474475615)
    assert diagnostics["functional_group_shannon"]["two_sided_exact_permutation_p"] == pytest.approx(0.8964285714285715)
    assert all(value["permutations"] == 40320 for value in diagnostics.values())
    assert REPORT["decision"] == {
        "raw_individual_exposure_dependency_overlap": "identified",
        "harmonized_fdq_like_functional_exposure": "not_identified",
        "within_lineage_dependency_moderation_signal": "not_detected_in_small_exploratory_diagnostic",
        "cross_lineage_dependency_x_functional_exposure": "not_identified",
    }


def test_committed_result_is_reproducible_from_derived_ledger() -> None:
    committed = json.loads(RESULT.read_text(encoding="utf-8"))
    assert REPORT == committed
