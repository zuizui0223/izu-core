# Chapter 1 double-filter handoff to Chapter 2

## Status

This note synchronizes the current Chapter 1 (`zuizui0223/island`, PR #142) interpretation with the active Chapter 2 mechanism programme.

The handoff is intentionally asymmetric:

- **Chapter 1 directly recovers the plant-side geographic filter at assemblage scale.**
- **Chapter 1 does not directly identify the pollinator-side geographic filter.**
- **Chapter 2 supplies the mechanism vocabulary and measurement chain needed to test the missing pollinator-side process.**

## Chapter 1 result: a double geographic filter is the current paper-level interpretation

Oceanic separation is interpreted as acting on two coupled systems.

### Filter A — plant source-to-island assembly

A regional source pool is filtered by:

- source availability;
- propagule dispersal ability;
- geographic separation;
- arrival probability;
- establishment;
- persistence.

The strongest current empirical support is the Palearctic taxonomic-depth result under the frozen PR142 progressive workflow:

`observed 4/4 -> after family 4/4 -> after source-matched genus 0/4`

across all-analysis/direct-only and all-native/native-nonendemic combinations.

The broad Palearctic floral/reproductive distance response is therefore compatible with genus-level lineage assembly beyond family composition rather than a robust beyond-genus primary residual.

### Filter B — pollination-channel continuity

A regionally available pollination channel may be filtered by:

- source-channel availability;
- flight/dispersal ability;
- ocean crossing;
- stepping-stone opportunity;
- establishment;
- habitat suitability;
- realized community context;
- retained effective service.

Chapter 1 does not estimate this filter directly. Its plant-side evidence is compatible with regional differences in pollination-associated architecture, but floral phenotype cannot identify visitor identity, dispersal, establishment, functional replacement or effective service.

The required channel states remain:

- retained;
- disrupted/deficient after source availability;
- structurally absent from the source region.

Structural absence is not loss.

## Distance interpretation

The formal Chapter 1 exposure is `log1p_distance_to_continent_km`; it is treated as a composite separation/connectivity/source-accessibility gradient rather than exact historical source distance.

Conceptually, `d -> 0` is a high-accessibility source boundary. Increasing `d` increases the opportunity for plant and interaction filters to act, but the response functions need not be identical:

`E_plant(z,d) != E_poll(g,d)`

and different pollination channels may also have different continuity curves:

`E_poll(g1,d) != E_poll(g2,d)`.

The Chapter 1 source-matched H3 analysis is the empirical correction that prevents this conceptual source limit from being mistaken for a literal mainland counterfactual.

## Chapter 1 ecological result passed downstream

The global plant response decomposes into at least two partially independent components:

1. reproductive assurance / selfing component;
2. pollination-associated floral architecture / attraction-access component.

These components can couple or decouple by biogeographic context.

Current broad interpretation:

- **Palearctic:** increasing separation is associated with greater accessibility/generalization and reproductive assurance; the floral attraction/access shift is not reducible to measured `selfing_core` alone.
- **Tropical:** reproductive assurance can increase while specialized/attractive floral architecture is maintained or strengthened.

The classical serial story `isolation -> selfing -> floral simplification` is therefore insufficient as a global explanation.

## Why this is a Chapter 2 problem

The unresolved link is not another plant trait. It is the interaction chain connecting partner arrival/loss to realized service and plant dependence.

The active Chapter 2 mechanism already has the required structure:

```text
partner loss / arrival balance
        x
plant starting functional state
        x
realized pollinator community
        |
        v
functional matching
        |
        v
effective service
        |
        v
local interaction / availability filtering
        |
        v
realized response branch
        |
        v
autonomous assurance
        |
        v
reproductive consequence
```

This framework can generate different downstream responses under a common broad perturbation without requiring a universal lineage-level trait rule.

## What Chapter 2 must not claim from Chapter 1

Do not infer that:

- the Palearctic response was caused by Bombus loss;
- the tropical response was caused by bird/butterfly replacement;
- guild-labelled Chapter 1 scores identify realized pollinators;
- Chapter 1 regional vectors map to specific synthetic parameter regimes;
- current distance slopes estimate pollinator dispersal ability;
- one pollinator functional group is empirically more mobile than another from Chapter 1 alone.

The mobility interpretation is a mechanistic hypothesis generated by the Chapter 1 pattern.

## Izu as the depth test

The Izu field programme is the direct test of the missing pollinator-side filter because it links, within the same populations and tagged plants:

- observation effort and visit rate;
- visitor identity/contact;
- single-visit pollen deposition;
- rate-weighted effective pollen service;
- open reproduction;
- bagged autonomous reproduction;
- supplemental-outcross reproduction;
- mature fruit/seed outcomes.

The prospective prediction freeze distinguishes service limitation, autonomous-assurance buffering, network/service allocation and non-assurance buffering before outcome inspection.

Izu is therefore not a validation case for a preferred Chapter 1 story. It is the continuity system in which the currently missing `pollinator movement/community -> effective service -> dependency/assurance -> reproduction` link can be measured directly.

## Dissertation logic

```text
Chapter 1 — island
WHEN / WHERE does source separation produce assemblage filtering?
Which floral/reproductive components couple or decouple?
How much is source/genus assembly?
        |
        v
identification ceiling:
pollinator-side geographic filter not directly measured
        |
        v
Chapter 2 — izu-core
HOW can partner arrival/loss and realized community produce different response branches?
        |
        v
comparative island confrontation
        |
        v
Izu
measure visitor -> SVD -> effective service -> dependency/assurance -> reproduction directly
```

## One-sentence handoff

> Chapter 1 shows that increasing source separation produces context-dependent plant assembly and decomposable reproductive/floral responses, while Chapter 2 asks whether the missing half of the double geographic filter—pollinator arrival, persistence and effective service—can generate those response branches when measured explicitly.
