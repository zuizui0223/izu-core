# Model 3 Island Ecology Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for native execution, or superpowers:subagent-driven-development if the user selects delegation. Steps use checkbox (`- [ ]`) syntax for tracking. This document is a plan, not a record of completed implementation.

**Goal:** Explain floral investment change, persistence and recovery across repeated islands by separating assurance, effective pollination and finite-population processes.

**Architecture:** Three sequential work packages: A audits the existing attenuation result; B adds shared-state reproductive assays and explicit island histories; C adds inherited assurance, mutation, paired density comparisons and prospective campaigns. New modules live under `scripts/model3_island/`; archived `scripts/model3_*.py` remain unchanged. Each package has its own acceptance gate before the next scientific campaign.

**Tech Stack:** Python >=3.10, NumPy >=1.24, SciPy >=1.10, pytest >=8.0; existing project optional development dependencies. Standard-library dataclasses, JSON, CSV, gzip and hashlib for records. No new service or framework.

**Spec:** `docs/MODEL3_ECOLOGICAL_COMPARISON_CONTRACT_20260926.md`, read together with `docs/MODEL3_ISLAND_ECOLOGY_REDESIGN_20260926.md` and `docs/MODEL3_NEAREST_PRECEDENTS_20260926.md`.

## Global constraints

- Baseline: commit `4c4347e148197b43ddbb231931cd733b5f79f720`; preserve archived code/data bytes and unrelated work.
- Q1 is motivation only. No regional fitting, regional S/C/I assignment or target rank ordering.
- Units are reproductive years. Overlapping-generation duration comes from parent ages, not a relabeling of years.
- Extinct traits are undefined; occupancy and conditional trait estimates retain all denominators.
- Current counterpart is a discrete genotype-density model, not a PDE or an exact stochastic trajectory mean.
- Fixed depression does not establish purging, load evolution or heterosis; fixed assurance does not establish selfing evolution.
- Work-package tests use synthetic fixtures. Their values are not calibrated island parameters.
- Production values, seeds, error tolerances and horizons require a signed/hash-frozen manifest before production; no desired sign is an acceptance gate.
- Implement native or delegated only after the user reviews this plan and selects execution. No production run is authorized by test success alone.

## Review focus

1. Tiny populations: one genotype can represent different individuals; exclude individual self pollen, not genotype-class mating (Task 2).
2. All trajectories extinct: report occupancy zero and trait estimate undefined, never silently drop the cell (Task 9).
3. Immigration with no residents: permit recolonization but do not define a resident-genotype immigrant control from an empty distribution (Tasks 5, 6).
4. Saturated recruitment: expected capped Poisson births differ from capped expected births (Task 1).
5. Long recovery with no new alleles: lost variation cannot be restored by visitor return alone; distinguish immigration from mutation and lineage replacement (Tasks 6, 9).

## Execution and evidence conventions

Run from the existing `work/simulation-review` checkout after checking attached-worktree status, current branch and unrelated files. Before modifying code, record baseline hashes for archived runners and result manifests in a new package-specific receipt. Never stage the entire tree.

Each task follows the listed red/green cycle. The per-task command is `python -m pytest tests/<file> -q --basetemp=.model3-island-tests/<task>`. First run must fail because the planned implementation is absent; after implementation require all tests to pass. Use fresh task-specific temp paths. Commit only the new module/test paths belonging to that task after review; proposed commit messages appear below. Existing regression suites run once after integrated changes, then again only after relevant fixes.

Shared types are explicitly defined in Task 3; earlier diagnostics use NumPy arrays and plain scalar arguments and remain usable independently. All functions reject nonfinite inputs and invalid dimensions rather than repairing them silently. The endpoint runner uses the Task 3 stream IDs without task-dependent reseeding.

## Package A: explain the existing finite/density difference

### Task 1: conditional recruitment expectation

