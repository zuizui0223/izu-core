# Independent primary-source acquisition status

## Current result

The priority independent-lineage programme currently has:

- **3 active B-grade directional sources**: *Weigela coraeensis*, *Ligustrum ovalifolium*, and *Hosta longipes*;
- **0 population-level numeric effects ready for holdout**;
- **0 dependency-matched numeric lineages ready for moderation**;
- **0 independent source that explicitly localizes and demonstrates the predeclared Oshima–Toshima shared second step**.

This is not a failed meta-analysis. It is a clear separation between a useful directional layer and a still-closed quantitative layer.

Issue #92 tracks lawful source recovery, source-package provenance, double transcription, locality mapping, sampling hierarchy, uncertainty and dependency admission.

## Source-route audit — 2026-08-13

Source discovery has advanced, but source delivery and numeric admission remain separate states.

- *Ligustrum ovalifolium*: the publisher confirms `boj12092-sup-0001-si.doc` (Table S1; pairwise Tukey–Kramer floral-trait context) and `boj12092-sup-0002-si.doc` (Table S2; pollinator identities). The supporting binaries are not recovered from the current lawful execution route.
- *Hosta longipes*: the publisher confirms all five supporting files, including `psbi12002-sup-0001-si.doc` as the population-locality key, plus photograph, pollinator-sample, morphology-dissimilarity and pollinator-identity appendices. The binaries are not recovered from the current lawful execution route.
- *Weigela coraeensis*: the Springer/CiNii article route is confirmed and an external listing identifies a matching `Supplementary material 1`, but that binary is not recovered and its role is not inferred. A same-taxon Honshu–Izu population-genetic study (DOI `10.1111/j.1365-2699.2011.02634.x`) is retained only as a possible future geography cross-check after population identity is established; it cannot substitute for the 2010 morphology source.

Thus `identified route`, `binary recovered`, and `numeric gate satisfied` are three different states. No source is promoted merely because a publisher or external index exposes a filename, record, or supplement label.

## Why publisher supplement listings do not open the holdout

| taxon | identified supporting route | what it can help recover | why it is insufficient alone |
|---|---|---|---|
| *Ligustrum ovalifolium* | `boj12092-sup-0001-si.doc`, `boj12092-sup-0002-si.doc` | pairwise floral-trait context and pollinator identities | a pairwise test/significance table and identities do not supply population means, independent `n`, uncertainty or effective dependency |
| *Hosta longipes* | `psbi12002-sup-0001-si.doc` through `psbi12002-sup-0005-si.doc` | localities, photographs, pollinator sample context, morphology dissimilarity, pollinator identities | localities/dissimilarity/metadata do not by themselves supply locality-level effect estimates and effective-dependency evidence |
| *Weigela coraeensis* | externally listed `Supplementary material 1`; exact binary/role unresolved | potentially relevant source material after lawful recovery | an external listing is not a publisher-confirmed source file and supplies no morphology value, `n`, uncertainty or locality mapping by itself |

A filename, supplement label or publisher listing is an **acquisition route**, not source data. No values are reconstructed from metadata.

## Source package required after acquisition

For every article or supplement, preserve:

- source ID, DOI and complete citation;
- original filename/supplement identifier;
- lawful acquisition route and date;
- checksum/hash and source version/correction status;
- redistribution status;
- page/table/figure/supplement locator for every extracted row.

Publisher PDFs are not committed unless redistribution permission is explicit. Repository data contain provenance, code and source-derived numeric facts rather than redistributing copyrighted files.

## Two admission gates

### Gate A — independent numeric morphology effect

A source can enter a numeric morphology synthesis only after all of the following are recovered:

1. lawful full text, author manuscript, repository copy, or user-supplied source;
2. named population/locality units;
3. trait means/proportions/counts or raw observations;
4. independent biological sample size, with plant and flower levels separated;
5. SD, SE, CI, or raw data adequate to derive uncertainty;
6. trait definition, landmarks and unit;
7. measurement hierarchy and field/common-garden/herbarium context;
8. page/table/figure/supplement locator;
9. exact taxonomic and geographic mapping without inventing an unreported boundary;
10. independent reviewer cross-check and disagreement resolution.

A p-value, significance letter, pairwise significance matrix, abstract direction, or plotted point without recoverable uncertainty is not an effect size. Figure digitization, when unavoidable, remains a separately flagged sensitivity layer rather than silent A-grade evidence.

### Gate B — dependency-moderated holdout

Gate B requires Gate A **plus**:

1. effective-pollinator dependency resolved independently of floral syndrome;
2. evidence measured in the same population or transferred under a prespecified, defensible rule;
3. observation effort and effectiveness level separated from visitor identity alone;
4. survivor conditioning, hybrid replacement and taxonomic substitution audited.

A paper may become useful for morphology before it becomes admissible for the `functional exposure × effective dependency` moderation test.

## Why dependency support, not just source count, matters

The prospective design simulation uses the current empirical dimensions but explicitly synthetic dependency/effect assumptions. Its main result is that many taxa within a narrow survivor range remain less informative than a smaller set spanning low, intermediate and high directly measured dependency values.

Thus source recovery should not simply maximize the number of floral papers. Priority rises when a source can supply:

- direct or experimentally constrained effective dependency;
- repeated exposure/population mapping;
- a dependency position that extends the currently missing predictor support;
- an independent lineage rather than a taxonomic/hybrid replacement comparator.

A single high-dependency endpoint is useful but should not carry the whole moderation slope. Multiple intermediate values are needed.

## Current directional reading

- *Weigela*: gradual mainland-distance corolla decline; not a localized shared second step.
- *Ligustrum*: Izu shortening with a Hachijo endpoint; change in a source-labelled generalist rejects “generalists never change” but does not identify the focal second boundary.
- *Hosta*: shorter southern-Izu corollas combined with complex/non-monotonic variation in other floral parts; “southern Izu” is not automatically the Oshima–Toshima boundary.

Together these sources strengthen the heterogeneous-response reading. They do not provide an independent quantitative replication of the focal Campanula autonomous-reproduction breakpoint.

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

It fails if publisher metadata is promoted to a numeric result, if a shared-step claim lacks exact geographic mapping, if a priority DOI/source is missing from the native registry, or if stored admission status disagrees with the required gates.

## Claim boundary

The present evidence supports B-grade response-shape constraints only. It does not support effect sizes, equivalence/no-change claims, effective-dependency classes, an empirical dependency × FDQ coefficient, or a cross-lineage causal breakpoint.
