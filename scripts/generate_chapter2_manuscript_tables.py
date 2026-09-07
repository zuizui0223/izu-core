from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE12 = ROOT / "data/results/chapter2_phase12_fixed_gate_summary_20260827.json"
PHASE3 = ROOT / "data/results/context_assurance_threshold_maps_gate_frozen_20260827.json"
WHY_DIAGNOSTICS = ROOT / "data/results/chapter2_conditional_why_diagnostics_frozen_20260827.json"
RELATIONAL = ROOT / "data/results/chapter2_relational_robustness_audit_frozen_20260831.json"
IZU_AUDIT = ROOT / "data/results/izu_signed_position_structural_audit_frozen_20260827.json"
EXTERNAL_READINESS = ROOT / "data/results/chapter2_external_prediction_readiness_frozen_20260828.json"
WORLD_CLOSURE = ROOT / "data/results/chapter2_world_saturation_manuscript_closure_20260906.json"
SUBMISSION_MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260831.json"
CONTEMPORARY = ROOT / "data/predictive_meta/hiraiwa_ushimaru_continuous_functional_exposure.json"
POLLEN = ROOT / "data/predictive_meta/hiraiwa_ushimaru_matching_to_pollen_heterogeneity.json"
OUT = ROOT / "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_TABLES_20260827.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _validate_sources() -> None:
    p12 = load(PHASE12)
    p3 = load(PHASE3)
    why = load(WHY_DIAGNOSTICS)
    relational = load(RELATIONAL)
    izu = load(IZU_AUDIT)
    external = load(EXTERNAL_READINESS)
    closure = load(WORLD_CLOSURE)
    manifest = load(SUBMISSION_MANIFEST)
    contemporary = load(CONTEMPORARY)
    pollen = load(POLLEN)

    rg = p12["response_geometry"]
    jt = p12["joint_transition_surface"]
    assert rg["matched_pollinator_realizations"] == 96
    assert rg["mixed_sign_realizations"] == 41
    assert jt["class_counts"] == {
        "mixed_mean_geometry": 16,
        "all_positive_mean_geometry": 22,
        "all_negative_mean_geometry": 10,
    }
    assert p3["context_map"]["lineages_with_any_sign_change"] == 737
    assert p3["assurance_map"]["eligible_baseline_declines"] == 580
    assert p3["assurance_map"]["lineages_with_any_sign_rescue"] == 0
    assert all(why["frozen_identity_checks"].values())

    assert relational["status"] == "frozen_complete_20260831"
    assert relational["seed_ensemble"]["community_realization_fraction_range"] == [
        0.6933825278526522,
        0.8017383395125494,
    ]
    zero = next(row for row in relational["trait_adjustment_context"] if row["trait_adjustment"] == 0.0)
    assert zero["realization_class_counts"]["mixed_sign"] == 64
    assert relational["equal_initial_pollinator_richness"]["realization_class_counts"]["mixed_sign"] == 53

    assert round(izu["raw_matching"]["slope"], 4) == 0.5669
    assert izu["null_corrected_matching"]["supported"] is False
    assert izu["island_center_assignment"]["n_exact_assignments"] == 120
    assert izu["island_center_assignment"]["n_assignments_ge_observed"] == 13

    assert external["formal_evaluation_gate"]["passed"] is False
    assert closure["formal_identifiability"] == {
        "research_entries": 25,
        "exact_geographic_labels": 21,
        "full_contracts": "0_of_25",
        "formal_external_prediction": "not_evaluable",
        "reopened": False,
    }
    assert closure["descriptive_breadth"]["research_entries"] == 42
    assert closure["descriptive_breadth"]["exact_geographic_labels"] == 37
    saturation = manifest["world_saturation_and_izu_continuity"]
    assert saturation["large_island_saturation_rule_met"] is True
    assert saturation["consecutive_zero_novelty_tranches"] == 2
    assert saturation["small_island_direct_historical_partner_loss"] == "0_of_8"
    assert saturation["small_island_direct_partner_arrival_reintroduction"] == "1_of_8"
    assert saturation["small_island_full_contracts"] == "0_of_8"

    assert contemporary["fixed_effect_subsets"]["izu_five_islands"]["fdq_coefficient"] == 1.94255840267522
    assert contemporary["fixed_effect_subsets"]["post_oshima_four_islands"]["fdq_coefficient"] == 2.0589617769543915
    assert contemporary["leave_one_site_sensitivity"]["izu_five_islands"]["all_positive"] is True
    assert contemporary["leave_one_site_sensitivity"]["post_oshima_four_islands"]["all_positive"] is True
    assert pollen["site_season_cluster_inference"]["izu_five_islands"]["tm_coefficient"] == 0.03528541439362961
    assert pollen["site_season_cluster_inference"]["post_oshima_four_islands"]["tm_coefficient"] == 0.03415875775284886


