"""Independent source-archive admission and six-class readout for Q2 support intervention.

Reads complete original typed genomes and recorded parentage. Re-derives event
start times by an independent scalar loop, rather than importing the producer's
convolution-based six-class classifier. Does NOT rerun Model 3 biology.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.chapter2_q2_i_support_order_20261016 import (
    CLASSES, DEFAULT_DESIGN, ROOT, declared_tasks, founder_state, load_protocol,
    sha, source_manifest,
)
from scripts.run_chapter2_q2_i_support_production_20261016 import (
    CASES_PER_SHARD, SHARDS, SOURCE_PATH, case_key,
)
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.chapter2_q2_i_support_order_20261016 import native_config
from scripts.run_model3_persistent_isolation import exposure


def classify_independently(trace, contract):
    n = len(trace)
    starts = {}
    for loc, direction, threshold, name in (
        (1, +1, float(contract["A_positive"]), "A"),
        (2, -1, float(contract["I_negative"]), "I"),
    ):
        indicators = [
            (trace[t, 0] > 0 and np.isfinite(trace[t, loc])
             and direction * (trace[t, loc] - trace[0, loc]) >= threshold - 1e-12)
            for t in range(n)
        ]
        window = int(contract["consecutive_occupied_censuses"])
        starts[name] = next((s for s in range(n-window+1)
                             if all(indicators[s:s+window])), None)
    a, i = starts["A"], starts["I"]
    tie = int(contract["ties_within_updates"])
    if a is None and i is None:
        category = "neither"
    elif a is None:
        category = "investment_only"
    elif i is None:
        category = "assurance_only"
    elif abs(a-i) <= tie:
        category = "near_simultaneous"
    else:
        category = "assurance_first" if a < i else "investment_first"
    extinction = next((t for t in range(n) if trace[t, 0] == 0), None)
    return dict(label=category, A_start=a, I_start=i,
                A_event=a is not None, I_event=i is not None,
                occupied_terminal=bool(trace[-1, 0] > 0),
                first_extinction=extinction)



def check_parentage_and_mendelian_I(data, offsets, year, parents):
    """Re-admit source offspring identity, ancestry and I-locus transmission.

    This is an independent check of saved parentage and homologs, NOT a replay
    of the original probability of drawing each parent or reproductive rate.
    I carries no new mutations and no seed immigrants in this registered design.
    """
    start, end, nex, nxt = map(int, (
        offsets[year], offsets[year+1], offsets[year+1], offsets[year+2]))
    ids = data["ids"]
    years = data["birth_years"]
    old_ids = ids[start:end].tolist()
    next_ids = ids[nex:nxt].tolist()
    if len(old_ids) != len(set(map(int, old_ids))) or len(next_ids) != len(set(map(int, next_ids))):
        raise ValueError("Nonunique source plant IDs in a census")
    old_map = {int(ident): start+i for i,ident in enumerate(old_ids)}
    next_map = {int(ident): nex+i for i,ident in enumerate(next_ids)}
    offspring = [int(x) for x in parents[:, 0]]
    newborn = [int(ids[pos]) for pos in range(nex, nxt)
               if years[pos] == year+1]
    if (len(offspring) != len(newborn) or len(set(offspring)) != len(offspring)
            or set(offspring) != set(newborn)):
        raise ValueError("Newborn offspring/parentage roster differs")
    old_state_fields = ("alleles", "allele_origin", "mutation_flags", "birth_years")
    # With no seed immigration, an older plant may only be an unchanged survivor.
    for ident,pos in next_map.items():
        if ident in offspring:
            continue
        if ident not in old_map or years[pos] > year:
            raise ValueError("Unaccounted migrant or adult without original source")
        old = old_map[ident]
        if any(not np.array_equal(data[name][pos], data[name][old])
               for name in old_state_fields):
            raise ValueError("An adult survivor changed its diploid genome")
    for child_id,mother_id,father_id in parents:
        child_id,mother_id,father_id = map(int, (child_id,mother_id,father_id))
        if child_id not in next_map or mother_id not in old_map or father_id not in old_map:
            raise ValueError("Parentage ID not found in the adjacent original censuses")
        child = next_map[child_id]
        if years[child] != year+1:
            raise ValueError("Child has inconsistent year of birth")
        for homolog, parent_id in enumerate((mother_id, father_id)):
            parent = old_map[parent_id]
            for locus in range(3):
                child_origin = data["allele_origin"][child,locus,homolog]
                possible = np.flatnonzero(
                    data["allele_origin"][parent,locus,:] == child_origin)
                if not len(possible):
                    raise ValueError("Offspring homolog origin absent from named parent")
                child_flag = bool(data["mutation_flags"][child,locus,homolog])
                if locus == 1:
                    # I mutations are disabled: values, ancestral origin and
                    # mutation flags must match an actual parental homolog.
                    matches = [
                        h for h in possible
                        if data["alleles"][child,locus,homolog] == data["alleles"][parent,locus,h]
                        and child_flag == bool(data["mutation_flags"][parent,locus,h])
                    ]
                    if not matches:
                        raise ValueError("Non-Mendelian investment allele or mutation flag")
                elif not child_flag:
                    # Nonmutated M/A alleles must also match their parent.
                    if not any(
                        (not bool(data["mutation_flags"][parent,locus,h]))
                        and data["alleles"][child,locus,homolog] == data["alleles"][parent,locus,h]
                        for h in possible
                    ):
                        raise ValueError("Unmutated offspring locus not transmitted by parent")


def replay_native_history(data, offsets, parent_offsets, d, task):
    """Independent *execution loop* with immutable native Model 3 operators.

    Reproduces the recorded same-RNG path exactly, comparing all ancestral
    genomes and parentage each census. It is an audit of the native producer,
    not a second independent biological draw or independent model family.
    """
    fs, vs, arm, policy = task
    state = founder_state(d, fs, policy)
    cfg = native_config(d)
    visitors = exposure(vs, arm)
    master = int(np.random.SeedSequence([
        fs, vs, d["randomization"]["master_seed_salt"]]).generate_state(1)[0])
    streams = {name: stream(master, name, 0) for name in STREAM_IDS}
    fields = ("alleles", "allele_origin", "mutation_flags", "ids", "birth_years")
    comparisons = 0
    for year in range(d["horizon"] + 1):
        start, end = int(offsets[year]), int(offsets[year+1])
        for field in fields:
            if not np.array_equal(getattr(state, field), data[field][start:end]):
                raise ValueError(f"Original-genome native replay mismatch in {field} at {year}")
            comparisons += 1
        if year == d["horizon"]:
            break
        ledger = reproduce(state, visitors.visitors[year], cfg)
        state, info = advance(state, ledger, visitors.seed_candidates[year],
                              cfg, streams, year=year,
                              mutation_traits=(True, False, True))
        left = int(parent_offsets[year])
        right = int(parent_offsets[year+1])
        if not np.array_equal(info["parentage"], data["parentage"][left:right]):
            raise ValueError(f"Original native replay parentage mismatch at {year}")
        comparisons += 1
    return comparisons


def admit_exact_shard_inventory(directory, declared_case_keys):
    """Refuse foreign, incomplete or unexpectedly duplicated original files."""
    mandatory = {"SOURCES.json", "ACTIVATION_SHA256.txt", "DESIGN_SHA256.txt",
                 "COMPLETION.json"}
    declared = set(declared_case_keys)
    expected = mandatory | {key + ext for key in declared
                            for ext in (".npz", ".json")}
    observed = {path.name for path in directory.iterdir()}
    if observed != expected or any(not item.is_file() for item in directory.iterdir()):
        raise ValueError("Unexpected or missing source-shard files")
    return len(declared)

def _arrays_checked(archive, d, task, *, native_replay=False, receipt=None):
    with np.load(archive, allow_pickle=False) as z:
        required = {"trace", "offsets", "parentage_offsets", "parentage",
                    "alleles", "allele_origin", "mutation_flags", "ids", "birth_years"}
        if set(z.files) != required:
            raise ValueError("Missing/foreign complete diploid-genome fields")
        data = {k: z[k].copy() for k in z.files}
    t, offsets, po = data["trace"], data["offsets"], data["parentage_offsets"]
    count = d["horizon"]
    if (t.shape != (count+1, 5) or offsets.shape != (count+2,)
            or po.shape != (count+1,) or data["parentage"].ndim != 2
            or data["parentage"].shape[1] != 3
            or offsets[0] != 0 or po[0] != 0
            or np.any(np.diff(offsets) < 0) or np.any(np.diff(po) < 0)):
        raise ValueError("Invalid annual source array layout")
    n_all = int(offsets[-1])
    if receipt is not None and (
        receipt.get("typed_genotype_records") != n_all
        or receipt.get("recorded_offspring_parentage") != len(data["parentage"])
        or receipt.get("censuses") != len(t)
    ):
        raise ValueError("Archived readout receipt counts differ from original typed arrays")
    if (n_all != len(data["ids"]) or
            data["alleles"].shape != (n_all, 3, 2)
            or data["allele_origin"].shape != (n_all, 3, 2)
            or data["mutation_flags"].shape != (n_all, 3, 2)
            or data["birth_years"].shape != (n_all,)
            or po[-1] != len(data["parentage"])):
        raise ValueError("Invalid typed state or parentage size")
    if not np.isfinite(t[:, 0]).all() or np.any(t[:, 0] < 0):
        raise ValueError("Invalid population counts")
    native_initial = founder_state(d, task[0], task[3])
    for key in ("alleles", "allele_origin", "mutation_flags", "ids", "birth_years"):
        if not np.array_equal(data[key][:offsets[1]], getattr(native_initial, key)):
            raise ValueError("Original founder state not read back")
    support = set(map(float, native_initial.alleles[:, 1, :].ravel()))
    for year in range(count+1):
        start, end = map(int, offsets[year:year+2])
        alleles = data["alleles"][start:end]
        n = end-start
        if t[year, 0] != n or np.any(data["mutation_flags"][start:end, 1, :]):
            raise ValueError("Original census or no-I-mutation mismatch")
        if not set(map(float, alleles[:, 1, :].ravel())) <= support:
            raise ValueError("Foreign I allele created without mutation or immigration")
        if n:
            traits = alleles.mean(axis=2)
            reconstructed = [traits[:, 2].mean(), traits[:, 1].mean(),
                             float(alleles[:, 1, :].min()),
                             int(np.sum(alleles[:, 1, :] < .45))]
            if not np.allclose(t[year, 1:], reconstructed, atol=1e-12, rtol=0):
                raise ValueError("Annual phenotype not regenerated from genomes")
        elif not np.isnan(t[year, 1:]).all():
            raise ValueError("Extinction was converted into biological trait values")
        if year < count:
            parents = data["parentage"][po[year]:po[year+1]]
            next_ids = data["ids"][offsets[year+1]:offsets[year+2]]
            old_ids = data["ids"][start:end]
            if (not np.isin(parents[:, 0], next_ids).all()
                    or not np.isin(parents[:, 1:], old_ids).all()):
                raise ValueError("Parentage not compatible with consecutive censuses")
            check_parentage_and_mendelian_I(data, offsets, year, parents)
    if native_replay:
        replay_native_history(data, offsets, po, d, task)
    return t


def _expected_sources(design_path):
    sources = source_manifest(design_path)
    sources[str(SOURCE_PATH.relative_to(ROOT))] = sha(SOURCE_PATH.read_bytes())
    return sources, sha(json.dumps(sources, sort_keys=True).encode("utf-8"))


def _read_cases(root, d, design_path, *, native_replay=False):
    expected = declared_tasks(d)
    cases = {case_key(x): x for x in expected}
    if len(cases) != 384:
        raise ValueError("Nonunique prospective task keys")
    sources, source_digest = _expected_sources(design_path)
    found = {}
    activation_ids = set()
    dirs = sorted(root.glob("shard-*"))
    if len(dirs) != SHARDS:
        raise ValueError("Require all 32 original producer shards")
    for shard in range(SHARDS):
        directory = root / f"shard-{shard:02d}"
        if directory not in dirs:
            raise ValueError("Missing expected named original shard")
        c = json.loads((directory / "COMPLETION.json").read_text(encoding="utf-8"))
        sr = json.loads((directory / "SOURCES.json").read_text(encoding="utf-8"))
        if sr != sources or c.get("source_manifest_sha256") != source_digest:
            raise ValueError("Original Model3 source identity mismatch")
        if (c.get("shard") != shard or c.get("case_count") != CASES_PER_SHARD
                or c.get("status") != "complete_source_produced_not_independently_read_back"
                or c.get("design_sha256") != sha(design_path.read_bytes())
                or (directory / "DESIGN_SHA256.txt").read_text().strip() != sha(design_path.read_bytes())):
            raise ValueError("Invalid frozen design or shard inventory")
        activation_ids.add((directory / "ACTIVATION_SHA256.txt").read_text().strip())
        declared_subset = [case_key(x) for x in expected[shard*CASES_PER_SHARD:
                                                        (shard+1)*CASES_PER_SHARD]]
        if c.get("cases") != declared_subset or set(c.get("receipt_hashes", {})) != set(declared_subset):
            raise ValueError("Wrong original 12-case shard inventory")
        admit_exact_shard_inventory(directory, declared_subset)
        for key in declared_subset:
            if key in found or key not in cases:
                raise ValueError("Repeated or foreign original case")
            receipt_path = directory / (key + ".json")
            if sha(receipt_path.read_bytes()) != c["receipt_hashes"][key]:
                raise ValueError("Original case receipt hash mismatch")
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            archive = directory / (key + ".npz")
            if (receipt["status"] != "full_source_case_not_independently_read_back"
                    or receipt["sha256"] != sha(archive.read_bytes())
                    or receipt["task"] != list(cases[key])
                    or receipt["source_manifest_sha256"] != source_digest
                    or receipt["censuses"] != 201):
                raise ValueError("Invalid original source case admission")
            trace = _arrays_checked(archive, d, cases[key], native_replay=native_replay, receipt=receipt)
            computed = classify_independently(trace, d["response"])
            if computed != receipt["events"]:
                raise ValueError("Independent 20-census event recheck differs")
            found[key] = computed
    if set(found) != set(cases) or len(activation_ids) != 1 or not next(iter(activation_ids)):
        raise ValueError("Incomplete original full study or mixed activations")
    return found


def _scores(cells, d):
    f = range(d["founders"]["first"], d["founders"]["last"]+1)
    h = range(d["visitors"]["first"], d["visitors"]["last"]+1)
    score = np.zeros((len(f), len(h), 2), dtype=float)
    for i, fs in enumerate(f):
        for j, vs in enumerate(h):
            kd = cells[case_key((fs, vs, "far", "dense_reachable"))]
            ks = cells[case_key((fs, vs, "far", "sparse_reachable"))]
            rank = lambda row: int(row["label"]=="assurance_first")-int(row["label"]=="investment_first")
            score[i, j, 0] = rank(kd)-rank(ks)
            score[i, j, 1] = int(kd["I_event"])-int(ks["I_event"])
    return score


def readout(root: Path, design_path: Path, *, native_replay=False):
    d = load_protocol(design_path)
    cases = _read_cases(Path(root), d, design_path, native_replay=native_replay)
    effects = _scores(cases, d)
    observed = effects.mean(axis=(0, 1))
    draws = d["inference"]["bootstrap_draws"]
    rng = np.random.default_rng(d["inference"]["bootstrap_seed"])
    boot = np.empty((draws, 2), dtype=float)
    for b in range(draws):
        f = rng.integers(0, 8, 8)
        h = rng.integers(0, 8, 8)
        boot[b] = effects[np.ix_(f, h)].mean(axis=(0, 1))
    alpha = d["inference"]["primary_familywise_alpha"]
    lo, hi = np.quantile(boot, [alpha/4, 1-alpha/4], axis=0)
    names = ["carrier_order_score_delta", "carrier_I_event_delta"]
    primary = {
        name: {"estimate":float(observed[k]),"familywise_conservative_CI":[float(lo[k]),float(hi[k])],
               "excludes_zero":bool(lo[k] > 0 or hi[k] < 0)}
        for k,name in enumerate(names)
    }
    cells = {}
    for arm in d["visitors"]["arms"]:
        cells[arm] = {}
        for policy in d["policies"]:
            rows = [case for key,case in cases.items()
                    if key.endswith("_"+arm+"_"+policy)]
            if len(rows) != 64:
                raise ValueError("Incomplete inference cell")
            counter = Counter(row["label"] for row in rows)
            cells[arm][policy] = {
                "six_class_counts":{label: counter[label] for label in CLASSES},
                "I_event_count":sum(row["I_event"] for row in rows),
                "A_event_count":sum(row["A_event"] for row in rows),
                "terminal_occupancy_count":sum(row["occupied_terminal"] for row in rows),
                "all_start_denominator":64,
            }
    if cells["far"]["dense_unreachable"]["I_event_count"] != 0 or cells["near"]["dense_unreachable"]["I_event_count"] != 0:
        raise ValueError("Structural no-I-access control produced impossible event")
    return {
        "status":"384_TYPED_SOURCE_PATHS_INDEPENDENT_EVENT_AND_BOOTSTRAP_RECHECKED",
        "experimental_scope":"synthetic within Model3 only; not natural islands",
        "full_cases":len(cases),
        "primary":primary,
        "joint_decision":"both_supported" if all(x["excludes_zero"] for x in primary.values())
                         else "partial_only" if any(x["excludes_zero"] for x in primary.values())
                         else "both_inconclusive",
        "cells":cells,
        "confidence_note":"Two-way crossed founder/visitor 9999 bootstrap, two-sided Bonferroni 97.5% intervals, zero cases omitted",
        "no_Q3_density_ABM_causal_mediation":True,
        "native_model_full_path_replay": bool(native_replay),
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--design", type=Path, default=DEFAULT_DESIGN)
    p.add_argument("--source-root", type=Path, required=True)
    p.add_argument("--native-replay", action="store_true", help="Re-execute all original RNG paths, compare every saved native genome/parentage. Not a new independent biological cohort.")
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    if a.out.exists():
        p.error("Refuse original readout overwrite")
    result = readout(a.source_root, a.design, native_replay=a.native_replay)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    print(json.dumps({"status":result["status"],"decision":result["joint_decision"]}))


if __name__ == "__main__":
    main()
