# Appendix S19. Exact realized-richness matching hard control

The earlier equal-richness sensitivity set initial pollinator richness to 9 mainland-like versus 9 island-like types but retained the baseline differences in partner loss and arrival. It therefore tested reduced **initial** richness, not realized richness after community dynamics. A stronger control was frozen on 2026-09-07 before execution to isolate that distinction.

## S19.1 Frozen matching rule

The original BASE community trajectories were generated unchanged for the same 96 matched community realizations, 120 steps and community seed 20260826. At every simulated step, the matching target was

`target richness = min(realized mainland richness, realized island richness)`.

If one snapshot contained more pollinator types than the other, only the larger snapshot was uniformly subsampled without replacement to the target. When richness was already equal, both snapshots were retained unchanged. If either original snapshot was empty, both matched snapshots were set to empty. Subsampling did not use plant state, pollinator trait, breadth, matching score, service or response. Six matching RNG seeds (`20260907`–`20260912`) were prespecified; they change only which members of the larger snapshot are retained.

The matched trajectories, not the original trajectories, were supplied to trait adjustment and final service. Thus realized richness was identical throughout the entire trajectory experienced by each plant starting position.

## S19.2 Prespecified decision gate

Before result inspection, a full clear required all five conditions:

1. exact post-matching richness equality for every step, realization and matching seed;
2. mixed mean response geometry for the primary matching seed;
3. mixed mean response geometry for all six prespecified matching seeds;
4. at least one mixed-sign individual community realization for every matching seed;
5. strictly positive state × community non-additivity for every matching seed.

Failure of the primary mixed mean geometry required reframing the richness-independent mechanism claim before author metadata rather than selecting another matching seed.

## S19.3 Hard-control validity

Each matching seed contained 96 trajectory pairs × 120 steps = **11,520 snapshot pairs**. Post-matching mainland-like and island-like richness was identical for every snapshot pair (`0` unequal pairs). The matched target richness averaged `2.3885` and ranged `0–11`; `10.15%` of matched snapshot pairs had target richness zero.

Before matching, the same frozen trajectories had mean mainland-like realized richness `14.4140`, mean island-like realized richness `2.3892`, and mean absolute richness gap `12.0261`. A non-zero richness gap occurred in `99.965%` of snapshot pairs. The hard control therefore removed a large realized-richness asymmetry rather than a negligible perturbation.

## S19.4 Mean regime changed, but individual branching persisted

For the primary matching seed (`20260907`), the mean response geometry was **all-positive**, so the prespecified full-clear gate failed. Individual community realizations nevertheless remained heterogeneous: `58/96` were mixed-sign, `21/96` all-positive, `4/96` all-negative and `13/96` other/zero-only configurations.

The same qualitative result held for every prespecified matching seed. All six produced all-positive mean geometry, while mixed-sign individual realizations ranged from **51/96 to 65/96**.

The response decomposition also remained strongly relational after exact richness matching. Across the six matching seeds:

- starting-position additive share: **0.94–2.21%**;
- community-realization additive share: **50.04–55.92%**;
- state × community non-additivity: **42.72–48.51%**;
- additive-sign mismatch: **31.80–36.76%** of response-matrix cells.

For the primary seed, the three sum-of-squares fractions were `0.94%`, `51.59%` and `47.47%`, respectively.

## S19.5 Revised interpretation

The hard control rejects the stronger statement that realized richness differences are unnecessary for the **ensemble mean** mixed response geometry. In the declared model, forcing realized richness to be equal at every step shifts the mean regime to all-positive across all six prespecified matching seeds. Realized richness therefore materially helps position the coarse mean regime.

The same result also rejects the opposite simplification that richness alone explains the branching. Mixed-sign individual communities remain common after exact richness matching, state × community non-additivity remains 42.7–48.5%, and the additive starting-position term remains small. **Mean regime is richness-sensitive, while response branching remains relational.** The supported hierarchy is therefore:

`realized richness / turnover -> coarse mean-regime placement`

`starting state × realized community composition -> branch contingency within that regime`.

This is a synthetic structural sensitivity, not an empirical richness manipulation. Matching to the minimum richness deliberately removes unilateral richness advantages and can zero both matched communities whenever either original community is empty. The result does not imply that richness is universally causal in natural island systems, nor that composition, partner identity, breadth, turnover or replacement differences have been removed.

Source locks:

- design: `data/design/chapter2_realized_richness_matching_freeze_20260907.json`;
- implementation: `scripts/audit_chapter2_realized_richness_matching.py`;
- frozen decision: `data/results/chapter2_realized_richness_matching_decision_20260907.json`;
- execution: PR #338, workflow run `34087352249`, artifact `10005728099`, digest `sha256:89962a20f23cfe6a7a11fa9191878ffa7a2b1524e9282b1adc1361c7d1a44854`.
