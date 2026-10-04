# Model 3: full mutation and common-environment validation

Status: all 4,368 declared cases completed and verified; final archival below.

## Question and design

Does isolation-generated evolutionary divergence persist after current visitor
environments become identical, when access, investment and assurance all evolve
and mutation can replenish variation? This extends earlier exploratory
one-locus diagnostics; it is not fitted to Chapter 1 and does not retrospectively
turn discovery analyses into prospective tests.

The initial 200 reproductive periods use near/far visitor immigration distances
0/3. The following 800 periods use the identical near visitor continuation.
Capacity is 48; founders and all other parameters are paired. There is no
plant immigration. Both delayed assurance with cost 0.5 and prior selfing
without that cost are tested, at mutation probability 0 and 0.01 (step SD 0.05).
These two settings jointly differ in timing and cost, so differences between
them do not isolate either mechanism separately.

The 1,024-case ABM stage failed its prespecified precision criterion, triggering
the fixed maximum of 64 histories x 8 demographic repeats x 2 settings x
2 mutation probabilities x 2 arms = 4,096 cases. An additional 128 ABM cases
use the projected founder support shared by the density benchmark.

The deterministic benchmark has 144 cases: four histories, both settings,
both arms, nested 5/7/9-node allele grids, original jump mutation and finite-volume
heat diffusion. At zero mutation the two mutation operators coincide and are
computed only once. All comparisons span the complete 1,000 periods.

## Ecological result: isolation history persists with three evolving traits

At the fixed maximum, all 16 focal precision comparisons passed (investment
and assurance at periods 200 and 1,000 for both settings and mutation rates).
Every interval halfwidth was <=0.025 and paired occupancy exceeded 90%.
These are descriptive 95% history-cluster bootstrap intervals, conditional
on paired survival, not multiplicity-adjusted confirmatory tests.

The following values are far-history minus near-history means after 800
periods of identical current visitor exposure (period 1,000):

| Assurance setting | Mutation probability | Investment difference [interval] | Assurance difference [interval] |
|---|---:|---|---|
| Delayed, cost 0.5 | 0 | -0.140408 [-0.163199, -0.116689] | 0.034050 [0.023049, 0.045382] |
| Delayed, cost 0.5 | 0.01 | -0.130106 [-0.148616, -0.111630] | 0.055755 [0.045287, 0.066346] |
| Prior, cost 0 | 0 | -0.030532 [-0.042927, -0.017704] | 0.003515 [-0.002117, 0.009197] |
| Prior, cost 0 | 0.01 | -0.016545 [-0.027210, -0.006708] | 0.001444 [0.000040, 0.002846] |

In the focal positive-mutation delayed-assurance setting, the differences at
the end of isolation were -0.194508 for investment and +0.072630 for assurance.
Both endpoint contrasts remained after environmental equalization, although
their point estimates were smaller. This is not a test of the difference
between time-specific contrasts, nor evidence that mutation caused a
statistically established attenuation relative to zero mutation.

Terminal access-position intervals included zero in all four setting/rate
groups. This abstract matching coordinate should not be labeled open versus
tubular flowers or a measured floral colour.

Only one core population became extinct: a near-history, zero-mutation,
delayed-assurance replicate. Its paired terminal occupancy is 511/512; all
other groups have 512/512 paired occupancy. Thus these parameter settings
provide little information about an extinction boundary.

Without mutation, occupied populations retained one investment allele and
their last-100-period mean investment change was zero. With mutation, mean
investment allele counts were about 6.63/6.44 (near/far) for delayed assurance
and 5.43/5.38 for prior assurance. Positive-mutation trajectories were still
changing: delayed near/far last-100-period investment changes were
-0.009166/+0.001721, and prior changes were -0.011508/-0.011966. The shared
visitor environment also remains temporally variable. No equilibrium,
irreversibility or alternative-attractor claim follows from these endpoints.

## Numerical result: positive-mutation three-locus fidelity is unresolved

The finest declared refinement compares 7 to 9 allele nodes, requiring the
maximum absolute terminal mean difference across the three traits to be <0.01.
Both 5-to-7 and 7-to-9 sensitivities over the full trajectory are also retained.

| Mutation operator | Mutation probability | Passing conditions | Largest terminal refinement difference |
|---|---:|---:|---:|
| Original jump | 0 | 16/16 | approximately zero |
| Original jump | 0.01 | 0/16 | 0.341635 |
| Finite-volume heat | 0.01 | 8/16 | 0.402644 |

Thus the positive-mutation deterministic reference is not resolved on these
grids. The jump-versus-heat differences at nine nodes are recorded but cannot
be interpreted as isolated diffusion-approximation error. Likewise, positive-
mutation ABM-versus-density differences are not validated estimates of finite-
population departure from the continuous-genotype model. Failure of this gate
does not prove that the PDE limit fails mathematically: discretization and
approximation error have not been adequately separated.

