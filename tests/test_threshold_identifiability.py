from channel_id.threshold_identifiability import Regime, classify_profile, run_recovery_audit

REGIMES = (
    Regime("mainland_large_bombus", 0, 0),
    Regime("oshima_ardens", 1, 0),
    Regime("non_oshima", 2, 1),
)


def test_classifier_recovers_clean_shapes() -> None:
    assert classify_profile(REGIMES, (1.0, 1.0, 1.0))[0] == "none"
    assert classify_profile(REGIMES, (1.0, 0.5, 0.0))[0] == "cline"
    assert classify_profile(REGIMES, (1.0, 1.0, 0.0))[0] == "second_step"


def test_recovery_audit_separates_cline_and_step() -> None:
    result = run_recovery_audit(REGIMES, replicates=500, effect_size=1.2, noise_sd=0.35, samples_per_regime=20, seed=7)
    assert result["second_step_recovery_rate"] > 0.80
    assert result["cline_false_second_step_rate"] < 0.20
