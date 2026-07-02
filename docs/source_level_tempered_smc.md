# Adaptive tempered SMC for source-level Izu comparisons

## Why replace the one-shot prior Monte Carlo integral

The earlier source-level marginal-compatibility runs produced importance ESS near
one or two for the leading candidates. In that situation, a single broad prior
draw can dominate the estimate. Increasing the number of draws alone may be
wasteful because most new prior draws again miss the narrow compatible region.

This implementation uses adaptive tempered sequential Monte Carlo (SMC):

```text
prior (beta = 0)
  -> likelihood-tempered intermediate targets
  -> full source-level likelihood (beta = 1)
```

At every transition, the next beta is chosen so the incremental importance ESS
meets a declared fraction of the particle count. Particles are systematically
resampled and then moved with a prior-independence Metropolis kernel.

## Why no profile-weighted shortcut

A profile optimizer can locate a high-likelihood parameter region, but drawing
only around that region without a fully specified proposal density would make a
marginal-likelihood comparison invalid. The SMC procedure instead keeps each
candidate's declared prior as the initial distribution. The independence move
proposes from that same prior, so the unknown analytic density of the existing
implicit priors cancels in the Metropolis ratio:

```text
acceptance ratio = likelihood(proposal)^beta / likelihood(current)^beta
```

Thus profile fits remain a separate diagnostic rather than a hidden proposal
that can alter a candidate's prior volume.

## Candidates and shared likelihood

The SMC comparison runs five candidates against the same source rows:

1. `environment_only`
2. `body_size_only`
3. `small_bee_substitution`
4. `ardens_bridge_loss`
5. `isolation_order`

The fifth candidate uses fixed `region_order` only as an ordinal proxy and does
not read pollinator availability fields. It is not a distance, colonization
history, or causal-isolation model.

All candidates use the same outcrossing, bagging, flower-length, and optional
guide-order likelihoods already defined for the direct source-level evidence.

## Reading diagnostics

A controlled incremental ESS is necessary, but not by itself sufficient, for a
reliable comparison. Report all of the following:

- replicated log-compatibility estimates across seeds;
- rank-one fraction and mean rank;
- number of tempering stages;
- minimum and mean incremental ESS;
- resample-move acceptance rate;
- agreement or disagreement with the separate profile optimizer;
- channel ablations and observation-scale sensitivity.

Do not interpret a small replicated difference as evidence for historical
causation. The SMC estimate remains conditional on the declared priors,
restricted candidates, and historical-summary likelihoods.

## Run

```bash
python scripts/run_source_level_tempered_smc.py \
  --particles 500 \
  --target-ess-fraction 0.70 \
  --rejuvenation-steps 1 \
  --seeds 20260702 20260703 20260704 \
  --output-json artifacts/source_level_tempered_smc.json \
  --output-md artifacts/source_level_tempered_smc.md
```

Use more particles and independent seeds only after the base run is reproducible.
A larger particle count does not relax the interpretation boundary.
