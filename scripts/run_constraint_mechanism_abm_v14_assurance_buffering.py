from __future__ import annotations

import argparse
import dataclasses
import importlib.util
import json
import random
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
V4_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v4_fixed_visit_budget.py"
V9_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v9_local_plant_opportunity.py"
V10_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v10_effective_service_dependency.py"
DESIGN = ROOT / "data/design/abm_v14_assurance_buffering_ablation_freeze.json"
DEFAULT_OUT = ROOT / "data/results/constraint_mechanism_abm_v14_assurance_buffering.json"

EPS = 1e-12
SATURATIONS = (1.0, 2.0, 3.0)
SUPPORT_STRENGTH = 0.5
QUALITY_STRENGTH = 1.0


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def disable_assurance(templates: list) -> list:
    return [
        dataclasses.replace(template, assurance_ceiling=0.0, assurance_responsiveness=0.0)
        for template in templates
    ]


def _delta(island: dict, mainland: dict, name: str, field: str) -> float:
    return float(island[name][field]) - float(mainland[name][field])


def _summarize(rows: list[dict]) -> dict:
    service_decline = [row for row in rows if row["service_decline"]]
    return {
        "lineage_contrasts": len(rows),
        "service_decline_lineages": len(service_decline),
        "synthetic_buffering_assurance_on": sum(row["synthetic_buffering_assurance_on"] for row in rows),
        "synthetic_buffering_assurance_off": sum(row["synthetic_buffering_assurance_off"] for row in rows),
        "assurance_sign_rescues": sum(row["assurance_sign_rescue"] for row in rows),
        "assurance_magnitude_rescues": sum(row["assurance_magnitude_rescue"] for row in rows),
        "mean_service_delta": mean(row["service_delta"] for row in rows) if rows else None,
        "mean_reproduction_delta_assurance_on": mean(row["reproduction_delta_assurance_on"] for row in rows) if rows else None,
        "mean_reproduction_delta_assurance_off": mean(row["reproduction_delta_assurance_off"] for row in rows) if rows else None,
        "mean_assurance_reproductive_rescue": mean(
            row["reproduction_delta_assurance_on"] - row["reproduction_delta_assurance_off"]
            for row in rows
        ) if rows else None,
        "service_decline_buffer_fraction_assurance_on": (
            sum(row["synthetic_buffering_assurance_on"] for row in service_decline) / len(service_decline)
            if service_decline else None
        ),
        "service_decline_buffer_fraction_assurance_off": (
            sum(row["synthetic_buffering_assurance_off"] for row in service_decline) / len(service_decline)
            if service_decline else None
        ),
    }


