# Model 3 island ecology: implementation and prospective campaign audit

2026-09-26. Status: implementation verification and resource pilot; no production
scientific outcome is asserted by this document. The active goal additionally
requires production, every-case validation, figures, interpretation and final
coverage review. Frozen baseline: `4c4347e148197b43ddbb231931cd733b5f79f720`.

## Ecological estimands

The question is when pollinator history changes floral investment and persistence,
whether autonomous assurance changes that response, and whether recovery of
visitors is sufficient to restore demographic and genetic states. The individual
versus density comparison is supporting evidence, not the ecological endpoint.
Q1 motivates questions but supplies no calibration or target regional response.

The nine explicit contrast families in `scripts/model3_island/campaign.py` cover
fixed-state reproductive assays; exposure-matched ordering and mismatch with a
common final environment; separate seed and visitor connectivity; founding and
inherited separation with matched-state controls; fixed versus inherited
assurance and discount/timing costs; visitor/immigrant/mutation recovery;
capacity and allele-grid comparisons; annual/lifetime reproductive allocation;
and crossed starting states, community histories and demographic repeats with
held-out-regime predictions. These are not a full factorial island universe.

## Implemented operator and checks

| Component | Evidence and interpretation |
|---|---|
| Recruitment expectation | Exact binomial/Poisson one-step cap expectation, not a nonlinear trajectory mean |
| Pollen self-exclusion | Individual diagonal discarded without redistribution; same-genotype different plants remain eligible |
| Inheritance | Three independent diploid loci, Mendelian segregation, reflected allele mutation |
| Assurance | Fixed or inherited capacity; prior/delayed timing, explicit viability depression and costs |
| Immigration | Separate arrival/establishment processes; source alleles and genealogical origin retained |
| Resident-genotype control | Genotype-matched immigrants keep external ancestry; undefined without residents and excluded from mechanistic conclusions |
| Island chronology | Repeated visitor identities and composition, permuted exposure order; seed timing held fixed |
| Time | Reproductive years; observed parental ages estimate generation interval |
| Density | Conditional discrete genotype-density closure with exact visitor-factorized inheritance, not PDE or stochastic expectation |
| Resolution | Grid-projected versus continuous-mutation individuals; explicit allele-grid refinement arms |
| Persistence | Extinction, recolonization, founder ancestry and survivor-selected trait support retained separately |
| S/C/I | Descriptive weighted cell-mean variation; within-cell stochastic variation and finite-repeat contamination remain explicit |
| Effective exposure | Fixed 21-plant reference panel; covariance diagnostic rejects nonstationarity and zero variance, never equated to old pooling k |

Capacity comparisons tile one underlying 48-plant genotype draw, giving matched
initial frequencies at 48/192/768 plants. Each copy has unique gene-copy ancestry.
Per-capita seed supply and fixed-total supply are different series. Mutations are
not rescaled with capacity or called an acceleration of natural evolution.

## Prospective numerical choices

Default duration is 200 reproductive years, with 400-year life-history contrasts
and 2,000-year mutation/recovery contrasts. These are model horizons, not fitted
geological ages. Survival 0, .75 and .9 produces nominal expected adult lifetimes
1, 4 and 10 years; realized parental ages are measured separately. Annual effort
and lifetime-matched effort have distinct controls.

Source/visitor reach distances are 0, 1 and 3 dispersal-scale units, never km.
Visitor arrivals are Poisson events and losses have annual hazard .05. Counts
represent visitor functional types, not observed abundances or a calibrated
species extinction rate. Background flora supports exogenous visitors.

Mutation probabilities 0, 0.0001 and 0.001 per inherited allele per reproductive
event, reflected effect SD .025, are declared sensitivity regimes. They are not
empirical mutation-rate estimates for a particular plant. Fixed depression .5
does not implement purging or evolving load. The only inherited traits are
abstract access/matching, investment and assurance; no colour or shape syndrome
is directly simulated. A fixed cost coefficient does not increase when visitors
decline. Low visitation need not lower marginal attraction benefits.

The revised production design specifies 80 cells, 128 independent histories
per main cell, two demographic/inheritance repeats, and 128 separate held-out
histories for each transport cell: 19,968 total cases, including assays. Assays
are not duplicated across demographic seeds. Half-width .125 is the prospective
unconditional occupancy precision target; 128 independent bounded history means
give a conservative 95% Hoeffding half-width about .120. Conditional trait
precision can fail and must be reported with eligible counts, not rescued by
extra outcome-selected replicates. No interim significance stopping is used.

Meaningful model differences are .05 investment, .10 occupancy and .10
heterozygosity. Numerical tolerances are .01 trait and .02 occupancy. These are
prospective operational thresholds, not empirically calibrated biological cutoffs.
Failure of refinement gates prevents a resolution-independent finite-population
claim; it does not invalidate a correctly labelled discrete model result.

## Verification observed so far

