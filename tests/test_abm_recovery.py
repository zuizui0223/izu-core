import random

import pytest

from channel_id.abm_recovery import (
    ObservationDesign,
    classify_features,
    extract_features,
    observe_features,
    run_recovery_benchmark,
)
from channel_id.virtual_izu_abm import run_abm


def test_extract_and_degrade_features():
    result = run_abm(scenario="pollinator_regime", generations=8, founders=30, seed=4)
    features = extract_features(result)
    assert "global.log_population" in features
    assert any(key.endswith("specialization") for key in features)
    observed = observe_features(
        features,
        design=ObservationDesign(island_fraction=0.5, missing_rate=0.1, measurement_sd=0.02),
        rng=random.Random(3),
    )
    assert observed
    assert len(observed) <= len(features)


def test_transparent_classifier_prefers_matching_centroid():
    observed = {"x": 0.1, "y": 0.2}
    centroids = {"a": {"x": 0.0, "y": 0.0}, "b": {"x": 5.0, "y": 5.0}}
    result = classify_features(observed, centroids, {"x": 1.0, "y": 1.0})
    assert result["predicted"] == "a"
    assert result["classification_margin"] > 0


def test_small_recovery_benchmark_returns_matrix():
    result = run_recovery_benchmark(
        scenarios=("environment_only", "pollinator_regime"),
        reference_replicates=2,
        test_replicates=2,
        generations=6,
        founders=25,
        seed=8,
    )
    assert 0 <= result["overall_accuracy"] <= 1
    assert set(result["recovery_matrix"]) == {"environment_only", "pollinator_regime"}
    assert len(result["records"]) == 4


def test_invalid_observation_design_rejected():
    with pytest.raises(ValueError):
        ObservationDesign(island_fraction=0).validate()