def build(
    *,
    replicates: int = 4,
    contexts: int = 4,
    n_lineages: int = 24,
    steps: int = 120,
    seed: int = 20260822,
) -> dict:
    v4 = load_module(V4_SCRIPT, "abm_v14_v4")
    v9 = load_module(V9_SCRIPT, "abm_v14_v9")
    v10 = load_module(V10_SCRIPT, "abm_v14_v10")

    rows: list[dict] = []
    upstream_mismatches = 0

    for saturation in SATURATIONS:
        for replicate in range(replicates):
            run_seed = seed + replicate + int(saturation * 10_000)
            templates_on = v4.make_lineages(random.Random(run_seed), n_lineages)
            templates_off = disable_assurance(templates_on)

            mainland_opportunity, _, _ = v9.run_weighted_network(
                0.0,
                run_seed,
                saturation,
                support_seed=run_seed + 31_000_000,
                support_strength=0.0,
                weight_seed=run_seed + 41_000_000,
                weight_strength=0.0,
                n_lineages=n_lineages,
                steps=steps,
            )
            island_opportunity, _, _ = v9.run_weighted_network(
                1.0,
                run_seed,
                saturation,
                support_seed=run_seed + 31_000_000,
                support_strength=0.0,
                weight_seed=run_seed + 41_000_000,
                weight_strength=0.0,
                n_lineages=n_lineages,
                steps=steps,
            )
            common = dict(
                v9=v9,
                saturation=saturation,
                support_strength=SUPPORT_STRENGTH,
                contexts=contexts,
                context_seed=run_seed + 51_000_000,
                quality_strength=QUALITY_STRENGTH,
            )
            mainland_on = v10.simulate_endpoint(
                mainland_opportunity,
                templates_on,
                quality_stream_offset=1_000_000,
                **common,
            )
            island_on = v10.simulate_endpoint(
                island_opportunity,
                templates_on,
                quality_stream_offset=2_000_000,
                **common,
            )
            mainland_off = v10.simulate_endpoint(
                mainland_opportunity,
                templates_off,
                quality_stream_offset=1_000_000,
                **common,
            )
            island_off = v10.simulate_endpoint(
                island_opportunity,
                templates_off,
                quality_stream_offset=2_000_000,
                **common,
            )

            for lineage_index in range(n_lineages):
                name = f"lineage_{lineage_index + 1}"
                service_delta_on = _delta(island_on, mainland_on, name, "mean_effective_service")
                service_delta_off = _delta(island_off, mainland_off, name, "mean_effective_service")
                if abs(service_delta_on - service_delta_off) > EPS:
                    upstream_mismatches += 1
                reproduction_on = _delta(island_on, mainland_on, name, "mean_reproduction")
                reproduction_off = _delta(island_off, mainland_off, name, "mean_reproduction")
                service_decline = service_delta_on < -EPS
                buffering_on = service_decline and reproduction_on >= -EPS
                buffering_off = service_decline and reproduction_off >= -EPS
                rows.append({
                    "saturation": saturation,
                    "replicate": replicate,
                    "lineage_index": lineage_index,
                    "service_delta": service_delta_on,
                    "reproduction_delta_assurance_on": reproduction_on,
                    "reproduction_delta_assurance_off": reproduction_off,
                    "service_decline": service_decline,
                    "synthetic_buffering_assurance_on": buffering_on,
                    "synthetic_buffering_assurance_off": buffering_off,
                    "assurance_sign_rescue": bool(buffering_on and reproduction_off < -EPS),
                    "assurance_magnitude_rescue": bool(
                        service_decline and reproduction_on > reproduction_off + EPS
                    ),
                    "mainland_final_assurance_on": float(mainland_on[name]["final_assurance"]),
                    "island_final_assurance_on": float(island_on[name]["final_assurance"]),
                    "dependency": float(island_on[name]["dependency"]),
                })

    by_saturation: dict[str, dict] = {}
    for saturation in SATURATIONS:
        subset = [row for row in rows if row["saturation"] == saturation]
        by_saturation[str(saturation)] = _summarize(subset)
    overall = _summarize(rows)

    if overall["assurance_sign_rescues"] > 0:
        decision = "existing_assurance_route_is_synthetically_sufficient_for_sign_level_buffering_in_frozen_model"
    elif overall["assurance_magnitude_rescues"] > 0:
        decision = "existing_assurance_route_changes_propagation_magnitude_but_no_sign_level_buffering_demonstrated"
    else:
        decision = "existing_assurance_route_does_not_generate_buffering_under_frozen_design"

    return {
        "analysis": "constraint_mechanism_abm_v14_assurance_buffering_ablation",
        "status": "full_frozen_matched_ablation_complete",
        "design": "data/design/abm_v14_assurance_buffering_ablation_freeze.json",
        "configuration": {
            "saturations": list(SATURATIONS),
            "replicates": replicates,
            "contexts": contexts,
            "lineages": n_lineages,
            "steps": steps,
            "seed": seed,
            "local_support_strength": SUPPORT_STRENGTH,
            "partner_effectiveness_strength": QUALITY_STRENGTH,
        },
        "upstream_service_identical_between_assurance_ablations": upstream_mismatches == 0,
        "upstream_service_mismatch_count": upstream_mismatches,
        "overall": overall,
        "by_saturation": by_saturation,
        "decision": decision,
        "empirical_mechanism_admission_changed": false,
        "hawaii_assurance_candidate_state": "candidate_only_no_abm_admission",
        "next_gate": (
            "Synthetic sufficiency, if present, does not admit assurance empirically. Keep the common buffer-mechanism admission interface unchanged and require a matched held-out/prospective empirical test before promotion."
        ),
        "claim_boundary": (
            "This matched ablation tests only synthetic capability of an existing ABM route. It does not validate Hawaiʻi, Guaiacum, Nicotiana, Issue #91, or a universal assurance mechanism."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replicates", type=int, default=4)
    parser.add_argument("--contexts", type=int, default=4)
    parser.add_argument("--lineages", type=int, default=24)
    parser.add_argument("--steps", type=int, default=120)
    parser.add_argument("--seed", type=int, default=20260822)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    result = build(
        replicates=args.replicates,
        contexts=args.contexts,
        n_lineages=args.lineages,
        steps=args.steps,
        seed=args.seed,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
