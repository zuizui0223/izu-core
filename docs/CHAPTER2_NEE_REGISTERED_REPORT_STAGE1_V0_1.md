# Stage-1 skeleton — Nature Ecology & Evolution Registered Report

Version: v0.1 — 2026-09-12  
Status: **pre-data working surface; not yet submission-ready**  
Parent promotion lock: `data/design/chapter2_nee_predata_promotion_lock_20260912.json`

## Working title

**Why the same pollinator-community reorganization need not produce the same plant reproductive response**

Alternative shorter title:

**Plant state and realized pollinator communities jointly determine reproductive response**

## Stage-1 scientific sentence

> Pollinator-community change is not expected to map to one plant response because coarse community amount, realized effective composition and plant pre-outcome state occupy different positions in the response architecture; we prospectively test whether plant state and effective-community composition interact, whether that relation propagates through pollination function to reproductive outcome, and whether averaging independent exposure opportunities changes the relative contribution of state versus community realization.

## Why this is a Registered Report question

The source mechanism is already frozen before focal field outcomes:

- realized richness changes coarse regime placement but does not eliminate branch contingency;
- realized composition x plant starting state remains non-additive after richness control;
- finite-community realization variance changes with aggregation/system scale;
- the relative contribution of plant starting state versus community realization changes across the frozen synthetic sequence.

The field study is therefore designed to **falsify natural predictions derived before outcome inspection**, rather than calibrate the synthetic model after observing Izu responses.

A null result is informative: it would show that the synthetic conditional-response mechanism does not transport under the declared natural mapping, or that one of the required natural states is not identifiable at the available measurement resolution.

---

# Introduction — planned logic

## Paragraph 1 — ecological problem

Pollinator-community reorganization can arise through colonization, extinction, replacement, phenology, disturbance and environmental change. Plant responses are often summarized using visitor richness, visitation rate, or mean reproductive success, implicitly treating community change as if it mapped monotonically to plant outcome.

## Paragraph 2 — conceptual gap

Three objects should be distinguished:

1. **coarse community amount/breadth** — how much or how many visitors are observed;
2. **realized effective composition** — which visitors actually provide functional pollen service and in what proportions;
3. **plant pre-outcome functional state** — the plant-side configuration on which the realized community acts.

The same coarse visitor breadth can therefore conceal different effective compositions, and the same effective community can have different consequences for plants in different starting states.

## Paragraph 3 — source theory

Chapter 2's frozen synthetic mechanism predicts a conditional response geometry. Exact richness matching moves the ensemble mean regime but leaves strong individual state x community non-additivity. Reducing finite-community realization variance changes the relative contribution of starting state versus realized community while non-additive branching can persist over the finite audited range.

The field study does not predict the synthetic numerical crossover or equate a field diversity index with synthetic `k`. It tests only the qualitative natural implications defined prospectively below.

## Paragraph 4 — empirical gap

The existing source audit contains many systems measuring response, community change, filtering or reproductive dependence separately, but no admitted study links pre-outcome plant state, realized visitor composition, visitor effectiveness, reproductive dependency and mature seed in one outcome-independent same-unit chain. Existing partial systems therefore motivate the measurement architecture but cannot provide the focal confirmatory test.

## Paragraph 5 — study objective

We will create a transition-linked natural test in which plant state, visitor exposure, single-visit effectiveness, pollination dependency and mature reproductive outcome are linked within prespecified `block_id x plant_id` units.

---

# Confirmatory hypotheses

## H1 — composition beyond amount [P1]

**Prediction:** after controlling for monitored exposure effort, total visitation and a predeclared coarse richness/diversity summary, realized effective-community composition will retain predictive information for the mature reproductive endpoint.

**Primary contrast:** model/estimand retaining effective composition versus the same frozen model with composition removed while keeping coarse amount/breadth terms.

**Falsification:** no out-of-block predictive or inferential gain from effective composition, or gain disappears after prespecified effort/total-service controls.

## H2 — plant state x realized community [P2; primary NEE hypothesis]

**Prediction:** pre-outcome plant functional state interacts with realized effective-community composition for same-plant reproductive response.

**Primary relational estimand:** the predeclared state x effective-community term or low-dimensional relational contrast defined before focal outcome opening.

**Falsification:** the relational term is not estimable with adequate support/reliability, or its predictive contribution is negligible under the frozen decision rule.

## H3 — functional bridge [P3]

**Prediction:** visitor identity/composition maps to an independent measure of pollination effectiveness before the mature reproductive endpoint is evaluated.

**Primary intermediate:** background-controlled single-visit conspecific pollen deposition where feasible.

**Falsification:** effective-service weights cannot be estimated reliably or visitor composition does not map to the independent functional intermediate under the frozen model.

## H4 — dependency consequence [P4]

**Prediction:** reproductive treatment contrasts identify whether realized pollination service can alter mature reproductive outcome.