- Package-A tests and one archived 400-year replay matched 21 saved arrays exactly.
- Fourteen archived runner/provenance files remained byte-identical after audit.
- All 162 current new-package tests passed in the integrated-final XML receipt.
- The explicit Model 3 regression run passed 286 tests.
- The latest full project run passed 1,940 tests with 1 skip. Subsequent
  source-snapshot verification and stream-audit additions passed the 162-test
  integrated run; the final reviewer/fix gate retains a final full-suite check.
- Existing tests reformatted two unrelated result JSONs. These formatting-only
  side effects were restored; they are not part of this change.
- Synthetic figure QA checked readable units, extinction denominators, and
  SVG/PDF/PNG exports. Those fixtures are not biological results.

## Resource gate and storage ruling

The six-year pilot exercised all 73 cells twice (146 complete cases). A subsequent
disjoint full-horizon resource pilot completed all 73 cells once. Only execution
time and file sizes were inspected for design decisions, not the signs or sizes
of ecological outcomes. Full raw storage projected to about 35.4 GB, exceeding
the available local disk. The density genotype-frequency trajectory dominated.

All yearly individual states and yearly demographic, reproductive, trait and
genetic summaries remain stored. The large deterministic genotype-frequency
matrix is computed in full, committed by a dtype/shape/value SHA256 digest, and
saved at 100-year checkpoints plus start and end. Unsaved genotype frequencies
require replay from the frozen source/config/history seed and are verified
against the digest. This is a storage change, not a shorter simulation, rounded
result, removed treatment or discarded replicate. It costs replay time for future
genotype-level queries. Runtime versions and source snapshots accompany campaigns.

Repacking pilot arrays projected roughly 2.62 GB without changing any scientific
arm. Runtime projected to 7.47 hours before reduced compression work; this is not
a timing guarantee. Before production, the ceiling is set to 12 hours, 3 GiB
process memory, 4 GiB output, and at least 4 GiB free disk. Checks occur between
annual steps, so one step may transiently exceed a bound. A resource stop is an
incomplete campaign, never successful scientific evidence.

## Claim boundaries and remaining completion gates

Generic selfing rescue, priority effects and finite/infinite population differences
already have close precedents; see `MODEL3_NEAREST_PRECEDENTS_20260926.md`. Novelty
must come from a supported discriminating ecological mechanism and prediction.
No first-of-kind claim follows from code completion or the pilot.

The initial source-bound production manifest is `data/design/model3_island_v1.json`.
No production run has begun. If review requires code repairs, rebind the identical
scientific design to a new source-bound version before production.

Whole-branch review and repairs are complete. Pending: complete
production receipts, all-case validation, numerical/precision decisions, ecological
report and figures. No chosen S/C/I ordering, irreversible history effect, drift-only
cause, regional reproduction or deterministic optimum is an acceptance criterion.


## Independent review and pre-production repairs

A fresh read-only whole-branch review compared baseline 4c4347e with c8fcc43.
All five findings were accepted and repaired in one review pass before production:

1. Save actual child/mother/father IDs and retained selfed/outcross recruit counts,
   distinct from expected reproductive allocations. Audit their census membership
   and exact count consistency. These measure viable retained resident recruits,
   not all fertilizations or immigrant parentage.
2. Separate initial visitor RNG from future arrivals; matched founding/separation
   controls now share every subsequent visitor state and identity, not just year 0.
3. Add seven explicitly linked uninterrupted recovery counterfactuals with matched
   horizons, mutation settings, seed windows, initial states and numerical grids.
4. Make resident-matched density immigration depend on its own density composition,
   never sampled ABM genotypes. Flag empty-resident controls as undefined.
5. An initially empty island has no founder-lineage or initial-trait baseline.
   Occupancy, joint survivors and eligible trait-change pairs are separate counts;
   undefined changes cannot be counted as sign disagreements.

The five regression failures were observed before repair; a sixth test checks
corrupted parentage. The final package run passes 168 tests. The full review run
passes 1,948 tests with one skip; the final rerun after the missing-baseline sign
summary correction also passes 1,948 tests with one skip (1949 total). No review finding was downgraded or deferred.

The reviewer appropriately withheld scientific judgments until complete production,
numerical/precision checks and effect interpretation. Historical pilot manifests
precede the expanded schema and require their archived source snapshots; they are
not silently repaired or promoted to current production evidence.

Resource pilot v3 used independent history seed 71004 and one demographic seed in
all 80 cells at their full horizons. All 80 receipts and state audits passed, and
all 80 cases replayed exactly. Only runtime, size and structural validity were
inspected. The projection is 30,696 seconds (8.53 hours) and 4,693,172,352 bytes for
19,968 cases / 5,683,200 annual trajectory steps. Parentage and the seven controls
explain the increase over the earlier estimate. Current free disk was 126 GiB.
The output ceiling is prospectively raised to 8 GiB; the 12-hour runtime, 3-GiB
process-memory and 4-GiB free-disk limits stay unchanged. Scientific arms and
replication are not reduced. Pilot timing overlapped testing and is an estimate.

The superseding production manifest is data/design/model3_island_v2.json. The v1
candidate was never run and remains an immutable historical pre-review snapshot.
Production and scientific completion remain pending; code completion is not a
biological result.
