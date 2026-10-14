"""Source-locked Q2 response-threshold audit of EXISTING raw clock-pilot ZIPs.

Read-only: no Model3 import, RNG, parent selection, birth, advance or biology.
Archives must match all six published SHA256s and all 1,536 previously
independently replayed raw-case SHA256s. Only means and census are read.
All thresholds besides the registered 0.05 are POSTHOC SENSITIVITY, not new
registered evolutionary experiments or claims about onset of selection.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import io
import json
from pathlib import Path
import re
import stat
import zipfile

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/results/genetic_access_pilot_20261014"
RECEIPT = DATA / "EXTERNAL_SOURCE_AND_MIRROR_RECEIPT.json"
RECEIPT_BLOB = "c36d861796ae903ed3768fe4cbd2cc3684eabd1d"
SOURCE_RECEIPT_BLOBS = {
    "main_c0": "09bcbf77d1aa0e5da755d95da5f342ded00aecf2",
    "main_c3": "e978ec6316fe041f7afccd5181adbc9b7c89466c",
    "main_c4": "a34d8c3aa7aaca031adb6eed3fc5ca7b7b9d3e1c",
    "confirmation_c0": "761c9fd595a4ddaa98e7355bb6b6c7dbf3e42a38",
    "confirmation_c3": "8f8c4f18c8afb68b683bcc66b9f9de1b7a33ca44",
    "confirmation_c4": "5f7a3b4de5fa6cd9ab6db271d8edb24d77fc9282",
}
SHARDS = tuple(SOURCE_RECEIPT_BLOBS)
THRESHOLDS = (0.025, 0.05, 0.075, 0.10)
CLASSES = ("assurance_first", "investment_first", "near_simultaneous",
           "assurance_only", "investment_only", "neither")
NAME = re.compile(r"^(main|confirmation)_c([034])_A([LH])_I([01])_r([0-9]{3})$")
MAX_MEMBER_BYTES = 32 * 1024**2
MAX_SHARD_TOTAL_BYTES = 1024**3


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def load_pinned_json(path: Path, sha1: str) -> dict:
    raw = path.read_bytes()
    if git_blob(raw) != sha1:
        raise ValueError("Original pinned Git blob drift: " + path.name)
    return json.loads(raw)


def hash_file(path: Path) -> str:
    d = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            d.update(chunk)
    return d.hexdigest()


def original_clock(means, census, threshold):
    """Independent replay of the original 0.05, 20 occupied, +/-5 event gate."""
    means = np.asarray(means)
    census = np.asarray(census)
    if means.shape != (201, 3) or census.shape != (201,):
        raise ValueError("Raw source lacks exactly 201 original censuses")
    if census.dtype.kind not in "iu" or census[0] != 48 or np.any(census < 0) or np.any(census > 48):
        raise ValueError("Original occupied population contract failed")
    occ = census > 0
    if not np.isfinite(means[occ]).all() or not np.isnan(means[~occ]).all():
        raise ValueError("Raw phenotype missing/finite data contract failed")
    if (~occ).any() and occ[np.flatnonzero(~occ)[0]:].any():
        raise ValueError("Extinct original population cannot recolonize")
    if not 0 < threshold <= 0.10:
        raise ValueError("Unregistered sensitivity threshold")
    time = {}
    for trait, idx, sign in (("A", 2, +1), ("I", 1, -1)):
        above = occ & (sign * (means[:, idx] - means[0, idx]) >= threshold)
        count = np.convolve(above.astype(np.int64), np.ones(20, dtype=np.int64), "valid")
        starts = np.flatnonzero(count == 20)
        time[trait] = int(starts[0]) if len(starts) else None
    a, i = time["A"], time["I"]
    if a is None:
        category = "neither" if i is None else "investment_only"
    elif i is None:
        category = "assurance_only"
    elif abs(a-i) <= 5:
        category = "near_simultaneous"
    else:
        category = "assurance_first" if a < i else "investment_first"
    return {"A": a, "I": i, "category": category}


def collect_shard(shard: str, archive: Path, expected_archive_sha: str, source_receipts: dict):
    """Check exact archived bytes, manifest, all 256 member digests and 0.05 replay."""
    if not archive.is_file() or hash_file(archive) != expected_archive_sha:
        raise ValueError("Original release ZIP absent or SHA-256 mismatch: " + shard)
    original = {x["case_key"]: x for x in source_receipts["original_case_receipts"]}
    if len(original) != 256 or source_receipts.get("status") != "ALL_256_PILOT_SHARD_RAW_GENOMES_REPLAYED":
        raise ValueError("Existing independent raw replay receipt is incomplete: " + shard)
    expected_files = {key+".npz" for key in original}
    if any(not key.startswith(shard+"_") or not NAME.fullmatch(key) for key in original):
        raise ValueError("Original names not consistent with designated shard")
    with zipfile.ZipFile(archive, "r") as z:
        infos = z.infolist()
        names = [i.filename for i in infos]
        if (len(names) != 257 or len(set(names)) != 257
                or set(names) != expected_files | {"_COMPLETION.json"}):
            raise ValueError("Unregistered ZIP entries or missing raw cases: " + shard)
        total = 0
        for info in infos:
            mode = info.external_attr >> 16
            total += info.file_size
            if ("/" in info.filename or "\\" in info.filename or info.is_dir()
                    or stat.S_IFMT(mode) not in (0, stat.S_IFREG)
                    or info.file_size > MAX_MEMBER_BYTES or total > MAX_SHARD_TOTAL_BYTES):
                raise ValueError("Unsafe/unbounded archived member: "+info.filename)
        completion = json.loads(z.read("_COMPLETION.json"))
        if (completion.get("schema") != "chapter2_clock_factorial_model3_native_raw_shard_v1"
                or completion.get("status") != "COMPLETE_REGISTERED_256_NATIVE_PATHS"
                or completion.get("cases") != 256 or completion.get("updates_per_case") != 200
                or len(completion.get("case_records", [])) != 256):
            raise ValueError("Raw original completion record invalid")
        c = {x["case_key"]: x for x in completion["case_records"]}
        if set(c) != set(original):
            raise ValueError("Raw completion case identities mismatch")
        rows = []
        for key, old in sorted(original.items()):
            raw = z.read(key + ".npz")
            digest = hashlib.sha256(raw).hexdigest()
            if digest != old["case_sha256"] or digest != c[key]["sha256"]:
                raise ValueError("Independently replayed case byte digest mismatch: " + key)
            with np.load(io.BytesIO(raw), allow_pickle=False) as saved:
                means = saved["means"]
                census = saved["population"]
            per_threshold = {str(t): original_clock(means, census, t) for t in THRESHOLDS}
            if per_threshold["0.05"] != old["event_0p05"]:
                raise ValueError("Independent 0.05 event reproduction differs from admitted source: "+key)
            m = NAME.fullmatch(key)
            if not m:
                raise ValueError("Bad registered source case ID")
            founder, context, width, hidden, history = m.groups()
            rows.append({
                "founder": founder, "context": int(context),
                "width": width, "hidden_I": int(hidden), "history": int(history),
                "events": per_threshold,
            })
    return rows


def summarize(rows, sha):
    all_pairs = defaultdict(dict)
    for row in rows:
        k = (row["founder"], row["context"], row["hidden_I"], row["history"])
        width = row["width"]
        if width not in ("L", "H") or width in all_pairs[k]:
            raise ValueError("Repeated treatment / unmatched raw source ID")
        all_pairs[k][width] = row
    if len(rows) != 1536 or len(all_pairs) != 768 or any(set(p) != {"L", "H"} for p in all_pairs.values()):
        raise ValueError("All 1,536 raw histories / 768 matched contrasts required")
    if len({(k[0],k[3]) for k in all_pairs}) != 128:
        raise ValueError("Expected only 128 original founder-history clusters")
    comparisons = {}
    for threshold in THRESHOLDS:
        th = str(threshold)
        counts = {w: Counter() for w in ("L", "H")}
        transitions = {v: {w: 0 for w in CLASSES} for v in CLASSES}
        strata = defaultdict(lambda: {"N":0, "D_L":0, "D_H":0})
        first_onset_all = {"A":{"L":0,"H":0}, "I":{"L":0,"H":0}}
        detected = {"A":{"L":0,"H":0}, "I":{"L":0,"H":0}}
        for (founder, ecology, _hidden, _history), pair in all_pairs.items():
            labels = {}
            for w in ("L","H"):
                event = pair[w]["events"][th]
                cls = event["category"]
                if cls not in CLASSES:
                    raise ValueError("Unexpected original six class")
                counts[w][cls] += 1
                labels[w] = cls
                for trait in ("A","I"):
                    time = event[trait]
                    # Fixed-horizon code for nondetection, NOT an eventual onset imputation.
                    first_onset_all[trait][w] += 182 if time is None else time
                    detected[trait][w] += int(time is not None)
            transitions[labels["L"]][labels["H"]] += 1
            d = strata[(founder,ecology)]
            d["N"] += 1
            d["D_L"] += int(labels["L"]=="assurance_first")-int(labels["L"]=="investment_first")
            d["D_H"] += int(labels["H"]=="assurance_first")-int(labels["H"]=="investment_first")
        result = {
            "all_starts_each_width":768,
            "counts":{w:{cl:counts[w][cl] for cl in CLASSES} for w in ("L","H")},
            "A_I_events":detected,
            "D_low":(counts["L"]["assurance_first"]-counts["L"]["investment_first"])/768,
            "D_high":(counts["H"]["assurance_first"]-counts["H"]["investment_first"])/768,
            "D_high_minus_low":(
                counts["H"]["assurance_first"]-counts["H"]["investment_first"]
                -counts["L"]["assurance_first"]+counts["L"]["investment_first"]
            )/768,
            "all_start_capped_first_onset_high_minus_low":{
                trait:(first_onset_all[trait]["H"]-first_onset_all[trait]["L"])/768
                for trait in ("A","I")},
            "six_strata":[
                {"founder":f,"context":c,"n_pairs":strata[(f,c)]["N"],
                 "D_high_minus_low":(strata[(f,c)]["D_H"]-strata[(f,c)]["D_L"])/strata[(f,c)]["N"]}
                for f in ("main","confirmation") for c in (0,3,4)
            ],
            "transition_low_to_high":transitions,
        }
        if any(z["n_pairs"]!=128 for z in result["six_strata"]):
            raise ValueError("Missing independent reader founder/ecology stratum")
        comparisons[th] = result
    primary = comparisons["0.05"]
    if (primary["counts"]["L"]["assurance_first"] != 56
            or primary["counts"]["H"]["assurance_first"] != 260
            or primary["counts"]["L"]["investment_first"] != 363
            or primary["counts"]["H"]["investment_first"] != 53
            or abs(primary["D_high_minus_low"]-0.6692708333333334)>1e-14
            or abs(primary["all_start_capped_first_onset_high_minus_low"]["A"]+51.302083333333336)>1e-12):
        raise ValueError("Archive sensitivity fails the original 0.05 source-locked primary")
    return {
        "schema":"chapter2_clock_raw_archive_posthoc_threshold_sensitivity_v1",
        "status":"RAW_BYTES_VERIFIED_EXISTING_BIOLOGY_ONLY_NO_NEW_EVOLUTION",
        "all_case_count":1536,
        "paired_A_width_histories":768,
        "independent_founder_genotype_backgrounds":2,
        "nested_original_founder_history_seed_clusters":128,
        "original_six_release_ZIP_sha256":sha,
        "event_rule":"first 20 consecutively occupied original 201 censuses, 5-update tie",
        "threshold_results":comparisons,
        "claim_limits":[
            "0.05 is the sole original registered response threshold; others are posthoc descriptive sensitivity.",
            "The full raw case SHA256s were compared with already independently native-replayed receipts; this does NOT rerun Model3 biology.",
            "Two historical founder genomes and matched histories are not independent origin-system replication.",
            "Changing A width also changes initial accessible allele range; a threshold-dependent time shift does not isolate selection onset or speed mediation.",
            "Undetected by the last eligible start t181 is assigned cap182 solely to compute a fixed-horizon descriptive statistic.",
            "Neither Q4 persistence, natural island founding, independent source pools nor new evolutionary trajectories are assessed.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", action="append", nargs=2, required=True,
                        metavar=("SHARD", "ZIP"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    paths = {}
    for shard, path in args.archive:
        if shard in paths:
            raise ValueError("Duplicate original ZIP shard")
        paths[shard] = Path(path)
    if set(paths) != set(SHARDS):
        raise ValueError("All and only six original ZIPs are required")
    receipt = load_pinned_json(RECEIPT, RECEIPT_BLOB)
    if (receipt["schema"] != "chapter2_clock_external_6_shard_archive_receipt_v1"
            or receipt["status"] != "RELEASE_ARCHIVED_AND_MIRROR_RECORDED"
            or set(receipt["archives"]) != set(SHARDS)):
        raise ValueError("Original release source receipt changed")
    all_rows = []
    for shard in SHARDS:
        reader = load_pinned_json(
            DATA / (shard+"_independently_verified.json"),
            SOURCE_RECEIPT_BLOBS[shard])
        all_rows.extend(collect_shard(
            shard, paths[shard], receipt["archives"][shard]["sha256"], reader))
    result = summarize(all_rows, {s:receipt["archives"][s]["sha256"] for s in SHARDS})
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.exists():
        raise FileExistsError("Do not overwrite an existing original-data sensitivity audit")
    with args.out.open("x",encoding="utf8",newline="\n") as f:
        json.dump(result,f,indent=2,ensure_ascii=False,allow_nan=False)
        f.write("\n")
    summary = [
        {"threshold":t, "D_H_minus_L":x["D_high_minus_low"],
         "A_capped_time_H_minus_L":x["all_start_capped_first_onset_high_minus_low"]["A"],
         "I_capped_time_H_minus_L":x["all_start_capped_first_onset_high_minus_low"]["I"],
         "A_events_L":x["A_I_events"]["A"]["L"], "A_events_H":x["A_I_events"]["A"]["H"]}
        for t,x in result["threshold_results"].items()
    ]
    print("Q2_ARCHIVE_THRESHOLD_RESULTS="+json.dumps(summary,separators=(",",":")))
    print("AUDIT_COMPLETE: original raw archive identities, all 1,536 members and 0.05 source events")


if __name__=="__main__":
    main()
