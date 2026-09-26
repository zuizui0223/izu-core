# Model 3 island ecology: completion evidence matrix

Status: production is running. This document defines the remaining reporting and
acceptance checks; no partial ecological outcomes have been inspected to select
contrasts. The active goal is not complete. Source commit: `13cc99b`; production
manifest: `data/design/model3_island_v2.json`, SHA256
`0dcf6190c27f5fc9c50b07a270826932691f8c21886ff4b148c6fe299bf3135e`.

## Scientific coverage

Counts below are compiled from the immutable manifest, not inferred from output
folders. All 19,968 cases must be accounted for, including non-evaluable and
extinct outcomes. A case is not an independent history: trajectory cells use two
demographic repeats per history, and assays do not duplicate that axis.

| Question | Declared contrast and ecological estimand | Cells / cases | Completion evidence still required |
|---|---|---:|---|
| Does reduced visitation change the return on attraction at fixed assurance? | Fixed-state activity × mismatch × assurance × investment-cost assays; outcross and total reproductive gradients, not evolved endpoints | 16 / 2,048 | All assay ledgers, history-level intervals, gradient figure distinguishing outcross benefit from total viable output |
| Does the order of absence or mismatch matter after visitors return? | Early versus late equal-duration gaps or mismatch, same visitor identities and total exposure, common final 120 years; uninterrupted reference | 5 / 1,280 | Investment trajectories, occupancy, genetic retention and paired terminal contrasts; no permanent-history claim beyond 200 years |
| Do seeds and visitors respond differently to isolation? | Independent seed and visitor distances 0, 1, 3 dispersal-scale units, ecological assembly histories | 9 / 2,304 | Two-dimensional connectivity figure with all cells, occupancy and conditional investment; distinguish bundled assembly from pure order effects |
| Does founding differ from inherited separation? | Empty founding versus inherited population/community plus identical-present-state label controls | 4 / 1,024 | Matched-history check, colonization and persistence accounting; no nonexistent founder baseline on an initially empty island |
| Is investment reduction associated with inherited assurance? | Fixed disabled/half/high assurance and inherited assurance with timing, pollen discount and cost controls | 7 / 1,792 | Investment and assurance trajectories, retained selfed/outcross recruits and expected reproduction separately; no natural direct/indirect mediation claim |
| Is visitor restoration sufficient for ecological and genetic recovery? | Visitor-only, source immigrants, resident-genotype immigrants, mutation regimes, 200/2,000-year horizons; seven fully matched uninterrupted controls | 14 / 3,584 | Treatment-minus-linked-control trajectories/endpoints for occupancy, traits, heterozygosity and ancestry; undefined resident controls explicit; replacement is not resident adaptation |
| Are finite-population results separable from numerical resolution? | Capacity 48/192/768 with matched initial frequencies and separate per-capita/fixed-total arrivals; grid refinement and grid/continuous individual mutation | 14 / 3,584 | Bias and MAE, occupancy and trait precision, grid comparisons and effect/tolerance checks; density is a discrete closure, not PDE or the stochastic trajectory mean |
| Does adult longevity change the effect of interruption? | Annual versus expected 4/10-year adults; annual and lifetime-matched reproductive budgets | 5 / 1,280 | Parental-age-derived generation intervals, persistence and recovery trajectories; years are not generations for overlapping adults |
| Do response components and predictions transfer across island regimes? | Three initial investment states crossed with histories and demographic repeats; two connectivity regimes and disjoint held-out histories | 6 / 3,072 | Occupancy/conditional investment S/C/I, within-cell variation, factor weights, survivor support and held-out errors; no required rank ordering |

## Required interpretation and quantitative checks

1. **Assurance and attraction:** juxtapose fixed-state reproductive gradients with
   inherited-trait trajectories. Declining visitors do not mechanically increase
   the cost coefficient. A selfing association alone does not distinguish causal
   pathways. Actual retained recruits and expected fertilization/viability ledgers
   have different denominators and must be labelled.
2. **Recovery:** compare each recovery treatment with its `counterfactual` link
   before comparing rescue mechanisms. Show demographic, genetic and trait
   recovery separately. Mutation is present throughout each declared treatment;
   seed immigration windows are explicit. A long horizon does not establish an
   irreversible state or prove equilibrium.
