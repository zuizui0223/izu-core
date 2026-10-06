# Model 3 birth diffusion and common-environment memory — 2026-10-04

## Question and relation to Chapter 2

Does reproductive mutation remove genetic arrest, and does it erase differences caused by earlier pollinator environments? This independently specified diagnostic extends Chapter2's generative ecology-to-selection-to-realization logic. Chapter1 supplied no fitted parameters or success target. The study isolates one evolving floral-investment locus, holding access and assurance fixed; it does not establish joint syndrome equilibria or explain observed floral colours.

## What was actually implemented

The finite ABM retains Mendelian gamete sampling and the original per-transmitted-allele mutation: Bernoulli probability u followed by a reflected normal jump of width sigma. The exact density counterpart uses the identical mutation kernel `(1-u)I+u*H(sigma^2/2)` on gametes before offspring formation.

An optional density approximation uses `H(u*sigma^2/2)`, the no-flux heat PDE semigroup. The coefficient is per allele at birth; it is not applied to adult phenotypes. Sexual inheritance remains an integral/difference operator. This is an actual mutation PDE coupled to sexual reproduction, not a pure continuous-time PDE replacing the full model.

The original node-projected heat kernel failed at coarse resolution: rare, narrow mutation is rounded away. A conservative finite-volume heat solver was added after preserving that failure. It preserves probability and the stationary constant density, is positive to numerical tolerance, and passes spectral convergence and semigroup tests. The default biological jump scheme and its RNG draws are unchanged.

## Declared experiment

-200 reproductive periods with center4 visitors versus no visitors; followed by800periods in the identical center4 environment.
-Identical founder genotype proportions(.4/.4,.4/.6,.6/.6), fixed access=.5, fixed assurance=.5.
-Mutation probability0 or.01, jump width.05. These are synthetic diagnostics, not natural rate estimates.
-ABM capacities48/192 and seeds6101–6108:64trajectories.
-Density11/21/41allele nodes, exact jump and point-heat schemes:24trajectories. Finite-volume correction:12additional trajectories.
-All declared trajectories completed and were archived.8paired repeats are a diagnostic, not a power analysis or a rare-attractor test.

## Numerical findings

For positive mutation,21-to41-node terminal mean differences were:

| Past environment | Exact jump | Finite-volume heat | Point-projected heat |
|---|---:|---:|---:|
| Visitors present |0.000079|0.001491|0.252087|
| Visitors absent |0.000442|0.004133|0.227053|

Exact and finite-volume schemes passed the declared.005refinement diagnostic. The point-projected heat scheme failed and is not used for biological inference. A two-grid difference below tolerance is a diagnostic, not a rigorous continuum error bound.

At41nodes, heat-versus-exact terminal differences were.002599and.007607. Thus the declared.005exact-versus-approximation gate failed for the absent-past condition. The diffusion is a useful nearby model, not a universally validated replacement for finite-jump mutation. No parameter was changed to force equivalence.

## Ecological result: mutation permits recovery but does not erase history within the observed period

After800periods of the same current environment, the mean investment gap between past-present and past-absent groups was:

| Capacity | Mutation probability | ABM mean gap | Descriptive paired bootstrap95% interval |
|---|---:|---:|---:|
|48|0|0.175|0.125–0.200|
|48|.01|0.173|0.119–0.225|
|192|0|0.200|0.200–0.200|
|192|.01|0.112|0.053–0.181|

All64ABM trajectories were occupied at the end. The zero-width interval in one row reflects identical outcomes among only8repeats, not population-level certainty. Intervals are exploratory with no multiplicity correction; raw paired outcomes are retained.

Without mutation, every terminal ABM population retained one investment allele and the last100period mean change was zero. With mutation, the average number of alleles was6.5–7.75at capacity48and30.625–32.125at capacity192. Mean investment increased beyond the original.6upper allele support. The formerly visitor-absent group still lagged the formerly visitor-present group after the shared environment.

Both positive-mutation groups were still changing, especially at capacity192(last100period increases approximately.022and.026). A surviving gap is finite-horizon historical memory, not proof of irreversible evolution, bistability or alternative stable endpoints. No claim that mutation significantly changed memory magnitude is made from these point estimates alone.

## Why deterministic and finite populations differ here

The exact density model's history gap after800common periods was approximately0without mutation and.002991with mutation. At the environmental switch in the zero-mutation absent-past case, density retained approximately2.12e-7copies of the.6allele at total population mass48. That fractional reservoir can recover deterministically; finite ABM populations had lost alternative alleles. The two descriptions therefore differ in genetic accessibility as well as demographic sampling and pollen self-exclusion. This diagnostic does not assign causal percentages among those processes.

The comparison does not imply the PDE is superior. It shows how a continuous description can retain extremely rare variants that a finite population no longer possesses, and how birth mutation can restore variation without immediate convergence in realized trajectories.

## Ch2 conclusion and claim limits

A common current pollinator environment need not immediately erase floral differences generated by past conditions. Finite loss of variants can arrest the response; mutation restarts evolution but did not eliminate historical differences within800shared periods in this diagnostic. This adds a concrete candidate mechanism for differences in realized floral investment, independent of Chapter1 fitting.

The model remains synthetic, with fixed inbreeding depression and fixed assurance. The new experiment does not estimate island geological time, natural mutation rates, the prevalence of past visitor absence, joint selfing/display attractors, or observed regional causes.

## Reproduction and archive

-Initial executed source commit:877f213; all88originalcases include exact source fingerprints in the archive manifest.
-Conservative PDE continuation: scripts/run_model3_mutation_memory_heat_fv.py, with a separate pre-execution numerical addendum and manifest.
-Summary: scripts/summarize_model3_mutation_memory.py.
-Raw archive: data/results/model3_mutation_memory_20261004.zip (all100cases and both manifests).
-Summary/effect sizes/precision failures: data/results/model3_mutation_memory_20261004.json.
-118targeted tests passed before independent review; full repository CI has not run.

Review: independent review found no blocker for the100executed cases and verified every raw-case checksum. The grid acceptance concerns terminal means only; it does not establish convergence of the full transient trajectories or distributions. The summarizer now includes any81-node continuation instead of silently omitting it. All present gates are computed from results. Runner hashes cover focal files; reproduce from the pinned Git commits as well, because helper/configuration dependency coverage is not exhaustive. No raw failure was discarded.
