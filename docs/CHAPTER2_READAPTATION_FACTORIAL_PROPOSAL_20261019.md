# New-environment readaptation and repeatability: design proposal

**Superseded in scope and numerical design:** the user requested a central-
hypothesis-only experiment feasible on the local PC. Use
[the bounded local design](CHAPTER2_READAPTATION_LOCAL_DESIGN_20261019.md).
The expanded composition/cost variants below are historical proposals, not
active implementation requirements or execution authorization.

Status: **proposal for review; no new biological futures executed or registered**.
This document records the user's 2026-10-19 choice to compare visitation activity
separately from visitor composition/floral matching. It does not change the
completed [160 x 160 confirmation](CHAPTER2_CONFIRM160_RESULTS_20261019.md).

## Question and intended conclusion

After a population has experienced pollination restriction, which responses to
a new pollination environment recur: the direction of assurance A, investment I
and matching M change, the attained state, the timing, or persistence?
Separate environmental predictability from repeatability within an identical
starting state and environment. Do not assume A is deterministic or I stochastic.
Successful readaptation means improved performance in the destination under a
specified common assay context, not necessarily larger flowers or recovery of
the ancestral trait mean. A is assurance capacity, not realized selfing rate.

The immediate scope is a model experiment, not inference about natural island
assembly. Evolving deleterious load and obligate outcrossing remain outside the
present model. Neither this proposal nor the confirmation closes those claims.

## Alternatives and recommended structure

1. Change activity alone: clean but omits the user-selected matching question.
2. Change activity and matching together: plausible environmental scenarios but
   cannot separate their effects.
3. **Cross activity with visitor matching/composition**, using the same introduced
   cohort across destinations and nested stochastic repeats. This is the
   recommended structure; it estimates both environmental contrasts and their
   interaction while exposing residual variability.

Use the existing model's separate `Config.activity` and `VisitorState.optima`,
`breadths`, and `effectiveness` controls. `activity_mode="fixed"` avoids making
visitor richness automatically change the activity multiplier. It does not hold
realized visits, pollen export or pollen delivery constant: matching also enters
these processes in `scripts/model3_island/reproduction.py`.

The first factorial should manipulate activity and visitor optima while holding
visitor count, breadth and effectiveness fixed. This isolates matching. A
separate composition contrast should change the distribution of visitor optima
at fixed count and mean, rather than relabeling visitor IDs. Changing identities
without functional parameters has no effect in this model. Richness, breadth and
effectiveness treatments must be separately named if later included; none is a
substitute for visitor taxonomic identity.

Destination optima must be fixed in absolute trait space before inspecting future
outcomes, with a symmetric destination grid to avoid choosing a favorable shift.
Do not define each destination around the observed evolved M and then treat it
as a common external environment. Register the exact grid and activity levels
after checking model ranges and manipulation diagnostics, before futures.

## Donors, transfer and comparison units

Recommended primary transfer: a finite cohort of sexually produced viable
offspring from the donor population, not copied adult genotypes. Implement this
as a distinct source-production and founding step using audited parental weights
and the existing Mendelian inheritance kernel. Do not silently reuse local
density-limited recruitment as a dispersal model.

Freeze a donor census by calendar time, not by an observed closure event. Include
both prior fixed-A and evolving-A histories as history treatments; the primary
readaptation future should allow A evolution in both. Continuing fixed A in a
future would instead test a continuing intervention and must be labeled as such.
Retain donor-policy differences as a package of past selection and demography,
not a pure A-genotype effect.

Separate three random levels: donor history, founding cohort, and future
reproduction/recruitment. Copy the same realized founding cohort to every
destination; draw multiple independent future streams within each cohort and
destination. Pairing across destinations is a computational intervention and
must not be described as the same seeds naturally dispersing multiple times.
Record maternal/paternal ancestry and inherited alleles in the founding cohort.

