"""Original source-locked 2x2 Mendelian-sign negative control (NO NEW BIOLOGY).

The previously admitted m0/m6 original-I-preserving (but artificially
A-reconstructed) confirmation t0 uses six A heterozygotes in a single identical
phenotype stratum. This read-only check integrates all FOUR signed A/I
one-offspring outcomes from the original native conditional parent lottery.
It distinguishes access to a two-locus combination from selection for the
apparently favourable A-up/I-down sign.

NO model history, RNG, offspring production, population advance or new source.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.model3_island import reproduction
from scripts.audit_chapter2_original_founder_compatibility_20261014 import (
    CONTEXTS, original_fixture, source_state, original_context, ledger_parity,
)
from scripts.audit_chapter2_original_confirmation_m0_m6_F1_20261015 import (
    assign_A_only, source_carriers, audit as original_F1_audit,
)
from scripts.audit_chapter2_full_F1_joint_distribution_20261014 import (
    one_offspring_joint_distribution,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILE = ROOT / "docs/audits/chapter2_Q2_original_confirmation_m0_m6_F1_20261015.json"
SOURCE_BLOB = "27077b320532f2585ec598140593485f254d563c"
OUTPUT = ROOT / "docs/audits/chapter2_Q2_original_F1_signed_tail_negative_control_20261015.json"
DELTA = .05
SIGNED_CELLS = (
    "A_up_I_down",
    "A_up_I_up",
    "A_down_I_down",
    "A_down_I_up",
)
ABS_TOL = 1e-12


def git_blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def load_admitted_source() -> dict:
    raw = SOURCE_FILE.read_bytes()
    if git_blob(raw) != SOURCE_BLOB:
        raise ValueError("Original m0/m6 native F1 admitted source JSON bytes changed")
    data = json.loads(raw)
    if (data.get("status") != "ORIGINAL_I_UNMODIFIED_F1_ANALYTICAL_ONLY_NOT_EVOLUTION"
            or data.get("original_t0_fixture_git_blob")
                    != "4b529cce12bc44e06d43a22b10c325a52bbd967b"
            or data.get("independent_source_genome_realizations") != 1
            or data.get("original_A_heterozygote_adults") != 48
            or data.get("original_A_heterozygosity_reset_in_each_arm") != 42
            or data.get("original_I_allele_copies_preserved") is not True
            or data.get("new_Model3_future_updates") != 0
            or [x["context"] for x in data.get("contexts", [])] != [0, 3, 4]):
        raise ValueError("F1 admitted source scope or context changed")
    return data


def signed_joint_events(joint: np.ndarray, A0: float, I0: float) -> dict[str, float]:
    """Founder-relative first-child directional events on 1/32 trait grid."""
    if (joint.shape != (33, 33) or not np.isfinite(joint).all()
            or joint.min() < 0 or abs(float(joint.sum()) - 1) > ABS_TOL):
        raise ValueError("Invalid original one-offspring bivariate probability mass")
    if not (0 < DELTA < .1 and 0 <= A0 <= 1 and 0 <= I0 <= 1):
        raise ValueError("Invalid original founder trait means and gate")
    v = np.arange(33, dtype=np.float64) / 32
    a_up = v >= A0 + DELTA
    a_down = v <= A0 - DELTA
    i_down = v <= I0 - DELTA
    i_up = v >= I0 + DELTA
    if not (a_up.any() and a_down.any() and i_up.any() and i_down.any()):
        raise ValueError("Original source trait thresholds outside grid")
    def chance(ai, ii):
        return float(joint[np.ix_(ai, ii)].sum())
    result = {
        "A_up_I_down": chance(a_up, i_down),
        "A_up_I_up": chance(a_up, i_up),
        "A_down_I_down": chance(a_down, i_down),
        "A_down_I_up": chance(a_down, i_up),
    }
    if sum(result.values()) > 1 + ABS_TOL:
        raise ValueError("Four disjoint directional events exceed probability 1")
    return result


def audit() -> dict:
    prior = load_admitted_source()
    # Pure replay of previously reviewed original native source, no offspring.
    fresh = original_F1_audit()
    if (len(prior["contexts"]) != len(fresh["contexts"])
            or prior["arm_m0_vs_m6_I_A_co_carrier_counts"] != [0, 6]):
        raise ValueError("Prior original-I static experimental arms incomplete")
    for old, new in zip(prior["contexts"], fresh["contexts"]):
        if old["context"] != new["context"]:
            raise ValueError("Original visitor context reassigned")
        for key in ("F1_joint_A_I_total_variation",
                    "entire_F1_A_marginal_max_bin_error",
                    "entire_F1_I_marginal_max_bin_error"):
            if abs(old[key] - new[key]) > ABS_TOL:
                raise ValueError("Previously admitted original native F1 probabilities drifted")
        for arm in ("m0", "m6"):
            key = "P_one_child_Aup_Itdown_relative_to_original_founder_mean"
            if abs(old[key][arm] - new[key][arm]) > ABS_TOL:
                raise ValueError("Previously admitted signed F1 tail probability drifted")

    original = source_state(original_fixture(), "confirmation")
    carriers = source_carriers(original)
    arms = {k: assign_A_only(original, ids) for k,ids in carriers.items()}
    means = original.alleles.mean(axis=(0,2))
    if abs(float(means[2]) - .5) > ABS_TOL:
        raise ValueError("Original A founder mean changed")
    rows = []
    fixture = original_fixture()
    for context in CONTEXTS:
        config, visitors = original_context(fixture, "confirmation", context)
        outcomes = {}
        for arm in ("m0", "m6"):
            ledger_parity(original, arms[arm], config, visitors)
            ledger = reproduction.reproduce(arms[arm], visitors, config)
            dist = one_offspring_joint_distribution(arms[arm], ledger)
            outcomes[arm] = signed_joint_events(dist,float(means[2]),float(means[1]))
        archived = next(x for x in prior["contexts"] if x["context"]==context)
        original_key="P_one_child_Aup_Itdown_relative_to_original_founder_mean"
        for arm in ("m0", "m6"):
            if abs(outcomes[arm]["A_up_I_down"] - archived[original_key][arm]) > ABS_TOL:
                raise ValueError("Old positive-direction F1 tail no longer source-matched")
        ref=outcomes["m6"]["A_up_I_down"]
        residual=max(abs(outcomes["m6"][key]-ref) for key in SIGNED_CELLS)
        if (ref <= 0 or residual > ABS_TOL or
                any(abs(outcomes["m0"][key]) > ABS_TOL for key in SIGNED_CELLS)):
            raise ValueError("Original-I-prepared m0/m6 A/I quadrants fail Mendelian sign null")
        rows.append({
            "context": context,
            "m0_signed_events": outcomes["m0"],
            "m6_signed_events": outcomes["m6"],
            "m6_four_sign_equal_within_1e_12": residual <= ABS_TOL,
            "one_child_joint_A_I_TV": archived["F1_joint_A_I_total_variation"],
            "source_original_A_heterozygotes": 48,
            "reset_A_heterozygotes_per_arm": 42,
            "original_I_homologs_unchanged": True,
        })
    if len(rows)!=3:
        raise ValueError("Original three visitor settings incomplete")
    return {
        "schema": "chapter2_original_I_F1_signed_quadrant_null_v1",
        "status": "SOURCE_AUTHENTICATED_NATIVE_T0_SIGN_NULL_NO_NEW_BIOLOGY",
        "base_source_json_git_blob": SOURCE_BLOB,
        "genetic_source": "one original confirmation F0, synthetic A copies in both arms, original I/M exact",
        "founder_relative_threshold": DELTA,
        "signed_event_classes": list(SIGNED_CELLS),
        "new_biological_trajectories": 0,
        "new_offspring_births": 0,
        "contexts": rows,
        "conclusion": "All four signed A/I double-tail events are equally accessible at first child in m6, while all four are unavailable in m0, for this frozen artificial A/genetically original-I experiment.",
        "cannot_establish": [
            "The A-up/I-down event is not a selectively preferred outcome merely because its one-offspring access increases.",
            "No selective fitness, reproduction in subsequent generations, 20-occupied-census six-class evolutionary order or Q4 persistence was measured.",
            "Only one original source genome, with an explicitly reconstructed A locus; not independent empirical island sources.",
            "This is a conditional Mendelian symmetry within the prepared parents, not a universal genome-wide evolutionary symmetry.",
            "Original 0.05 event threshold and source-case pilot are not retuned or rerun.",
        ],
    }


def main() -> None:
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--check", action="store_true")
    cli.add_argument("--write", action="store_true")
    args=cli.parse_args()
    if args.check and args.write:
        cli.error("Select one of --check or --write")
    result=audit()
    data=json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n"
    if args.check:
        expected=json.loads(OUTPUT.read_text(encoding="utf-8"))
        if expected.keys()!=result.keys():
            raise SystemExit("Source audit structural schema mismatch")
        # Native floating-point sums can differ at last few ULPs.
        for old,new in zip(expected["contexts"],result["contexts"]):
            if old.keys()!=new.keys() or old["context"]!=new["context"]:
                raise SystemExit("Original signed quadrant source rows differ")
            for arm in ("m0","m6"):
                for key in SIGNED_CELLS:
                    if abs(old[arm+"_signed_events"][key]-new[arm+"_signed_events"][key])>ABS_TOL:
                        raise SystemExit("Original signed quadrant probabilities changed")
        print("PASS: original-I F1 signed four-quadrant negative control source matched")
    elif args.write:
        if OUTPUT.exists():
            raise FileExistsError("Never overwrite original-source signed F1 review")
        OUTPUT.parent.mkdir(parents=True,exist_ok=True)
        OUTPUT.write_text(data,encoding="utf-8",newline="\n")
        print("WROTE: original conditional F1 signed quadrant source result")
    else:
        print(data,end="")


if __name__ == "__main__":
    main()