**Core treatment family:** open natural pollination, bagged autonomous treatment and supplemental outcross treatment. A single-visit-then-bagged treatment may be included if feasible and frozen before confirmatory execution.

**Falsification:** treatment implementation/retention is inadequate or the declared dependency contrast cannot be estimated.

## H5 — determinant-order shift with exposure aggregation [P5]

**Prediction:** as additional independent prespecified community-exposure opportunities are aggregated, community-realization contribution will decline relative to plant-state contribution, while state x community non-additivity is retained and reported over at least part of the estimable field range.

**Explicit non-predictions:**

- no prediction of a field threshold at synthetic `k = 4`;
- no claim that visitor richness, Hill diversity or effective-service breadth equals synthetic `k`;
- no requirement that contribution changes monotonically at every adjacent aggregation level.

**Falsification:** no directional redistribution of contribution, the pattern disappears under out-of-block prediction, or a prespecified effort/total-service/site/time control explains the apparent redistribution.

## H6 — external transport [P6; escalation hypothesis]

**Prediction:** the H2 state x effective-community relation will be challenged in at least one independent natural context or untouched external dataset if an admissible dataset exists before Stage-1 lock.

H6 is a breadth/escalation criterion, not a condition for the validity of H1-H5 and not a requirement for the closed Oikos manuscript.

---

# Methods

## Study system

Prospective Izu field system. Final taxa, populations, sites and field windows must be frozen before confirmatory outcome collection/opening.

Historical *Bombus* loss is not the confirmatory treatment and will not be inferred from contemporary associations.

## Strict observational/experimental unit

```text
block_id x plant_id
```

A block is a prespecified population/site/time exposure window fixed before reproductive outcomes are known. Blocks cannot be split, merged or moved after inspecting effectiveness, dependency or seed outcomes.

Flowers and visits are subsamples within plants. Plants are nested within blocks.

## Pre-outcome plant state

The primary plant-state vector must be measured before the reproductive outcome and frozen before focal outcome opening.

Current admissible role:

- same-plant floral geometry / corrected functional position;
- additional pre-outcome coordinates only if justified and frozen before confirmatory execution.

No phenotype measured after the focal response may be back-filled as starting state.

## Visitor exposure

Required records:

- usable monitored flower-hours;
- zero-visit windows retained;
- visitor taxon/group identity with resolution status;
- visit counts/rates linked to block and plant where the protocol allows.

Raw richness is an E1 coarse-regime exposure only and is never treated as a literal counterpart of synthetic `k`.

## Visitor effectiveness

Primary intended measure:

- single-visit conspecific pollen deposition on a previously unvisited receptive stigma;
- paired/background no-visit SVD control;
- visitor-group-specific background-adjusted effectiveness where support permits.

Effective-service weight for visitor group `g` in block `b` is intended to combine effort-standardized visitation and independently measured background-adjusted effectiveness.

Negative/invalid weights are not silently truncated unless the exact rule is fixed at Stage 1.

## Effective-community representation

Primary representation should preserve functional composition. Candidate summaries include:

- normalized effective-service composition vector;
- effective-service Hill q=2 and evenness as secondary breadth/concentration summaries;
- total effective service as a separate amount term.

The vector representation and any dimension reduction must be frozen before focal endpoint inspection.

## Reproductive dependency treatments

Core within-plant/block treatment family:

1. open natural pollination;
2. bagged autonomous treatment;
3. supplemental outcross treatment.

Treatment allocation, number of flowers per treatment, randomization and replacement rules must be frozen before confirmatory execution.

If a single-visit-then-bagged arm is added, it must be declared before field execution and cannot be activated only after observing visitor-group effects.

## Mature endpoint

Primary terminal endpoint: mature seed outcome linked through treatment and `fruit_id` where applicable.

The exact response scale (count, proportion, hurdle/two-part representation, or other) will be fixed from pilot dispersion/measurement diagnostics using outcome-blind rules where possible and before confirmatory focal analysis.

## Missingness and measurement failure

- zero visits are observations, not missing data;
- missing/uncontrolled SVD is not imputed as zero effectiveness;
- lost/damaged reproductive treatments remain explicit failure states;
- incomplete mature-fruit/seed linkage is reported and cannot be silently dropped;
- any exclusion must follow a Stage-1 rule independent of effect direction.

---

# Sampling plan

## Design objective

The design must power/identify the **relational H2 estimand**, not merely detect a visitation or treatment main effect.

## Pilot role

Pilot data may be used only to estimate:

- block/plant recruitment and retention;
- visitation zero inflation and count dispersion;
- SVD measurement success and background variance;
- treatment loss/damage rates;
- mature-seed variance/distribution family;
- plausible support of effective-community composition across blocks.

Pilot outcomes must not be used to choose a predictor because its association is favorable.

## Power / Bayesian design criterion — OPEN ITEM BEFORE STAGE 1

The final Stage-1 package must include one of:

