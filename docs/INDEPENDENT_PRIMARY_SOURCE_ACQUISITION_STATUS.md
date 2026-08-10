# Independent primary-source acquisition status

## Current result

The priority independent-lineage programme currently has:

- **3 active B-grade directional sources**: *Weigela coraeensis*, *Ligustrum ovalifolium*, and *Hosta longipes*;
- **0 population-level numeric effects ready for holdout**;
- **0 dependency-matched numeric lineages ready for moderation**;
- **0 independent source that explicitly localizes and demonstrates the predeclared Oshima–Toshima shared second step**.

This is not a failed meta-analysis. It is a clear separation between a useful
directional layer and a still-closed quantitative layer.

Issue #92 tracks lawful source recovery and transcription.

## Why publisher supplement listings do not open the holdout

Publisher metadata now identifies acquisition routes for two sources:

| taxon | listed supporting files | what they can help recover | why they are insufficient alone |
|---|---|---|---|
| *Ligustrum ovalifolium* | `boj12092-sup-0001-si.doc`, `boj12092-sup-0002-si.doc` | pairwise floral-trait context and pollinator identities | a pairwise test/significance table and identities do not supply population means, independent `n`, and uncertainty |
| *Hosta longipes* | `psbi12002-sup-0001-si.doc` through `psbi12002-sup-0005-si.doc` | localities, photographs, pollinator sample context, morphology dissimilarity, pollinator identities | localities/dissimilarity/metadata do not by themselves supply locality-level effect estimates and effective-dependency evidence |
| *Weigela coraeensis* | no current supplement route locked | full text and locality/trait tables remain the decisive route | the abstract supplies a gradual response shape only |

A filename or publisher listing is an **acquisition route**, not source data.
No values are reconstructed from metadata.

## Two admission gates

### Gate A — independent numeric morphology effect

A source can enter a numeric morphology synthesis only after all of the
following are recovered:

1. lawful full text, author manuscript, repository copy, or user-supplied source;
2. named population/locality units;
3. trait means/proportions/counts or raw observations;
4. independent biological sample size;
5. SD, SE, CI, or raw data adequate to derive uncertainty;
6. trait definition and unit;
7. page/table/figure/supplement locator;
8. exact geographic mapping without inventing an unreported boundary.

### Gate B — dependency-moderated holdout

Gate B requires Gate A **plus**:

1. effective-pollinator dependency resolved independently of floral syndrome;
2. evidence measured in the same population or transferred under a
   prespecified, defensible rule.

This distinction matters. A paper may become useful for morphology before it
becomes admissible for the `functional exposure × effective dependency`
moderation test.

## Current directional reading

- *Weigela*: gradual mainland-distance corolla decline; not a localized shared
  second step.
- *Ligustrum*: Izu shortening with a Hachijo endpoint; change in a
  source-labelled generalist does not imply the specialist hypothesis is false,
  but it rejects “generalists never change.”
- *Hosta*: shorter southern-Izu corollas combined with complex/non-monotonic
  variation in other floral parts; “southern Izu” is not automatically the
  Oshima–Toshima boundary.

Together these sources strengthen the current heterogeneous-response reading.
They do not provide an independent quantitative replication of the focal
Campanula autonomous-reproduction breakpoint.

## Machine-readable audit

```bash
python scripts/audit_independent_source_acquisition.py
```

Output:

```text
artifacts/independent_source_acquisition/summary.json
```

The audit reads:

- `data/design/independent_primary_source_acquisition.json`;
- `data/predictive_meta/primary_source_native_evidence.csv`.

It fails if publisher metadata is promoted to a numeric result, if a
shared-step claim lacks exact geographic mapping, if a priority DOI/source is
missing from the native registry, or if stored admission status disagrees with
the required gates.

## Claim boundary

The present evidence supports B-grade response-shape constraints only. It does
not support effect sizes, equivalence/no-change claims, effective-dependency
classes, or a cross-lineage causal breakpoint.
