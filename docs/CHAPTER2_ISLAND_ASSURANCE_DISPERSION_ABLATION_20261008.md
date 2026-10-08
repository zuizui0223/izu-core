# The assurance-dispersion ablation: terminal model inference boundary (2026-10-08)

**Status:** completed 3,072-trajectory, *post-outcome exploratory* technical assay. This is **not** new independent ecological replication or an identification of a genetic-variance causal mechanism.

## Question and genetic intervention

The previous 16-history allele-distribution transplant showed that an adjustment largely targeting the **population mean** of reproductive-assurance alleles reproduced the immediate viable maternal return of a full donor genotype transfer almost exactly. Some 80-reproductive-update occupancy differences persisted. This experiment asks whether the latter require the **within-population dispersion of the assurance locus**, conditional on the same evolved mean.

For each of four *previously exposed* visitor histories, all four reproductive settings and both near/far genetic backgrounds, we performed
`A_new = mean(A) + q * (A - mean(A))`
on both diploid copies of the assurance locus. The declared `q = 0, 0.5, 1` gives identical mean A and initial A-allele variance `0%, 25%, 100%` of its original value. `q=1` is the exact native genotype control. We crossed the three interventions with mutation probability 0 or .01, postvisitor histories near or far, synthetic ovule budgets 3 or 4, and four postshock demographic RNG repeats, for 3,072 complete trajectories. At `q=0` and mutation=0, all surviving populations retained zero A variance.

**Crucial distinction:** rescaling A by `q` also rescales its covariance with matching and floral investment, and therefore does **not** isolate standing variation from genetic association. The mutation=0 treatment suppresses new mutation at *all three* loci, not merely assurance. The carrying capacity is 8, no immigration is admitted and the budgets were informed by previously exposed exploratory outcomes.

## Complete four-setting results

Absolute 80-update occupancy rates, separated by historical recipient background and postshock mutation probability. The three values in each cell are `q=0 / q=0.5 / q=1`. Each row has 64 trajectories per q (four visitor histories × two future pollination environments × two budgets × four nested postshock RNG replicates).

| Setting | Recipient | Mutation | q=0 | q=.5 | q=1 | q0−q1 (percentage points) |
|---|---|---:|---:|---:|---:|---:|
| Delayed control | Near | 0 | .4375 | .4375 | .4375 | 0.00 |
| Delayed control | Far | 0 | .9531 | .9531 | .9531 | 0.00 |
| Delayed control | Near | .01 | .4531 | .4375 | .4375 | +1.56 |
| Delayed control | Far | .01 | .9375 | .9375 | .9375 | 0.00 |
| Prior selfing | Near | 0 | .5625 | .5938 | .5625 | 0.00 |
| Prior selfing | Far | 0 | .7656 | .7656 | .7188 | +4.69 |
| Prior selfing | Near | .01 | .5781 | .5781 | .6094 | −3.13 |
| Prior selfing | Far | .01 | .7656 | .7656 | .7500 | +1.56 |
| Pollen discount | Near | 0 | .5313 | .5156 | .5000 | +3.13 |
| Pollen discount | Far | 0 | .7344 | .7344 | .7500 | −1.56 |
| Pollen discount | Near | .01 | .4531 | .5313 | .5156 | −6.25 |
| Pollen discount | Far | .01 | .7344 | .7188 | .6875 | +4.69 |
| Assurance cost | Near | 0 | .0469 | .0469 | .0469 | 0.00 |
| Assurance cost | Far | 0 | .0625 | .0781 | .0469 | +1.56 |
| Assurance cost | Near | .01 | .0469 | .0469 | .0625 | −1.56 |
| Assurance cost | Far | .01 | .0781 | .0625 | .0469 | +3.13 |

**Direct raw comparison across the complete factorial:** `q0` and `q1` had different binary terminal occupancy in **43 of 1,024 matched condition sets**. The zero-dispersion state survived when the native state did not in 24 cases, while the native state survived when zero dispersion did not in 19. The equally weighted overall occupancy contrast was **+0.0048828125**, i.e., +0.49 percentage points for `q=0` versus `q=1`. The intermediate `q=.5` versus `q=1` comparison yielded 43 discordant pairs with 26 versus 17 signed outcomes, and an overall +0.88-point descriptive contrast.

Within-setting (pooling backgrounds and mutation arms), the zero-vs-native occupancy difference was delayed +0.39 points, prior +0.78 points, pollen-discount **0.00** points, costly +0.78 points. These are **descriptive** values nested within only four reused independent visitor histories. The near-zero pooled mean is *not* equivalence evidence: most terminal outcomes may be at demographic survival/extinction ceilings, and weak differences can be masked by stochastic parent/recruitment draws.

## Mechanistic conclusion and stop line

1. The *instantaneous maternal viable seed accounting* is strongly associated with assurance mean in this model. This is a predictable consequence of the model's mating and cost equations, not novel empirical evidence by itself.
2. The observed terminal population result varies with mutation supply, demographic RNG, background and mating system. This exploratory A-locus dispersion intervention shows **no stable, general gain from retaining standing assurance dispersion** under the declared eight-individual demographic shock.
3. A distinct, small residual in the full-donor versus bounded mean-target comparison remains compatible with genetic variance, covariance, allele ranking and stochastic recruitment effects. **No separate variance-only mechanism is identified** and we do not reinterpret the earlier frozen independent16 donor-effect test as successful.
4. Stop the cycle of tuning small synthetic grids to make a desired persistence effect. Next scientific priority for the island paper is an independent observational confrontation: distinguish **colonization filtering** from **post-establishment lineage evolution**, measure realized viable selfing, outcross maternal and paternal returns, and test a predeclared divergence-masking prediction in natural island systems. The current abstract floral-investment scale cannot be retrofitted to actual corolla size, colour or island kilometres.

## Evidence and reproducibility

- Pre-execution declared exploratory design: `data/design/chapter2_island_assurance_dispersion_ablation_20261008.json`
- Machine-readable all-setting result: `data/results/chapter2_island_assurance_dispersion_ablation_20261008.json`
- Replayers: `scripts/run_chapter2_island_assurance_dispersion_ablation.py`, `scripts/summarize_chapter2_island_assurance_dispersion_ablation.py`
- Review archive: `izu_core_island_assurance_dispersion_ablation_20261008.zip` SHA256 `dd3effcd0c2043e2dbb386587dfe653456c8a6cd87f41d66b5541d06f2e7a646`. Four raw shard SHA256 digests are locked in the result JSON, and the original biology source snapshot is kept in the local archive. This ZIP is **not** a DOI-backed deposit.
- Isolated manual GitHub Actions workflow `.github/workflows/chapter2-island-assurance-dispersion-ablation.yml` verifies the complete all-setting grid and demands numerical agreement with frozen descriptive readout. Do not claim GitHub Actions replay succeeded before job completion.
- The established primary four-setting confirmation in merged PR #411, the failed independent64 payoff all-five gate, failed independent16 priority gate and failed independent16 donor-transfer between-setting gate retain their original labels. **PR #413 stays Draft** and the Ecology Letters active manuscript stays unchanged.
