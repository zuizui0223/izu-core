# Izu regime-transition comparative design

## Scientific question

The central test is not whether every island trait forms a monotonic mainland-to-island cline. It is whether independent plant lineages show repeatable **response shapes** at the same ecological boundaries:

```text
large Bombus -> B. ardens -> no effective Bombus
```

The focal *Campanula microdonta* calibration currently contributes three adopted channels only:

| channel | retained focal shape |
|---|---|
| floral size | continuous erosion |
| multilocus outcrossing | continuous erosion |
| autonomous reproductive capacity | second-transition step |

Nectar-guide and visible-signal results are not adopted. They remain future channels with no current direction or breakpoint.

## Why the breakpoint question is useful

Most island comparisons are naturally reported as mainland-versus-island differences, correlations with isolation, or broad syndrome shifts. Those approaches can miss a response that is nearly flat until an interaction partner becomes ecologically ineffective and then changes abruptly.

The prospective contribution of this programme is therefore to compare, for each independent lineage and response channel:

1. `none` — no ordered regime response;
2. `cline` — continuous change along an island/environment axis;
3. `first_step` — change at large Bombus to *B. ardens*;
4. `second_step` — change at *B. ardens* to no effective Bombus;
5. `two_step` — two distinct regime changes; and
6. `environment_history` — climate, area, isolation, colonisation history, or taxonomy explains the pattern without a pollinator-regime step.

A shared breakpoint across independently eligible specialist-like lineages would be more informative than several unrelated mainland-island contrasts. It would still be association, not proof of historical causation, until the environment/history alternative and interaction effectiveness are measured.

## Response domains

### 1. Continuous or proportional traits

Examples:

- flower length or display area;
- multilocus outcrossing rate;
- bagged fruit/capsule or seed set;
- herkogamy or dichogamy;
- nectar or reward quantity.

These retain their native uncertainty and sampling unit. Means without n and uncertainty cannot enter a quantitative synthesis.

### 2. Binary or ordinal states

A difficult continuous trait can be replaced by a defensible source-native state when the state is biologically meaningful and consistently defined. Candidate states include:

- self-incompatible versus self-compatible;
- autonomous reproduction absent versus present;
- restrictive versus broadly accessible floral architecture;
- specialist-like versus generalist effective-pollinator guild;
- one effective guild versus multiple effective guilds;
- trait/morph absent, polymorphic, or fixed.

Binary and ordinal observations are not degraded continuous measurements. They require Bernoulli, ordinal, or multistate transition models and must not be pooled with continuous effect sizes.

### 3. Island presence/absence

Species occupancy can be useful, but it answers a different question.

A detection-aware occupancy analysis can test whether a dependency class is disproportionately filtered at a regime boundary. For example:

```text
Pr(present on island)
  ~ pollinator regime
  * mainland dependency class
  + climate + area + isolation + history
  + lineage/phylogeny effects
  + observation effort
```

This can reveal range truncation or colonisation filtering: specialist-like plants may fail to cross the second boundary more often than open generalists.

It cannot demonstrate that a floral trait evolved after colonisation. Raw GBIF/iNaturalist occurrence is therefore candidate/occupancy evidence only, never a floral phenotype or pollinator-effectiveness measure.

### 4. Interaction states

Visitor identity alone is insufficient. An interaction state becomes admissible only when the source establishes a relevant function, such as legitimate contact, pollen deposition, pollen export, or reproductive contribution.

Partner breadth may then be represented as:

- effective guild richness;
- effective-link presence/absence;
- specialist/generalist class;
- turnover from one effective guild to another.

Sampling effort must be modelled because an unobserved interaction is not automatically absent.

## Generalists as negative controls

The falsification prediction is not that every generalist trait is perfectly flat. Generalist plants may respond to climate, island size, herbivory, drift, or different pollinator assemblages.

The narrower prediction is:

> Open-generalist lineages should not repeatedly share the same specialist-specific breakpoint at the Bombus-service boundary.

The primary test is therefore a dependency-class by boundary interaction, or a difference-in-differences contrast, rather than separate claims that specialists decline and generalists equal zero.

