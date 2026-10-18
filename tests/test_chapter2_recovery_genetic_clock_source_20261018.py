"""Exact same-seed 8-history genetic-access source audit, not new biology."""
import json
import warnings

from scripts.audit_chapter2_recovery_genetic_clock_20261018 import (
    replay_original_historical_clock,
)


def test_source_only_8_history_genotype_upper_support_clock_and_snapshot_identity():
    result = replay_original_historical_clock()
    assert result["status"] == "POST_OUTCOME_SOURCE_ONLY_SAME_SEED_REPLAY_NOT_CONFIRMATORY"
    assert result["new_unique_random_streams"] == 0
    assert result["new_pollinator_restoration_futures"] == 0
    assert result["historical_policy_paths"] == 8
    assert result["independent_crossed_founder_visitor_cells"] == 4
    assert result["imposed_functional_pollinator_extirpation_TE"] == 35
    assert result["by_historical_assurance_policy"]["fixed"]["strict_support_losses_by_t45"] == 0
    assert result["by_historical_assurance_policy"]["evolving"]["strict_support_losses_by_t45"] == 1
    for row in result["histories"]:
        series = row["series"]
        assert len(series) == 46
        assert [s["t"] for s in series] == list(range(46))
        target = row["founder_mean_I_target"]
        closed = False
        last_values = None
        for s in series:
            if s["census"] > 0:
                assert s["max_retained_I_allele"] >= s["mean_I"] - 1e-12
                values=set(s["retained_I_allele_values"])
                assert s["number_retained_I_allele_values"] == len(values)
                assert s["I_allele_copy_variance"] >= 0
                assert s["I_expressed_population_variance"] >= 0
                if last_values is not None:
                    assert values <= last_values
                last_values=values
                if s["high_I_founder_mean_structurally_closed"]:
                    assert s["max_retained_I_allele"] < target
                    closed = True
                if closed:
                    assert s["high_I_founder_mean_structurally_closed"]
            else:
                assert s["high_I_founder_mean_structurally_closed"] is None
    # Log a compact source-only receipt; verify agreement across the three
    # Python CI versions before accepting its numeric values.
    summary = {
        "source_mode": result["status"],
        "TE": result["imposed_functional_pollinator_extirpation_TE"],
        "by_policy": result["by_historical_assurance_policy"],
        "first_loss_by_historical_path": [
            {
                "founder_index": r["founder_index"],
                "visitor_history_index": r["visitor_history_index"],
                "historical_A": r["historical_A"],
                "first_high_I_support_loss": r["first_strict_high_I_loss_while_occupied"],
                "first_extinction": r["first_extinction"],
                "precedes_TE": r["structural_loss_precedes_imposed_TE"],
            } for r in result["histories"]
        ],
        "source_sha256": result["source_sha256"],
        "auditor_sha256": result["auditor_sha256"],
        "loss_genotype_environment_snapshots": [
            {
                "founder_index": r["founder_index"],
                "visitor_history_index": r["visitor_history_index"],
                "historical_A": r["historical_A"],
                "target_I": r["founder_mean_I_target"],
                "first_loss_t": r["first_strict_high_I_loss_while_occupied"],
                "snapshots": [r["series"][t] for t in (35, 38, 39, 45)],
            }
            for r in result["histories"]
            if r["first_strict_high_I_loss_while_occupied"] is not None
        ],
    }
    warnings.warn("Q2_SAME_SEED_HISTORICAL_GENETIC_CLOCK=" + json.dumps(
        summary, sort_keys=True, separators=(",", ":"), allow_nan=False), stacklevel=1)
