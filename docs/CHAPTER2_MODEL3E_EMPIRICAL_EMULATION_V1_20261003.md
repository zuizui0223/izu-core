# Model 3E empirical emulation v1 — result and failure diagnosis

**Date:** 2026-10-03  
**Status:** first prospective empirical emulation completed; held-out validation failed  
**Role:** negative/diagnostic result; does not replace frozen Model 3 or the active Oikos submission

## Question

Can a numerical world built from the Model 3 reproductive logic reproduce the
Chapter 1 island-syndrome pattern, rather than merely show that heterogeneous
responses are possible?

The empirical targets were frozen from the Chapter 1 v14 canonical result before
Model 3E was executed.

### Fit targets

- H1 all-analysis domain slopes in four geographic strata:
  reproductive assurance, floral accessibility/generalization and display dulling;
- H3 global isolation → pollen-limitation slope.

### Held-out targets

- H2 selfing-adjusted accessibility and display responses;
- H4 association of assurance/accessibility with lower current pollen limitation.

H2/H4 were not calculated until the H1/H3 screen and the five accepted parameter
sets had been frozen.

## Model 3E v1

The first emulator retained one focal evolving plant population per pseudo-island.

The three inherited trait axes were:

- floral generalization/accessibility breadth (g);
- pollinator-facing display investment (z);
- reproductive assurance (a).

Pollen limitation was calculated directly as

[
logleft(
rac{	ext{pollen-supplemented viable maternal reproduction}}
{	ext{natural viable maternal reproduction}}
ight).
]

Four ecological contexts were generated from fixed seeds and one shared
hyperprior, not tuned to the Chapter 1 regional results. Forty pseudo-islands
were generated per parameter set (4 strata × 5 isolation values × 2 visitor
histories).

## H1/H3 screen

Forty-eight Latin-hypercube parameter sets were prospectively screened using
H1/H3 only.

- 13/48 met the preregistered eligibility and score rule.
- The five frozen accepted sets were:
  `p010, p046, p036, p032, p029`.

The screen reproduced important parts of the Chapter 1 functional structure:

- assurance isolation slope > 0 in all four strata;
- accessibility isolation slope > 0 in all four strata;
- positive isolation-associated pollen limitation.

For example, the H3 model slope was:

- p010: 0.1050;
- p036: 0.0904;

against the empirical target 0.0794 ± 0.0377.

However, the display domain already failed at the training stage. All five
accepted sets had optimal display scale 0 and display NRMSE = 1. Most simulated
display-dulling slopes were negative, whereas the Chapter 1 domain is near zero
to positive across strata.

Therefore the preregistered numerical acceptance rule passed, but **full H1
island-syndrome reproduction did not**.

## Held-out H2/H4 test

The five frozen H1/H3-selected parameter sets were then tested without retuning.

Result:

- successful parameter sets: **0/5**;
- best H1/H3 fit p010: **failed**;
- overall held-out success: **false**.

### H2

p010 reproduced positive selfing-adjusted accessibility in:

- northern mid-latitude;
- northern high-latitude;
- tropical;

but not southern extratropical.

The same three-of-four pattern occurred in p046 and p032.

### H4

The best H1/H3 fit p010 produced:

- accessibility → current pollen limitation: **−0.638**;
- assurance → current pollen limitation: **+0.299**.

The empirical H4 targets are approximately:

- accessibility: **−0.296**;
- assurance: **−0.297**.

Only p036 produced both H4 coefficients negative, but p036 failed the H2
accessibility rule.

Thus no parameter set satisfied both the selfing-independent accessibility
pattern and the functional H4 bridge.

## Why v1 failed

The failure is mechanistically informative.

### 1. The observational unit is wrong for Chapter 1

Chapter 1 measures **floral composition across many species within island floras**.

Model 3E v1 instead compares **one evolving focal population per pseudo-island**.

This creates a strong environment–trait covariance: severe pollination environments
select higher assurance, so populations with high evolved assurance can still be
the populations experiencing high current pollen limitation. The direct buffering
effect of assurance can therefore be masked or reversed in a cross-island
regression.

That is exactly the direction of the held-out H4 failure.

### 2. Display benefit is too universal

In v1, display investment multiplies attraction to every visitor functional type.
Isolation can therefore favour compensatory attraction even when visitors are
scarce. The model has no visitor guild whose response to display is preferentially
lost or retained under isolation.

This makes the Chapter 1 display-dulling component difficult to generate.

### 3. Generalization is closer, but not sufficient

A heritable access-breadth trait can reproduce positive isolation-associated
generalization in several contexts and often survives assurance adjustment, but
the southern-extratropical relation is not stable across the frozen accepted
sets.

## Next model: flora-level empirical emulator

The next prospective model should match Chapter 1's observational unit rather
than retune v1.

The required extension is:

```text
mainland/source species pool
  × species-specific assurance
  × species-specific access breadth
  × species-specific display strategy
        ↓
isolation-dependent visitor environment
        ↓
species-specific pollen limitation / viable reproduction
        ↓
colonization + persistence + optional within-lineage evolution
        ↓
island flora composition
        ↓
the same H1/H2/H3/H4 statistics used in Chapter 1
```

Two biological additions are required:

1. **multi-species community assembly**, so trait–pollen-limitation relations can
   be compared among species within overlapping environments rather than only
   among evolved island endpoints;
2. **visitor-specific display sensitivity**, so changes in visitor functional
   composition can alter the return to display rather than all visitors responding
   identically to investment.

This is a new prospective model. The v1 search ranges and held-out failure remain
frozen and are not retuned into a positive result.

## Current conclusion

> **Model 3E v1 reproduces part of the recurrent functional core and the
> isolation-associated pollen-limitation gradient, but it does not reproduce the
> full Chapter 1 island syndrome. The failure points to a missing flora-assembly
> level and overly generic display biology.**
