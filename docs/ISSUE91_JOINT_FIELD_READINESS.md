# Issue #91 joint field readiness

## Current state

The field implementation is ready, but the focal empirical rows are still missing.

Two readiness questions must remain separate:

```text
A. effective-pollinator dependency readiness
B. functional-exposure (FDQ) readiness
```

A population can pass A while B is withheld. A dependency × FDQ analysis requires both.

## A. Dependency readiness

The direct dependency panel uses the existing linked chain:

```text
plant registry
  -> usable observation effort, including zero-visit windows
  -> visitor bout / contact
  -> SVD + no-visit background control
  -> rate-weighted effective service
  -> open_pollinated / bagged_autonomous / supplemental_outcross
  -> fruit / seed linkage
```

Structural completion of this panel does **not** require FDQ. Group-level visitor records can remain valid for SVD and service summaries even when species-level taxonomic resolution is unavailable.

## B. FDQ readiness

The prospective functional-exposure path is:

```text
confirmed visitor_taxon_id
  + site-specific admitted proboscis_length_mm
  + visitor-bout abundance
  -> Rao-Q FDQ
```

The source-locked estimand is:

```text
FDQ = sum_i sum_j p_i p_j |L_i - L_j|
```

Official FDQ is emitted only when every positive-abundance visit in an exposure unit is taxon-resolved at confirmed confidence and every positive-abundance taxon has an admitted numeric site-linked trait.

Missing/unresolved visitors are never dropped followed by renormalization. Usable zero-visit effort is retained but is not called `FDQ = 0`.

## Trait acquisition

Two routes are admissible.

### Historical source-native route

Hiraiwa & Ushimaru (2017) report species × site mean proboscis length in supplementary Table S2. The current repository still has zero recovered numeric values for the 209 named taxa in the frozen 2024 visitor artifact, so historical source-native reuse remains blocked.

### Prospective measured-new route

New #91 visitor taxa can be made FDQ-ready without waiting for Table S2 by using:

```text
templates/field_pollinator_proboscis_measurement_template.csv
scripts/audit_field_proboscis_measurement.py
```

The source-matched admission rule is:

- one independent specimen per row;
- digital-caliper proboscis length in mm;
- summarize by visitor taxon × site;
- target five independent specimens;
- fewer than five only when `all_available_at_site=yes` explicitly records that all available specimens were measured;
- only admitted groups become `trait_status=measured_new`.

Family means, body-size classes, visitor groups, functional bins and fuzzy taxonomic matching are not primary FDQ trait substitutes.

## Field collection order

Inside one focal population:

1. establish stable plant/flower IDs and usable observation effort;
2. retain `visitor_taxon_id` whenever taxonomic identification is confirmed and preserve lawful/feasible trait specimens when the site-linked trait is missing;
3. secure no-visit SVD controls;
4. obtain controlled SVD across independent plants;
5. complete the three reproductive treatments across independent plants;
6. preserve terminal fruit/seed and loss/damage outcomes;
7. add parentage only after the core linkage is intact.

The second step protects future FDQ without delaying dependency structural completion.

## Joint-analysis gate

The empirical dependency × FDQ question opens only when the same declared exposure/dependency unit has:

- an admitted direct dependency estimate;
- an official FDQ value under complete taxon/trait coverage;
- adequate independent plant/site/time support for the intended inference.

Campanula alone remains one focal system, not a cross-lineage interaction test.

## Claim boundary

FDQ is a functional-exposure quantity, not pollinator effectiveness. SVD/effective service is not reproductive dependency. Direct dependency is not historical selection. Keeping these gates separate prevents a missing trait table from invalidating useful dependency data while also preventing broad visitor labels from being silently promoted into the quantitative FDQ axis.
