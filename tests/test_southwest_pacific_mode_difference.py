import pytest

from scripts.analyze_southwest_pacific_mode_difference import (
    analyse,
    cluster_bootstrap,
    split,
)


def rows():
    output = []
    for index, (fm, lr, syndrome, island, family) in enumerate(
        [
            (1, 0.30, 1, "A", "F1"),
            (2, 0.10, 1, "A", "F1"),
            (4, -0.10, 1, "B", "F2"),
            (8, -0.30, 1, "C", "F3"),
            (1, 0.05, 0, "A", "F4"),
            (2, 0.03, 0, "B", "F4"),
            (4, 0.01, 0, "C", "F5"),
            (8, -0.01, 0, "C", "F6"),
        ],
        start=1,
    ):
        fi = fm * (10**lr)
        output.append(
            {
                "Pair number": index,
                "FI": fi,
                "FM": fm,
                "LR": lr,
                "Syndrome": syndrome,
                "Island": island,
                "Family": family,
            }
        )
    return output


def test_split_uses_source_coded_pollination_mode_only():
    animal, wind = split(rows())
    assert len(animal) == 4
    assert len(wind) == 4


def test_direct_difference_is_not_inferred_from_separate_significance():
    result = analyse(rows(), repetitions=200)
    assert result["animal_slope"] < result["wind_slope"]
    assert result["animal_minus_wind_slope"] < 0
    assert result["effect_registry_eligible"] is False
    assert result["causal_claim_allowed"] is False
    assert "not effective dependency" in result["claim_boundary"]


def test_shared_cluster_bootstrap_is_deterministic():
    first = cluster_bootstrap(rows(), "Island", 200)
    second = cluster_bootstrap(rows(), "Island", 200)
    assert first == second
    assert first["n_source_clusters"] == 3
    assert first["slope_difference"]["n_valid"] == 200


def test_both_modes_are_required():
    with pytest.raises(ValueError, match="both pollination modes"):
        split([row for row in rows() if row["Syndrome"] == 1])
