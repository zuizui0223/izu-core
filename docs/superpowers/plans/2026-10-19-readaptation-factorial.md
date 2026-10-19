# Factorial readaptation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Measure destination-dependent readaptation and within-cohort repeatability after standardized seed transfer, with independently auditable ancestry and all-start outcomes.

**Architecture:** Add an external experiment wrapper around unchanged Model3 biological functions. Separate donor admission, seed-cohort construction, destination futures, common-context assays and raw-only summaries. Archive the numerical contract and its hash before any production future.

**Tech Stack:** Existing Python 3.10+ / NumPy / pytest; JSON contracts and NPZ arrays; manual GitHub Actions only after a separately approved production contract.

**Spec:** `docs/CHAPTER2_READAPTATION_FACTORIAL_PROPOSAL_20261019.md`; structure approved by the user on 2026-10-19. Numerical choices below are proposed, not registered or executed.

## Global Constraints

- No changes under `scripts/model3_island/`, to original experiment manifests, or to original source commit `f7792629b35b07e93ac9c98f8feb4d3894da85eb`.
- Seed offspring, not adult genome copies; both historical policy groups have evolving A in the future.
- Pair identical realized cohorts across destinations and future A-cost treatments.
- Crossed donor axes, nested cohorts and futures are not independent island replicates.
- New streams; no favorable-donor selection; extinct or seedless donors retained.
- Estimate probabilities and performance, not a preregistered hypothesis victory. No biological SESOI is invented from known results.
- All future outcomes remain unknown at contract freeze; no extension of repeats after seeing outcomes.

## Proposed numerical contract

Use eight founder indices and eight visitor indices `[0,20,40,60,80,100,120,140]`
from the admitted 160-axis ordering; this is a fixed systematic subset, not a
random sample of all 160 axes. No full-archive generalization is claimed. Admit
both historical policies at census 80 from budget B8. This asks about late
readaptation after the recorded restriction history; it does not estimate how
readaptation changes with the age of the donor population.

For each of the 128 donors, draw four founding cohorts. Compute the native
donor-policy reproductive ledger under its actual census-80 environment (zero
visitors) and native A cost .5. Draw viable source production
`S ~ Poisson(sum(outcross) + sum(self_viable))`; transfer `min(S,12)` viable
offspring. Sample parental pairs from the ledger and transmit diploid alleles
with the unchanged inheritance kernel. This is standardized capped propagule
transfer, not a model of dispersal distance or a natural dispersal rate.
All transferred viable offspring establish at the initial census; destination
establishment filtering is therefore outside this primary contrast. Subsequent
reproduction/recruitment and extinction are stochastic. Report this boundary.

Destinations use six functional visitors, breadth .2, effectiveness 1 and fixed
activity mode. Cross activity `[.25,1,4]` with four optima vectors:
six copies of .3, six copies of .5, six copies of .7, and
`[.3,.38,.46,.54,.62,.7]`. The first three isolate shifts in matching; the fourth
contrasts functional dispersion with the .5-centered vector at the same mean.
Visitor count is not taxonomic richness. Add one zero-visitor/no-change-service
comparator, yielding 13 destinations. Numeric activity is a model parameter,
not an empirically calibrated visits-per-flower rate.

Use future A costs `[.5,0]` as separate environments, delayed selfing, zero pollen
discount, inbreeding depression .5, K48, B8, adult survival 0, no mutation and no
further immigration. The cost-zero future starts from cost-.5 donor history;
it cannot establish how cost-free assurance originally evolved.

Run 64 independent future repeats per cohort/destination/cost for 80 updates;
save trait, demographic, reproduction and allele-support summaries at every
census, with full states/ancestry retained for independent audit. Evaluate common
assays at censuses 0,20,40,80. Empty populations have occupancy 0 and undefined
trait/performance values, never zero-valued traits.

Maximum allocation: 128 donors, 512 cohort draws, 851,968 future trajectories,
68,157,440 future updates, and 69,009,408 future census records. Failure does not
remove an allocation from the manifest. The upper count excludes a separately
budgeted validation replay and assay computations; preflight must count both.
This is a resource proposal, not an authorized production launch. Do not reduce
the grid or repeats after outcome inspection to fit a budget.

