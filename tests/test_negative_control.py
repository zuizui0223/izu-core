from channel_id.negative_control import (
    Contrast,
    analyse_negative_control,
    classify_effect,
    leave_one_lineage_out,
    precision_multiplier_audit,
    simulate_refutation_power,
)


def rows():
    return (
        Contrast("s1", "specialist", "length", 10.0, 8.5, 0.2, 0.2, "bombus_loss", "p1"),
        Contrast("g1", "generalist", "length", 10.0, 10.0, 0.1, 0.1, "bombus_loss", "p1"),
        Contrast("s2", "specialist", "width", 6.0, 5.0, 0.15, 0.15, "bombus_loss", "p2"),
        Contrast("g2", "generalist", "width", 6.0, 6.0, 0.1, 0.1, "bombus_loss", "p2"),
    )


def test_equivalence_is_not_non_significance():
    assert classify_effect(rows()[1], equivalence_margin=0.5)["status"] == "equivalent"


def test_specialist_generalist_interaction():
    result = analyse_negative_control(rows(), equivalence_margin=0.5)
    assert result["group_summary"]["specialist"]["changed"] == 2
    assert result["group_summary"]["generalist"]["equivalent"] == 2
    assert result["specialist_minus_generalist"]["effect"] < 0


def test_refutation_power_returns_rates():
    result = simulate_refutation_power(
        rows(), equivalence_margin=0.5,
        specialist_effect=-1.2, generalist_effect=0.0,
        replicates=100, seed=1,
    )
    assert abs(sum(result["rates"].values()) - 1.0) < 1e-12
    assert result["rates"]["supports_selective_response"] > 0.5


def test_leave_one_lineage_out_preserves_sign():
    result = leave_one_lineage_out(rows(), equivalence_margin=0.5)
    assert result["sign_stable"] is True
    assert len(result["estimates"]) == 4


def test_precision_audit_improves_support():
    result = precision_multiplier_audit(
        rows(), equivalence_margin=0.5,
        specialist_effect=-1.0, generalist_effect=0.0,
        multipliers=(1.0, 0.5), replicates=300,
    )
    assert result[1]["approximate_sample_size_multiplier"] == 4.0
    assert result[1]["rates"]["supports_selective_response"] >= result[0]["rates"]["supports_selective_response"]
