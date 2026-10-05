# Supporting information: ecological process decomposition

This guide identifies the methods, complete results and numerical limits for the
current process manuscript. It supersedes the old bridge-only submission SI as
the entry point for this paper. The component documents retain separate cohorts
and frozen numerical evidence; they are not interchangeable replicates.

## S1. One biological model, distinct questions

Plants carry two alleles at each of three unlinked loci: matching position,
attraction investment and autonomous-selfing capacity. A phenotype is the
within-locus allele mean. Visitors have matching optima, breadths and functional
effectiveness. Continuing establishment and disappearance change pollen exposure.
In the primary gradient, successful new visitor types arrive at expected rate
lambda = 0.24 exp(-d) per reproductive update. This is neither visitation rate
nor a calibrated geographic distance. Plant capacity remains 48, and plant
immigration is absent. Individual-model finiteness is not island area.

For investment z and capacity a, the ovule budget is
O = O0 exp(-c_z z^2 - c_a a^2). Visitor matching and investment affect pollen
export and receipt; finite individuals exclude return of exported pollen to
themselves. Receipt gives a saturating outcross fertilization probability p.
Delayed selfing gives outcross output O p and viable selfed output
(1-delta) a O (1-p). Prior selfing gives O (1-a) p and (1-delta) a O.
Male contributions also enter parental success; maternal seed output alone is
not the full selection calculation. Delta is fixed depression, not evolving load.

ABM samples recruitment, parents, Mendelian inheritance and mutations. Genotype
density propagates the corresponding conditional population representation.
These are parallel calculations; density is not claimed to be the exact mean of
finite ABM. The primary annual-style treatment replaces generations each update,
but updates are not calibrated natural years. See
[implemented reproductive pathways](MODEL3_POLLEN_FITNESS_PATHWAYS_20261005.md)
and [model architecture](MODEL3_FINAL_ARCHITECTURE_20261004.md).

## S2. Selection conditions and reciprocal effects

[Joint thresholds and checks](MODEL3_PDE_CLOSEOUT_20261004.md) derive investment
and capacity conditions from rare-mutant contributions in a fixed resident.
All 900 finite-difference checks are retained. The
[13-rate local diagnostic](MODEL3_ISOLATION_SELECTION_GRADIENT_20261005.md)
includes 45 resident states, 64 histories and three snapshots. These gradients
are selection diagnostics, not realized velocities.

[Reciprocal selection](MODEL3_RECIPROCAL_SELECTION_20261005.md) and the
[independent parameter grid](MODEL3_PARAMETER_SELECTION_RESULTS_20261005.md)
retain all four joint sign regimes and the 25 positive capacity-to-investment
cross-effect exceptions. Parameter-grid counts are not natural frequencies.
[Sensitivity coverage](MODEL3_ASSUMPTION_SENSITIVITY_SCOPE_20261005.md)
distinguishes biological assumptions from replicate uncertainty and timing rules.

## S3. Sequence, magnitude and necessity

The [maintained-condition cohort](MODEL3_PERSISTENT_PROCESS_RESULTS_20261005.md)
and [complete replenishment extension](MODEL3_REPLENISHMENT_EVOLUTION_RESULTS_20261005.md)
report change from founders separately from additional divergence relative to
high supply. The extension contains 13 rates, two joint reproductive settings,
64 independent histories and eight nested demographic repeats: 13,312 cases,
of which 2,048 endpoint cases are reused. These are not 512 independent visitor
environments per condition. All 9,984 event records and 156 endpoint rows are
retained. Pointwise bootstrap intervals do not imply simultaneous coverage.

Change thresholds 0.025, 0.05 and 0.10 must be held for 20 updates; events within
five updates are near-simultaneous. Unreached events remain censored. Temporal
crossing is not infinitesimal onset. The extension is exploratory because its
endpoint results were already known when the intermediate-rate design was fixed.

The [capacity intervention](MODEL3_ASSURANCE_INTERVENTION_RESULTS_20261005.md)
contains 8,192 cases with capacity initially fixed at 0.5 without standing
capacity variation. It permits or prevents subsequent capacity evolution.
This tests necessity of capacity evolution, not absence of selfing, and cannot
be pooled with the standing-variation temporal cohort. Survivor denominators and
extinction remain explicit; extinct populations are not assigned zero traits.

## S4. Finite realization, variation and mutation approximation

The older zero-mutation bridge uses 128 histories, eight demographic repeats,
three starting states and 200 updates, with separate count-matching, visitor
pooling and population-capacity interventions. It does not substitute for the
three-trait positive-mutation gradient. Its interpretation and natural evidence
are retained in [complementary evidence](CHAPTER2_COMPLEMENTARY_EVIDENCE_20261005.md).

The [one-locus mutation diagnostic](MODEL3_MUTATION_MEMORY_20261004.md) uses
different histories for 200 updates followed by 800 common-environment updates.
It is supplementary. Genetic richness, trait variance and fitness are distinct;
there is no diversity bonus or evolving deleterious load in reproduction.

Mutation is exactly (1-u)I + u H(sigma^2/2) for the reflected Gaussian jump
operator, while the heat approximation is H(u sigma^2/2). Sexual reproduction
and inheritance remain integral/difference operations. Small-jump validity does
not follow from rare mutation alone. The restricted comparison retains its failed
tolerance; the full positive-mutation grid comparison failed 31 of 32 endpoint
gates. The [stop and alternative-evaluation record](MODEL3_LONG_COMPARISON_DECISION_20261005.md)
closes the stopped high-resolution run unresolved. No incomplete trajectory is
used as ecological evidence, and this paper does not claim full-model PDE validation.

## S5. Pollen limitation versus viable reproduction

[Supplementation assays](MODEL3_POLLEN_ASSAY_RESULTS_20261005.md) retain 12,288
evolved snapshots, while [whole-population trait manipulations](MODEL3_TRAIT_POLLEN_RESULTS_20261005.md)
retain 6,912 cases. Both keep fractional pollen deficits distinct from absolute
viable offspring output. Lower investment can reduce output even when the
fractional deficit declines. The [fixed-plant return decomposition](MODEL3_FIXEDPLANT_RETURNS_RESULTS_20261005.md)
uses the same plants in contrasting visitor environments and separates outcross,
selfed and total contribution derivatives. Those finite-plant derivatives are
not relabelled rare-mutant log-fitness gradients.

## S6. Figure and source reproduction

The review ZIP includes all four main plotting scripts, their required numerical
inputs, companion PDFs and tables. `verify_chapter2_process_review.py` verifies
member hashes, extracts to a fresh directory, redraws all four main figures and
checks numerical equality. This is figure reproduction from completed results,
not an independent implementation of biology. The separate 13-rate raw archive
is identified by `data/results/model3_replenishment_archive_20261005.json`.
No public data deposition is claimed.

[Q1 correspondence](MODEL3_Q1_MECHANISM_MAP_20261005.md) retains independent
motivation: no flower colour, accessibility or regional pattern is fitted, and
the pollen-deficit assay is not the empirical Q1 effect-size definition.
