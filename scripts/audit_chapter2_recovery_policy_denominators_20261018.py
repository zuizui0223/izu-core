"""Post-outcome read-only comparison of TWO different recovery denominators.

No biological simulation, no new seeds, no independent confirmation.
The original 18-cell warning/readout is the sole source, and its parent
historic design has 2 crossed founders x 2 visitor histories, not 144 islands.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "docs/audits/CHAPTER2_RECOVERY_MICROPILOT_CI_SOURCE_READOUT_20261018.json"


def compare_readout(readout: dict) -> dict:
    if readout.get("schema") != "chapter2_pollinator_recovery_micro_pilot_ci_log_readout_v1":
        raise ValueError("unexpected exploratory readout")
    if readout["source"]["workflow_run_id"] != 39045405754:
        raise ValueError("wrong original CI source")
    rows = readout["results"]["complete_18_cell_readout"]
    expected = {(t, policy, env, future)
                for t in (10, 30, 45)
                for policy, future in (
                    ("fixed", "continue_historical_policy"),
                    ("evolving", "continue_historical_policy"),
                    ("evolving", "freeze_at_attained_A"),
                )
                for env in ("functional_pollinators_restored", "continued_pollinator_loss")}
    actual = [(r["t"], r["historical_A"], r["service"], r["future_A"]) for r in rows]
    if len(actual) != 18 or set(actual) != expected or len(set(actual)) != 18:
        raise ValueError("missing/duplicate exploratory cells")
    by_key = dict(zip(actual, rows))

    results = []
    for t in (10, 30, 45):
        arm = {}
        for policy in ("fixed", "evolving"):
            future = "continue_historical_policy"
            restored = by_key[(t, policy, "functional_pollinators_restored", future)]
            absent = by_key[(t, policy, "continued_pollinator_loss", future)]
            for row in (restored, absent):
                if (row["N_nested"] != 8 or
                    not 0 <= row["N_unconditional_success"] <= 8 or
                    row["N_high_I_support_closed_states"] > 4 or
                    row["N_eligible"] > row["N_nested"]):
                    raise ValueError("invalid nested source inventory")
                conditional = row["P_regain_conditional"]
                if (conditional is None) != (row["N_eligible"] == 0):
                    raise ValueError("conditional recovery eligibility/mean mismatched")
                if conditional is not None:
                    approx = conditional * row["N_eligible"]
                    if not (0 <= approx <= row["N_eligible"]
                            and abs(approx-round(approx)) < 1e-9):
                        raise ValueError("invalid conditional future event frequency")
            arm[policy] = dict(
                unconditional_high_I_attainment_restored=restored["N_unconditional_success"]/8,
                unconditional_high_I_attainment_no_visitors=absent["N_unconditional_success"]/8,
                eligible_declined_nested_futures=restored["N_eligible"],
                eligible_declined_source_states=restored["N_eligible"]//2,
                conditional_regaining_fraction=restored["P_regain_conditional"],
                occupied_source_genetic_support_closures=restored["N_high_I_support_closed_states"],
            )
        f,e=arm["fixed"],arm["evolving"]
        results.append(dict(
            t=t, historical_policies=arm,
            descriptive_unconditional_historical_A_evolving_minus_fixed=(
                e["unconditional_high_I_attainment_restored"] -
                f["unconditional_high_I_attainment_restored"]),
            descriptive_conditional_evolving_minus_fixed=(
                e["conditional_regaining_fraction"] -
                f["conditional_regaining_fraction"]
                if e["conditional_regaining_fraction"] is not None
                and f["conditional_regaining_fraction"] is not None
                else None),
        ))
    return dict(
        status="READ_ONLY_POST_OUTCOME_DENOMINATOR_AUDIT_NOT_CONFIRMATORY",
        source_run_id=readout["source"]["workflow_run_id"],
        statistical_independence="2 founders x 2 visitor histories crossed; nested future streams",
        results=results,
        inference_limits=[
            "Unconditional high-I attainment includes states that never declined, so is not per se regaining after decline.",
            "Conditional regaining selects on surviving and declined states after historical A assignment, not a randomized policy estimand.",
            "A historical A effect is not confirmed with 4 crossed founder/visitor cells; neither point difference is a powered causal estimate.",
            "Original restored-versus-no-visitor demographic RNG seeds differ by environmental arm; ecological comparison is NOT common-RNG paired.",
            "No clinical, field, natural-island, t-star or independent source replication inference.",
            "All original historical Q1–Q4 and the previous 144-path pilot outcomes remain unchanged.",
        ],
    )


def main() -> None:
    result=compare_readout(json.loads(INPUT.read_text(encoding="utf-8")))
    print(json.dumps(result,sort_keys=True,indent=2,allow_nan=False))


if __name__ == "__main__":
    main()