Read-only dtype inspection of an admitted raw NPZ gives 5,664 bytes per full
48-plant state (alleles, origins, mutation flags, IDs and birth years). The
proposed census allocation therefore has a 364.03 GiB state upper bound; full
three-column parentage adds 73.125 GiB, before telemetry, containers, assay
records and replay. These are uncompressed bounds, not measured archive size.
Preflight must establish a workable archive/streaming strategy and wall-clock
budget before production is considered. A revised prospective allocation is
permitted before outcomes exist, with a new contract and explicit precision
tradeoff; silent truncation of the running experiment is not.

With 64 independent repeats conditional on a cohort/environment, zero observed
failures has a one-sided exact 95% failure-probability upper bound
`1 - .05**(1/64)` (about 4.6%). This is pointwise, not simultaneous across the
many contexts; it cannot certify deterministic behavior. Nested cohorts cannot
be pooled to manufacture 256 repeats of the identical starting state.

## Estimands and inference

Primary reporting is estimation-only. For each cohort/destination/cost report
occupancy and positive/zero/negative A/I/M change at census 80, with absent traits
reported as a separate extinction outcome. Give exact pointwise binomial bounds
for each mutually exclusive indicator; label them pointwise, never a familywise
confirmation. Report raw endpoint distributions and elapsed-time distributions.
No direction deadband or event threshold is inferred from observed futures.

Summarize destination differences paired within the cohort and equally weighted
over the 128 admitted donors. Source-axis dispersion is descriptive for the
fixed subset. Do not attach superpopulation confidence intervals based on 851,968
independent observations. The full joint tables allow later explicitly labeled
exploration without altering the primary report.

Common-context assay: evaluate each focal diploid genotype separately with 47
identical reference competitors (M=I=A=.5 at both alleles) in the destination,
using its future cost and budget. Compute focal `.5*maternal_outcross +
.5*paternal_outcross + viable_self` from the full ledger. Average over the
population's diploids and subtract the founding cohort's assay mean. This is
conditional reproductive performance in a fixed competitor context, not an
invasion exponent or a universal adaptive optimum. Assay all-start occupancy
separately from performance conditional on survival; never hide the latter's
survivor selection.

## Review Focus

- Empty/low-output donor: keep allocated outcomes and preserve a valid empty state.
- Parent matrix orientation: rows are fathers, columns mothers; selfing is diagonal.
- Hidden A under historical fixed policy: produce donor seed with native expression, then allow inherited A expression in future.
- RNG reuse across cohorts/futures: identical cohorts across treatments but distinct future streams.
- Fixed activity does not fix realized pollen service; visitor ID renaming alone has no biological effect.

## Task 1: Contract admission and deterministic preflight

**Files:** create `scripts/readaptation_contract_20261019.py`, `tests/test_readaptation_contract_20261019.py`, and a proposed JSON contract in `docs/protocols/`.

**Interfaces:** `load_contract(path: Path) -> dict`; `preflight(contract: dict) -> dict`. No model transitions or outcome reads in preflight.

- [ ] Write failing tests for the exact allocation counts above, duplicate source IDs, unknown treatment values and false execution authorization.
- [ ] Run `python -m pytest tests/test_readaptation_contract_20261019.py -q`; verify the expected missing-module failure.
- [ ] Implement strict schema, source/asset SHA admission, canonical keys and SHA256-derived 128-bit stream seeds from namespace plus donor/cohort/treatment/repeat/stage. Reject collisions across the full manifest.
- [ ] Compute raw-array/archive/replay/assay budgets from actual dtypes; benchmark only synthetic technical fixtures before requesting a production budget.
- [ ] Rerun the test file; commit only contract/preflight and their tests. The candidate contract must keep `execution_authorized=false`.

## Task 2: Source offspring and destination pairing

**Files:** create `scripts/readaptation_transfer_20261019.py` and `tests/test_readaptation_transfer_20261019.py`.

