# Analysis method state — 2026-08-18

## Bottom line

The current `izu-core` scientific mainline is **not an agent-based model (ABM)**.

The repository currently works as a source-locked comparative evidence synthesis and pathway-testing framework. Its main inferential objects are island systems, pollination-network architecture, functional/trait-matching measures, reproductive-assurance measures, and reproductive outcomes recovered from primary studies or repository-native field data.

## What the current analysis actually does

1. **Source lock / provenance gate**
   - only admissible source-native measurements are entered;
   - missing cells are never coded as zero;
   - incompatible estimands are not pooled into a synthetic common effect.

2. **System × response-axis matrix**
   Systems are compared across axes including:
   - floral morphology;
   - mating / reproductive assurance;
   - visual signal;
   - pollinator effectiveness;
   - interaction-network architecture / rewiring;
   - reproductive outcome.

3. **Categorical architecture synthesis**
   Observed systems are classified conservatively into recurring architecture classes such as concentrated dependency, complementary/redundant generalism, species-specific mosaic, and novel-partner replacement.

4. **Pathway evidence testing**
   The current causal ordering under test is approximately:

   `geography / isolation -> feasible pollinator opportunity space -> interaction architecture / trait matching -> realized pollination or reproductive performance`

   Evidence is registered as full, partial, or architecture-only depending on which links are source-native in the same study/system.

5. **Falsification-first comparative analysis**
   Mainland and continental-island controls are used to reject over-broad claims. Current examples:
   - pollination dependence itself is not island-specific;
   - architectural contingency itself is not island-specific;
   - the surviving island-specific candidate concerns oceanic insularity changing the feasible interaction opportunity space.

## What it is not

- not an ABM;
- not an individual-based simulation;
- not a mechanistic evolutionary simulation;
- not a standard common-effect meta-analysis;
- not currently a Bayesian hierarchical model over all island systems;
- not a SEM fitted to one harmonized global data table.

Some source studies use GLMMs, network metrics, trait-matching indices, breeding experiments, or other statistical models, but `izu-core` currently integrates their admissible outputs rather than pretending they are one homogeneous dataset.

## Where ABM would fit

ABM would be a **next-stage mechanistic hypothesis test**, not a replacement for the current empirical comparative layer.

A useful future ABM could represent:
- plant individuals or populations;
- pollinator functional types / partner pools;
- colonization and extinction of pollinators;
- trait matching and visitation effectiveness;
- reproductive assurance / selfing as an alternative route;
- island isolation and opportunity-space constraints.

The empirical repository would provide the constraints and falsification targets. The ABM would then test whether the observed divergent architectures can emerge from the proposed mechanism without hard-coding the outcomes.

## Current recommendation

Keep the empirical comparative pipeline as the evidential backbone. Add ABM only after the pathway claim is sufficiently constrained, and evaluate the ABM against held-out island systems rather than using it as proof of the empirical pattern.