**Files:** create `scripts/model3_island/__init__.py`, `scripts/model3_island/expectation.py`, `tests/test_model3_island_expectation.py`.

**Interfaces:** `capped_poisson_mean(rate: float, vacancies: int) -> float`; `expected_recruits(n: int, survival: float, capacity: int, rate: float) -> float`. Use stable SciPy CDF/survival functions and a binomial-weighted sum over survivor counts. Formula and independence conditions are in comparison-contract section 3.

- [ ] Write tests: rate=0 or vacancies=0 gives 0; rate=1,vacancies=1 gives `1-exp(-1)` within 1e-12; n=1,survival=0,capacity=1,rate=1 gives the same result; survival=1,n=capacity gives 0. Reject capacity<n and noninteger counts. Enumerate small n in {0,1,2,3} and verify the contract formula; test a large rate without overflow.
- [ ] Run `python -m pytest tests/test_model3_island_expectation.py -q --basetemp=.model3-island-tests/t1`; require the expected missing-module failure.
- [ ] Implement the two scalar functions, preserving the archived reproduction-before-survival assumption. Do not call the result an expected conditional trait mean.
- [ ] Rerun the same command; require PASS and the concavity upper bound across fixed fixtures.
- [ ] Commit these three files: `feat: add finite recruitment expectation benchmark`.

### Task 2: pollen and genotype expectation audit

**Files:** create `scripts/model3_island/finite_audit.py`, `tests/test_model3_island_finite_audit.py`.

**Interfaces:** `aggregate_transfer(genotype: ndarray, visitors: ndarray, *, breadth: float, activity: float, budget: float, background: float) -> dict[str, ndarray]`; `expected_genotype_counts(genotype: ndarray, pairs: ndarray, *, survival: float, capacity: int) -> dict[str, ndarray]`. Return class genotypes, class counts, class-level transfer or next expected counts with explicit keys. Build class membership from exact genotype values; no tolerance-merging.

- [ ] Write fixtures with one plant, two identical plants, two distinct plants, zero visitors and three visitors. Compare class-summed transfer with archived individual pollen matrices at 1e-12; same-genotype cross-individual transfer must remain positive when visitors are effective. Verify removed pollen equals delivered plus documented loss.
- [ ] Run `python -m pytest tests/test_model3_island_finite_audit.py -q --basetemp=.model3-island-tests/t2`; require expected failure.
- [ ] Implement finite class multiplicity correction, retaining the archived allocation denominator and discarded self dose. Derive offspring genotype probabilities by exact Mendelian enumeration and multiply by Task 1's expected recruits; add expected adult counts. For small states compare against enumerated parental/gamete outcomes.
- [ ] Rerun; require PASS, nonnegative counts and expected total<=capacity. No genotype-diagonal deletion. No iteration claim about an exact long-run mean.
- [ ] Commit module and tests: `feat: audit finite pollen and offspring expectations`.

**Package A gate:** produce a diagnostic receipt comparing archived replay, one-step counts and pollen exclusion. Existing endpoint attenuation remains combined evidence until this gate. This package can be reviewed and used without Packages B/C.

## Package B: ecology and diagnostic interventions

### Task 3: shared state, configuration and random-stream contract

**Files:** create `scripts/model3_island/types.py`, `scripts/model3_island/randomness.py`, `tests/test_model3_island_state.py`.

**Interfaces:** immutable `Config` carries explicit capacity, years, survival, annual ovule/pollen budgets, investment cost, pollen scale, depression, mutation rate/effect SD, assurance mode, arrival/establishment/kernel settings and event order version. No hidden biological defaults in a production manifest. `PlantState` contains `alleles` shaped N x 3 x 2 (access, investment, assurance), `allele_origin` of identical shape with founder/source IDs, individual IDs and birth years. `VisitorState` contains IDs, optima, breadths and effectiveness. `History` stores pre-reproduction visitor states and seed-arrival candidates for each year. `Ledger` is named per-year accounting. `stream(master: int, component: str, replicate: int) -> Generator` uses stable integer component IDs, never Python's salted hash.

