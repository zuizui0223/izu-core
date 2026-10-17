"""Read-only source-arithmetic reconciliation for the Chapter 2 paper.

This audits published repository receipts, not stochastic raw trajectories.
It runs no biological model, changes no registered estimand, and does not
constitute an independent reproduction of the original simulation.
The pinned Git blob SHA-1 values protect exact source-text identity.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SOURCES = {
    "q1": ("data/results/chapter2_assurance_generality_20261006.json",
           "4d390b4fb1a5d05c3bf58ea3aee2b1251cf945a3"),
    "sequence": ("data/results/chapter2_1005_confirmatory_replication_20261006.json",
                 "4537b82ba08f2a89f362cb9e5a6a395384af8db1"),
    "q2": ("docs/audits/CHAPTER2_Q2_I_SUPPORT_384_ORIGINAL_READOUT_20261016.json",
           "003d243de204556b6484bb549ab354c7d7859f07"),
    "q3": ("data/results/directional_access_20261013/READOUT.json",
           "36aa40f63506313cbdb9c110f91f760df344bd0c"),
    "q4": ("data/results/chapter2_island_demographic_independent32_20261008.json",
           "5c46c3c3a1a0f02c9526b265590fc6a6de54005c"),
    "evidence": ("docs/CHAPTER2_TWO_PROPOSITION_EVIDENCE_RECEIPT_20261016.json",
                 "c62ced9df7962de456f40450af13adfde65bb2a0"),
}
MANUSCRIPT = "docs/CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md"
MANUSCRIPT_BLOB = "6bd3afbb93806377de1c0d8274ea5d8d00226251"


class EvidenceMismatch(ValueError):
    """A frozen result, cross-channel arithmetic or manuscript boundary differs."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise EvidenceMismatch(message)


def same(a: float, b: float, name: str, tolerance: float = 1e-12) -> None:
    require(abs(float(a) - float(b)) <= tolerance, name + " does not reconcile")


def blob_sha(raw: bytes) -> str:
    """Git blob SHA-1, NOT a data-file SHA-256."""
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def read_sources(root: Path = ROOT, *, check_identity: bool = True):
    documents = {}
    observed_sha = {}
    for name, (relpath, pin) in SOURCES.items():
        raw = (root / relpath).read_bytes()
        sha = blob_sha(raw)
        if check_identity:
            require(sha == pin, f"Frozen source changed: {relpath}")
        documents[name] = json.loads(raw)
        observed_sha[name] = sha
    original_paper = (root / MANUSCRIPT).read_bytes()
    if check_identity:
        require(blob_sha(original_paper) == MANUSCRIPT_BLOB, "Original paper changed")
    return documents, original_paper.decode("utf-8"), observed_sha