Zero mutation is a more limited comparison: the common five-node founder
alleles remain on that support. Grid agreement there checks numerical
representation of the same discrete allelic support, not a general continuum
convergence theorem.

## Meaning of the three comparisons

The signed contrasts obey ABM-heat = (ABM-jump) + (jump-heat). This arithmetic
decomposition is not a causal attribution. The finite and deterministic
branches also differ in individual pollen self-exclusion, stochastic
recruitment/segregation and nonlinear density regulation. Causal percentages
for drift, self-exclusion or regulation are not estimated here.

The PDE is a reflecting diffusion of transmitted alleles coupled to sexual
inheritance. It does not replace the full model with an autonomous phenotype
PDE, and it is not a separate fourth ecological model.

## Interpretation rules

Selection thresholds from the earlier corrected invasion analysis remain
local model-conditional statements. Realized evolutionary changes are not
automatically equal to those local gradients. Persistence, history contrasts,
allele retention and late-period changes are reported separately. An endpoint
gap after 800 shared periods is historical memory over that horizon, not
irreversibility or two stable attractors.

The joint bootstrapped effects condition on both arms being occupied and weight
histories equally. Marginal arm summaries instead use the occupied replicates
of each arm. Adaptive precision intervals are descriptive. Four benchmark
histories are a bounded computational comparison, not natural-island prevalence.

## Chapter 2 conclusion

The model derives local syndrome-direction selection from reproductive costs
and returns rather than specifying an island optimum. The new full ABM
experiment shows that isolation-generated differences in investment and
assurance can persist after current visitor conditions are equalized, even
with mutation and joint trait evolution. Their magnitude depends on the
declared reproductive setting. This is a mechanistic possibility independent
of fitting Chapter 1, not an explanation established for its four regions.

The positive-mutation three-way continuous-model bridge remains numerically
unresolved at the declared grid budget. Consequently, the current campaign
does not establish that its ABM memory is larger than a converged deterministic
or PDE prediction. The previously completed one-locus memory diagnostic is
separate evidence and is not silently promoted to this full model.

This completes the declared bounded validation campaign, including its
negative numerical result. It does not establish a publication-ready,
quantitatively interchangeable positive-mutation continuum replacement.

## Reproduction and archive

- Compact repository result: `data/results/model3_full_mutation_20261004.json`
  (298,382 bytes), including core, density and three-way summaries, source
  fingerprints, runtime versions and raw-archive identity.
- Raw local archive: `outputs/model3_full_mutation_20261004_raw.zip`
  (224,236,731 bytes), SHA256
  `4647eb772303f0b53387227f052bae6ce0aff84d1b056ab3cdf6f71348917c48`.
  It contains all 4,368 trajectories and receipts, both source snapshots
  (simulation and final postprocessing), stage summaries and verification.
  Every archived trajectory hash was rechecked after ZIP creation.
- The raw archive is retained in the workspace; it is not a public permanent
  archive or an assertion that the complete raw package was pushed to GitHub.
- Run `python -m scripts.run_model3_full_mutation --mode core --histories 64
  --repeats 8 --workers 2 --out outputs/model3_full_mutation_20261004`, then
  the same runner with `--mode benchmark` and `--mode density --workers 4`.
  Set `OPENBLAS_NUM_THREADS=1`, `OMP_NUM_THREADS=1` and `PYTHONUTF8=1`.
  The plans retain the actual stage-1-to-stage-2 precision decision.
- Summarize with `scripts.summarize_model3_full_mutation` in modes core
  (64 histories, 8 repeats), benchmark, density and comparison; verify with
  `scripts.verify_model3_full_mutation --out outputs/model3_full_mutation_20261004`.
- Runtime metadata was collected during execution rather than before launch.
  The frozen runner's resume archive check is supplemented by the final
  verifier. Use the archived sources to reproduce these results.

Validation: 115 focused engine, campaign, summary and verifier tests passed.
Independent read-only review checked implementation and the final numerical
tables, including the failed continuum gate. This is not full repository CI.

The full ABM time-series figure can be regenerated with
`python -m scripts.plot_model3_full_mutation --source outputs/model3_full_mutation_20261004
--out outputs/model3_full_mutation_figures`. It uses all original time points,
64 history means per condition (8 paired replicates each), and the original
endpoint bootstrap intervals. Plotted endpoint means are checked against the
final summary. PNG, PDF, SVG and the history-mean arrays are written locally;
the rendered figure was inspected for labels, legend, phase boundary and
line meanings. No failed-grid continuum trajectories are presented as validated
curves in this figure.

## Novelty assessment

The focused [primary-source audit](MODEL3_MUTATION_HISTORY_NOVELTY_20261004.md)
finds prior work on variation loss, history-dependent trait responses and
failure to reverse selfing after pollinator restoration. Residual history
contrasts alone therefore do not establish novelty. A stronger contribution
would distinguish recovery across the three traits and identify which
processes generate it. Positive-mutation finite-versus-continuum attribution
remains withheld until the ongoing refinement resolves numerical accuracy.