- [ ] Test invalid units/shapes, duplicate IDs, traits outside [0,1], negative rates, unknown schema versions and a zero-length population. Assert changing the inheritance seed leaves visitor history unchanged.
- [ ] Run `python -m pytest tests/test_model3_island_state.py -q --basetemp=.model3-island-tests/t3`; require expected failure.
- [ ] Implement validated dataclasses and streams for founders, visitor arrivals/losses, seed arrivals/settlement, survival, parent sampling, segregation and mutation. Store each stream identity in receipts.
- [ ] Include per-allele mutation flags alongside ancestry, and explicit Config fields `assurance_timing` (delayed or prior), `pollen_discount` (nonnegative), `assurance_cost` (nonnegative), `activity_mode` (fixed or count_scaled), `reference_visitor_count` (positive). All are serialized; no inferred biological defaults.
- [ ] Rerun; require PASS and deterministic replay from serialized configuration.
- [ ] Commit new files: `feat: define island state and independent random streams`.

### Task 4: shared reproduction and fixed-state assays

**Files:** create `scripts/model3_island/reproduction.py`, `scripts/model3_island/assays.py`, `tests/test_model3_island_assays.py`.

**Interfaces:** `reproduce(state: PlantState, visitors: VisitorState, config: Config) -> Ledger`; `investment_assay(state, visitors, config, *, step: float) -> dict`. Ledger includes donor-recipient outcross expectations, raw/viable self offspring, ovules, exported/delivered/lost pollen and maternal/paternal contributions. Assay perturbs each focal individual's investment allele mean by admissible +/-step with central differences inside support, one-sided differences at boundaries, and labels the scheme.

- [ ] Test exact archived reproduction when assurance is fixed, breadth=.2, effectiveness=1 and legacy budgets are supplied. Test no visitors, assurance disabled, zero allocation cost and mismatched visitors. Assert input arrays are byte-identical after assays. Count both parental contributions, including self offspring, consistently.
- [ ] Run `python -m pytest tests/test_model3_island_assays.py -q --basetemp=.model3-island-tests/t4`; require expected failure.
- [ ] Implement variable visitor effectiveness in pollen delivery and explicit delayed assurance from the assurance coordinate or fixed treatment. Keep the archived allocation trade-off; no forced covariance. Report local outcross return and total viable return separately. Compare step=.001 with .0005 as numerical diagnostic, not ecological threshold.
- [ ] Define sensitivity operators explicitly: prior assurance self-fertilizes fraction a of ovules before outcrossing; delayed assurance acts on fraction a of remaining unfertilized ovules. Both apply fixed depression to selfed offspring. Optional pollen discount multiplies exported budget by exp(-pollen_discount*a); optional assurance maintenance cost multiplies ovule supply by exp(-assurance_cost*a*a). Zero coefficients recover the cost-free baseline; these phenomenological costs require source justification/range declaration before production. Increasing cost-free delayed assurance is not evidence of an emergent evolutionary optimum.
- [ ] Distinguish number of functional types from visitor abundance: `fixed` activity reproduces the archived mean-affinity model; `count_scaled` uses activity times visitor_count/reference_visitor_count, so richness can alter total service. Apply effectiveness after export as pollen delivery efficiency in [0,1], preserving explicit inefficiency loss. Add tests for zero efficiency, zero visitors and invariance/response to duplicated visitors under the two activity modes.
- [ ] Rerun; require PASS and correct pollen/ovule conservation. Do not require pollinator loss to reduce the gradient.
- [ ] Commit new files: `feat: add fixed-state floral return assays`.

### Task 5: island histories and controlled chronology

**Files:** create `scripts/model3_island/history.py`, `tests/test_model3_island_history.py`.

