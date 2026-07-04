# Herbarium image data-expansion protocol

## Why this is the next viable public-data lane

The strict iNaturalist audit found that public field photographs currently do
not yield a balanced positive specialist holdout across mainland, Oshima and the
no-Bombus islands. That does **not** mean public data are exhausted. Digitized
preserved specimens provide a distinct candidate source with three advantages:

- collection date, locality, institution and catalogue metadata;
- occasional flowers plus a sheet ruler or other scale reference; and
- independent coverage that can complement field-observation photographs.

They are not automatically phenotype data. A mounted specimen can be sterile,
fruiting, closed, poorly preserved, or lack the predeclared structure.

## What the audit retrieves

`paper/audit_gbif_herbarium_media.py` queries GBIF for Japanese records matching
all of the following:

- `PRESERVED_SPECIMEN`;
- `StillImage` media;
- coordinates; and
- one taxon in `data/predictive_meta/herbarium_cohort_manifest.csv`.

Candidate records are then placed into the project's existing conservative
regional proxy circles: Izu-peninsula mainland, Oshima, and individual
no-Bombus islands. The audit records every request, taxon match, retrieval
status and media candidate. API errors are never converted to zero counts.

## Candidate gate

A taxon reaches a protected blind sheet only when the audit has at least two
candidate media records in each of:

```text
large-Bombus mainland proxy
B. ardens Oshima proxy
pooled no-Bombus island proxies
```

The blind sheet contains taxon, image URL and score fields but no region or
regime. The matching key contains the hidden regional metadata and must remain
unopened until scoring is complete.

## Human stage-0 screen

A candidate becomes an ordinal morphology observation only when a reviewer
records all of the following while blinded:

1. flower is open;
2. the predeclared focal structure is visible;
3. a scale/ruler or usable reference is present; and
4. the image is comparable for that taxon's prespecified trait.

A missing image feature is an exclusion, not score zero. Specimen image data
remain a lower evidence tier than source tables and cannot estimate pollinator
identity, effective pollination, realised outcrossing or historical causality.

## Role in the synthesis

- **Campanula**: can add an auxiliary morphology check only; it does not replace
  source-locked flower length, outcrossing or bagged-capsule data.
- **Specialist-like taxa**: specimen cohorts may create an independent visible
  morphology test where field-photo coverage failed.
- **Generalists**: specimen cohorts may strengthen the negative-control test.
- **Ligustrum / Weigela original articles**: still require original table
  recovery for numerical primary-source evidence; specimen images do not
  substitute their source-native comparisons.