All allocated donors remain in denominators. No viable propagules, donor
extinction and later recipient extinction are outcomes, not exclusions.
Report outcomes conditional on supplying a cohort separately. Within-cohort
repeatability is necessarily conditional on a cohort existing; no trait value
is imputed to an empty population.

## Measurements and separation of explanations

| Layer | Record | Interpretation |
|---|---|---|
| Manipulation | activity, functional visitor parameters, export, delivery, outcross/selfed seed output | Whether the intended environmental contrast changes pollen service |
| Evolution | A/I/M means, distributions, allele support and variance at fixed censuses | Heritable state change; not adaptation by itself |
| Repeatability | direction probabilities, endpoint dispersion and event-time distributions within each identical cohort/destination | Finite-process predictability at a stated horizon |
| Demography | founding success, occupancy, extinction time, reproductive output | Establishment and persistence, including failures |
| Performance | initial and evolved genotypes assayed in the same destination at standardized density/competition | Conditional performance change separated from density change |

Preserve a snapshot of every founding cohort for the common-context assay.
Use a shared, explicitly specified reference competitor/background and the same
focal abundance for initial and evolved samples. Account for maternal and
paternal outcross contribution and viable selfing consistently. Report the
assay estimand as conditional reproductive performance; whole-population seed
output, invasion fitness and persistence are different quantities.

Report the realized selfing fraction with its reproductive denominator, alongside
A. Retain strict and epsilon genetic-access diagnostics as support bounds;
these are not direct tests of realized readaptation.

For direction probabilities, report positive/zero/negative changes separately.
Any biologically meaningful deadband must be declared before outcome inspection;
numerical precision is not a biological SESOI. Timing analyses must include
right censoring and extinction as a competing event, rather than comparing only
pairs in which both events happened.

Do not rank A/I/M determinism by raw variance or raw event agreement alone:
trait scale, starting variance, event prevalence and target distance differ.
Report both raw distributions and explicitly defined comparable standardized
summaries. A high-probability endpoint can coexist with variable timing.
Use repeated futures to estimate within-context variability; the previous
160 x 160 experiment has no such within-cell repetition and cannot supply it.

## Inference, provenance and execution gates

The design contains crossed founder and visitor histories and nested cohorts
and future repeats. Nested repeats do not increase the independent source-axis
sample size. Separate source heterogeneity, environment contrasts and residual
future variation without equating all residual variation to genetic drift.

Before production, complete and freeze the following concrete contract:

- donor archive/source hashes, calendar census and donor selection rule;
- offspring-production/dispersal rule, cohort size, founding establishment rule,
  number of cohort draws, and handling of insufficient propagules;
- exact activity/optima/composition grid, no-change comparator and future horizon;
- future resource budget, A cost/timing and mutation/immigration settings;
- separate cost-free delayed-selfing block if included, never pooled implicitly
  with the current cost-.5 biological treatment;
- primary estimands, multiplicity family, crossed/nested uncertainty method,
  biologically justified effect threshold or an explicit estimation-only aim;
- numerical fixtures, expected precision under adverse variance, update/storage
  budget, unique random namespaces, archive contents and independent readback.

The existing 160 x 160 outcomes are known. Selecting donors from that archive
makes the next experiment conditional on this known source; it is not a fresh
confirmation of source-history effects. A fresh-source component would be needed
for that claim. Future streams must be new and disjoint from all existing runs.

No choice in this proposal authorizes post-outcome selection of destinations,
deadbands, favorable donors or analysis methods. No outcome of the new experiment
is asserted here. Missing execution-contract values are design decisions to
resolve, not placeholders accepted by a runnable configuration.

## Implementation boundary

Keep any new runner outside `scripts/model3_island/` to preserve historical
source-glob manifests. Reuse the existing biological functions without changing
their frozen source. Add explicit tests for parental orientation, diploid
inheritance, destination pairing, RNG separation, empty-donor accounting,
functional visitor controls and all-start denominators before production.

This proposal is the architectural design stage. A numerical execution contract,
implementation plan, independent review and preflight are still required. There
is no launch workflow or production command in this proposal.