1. simulation-based frequentist power for the frozen H2 relational estimand under a prespecified smallest effect of scientific interest; or
2. Bayesian assurance / expected posterior precision for that relational estimand.

The simulation must preserve the actual hierarchy:

```text
flowers/visits within plant
plants within block
repeated prespecified blocks within site/island where applicable
```

A nominal flower or visit count cannot be treated as independent sample size.

## Precision safeguards

The final sample-size rule should include minimum support for:

- number of independent plants;
- number of prespecified blocks;
- effective-service composition variation;
- SVD-controlled visitor groups;
- retained plants with all core reproductive treatments reaching terminal status.

Exact numbers remain open until pilot feasibility/dispersion is frozen.

---

# Confirmatory analysis pipeline

## A1 — measurement/admission audit

Before biological inference, report:

- raw/usable monitored flower-hours;
- zero-visit windows;
- taxonomic/group resolution;
- SVD coverage and background controls;
- full-chain plant/block counts;
- treatment retention/failure;
- mature fruit-to-seed linkage completeness.

Failure of a measurement gate yields `not_evaluable`, not biological absence.

## A2 — H1 coarse amount versus composition

Fit the frozen hierarchical response model with effort/amount/breadth terms. Compare against the model adding effective-community composition using the predeclared inferential or out-of-block predictive criterion.

## A3 — H2 relational test

Estimate the predeclared plant-state x effective-community relation with plants nested in blocks. No post-hoc thresholding of plant state, dependency or community breadth.

## A4 — H3 functional intermediate

Test visitor/group differences in background-controlled effectiveness and construct the effective-service representation only when its measurement gate passes.

## A5 — H4 dependency/endpoint test

Estimate open/bagged/supplemental contrasts on the mature endpoint under the frozen hierarchical model.

## A6 — H5 exposure aggregation

Create aggregation levels only from prespecified independent exposure opportunities. Re-estimate or compare plant-state, community-realization and relational contributions under the frozen procedure.

No breakpoint search is allowed. The synthetic `k≈4` location is never used as a field cutoff.

## A7 — H6 transport

Apply the frozen H2 mapping to the independent system/dataset without retuning predictor direction, threshold, outcome definition or aggregation level.

---

# Quality-control and interpretation states

Each confirmatory hypothesis receives one of:

```text
SUPPORTED
FALSIFIED_OR_ADVERSE
NOT_EVALUABLE
```

`NOT_EVALUABLE` is mandatory when the relevant measurement or support gate fails. It cannot be collapsed into a biological null.

No combination of secondary/exploratory analyses can rescue a failed primary gate.

---

# External evidence before new Izu data

Use `docs/CHAPTER2_EXTERNAL_TRANSPORT_TRIAGE_20260912.md`.

Current interpretation:

- Seychelles / *Thespesia*: individual-level exposure + direct dependency architecture prototype;
- *Nicotiana glauca*: strongest visitor-effectiveness + reproductive-dependency component bridge, provenance still partial;
- *Guaiacum sanctum*: strong population-level visitor-assemblage + breeding-experiment separation;
- no admitted external system supplies the full outcome-independent same-unit chain.

These systems constrain design and may test components; they do not count as pilot confirmation of H1-H5.

---

# Data, code and protocol commitments

If submitted as a Nature Ecology & Evolution Registered Report, Stage 1 will commit to:

- sharing anonymized/raw ecological data as appropriate, processed data, study materials and analysis code for published results;
- registering the Stage-1 approved protocol in a recognized repository following acceptance in principle;
- retaining a field/laboratory log and linking the Stage-2 manuscript to the approved protocol and public archive;
- separating confirmatory from exploratory analyses.

---

# Open items before this becomes Stage-1 submission-ready

Only the following classes may remain open:

1. exact Izu sites/populations/taxa and feasible field dates;
2. pilot-derived dispersion, retention and measurement-success parameters;
3. final power/Bayesian assurance calculation;
4. exact plant-state coordinate set if a feasibility variable is not yet measurable;
5. final effective-community dimension-reduction representation, chosen without focal endpoint inspection;
6. ethics/permit statements if required;
7. author list, affiliations and declarations.

The biological hypotheses P1-P5, same-block linkage, no-literal-`k` mapping, failure-state handling and promotion logic are not open to outcome-driven revision.

---

# Promotion rule

```text
Stage-1-ready design + broad H1-H5 importance
    -> submit NEE Registered Report

Stage-1 editor/review judges breadth insufficient but design strong
    -> retain same frozen protocol and route to another broad ecology venue

field measurement gates fail
    -> report NOT_EVALUABLE where appropriate; do not retune the synthetic mechanism

H2/P2 adverse or null under adequate measurement
    -> valid falsification; current closed Oikos mechanism paper remains unchanged
```

## Final stop rule

> The purpose of pre-data work is to make the future result harder to reinterpret, not easier to rescue.
