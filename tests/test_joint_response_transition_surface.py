from scripts.run_joint_response_transition_surface import (
    PARAMETER_RANGES,
    build,
    config_from_point,
    latin_hypercube,
)


def test_latin_hypercube_is_deterministic_and_within_declared_ranges():
    first = latin_hypercube(4, 123)
    second = latin_hypercube(4, 123)
    assert first == second
    assert len(first) == 4
    for point in first:
        for name, value in point.items():
            lo, hi = PARAMETER_RANGES[name]
            assert lo <= value <= hi


def test_joint_point_maps_to_valid_config():
    point = {name: (lo + hi) / 2 for name, (lo, hi) in PARAMETER_RANGES.items()}
    cfg = config_from_point(point)
    assert 0.0 <= cfg.mainland.generalist_fraction <= 1.0
    assert 0.0 <= cfg.island.generalist_fraction <= 1.0
    assert cfg.generalist_breadth > cfg.specialist_breadth


def test_small_joint_build_keeps_fail_honest_scope():
    payload = build(points=2, replicates=1, seed=20260826)
    assert payload["status"] == "scientific_reassessment_gate_phase2"
    assert payload["design"]["common_seed_ensemble_across_parameter_points"] is True
    assert payload["design"]["empirical_inputs_loaded"] == []
    assert sum(payload["class_counts"].values()) == 2
    assert "must not be interpreted as natural ecological prevalence" in payload["claim_boundary"]
    assert "do not retune" in payload["failure_rule"].lower()
