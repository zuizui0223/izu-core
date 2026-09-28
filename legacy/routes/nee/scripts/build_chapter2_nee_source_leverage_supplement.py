from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOO = ROOT / "data/results/chapter2_natural_regime_six_source_all_loo_diagnostic_20260915.json"
CHALLENGE = ROOT / "data/results/chapter2_natural_regime_source_robustness_challenge_closure_20260915.json"
REVIEW_CLOSURE = ROOT / "data/results/chapter2_postfreeze_code_review_closure_20260923.json"
OUT = ROOT / "docs/CHAPTER2_NEE_SUPPLEMENTARY_SOURCE_LEVERAGE_20260915.md"

SOURCE_LABELS = {
    "aslan_etal_2019_hawaii_native_pollination": "Hawaii (Aslan et al. 2019)",
    "cyrille_etal_2025_martinique_gardens": "Martinique (Cyrille 2025)",
    "euppollnet_31_roberts_england_step": "England STEP / Great Britain",
    "lara_romero_etal_2019_tenerife_pollination": "Tenerife (Lara-Romero et al. 2019)",
    "lazaro_etal_2022_mallorca_stability": "Mallorca (Lázaro et al. 2022)",
    "serra_marin_etal_2025_cabrera_pollination": "Cabrera (Serra-Marin et al. 2025)",
}


def fmt(x: float) -> str:
    return f"{x:.3f}"


