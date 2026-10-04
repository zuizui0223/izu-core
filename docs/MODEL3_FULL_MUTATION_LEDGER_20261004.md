# Full mutation campaign execution ledger

Plan: `docs/superpowers/plans/2026-10-04-model3-full-mutation.md`.
Execution counts and shared-founder refinement: its `-execution.md` addendum.

## Completed implementation checks

- Sparse/tensor inheritance preserves the full joint genotype distribution.
  Twelve operator comparisons against the original dense implementation passed
  at absolute tolerance 1e-10 across both selfing timings, mutation on/off,
  and the three mutation operators. This is an algebraic implementation check,
  not evidence that diffusion approximates jump mutation.
- Campaign tests check the common visitor continuation after period 200,
  absence of plant immigration, declared case counts, retention of stage 1
  within stage 2, corruption rejection, and summary direction/allele columns.
- The initial 1,024 core cases completed. The declared precision gate passed
  in only 2 of 8 setting/rate/endpoint groups; each group requires both focal
  traits. Therefore the fixed 64-history, 8-repeat maximum was launched.
- The 128 projected-founder ABM controls completed. These four histories
  support a matched numerical comparison, not population-level precision.

## Final execution evidence

- All 4,096 core cases completed; all prespecified precision groups passed
  at the fixed maximum. No further seeds or parameter changes were used.
- All 144 density cases completed. Positive-mutation refinement failed in
  all 16 jump conditions and 8 of 16 heat conditions. Zero-mutation cases
  all passed. Quantitative positive-mutation bridge claims remain withheld.
- Matched ABM/density/heat contrasts are retained with explicit limitations.
- Final verifier accepted all 4,368 cases and 25 source files, including
  declared task identities, hashes, population traces and saved checkpoints.
- Full interpretation is in `MODEL3_FULL_MUTATION_RESULTS_20261004.md`.
  Raw archive and compact summary are prepared separately; see that report.

## Provenance ruling

Source fingerprints and a source archive were captured before execution.
Runtime package versions were recorded during execution, not before launch,
in `runtime_observed.json`; do not describe them as a pre-execution snapshot.
The documented commands explicitly limited BLAS/OpenMP threads to one.
The summarizer is outside the simulation snapshot and has been extended to
report allele retention, change from founders, last-100-period change, and
matched benchmark contrasts. Archive its final version with the results.

## Interpretation boundaries

The three traits evolve jointly. Capacity is 48 in this campaign, so it adds
no capacity-scaling evidence. Time is in uncalibrated reproductive periods.
Survivor-conditioned trait differences are distinct from persistence.
Finite-horizon memory is distinct from alternative stable endpoints.
Terminal mean grid agreement is not full-distribution convergence.
The continuous-genotype integral formulation and mutation PDE component
remain representations of the deterministic branch of Model 3.

Evolution Letters is a target for communicating a substantive evolutionary
prediction, not an acceptance rule for results. No settings, seeds or
precision thresholds are changed to obtain a stronger story.

## Independent implementation review

Read-only review found no evident engine defect. Two postprocessing findings
were repaired: summary readers now check declared task identity as well as
archive hashes, and grid summaries retain both 5-to-7 and 7-to-9 differences.
A mislabeled-but-hash-valid receipt regression failed before the repair and
passed afterward. The final signed three-way comparison is also tested.

The frozen runner does not verify an existing source ZIP on resume. Its
25 archived members were therefore verified externally against the source
manifest, including exact member names. The final campaign verifier repeats
that check. Do not edit the active simulation source merely to fix a future
resume safeguard; retain the original snapshot for this campaign.

Conditioning: arm means describe each arm's occupied replicates. Paired
effects describe jointly occupied replicates averaged within history and
then equally across histories. They are not generally the difference of
the marginal arm means when survival differs. All are descriptive.