A strong result would have all three features:

1. specialist-like lineages disproportionately select the same step model;
2. open generalists select `none`, unrelated clines, or heterogeneous breakpoints; and
3. the specialist-control difference survives climate, area, isolation, history, taxonomy, and observation-process sensitivity.

## Mating-system and specialisation transitions

### Self-incompatibility to self-compatibility

SI to SC is a valid binary or multistate response and is biologically plausible under mate or pollinator limitation. It should be described as **loss of self-incompatibility** or **gain of self-compatibility**, not simply as more selfing.

SC, autonomous selfing, and realised selfing are different channels:

- SC: self pollen can fertilise;
- autonomous capacity: reproduction occurs without a pollinator treatment;
- realised selfing: offspring are actually selfed in nature.

They may change at different points along the island sequence.

### Specialist to generalist

This is better described as **de-specialisation**, **functional broadening**, or **interaction rewiring** than “reverse evolution.” Specialisation is multidimensional: floral accessibility, reward schedule, visitor breadth, and effective pollen transfer can move independently.

Possible island responses include:

- retention of the same specialised interaction;
- replacement by a different specialised guild;
- broadening to several smaller or more variable pollinators;
- increased autonomous reproduction without broader pollination;
- ecological loss of an interaction before a morphological response evolves.

The model must therefore permit alternative-guild replacement and generalisation, not force every lineage onto a selfing-syndrome axis.

## Independent comparison unit

One lineage x one prespecified response family is one evolutionary comparison unit. Multiple islands, populations, images, or correlated traits within that unit are observations, not independent replications.

Admission requires:

1. accepted taxonomy and a defensible within-lineage comparison;
2. named localities mapped to regimes;
3. a source-native response with its observation unit;
4. a trait/state definition fixed before scoring;
5. no unresolved variety-by-geography or taxon-by-geography confounding; and
6. separation of calibration, positive holdout, negative control, and contextual evidence.

## Statistical workflow

1. **Lock dependency class and response definition.** Do not classify a species after seeing its island response.
2. **Fit the native observation model.** Gaussian/count/proportion, Bernoulli, ordinal, multistate, or occupancy.
3. **Compare response shapes.** `none`, `cline`, `first_step`, `second_step`, `two_step`, and `environment_history`.
4. **Preserve uncertainty.** Small-island cells and source uncertainty must propagate to model comparison.
5. **Use lineage-level validation.** Leave one lineage out; never leave one flower or photo out while treating correlated records as independent.
6. **Test the moderator.** Compare specialist-like and open-generalist lineages with an interaction term.
7. **Report model ambiguity.** A lineage may remain compatible with several shapes.
8. **Separate description from causation.** Shared breakpoints support a regime-linked hypothesis; causal identification needs interaction effectiveness and environmental/history controls.

## Current work queue

1. Recover the population tables and locality mapping for *Weigela coraeensis* and *Ligustrum ovalifolium*.
2. Build the regime-transition registry with response domain, observation model, dependency class, regime coverage, and evidence status.
3. Screen independent lineages for source-native SI/SC, autonomous reproduction, flower-size, accessibility, effective-guild, and occupancy channels.
4. Develop the explicit environment/history competitor.
5. Run power and identifiability simulations using the actual mix of continuous, binary, ordinal, and occupancy records.
6. Keep all nectar-guide records outside current evidence until a final dataset and analysis are declared.

## Empirical precedents informing the design

The design builds on, but differs from, several established lines of empirical work:

- population-level losses of self-incompatibility and associated floral change, such as *Leavenworthia alabamica*;
- repeated and asymmetric SI-to-SC transitions identified by comparative and molecular studies;
- nested and asymmetric plant-pollinator networks, where specialists often interact with generalist partners;
- island pollination networks containing endemic super-generalists and interaction rewiring; and
- robustness studies showing that interaction loss can precede species loss.

The proposed Izu contribution is to join these ideas in a predeclared, within-archipelago test of **where** continuous erosion, discrete state change, ecological filtering, or no response occurs relative to two pollinator-regime boundaries.
