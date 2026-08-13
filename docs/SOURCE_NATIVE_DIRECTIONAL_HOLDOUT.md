# Source-native directional holdout

## Purpose

Some independent Izu studies report biologically useful directions or response shapes but their publicly accessible routes do not expose the population means, uncertainty, sample sizes and exact locality tables required for the A-grade quantitative holdout.

Those studies are not discarded and their missing numbers are not reconstructed. They enter a separate **B-grade source-native directional layer**.

The layer answers a narrower question:

> Does an independent original source itself demonstrate the same predeclared Oshima-to-Toshima second boundary, or does it only document a broader/other geographic response?

It cannot estimate an effect size or causal effect.

## Hard rule for shared-second-step support

A directional record may be labelled `supports` only when the original source explicitly localizes observations on the Oshima side and the post-boundary side and reports a response compatible with that boundary.

The following are **not** sufficient:

- “Izu Islands”;
- “southern Izu”;
- “Hachijo was strongest”;
- a gradual decline with mainland distance;
- a significant mainland-versus-island contrast without named island mapping.

This prevents broad island geography from being silently converted into the focal breakpoint.

## Dependency is a separate gate

`data/predictive_meta/source_native_dependency_registry.csv` classifies pollinator dependency from explicit source evidence rather than floral form.

A dependency class and a usable within-lineage island comparator are separate requirements. Current source-native status is:

- **Ligustrum ovalifolium** — source-labelled `generalist`; candidate negative control for a *shared breakpoint*, not for zero geographic change;
- **Weigela coraeensis** — `unresolved`; the accessible primary abstract compares visitor composition and suggests pollinator-fauna influence but does not establish exclusive/effective Bombus dependence;
- **Hosta longipes** — `unresolved`; the abstract reports geographically variable pollinator fauna but does not resolve one effective-pollinator dependency class;
- **Goodyera henryi** — source-resolved `bombus_dependent`, but the Kozu comparator is hybrid, so it is not a clean same-lineage regime test;
- **Goodyera similis** — direct non-Bombus scoliid-wasp dependency on mainland and Kozu; retained as a dependency-control direction;
- island **Lilium auratum var. platyphyllum** — source-supported Lepidoptera specialization, retained as an alternative-mechanism context because variety identity is confounded with geography.

Therefore the independent Bombus-dependent within-lineage holdout is currently blocked even before the numeric-effect gate is considered.

## Current independent directional lineages

### Weigela coraeensis

The source reports smaller Izu corollas and a gradual decrease in corolla length with mainland distance. It also reports no floral-scent difference between the compared varieties.

These are useful directional channels, but the source table needed to map exact populations to the three-regime scaffold is not available through the verified public route. Therefore the current directional classification is `does_not_demonstrate` a shared second step, not `supports` and not `falsifies`.

The source does not establish exclusive/effective Bombus dependence, so Weigela is kept `uncertain` in this strict dependency layer. The no-reported-scent-difference channel is not an equivalence result.

### Ligustrum ovalifolium

The source reports shorter Izu corolla tubes/stamens and stronger shortening on Hachijo, and the article itself labels the system `generalist` in its keywords.

This is important for the negative-control logic: a generalist can change geographically. The negative-control prediction is therefore **absence of a repeated specialist-specific breakpoint**, not zero island response.

The accessible supporting-information metadata provides significance and pollinator tables but not the population means plus uncertainty required for an effect-size analysis. The exact Oshima-to-Toshima boundary is therefore not demonstrated.

### Hosta longipes

The source reports shorter corollas in southern Izu, while other floral parts show complex geographic variation. Exact locality and pollinator tables exist as supporting material but their contents are not currently recoverable through the verified public route.

The dependency class is retained as `uncertain`, and `southern Izu` is not translated into the Oshima-to-Toshima boundary.

## Current directional conclusion

No independent B-grade lineage currently demonstrates the predeclared Oshima-to-Toshima shared second step.

This means:

- the universal claim that every independent lineage repeats the focal breakpoint is **not supported by the current directional evidence**;
- it does **not** statistically falsify a pollinator-regime interaction, because exact breakpoint localization and dependency classification remain incomplete;
- independent sources already show heterogeneity: gradual decline, endpoint-intensified island shortening and complex multivariate morphology;
- the only source-resolved Bombus-dependent independent lineage currently identified (Goodyera henryi) lacks a pure same-lineage island comparator;
- the A-grade quantitative specialist holdout remains closed.

## Run

```bash
python scripts/run_source_native_directional_holdout.py
python scripts/run_source_native_dependency.py
```

The reports preserve every claim boundary, show which lineages support/fail to demonstrate/cannot resolve the shared second step, and state whether a clean source-resolved Bombus-dependent comparator exists.
