# Source-level island likelihood

## Why this is the next step

`island_multichannel` was built as a conservative integration layer over one
summary per island.  That is useful for a first compatibility map, but it
collapses information already available in the direct Inoue table
transcriptions:

- Oshima has two reported outcrossing estimates;
- Niijima has two reported outcrossing estimates;
- Hachijo has three reported outcrossing estimates;
- each outcrossing row has a reported SD and, usually, an accompanying n;
- bagging is recorded as flowers and capsules set, not merely a rounded percent;
- common-garden flower length has an SD and n that differs sharply among islands.

This module preserves those rows. It does **not** pretend that they are raw
individual data or that the papers constitute repeated modern samples.

## Retained observation models

### Outcrossing

For a population-level reported estimate `t`, the model uses a normal likelihood
on the logit scale:

\[
\operatorname{logit}(t_{ij}) \sim
\mathcal{N}\left(\operatorname{logit}(\hat t_i),\;
\sqrt{\operatorname{SE}_{ij}^2 + \sigma_{t,\mathrm{resid}}^2}\right).
\]

`SE` is a delta-method approximation from the reported SD and n. A nonzero
residual term remains because a fixation-index-derived `t` is not a binomial
count of independently sampled seeds. Where the source does not report an SD,
the model uses a declared conservative substitute rather than inventing
precision.

### Bagged capsule set

For `k` capsules set among `n` bagged flowers, the model uses a beta-binomial
likelihood:

\[
k_i \sim \operatorname{BetaBinomial}(n_i,\; p_i,\; \kappa).
\]

This avoids treating 100% in a historical table as a literal population
probability of one. `kappa` is deliberately fixed and must be sensitivity-tested;
the one historical experiment does not identify its own overdispersion.

### Flower length

For a reported mean flower length with SD and n:

\[
\bar L_i \sim \mathcal{N}\left(\hat L_i,\;
\sqrt{SD_i^2/n_i + \sigma_{L,\mathrm{population}}^2}\right).
\]

The between-population term prevents a large experimental n from silently
eliminating biological or source-level heterogeneity.

### Guide/spot direction

The guide channel is the same review-gated ordered comparison used by the island
summary model. It stays absent until a source-locatable comparison is reviewed.

## Run

```bash
python scripts/run_source_level_island_analysis.py \
  --output-json artifacts/source_level_island_analysis.json \
  --output-md artifacts/source_level_island_analysis.md
```

The runner uses the existing source-locked inputs:

```text
data/two_breakpoint_evidence/inoue1990_outcrossing.csv
data/two_breakpoint_evidence/inoue1988_bagging.csv
data/two_breakpoint_evidence/inoue1995_flower_length.csv
```

It writes full-evidence and leave-one-channel-out rankings.

## Interpretation

The source-level result may differ from the island-summary result. That is not a
contradiction: it quantifies how much the original ranking depended on collapsing
populations and experiments into a single number per island.

A scenario is not supported merely because it ranks first. The minimum reporting
set is:

1. all likelihood scales and prior ranges;
2. source-level versus island-summary ranking;
3. channel-ablation ranking;
4. sensitivity to beta-binomial concentration and the outcrossing residual;
5. the explicit statement that visitor regimes are availability/context evidence,
   not direct estimates of effective pollination.
