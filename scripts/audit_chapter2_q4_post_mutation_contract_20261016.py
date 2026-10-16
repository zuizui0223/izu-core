"""Fail-closed source/design admission for the frozen Q4 independent-32 producer.

This module does NOT run evolution or modify the 2026-10-08 producer. The
archived producer uses pre_mutation_rate for *both* the 400-update preparation
and the 80-update challenge, although its frozen design records two fields.
Equality of those two values is essential to reproducing the original result.

A changed post rate needs a separately versioned producer and source-locked
experiment, not silent reuse of historical results.
"""
from __future__ import annotations

import argparse
import ast
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_island_demographic_independent32_20261008.json"
PRODUCER = ROOT / "scripts/run_chapter2_island_demographic_independent32.py"


def _subscript_name(node: ast.AST) -> tuple[str, str] | None:
    if (isinstance(node, ast.Subscript)
            and isinstance(node.value, ast.Name)
            and isinstance(node.slice, ast.Constant)
            and isinstance(node.slice.value, str)):
        return node.value.id, node.slice.value.value
    return None


def admit(design: dict, producer_source: str) -> dict:
    """Verify what the *historical source actually does*, then assert design.

    Source-structural assertions intentionally fail if the frozen producer is
    refactored. A new producer implementation needs a new explicit contract.
    """
    if design.get("status") != "frozen_before_new_history_demographic_confirmation":
        raise ValueError("Q4: unrecognized frozen experiment status")
    if design.get("pre_mutation_rate") != design.get("post_mutation_rate"):
        raise ValueError(
            "Q4: historical source ignores post_mutation_rate during its "
            "future-80 updates; pre/post mutation rates must match exactly. "
            "Create a new versioned producer and design for unequal rates."
        )
    rate = design.get("pre_mutation_rate")
    if (isinstance(rate, bool) or not isinstance(rate, (int, float))
            or not math.isfinite(rate) or not 0 <= rate <= 1):
        raise ValueError("Q4: invalid mutation probability")
    tree = ast.parse(producer_source)
    run_group = next(
        (n for n in tree.body if isinstance(n, ast.FunctionDef)
         and n.name == "run_group"), None,
    )
    if run_group is None:
        raise ValueError("Q4: historical run_group function not found")

    before = []
    after = []
    for node in ast.walk(run_group):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        call = node.value
        if not isinstance(target, ast.Name) or not isinstance(call, ast.Call):
            continue
        if (target.id == "cfg" and isinstance(call.func, ast.Name)
                and call.func.id == "config"):
            before.append(call)
        if (target.id == "post_cfg" and isinstance(call.func, ast.Name)
                and call.func.id == "replace"):
            after.append(call)
    if len(before) != 1 or len(after) != 1:
        raise ValueError("Q4: producer configuration constructors changed")
    init = before[0]
    if len(init.args) != 4 or _subscript_name(init.args[2]) != ("d", "pre_mutation_rate"):
        raise ValueError("Q4: producer pre-rate binding changed")
    post = after[0]
    if (len(post.args) != 1 or not isinstance(post.args[0], ast.Name)
            or post.args[0].id != "cfg"):
        raise ValueError("Q4: producer post-state no longer inherits pre-config")
    kw = {x.arg: x.value for x in post.keywords}
    if ("mutation_rate" in kw or set(kw) != {"capacity", "ovule_budget"}
            or _subscript_name(kw["capacity"]) != ("d", "post_capacity")):
        raise ValueError("Q4: post-rate or demographic source changed")
    if (not any(
            isinstance(n, ast.Call)
            and isinstance(n.func, ast.Name) and n.func.id == "advance"
            and len(n.args) > 3 and isinstance(n.args[3], ast.Name)
            and n.args[3].id == "post_cfg"
            for n in ast.walk(run_group))):
        raise ValueError("Q4: future advance no longer uses post_cfg")
    return {
        "status": "PASS_FROZEN_Q4_PRE_POST_MUTATION_RATE_IDENTITY",
        "effective_original_pre_rate": float(rate),
        "effective_original_future_rate": float(rate),
        "future_A_evolvability": "continues original mode during 80 updates",
        "claim_limit": (
            "Checks a frozen source/design identity only; cannot isolate "
            "historical A allele legacy or externally validate island persistence."
        ),
    }


def audit() -> dict:
    return admit(
        json.loads(DESIGN.read_text(encoding="utf-8")),
        PRODUCER.read_text(encoding="utf-8"),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    print(json.dumps(audit(), indent=2))


if __name__ == "__main__":
    main()
