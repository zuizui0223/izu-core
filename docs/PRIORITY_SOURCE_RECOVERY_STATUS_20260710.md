# Priority primary-source recovery status — 2026-07-10

## Access audit

The four predeclared DOI records were resolved successfully through OpenAlex.
No legal OA PDF or OA repository landing was found for any of them in the
current all-location metadata.

| priority | source | access class | next action |
|---:|---|---|---|
| 1 | Weigela 2010 | closed / publisher only | institutional library or author manuscript request |
| 2 | Ligustrum 2013 | closed / publisher only | institutional library or author manuscript request |
| 3 | Lilium 2018 | closed / publisher only | institutional library or author manuscript request |
| 4 | Clerodendrum 2012 | closed / publisher only | retain as context unless full text is needed |

The machine-readable result is
`data/predictive_meta/priority_source_access_routes_20260710.csv`.

## Extraction order after a PDF is obtained

### Weigela

Recover the locality table first. Only then map each population to mainland,
Oshima/*B. ardens*, or no-Bombus. Extract trait means, n, dispersion and exact
table/figure locations. The title alone supplies no direction.

### Ligustrum

Recover the population-level floral table and named island localities. The
publisher abstract already supports qualitative shortening on Izu and stronger
shortening on Hachijo, but those statements remain direction-only until the
original values and uncertainty are transcribed.

### Lilium

Recover floral traits and pollinator assemblages, then test whether the
comparison is confounded by variety identity. Do not pool it as a within-lineage
island effect automatically.

### Clerodendrum

This is explicitly a comparison between taxa. It remains contextual and cannot
be used as a within-lineage prediction replicate.

## Current decision

No source is promoted. `quantitative_effects.csv` remains empty for these
papers. The ordered workflow is blocked at original-source acquisition, not at
analysis code.

The next evidence-bearing action requires one of:

1. authenticated institutional-library retrieval;
2. a PDF supplied by the user; or
3. a lawful author manuscript supplied by an author or repository.

Until then, the independent specialist holdout remains unopened and the
environment-only final comparison is not advanced ahead of it.
