"""Retrospective paired onset audit of original Model3 pilot: NO new biology.

Reads the six SHA-pinned, independently replayed 256-case event receipts.
The event clock is a 0.05 threshold sustained for 20 occupied censuses;
it is not a clock for the beginning of natural selection.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha1
from pathlib import Path
import argparse
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/results/genetic_access_pilot_20261014"
READOUT = DATA / "PAIRED_CLOCK_RETROSPECTIVE_20261014.json"
FOUNDERS = ("main", "confirmation")
CONTEXTS = (0, 3, 4)
CLASSES = (
    "assurance_first", "investment_first", "near_simultaneous",
    "assurance_only", "investment_only", "neither",
)
BLOBS = {
    "main_c0": "09bcbf77d1aa0e5da755d95da5f342ded00aecf2",
    "main_c3": "e978ec6316fe041f7afccd5181adbc9b7c89466c",
    "main_c4": "a34d8c3aa7aaca031adb6eed3fc5ca7b7b9d3e1c",
    "confirmation_c0": "761c9fd595a4ddaa98e7355bb6b6c7dbf3e42a38",
    "confirmation_c3": "8f8c4f18c8afb68b683bcc66b9f9de1b7a33ca44",
    "confirmation_c4": "5f7a3b4de5fa6cd9ab6db271d8edb24d77fc9282",
}
CASE_RE = re.compile(r"^(main|confirmation)_c([034])_A([HL])_I([01])_r([0-9]{3})$")
HASH_RE = re.compile(r"^[0-9a-f]{64}$")


def event_class(a, i):
    if a is None:
        return "neither" if i is None else "investment_only"
    if i is None:
        return "assurance_only"
    if abs(a - i) <= 5:
        return "near_simultaneous"
    return "assurance_first" if a < i else "investment_first"


def git_blob_sha(data):
    return sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def verified_rows(data_dir=DATA):
    rows = []
    seen = set()
    for f in FOUNDERS:
        for c in CONTEXTS:
            name = f"{f}_c{c}"
            # GitHub blobs are LF; normalize platform text checkout only.
            content = (data_dir / f"{name}_independently_verified.json").read_bytes().replace(b"\r\n", b"\n")
            if git_blob_sha(content) != BLOBS[name]:
                raise ValueError(f"Source blob mismatch: {name}")
            data = json.loads(content)
            if (data.get("status") != "ALL_256_PILOT_SHARD_RAW_GENOMES_REPLAYED"
                    or data.get("cases") != 256 or data.get("updates") != 51200
                    or data.get("original_model3_biological_source_replayed") is not True
                    or data.get("original_t0_historical_source_admitted") is not True
                    or tuple(data.get("six_event_categories", [])) != CLASSES):
                raise ValueError(f"Old independent reader admission failed: {name}")
            cases = data["original_case_receipts"]
            if len(cases) != 256:
                raise ValueError(f"Unexpected number of source cases: {name}")
            for case in cases:
                k = case["case_key"]
                m = CASE_RE.fullmatch(k)
                if not m or m.group(1) != f or int(m.group(2)) != c:
                    raise ValueError(f"Unexpected identity: {k}")
                width, hidden, r = m.group(3), int(m.group(4)), int(m.group(5))
                if r > 63 or k in seen:
                    raise ValueError(f"Duplicate or out-of-range paired seed: {k}")
                seen.add(k)
                if case.get("updates") != 200 or not HASH_RE.fullmatch(case.get("case_sha256", "")):
                    raise ValueError(f"Original case receipt invalid: {k}")
                ev = case["event_0p05"]
                a, i = ev["A"], ev["I"]
                for t in (a, i):
                    # Last possible 20-census start in t0..200 is t181.
                    if t is not None and (type(t) is not int or not 0 <= t <= 181):
                        raise ValueError(f"Invalid original event time: {k}")
                if ev["category"] != event_class(a, i):
                    raise ValueError(f"Six-class mismatch: {k}")
                rows.append(dict(founder=f, context=c, width=width, hidden_I=hidden,
                                 history=r, A=a, I=i, category=ev["category"]))
    if len(rows) != 1536 or len(seen) != 1536:
        raise ValueError("Incomplete original 1,536-path readback")
    return rows


def time_summary(values):
    if not values:
        raise ValueError("Missing paired clock outcomes")
    return {
        "n": len(values),
        "mean_high_minus_low_updates": sum(values)/len(values),
        "median_high_minus_low_updates": sorted(values)[len(values)//2],
        "high_earlier": sum(x < 0 for x in values),
        "equal": sum(x == 0 for x in values),
        "high_later": sum(x > 0 for x in values),
    }


def summarize(rows):
    pairs = defaultdict(dict)
    for row in rows:
        k = (row["founder"], row["context"], row["hidden_I"], row["history"])
        w = row["width"]
        if w not in ("L", "H") or w in pairs[k]:
            raise ValueError(f"Duplicate/invalid A-width arm: {k}")
        pairs[k][w] = row
    if len(pairs) != 768 or any(set(v) != {"L", "H"} for v in pairs.values()):
        raise ValueError("Missing/unmatched A-width history")
    if {(k[0], k[3]) for k in pairs} != {(f, h) for f in FOUNDERS for h in range(64)}:
        raise ValueError("Incomplete founder/history clusters")
    if {k[1] for k in pairs} != set(CONTEXTS):
        raise ValueError("Missing visitor ecology")

    by_width = {"L": Counter(), "H": Counter()}
    transitions = {a: {b: 0 for b in CLASSES} for a in CLASSES}
    event_status = {trait: {k: 0 for k in ("neither", "high_only", "low_only", "both")}
                    for trait in ("A", "I")}
    time_diffs = {"A": [], "I": []}
    strata = defaultdict(lambda: dict(n=0, dlo=0, dhi=0, direct=0))
    for (founder, context, _hidden, _history), pair in sorted(pairs.items()):
        lo, hi = pair["L"], pair["H"]
        lc, hc = lo["category"], hi["category"]
        if lc not in CLASSES or hc not in CLASSES:
            raise ValueError("Unknown category")
        transitions[lc][hc] += 1
        by_width["L"][lc] += 1
        by_width["H"][hc] += 1
        s = strata[(founder, context)]
        s["n"] += 1
        s["dlo"] += int(lc == "assurance_first") - int(lc == "investment_first")
        s["dhi"] += int(hc == "assurance_first") - int(hc == "investment_first")
        s["direct"] += int(lc == "investment_first" and hc == "assurance_first")
        for trait in ("A", "I"):
            lt, ht = lo[trait], hi[trait]
            status = ("both" if lt is not None and ht is not None else
                      "low_only" if lt is not None else
                      "high_only" if ht is not None else "neither")
            event_status[trait][status] += 1
            if status == "both":
                time_diffs[trait].append(ht-lt)

    dlow = by_width["L"]["assurance_first"] - by_width["L"]["investment_first"]
    dhigh = by_width["H"]["assurance_first"] - by_width["H"]["investment_first"]
    return {
        "schema": "chapter2_original_1536_pilot_paired_clock_posthoc_readout_v1",
        "status": "EXPLORATORY_RETROSPECTIVE_EXISTING_SOURCE_NOT_INDEPENDENT_FOUNDER_CONFIRMATION",
        "source_verified_receipt_git_blobs": BLOBS,
        "original_case_records": 1536,
        "matched_width_pairs": 768,
        "distinct_original_founder_genotype_backgrounds": 2,
        "nested_paired_founder_history_seed_clusters": 128,
        "contexts": list(CONTEXTS),
        "event_definition": "A+0.05/I-0.05 sustained over 20 occupied censuses; near +/-5; starts 0..181; original reader events only",
        "counts_all_starts": {w: {k: by_width[w][k] for k in CLASSES} for w in ("L", "H")},
        "D_A_first_minus_I_first": {"low": dlow/768, "high": dhigh/768,
                                     "high_minus_low": (dhigh-dlow)/768},
        "paired_transition_counts_rows_low_columns_high": transitions,
        "paired_event_detection": event_status,
        "paired_first_sustained_onset_differences": {
            trait: time_summary(time_diffs[trait]) for trait in ("A", "I")
        },
        "six_founder_context_strata": [
            {"founder": f, "context": c, "n_pairs": strata[(f,c)]["n"],
             "D_low": strata[(f,c)]["dlo"]/strata[(f,c)]["n"],
             "D_high": strata[(f,c)]["dhi"]/strata[(f,c)]["n"],
             "D_change": (strata[(f,c)]["dhi"]-strata[(f,c)]["dlo"])/strata[(f,c)]["n"],
             "direct_I_first_to_A_first": strata[(f,c)]["direct"]}
            for f in FOUNDERS for c in CONTEXTS
        ],
        "claim_limits": [
            "Descriptive posthoc decomposition of the already admitted six original pilot shards; no new biological updates.",
            "Shared founder and future RNG histories across contexts/hidden-I are not independent island populations.",
            "A/I observed-on-both conditional clock differences are subject to event detection selection; do not interpret as all-start causal mediation.",
            "Response onset is not natural selection onset; 0.05 threshold geometry and the 20-census window are built into this statistic.",
            "Only the original 0.05 event receipts are present in these JSONs; 0.025/0.10 reclassification requires stored annual census originals.",
            "No founder-2+ generalization, independent source-co-carriage effect, proof of genetic rate mediator, or Q4 survival benefit.",
            "The six independently verified case receipts do not substitute for a fresh, independent replay of every original genome.",
        ],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="Compare committed output with independent verified receipts")
    ap.add_argument("--write", action="store_true", help="Regenerate from existing verified receipts only")
    args = ap.parse_args()
    if args.check and args.write:
        ap.error("Choose --check or --write")
    result = json.dumps(summarize(verified_rows()), indent=2, ensure_ascii=False)+"\n"
    if args.check:
        if READOUT.read_text(encoding="utf-8") != result:
            raise SystemExit("FAIL: committed paired clock differs from original source receipts")
        print("PASS: committed paired clock agrees with verified original receipts")
    elif args.write:
        READOUT.write_text(result, encoding="utf-8", newline="\n")
        print("WROTE: read-only paired clock retrospective output")
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