TABLES = """# Chapter 2 Supporting Tables

Updated: 2026-09-07

These tables are supporting material for the active Oikos manuscript. Main-text figures carry the inferential argument; the tables below preserve exact model settings, sensitivity summaries, structural attacks, world-saturation provenance and contemporary Izu diagnostics.

Synthetic frequencies and thresholds are design/sensitivity descriptors, not natural prevalence or field-calibrated thresholds. The Izu analyses are source-locked observational secondary analyses and do not identify historical pollinator-loss causation.

## Table S1. Baseline scenario and lineage parameterization

| Quantity | Mainland-like | Oceanic-island | Status |
| --- | ---: | ---: | --- |
| Initial pollinator types | 9 | 4 | generic island-direction scenario |
| Partner arrival probability / step | 0.28 | 0.12 | generic island-direction scenario |
| Partner loss probability / extant partner / step | 0.015 | 0.055 | generic island-direction scenario |
| Pollinator trait dispersion | 0.22 | 0.16 | generic sensitivity choice |
| Generalist fraction | 0.35 | 0.58 | generic island-direction scenario |
| Replacement fraction | 0.05 | 0.22 | generic island-direction scenario |
| Generalist breadth | 0.42 | 0.42 | generic matching choice |
| Specialist breadth | 0.16 | 0.16 | generic matching choice |
| Replacement match multiplier | 0.82 | 0.82 | generic matching choice |

| Lineage/design quantity | Value | Status |
| --- | --- | --- |
| Initial functional trait | truncated Normal(0.5, 0.18) | generic sensitivity choice |
| Pollinator dependency | Uniform(0.35, 0.95) | generic sensitivity choice |
| Assurance ceiling | Uniform(0.10, 0.90) | generic sensitivity choice |
| Assurance responsiveness | Uniform(0.004, 0.035) | generic sensitivity choice |
| Trait-adjustment scale | Uniform(0.01, 0.055) | generic sensitivity choice |
| Initial assurance state | 0.08 | generic sensitivity choice |
| Lineages | 24 | design choice |
| Historical baseline steps | 120 | design choice |
| Saturation | 1, 2, 3 | sensitivity values |

## Table S2. Response geometry and joint-design regime summary

| Result | Count / interval | Interpretation |
| --- | --- | --- |
| Matched pollinator-community realizations | 96 | frozen synthetic design |
| Mixed-sign realizations | 41/96 | design descriptor, not prevalence |
| All-positive realizations | 42/96 | one-direction regime also occurs |
| All-negative realizations | 13/96 | one-direction regime also occurs |
| Mean sign switch 1 | 0.30-0.35 | synthetic coordinate only |
| Mean sign switch 2 | 0.65-0.70 | synthetic coordinate only |
| Joint Latin-hypercube points | 48 | ten parameters varied jointly |
| Mixed mean geometry | 16/48 | nontrivial but non-universal region |
| All-positive mean geometry | 22/48 | regime boundary retained |
| All-negative mean geometry | 10/48 | regime boundary retained |
| Equal-initial-richness mixed realizations | 53/96 | reduced initial richness not necessary for mixed geometry |

## Table S3. Local filtering and autonomous-assurance sensitivity

### Local availability / interaction filtering

| Filtering strength | Negative -> non-negative | Positive -> non-positive |
| ---: | ---: | ---: |
| 0.10 | 9.33% | 14.93% |
| 0.25 | 15.30% | 38.42% |
| 0.40 | 15.67% | 56.54% |
| 0.50 | 11.94% | 64.43% |
| 0.60 | 17.54% | 77.01% |
| 0.75 | 49.25% | 84.40% |

Any sign change somewhere in the declared envelope occurred in 737 lineage contrasts. Median first sign-change strength was 0.60 among changing baseline-negative contrasts and 0.40 among changing baseline-positive contrasts. These are synthetic strength coordinates.

### Autonomous assurance

| Assurance multiplier | Sign rescues | Magnitude-improvement fraction among 580 eligible declines |
| ---: | ---: | ---: |
| 0.0 | 0 | 0.0% |
| 0.5 | 0 | 97.4% |
| 1.0 | 0 | 95.7% |
| 1.5 | 0 | 94.0% |
| 2.0 | 0 | 94.0% |
| 3.0 | 0 | 93.3% |
| 4.0 | 0 | 92.9% |

Upstream effective service was unchanged across assurance multipliers. In this implementation, assurance attenuates decline magnitude without sign rescue in the tested envelope.

## Table S4. Conditional-WHY and relational-robustness diagnostics

| Diagnostic | Result | Interpretation boundary |
| --- | ---: | --- |
| Additive ten-parameter model R2 | 0.611 | descriptive fit to 48 fixed design points |
| Leave-one-point-out RMSE | 0.329 | substantial predictive error; not a precise classifier |
| Partner-loss full-range coefficient | +0.634 | fixed-surface association with negative-grid fraction |
| Partner-arrival full-range coefficient | -0.626 | fixed-surface association with negative-grid fraction |
| Historical starting-position SS fraction | 2.18% | one frozen 21 x 96 matrix |
| Historical community-realization SS fraction | 80.17% | one frozen 21 x 96 matrix |
| Historical state x community non-additivity | 17.64% | exact non-additive remainder in the fixed deterministic matrix |
| Six-seed community fraction range | 69.34-80.17% | exact historical magnitude is ensemble dependent |
| Six-seed starting-position range | 2.17-3.14% | starting position never largest |
| Six-seed non-additivity range | 17.64-27.91% | relational contingency persists |
| Horizon 30/60/120/240 mixed counts | 65/48/41/43 of 96 | mixed geometry persists across horizons |
| Trait adjustment = 0 mixed count | 64/96 | trait adjustment not required for state-dependent mixed geometry |
| Equal initial richness mixed count | 53/96 | richness reduction not necessary for mixed geometry |

The historical 17.64% remainder must not be described as containing within-cell simulation noise. Pollinator trajectories are generated once per realization and shared across starting positions; conditional on the trajectory, each response-matrix cell is deterministic.

## Table S5. Historical Izu signed-position projection and structural attacks

| Analysis | Rows / plants | Slope | 95% CI | Additional diagnostic | Interpretation |
| --- | ---: | ---: | ---: | --- | --- |
| Frozen source-position x island-centre projection -> raw matching | 83 / 30 | +0.5669 | +0.2977 to +0.8361 | 0/10,000 source-position permutations >= observed | correct source-state identity carries information for raw matching |
| Exact island-centre reassignment | 120 assignments | observed +0.5669 | range +0.4133 to +0.6078 | 13/120 assignments >= observed | exact centre-shift magnitudes/order are not uniquely identified |
| Source-position-only raw comparator | 83 / 30 | -0.2033 | -- | R2 0.409; AIC 362.1 versus full geometry R2 0.365; AIC 368.1 | raw signal is strongly source-state/background-composition structured |
| Same frozen projection -> null-corrected matching | 83 / 30 | +0.0333 | -0.2680 to +0.3346 | permutation p = 0.3919 | historical signed-position predictor does not explain beyond-background sorting |
| Prespecified Oshima-source sensitivity | 62 / 22 | +0.2808 | -0.3980 to +0.9596 | one leave-one-island slope slightly negative | source baseline is not interchangeable |

This is a same-system structural triangulation, not external validation of the synthetic model.

## Table S6. Frozen external-prediction readiness

| Audit quantity | Result | Interpretation boundary |
| --- | ---: | --- |
| Formal research entries | 25 | research entries, not independent archipelagos |
| Exact geographic labels in frozen formal layer | 21 | frozen denominator |
| Direct response outcome | 21/25 | outcome-rich literature |
| Direct community functional shift | 13/25 | marginal availability only |
| Direct local filtering | 9/25 | marginal availability only |
| Direct richness / FD change | 8/25 | marginal availability only |
| Direct source functional state | 5/25 | sparse historical coordinate |
| Direct partner loss | 5/25 | sparse historical coordinate |
| Direct reproductive assurance | 5/25 | sparse downstream coordinate |
| Direct partner arrival/replacement | 2/25 | strongest measurement bottleneck |
| Full outcome-independent contracts | 0/25 | no external response classifier fitted |
| H0-H4 / held-out / permutation evaluation | `not_evaluable` | data-readiness stop, not failed fitted prediction |

## Table S7. Geography-first world-saturation audit

| Layer | Result | Role |
| --- | --- | --- |
| Descriptive source-verified breadth | 42 research entries / 37 exact labels | broad empirical response/process vocabulary; does not reopen formal denominator |
| Independent island master | 4,663 candidate polygons >=20 km2 | geography-first starting frame rather than literature-built target list |
| First 20 omitted systems | response 10/20; breeding/assurance 9/20; community/process 7/20; filtering 2/20 | additional contemporary information recovered |
| First 20 omitted systems: direct historical loss | 0/20 | historical transition coordinate still absent |
| First 20 omitted systems: direct arrival/replacement | 0/20 | historical transition coordinate still absent |
| First 20 omitted systems: full contracts | 0/20 | bottleneck persists |
| Later Gulf of California tranche | historical/ploidy alternative mechanism added | reset zero-novelty stopping count |
| Next two eligible tranches | zero new response/process/falsification states and zero full contracts | declared 2/2 large-island saturation reached |
| Mandatory <20 km2 supplement | 8 systems | small-island history-rich check |
| Small-island direct historical partner loss | 0/8 | still absent |
| Small-island direct arrival/reintroduction | 1/8 | Tiritiri Matangi |
| Small-island full contracts | 0/8 | full matched transition chain still absent |
| Final retained chronology role | Surtsey | dated empty-island founding / colonization chronology |
| Final retained reintroduction role | Tiritiri Matangi | documented pollinator reintroduction + functional pollination test |
| Final retained historical-alternative role | Gulf of California Pachycereus | ploidy/history alternative and failure of simple current-abundance explanation |

The geography-first audit stops breadth expansion because additional coverage ceased adding mechanism states under the declared procedure. It does not claim a world census or prevalence estimate.

## Table S8. Contemporary Izu functional chain and branching

### FDQ -> corrected trait matching

| Subset | Site x season rows | FDQ coefficient | Leave-one-island range |
| --- | ---: | ---: | ---: |
| All eight source sites | 40 | +1.8346 | -- |
| Mainland three sites | 15 | +1.5414 | -- |
| Izu five islands | 25 | +1.9426 | +1.4320 to +2.2257; all positive |
| Post-Oshima four islands | 20 | +2.0590 | +1.4561 to +2.3325; all positive |

### Corrected matching -> pollen receipt

| Subset | Plant x site x season cells | TM coefficient | Site x season clustered 95% interval | Key omission result |
| --- | ---: | ---: | ---: | --- |
| All eight sites | 124 | +0.0295 | -0.0175 to +0.0765 | interval includes zero |
| Mainland | 46 | +0.0468 | -0.0518 to +0.1455 | interval includes zero |
| Izu five islands | 78 | +0.0353 | -0.0314 to +0.1019 | leave-Hachijo and leave-season-3 can reverse sign; all 24 leave-one-site-season omissions positive |
| Post-Oshima four islands | 60 | +0.0342 | -0.0510 to +0.1194 | Hachijo x season 3 is the single site-season omission that reverses sign |

All nine estimable leave-one-plant models remain positive in both Izu subsets; one Oxalis omission is non-estimable because the fixed-effect design becomes singular. The downstream coefficient is therefore not driven by one estimable plant taxon, but it is sensitive to network state.

### Eight shared Oshima-to-post plant targets

| Response channel | Lower / shorter post | Higher / longer post | Equal |
| --- | ---: | ---: | ---: |
| Corrected trait matching | 8 | 0 | 0 |
| Floral tube morphology | 3 | 4 | 1 |
| Pollen receipt | 4 | 4 | 0 |

Only 2/8 targets show the complete matching-lower + tube-shorter + pollen-lower combination. This is descriptive response branching within shared island environments, not eight independent boundary experiments.

## Interpretation boundary

Tables S1-S4 preserve synthetic design and robustness. Table S5 preserves historical Izu structural attacks. Table S6 is the frozen formal identifiability stop. Table S7 is a separate geography-first saturation audit and cannot change the frozen 25-entry measurement fractions. Table S8 is contemporary observational Izu evidence: the FDQ-to-matching association is sign-stable across island omissions, while matching-to-pollen propagation is positive on average but cluster-uncertain and network-state sensitive. None of these tables identifies historical Bombus loss, causal floral evolution, natural response prevalence or a calibrated universal island predictor.
"""


def build() -> str:
    _validate_sources()
    return TABLES


def main() -> None:
    text = build()
    OUT.write_text(text, encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
