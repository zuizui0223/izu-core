from channel_id.confounding import (
    SiteConfoundingDesign,
    benchmark_site_confounding,
)


def test_site_confounding_creates_a_false_pooled_guide_visit_association() -> None:
    summary = benchmark_site_confounding(
        SiteConfoundingDesign(
            site_count=24,
            individuals_per_site=25,
            baseline_visit_rate=3.0,
            guide_site_slope=0.18,
            visit_site_log_slope=0.5,
            within_site_guide_sd=0.12,
        ),
        repetitions=300,
        seed=20260629,
    )

    # The data generator contains no individual-level guide effect.  The pooled
    # slope is positive only because guide means and visits share site quality.
    assert summary.mean_pooled_slope > 1.0
    assert summary.pooled_positive_rate > 0.95
    assert abs(summary.mean_within_site_slope) < 0.15