def reconcile(root: Path = ROOT, *, check_identity: bool = True) -> dict:
    d, paper, hashes = read_sources(root, check_identity=check_identity)
    q1, seq, q2, q3, q4, ev = (d[k] for k in
                                    ("q1", "sequence", "q2", "q3", "q4", "evidence"))

    # Q1: the primary contrast is algebraically a difference of arm contrasts,
    # not a causal mediation percentage. Historical repeats are nested.
    require(q1["declared_cases"] == 8448, "Original Q1 case inventory")
    require(q1["independent_visitor_histories"] == 64, "Q1 independent unit")
    require(q1["nested_demographic_repeats"] == 8, "Q1 nested repeats")
    require(q1["adjudication"]["status"] == "all_four_confirmed", "Original Q1 decision")
    require(len(q1["settings"]) == 4, "Expected all four mating conditions")
    q1_rows = []
    for row in q1["settings"]:
        f = row["fixed_far_minus_near"]
        e = row["evolving_far_minus_near"]
        recorded = row["attenuation_evolving_minus_fixed"]
        derived = e["mean"] - f["mean"]
        same(derived, recorded["mean"], "Q1 difference-in-differences")
        require(f["bootstrap95"][1] < 0, "Fixed-A far-near interval not negative")
        require(recorded["bootstrap95"][0] > 0, "Original compression interval not positive")
        require(row["passes_frozen_rule"] is True, "Original Q1 all-four rule")
        q1_rows.append({"setting": row["setting"], "derived_D": derived,
                        "registered_D": recorded["mean"]})
    require(len({r["setting"] for r in q1_rows}) == 4, "Duplicate Q1 setting")

    # The 51/64 threshold chronology is a separate registered cohort, NOT a
    # same-history mediation experiment. The counterfactual fixes A expression
    # at 0.5, rather than preventing self-fertilization.
    sequence = seq["primary_sequence"]
    require(sequence["setting"] == "assurance_cost", "Wrong sequence mating context")
    same(sequence["threshold"], 0.05, "Q2 response threshold")
    require(sequence["counts"]["assurance_first"] == 51
            and sum(sequence["counts"].values()) == 64, "Original sequence categories")
    prior = [r for r in seq["threshold_sensitivity"]
             if r["setting"] == "prior_selfing"
             and r["mutation_rate"] == 0.01 and r["threshold"] == 0.05]
    require(len(prior) == 1 and prior[0]["counts"]["assurance_first"] == 30,
            "Prior-selfing negative/heterogeneity control")
    fresh = ev["fresh_founder_q1"]["settings"]
    require(len(fresh) == 4, "Fresh-founder Q1 inventory")
    require(all(r["negative_fixed_founder_means"] == 8
                and r["fixed_far_change_bootstrap95"][1] < 0
                for r in fresh), "Fresh-founder fixed-A counterexample")

    # Q2: derive the two co-primary point estimates using the published
    # ORIGINAL six-category source cells, not a downstream narrative sentence.
    require(q2["original_run"]["original_cases"] == 384, "Q2 case inventory")
    require(q2["original_run"]["crossed_founder_labels"] == 8
            and q2["original_run"]["crossed_visitor_history_labels"] == 8,
            "Q2 crossed independent axes")
    require(q2["registered_inference"]["result"] == "both_inconclusive",
            "Q2 predeclared result was not supported")
    far = q2["original_six_class_cells"]["far"]
    dense, sparse, impossible = (far[k] for k in
                                ("dense_reachable", "sparse_reachable", "dense_unreachable"))
    for arm in (dense, sparse, impossible):
        require(sum(arm["counts"]) == 64, "Q2 complete six-category count")
    order_difference = ((dense["counts"][0] - dense["counts"][1])
                        - (sparse["counts"][0] - sparse["counts"][1])) / 64
    event_difference = (dense["I_events"] - sparse["I_events"]) / 64
    effects = q2["coprimary"]
    for name, value in (("carrier_order_score_delta", order_difference),
                        ("carrier_I_event_delta", event_difference)):
        original = effects[name]
        same(value, original["estimate"], "Q2 " + name)
        lower, upper = original["simultaneous_familywise_CI"]
        require(lower < 0 < upper and original["excludes_zero"] is False,
                "Q2 simultaneous CI/exclusion status cannot be promoted")
    change = q2["far_within_paired_I_event_transition_counts"]
    require(sum(change[k] for k in ("both_absent", "gained_in_dense",
                                   "lost_in_dense", "both_present")) == 64,
            "Q2 matched transitions not exhaustive")
    require(change["gained_in_dense"] + change["both_present"] == dense["I_events"]
            and change["lost_in_dense"] + change["both_present"] == sparse["I_events"],
            "Q2 matched net effect differs")
    require(impossible["I_events"] == 0, "Structural no-access control")

    # Q3: condition on the genetic-support definition. There is no I-locus
    # mutation/immigration in this original source, so S(t+1) is a subset of
    # S(t); we do NOT call a selected 315/1238 count a population risk.
    require(q3["cases"] == 2304 and len(q3["cells"]) == 18,
            "Original Q3 source case inventory")
    for k in ("cases", "excluded_before_fixation", "excluded_at_fixation"):
        same(sum(cell[k] for cell in q3["cells"]), q3[k], "Q3 cell total " + k)
    require(q3["excluded_before_fixation"] == 703
            and q3["excluded_before_fixation"] + q3["excluded_at_fixation"] == q3["ever_excluded"],
            "Q3 selected allele support")
    source_support = ev["support_loss"]
    require(source_support["cases"] == 2304
            and source_support["excluded_before_fixation"] == 703
            and source_support["first_exclusion_transitions"] == 1238
            and source_support["conditional_expected_low_I_allele_frequency_favouring_but_realized_zero"] == 315,
            "Cross-receipt Q3 genomic counts")

    # Q4: the pooled interaction is the equal-four-setting average within
    # the separately registered stress cohort. Never pool its 4096 futures
    # with Q1/Q2/Q3 independent units.
    require(q4["independent_histories"] == 32
            and q4["post_switch_trajectories"] == 4096,
            "Q4 source inventory")
    q4rows = q4["per_setting"]
    require(len(q4rows) == 4 and len({r["setting"] for r in q4rows}) == 4,
            "Four nonduplicate Q4 settings")
    average = sum(row["interaction"] for row in q4rows) / 4
    same(average, q4["predeclared_pooled_primary"]["mean"], "Q4 pooled interaction")
    require(q4["predeclared_pooled_primary"]["pass"] is True
            and q4["predeclared_pooled_primary"]["bootstrap95"][0] > 0,
            "Registered Q4 pooled positive effect")
    prior_q4 = next(r for r in q4rows if r["setting"] == "prior_selfing")
    require(prior_q4["bootstrap95"][0] < 0 < prior_q4["bootstrap95"][1],
            "Q4 prior-selfing-specific uncertainty")

    # A narrow claim-preservation smoke check, NOT linguistic proof that all
    # 5000 paper words are scientifically valid.
    for phrase in ("51/64", "384-path", "Both co-primary intervals included zero",
                   "703/2,304", "A evolvability **continued during the future**",
                   "not a natural mediation analysis"):
        require(phrase in paper, f"Original manuscript missing scope guard: {phrase}")

    return {
        "status": "PASS_SOURCE_ARITHMETIC_ONLY",
        "main_commit_reviewed": "3a5443a2c5360b6f3b894809ded58aa004584ec2",
        "read_only": True,
        "new_biological_runs": 0,
        "independent_raw_genome_replay": False,
        "source_git_blob_sha1": hashes,
        "checks": {
            "q1": {"old_settings": 4, "old_source_cases": 8448,
                   "fresh_founder_fixed_A_negative_settings": 4,
                   "fresh_founder_compression_supported": 3,
                   "did": q1_rows},
            "sequence": {"assurance_first": 51, "visitor_histories": 64,
                         "prior_selfing_assurance_first": 30,
                         "evolving_A_blocked_still_selfs": True},
            "q2": {"source_cases": 384,
                   "order_score_from_original_categories": order_difference,
                   "I_event_from_original_counts": event_difference,
                   "both_coprimary": "INCONCLUSIVE",
                   "matched_gain": change["gained_in_dense"],
                   "matched_loss": change["lost_in_dense"]},
            "q3": {"original_histories": 2304,
                   "pre_fixation_support_losses": 703,
                   "loss_selected_expected_gain_but_absent": 315,
                   "conditioned_transitions": 1238},
            "q4": {"independent_histories": 32, "futures": 4096,
                   "mean_from_four_settings": average,
                   "preregistered_interval": q4["predeclared_pooled_primary"]["bootstrap95"]},
        },
        "limits": [
            "Not an independent stochastic re-run, genomic archive audit or causal mediation identification",
            "Fixed A means capacity evolution disabled at A=0.5; selfing remains",
            "Two-way Q2 confidence intervals still include zero",
            "Q3 access monotonicity requires no mutation/immigration at investment locus",
            "Q4 simulated postshock stress interaction is not natural-island rescue",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--no-blob-pins", action="store_true",
                        help="For synthetic adversarial tests only; not source admission.")
    args = parser.parse_args()
    output = reconcile(args.repo_root, check_identity=not args.no_blob_pins)
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
