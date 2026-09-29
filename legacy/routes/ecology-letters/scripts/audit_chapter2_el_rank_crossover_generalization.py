from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_el_rank_crossover_generalization_freeze_20260912.json"
OUT = ROOT / "data/results/chapter2_el_rank_crossover_generalization_20260912.json"


def exact_components(*, a: float, b: float, c: float, var_x: float, var_z: float, k: int, rho: float) -> dict:
    var_zbar = var_z * (rho + (1.0 - rho) / k)
    starting = a * a * var_x
    community = b * b * var_zbar
    interaction = c * c * var_x * var_zbar
    total = starting + community + interaction
    return {
        "k": k,
        "rho": rho,
        "var_zbar": var_zbar,
        "starting": starting,
        "community": community,
        "interaction": interaction,
        "total": total,
        "starting_fraction": starting / total,
        "community_fraction": community / total,
        "interaction_fraction": interaction / total,
        "starting_exceeds_community": starting > community,
    }


def build() -> dict:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    if design.get("status") != "frozen_before_generic_audit_execution":
        raise ValueError("generic EL audit design is not frozen")

    cfg = design["generic_exact_audit"]
    rows = []
    for rho in cfg["rho_values"]:
        for k in cfg["k_values"]:
            rows.append(
                exact_components(
                    a=float(cfg["a"]),
                    b=float(cfg["b"]),
                    c=float(cfg["c"]),
                    var_x=float(cfg["x_variance"]),
                    var_z=float(cfg["z_variance"]),
                    k=int(k),
                    rho=float(rho),
                )
            )

    by_rho = {}
    for rho in cfg["rho_values"]:
        selected = [row for row in rows if row["rho"] == float(rho)]
        by_rho[str(rho)] = {
            "rows": selected,
            "starting_constant": max(row["starting"] for row in selected) == min(row["starting"] for row in selected),
            "community_strictly_decreases": all(
                b["community"] < a["community"] for a, b in zip(selected, selected[1:])
            ),
            "interaction_positive_all_finite_k": all(row["interaction"] > 0 for row in selected),
            "first_k_starting_exceeds_community": next(
                (row["k"] for row in selected if row["starting_exceeds_community"]), None
            ),
        }

    independent = by_rho["0.0"]
    correlated_high = by_rho["0.4"]
    checks = {
        "independent_starting_constant": independent["starting_constant"],
        "independent_community_strictly_decreases": independent["community_strictly_decreases"],
        "independent_interaction_positive_all_finite_k": independent["interaction_positive_all_finite_k"],
        "independent_crosses_after_k1": independent["first_k_starting_exceeds_community"] not in (None, 1),
        "rho_0_4_no_crossover_in_grid": correlated_high["first_k_starting_exceeds_community"] is None,
    }
    if not all(checks.values()):
        raise RuntimeError(f"predeclared generic checks failed: {checks}")

    a = float(cfg["a"])
    b = float(cfg["b"])
    var_x = float(cfg["x_variance"])
    var_z = float(cfg["z_variance"])
    exact_independent_threshold = (b * b * var_z) / (a * a * var_x)
    rho_critical = (a * a * var_x) / (b * b * var_z)

    return {
        "schema_version": "1.0",
        "analysis": "chapter2_el_rank_crossover_generalization",
        "status": "generic_exact_audit_complete",
        "design": DESIGN.relative_to(ROOT).as_posix(),
        "rows": rows,
        "summaries": by_rho,
        "checks": checks,
        "derived_quantities": {
            "independent_exact_crossover_requires_k_greater_than": exact_independent_threshold,
            "correlation_floor_prevents_asymptotic_crossover_when_rho_at_least": rho_critical,
        },
        "interpretation": {
            "general_sufficient_condition": "realization-driven variance averages down faster than a nonzero mean-community starting-state contrast",
            "countercondition": "shared correlated stochasticity can leave a community-variance floor that prevents rank reversal",
            "field_mapping": "effective stochastic independence, not raw richness or raw system size, is the relevant scaling coordinate",
        },
        "claim_boundary": design["claim_boundary"],
    }


def main() -> None:
    payload = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"checks": payload["checks"], "derived_quantities": payload["derived_quantities"]}, indent=2))


if __name__ == "__main__":
    main()
