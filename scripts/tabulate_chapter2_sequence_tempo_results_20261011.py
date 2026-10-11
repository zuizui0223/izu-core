"""Render factual tables from an official complete tempo readout, never raw cases.

This temporary presentation helper neither runs biology nor recalculates inference.
It preserves source metric names, all settings/sample times, conditional support,
and the official descriptive intervals. Null values display as NA; observed zero as0.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
import math
from pathlib import Path

STATUS = "COMPLETE_SYNTHETIC_TEMPORAL_SEQUENCE_OUTCOME_SOURCE_ONLY_NOT_NATURAL_ECOLOGY"
TIMES = (0, 10, 20, 40, 60, 80, 100, 120, 200, 300)
CATEGORIES = ("A_first", "I_first", "near_simultaneous", "A_only", "I_only", "neither")
FIELDS = ("median", "n_evaluated", "n_boundary", "n_positive", "n_negative", "n_near_zero")
SECONDARY_FIELDS = ("mean_abrupt", "mean_gradual", "mean_abrupt_on_paired_support",
                    "mean_gradual_on_paired_support", "abrupt_minus_gradual",
                    "descriptive_history_profile_bootstrap95", "bootstrap_nonempty_resamples",
                    "eligible_abrupt_trajectories", "eligible_gradual_trajectories",
                    "eligible_paired_trajectories", "eligible_abrupt_profiles",
                    "eligible_gradual_profiles", "eligible_paired_profiles", "profile_support")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def reject_nonfinite(value):
    raise ValueError(f"Nonstandard JSON numeric value: {value}")


def number(value, scale=1):
    if value is None:
        return "NA"
    require(isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value),
            "Expected a finite numeric source value or null")
    value *= scale
    return "0" if value == 0 else format(value, ".10g")


def interval(value, scale=1):
    if value is None:
        return "NA"
    require(isinstance(value, list) and len(value) == 2, "Missing two-sided source interval")
    return f"[{number(value[0], scale)}, {number(value[1], scale)}]"


def count_from_probability(value):
    require(isinstance(value, (int, float)) and 0 <= value <= 1, "Invalid category probability")
    observed = value * 64
    require(abs(observed - round(observed)) < 1e-8, "Category is not an integer count out of64")
    return str(round(observed))


def table(headers, rows):
    def cell(value):
        return str(value).replace("|", "\\|").replace("\n", " ")
    lines = ["| " + " | ".join(map(cell, headers)) + " |",
             "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(map(cell, row)) + " |" for row in rows)
    return "\n".join(lines) + "\n"


def setting(block):
    return f"{block['timing']} / {number(block['direct_assurance_cost'])} / {number(block['mutation_rate'])}"


def primary_table(blocks, metrics):
    rows = []
    for block in blocks:
        for name in metrics:
            metric = block["outcomes"][name]
            rows.append((setting(block), f"`{name}`", metric["horizon_updates"],
                         number(metric["P_abrupt"], 100), number(metric["P_gradual"], 100),
                         number(metric["abrupt_minus_gradual"], 100),
                         interval(metric["descriptive_history_profile_bootstrap95"], 100)))
    return table(("Setting", "Source metric", "Horizon (updates)", "P_abrupt (%)", "P_gradual (%)",
                  "abrupt_minus_gradual (pp)", "Descriptive95CI (pp)"), rows)


def support(metric, arm):
    return f"{metric['eligible_' + arm + '_trajectories']} / {metric['eligible_' + arm + '_profiles']}"


def secondary_table(blocks, names):
    rows = []
    for block in blocks:
        for name in names:
            metric = block["secondary_endpoints"][name]
            rows.append((setting(block), f"`{name}`", number(metric["mean_abrupt"]),
                         number(metric["mean_gradual"]), number(metric["mean_abrupt_on_paired_support"]),
                         number(metric["mean_gradual_on_paired_support"]), number(metric["abrupt_minus_gradual"]),
                         interval(metric["descriptive_history_profile_bootstrap95"]),
                         support(metric, "abrupt"), support(metric, "gradual"), support(metric, "paired"),
                         metric["bootstrap_nonempty_resamples"]))
    return table(("Setting", "Source metric", "mean_abrupt", "mean_gradual", "mean_abrupt_on_paired_support",
                  "mean_gradual_on_paired_support", "abrupt_minus_gradual", "Descriptive95CI",
                  "Abrupt support (trajectories / profiles)", "Gradual support (trajectories / profiles)",
                  "Paired support (trajectories / profiles)", "Nonempty bootstrap resamples"), rows)


def validate(readout):
    require(readout.get("status") == STATUS, "Only official complete-source readouts may be tabulated")
    require((readout["total_verified_trajectory_cases"], readout["n_independent_synthetic_visitor_profiles"],
             readout["n_nested_demographic_replicates_per_profile"], readout["n_paired_setting_blocks"]) ==
            (1024, 16, 4, 8), "Complete1024-case/16-profile/4-repeat/8-setting readout required")
    require(readout["bootstrap"]["draws"] == 9999 and readout["bootstrap"]["seed"] == 48272026 and
            readout["bootstrap"]["percentile_tails"] == [.025, .975], "Registered descriptive bootstrap differs")
    blocks = readout["results"]
    expected = {(timing, cost, mu) for timing in ("delayed", "prior") for cost in (0, .5) for mu in (0, .01)}
    require(len(blocks) == 8 and {(b["timing"], b["direct_assurance_cost"], b["mutation_rate"]) for b in blocks} == expected,
            "All eight unique treatment settings required")
    names = set(blocks[0]["secondary_endpoints"])
    for block in blocks:
        require(block["independent_synthetic_visitor_profile_units"] == 16 and block["nested_repeats_per_profile"] == 4,
                "Setting denominators differ")
        require(set(block["secondary_endpoints"]) == names, "Secondary source fields differ across settings")
        for name, metric in block["secondary_endpoints"].items():
            require(set(SECONDARY_FIELDS) <= metric.keys(), f"Incomplete secondary source endpoint: {name}")
            require(len(metric["profile_support"]) == 16, f"Missing original profile support: {name}")
            for arm in ("abrupt", "gradual", "paired"):
                require(0 <= metric["eligible_" + arm + "_trajectories"] <= 64 and
                        0 <= metric["eligible_" + arm + "_profiles"] <= 16, f"Invalid support count: {name}")
    return sorted(blocks, key=lambda b: (b["timing"] == "prior", b["direct_assurance_cost"], b["mutation_rate"]))


def render(readout, source_path, raw_hash, complete_readout_link):
    blocks = validate(readout)
    link = complete_readout_link or "sandbox:" + str(source_path.resolve())
    lines = ["# Draft factual tables — complete frozen tempo cohort\n",
             "This draft transcribes the official complete readout. It adds no biological interpretation, inference, or simulations.\n",
             f"Source JSON SHA256: `{raw_hash}`. Status: `{readout['status']}`.\n",
             f"Design SHA256: `{readout['design_sha256']}`. Executable source identity SHA256: `{readout['verified_source_identity_sha256']}`.\n",
             "Denominators:1024 trajectories;16 independent synthetic profiles;4 nested demographic repeats;8 settings;64 trajectories per arm within each setting.\n",
             "Setting column: mating timing / direct assurance cost / mutation rate. Primary probabilities are percentages; schedule differences and their intervals are percentage points (pp).\n",
             "All intervals below are the source's two-sided descriptive percentile intervals:9999 profile resamples, seed48272026, tails .025/.975. NA denotes a source null; observed zero displays as0.\n",
             "For secondary endpoints, mean_abrupt and mean_gradual use their separately eligible arm support. The paired-support means and paired contrast use only jointly eligible repeats, averaged first within profile. Support cells show eligible trajectories / eligible profiles. Counts/medians for sampled gradients are source profile averages, not pooled counts of sampled plants.\n",
             f"[Complete readout and per-endpoint profile_support arrays]({link}). All source secondary fields are included below; the16-profile arrays are retained in that linked readout.\n",
             "## Primary registered crossing probabilities by100\n",
             primary_table(blocks, ("A_crossed_by100", "I_crossed_by100")),
             "## Unconditional occupancy\n", primary_table(blocks, ("persistence100", "persistence400"))]
    for horizon in (100, 400):
        rows = []
        for block in blocks:
            counts = {arm: [] for arm in ("abrupt", "gradual")}
            for category in CATEGORIES:
                name = category + "_by100" if horizon == 100 else category
                metric = block["outcomes"][name]
                require(metric["horizon_updates"] == horizon, "Source category horizon mismatch")
                for arm in counts:
                    counts[arm].append(int(count_from_probability(metric["P_" + arm])))
                rows.append((setting(block), f"`{name}`", counts["abrupt"][-1], counts["gradual"][-1]))
            require(all(sum(values) == 64 for values in counts.values()), "Six categories must partition64 cases per arm")
        lines.extend((f"## Six order categories by{horizon}: observed counts out of64 per arm\n",
                      table(("Setting", "Source category", "Abrupt count /64", "Gradual count /64"), rows)))
    lag = ("A_minus_I_crossing_lag_by400",)
    genetics = tuple(f"{trait}_{statistic}_at{t}" for t in (10, 100, 400)
                     for trait in ("X", "I", "A") for statistic in ("mean", "variance"))
    series = tuple(f"{source}_{statistic}" for source in
                   ("pollen_delivery", "functional_overlap", "expected_I_change_pre_mutation", "expected_A_change_pre_mutation")
                   for statistic in ("mean", "min", "max"))
    recruitment = ("resident_selfed_recruits_total", "resident_outcross_recruits_total",
                   "resident_selfed_recruit_fraction", "parentage_updates_available", "parentage_recorded_recruits_total")
    gradients = tuple(f"gradient_{trait}_{field}_at{t}" for t in TIMES
                      for trait in ("investment", "assurance") for field in FIELDS)
    for title, names in (("Conditional A-minus-I onset lag by400 (updates)", lag),
                         ("X/I/A means and variances at10/100/400", genetics),
                         ("Original time-series summary quantities", series),
                         ("Original realized recruitment and parentage quantities", recruitment),
                         ("Fixed-time sampled gradients: all10 times, both traits, all8 settings", gradients)):
        lines.extend(("## " + title + "\n", secondary_table(blocks, names)))
    expected_names = set(lag + genetics + series + recruitment + gradients)
    additional = sorted(set(blocks[0]["secondary_endpoints"]) - expected_names)
    if additional:
        lines.extend(("## Additional official secondary source fields\n", secondary_table(blocks, additional)))
    lines.append("## Source metadata\n")
    lines.append(f"Secondary fields per setting: {len(blocks[0]['secondary_endpoints'])}; sampled gradient source fields per setting: {len(gradients)}.\n")
    lines.append("Execution runtime identity, as recorded in the source readout:\n\n```json\n" +
                 json.dumps(readout["execution_runtime_identity"], indent=2, sort_keys=True) + "\n```\n")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--readout", type=Path, required=True, help="Official complete uncompressed JSON; never a raw-case directory")
    parser.add_argument("--out", type=Path, required=True, help="New draft Markdown path")
    parser.add_argument("--complete-readout-link", help="Optional actual compressed-readout URL or Markdown target")
    args = parser.parse_args()
    require(args.readout.is_file(), "Official full JSON file required")
    require(args.out.resolve() != args.readout.resolve(), "Cannot overwrite the source readout")
    raw = args.readout.read_bytes()
    readout = json.loads(raw, parse_constant=reject_nonfinite)
    draft = render(readout, args.readout, sha256(raw).hexdigest(), args.complete_readout_link)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8") as stream:
        stream.write(draft)
    print(json.dumps({"status": "DRAFT_FACTUAL_TABLES_FROM_OFFICIAL_COMPLETE_READOUT",
                      "source_sha256": sha256(raw).hexdigest(), "output": str(args.out.resolve())}, sort_keys=True))


if __name__ == "__main__":
    main()
