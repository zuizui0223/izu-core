"""Fail-closed parentage add-on to legacy Izu linked field-chain audit.

This auditor checks traceability and probability bookkeeping. It does NOT
run genotype parentage inference, validate the genotype error model, authorize
field work, or certify evolutionary selection. Output statuses are structural.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "data/design/izu_parentage_bridge_template_20261010.json"
SCHEMA = "izu_parentage_extension_v1"
HEX = set("0123456789abcdef")
REQUIRED = ("site_admissions", "chain_plants", "fruits", "offspring",
            "candidate_fathers", "assignments")


def digest_ok(s):
    return isinstance(s, str) and len(s) == 64 and all(c in HEX for c in s.lower())


def flag(v):
    return v is True or (isinstance(v, str) and v.strip().lower() in ("true", "yes"))


def nonblank(v):
    return isinstance(v, str) and bool(v.strip())


def _unique(rows, fields, errors, label):
    out = {}
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"{label}[{i}]: non-object")
            continue
        key = tuple(row.get(x) for x in fields)
        if any(not nonblank(x) for x in key):
            errors.append(f"{label}[{i}]: missing key {fields}")
            continue
        if key in out:
            errors.append(f"{label}: duplicate {key}")
        else:
            out[key] = row
    return out


def audit(d):
    if not isinstance(d, dict) or d.get("schema") != SCHEMA:
        raise ValueError("unrecognized parentage bridge schema")
    for field in REQUIRED:
        if not isinstance(d.get(field), list):
            raise ValueError(f"{field} must be a list")
    mode = d.get("evidence_mode")
    if mode not in ("template", "synthetic_test", "field_claimed"):
        raise ValueError("evidence_mode must be template/synthetic_test/field_claimed")
    errors = []
    sites = _unique(d["site_admissions"], ("block_id",), errors, "site")
    chain = _unique(d["chain_plants"], ("block_id", "plant_id"),
                    errors, "chain plant")
    fruits = _unique(d["fruits"], ("fruit_id",), errors, "fruit")
    offspring = _unique(d["offspring"], ("seed_id",), errors, "offspring")
    father_panel = _unique(d["candidate_fathers"],
                           ("pool_id", "father_id"), errors, "father panel")
    assign = defaultdict(list)

    for key, row in sites.items():
        block = key[0]
        if row.get("admission_status") not in ("candidate", "admitted", "excluded"):
            errors.append(f"block {block}: invalid admission status")
        if not nonblank(row.get("pool_id")):
            errors.append(f"block {block}: missing candidate-father pool")
        if row.get("admission_status") == "admitted":
            for f in ("r1_audit_ref", "permit_evidence_ref", "access_evidence_ref"):
                if not nonblank(row.get(f)):
                    errors.append(f"block {block}: no independently referenced {f}")
    for key, row in chain.items():
        if (row.get("block_id"),) not in sites:
            errors.append(f"chain plant {key}: unknown block")
        if not nonblank(row.get("source_chain_row_ref")):
            errors.append(f"chain plant {key}: missing legacy chain provenance")
        # A 'full_chain_plant' declaration is imported from the legacy audit,
        # not inferred from parentage or made true by this validator.
    for key, row in fruits.items():
        fid = key[0]
        ck = (row.get("block_id"), row.get("plant_id"))
        if ck not in chain:
            errors.append(f"fruit {fid}: no linked chain plant")
        if row.get("treatment_type") not in (
                "open_pollinated", "bagged_autonomous", "supplemental_outcross"):
            errors.append(f"fruit {fid}: unknown flower treatment")
        n = row.get("mature_seed_count")
        if isinstance(n, bool) or not isinstance(n, int) or n < 0:
            errors.append(f"fruit {fid}: mature_seed_count must be >=0 integer")
        if not nonblank(row.get("source_fruit_row_ref")):
            errors.append(f"fruit {fid}: missing source fruit provenance")
    for key, row in father_panel.items():
        if not nonblank(row.get("sample_id")):
            errors.append(f"father {key}: missing physical sample reference")
        if not digest_ok(row.get("genotype_sha256")):
            errors.append(f"father {key}: missing valid genotype SHA-256")
    tested_per_fruit = Counter()
    usable_ids = set()
    for key, row in offspring.items():
        sid = key[0]
        fid = row.get("fruit_id")
        fr = fruits.get((fid,))
        if fr is None:
            errors.append(f"offspring {sid}: parent fruit not registered")
            continue
        if (row.get("block_id"), row.get("plant_id")) != (
                fr.get("block_id"), fr.get("plant_id")):
            errors.append(f"offspring {sid}: block/mother does not match fruit")
        if fr.get("treatment_type") != "open_pollinated":
            errors.append(f"offspring {sid}: paternity samples only from open_pollinated fruits")
        tested_per_fruit[fid] += 1
        status = row.get("assay_status")
        if status not in ("usable", "failed", "pending"):
            errors.append(f"offspring {sid}: invalid assay_status")
        if status == "usable":
            usable_ids.add(sid)
            if not digest_ok(row.get("genotype_sha256")) or not nonblank(
                    row.get("genotyping_batch_id")):
                errors.append(f"offspring {sid}: usable requires genotype bytes provenance")
    for (fid,), row in fruits.items():
        n = row.get("mature_seed_count")
        if isinstance(n, int) and not isinstance(n, bool) and n >= 0:
            if tested_per_fruit[fid] > n:
                errors.append(f"fruit {fid}: offspring sampled > mature seed count")
    for i, row in enumerate(d["assignments"]):
        if not isinstance(row, dict):
            errors.append(f"assignments[{i}]: non-object")
            continue
        sid, category = row.get("seed_id"), row.get("category")
        if sid not in usable_ids:
            errors.append(f"assignment {sid}: only a genotyped usable seed can be assigned")
            continue
        if category not in ("self", "named_father", "unsampled_or_unknown"):
            errors.append(f"assignment {sid}: bad category")
            continue
        p = row.get("posterior_probability")
        if isinstance(p, bool) or not isinstance(p, (float, int)) or not math.isfinite(p) or not 0 <= p <= 1:
            errors.append(f"assignment {sid}: invalid posterior")
            continue
        father = row.get("father_id")
        if category == "named_father":
            site = sites.get((offspring[(sid,)].get("block_id"),))
            pool = site.get("pool_id") if site else None
            if not nonblank(father) or (pool, father) not in father_panel:
                errors.append(f"assignment {sid}: father absent from genotyped candidate pool")
            if father == offspring[(sid,)].get("plant_id"):
                errors.append(f"assignment {sid}: mother must be represented as 'self'")
        elif father not in (None, ""):
            errors.append(f"assignment {sid}: non-named category cannot carry father ID")
        assign[sid].append(row)
    for sid in usable_ids:
        rows = assign.get(sid, [])
        labels = [(r.get("category"), r.get("father_id")) for r in rows]
        if len(set(labels)) != len(labels):
            errors.append(f"assignment {sid}: duplicate posterior category/father")
        if sum(r.get("category") == "self" for r in rows) != 1 or sum(
                r.get("category") == "unsampled_or_unknown" for r in rows) != 1:
            errors.append(f"assignment {sid}: must preserve explicit self AND unsampled/unknown")
        mass = sum(float(r["posterior_probability"]) for r in rows
                   if isinstance(r.get("posterior_probability"), (int, float)))
        if abs(mass - 1) > 1e-6:
            errors.append(f"assignment {sid}: posterior mass {mass} != 1")
    method = d.get("parentage_method") or {}
    refs = d.get("source_receipts") or {}
    model_ready = bool(
        nonblank(method.get("model_id"))
        and flag(method.get("genotyping_error_model_documented"))
        and flag(method.get("unsampled_fathers_modelled"))
        and flag(method.get("maternal_genotypes_verified"))
        and digest_ok(method.get("paternity_likelihood_report_sha256"))
    )
    receipt_ready = all(digest_ok(refs.get(k)) for k in (
        "chain_audit_sha256", "site_registry_audit_sha256",
        "parentage_genotype_archive_sha256", "parentage_model_report_sha256"))
    records = []
    for key, row in chain.items():
        block, mother = key
        ss = sites.get((block,), {})
        seeds = [s for (s_id,), s in offspring.items() if (
            s.get("block_id"), s.get("plant_id")) == key]
        usable = [s for s in seeds if s.get("seed_id") in usable_ids]
        valid = [s for s in usable if s.get("seed_id") in assign and not any(
            f"assignment {s['seed_id']}:" in err for err in errors)]
        structurally_linked = bool(
            flag(row.get("full_chain_plant")) and
            flag(row.get("predeclared_block")) and
            len(usable) > 0 and len(valid) == len(usable) and
            model_ready and receipt_ready and
            ss.get("admission_status") == "admitted")
        summary = {"block_id":block,"plant_id":mother,
                   "n_seed_assayed":len(seeds),
                   "n_seed_usable":len(usable),
                   "n_seed_failed":sum(s.get("assay_status") == "failed" for s in seeds),
                   "n_seed_pending":sum(s.get("assay_status") == "pending" for s in seeds),
                   "parentage_structurally_linked":structurally_linked,
                   "expected_self_fraction_among_genotyped":None,
                   "expected_unsampled_fraction_among_genotyped":None,
                   "expected_named_father_fractions_among_genotyped":None}
        if valid:
            den=len(valid)
            summary["expected_self_fraction_among_genotyped"]=sum(
                next((float(a["posterior_probability"]) for a in assign[s["seed_id"]]
                      if a["category"] == "self"), 0) for s in valid)/den
            summary["expected_unsampled_fraction_among_genotyped"]=sum(
                next((float(a["posterior_probability"]) for a in assign[s["seed_id"]]
                      if a["category"] == "unsampled_or_unknown"), 0) for s in valid)/den
            fathers = defaultdict(float)
            for s in valid:
                for a in assign[s["seed_id"]]:
                    if a["category"] == "named_father":
                        fathers[a["father_id"]] += a["posterior_probability"]/den
            summary["expected_named_father_fractions_among_genotyped"] = dict(sorted(fathers.items()))
        records.append(summary)
    if errors:
        status="INVALID_DATA_OR_LINKAGE"
    elif not d["offspring"]:
        status="NO_FIELD_OFFSPRING_DATA"
    elif mode=="synthetic_test":
        status="SYNTHETIC_SCHEMA_CHECK_ONLY"
    elif mode=="template":
        status="TEMPLATE_NOT_FIELD_EVIDENCE"
    elif records and all(r["parentage_structurally_linked"] for r in records):
        status="STRUCTURALLY_LINKED_OBSERVED_PARENTAGE_NOT_CAUSAL"
    else:
        status="FIELD_PARENTAGE_GATE_BLOCKED"
    return {"status":status,"schema":SCHEMA,"evidence_mode":mode,
            "n_blocks":len(sites),"n_registered_mothers":len(chain),
            "n_sampled_seeds":len(offspring),"n_usable_seeds":len(usable_ids),
            "n_structurally_linked_mothers":sum(r["parentage_structurally_linked"] for r in records),
            "site_admission_is_external":True,
            "paternity_algorithm_not_executed":True,
            "errors":errors,"mother_rows":records,
            "boundary":"Offspring posterior fractions are conditional on genotyped seeds, not all mature seeds or realized offspring fitness. They cannot certify natural selection or population persistence."}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest",type=Path,default=TEMPLATE)
    parser.add_argument("--out",type=Path)
    args=parser.parse_args()
    result=audit(json.loads(args.manifest.read_text(encoding="utf-8")))
    blob=json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n"
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(blob,encoding="utf-8")
    print(blob,end="")
    raise SystemExit(2 if result["errors"] else 0)


if __name__=="__main__":
    main()
