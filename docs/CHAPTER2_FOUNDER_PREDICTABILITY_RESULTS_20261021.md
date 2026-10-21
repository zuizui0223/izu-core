# Can founding identity predict floral investment change?

## Question and analysis status

Exploratory reanalysis of existing stored states, not a new simulation or prospective confirmation. The [analysis specification](protocols/CHAPTER2_FOUNDER_PREDICTABILITY_20261021.md) was committed as `ab166dbc` before computing these scores; earlier aggregate results were known. [Reproducible results](audits/CHAPTER2_FOUNDER_PREDICTABILITY_20261021.json), [compact input matrices](audits/CHAPTER2_FOUNDER_PREDICTABILITY_MATRIX_20261021.npz) and [source receipts](audits/CHAPTER2_FOUNDER_PREDICTABILITY_MATRIX_20261021.json) accompany the reader.

The primary target was I change from census 0 to 80 under evolving assurance at B8. All 25,600 crossings survive. One cell is held out at a time: founder-only prediction uses that founder's other 159 histories; history-only uses that visitor history's other 159 founders; additive prediction uses both identities. Skill is 1 minus squared prediction error divided by that of a leave-cell-out intercept. Negative skill means worse prediction than the intercept. This is conditional prediction for new pairings of observed sources, not prediction from initial traits alone or for a newly encountered founder.

## Result: founder identity alone did not predict floral change

| I outcome / policy | Founder-only error reduction | Visitor-history-only | Additive |
|---|---:|---:|---:|
| Change, evolving A (primary) | −0.459% | +0.359% | −0.093% |
| Change, fixed A | −0.620% | +0.413% | −0.202% |
| Endpoint, evolving A (sensitivity) | +0.939% | +0.337% | +1.300% |
| Endpoint, fixed A (sensitivity) | +0.740% | +0.391% | +1.152% |

**Headline supported by the primary analysis:** across these 160 founders and 160 visitor histories, knowing a founder's performance in other histories did not improve prediction of its floral investment change in a held-out pairing.

This contradicts a strong founder-main-effect interpretation for this particular outcome and design. It does not contradict structural genetic constraints or prove that founder genotype has no influence. Nonlinear genotype-by-history effects may remain large; repeated realizations of each pairing are absent. Initial founder distributions were generated under one design, not sampled across the diversity of natural colonists. Visitor histories vary assemblage identity under the imposed count schedule, not every ecological dimension of environment.

## What the unexplained component means

For evolving-A I change, descriptive sums of squares allocate 0.785% to founder marginals, 1.593% to history marginals, and 97.622% to the combined interaction-plus-realization residual. Fixed-A values are 0.626%, 1.646%, and 97.728%. These in-sample fractions differ from held-out prediction skill. **The residual is not a measured fraction caused by chance, drift, or founder-by-environment interaction separately.** No four-way decomposition is possible from one observation per crossed treatment cell.

Mandatory secondary comparisons: for evolving M change, history-only skill is 40.146% and additive skill 40.011%; founder-only skill is −0.642%. For evolving A change, all three skills are negative (founder −0.583%, history −0.494%, additive −1.083%). These are secondary results, not substitutes for the primary I outcome. Low prediction skill concerns variation between outcomes, not their absolute dispersion: it cannot establish that A is more stochastic than I or negate concentration of A endpoints.

## Consequence for the manuscript

Keep two propositions separate: founding state bounds what is genetically possible, but founder identity need not predict how much I changes across visitor histories. The evidence does not support the headline that a particular percentage is determined by founders and the remainder by chance. Instead, the result narrows predictability: broad source main effects provided little held-out skill for I in this cohort, while visitor matching M had a clearer history-associated signal. This is consistent with the broader manuscript distinction between selective direction, finite realization and retained genetic options, but is not proof of the mechanism behind their differences.

No confidence interval or p-value is supplied: leave-cell predictions share training data, and this is a finite-design exploratory prediction score. Natural islands, unseen source distributions, trait plasticity, speciation and recolonization success are outside its prediction target.

## Reproduction and checks

The original [artifact run](https://github.com/zuizui0223/izu-core/actions/runs/39226906489) supplies 32 output shards. All receipts were checked against tracked original source archive hashes, the producer script hash, and each shard's bytes. Coordinates cover each of the 25,600 pairs exactly once; B8 survival and initial-mean consistency were checked. The stored means include latent A in the fixed policy; no fixed-A response score is reported.

Run `python scripts/analyze_founder_predictability_20261021.py --matrix docs/audits/CHAPTER2_FOUNDER_PREDICTABILITY_MATRIX_20261021.npz --output result.json` to reproduce the scores from the compact matrices after hash verification. Archive extraction additionally takes `--archive PATH`.

Unit checks compare PRESS to explicit least-squares refits, pure founder/history signals, constant outcomes, interaction-only matrices, permutation/offset invariance, invalid input and rejected provenance. No original raw biological trajectory was newly simulated or replayed.

## Why M and I may differ

In the producer, visitor optima are sampled between 0.3 and 0.7. All histories share six visitors before update 5, one retained visitor through update 34, and none from update 35. The affinity kernel is `(0.1 + I) * exp(-((M - optimum)/breadth)**2)`: M changes match to a history-specific optimum, whereas I scales investment while paying allocation costs. Thus the sampled history axis directly changes the matching landscape; it does not independently vary all environmental determinants of I. Census80 reflects a legacy after visitors disappear. This is a source-based mechanistic interpretation, not a tested mediation of the 40.15% versus 0.36% skill contrast. No claim of universal M predictability, phenotypic plasticity, or pure I drift follows. Sources: [production schedule](../scripts/q3_production160_20261019.py), [visitor construction](../scripts/q3_native_runner_20261019.py), [reproduction kernel](../scripts/model3_island/reproduction.py).

Independent review verified all shard receipt hashes, coordinate coverage, occupancy and exact compact-matrix agreement, and independently reproduced the primary founder score. Initial I spans approximately 0.46875–0.52474, so the result concerns a restricted founding distribution.
