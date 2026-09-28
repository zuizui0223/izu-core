# Constraint-mediated pollination ABM v2: lineage-level response branching — 2026-08-19

## Why v2 exists

Held-out Izu validation left the v1 mechanism partly intact but exposed one concrete failure: v1 could generate multiple interaction architectures, yet its reported reproductive outcome was an island-wide mean decline. The held-out Hiraiwa–Ushimaru cross-channel data instead show a shared matching decline with divergent downstream responses: corrected trait matching is lower in 8/8 shared targets, while pollen receipt is lower in 4 and higher in 4, and tube morphology is shorter in 3, longer in 4 and unchanged in 1.

The goal of v2 is therefore narrow: test whether lineage-level response-sign branching can arise from common process rules without using Izu outcomes to tune parameters.

## Mechanism added

Relative to v1, each lineage receives independently drawn values for:

- pollinator dependency;
- reproductive-assurance ceiling;
- assurance responsiveness;
- floral-trait adjustment rate.

These quantities are biologically motivated by the repository's independent comparative evidence that plants differ in reproductive dependency, assurance and response mode. They are not conditioned on geography, on final architecture labels, or on the Izu 4/4 pollen split.

The same lineage templates are paired between a mainland-like and oceanic-island scenario. Geography changes only the shared partner-opportunity process inherited from v1.

## Predeclared qualitative test

A necessary condition for the mechanism to explain downstream branching is that the paired oceanic-minus-mainland reproductive response can take both positive and negative signs under common process rules.

The model is not required or allowed to reproduce the empirical Izu sign frequency. The eight Izu species share island environments and are not eight independent island experiments.

## Result

120 paired runs × 16 lineages produced 1,920 paired lineage contrasts.

- positive reproductive response: **47**;
- negative reproductive response: **1,873**;
- mixed-sign runs: **10/120**;
- mean mainland-like reproduction: **0.5872**;
- mean oceanic-island reproduction: **0.2799**;
- mean oceanic-minus-mainland delta: **-0.3073**.

Thus lineage-level dependency and assurance heterogeneity are sufficient to generate **both response signs** without Izu-specific tuning. However, the result remains strongly decline-biased.

## Interpretation

This is a useful but limited advance.

1. A universal downward reproductive response is no longer structurally forced by the model.
2. Shared geographic constraint can generate lineage-specific positive and negative outcomes through different dependency/assurance states.
3. The current mechanism still makes positive outcomes rare, so v2 does **not** explain the breadth of the held-out downstream heterogeneity.

The correct decision is therefore:

> `lineage_heterogeneity_can_generate_sign_branching_but_v2_remains_strongly_decline_biased`

## What not to do next

Do not tune dependency ranges until the synthetic sign frequencies resemble 4/4 Izu pollen responses. That would leak the held-out outcome into calibration and destroy the validation.

Do not add architecture-specific rescue terms merely because Hawaii, Seychelles or Canary occupy different descriptive classes.

## Next discriminating mechanism

The next candidate should be independently motivated and alter the quality, not just the quantity, of pollination service. The strongest candidate from the empirical programme is **effective-service heterogeneity among partners**: replacement/generalist partners can be beneficial, neutral or poor depending on matching and per-visit effectiveness. This can be added as a partner-level effectiveness trait drawn independently of geography, then tested to see whether it broadens lineage-level response branching without Izu tuning.

Only after that mechanism is frozen should Izu and the secondary held-out island systems be re-evaluated.

## Claim boundary

ABM v2 is synthetic mechanistic evidence. It does not upgrade an empirical pathway, estimate the prevalence of response classes, or establish that dependency/assurance differences caused the observed Izu species responses.
