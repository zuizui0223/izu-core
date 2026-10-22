"""Read-only Chapter 2 computational Reporting Summary preflight.

No biological populations are generated, no study is reanalysed for p-values,
and no deposit/DOI rights are inferred from tracked metadata.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "fresh_design": "data/design/chapter2_q1_fresh_founder_generality_20261016.json",
    "fresh_receipt": "docs/CHAPTER2_TWO_PROPOSITION_EVIDENCE_RECEIPT_20261016.json",
    "baseline_design": "docs/protocols/CHAPTER2_BASELINE_POLLEN_LIMIT_2X2_FROZEN_20261019.json",
    "baseline_results": "docs/audits/CHAPTER2_BASELINE_POLLEN_384_AUDIT_20261019.json",
    "matched_repeat": "docs/audits/CHAPTER2_MATCHED_AI_REPEATABILITY_20261019.json",
    "prediction": "docs/audits/CHAPTER2_FOUNDER_PREDICTABILITY_20261021.json",
    "registered_plan": "docs/protocols/CHAPTER2_CONFIRM160_EXECUTION_20261019.json",
    "registered_result": "docs/audits/CHAPTER2_CONFIRM160_COMPACT_RESULTS_20261019.json",
    "original_assets": "docs/audits/CHAPTER2_CONFIRM160_ASSET_SHA256_20261019.json",
    "q2_null": "docs/audits/CHAPTER2_Q2_I_SUPPORT_384_ORIGINAL_READOUT_20261016.json",
    "transfer": "docs/audits/CHAPTER2_READAPTATION_DESCRIPTIVE_TABLES_20261019.json",
    "transfer_audit": "docs/audits/CHAPTER2_READAPTATION_INDEPENDENT_AUDIT_20261019.json",
    "secondary": "docs/audits/CHAPTER2_SECONDARY_COLONIZATION_PEDIGREE_VERIFIED_20261020.json",
}
SUMMARY = "docs/CHAPTER2_R1_R5_COMPUTATIONAL_REPORTING_SUMMARY_20261022.md"


def demand(ok: bool, detail: str) -> None:
    if not ok:
        raise ValueError("R1-R5 reporting admission: " + detail)


def verify(root: Path = ROOT) -> dict:
    root = Path(root)
    files = {}
    digest = {}
    for key, rel in SOURCES.items():
        raw = (root / rel).read_bytes()
        files[key] = json.loads(raw)
        digest[rel] = sha256(raw).hexdigest()

    q1, receipt = files["fresh_design"], files["fresh_receipt"]
    d = q1["founder_genomes"]
    h = q1["visitor_histories"]
    demand(d["n_independent"] == h["n_independent"] == 8, "fresh Q1 source axes")
    demand(q1["updates"] == 1000 and q1["main_cases"] == 1024
           and q1["null_control"]["cases"] == 64 and q1["total_cases"] == 1088,
           "fresh Q1 main/null allocations")
    demand(len(q1["settings"]) == 4
           and q1["null_control"]["exact_matched_fixed_evolving_pair_traces"] == 32,
           "fresh Q1 null pair and setting coverage")
    demand(receipt["fresh_founder_q1"]["original_32_shard_case_count"] == 1088,
           "fresh Q1 original receipt")
    demand(all(row["negative_fixed_founder_means"] == 8 for row in
               receipt["fresh_founder_q1"]["settings"]), "R1 fixed-A negative founder means")

    b = files["baseline_design"]
    rawb = files["baseline_results"]
    sample = b["cohort"]
    factors = b["factorial"]
    demand(sample["independent_founder_seed_count"] == 12
           and len(sample["nested_demography_stream_ids"]) == 4
           and factors["freeze_prefix_updates"] == 30
           and factors["total_updates_per_trajectory"] == 80
           and b["budget"]["complete_trajectories"] == rawb["raw_rows"] == 384
           and rawb["founders"] == 12,
           "baseline pollen factorial allocation")
    demand(b["status"] == "FROZEN_EXPLORATORY_MECHANISM_PILOT_NOT_INDEPENDENT_CONFIRMATION"
           and b["analysis"]["unit_of_independent_resampling"] ==
           "founder seed, not demographic replicate or paired arm",
           "baseline inference rank and resampling")

    repeat = files["matched_repeat"]
    demand(repeat["original_arm_trajectories"] == 12288
           and repeat["repeats_per_context"] == 4 and repeat["horizon"] == 200
           and len(repeat["settings"]) == 4,
           "repeated A-I archive inventory")
    central = repeat["settings"]["delayed_control"]["central"]
    demand(central["paired_eligible_contexts"] == 128
           and central["A"]["far_identical_endpoint_contexts"] == 107
           and central["I"]["far_identical_endpoint_contexts"] == 17
           and central["A"]["contrast_labels"]["0.0"]["all_neutral_contexts"] == 103,
           "central matched A/I conditioning")

    prediction = files["prediction"]
    demand(prediction["primary"] ==
           "evolving_I_change founder-only leave-cell-out skill", "known-source prediction target")
    for row in prediction["results"].values():
        demand(row["n_founders"] == row["n_histories"] == 160,
               "known-source held-out coordinate coverage")

    c = files["registered_result"]
    policy = files["registered_plan"]
    demand(policy["execution_authorized"] and policy["complete_only"]
           and policy["optional_stopping"] is False
           and policy["shards"] == 32 and policy["max_parallel"] == 8,
           "registered execution contract")
    demand(c["crossings"] == 25600 and c["independent_axes"] == [160, 160]
           and c["actual_restoration_tested"] is False, "registered crossed design")
    demand(c["saved_states"] == 6553600
           and c["unique_updates"] == 6400000,
           "registered raw state and update count")
    a = c["arms"]
    demand(a["fixed_B8"]["alive"] == a["evolving_B8"]["alive"] == 25600
           and a["fixed_B4p5"]["alive"] == 1385
           and a["evolving_B4p5"]["alive"] == 25118
           and a["fixed_B8"]["genetic_first"] == 13868
           and a["evolving_B8"]["genetic_first"] == 16000,
           "registered G/S numerator-denominator identities")
    e = {x["name"]: x for x in c["primary"]["endpoints"]}
    demand(abs(e["genetic_loss"]["estimate"] - .08328125) < 1e-12
           and abs(e["survival_interaction"]["estimate"] - .9270703125) < 1e-12,
           "registered G/S estimates")
    demand(c["primary"]["df"] == 159
           and c["primary"]["marginal_confidence"] == .975
           and c["primary"]["familywise_alpha"] == .05
           and c["primary"]["both_exceed_margin"] is False
           and c["biological_SESOI_endorsed"] is False,
           "registered inference rank, no biological equivalence")
    assets = files["original_assets"]
    demand(len(assets) == 97
           and len([x for x in assets if x.startswith("raw-shard-")]) == 32
           and len([x for x in assets if x.startswith("seal-")]) == 32
           and len([x for x in assets if x.startswith("hashes-")]) == 32
           and "SUMMARY160.json" in assets,
           "source original-asset inventory 32+32+32+1")

    q2 = files["q2_null"]
    demand(q2["original_run"]["original_cases"] == 384
           and q2["scientific_status"] == "complete_preregistered_both_coprimary_inconclusive",
           "Q2 original inconclusive co-primaries")

    r5 = files["transfer"]
    audit = files["transfer_audit"]
    demand(len(r5["cohort_allele_counts"]) == 64
           and len(r5["tables"]) == 10
           and audit["allocated"] == 10240
           and audit["cohorts"] == 64
           and audit["biological_replay_is_independent"] is False,
           "R5 nested cohort and reader status")
    demand(all(t["allocated"] == 1024
               and 0 <= t["occupied"] <= t["allocated"]
               and t["survivor_assay_change"]["n"] == t["occupied"]
               for t in r5["tables"]), "R5 survival-conditioned assay denominators")
    demand(audit["maximum_interval_absolute_difference"] < 1e-12
           and audit["interval_arithmetic_tolerance"] == 1e-12,
           "R5 source technical quantile tolerance")
    pedigree = files["secondary"]
    demand(pedigree["paths"] == 240
           and pedigree["independent_crossed_blocks"] == 4
           and pedigree["new_independent_scientific_samples"] == 0,
           "secondary pilot nested source identity")

    p = root / SUMMARY
    method = p.read_text(encoding="utf8")
    required = (
        "25,600 crossed source cells", "24/32", "4/32", "97 recorded original assets",
        "both co-primary endpoints", "520/521", "521 original Actions",
        "not a new biological experiment", "No researcher-chosen favourable"
    )
    # Some counts are accompanied by Markdown emphasis; exact lexical
    # guard is only used for stable scientific or archive-disposition phrases.
    required = tuple(x for x in required if x not in
                     ("24/32", "4/32", "both co-primary endpoints"))
    for phrase in required:
        demand(phrase.lower() in method.lower(),
               "reporting manuscript omitted: " + phrase)
    demand("NOT established" in method
           and "not a journal-approved Reporting Summary" in method
           and "not a new confirmation" in method,
           "submission and inference boundaries omitted")

    return {
        "status": "SOURCE_BOUND_REPORTING_SUMMARY_PASS_NO_EXTERNAL_DEPOSIT_CLAIM",
        "source_sha256": dict(sorted(digest.items())),
        "n_source_files_checked": len(digest),
        "registered_G_pp": 100 * e["genetic_loss"]["estimate"],
        "registered_S_pp": 100 * e["survival_interaction"]["estimate"],
        "reported_counts": {
            "fresh_main": 1024, "fresh_technical_null": 64,
            "pollen_baseline": 384, "matched_repeat": 12288,
            "crossed_160x160": 25600, "original_assets": 97,
            "bounded_transfer_futures": 10240,
            "secondary_colonization_nested": 240
        },
        "no_new_biological_simulation": True,
        "journal_reporting_summary_author_approved": False,
        "doi_external_deposit_verified": False,
        "external_rights_confirmed": False,
        "independent_biological_model_reimplementation": False,
        "cohorts_pooled_as_independent_islands": False,
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    out = args.out
    if out.exists():
        p.error("refusing to overwrite existing reporting verification")
    d = verify(args.root)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("x", encoding="utf-8") as f:
        json.dump(d, f, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False)
        f.write("\n")
    print(json.dumps({"status": d["status"], "source_files": d["n_source_files_checked"],
                      "new_biology": 0}))


if __name__ == "__main__":
    main()
