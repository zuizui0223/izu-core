# Chapter 2 Journal of Ecology Supporting Information route — 2026-10-06

## Principle

The Journal of Ecology main text carries only the confirmed ecological process
needed to answer the paper-level question:

1. visitor limitation changes the reproductive return to floral attraction
   before plant evolution;
2. reproductive-assurance change can precede investment decline in the declared
   delayed-selfing/costly positive-mutation setting;
3. assurance evolution is not required for investment decline;
4. the temporal sequence is not universal across reproductive settings;
5. pollen-deficit and viable-offspring readouts can differ.

Everything else is retained as scope, mechanism or reproducibility support rather
than a competing headline.

## Main-text evidence

| Main object | Evidence source | Main figure |
|---|---|---|
| Fixed-plant reproductive return | `MODEL3_FIXEDPLANT_RETURNS_RESULTS_20261005.md` | Figure 1 |
| Sequence discovery + frozen replication | `MODEL3_PERSISTENT_PROCESS_RESULTS_20261005.md`; `chapter2_1005_confirmatory_replication_20261006.json` | Figure 2A |
| Fixed-assurance necessity intervention + replication | `MODEL3_ASSURANCE_INTERVENTION_RESULTS_20261005.md`; confirmatory result | Figure 2B |
| Prior-selfing scope failure | confirmatory result, 30/64 assurance-first at threshold 0.05 | Figure 2A |
| Pollen-deficit / viable-offspring mismatch | `MODEL3_TRAIT_POLLEN_RESULTS_20261005.md` | Figure 3 |

## Supporting Information

### S1. Selection conditions and parameter dependence

Retain:
- local rare-mutant inequalities;
- 13-rate / distance replenishment diagnostics;
- reciprocal-selection surfaces;
- broad reproductive-cost, inbreeding-depression and pollen-discount parameter
  grid;
- numerical derivative verification.

Purpose: demonstrate how the focal mechanism sits inside the declared synthetic
parameter space without turning the main paper into a parameter atlas.

### S2. Finite genetic realization

Retain:
- phenotype/genotype closure counterexample;
- finite ABM versus deterministic genotype-density comparisons;
- Price accounting;
- one-locus mutation-accessibility diagnostic;
- allele-richness and late-change summaries.

Purpose: bound how reproductive selection becomes an inherited finite-population
response. These results do not define the paper-level causal claim.

### S3. Mutation/history experiment and numerical ceiling

Retain:
- the full-mutation common-environment experiment;
- persistent history under zero and positive mutation;
- all positive-mutation grid-refinement failures;
- the stopped high-resolution deterministic/PDE comparison.

Purpose: preserve the valid history/genetic-accessibility result while making
explicit that converged positive-mutation deterministic/PDE equivalence is not
established.

### S4. Exploratory attenuation of geographic divergence

Retain:
- evolving-minus-fixed assurance interaction
  (+0.08468 delayed; +0.24505 prior);
- near- and far-side within-population investment changes.

Purpose: show the exploratory observation that assurance evolution may narrow
between-environment divergence even while substantial within-environment change
occurs. This interaction was not independently replicated and is not a main-text
established claim.

### S5. Repeatability analyses

Retain the scientifically distinct content from the retired Evolution Letters
repeatability manuscript:
- directional sign uniformity versus history-level repeatability;
- population-capacity and history-pooling comparisons;
- prospective repeatability validations.

Purpose: preserve non-overlapping evidence without maintaining a second active
paper built from the same Model 3 result surface.

### S6. Natural-island confrontation

Retain:
- formal source audit;
- system-by-system confrontation ledger;
- Izu sensitivity and null-corrected failures;
- Ogasawara and other comparative examples;
- explicit missing inherited-longitudinal layer.

Purpose: establish biological plausibility and the empirical gap. Natural
systems are not used to calibrate synthetic cells or validate a named historical
transition.

## Material that must not migrate back into the headline

- the unresolved high-resolution positive-mutation deterministic/PDE comparison;
- a universal assurance-first statement;
- a complete mediation claim through realized selfing;
- a calibrated mapping from synthetic distance/time to kilometres/years;
- a claim that pollen limitation is itself a fitness measure;
- region-to-model-cell assignments for Chapter 1 or named islands.

## Submission consistency rule

The anonymous Journal of Ecology manuscript is
`docs/CHAPTER2_MANUSCRIPT_JOE_20261006.md`.

The longer scientific source
`docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md`
remains provenance and should not be submitted in parallel.

Any future main-text restoration from S1–S6 requires an explicit reason tied to
a reviewer/editor request or a claim that cannot otherwise be evaluated.
