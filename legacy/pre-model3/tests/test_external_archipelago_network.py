import math

import pytest

from channel_id.external_archipelago_network import (
    WeightedNetwork,
    exact_two_sided_sign_test,
    morisita_horn_similarity,
    network_metrics,
    shared_plant_contrasts,
    summarize_shared_plant_contrasts,
)


def test_network_metrics_are_transparent_and_drop_empty_axes():
    network = WeightedNetwork.from_rows(
        ["Plant A", "Plant B", "empty"],
        ["Bee", "Fly", "empty"],
        [[2, 0, 0], [1, 1, 0], [0, 0, 0]],
    )
    result = network_metrics(network)
    assert result["n_plants"] == 2
    assert result["n_pollinators"] == 2
    assert result["n_positive_links"] == 3
    assert result["total_visitation_rate"] == 4
    assert result["binary_connectance"] == pytest.approx(0.75)
    assert result["mean_pollinator_richness_per_plant"] == pytest.approx(1.5)


def test_morisita_horn_similarity_has_expected_endpoints():
    assert morisita_horn_similarity([1, 0], [1, 0]) == pytest.approx(1.0)
    assert morisita_horn_similarity([1, 0], [0, 1]) == pytest.approx(0.0)
    assert morisita_horn_similarity([2, 1], [1, 2]) == pytest.approx(0.8)


def test_shared_plant_contrast_aligns_pollinator_labels_not_column_order():
    continental = WeightedNetwork.from_rows(
        ["Species one", "Species two"],
        ["Bee", "Fly"],
        [[4, 1], [2, 2]],
    )
    oceanic = WeightedNetwork.from_rows(
        ["species two", "species one"],
        ["Fly", "Bee", "Moth"],
        [[1, 0, 1], [1, 1, 0]],
    )
    rows = shared_plant_contrasts(continental, oceanic)
    by_name = {row["plant_name"]: row for row in rows}
    first = by_name["Species one"]
    assert first["continental_total_visitation_rate"] == 5
    assert first["oceanic_total_visitation_rate"] == 2
    assert first["continental_pollinator_richness"] == 2
    assert first["oceanic_pollinator_richness"] == 2
    assert first["shared_pollinator_count"] == 2
    assert first["visitation_log_response_ratio"] == pytest.approx(math.log(2 / 5))


def test_sign_test_and_summary_do_not_count_ties():
    assert exact_two_sided_sign_test(7, 0) == pytest.approx(0.015625)
    rows = [
        {
            "continental_total_visitation_rate": 10,
            "oceanic_total_visitation_rate": 5,
            "visitation_log_response_ratio": math.log(0.5),
            "pollinator_richness_difference_oceanic_minus_continental": -1,
            "pollinator_richness_log_response_ratio": math.log(0.5),
            "pollinator_morisita_horn_turnover": 0.4,
        },
        {
            "continental_total_visitation_rate": 8,
            "oceanic_total_visitation_rate": 4,
            "visitation_log_response_ratio": math.log(0.5),
            "pollinator_richness_difference_oceanic_minus_continental": 0,
            "pollinator_richness_log_response_ratio": 0.0,
            "pollinator_morisita_horn_turnover": 0.8,
        },
    ]
    result = summarize_shared_plant_contrasts(rows)
    assert result["visitation_direction_counts"] == {
        "oceanic_lower": 2,
        "oceanic_higher": 0,
        "equal": 0,
    }
    assert result["pollinator_richness_direction_counts"] == {
        "oceanic_lower": 1,
        "oceanic_higher": 0,
        "equal": 1,
    }
    assert result["median_pollinator_morisita_horn_turnover"] == pytest.approx(0.6)
    assert "do not measure" in result["claim_boundary"].lower()


def test_negative_weights_are_rejected():
    with pytest.raises(ValueError, match="non-negative"):
        WeightedNetwork.from_rows(["plant"], ["pollinator"], [[-1]])
