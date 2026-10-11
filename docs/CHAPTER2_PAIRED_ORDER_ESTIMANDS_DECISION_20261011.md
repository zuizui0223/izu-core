# Chapter 2 — Does observed evolutionary precedence mean island-induced causation?

**2026-10-11 — frozen retrospective paired-history reanalysis, not a new prospective experiment.**

## Decision

The empirical proposition "selfing capacity changes before floral attraction investment" cannot be substituted for "selfing capacity is the first response specifically induced by isolation." We compared two distinct order estimands from the **same archived 64 visitor histories**, with identical threshold, 20-update sustained crossing and five-update near-simultaneous tolerance:

1. **Founder-relative change:** In the more-isolated arm, when do assurance capacity A and investment I first change sufficiently compared with their OWN starting values?
2. **Incremental isolation response:** When do the FAR-minus-NEAR contrasts in A and I first cross the same magnitudes relative to the common external control?

Both readouts were already frozen in `data/results/model3_persistent_isolation_summary_20261005.json`. This audit adds a **same-history cross-tab**, not new biological outcomes, redefinition of threshold, historical genome recording or causal time manipulation.

## Delayed selfing / direct assurance cost 0.5 / mutation 0.01

At the source primary 0.05 sustained-change threshold:

| Criterion | Assurance first | Investment first | Within 5 updates | Investment only |
|---|---:|---:|---:|---:|
| Far population relative to founder | **51/64** | 0/64 | 13/64 | 0 |
| Additional FAR-minus-NEAR divergence | **10/64** | **32/64** | 20/64 | 2/64 |

Within the **same histories**, 22/64 are **strictly** classified as A-first under founder-relative change and I-first under additional FAR-minus-NEAR divergence. There are **52/64** history-level label changes in total, but the other 30 comprise ties and/or censored events. They MUST NOT be called reversed evolutionary sequence.

The lag between crossing times `I_time-A_time` has median **+24 updates** when based on founding traits and **−6.5 updates** for the 62 histories in which both far-minus-near divergence thresholds are reached. Negative lag means investment divergence crossed first. These are median **within-history** lags, not the difference of two independently pooled median crossing times.

The two observations are compatible. Both far and near may change assurance early; the incremental *effect of the stronger isolation treatment* can nevertheless appear in investment first. The important distinction is between **within-lineage chronology** and **the chronological emergence of a between-treatment difference**.

## Prior selfing / zero direct assurance cost / mutation 0.01

At the same threshold:

- Far from founder: assurance first **38/64**, near-simultaneous **26/64**.
- Incremental FAR-minus-NEAR: investment only **31/64**, neither **16/64**, assurance only **4/64**, investment first **3/64**, assurance first **7/64**, near-simultaneous **3/64**.
- Any category changed **56/64**; STRICT A-first to I-first **2/64**. Most differences reflect censored/unreached divergence events, not evidence of an order reversal.
- Founder-relative median I-minus-A lag **+6** versus +24 in the delayed/costly setting.

**Vital limitation:** The two historical reproductive settings change BOTH timing (prior vs delayed) and direct assurance cost (0 vs 0.5). Thus the difference between 38/64 and 51/64 cannot be assigned to selfing timing alone. It motivates independently factorial mating-timing and assurance-cost interventions, with all initial genotypes and visitor histories held fixed.

## All conditions, not cherry-picked

The machine-readable audit retains **all 12 conditions** (two historical mating settings × mutation0/.01 × three original thresholds .025/.05/.1), all 64 actual paired history identifiers and all six original classification categories including one-event and no-event censoring. A test fails if any history is missing, if archived classification counts change, or if an arbitrary label change is called a strict opposite sequence.

The 64 visitor histories are the independent environmental clusters. Three threshold sensitivities and two definitions from a single cohort are NOT six independent biological populations.

## What this proves, and does not prove

This establishes a **referent dependence of measured precedence in the archived evolutionary trajectories**: founder-relative onset and treatment-attributable divergence can have different chronology even when all underlying observations are the same. This directly limits the interpretation of ancestral-state character sequences in island mating-system evolution, but it is a Model 3 illustration rather than an independently replicated phylogenetic study.

It does **not** prove:
- that an early increase in assurance was genetically necessary for later investment reduction (independent fixed-assurance interventions in #411 address necessity separately);
- that the natural first mutation or selection-gradient sign crossing occurred at the same date as a 0.05 phenotypic threshold crossing;
- that experimentally swapping the actual order of inherited allele substitutions has zero fitness effect. The independent #418 result concerns **assigned transient expression schedules**, with a history-paired far-minus-near 80-update occupancy DID of −0.01359 and predeclared practical equivalence within ±0.05; not a blanket absence of small order effects;
- that the earliest driver was pollinator disappearance alone. Existing histories change visitor immigration/composition jointly, and the expected selection return depends on maternal, paternal, selfing and allocation pathways;
- that a 64-history synthetic output validates timing in natural island populations.

## Time-window and mechanism test that is still needed

**Stage A, retrospective diagnostic only:** inspect original frozen ABM annual genomic/population/visitor records and recompute original full-paternal-inclusive resident/focal `W=.5F+.5P+S` local gradients for A and I at each update, using the actual plant state at that update, including absent visitor times and extinction. Annual genomic states are NOT reconstructible from the archived 10-column trait means/variance trajectory alone; the old `*.npz` contains complete genomes only at t0,200,400,1000. Therefore claiming the *actual gradient-sign switch time* from these aggregate archives would be invalid without authentic original-RNG replay or a separate properly designed recorder.

**Stage B, fresh experimental hypothesis:** fix independent visitor history seeds and matched diploid founders **before outcome**, then vary gradual versus abrupt functional-pollinator loss under comparable cumulative delivery and initial pollen limitation. Test if abrupt loss advances the investment gradient transition and changes founder-relative A→I sequence. This is a new, source-identified experiment, NOT already confirmed by the existing cohort.

**Stage C, cost/timing disambiguation:** factorially vary `assurance_timing` and `assurance_cost` while fixing source genomes and exposure trajectories. See whether near-simultaneous crossings in the prior-selfing historical arm reflect pollen discount from ovule preemption, lower direct assurance costs, or differences in genotype variance supply.

A primary prospective cross-system claim would require real plant and visitor functional traits, independently inferred trait evolution, uncertainty in ancestral-state histories, and an actual pollen limitation proxy. Do not title the current manuscript as a universal evolutionary sequence law before these gates are passed.

## Execution and evidence provenance

```bash
python -m scripts.audit_chapter2_paired_precedence_estimands_20261011 --out /tmp/chapter2_paired_orders.json
pytest -q tests/test_chapter2_paired_precedence_estimands_20261011.py
```

- Original frozen source: `data/results/model3_persistent_isolation_summary_20261005.json`.
- Original timing protocol: `data/design/model3_temporal_order_diagnostic_20261005.json` with 20 sustained updates and threshold sensitivity .025/.05/.1.
- Original method: `scripts/summarize_model3_persistent_order.py` and `scripts/model3_temporal_order.py`.
- Original earlier confirmatory: [#411](https://github.com/zuizui0223/izu-core/pull/411), [#418](https://github.com/zuizui0223/izu-core/pull/418); #418's practical equivalence applies to assigned expression timing, not observed inherited order.
- Model3 source results, current manuscript, original selection biology and original confirmed inference ranks remain unchanged.

Scientific title decision: **KEEP the confirmed attenuation result as the published lead until independent threshold-timing mechanisms are tested.** The interesting, testable revised framing is that *chronological precedence is a measurement of an evolutionary path, not by itself a unique statement about its environmental cause or its long-run fitness consequence*.