**Interfaces:** `make_history(config: Config, *, seed: int) -> History`; `permute_exposure(history: History, order: ndarray, recovery: History) -> History`; `reach_probability(distance: float, scale: float, kernel: str) -> float`. Admit declared exponential `exp(-d/scale)` and heavy-tail `(1+d/scale)^(-2)` candidates; neither is asserted calibrated. Seed and visitor rates have separate source supplies, reach and establishment probabilities. Draw Poisson arrival counts, Bernoulli establishment and visitor survival independently; visitor loss hazard uses `1-exp(-hazard*dt)`.

- [ ] Test d=0 gives reach=1, distance monotonicity, zero supply gives zero arrivals, multiple arrivals are supported, absent background resources reject autonomous visitor establishment unless resource dependence is configured. Test permutation preserves IDs/traits/exposure multiset and recovery suffix exactly.
- [ ] Run `python -m pytest tests/test_model3_island_history.py -q --basetemp=.model3-island-tests/t5`; require expected failure.
- [ ] Implement founding and separation initial-history modes explicitly. Founding starts focal plants absent or with declared arriving founders; separation starts a declared inherited state then changes connectivity. Record initialization source and event time. Expose background resource support; no whole-island coevolution claim.
- [ ] Rerun; require PASS and replay after population extinction. Do not force equal delivered pollen between histories, because evolved plant state changes it.
- [ ] Commit files: `feat: model separate island arrivals and exposure chronology`.

### Task 6: inheritance, mutation, recruitment and ancestry

**Files:** create `scripts/model3_island/population.py`, `tests/test_model3_island_population.py`.

**Interfaces:** `inherit(state: PlantState, mothers: ndarray, fathers: ndarray, config: Config, *, segregation_rng, mutation_rng, year: int) -> PlantState`; `advance(state, ledger, seed_candidates, config, streams, *, year: int) -> tuple[PlantState, dict]`.

New baseline event order: reproduce with current residents; adult survival; generate resident offspring; establish immigrant seed candidates; uniformly sample resident/immigrant recruit pool into vacancies; assign ages/IDs. With no immigration/mutation, map the operator to archived recruitment. No immigrants breed in their arrival year. This explicit immediate-recruit baseline excludes seed banks and juvenile delays; add them only as separately declared model classes.

- [ ] Test Mendelian probabilities by exact small-state support, zero mutation preserves parental alleles, mutation rate=1 alters draws under a nonzero SD fixture, ancestry follows transmitted alleles, and novel mutations retain genealogical origin plus a mutation flag. Ensure unique IDs and correct birth years.
- [ ] Run `python -m pytest tests/test_model3_island_population.py -q --basetemp=.model3-island-tests/t6`; require expected failure.
- [ ] Implement independent loci and per-gamete-allele mutation using reflected Gaussian steps on [0,1]; flag boundary rule as a sensitivity assumption. Delayed-assurance alleles express only in evolving mode. Use fixed depression, with no load/purging claims. Resident-genotype immigration controls are invalid for an empty state; return an explicit non-evaluable control status rather than fabricate founders.
- [ ] Rerun; require PASS, empty-island recolonization with source seeds, no spontaneous rescue with zero arrivals and zero mutation, and no capacity overflow. Record first extinction separately from later occupancy.
- [ ] Commit files: `feat: add island recruitment mutation and ancestry`.

**Package B gate:** reproduce legacy limits and validate chronology/assays before interpreting any new biological trajectory. The new event order and parameter units are versioned. No numerical production ranges are inferred from test fixtures.

## Package C: paired prediction, ecological campaigns and reporting

### Task 7: paired individual and distribution trajectories

**Files:** create `scripts/model3_island/density.py`, `scripts/model3_island/simulate.py`, `tests/test_model3_island_pairs.py`.

