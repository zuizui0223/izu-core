"""Analyse public-image visual signatures with incomplete regime coverage.

Each taxon contributes to an available pairwise transition only. A complete
three-regime series is not required. Image rows are joined to geography only
after descriptors have been extracted into the blind table.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from channel_id.public_visual_signature import add_within_taxon_salience, summarize_group_signatures, transition_contrasts


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def require(rows: list[dict[str, str]], fields: set[str], label: str) -> None:
    if not rows:
        raise ValueError(f"{label} is empty")
    missing = sorted(fields - set(rows[0]))
    if missing:
        raise ValueError(f"{label} missing columns: {', '.join(missing)}")


def join(blind_path: Path, key_path: Path) -> list[dict[str, object]]:
    blind = read_csv(blind_path)
    key = read_csv(key_path)
    require(blind, {"image_id", "taxon", "analysis_group", "feature_status", "mean_saturation", "colourfulness", "radial_chroma_contrast", "hue_entropy", "edge_density"}, "blind feature table")
    require(key, {"image_id", "pollinator_regime"}, "feature key")
    keyed = {row["image_id"].strip(): row for row in key}
    if len(keyed) != len(key):
        raise ValueError("feature key has duplicate image_id")
    output: list[dict[str, object]] = []
    for row in blind:
        image_id = row["image_id"].strip()
        if image_id not in keyed:
            raise ValueError(f"blind feature row has no key: {image_id}")
        result: dict[str, object] = dict(row)
        result["pollinator_regime"] = keyed[image_id]["pollinator_regime"].strip()
        if row["feature_status"].strip() == "ok":
            for field in ("mean_saturation", "colourfulness", "radial_chroma_contrast", "hue_entropy", "edge_density"):
                result[field] = float(row[field])
        output.append(result)
    return output


def load_contract(path: Path) -> dict[tuple[str, str, str, str], dict[str, str]]:
    rows = read_csv(path)
    require(rows, {"scenario", "analysis_group", "feature_id", "transition", "allowed_directions", "rule_status", "interpretation"}, "signature contract")
    output: dict[tuple[str, str, str, str], dict[str, str]] = {}
    for row in rows:
        key = (row["scenario"].strip(), row["analysis_group"].strip(), row["feature_id"].strip(), row["transition"].strip())
        if key in output:
            raise ValueError(f"duplicate signature contract rule: {key}")
        output[key] = row
    return output


def assess(contrasts: list[dict[str, object]], contract: dict[tuple[str, str, str, str], dict[str, str]]) -> list[dict[str, object]]:
    scenarios = sorted({key[0] for key in contract})
    rows: list[dict[str, object]] = []
    for contrast in contrasts:
        for scenario in scenarios:
            key = (scenario, str(contrast["analysis_group"]), str(contrast["feature_id"]), str(contrast["transition"]))
            rule = contract.get(key)
            if rule is None:
                continue
            allowed = {item for item in rule["allowed_directions"].split("|") if item}
            observed = str(contrast["point_direction"])
            status = rule["rule_status"].strip()
            result = "not_identified" if status != "active" else ("supported" if observed in allowed else "contradicted")
            rows.append({
                "scenario": scenario, "taxon": contrast["taxon"], "analysis_group": contrast["analysis_group"],
                "transition": contrast["transition"], "delta_focal_minus_reference": contrast["delta_focal_minus_reference"],
                "bootstrap_ci90_low": contrast["bootstrap_ci90_low"], "bootstrap_ci90_high": contrast["bootstrap_ci90_high"],
                "point_direction": observed, "allowed_directions": "|".join(sorted(allowed)), "assessment": result,
                "interpretation": rule["interpretation"],
            })
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("\n", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)


def render(summary: dict[str, object], groups: list[dict[str, object]], assessments: list[dict[str, object]]) -> str:
    lines = [
        "# Public-image visual-signature audit", "",
        "Exploratory scale-free image-descriptor analysis. This is not an absolute size, guide anatomy, pollinator, or causal measurement.", "",
        "## Data recovery", "",
        f"- taxa in manifest: {summary['taxa_in_manifest']}",
        f"- images with descriptors: {summary['images_with_features']}",
        f"- taxa with any pairwise transition: {summary['taxa_with_any_transition']}",
        f"- first-transition contrasts: {summary['first_transition_contrasts']}",
        f"- second-transition contrasts: {summary['second_transition_contrasts']}",
        f"- endpoint contrasts: {summary['endpoint_contrasts']}", "",
        "## Taxon-level summary", "",
        "| group | transition | taxa | median delta | decrease | flat | increase |", "|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in groups:
        lines.append(f"| {row['analysis_group']} | {row['transition']} | {row['taxa_contributing']} | {float(row['median_taxon_delta']):.3f} | {row['taxa_decrease']} | {row['taxa_flat']} | {row['taxa_increase']} |")
    scores = Counter((row["scenario"], row["assessment"]) for row in assessments)
    lines.extend(("", "## Contract decisions", "", "| scenario | supported | contradicted | not identified |", "|---|---:|---:|---:|"))
    for scenario in sorted({row["scenario"] for row in assessments}):
        lines.append(f"| {scenario} | {scores[(scenario, 'supported')]} | {scores[(scenario, 'contradicted')]} | {scores[(scenario, 'not_identified')]} |")
    lines.extend(("", "## Boundary", "", "Taxa, not images, are the aggregation unit. An incomplete taxon is retained only for its observed pairwise transition. Apparent signatures require later validation against source tables or hand-audited subsets."))
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blind-features", type=Path, required=True)
    parser.add_argument("--key", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--min-images-per-regime", type=int, default=2)
    parser.add_argument("--bootstrap-draws", type=int, default=500)
    parser.add_argument("--tolerance", type=float, default=0.25)
    args = parser.parse_args()
    if args.min_images_per_regime <= 0 or args.bootstrap_draws <= 0 or args.tolerance < 0:
        raise SystemExit("invalid analysis threshold")
    manifest = read_csv(args.manifest)
    require(manifest, {"taxon"}, "manifest")
    joined = add_within_taxon_salience(join(args.blind_features, args.key))
    contrasts = transition_contrasts(joined, args.min_images_per_regime, args.bootstrap_draws, args.tolerance)
    groups = summarize_group_signatures(contrasts)
    assessments = assess(contrasts, load_contract(args.contract))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir / "visual_fingerprint_joined.csv", joined)
    write_csv(args.output_dir / "visual_signature_transition_contrasts.csv", contrasts)
    write_csv(args.output_dir / "visual_signature_group_summary.csv", groups)
    write_csv(args.output_dir / "visual_signature_contract_assessments.csv", assessments)
    summary = {
        "taxa_in_manifest": len(manifest),
        "images_with_features": sum(str(row.get("feature_status")) == "ok" for row in joined),
        "taxa_with_any_transition": len({str(row["taxon"]) for row in contrasts}),
        "first_transition_contrasts": sum(row["transition"] == "large_to_ardens" for row in contrasts),
        "second_transition_contrasts": sum(row["transition"] == "ardens_to_no_bombus" for row in contrasts),
        "endpoint_contrasts": sum(row["transition"] == "large_to_no_bombus" for row in contrasts),
        "boundary": "Exploratory public-image signature layer. Taxa, not images, are the analysis unit; descriptors are not validated floral trait measurements.",
    }
    (args.output_dir / "visual_signature.summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "PUBLIC_VISUAL_SIGNATURE_REPORT.md").write_text(render(summary, groups, assessments), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":n    main()
