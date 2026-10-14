"""Exact ORIGINAL Model3 founder-genotype constraint on phenotype-matched co-carriage.

Reads only the *historical* source-pinned t0 typed-array fixture; does not
generate genotypes, sample synthetic sources, call native reproduction, or
produce any Model3 offspring / future updates.

We hold the original I HOMOLOGS fixed across arms and allow assignment of
symmetric A heterozygosity only *within* identical expressed (M,I,A) strata.
For an unchanged stratum-level A-carrier count k, moving all k carriers from
I-homozygotes (m=0) to I-heterozygotes (m=k) requires both at least k homo
and k hetero I individuals. The total possible increase in overlap is thus
sum_strata(min(n_I_het, n_I_homo)). This is an exact upper bound for this
specific control, NOT a universal bound on all genotype interventions.
"""
from __future__ import annotations

import base64
from collections import defaultdict
from hashlib import sha1, sha256
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data/design/chapter2_clock_original_t0_typed_fixture_20261013.json"
OUTPUT = ROOT / "data/results/chapter2_Q2_original_founder_carriage_swap_bound_20261015.json"
SOURCE_GIT_BLOB = "4b529cce12bc44e06d43a22b10c325a52bbd967b"
ORIGINAL_MODEL_COMMIT = "328548612e93469fcc8663f24548530a57399b9a"
BLOCKS = ("main", "confirmation")
ORIGINAL_N = 48
ORIGINAL_I_SHA = {
    "main": "1e2f173e46c20af3ecc811c81f95a38a5b09bf539e834542a6bdaf1281634930",
    "confirmation": "13cbb1c08a8da3d79db6c6cacf7443a6c865f170c7f64beea2d7f7639dbed114",
}
SOURCE_FIELDS = {
    "ids": ("<i8", (48,)),
    "alleles": ("<f8", (48, 3, 2)),
    "allele_origin": ("<i8", (48, 3, 2)),
    "mutation_flags": ("|b1", (48, 3, 2)),
    "birth_years": ("<i8", (48,)),
}


def _git_blob(raw: bytes) -> str:
    return sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def _read_typed(field: dict, dtype: str, shape: tuple, *, required_sha: str | None = None) -> bytes:
    if field.get("dtype") != dtype or field.get("shape") != list(shape):
        raise ValueError("Original t0 typed-array shape/dtype drift")
    raw = base64.b64decode(field["data_b64"], validate=True)
    count = 1
    for d in shape:
        count *= d
    width = 1 if dtype == "|b1" else 8
    if (len(raw) != count * width
            or sha256(raw).hexdigest() != field.get("sha256")
            or (required_sha is not None and sha256(raw).hexdigest() != required_sha)):
        raise ValueError("Original t0 typed-array field content/SHA invalid")
    return raw


def load_original() -> dict:
    raw = FIXTURE.read_bytes()
    if _git_blob(raw) != SOURCE_GIT_BLOB:
        raise ValueError("Original t0 fixed Git blob is not the source archive")
    d = json.loads(raw)
    if (d.get("schema") != "clock_original_t0_typed_fixture_20261013_v1"
            or d.get("scope") != "ONLY_ORIGINAL_HISTORICAL_T0_NOT_SIMULATED"
            or d.get("original_biological_commit") != ORIGINAL_MODEL_COMMIT
            or d.get("new_biological_histories") != 0
            or d.get("original_full_file_admitted_from_source_archives") is not True
            or set(d.get("original_founders", {})) != set(BLOCKS)):
        raise ValueError("Original source-admission contract is not unchanged")
    return d