**Interfaces:** `density_step(counts: ndarray, grid: ndarray, visitors, immigrants, config) -> tuple[ndarray, Ledger]`; `simulate(config: Config, history: History, founders: PlantState, *, replicate: int) -> dict`. Exact sexual inheritance uses gamete frequencies and sparse/nonmaterialized pair operations rather than a cubic dense three-locus tensor. Mutation transition probabilities integrate the same reflected kernel over allele-bin cells; immigration uses the same source distribution/projection contract.

- [ ] Test normalized inheritance/mutation kernels, no-mutation identity, identical projected founders, and shared visitor paths. Reproduce archived two-locus density with fixed assurance and legacy configuration. Test a point mass at boundaries and absence of visitors.
- [ ] Run `python -m pytest tests/test_model3_island_pairs.py -q --basetemp=.model3-island-tests/t7`; require expected failure.
- [ ] Implement the declared deterministic recruitment closure and label it distinctly from Task 1. Record all yearly state and ledger outputs plus parent-age generation estimates. Density removes individual self-exclusion only in its declared infinite limit. A finite correction is admitted only for valid integer class counts; never extrapolate it to fractional individuals silently.
- [ ] Rerun; require PASS. Run outcome-blind resource benchmarks for grid sizes before promising long campaigns. Refinement uses common underlying founder draws and source measures, with projection differences recorded.
- [ ] Commit files: `feat: add matched island individual and density trajectories`.

### Task 8: prospective campaign compilation and receipts

**Files:** create `scripts/model3_island/design.py`, `scripts/model3_island/run.py`, `tests/test_model3_island_design.py`; later create `data/design/model3_island_v1.json` only after its scientific fields are fixed.

**Interfaces:** `compile_design(document: dict) -> list[dict]`; `validate_design(document: dict) -> None`; CLI `python -m scripts.model3_island.run --design PATH --output PATH --mode pilot|production`. Required fields: parameter units/ranges, event-order version, mechanism flags, factorial/counterfactual definitions, pilot/production/heldout seed lists, numerical tolerances, effect thresholds, time horizons, precision target, maximum runtime/memory, source hashes and claim exclusions.

- [ ] Test rejection of missing scientific fields, overlapping seed cohorts, kilometre labels without scale calibration, unsupported PDE label, repeated case IDs and output collisions. Compute planned case count exactly, including paired arms and within-history repeats.
- [ ] Run `python -m pytest tests/test_model3_island_design.py -q --basetemp=.model3-island-tests/t8`; require expected failure.
- [ ] Implement read-only manifest hashing, resumable case-level outputs with input/code hashes and an atomic completion receipt. Resume only matching immutable cases; never infer completion from file presence. Production refuses a pilot manifest or an unfrozen manifest.
- [ ] Rerun; require PASS and interrupted-run replay identical to uninterrupted run on tiny fixtures.
- [ ] Commit files: `feat: freeze and resume island experiments`.

Production design families must include: (a) fixed-capacity assurance/activity/mismatch assays; (b) chronology with common restored environment; (c) separate seed and visitor connectivity; (d) founding/separation bundled and matched-state controls; (e) assurance fixed/evolving, with declared discounting sensitivity; (f) mutation/immigration recovery; (g) capacity/grid scaling at fixed density, separately from island-area scaling; (h) lifespan with annual-effort and lifetime-effort controls; (i) crossed S/C with demographic replicates and held-out regime transport. No automatic full Cartesian product: compile each scientific contrast with its shared controls and explicit weights.

Replication follows declared Monte Carlo precision. For unconditional proportions use the conservative planning inequality R >= ceil(1.96^2/(4*h^2)); conditional traits and rare events require their own precision rules. Fix allowed batch sizes and maximum R before outcomes, use valid sequential intervals if stopping by precision, and report maximum-budget failures as imprecise. Pilot assesses runtime and numerical validity, not selects the most attractive effect.

### Task 9: ecological endpoints, S/C/I and figures

**Files:** create `scripts/model3_island/summarize.py`, `scripts/model3_island/plot.py`, `tests/test_model3_island_summary.py`.