3. **Extinction:** unconditional occupancy keeps every history. Trait differences
   are conditional on eligible surviving pairs and a defined initial baseline.
   Report selection of that subset rather than assigning zero traits to extinction.
4. **Finite processes:** retain the archived exact one-step expectation and finite
   pollen-exclusion audit as separate evidence. Do not add these nonlinear
   diagnostic contrasts into a unique percentage attribution of long-run change.
   The new full trajectory difference combines processes; drift-only attribution
   remains excluded without an identifying intervention.
5. **Numerical gates:** inspect fixed-assurance 5/7/11-node and inherited-assurance
   coarse/fine controls, separately for individual projection modes and density.
   Declared tolerances are .01 trait and .02 occupancy; meaningful differences are
   .05 investment, .10 occupancy and .10 heterozygosity. An observed small error
   and a confidently bounded small error are different evidence. Insufficient
   Monte Carlo precision is reported, not repaired by selecting extra histories.
6. **Precision:** report the declared 128 independent histories per cell and two
   demographic repeats, independent-history occupancy bounds and conditional
   interval widths. The occupancy half-width target is .125; the much smaller
   numerical occupancy tolerance need not be resolvable with this replication.
   Do not call two demographic repeats two independent visitor histories.
7. **S/C/I and exposure:** S is the declared initial-state axis, C the realized
   exogenous history axis, and I their non-additive cell-mean component. Report
   within-cell sampling variation separately. The stored 21-plant reference
   service panel is independent of evolved plant traits. A lifetime-weighted
   effective-exposure diagnostic needs a defensible stationary covariance and
   uncertainty; changing schedules, zero variance or an unverified covariance
   cannot be assigned a numerical k. This diagnostic is not old history pooling.
8. **Novelty:** compare supported ecological predictions against the primary
   precedents already reviewed in `MODEL3_NEAREST_PRECEDENTS_20260926.md`.
   Generic selfing rescue, priority effects and finite/density differences are
   not claimed as new. Q1 remains motivation, not a fitted four-region response.

## Execution and deliverable audit

| Requirement | Current evidence | Remaining action |
|---|---|---|
| Preserve frozen models and prior results | 14 baseline SHA256 checks pass in preproduction receipt | Recheck after final reporting and staging |
| Implement approved modules and correct reviewed issues | 168 package tests; final full suite 1,948 pass, 1 skip; five review findings repaired | Preserve receipts and distinguish verification from biological validation |
| Immutable prospective experiment | Source-bound v2 manifest and `13cc99b` implementation | Verify source snapshot and manifest identity against actual outputs |
| All production cases | Running process and case receipts, no terminal success yet | Require exactly 19,968 validated receipts and terminal completion |
| Stored states and replay | Pilot 80/80 audited and replayed | Stream every production state through audit; replay first compiled case per cell (80) |
| Ecological summaries | Summary implementation and synthetic tests | Complete source-backed JSON/CSV; all cells, denominators, precision and non-support retained |
| Scientific figures | Existing per-cell SVG/PDF/PNG exporter with synthetic QA | Render actual complete data, inspect readable ecological comparison figures and consistent units/scales |
| Scientific interpretation | Questions, endpoints and claim boundaries above | Write results/discussion grounded in full audited production and numerical gates |
| Reproducibility and GitHub | Verified implementation committed locally | Preserve immutable source/runtime, compact results and provenance; path-specific commit/push, verify remote HEAD and CI; do not claim local raw arrays were deposited |
| Entire goal | Unproven while production/reporting remain | Revisit every row with direct evidence before marking complete |

Terminal audit command (only after production completion):

```powershell
python -m scripts.model3_island.audit --design data/design/model3_island_v2.json --results data/results/model3_island_v2 --output data/results/model3_island_v2_audit.json --mode production --replay-per-cell
```

Complete summary and per-cell figure command:

```powershell
python -m scripts.model3_island.summarize --design data/design/model3_island_v2.json --results data/results/model3_island_v2 --output data/results/model3_island_v2_summary --mode production
```

These commands are required work, not evidence of completion until their actual
outputs have been inspected. Never restart the currently valid production merely
because a monitoring interval expires.