**Interfaces:** `make_cohort(donor, donor_config, donor_visitors, streams, cohort_key) -> tuple[PlantState, dict]`; `destination_states(contract: dict) -> dict[str, VisitorState]`.

- [ ] Write failing tests for zero donor, zero production, fewer than 12 offspring, maternal/paternal orientation, Mendelian origin support and native fixed-A seed production.
- [ ] Run the test file and verify failure before implementation.
- [ ] Implement capped viable-offspring transfer with existing `reproduce` and `inherit`, recording source draw, pair probabilities, parents and ancestry; use explicit fresh time/ID namespaces on entry.
- [ ] Test exact cohort byte identity across all assigned destinations/costs and deterministic rerun with identical stream keys.
- [ ] Test the 13 destination definitions, equal visitor counts and means for the composition contrast, and invariance under visitor ID renaming.
- [ ] Run the test file to PASS and commit.

## Task 3: Futures, common-context assay and telemetry

**Files:** create `scripts/readaptation_futures_20261019.py`, `scripts/readaptation_assay_20261019.py` and corresponding `tests/test_readaptation_futures_20261019.py`, `tests/test_readaptation_assay_20261019.py`.

**Interfaces:** `run_future(cohort, config, visitors, stream_key, horizon: int) -> dict`; `assay_population(state, config, visitors) -> dict`.

- [ ] Write failing tests for no-immigration extinction absorption, fixed horizon, evolving A in both history groups, separate cost treatments, and no initial-state alteration.
- [ ] Write assay tests with hand-computable zero-visitor/self-only ledgers, paternal outcross contributions, fixed 47-competitor context, identical baseline/evolved state difference zero, and empty state undefined.
- [ ] Run tests and observe expected failure; implement wrappers using unchanged `advance`/`reproduce`, storing all required per-census arrays and checksums.
- [ ] Assert source modules' hashes are unchanged and technical replay matches byte-for-byte; run both test files to PASS and commit.

## Task 4: Raw-only summaries and independent admission

**Files:** create `scripts/audit_readaptation_raw_20261019.py` and `tests/test_readaptation_raw_20261019.py`.

**Interfaces:** `audit_archive(path: Path, contract: dict) -> dict`; no producer or model imports.

- [ ] Write failing fixtures for missing/duplicate allocations, tampered cohort hashes, source/offspring origin mismatch, missing extinction records and wrongly pooled repeated cohorts.
- [ ] Implement exact all-start counts, paired destination tables, pointwise probability bounds, trait/occupancy separation and assay arithmetic readback. Identify which biological operations require replay rather than raw arithmetic.
- [ ] Test the 64-repeat zero-failure bound against `1-.05**(1/64)` and interval labels; add a fixture where all endpoints agree but event times differ.
- [ ] Run `python -m pytest tests/test_readaptation_contract_20261019.py tests/test_readaptation_transfer_20261019.py tests/test_readaptation_futures_20261019.py tests/test_readaptation_assay_20261019.py tests/test_readaptation_raw_20261019.py -q` to PASS; commit and request independent review.

## Task 5: Production gate and paper integration

- [ ] Inspect preflight runtime/storage, technical replay and independent review; resolve findings before freeze.
- [ ] Publish the exact numerical/source contract and request explicit approval for its measured production budget. Structural approval is not production approval.
- [ ] Only after that approval, add a manual source-pinned workflow following the existing authorized-run admission pattern; independently audit workflow dispatch restrictions before launch.
- [ ] Execute once, retain partial failures and all allocated denominators, and audit every final asset before outcome interpretation.
- [ ] Integrate results and limitations into the existing paper through reviewed PRs. Report unsupported or unidentifiable claims; do not declare the entire central hypothesis proven by this conditional experiment.

## Self-review and handoff

All approved design layers map to Tasks 1-5. Numerical choices are explicit and
remain prospective proposals. The primary source subset and cost-change boundary
limit claims by design. No implementation or experiment has run under this plan.
Recommended execution method: native implementation in this thread, followed by
independent review; shared sequential interfaces make parallel implementation
unnecessary. Plan review precedes implementation; production remains a separate
gate after measured preflight.
