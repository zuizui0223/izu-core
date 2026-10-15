"""Read-only, source-bound Ch2 asymmetry audit for novelty assessment.

No new model trajectory, historic causal mechanism, independent validation,
or priority claim. Reuses frozen JSON and an explicitly one-repeat checkpoint
audit. Does not fetch the raw ZIPs or replace their independent source checks.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/results"
GENERALITY = DATA / "chapter2_assurance_generality_20261006.json"
ARMS = DATA / "chapter2_assurance_attenuation_decomposition_20261006.json"
GRADIENT = DATA / "chapter2_assurance_gradient_components_20261006.json"
CHECKPOINTS = ROOT / "docs/CHAPTER2_FAR_ASSURANCE_ORIGINAL_GENOME_PRICE_AUDIT_20261015.md"
SETTINGS = ("delayed_control", "prior_selfing", "pollen_discount", "assurance_cost")


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _rows(table: str, start: str, stop: str) -> dict[str, list[str]]:
    if start not in table or stop not in table:
        raise AssertionError("checkpoint source section missing")
    part = table.split(start, 1)[1].split(stop, 1)[0]
    rows = {}
    for line in part.splitlines():
        if not line.startswith("|"):
            continue
        cells = [col.strip() for col in line.strip().strip("|").split("|")]
        if cells[0] in SETTINGS:
            if cells[0] in rows:
                raise AssertionError(f"duplicate {cells[0]} in checkpoint table")
            rows[cells[0]] = cells[1:]
    if set(rows) != set(SETTINGS):
        raise AssertionError(f"incomplete checkpoint table: {sorted(rows)}")
    return rows


def audit() -> dict:
    original = _json(GENERALITY)
    arms = _json(ARMS)
    gradient = _json(GRADIENT)
    if (
        original["status"] != "complete_generality_readout"
        or original["adjudication"]["status"] != "all_four_confirmed"
        or original["adjudication"]["n_passed"] != 4
        or original["independent_visitor_histories"] != 64
        or original["declared_cases"] != 8448
        or original["structural_control"]["matched_pairs_checked"] != 128
        or original["structural_control"]["mismatches"]
        or arms["source_cases_verified"] != 8448
        or arms["independent_visitor_histories"] != 64
        or gradient["independent_visitor_histories"] != 64
        or len(original["settings"]) != 4
        or len(arms["settings"]) != 4
        or original["design_sha256"] != arms["source_design_sha256"]
        or original["design_sha256"] != gradient["source_design_sha256"]
    ):
        raise AssertionError("frozen 4-setting experiment provenance failed")

    gr400 = {r["setting"]: r for r in gradient["rows"] if r["snapshot"] == 400}
    arc = {r["setting"]: r for r in arms["settings"]}
    gen = {r["setting"]: r for r in original["settings"]}
    if set(gr400) != set(SETTINGS) or set(arc) != set(SETTINGS) or set(gen) != set(SETTINGS):
        raise AssertionError("missing original 4-setting records")

    checkpoint_doc = CHECKPOINTS.read_text(encoding="utf-8")
    early = _rows(
        checkpoint_doc,
        "### 1. When does the endpoint contrast arise?",
        "### 2. Do the actual parents' inherited genetic returns align with the far-positive endpoint?",
    )
    price = _rows(
        checkpoint_doc,
        "### 2. Do the actual parents' inherited genetic returns align with the far-positive endpoint?",
        "### 3. Native zero-visitor factorization and A–I association",
    )
    out = []
    for setting in SETTINGS:
        a = arc[setting]["estimates"]
        p = gen[setting]
        near = a["evolution_effect_near"]
        far = a["evolution_effect_far"]
        fixed_far_founder = a["fixed_far_investment_change"]["mean"]
        evolved_far_founder = a["evolving_far_investment_change"]["mean"]
        contrast = a["attenuation"]
        static_near = gr400[setting]["assurance_effect_high_minus_low"]["near"]["gradient"]["mean"]
        static_far = gr400[setting]["assurance_effect_high_minus_low"]["far"]["gradient"]["mean"]
        if not (
            near["mean"] < 0 < far["mean"]
            and near["bootstrap95"][1] < 0 < far["bootstrap95"][0]
            and fixed_far_founder < 0
            and evolved_far_founder < 0
            and static_near < static_far < 0
            and abs(far["mean"] - near["mean"] - contrast["mean"]) < 1e-10
            and abs(contrast["mean"] - p["attenuation_evolving_minus_fixed"]["mean"]) < 1e-10
            and contrast["bootstrap95"][0] > 0
        ):
            raise AssertionError(f"source mean, interval, or different-estimand gate: {setting}")
        if len(early[setting]) != 6 or len(price[setting]) != 4:
            raise AssertionError(f"one-repeat original checkpoint format changed: {setting}")
        cp = [float(v) for v in early[setting]]
        # early: near t200, t400, t1000; far t200, t400, t1000
        if not (cp[1] < 0 and all(v > 0 for v in cp[3:])):
            raise AssertionError(f"one-repeat trait trajectory check: {setting}")
        # price: far t200, far t400, original absent-visitors count, A-align t400
        price200, price400 = float(price[setting][0]), float(price[setting][1])
        if price400 >= 0:
            raise AssertionError(f"t400 conditional one-step Price effect sign: {setting}")
        if price[setting][2] != "50/64":
            raise AssertionError(f"zero-visitor count changed: {setting}")
        out.append({
            "setting": setting,
            "main_64history_8repeat_evolving_minus_fixed_near": near["mean"],
            "main_64history_8repeat_evolving_minus_fixed_far": far["mean"],
            "main_far_fixed_I_change_from_founder": fixed_far_founder,
            "main_far_evolving_I_change_from_founder": evolved_far_founder,
            "main_64history_8repeat_differential_attenuation": contrast["mean"],
            "static_assurance_higher_minus_lower_gradient_near_t400": static_near,
            "static_assurance_higher_minus_lower_gradient_far_t400": static_far,
            "source_64history_1repeat_far_EminusF_t200": cp[3],
            "source_64history_1repeat_far_EminusF_t400": cp[4],
            "source_64history_1repeat_far_EminusF_t1000": cp[5],
            "source_64history_1repeat_far_conditional_Price_EminusF_t200": price200,
            "source_64history_1repeat_far_conditional_Price_EminusF_t400": price400,
        })

    return {
        "status": "retrospective_source_crosswalk_not_causal_attribution",
        "checks_passed": len(out),
        "main_inference_unit": "64 visitor histories per setting, 8 nested demographic repeats",
        "checkpoint_inference_unit": "64 original visitor histories, 1 of 8 original demographic repeats",
        "new_evolutionary_trajectories": 0,
        "findings": out,
        "claim_ceiling": [
            "near and far are both pollen-limited synthetic visitor regimes, not mainland/island",
            "far E-F positive is RELATIVE to fixed-A, not positive investment evolution from founder",
            "rare-mutant A-to-I coupling, one-step Price, and endpoint E-F are distinct estimands",
            "negative t400 conditional Price does not negate positive earlier/later level contrasts",
            "t200/t400 checkpoint results have only one nested demographic repeat",
            "the historical cause of positive far E-F is not identified",
            "prior-art novelty/priority cannot be proven by this numeric crosswalk",
        ],
    }


def main() -> None:
    print(json.dumps(audit(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