**Interfaces:** `summarize(records: list[dict], design: dict) -> dict`; `decompose_crossed(values: ndarray, weights: dict) -> dict`, values indexed S x C x D; CLI `python -m scripts.model3_island.summarize --design PATH --results PATH --output PATH`. Outputs CSV/JSON plus SVG/PDF/PNG figures.

- [ ] Test all-extinct cells, asymmetric pair survival, immigrant replacement and signed-bias cancellation. Fixture with errors +1,-1 must yield zero signed bias and MAE=1. Additive crossed fixture has I=0; interaction-only checkerboard has positive I; within-cell noise is reported separately, not assigned to I.
- [ ] Run `python -m pytest tests/test_model3_island_summary.py -q --basetemp=.model3-island-tests/t9`; require expected failure.
- [ ] Implement occupancy and conditional trait reports with denominators, visitor recovery versus genetic recovery, ancestry composition, paired intervention uncertainty clustered at independent history level, and held-out prediction errors. Use balanced cell means for descriptive S/C/I and report noise/finite-repeat bias; do not call these latent variance shares without a separately validated estimator. Reject causal ranking comparisons with differing factor weights or unsupported survivor support.
- [ ] Add `effective_exposure(service: ndarray, weights: ndarray, correlation: ndarray) -> dict`: normalized nonnegative reproductive weights w give k_eff=1/(w.T @ correlation @ w) when a valid positive-semidefinite unit-diagonal stationary correlation estimate is supplied. Independent equal-weight exposures give k_eff=T; perfect correlation gives 1. Zero variance, insufficient observations, invalid covariance, nonpositive denominator or a nonstationary history returns an explicit non-evaluable reason. Negative correlations can produce k_eff>T and must not be clipped silently. Estimate service on a fixed reference genotype panel to avoid defining environmental correlation from evolved plant response; use replication uncertainty. This diagnostic is not the old pooling intervention or number of simulated islands.
- [ ] Rerun; require PASS and vector figures with axes/units/uncertainty visible. Inspect exported figures. Never title a panel 'optimum' from a terminal density value.
- [ ] Commit files: `feat: report ecological recovery and conditional response structure`.

### Task 10: integrated audit and scientific handoff

**Files:** create `docs/MODEL3_ISLAND_IMPLEMENTATION_AUDIT.md`; update only new-package documentation/receipts as warranted.

- [ ] Run all new tests: `python -m pytest tests/test_model3_island_*.py -q --basetemp=.model3-island-tests/integrated` (PowerShell: enumerate paths if wildcard expansion is unsupported).
- [ ] Run existing Model 3 regression tests using the explicit `tests/test_model3_*.py` path list; then the full project suite once. Record actual commands/counts/failures; do not copy old passing counts.
- [ ] Compare archived hashes and tracked diff against baseline; require no mutation of frozen runners or result bytes. Review every production claim against the manifest, operator and endpoint coverage.
- [ ] Run the tiny declared pilot only, inspect receipts and resource use, then finalize the production manifest with ecological scales and power/precision rationale before any production results. This is a separate scientific gate, not permission to choose parameters from promising pilot outcomes.
- [ ] Commit only reviewed new-package files and audit: `docs: audit island evolution implementation and production gate`.

## Coverage and handoff

Contract sections 1–2 map to Tasks 4/6/9; sections 3–5 to Tasks 1/2/7; section 6 to Tasks 5/6; section 7 to Tasks 3/7/8/9; section 8 to Tasks 8/10. Nearest-literature limits remain in the redesign document and must accompany reports. This plan does not claim that mutation, selfing evolution or history effects have already been implemented.

Recommended execution: native sequential implementation, first Package A, because its expectation and pollen audits constrain all later interpretations. Review that package before biological expansion. The user may choose delegated implementation instead. Both preserve all three packages and the independent Q1 boundary.
