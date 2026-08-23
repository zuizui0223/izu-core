# ABM v14 — autonomous-assurance buffering ablation

## Question

Can the **existing** autonomous-assurance route create a buffering state when island effective pollinator service declines, without adding a new parameter or fitting any empirical island outcome?

The design was frozen before the full run in `data/design/abm_v14_assurance_buffering_ablation_freeze.json`.

## Matched design

The comparison keeps the v9/v10 opportunity, support, partner-effectiveness, dependency, trait-position and random streams identical.

- **assurance ON:** retain each frozen lineage's `assurance_ceiling` and `assurance_responsiveness`;
- **assurance OFF:** set both fields to zero;
- effective service must remain exactly identical between ON and OFF.

The full frozen run contains:

- 3 saturations;
- 4 replicates per saturation;
- 24 lineages;
- 4 local contexts;
- 288 mainland–island lineage contrasts.

No Hawaiʻi, Guaiacum, Nicotiana or Issue #91 effect size or observed buffering frequency was used to choose a threshold. The only boundary is zero direction.

## Predeclared state

A lineage is called **synthetically buffered** only when:

1. island effective service is lower than mainland effective service; and
2. island-minus-mainland reproduction is non-negative.

An **assurance sign rescue** requires that the same matched lineage is buffered with assurance ON but has a negative reproductive contrast with assurance OFF.

## Frozen result

Across 288 lineage contrasts:

- effective service declined in **202**;
- assurance ON produced synthetic buffering in **1** of those 202 contrasts;
- assurance OFF produced synthetic buffering in **0**;
- assurance therefore caused **1 sign-level rescue**;
- assurance improved the reproductive contrast magnitude in **197/202** service-decline contrasts;
- effective service was exactly identical between ON and OFF in every comparison.

The one sign rescue occurred at saturation `1.0`. No sign rescue occurred at `2.0` or `3.0`.

The mean island-minus-mainland reproductive contrast changed from about `-0.08505` with assurance OFF to `-0.08357` with assurance ON. Thus the existing route broadly reduces the magnitude of reproductive loss, while sign-level buffering is rare in this initial frozen stochastic block.

Decision:

`existing_assurance_route_is_synthetically_sufficient_for_sign_level_buffering_in_frozen_model`

## Interpretation

This result establishes **synthetic sufficiency in principle**, not empirical mechanism identification.

The strongest reading is:

> Autonomous assurance can rescue a declining-service lineage across the zero reproductive boundary in the declared model, but in the initial frozen run it behaves mainly as a magnitude modifier rather than a broad generator of buffering states.

That interpretation is consistent with the earlier v10/v11 finding that downstream factors can alter branch identity or magnitude without being necessary to generate the underlying two-sided lineage branching.

## What did not change

The empirical admission interface remains unchanged:

- Hawaiʻi autonomous assurance: `candidate_only_no_abm_admission`;
- current mapping-ready buffer candidates: `0`;
- empirically admitted buffer mechanisms: `0`.

The `1/202` synthetic buffering frequency is **not** an estimate of how often autonomous assurance buffers island plants in nature. It is not calibrated to the observed island-system frequencies.

## Next test

Because the sign-level result is one event, the next scientific step is a **predeclared independent stochastic robustness block** using the same model and parameter values but a non-overlapping seed stream and more replicates.

The robustness test must be frozen before running. It should ask only whether sign rescue reappears and whether the magnitude-rescue pattern persists. It must not alter assurance ceilings, responsiveness, support, partner quality or thresholds.

## Claim boundary

v14 is a synthetic mechanism-capability result. It does not show that autonomous assurance caused the Hawaiʻi buffering boundary, does not make assurance a universal island buffer, and does not authorize fitting the known Hawaiʻi outcome. Empirical promotion still requires the separately frozen matched-evidence and held-out-test admission contract.
