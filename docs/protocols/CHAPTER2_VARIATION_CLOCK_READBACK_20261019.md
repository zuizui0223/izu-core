# Stored-genotype variation clocks: post-outcome read-only analysis

## Scope fixed before this readback

User request: determine when inherited variation in M, I and A disappears,
which value fixes, and how the historical assurance policy changes this process.
Read all 160 founder x 160 visitor crossings, both policies, prefix 0..35 and
both B8/B4.5 continuations 35..80. Remove duplicated fork census 35. No new
simulation, random draw, parameter adjustment or selected successful subset.
This is an exploratory analysis of previously observed data, not a new confirmation.

Use the 97 immutable-byte assets admitted by the original independent raw audit
at source f7792629b35b07e93ac9c98f8feb4d3894da85eb. Recheck every asset against
its committed hash inventory, every member read against its archive manifest,
and exact prefix/fork continuity. Analysis imports no simulator or producer.
Persist per-shard outputs and receipts so an interruption need not restart work.

## Quantities

For each occupied census count distinct allele VALUES separately at M/I/A.
Monomorphism means exactly one value among all living allele copies; identical
heterozygous individuals do not qualify. Exclude padded slots using saved counts.
Extinction is an absorbing, separate state, never monomorphism. First observed
monomorphism, its allele value, extinction census and final state are recorded.
No-event by census80 remains censored; do not assign it a fictional fixation date.
Record genotype-mean variance as a separate descriptive quantity: zero phenotype
variance can coexist with allele polymorphism. Fixed-A expression is .5 regardless
of latent alleles and does not measure genetic fixation.

Report all-start occupied-polymorphic, occupied-monomorphic, extinct, cumulative
monomorphism-before-extinction curves at each census; fixed-value distributions
and their relation to each original founder mean. Integrate occupied-polymorphic
censuses 0..79 (0..80 updates maximum). At B4.5 this occupancy/variation duration
mixes extinction and fixation and must not be interpreted as a pure fixation clock.
Record A/I order as both-events A-first/I-first/tied, A-only, I-only, neither;
never drop non-events to claim a universal sequence. M starts with many more
allele values than I/A, so raw between-trait clock rankings are not standardized.

## Policy comparison

Pair evolving minus fixed within each founder/visitor/budget. Two endpoints per
trait/budget: monomorphism-before-extinction by80 and occupied-polymorphic duration.
Report paired means, founder/visitor marginal ranges, descriptive pointwise95%
and Bonferroni family95% intervals for all12 endpoint/trait/budget comparisons.
Use the existing two-axis row/column/residual variance and t159 convention;
25,600 cells are not independent replicates, and this is post-outcome inference
without universal coverage or causal mediation identification. B8 is the main
no-extinction interpretation; B4.5 retains competing mortality explicitly.

## Seed-transfer distinction

Separately inspect all64 admitted readaptation seed cohorts against their32 donors
at census80. Record entry mean I, founder target attainment, per-locus donor and
cohort richness, and donor-polymorphic to cohort-monomorphic transitions. These
are nested descriptions of the fixed subset, not additional160x160 evidence.
No earlier-time continuation is authorized or executed by this analysis.

## Verification and delivery

Synthetic arrays only for tests: late fixation, extinction without fixation,
fixation then extinction, constant heterozygotes, padded zeros, fork duplication,
and independent crossed-array arithmetic. Review implementation before full readback;
independently check sampled raw states and aggregate results before manuscript claims.
Deliver source, tests, compact report and audit hashes via GitHub PR; retain detailed
readback as a release asset if unsuitable for ordinary Git. Preserve null/reversed
results and archive hashes; do not retune definitions after reading outcomes.