def one_block(block: str, fields: dict) -> dict:
    if block not in BLOCKS or set(fields) != set(SOURCE_FIELDS):
        raise ValueError("Only two original typed founder blocks are admissible")
    decoded = {}
    for name, (dtype, shape) in SOURCE_FIELDS.items():
        decoded[name] = _read_typed(
            fields[name], dtype, shape,
            required_sha=ORIGINAL_I_SHA[block] if name == "alleles" else None)
    ids = struct.unpack("<48q", decoded["ids"])
    years = struct.unpack("<48q", decoded["birth_years"])
    alleles = struct.unpack("<288d", decoded["alleles"])
    if ids != tuple(range(ORIGINAL_N)) or any(years) or any(decoded["mutation_flags"]):
        raise ValueError("Original F0 individual IDs, birth and mutation markers invalid")
    groups: dict[tuple[float, float, float], list[tuple[int, bool, float]]] = defaultdict(list)
    for ind in range(ORIGINAL_N):
        expressed = []
        i_halfwidth = 0.0
        for locus in (0, 1, 2):
            x = alleles[(ind * 3 + locus) * 2]
            y = alleles[(ind * 3 + locus) * 2 + 1]
            if not (0 <= x <= 1 and 0 <= y <= 1):
                raise ValueError("Original t0 allele outside [0,1]")
            expressed.append((x+y)/2)
            if locus == 1:
                i_halfwidth = abs(x-y)/2
        if expressed[2] != 0.5:
            raise ValueError("Original A expressed trait not fixed at 0.5")
        groups[tuple(expressed)].append((ind, i_halfwidth > 0, i_halfwidth))
    out = []
    for phen, group in sorted(groups.items()):
        nh = sum(int(a[1]) for a in group)
        nc = len(group) - nh
        cap = min(nh, nc)
        out.append({
            "expressed_M_I_A": list(phen),
            "individual_ids": [v[0] for v in group],
            "individuals": len(group),
            "I_heterozygote_adults": nh,
            "I_homozygote_adults": nc,
            "I_heterozygote_halfwidths": sorted({v[2] for v in group if v[1]}),
            "phenotype_stratified_A_carrier_swap_capacity": cap,
        })
    return {
        "original_adults": ORIGINAL_N,
        "original_source_alleles_sha256": sha256(decoded["alleles"]).hexdigest(),
        "distinct_expressed_M_I_A_strata": len(out),
        "original_I_heterozygote_adults": sum(r["I_heterozygote_adults"] for r in out),
        "original_I_homozygote_adults": sum(r["I_homozygote_adults"] for r in out),
        "exact_matched_A_carrier_swap_capacity_with_I_original": sum(
            r["phenotype_stratified_A_carrier_swap_capacity"] for r in out),
        "all_strata_I_status_pure": all(
            r["phenotype_stratified_A_carrier_swap_capacity"] == 0 for r in out),
        "m0_to_m12_without_rewriting_I_is_feasible_under_this_control": (
            sum(r["phenotype_stratified_A_carrier_swap_capacity"] for r in out) >= 12),
        "strata": out,
    }


def report(d: dict) -> dict:
    blocks = {
        name: one_block(name,d["original_founders"][name]["source_state_arrays"])
        for name in BLOCKS
    }
    result = {
        "schema": "chapter2_q2_original_t0_phenotype_matched_carriage_swap_bound_v1",
        "status": "AUTHENTICATED_OLD_T0_STATIC_CONSTRAINT_NO_NEW_BIOLOGY",
        "frozen_original_t0_git_blob": SOURCE_GIT_BLOB,
        "original_model3_biology_commit": ORIGINAL_MODEL_COMMIT,
        "blocks": blocks,
        "full_genome_model3_future_updates": 0,
        "simulated_new_offspring": 0,
        "new_independent_source_genomes": 0,
        "matched_control_definition": (
            "I homologs fixed exactly as in original t0; adult M/I/A expression fixed per ID; "
            "A symmetric heterozygote carriers may be reassigned only within groups of exactly "
            "equal expressed M/I/A, preserving A-carrier counts in each phenotype group between arms."),
        "interpretation_limits": [
            "For this exact within-phenotype-stratum swap, the largest possible change in "
            "I/A carrier overlap is sum over groups min(I-heterozygote, I-homozygote counts).",
            "An m=0 to m=12 contrast is unavailable in EITHER of the two authenticated source "
            "genomes under unchanged I homologs and this phenotype-stratum matching rule.",
            "This is not a proof that other synthetic interventions or statistical balancing "
            "schemes cannot produce m12; they would change genetic context, t0 controls, or both.",
            "Exactly matched parental return law and the complete F1 marginals of a future "
            "intervention still need source-pinned native calculation; this capacity is only "
            "a necessary matching constraint, not proof of sufficiency.",
            "Repeated phenotypes/genes in original Model3 t0 are simulation sources, "
            "not a measured mainland allele-frequency or true independent island sample.",
            "Old published A-width pilot is a DIFFERENT genetic intervention and is not "
            "an estimate of a co-carriage effect, genetic speed mediation or Q4 persistence.",
        ],
    }
    if (blocks["main"]["original_I_heterozygote_adults"] != 24
            or blocks["confirmation"]["original_I_heterozygote_adults"] != 30
            or blocks["main"]["exact_matched_A_carrier_swap_capacity_with_I_original"] != 0
            or blocks["confirmation"]["exact_matched_A_carrier_swap_capacity_with_I_original"] != 6
            or blocks["main"]["distinct_expressed_M_I_A_strata"] != 8
            or blocks["confirmation"]["distinct_expressed_M_I_A_strata"] != 5):
        raise ValueError("Expected original t0 source heterozygosity/phenotype stratum drift")
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.check and args.write:
        parser.error("Choose --check or --write")
    result = json.dumps(report(load_original()),ensure_ascii=False,indent=2,allow_nan=False) + "\n"
    if args.check:
        if OUTPUT.read_text(encoding="utf-8") != result:
            raise SystemExit("FAIL: committed summary differs from original typed founder arrays")
        print("PASS: both original typed t0 blocks and their source-stratified overlap bounds agree")
    elif args.write:
        if OUTPUT.exists():
            raise FileExistsError("Do not overwrite a frozen scientific readout")
        OUTPUT.parent.mkdir(parents=True,exist_ok=True)
        with OUTPUT.open("x",encoding="utf-8",newline="\n") as stream:
            stream.write(result)
        print("WROTE: original-source co-carriage feasibility readout")
    else:
        print(result, end="")


if __name__=="__main__":
    main()
