"""Read-only cohort/RNG independence admission for Chapter 2.

A numeric seed belongs to a biological stream namespace (visitor history,
demographic population, founder genotype, bootstrap) and source generator.
Reject an *executed* visitor-history independence claim if two executed cohorts
share generator+visitor identities. Deliberately matched RNG within the same
experiment and a new-demographic-only validation are not violations.

The explicit ledger is seven high-impact archived designs, NOT a certification
that every historic design or offsite research script is independent.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs/CHAPTER2_COHORT_SEED_LEDGER_20261016.json"


def seed_ids(raw: dict | None) -> set[int]:
    if raw is None:
        return set()
    if not isinstance(raw, dict) or ("ids" in raw) == ("first" in raw):
        raise ValueError("RNG identities require exactly an explicit ids list or first/last")
    if "ids" in raw:
        values = raw["ids"]
        if not isinstance(values, list):
            raise ValueError("RNG identities must be a list")
    else:
        if set(raw) != {"first", "last"}:
            raise ValueError("RNG identity range must declare first and last")
        start, stop = raw["first"], raw["last"]
        if (type(start) is not int or type(stop) is not int
                or start < 0 or stop < start or stop - start > 200000):
            raise ValueError("Invalid RNG identity range")
        values = list(range(start, stop + 1))
    if not values or any(type(v) is not int or v < 0 for v in values):
        raise ValueError("RNG identities must be nonnegative exact integers")
    if len(values) != len(set(values)):
        raise ValueError("Repeated RNG identities inside one cohort namespace")
    return set(values)


def _range(document: dict, key: str) -> set[int]:
    entry = document[key]
    first = "first" if "first" in entry else "first_seed"
    last = "last" if "last" in entry else "last_seed"
    return seed_ids({"first": entry[first], "last": entry[last]})


def _declared_design_seeds(record: dict, data: dict, designs: dict[str, dict]):
    ident = record["id"]
    if ident == "fhs_discovery_20261003":
        if data["source"]["histories"] != 128:
            raise ValueError("Historical discovery visitor-history count changed")
        # Original visitor identities are declared in its prospective matched
        # demographic successor, which explicitly identifies 74001–74128.
        successor = designs["fhs_new_demography_20261003"]
        if successor["validation_source"]["history_seeds"] != (
            "all original 128 visitor histories 74001-74128"
        ):
            raise ValueError("Historic visitor seed source pointer changed")
        return set(range(74001, 74129)), set(range(101, 109)), set()
    if ident == "fhs_new_demography_20261003":
        value = data["validation_source"]
        if value["history_seeds"] != "all original 128 visitor histories 74001-74128":
            raise ValueError("New-demography experiment incorrectly claims new visitor histories")
        return set(range(74001, 74129)), set(value["new_demographic_seeds"]), set()
    if ident == "fhs_new_visitor_retired_20261003":
        value = data["validation_source"]
        return set(value["history_seeds"]), set(value["new_demographic_seeds"]), set()
    if ident == "fhs_new_visitor_20261004":
        value = data["execution"]
        return set(value["visitor_history_seeds"]), set(value["demographic_seeds"]), set()
    if ident == "q1_single_founder_20261006":
        d = data["main_campaign"]
        return _range(d, "visitor_history_seeds"), _range(d, "demographic_repeat_seeds"), {d["founder_seed"]}
    if ident == "q1_new_founders_20261016":
        return (_range(data, "visitor_histories"),
                {data["demography"]["repeat_seed"]},
                _range(data, "founder_genomes"))
    if ident == "q4_island_independent32_20261008":
        return (_range(data, "independent_visitor_histories"),
                set(data["demographic_repeat_seeds"]), {74001})
    raise ValueError("Unadmitted cohort type: " + ident)


def _verify_registry_documents(rows: list, root: Path) -> dict:
    seen = set()
    docs = {}
    for r in rows:
        name = r["id"]
        if name in seen:
            raise ValueError("Duplicate registered cohort id: " + name)
        seen.add(name)
        path = root / r["design"]
        if not path.is_file():
            raise ValueError("Missing source design: " + r["design"])
        docs[name] = json.loads(path.read_text(encoding="utf-8"))
    return docs


def _documented_outcome(r: dict, d: dict, root: Path) -> dict:
    status = r["execution"]
    if status == "superseded_before_execution":
        if r.get("result") is not None or d.get("status") != status:
            raise ValueError("Superseded design incorrectly contains a result")
        if d.get("supersession", {}).get("outcomes_generated_under_earlier_design") is not False:
            raise ValueError("Supersession lacks explicit zero original outcomes")
        if not r.get("superseded_by"):
            raise ValueError("Superseded design is missing successor")
        return {"state": status, "result": None}
    if status != "completed":
        raise ValueError("Unsupported inferred execution state (no automatic assumptions)")
    target = r.get("result")
    if not isinstance(target, str) or not (root / target).is_file():
        raise ValueError("Executed cohort must have a real result locator: " + r["id"])
    if target.endswith(".json"):
        result = json.loads((root / target).read_text(encoding="utf-8"))
        recorded = result.get("design")
        if recorded is not None and recorded != r["design"]:
            raise ValueError("Cohort result design pointer differs: " + r["id"])
        declared_status = result.get("status")
        if not isinstance(declared_status, str) or not (
            "complete" in declared_status or "passed" in declared_status
        ):
            raise ValueError("Claimed executed result is not an admitted completion: " + r["id"])
    elif target.endswith(".md"):
        content = (root / target).read_text(encoding="utf-8")
        if "38853989138" not in content or "1,088" not in content:
            raise ValueError("Missing original source run for new founder cohort")
    else:
        raise ValueError("Unknown result representation for " + r["id"])
    return {"state": status, "result": target}


def _pool(r: dict, name: str) -> set[int]:
    return seed_ids(r.get(name))


def audit_registry(document: dict, root: Path = ROOT) -> dict:
    if document.get("schema") != "chapter2_cohort_seed_independence_v1":
        raise ValueError("Unknown independence registry schema")
    rows = document["cohorts"]
    if not isinstance(rows, list) or len(rows) < 7:
        raise ValueError("Missing required cohort records")
    docs = _verify_registry_documents(rows, root)
    by_id = {r["id"]: r for r in rows}
    expanded = {}
    cohorts = []
    for row in rows:
        ident = row["id"]
        source = docs[ident]
        stored = [_pool(row, name) for name in (
            "visitor_seeds", "demographic_seeds", "founder_seeds")]
        declared = _declared_design_seeds(row, source, docs)
        if not all(a == b for a, b in zip(stored, declared)):
            raise ValueError("Registry seeds do not match frozen source design: " + ident)
        evidence = _documented_outcome(row, source, root)
        if not row.get("visitor_generator") or not row.get("scientific_role"):
            raise ValueError("RNG namespace and scientific role must be explicit")
        expanded[ident] = {"visitor": stored[0], "demographic": stored[1], "founder": stored[2]}
        cohorts.append({
            "id": ident, "execution": evidence["state"], "source_design": row["design"],
            "result": evidence["result"],
            "visitor_generator": row["visitor_generator"],
            "visitor_count": len(stored[0]),
            "demographic_seed_count": len(stored[1]),
            "founder_seed_count": len(stored[2]),
            "scientific_role": row["scientific_role"],
        })
    for row in rows:
        if row["execution"] == "superseded_before_execution":
            parent = row["superseded_by"]
            if parent not in by_id or by_id[parent]["execution"] != "completed":
                raise ValueError("Superseded registry entry has no executed successor")
            old = docs[row["id"]]
            if old["superseded_by"] != by_id[parent]["design"]:
                raise ValueError("Supersession chain does not match source")
            if (old["supersession"]["canonical_design_commit_utc"]
                    >= old["supersession"]["first_validation_workflow_started_utc"]):
                raise ValueError("Canonical source design was not frozen before execution")
            for dim in ("visitor", "demographic"):
                if expanded[row["id"]][dim] != expanded[parent][dim]:
                    raise ValueError("Superseded and canonical randomized cohort differ")
    overlaps = []
    for left, right in combinations(rows, 2):
        aid, bid = left["id"], right["id"]
        la, lb = expanded[aid], expanded[bid]
        same_gen = left["visitor_generator"] == right["visitor_generator"]
        vh = la["visitor"] & lb["visitor"] if same_gen else set()
        dem = la["demographic"] & lb["demographic"]
        founders = la["founder"] & lb["founder"]
        both_executed = left["execution"] == right["execution"] == "completed"
        intentional = (aid in right.get("intentional_visitor_sharing_with", [])
                       or bid in left.get("intentional_visitor_sharing_with", []))
        if vh and both_executed and not intentional:
            raise ValueError("Two executed cohorts reuse visitor histories without matching declaration: "
                             + aid + " / " + bid)
        for source, target, first, second in (
            (left, right, la, lb), (right, left, lb, la)):
            if target["id"] in source.get("claims_independent_visitor_from", []) and same_gen:
                if first["visitor"] & second["visitor"]:
                    raise ValueError("False independent visitor-history claim: " + source["id"])
            if target["id"] in source.get("claims_independent_demography_from", []):
                if first["demographic"] & second["demographic"]:
                    raise ValueError("False independent demographic RNG claim: " + source["id"])
            if target["id"] in source.get("claims_independent_founder_from", []):
                if first["founder"] & second["founder"]:
                    raise ValueError("False independent founder-genome claim: " + source["id"])
            if target["id"] not in by_id:
                raise ValueError("Unknown comparison cohort")
        if vh or dem or founders:
            overlaps.append({
                "a": aid, "b": bid, "both_executed": both_executed,
                "same_visitor_generator": same_gen,
                "visitor_overlap": len(vh),
                "demographic_numeric_overlap": len(dem),
                "founder_numeric_overlap": len(founders),
                "intentional_visitor_matching": bool(vh and intentional),
                "does_not_count_as_two_independent_history_validations":
                    bool(vh) or not both_executed,
            })
    for row in rows:
        for key in ("claims_independent_visitor_from",
                    "claims_independent_demography_from",
                    "claims_independent_founder_from",
                    "intentional_visitor_sharing_with"):
            for related in row.get(key, []):
                if related not in by_id or related == row["id"]:
                    raise ValueError("Unknown or self-related seed cohort reference")
    for child in document.get("known_dependent_readouts", []):
        if child["parent_cohort"] not in by_id:
            raise ValueError("Secondary readout parent is missing")
        if not (root / child["path"]).is_file():
            raise ValueError("Registered secondary readout missing")
        if "same_" not in child["role"] and "not_independent" not in child["role"]:
            raise ValueError("Secondary readout must declare shared cohort status")
    return {
        "status": "PASS_EXPLICIT_COHORT_SEED_NAMESPACE_AUDIT",
        "executed_registered_cohorts": sum(r["execution"] == "completed" for r in rows),
        "superseded_without_outcomes": sum(r["execution"] == "superseded_before_execution" for r in rows),
        "cohorts": cohorts, "overlaps": overlaps,
        "dependent_readouts": document.get("known_dependent_readouts", []),
        "claim_limits": document["explicit_limits"],
    }


def _seed_descriptors(obj, prefix="", depth=0):
    if depth > 9:
        return []
    outputs = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            path = (prefix + "." + key).strip(".")
            if "seed" in key.lower():
                if isinstance(value, (int, str)) or isinstance(value, list):
                    count = len(value) if isinstance(value, list) else 1
                    outputs.append({"path": path, "type": type(value).__name__, "count": count})
                elif isinstance(value, dict) and {"first", "last"} <= set(value):
                    outputs.append({"path": path, "type": "inclusive_range",
                                    "count": value["last"] - value["first"] + 1})
            if isinstance(value, (dict, list)):
                outputs.extend(_seed_descriptors(value, path, depth+1))
    elif isinstance(obj, list):
        for n, value in enumerate(obj):
            if isinstance(value, (dict, list)):
                outputs.extend(_seed_descriptors(value, prefix + f"[{n}]", depth+1))
    return outputs


def scan_design_seed_fields(root: Path = ROOT) -> dict:
    """Inventory ALL design JSON seed field locations, no inferred independence."""
    designs = sorted((root / "data/design").glob("*.json"))
    rows, invalid = [], []
    for path in designs:
        rel = path.relative_to(root).as_posix()
        try:
            original = json.loads(path.read_text(encoding="utf-8"))
            occurrences = _seed_descriptors(original)
        except (ValueError, TypeError, KeyError, OSError) as exc:
            invalid.append({"path": rel, "error": str(exc)})
            continue
        if occurrences:
            rows.append({"path": rel, "status": original.get("status"),
                         "seed_fields": occurrences[:30],
                         "fields_truncated": max(0, len(occurrences)-30)})
    return {
        "json_design_files_scanned": len(designs),
        "designs_with_declared_seed_fields": len(rows),
        "invalid_json_designs": invalid,
        "seed_field_inventory": rows,
        "caution": "Paths/field names are a lexical inventory; it does NOT infer RNG stream independence, actual execution, or biological replicates.",
    }


def audit(root: Path = ROOT, registry: Path = LEDGER) -> dict:
    data = json.loads(registry.read_text(encoding="utf-8"))
    result = audit_registry(data, root)
    result["source_registry_sha256"] = hashlib.sha256(registry.read_bytes()).hexdigest()
    result["wider_design_inventory"] = scan_design_seed_fields(root)
    if result["wider_design_inventory"]["invalid_json_designs"]:
        raise ValueError("Source design JSON parse failure")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    options = parser.parse_args()
    if options.out.exists():
        raise FileExistsError("Refusing to overwrite signed cohort audit")
    report = audit()
    options.out.parent.mkdir(parents=True, exist_ok=True)
    options.out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": report["status"],
        "executed_registered_cohorts": report["executed_registered_cohorts"],
        "superseded_without_outcomes": report["superseded_without_outcomes"],
        "overlaps": report["overlaps"],
        "designs_with_seed_fields": report["wider_design_inventory"]["designs_with_declared_seed_fields"],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