def build() -> str:
    loo = json.loads(LOO.read_text(encoding="utf-8"))
    challenge = json.loads(CHALLENGE.read_text(encoding="utf-8"))
    review = json.loads(REVIEW_CLOSURE.read_text(encoding="utf-8"))
    phi = review["phi_timebin_sensitivity"]

    lines: list[str] = []
    lines.append("# Supplementary source-leverage and redundancy diagnostics")
    lines.append("")
    lines.append("This supplement reports diagnostics that are deliberately stricter than the frozen primary routing rule. The primary six-source natural-regime plane and its prespecified largest-source leave-out rule are unchanged. These diagnostics quantify where source-specific leverage remains and document a prospectively frozen attempt to reduce that leverage without opening candidate coordinates prematurely.")
    lines.append("")
    lines.append("## Supplementary Table 1 | Leave-one-study-out source leverage")
    lines.append("")
    lines.append("| Excluded source study | Systems remaining | D1 q90/q10 | phi q90-q10 | Interior occupancy | Absolute Spearman(log D1, phi) | All frozen dispersion criteria pass? |")
    lines.append("|---|---:|---:|---:|---:|---:|:---:|")
    for row in loo["all_source_leave_one_out"]:
        s = row["summary"]
        label = SOURCE_LABELS[row["excluded_source"]]
        lines.append(
            f"| {label} | {row['systems_remaining']} | {fmt(s['D1_q90_q10_ratio'])} | "
            f"{fmt(s['phi_q90_q10_span'])} | {fmt(s['interior_occupancy'])} | "
            f"{fmt(abs(s['weighted_spearman_logD1_phi']))} | {'yes' if row['nee_dispersion_criteria_pass'] else 'no'} |"
        )
    lines.append("")
    full = loo["full_summary"]
    lines.append(
        "The full six-source plane contains 42 systems. Source-balanced D1 q90/q10 = "
        f"{fmt(full['D1_q90_q10_ratio'])}, phi span = {fmt(full['phi_q90_q10_span'])}, "
        f"interior occupancy = {fmt(full['interior_occupancy'])}, and absolute Spearman = "
        f"{fmt(abs(full['weighted_spearman_logD1_phi']))}."
    )
    lines.append("")
    lines.append(
        "Two exclusions are load-bearing under the stricter all-source diagnostic using the original source-native schedules. Removing England STEP reduces synchrony dispersion below the frozen numerical floor (phi span = 0.162). Removing Martinique reduces joint-interior occupancy below the frozen numerical floor (0.188), although breadth dispersion remains >2. These diagnostics were calculated after the primary route decision and do not redefine that decision."
    )
    lines.append("")
    lines.append("## Supplementary Table 1b | Equal-depth six-bin synchrony sensitivity")
    lines.append("")
    full_diag = phi["full_data"]
    primary = phi["six_bin_phi_only_primary"]
    joint = phi["six_bin_joint_coordinate_secondary"]
    lines.append(
        "A later code review identified a sampling-depth concern: across the 42 admitted systems, full-data `phi` correlated negatively with time-bin count "
        f"(`rho_s={full_diag['spearman_phi_vs_time_bins']:.3f}`; for `rho_eq`, `rho_s={full_diag['spearman_rho_eq_vs_time_bins']:.3f}`). "
        "Before executing the sensitivity, all systems were frozen to repeated rarefaction to six distinct source-native bins, with 1,000 requested iterations and the original partner identities, source weights and NEE dispersion thresholds retained. "
        f"Of 1,000 iterations, {phi['valid_iterations']} were valid."
    )
    lines.append("")
    lines.append("| Sensitivity quantity | Result |")
    lines.append("|---|---:|")
    lines.append(f"| All-source phi-only dispersion criteria pass | {100*primary['all_source_dispersion_pass_fraction']:.1f}% |")
    lines.append(f"| England-excluded all four dispersion criteria pass | {100*primary['england_removed_all_criteria_pass_fraction']:.1f}% |")
    lines.append(f"| England-excluded phi-span criterion pass | {100*primary['england_removed_phi_span_pass_fraction']:.1f}% |")
    lines.append(f"| Six-bin phi-span median | {primary['phi_span_median']:.3f} |")
    lo, hi = primary["phi_span_95_interval"]
    lines.append(f"| Six-bin phi-span 95% interval | {lo:.3f}–{hi:.3f} |")
    lines.append(f"| Joint-coordinate all-source criteria pass | {100*joint['all_source_dispersion_pass_fraction']:.1f}% |")
    lines.append("")
    england = {row["system_id"]: row for row in phi["england_systems"]}
    lines.append(
        "England itself remained highly synchronous after rarefaction: "
        f"Carlisle median `phi={england['Carlisle']['rarefied_phi_median']:.3f}` (full {england['Carlisle']['original_phi']:.3f}), "
        f"Livingstone_far {england['Livingstone_far']['rarefied_phi_median']:.3f} (full {england['Livingstone_far']['original_phi']:.3f}), "
        f"and Livingstone_house {england['Livingstone_house']['rarefied_phi_median']:.3f} (full {england['Livingstone_house']['original_phi']:.3f}). "
        "Thus England's high values are not explained by having only eight source-native rounds. At the same time, the failure of the original England-deletion span is not robust to equal temporal depth: other sources move upward when reduced to six bins, so the apparent uniqueness of the England high-synchrony edge is partly a sampling-depth property. Because this small-T perturbation itself shifts `phi`, the rarefied plane is retained strictly as a sensitivity analysis and does not replace the full-data primary coordinates."
    )
    lines.append("")
    lines.append("## Supplementary Table 2 | Prospectively frozen source-redundancy challenge")
    lines.append("")
    lines.append("| Rank | Candidate | Disposition before coordinate extraction | D1 or phi opened? |")
    lines.append("|---:|---|---|:---:|")
    for row in challenge["candidate_sequence"]:
        disposition = row["disposition"].replace("_", " ").lower()
        lines.append(
            f"| {row['rank']} | {row['candidate']} | {disposition} | {'yes' if row['coordinate_opened'] else 'no'} |"
        )
    lines.append("")
    lines.append(
        "The redundancy challenge was frozen before reopened coordinate extraction. Candidate order, admission rules, coordinate definitions, source balancing and dispersion thresholds were fixed in advance. All four candidates closed before D1 or phi extraction, so no candidate values were available for selection. The challenge therefore did not remove the England dependence and was closed without expanding the source universe further."
    )
    lines.append("")
    lines.append("## Scale bridge: natural D1 is not synthetic k")
    lines.append("")
    lines.append(
        "Synthetic k is the nominal number of exchangeable model components, and synthetic k_eff is the variance-equivalent effective independence implied by k and correlation. Natural Hill D1 is instead the effective diversity of pooled, effort-standardized partner interaction shares. No numerical D1-to-k or D1-to-k_eff mapping is estimated or used, and no natural analogue of the synthetic k≈4 crossover is claimed. The theory-to-data connection is structural only: partner breadth and temporal synchrony are measured separately because a single second-moment compression need not preserve nonlinear response-relevant information."
    )
    lines.append("")
    lines.append("## Interpretation boundary")
    lines.append("")
    lines.append(
        "These diagnostics support a deliberately narrow inference. The full-data natural plane demonstrates a broad, empirically occupied two-dimensional context space under the frozen measurement contract. Under the original schedules, that coverage is source-complementary rather than leave-any-source-out invariant; under equal six-bin depth, England-excluded synchrony coverage is usually restored, showing that source leverage and temporal sampling depth are partially confounded. Great Britain retains the pre-existing EuPPollNet island-study classification; it is not reclassified from its effect on the route. Failed or unavailable candidate sources are data-eligibility outcomes, not biological negatives."
    )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    text = build()
    OUT.write_text(text, encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
